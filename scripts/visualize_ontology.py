import rdflib
from rdflib import RDF, RDFS, OWL, Namespace, BNode
import subprocess
import shutil

# Namespaces
SCIMANTIC = Namespace("http://scimantic.io/")
PROV = Namespace("http://www.w3.org/ns/prov#")

def generate_mermaid():
    g = rdflib.Graph()
    g.parse("scimantic-core/ontology/scimantic.ttl", format="turtle")

    entities = []
    activities = []
    relations = []

    # Helper to get refined local name
    def get_name(uri):
        if not uri: return ""
        if "#" in str(uri):
            return str(uri).split("#")[-1]
        return str(uri).split("/")[-1]

    # 1. Identify Classes
    for s in g.subjects(RDF.type, OWL.Class):
        if str(s).startswith(str(SCIMANTIC)):
            name = get_name(s)

            is_entity = False
            is_activity = False

            # Simple hierarchy check
            parents = list(g.objects(s, RDFS.subClassOf))

            if PROV.Entity in parents:
                is_entity = True
            elif PROV.Activity in parents:
                is_activity = True
            else:
                for p in parents:
                    if (p, RDFS.subClassOf, PROV.Entity) in g:
                        is_entity = True
                    if (p, RDFS.subClassOf, PROV.Activity) in g:
                        is_activity = True

            if is_entity:
                entities.append(name)
            elif is_activity:
                activities.append(name)

    # Explicitly include external URREF classes as Entities
    # This ensures UncertaintyModel appears inside the "Entities" box
    if "UncertaintyModel" not in entities:
        entities.append("UncertaintyModel")

    # 2. Extract Relationships from OWL Restrictions AND Domain/Range

    # Mapping Predicates to Vision Strings
    # Key: Tuple(Label, IsInverse)
    # IsInverse = True means we draw Target -> Source (Activity Flow)
    # IsInverse = False means we draw Source -> Target (Dependence/Derivation)
    pred_map = {
        PROV.wasGeneratedBy: ("generates", True), # Entity -> Activity (genBy) => Activity -> Entity
        PROV.used: ("input to", True),            # Activity -> Entity (used)  => Entity -> Activity
        PROV.wasInformedBy: ("informs", True),    # A2 -> A1 (informedBy)      => A1 -> A2

        # Provenance & Discourse (Source -> Target)
        PROV.wasDerivedFrom: ("derives from", False), # E2 -> E1 (derivedFrom) => E2 -> E1
        SCIMANTIC.motivates: ("motivates", False),
        SCIMANTIC.supports: ("supports", False),
        SCIMANTIC.contradicts: ("contradicts", False),
        SCIMANTIC.refines: ("refines", False),
        SCIMANTIC.parameter: ("parameter", False), # ExperimentalMethod -> Parameter

        # Uncertainty
        SCIMANTIC.hasUncertainty: ("has uncertainty", False)
    }

    # Set of unique relation strings to avoid duplicates
    relations_set = set()

    # A. From Restrictions
    subjects = [s for s in g.subjects(RDF.type, OWL.Class) if str(s).startswith(str(SCIMANTIC))]
    for s in subjects:
        source_name = get_name(s)
        for bn in g.objects(s, RDFS.subClassOf):
            if isinstance(bn, BNode):
                if (bn, RDF.type, OWL.Restriction) in g:
                    prop = g.value(bn, OWL.onProperty)
                    target = g.value(bn, OWL.allValuesFrom)
                    if not target: current = g.value(bn, OWL.someValuesFrom); target = current

                    if target and (str(target).startswith(str(SCIMANTIC)) or str(target).startswith(str(PROV)) or "URREF" in str(target)):
                        target_name = get_name(target)
                        if prop in pred_map:
                            label, is_inverse = pred_map[prop]
                            if is_inverse:
                                relations_set.add(f"{target_name} -. {label} .-> {source_name}")
                            else:
                                relations_set.add(f"{source_name} -. {label} .-> {target_name}")

    # B. From Domain/Range properties
    for p in g.subjects(RDF.type, OWL.ObjectProperty):
        if p in pred_map:
            label, is_inverse = pred_map[p]

            # Get Domain(s)
            domains = []
            for d in g.objects(p, RDFS.domain):
                if isinstance(d, BNode):
                    union = g.value(d, OWL.unionOf)
                    if union:
                        current = union
                        while current != RDF.nil:
                            first = g.value(current, RDF.first)
                            domains.append(get_name(first))
                            current = g.value(current, RDF.rest)
                else:
                    domains.append(get_name(d))

            # Get Range(s)
            ranges = []
            for r in g.objects(p, RDFS.range):
                ranges.append(get_name(r))

            for source_name in domains:
                for target_name in ranges:
                    if not source_name or not target_name: continue

                    # Filter out generic PROV classes
                    if target_name in ["Activity", "Entity", "Plan", "Agent", "Bundle"]: continue
                    if source_name in ["Activity", "Entity", "Plan", "Agent", "Bundle"]: continue

                    if is_inverse:
                        relations_set.add(f"{target_name} -. {label} .-> {source_name}")
                    else:
                        relations_set.add(f"{source_name} -. {label} .-> {target_name}")

    # Build Mermaid
    lines = ["graph TB"]

    # Master Subgraph
    lines.append('    subgraph Scimantic_Ontology ["Scimantic Ontology Flow"]')
    lines.append('    direction TB')

    # Subgraph Entities
    lines.append('        subgraph Entities ["Entities (Things)"]')
    lines.append('        direction TB')
    for e in entities:
        lines.append(f'            {e}[{e}]')
    lines.append('        end')

    # Subgraph Activities
    lines.append('        subgraph Activities ["Activities (Processes)"]')
    lines.append('        direction TB')
    for a in activities:
        lines.append(f'            {a}[{a}]')
    lines.append('        end')

    lines.append('    end') # End Master

    # Relations (outside subgraphs to allow cross-linking freely)
    for r in sorted(list(relations_set)):
        lines.append(f'    {r}')

    # Styles
    # Entity Zone: Light Blue, Activity Zone: Light Gray
    lines.append('    style Scimantic_Ontology fill:#ffffff,stroke:#333,stroke-width:2px,color:black;')
    lines.append('    style Entities fill:#eff6ff,stroke:#2563eb,stroke-width:1px,color:black,stroke-dasharray: 5 5;')
    lines.append('    style Activities fill:#f9fafb,stroke:#4b5563,stroke-width:1px,color:black,stroke-dasharray: 5 5;')

    # Node Styles
    # Entity Nodes: White with Blue border
    lines.append('    classDef entity fill:#ffffff,stroke:#2563eb,stroke-width:2px,color:black;')
    # Activity Nodes: White with Gray border (Rounded)
    lines.append('    classDef activity fill:#ffffff,stroke:#4b5563,stroke-width:2px,color:black,rx:5,ry:5;')

    if entities:
        lines.append(f'    class {",".join(entities)} entity;')
    if activities:
        lines.append(f'    class {",".join(activities)} activity;')

    mermaid_content = "\n".join(lines)

    # Write Mermaid source
    mmd_content = f"%%{{init: {{'theme': 'base', 'themeVariables': {{'primaryColor': '#ffffff', 'edgeLabelBackground':'#ffffff', 'tertiaryColor': '#ffffff'}} }} }}%%\n{mermaid_content}"

    with open("ontology_graph.mmd", "w") as f:
        f.write(mmd_content)

    print("Generated ontology_graph.mmd")

    # Generate PNG using mmdc with WHITE background
    cmd = ["npx", "@mermaid-js/mermaid-cli", "-i", "ontology_graph.mmd", "-o", "ontology_graph.png", "-b", "white"]

    try:
        print("Running mmdc to generate PNG...")
        subprocess.run(cmd, check=True)
        print("Generated ontology_graph.png")
    except subprocess.CalledProcessError as e:
        print(f"Error generating PNG: {e}")
    except FileNotFoundError:
        print("Error: npx not found. Please ensure Node.js is installed.")

if __name__ == "__main__":
    generate_mermaid()
