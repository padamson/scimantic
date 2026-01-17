import rdflib
from rdflib import RDF, RDFS, OWL, Namespace, BNode
import subprocess
from pathlib import Path

# Namespaces
SCIMANTIC = Namespace("http://scimantic.io/")
PROV = Namespace("http://www.w3.org/ns/prov#")
URREF = Namespace("https://raw.githubusercontent.com/adelphi23/urref/469137/URREF.ttl#")

def get_name(uri):
    if not uri: return ""
    if "#" in str(uri):
        return str(uri).split("#")[-1]
    return str(uri).split("/")[-1]

def generate_mermaid_v2():
    g = rdflib.Graph()
    g.parse("scimantic-core/ontology/scimantic.ttl", format="turtle")

    # --- Configuration: Explicit Include Lists & Order ---
    # These lists define WHAT is shown and the vertical ORDER (Rank).

    # 1. Activities (Processes) - Left Column
    ordered_activities = [
        "QuestionFormation",
        "LiteratureSearch",
        "EvidenceExtraction",
        "EvidenceAssessment",
        "HypothesisFormation",
        "DesignOfExperiment",
        "Experimentation",
        "Analysis",
        "ResultAssessment"
    ]

    # 2. Entities (Things) - Right Column(s)
    ordered_entities = [
        "Question",
        "Annotation",
        "Evidence",
        "Premise",
        "Hypothesis",
        "ExperimentalMethod",
        "Dataset",
        "Result",
        "Conclusion"
    ]

    # Combine for filtering
    allowed_nodes = set(ordered_activities + ordered_entities)

    # --- Predicate Mapping (Label, IsInverse) ---
    pred_map = {
        PROV.wasGeneratedBy: ("generates", True),
        SCIMANTIC.wasGeneratedBy: ("generates", True),
        PROV.used: ("input to", True),
        SCIMANTIC.used: ("input to", True),
        PROV.wasInformedBy: ("informs", True),
        SCIMANTIC.wasInformedBy: ("informs", True),
        PROV.wasDerivedFrom: ("derives from", False),
        SCIMANTIC.wasDerivedFrom: ("derives from", False),
        PROV.wasAssociatedWith: ("associated with", True),
        SCIMANTIC.wasAssociatedWith: ("associated with", True),
        SCIMANTIC.motivates: ("motivates", False),
        SCIMANTIC.supports: ("supports", False),
        SCIMANTIC.contradicts: ("contradicts", False),
        SCIMANTIC.refines: ("refines", False),
        SCIMANTIC.parameter: ("parameter", False),
        SCIMANTIC.hasUncertainty: ("has uncertainty", False)
    }

    # --- Helper: Get Union Members ---
    def get_union_members(class_uri):
        members = []

        # 1. Direct unionOf: class_uri owl:unionOf ?list
        for _, _, union_list_node in g.triples((class_uri, OWL.unionOf, None)):
             c = rdflib.collection.Collection(g, union_list_node)
             for member in c:
                 members.append(member)

        # 2. EquivalentClass union: class_uri owl:equivalentClass [ owl:unionOf ?list ]
        if not members:
            for _, _, bnode in g.triples((class_uri, OWL.equivalentClass, None)):
                for _, _, union_list_node in g.triples((bnode, OWL.unionOf, None)):
                    c = rdflib.collection.Collection(g, union_list_node)
                    for member in c:
                        members.append(member)
        return members

    # --- Extraction Cycle ---
    tuples = [] # List of (Source, Label, Target, SortKey)

    # Helper to add tuple
    def add_tuples(src, label, tgt):
        # Check if Target is a Union Class
        union_members = get_union_members(tgt)

        targets_to_add = []

        if union_members:
            # If target is a union, expand it!
            targets_to_add = union_members
        else:
            # Otherwise just use the target
            targets_to_add = [tgt]

        for final_tgt in targets_to_add:
            src_clean = get_name(src)
            tgt_clean = get_name(final_tgt)

            # Filter
            if src_clean not in allowed_nodes or tgt_clean not in allowed_nodes:
                continue

            # Explicit Sort Logic requested:
            is_entity_src = src_clean in ordered_entities
            src_index = 999
            if is_entity_src:
                src_index = ordered_entities.index(src_clean)
            elif src_clean in ordered_activities:
                src_index = ordered_activities.index(src_clean)

            # Tuple: (Source, Target, Label, IsInverseVisual)
            tuples.append({
                "src": src_clean,
                "tgt": tgt_clean,
                "label": label,
                "is_entity_src": is_entity_src,
                "src_index": src_index
            })

    # 1. From Restrictions
    # Iterate over all subjects in the graph (Classes)
    for s in g.subjects(RDF.type, OWL.Class):
        # Check for restrictions (subClassOf Restriction)
        for _, _, bnode in g.triples((s, RDFS.subClassOf, None)):
            if (bnode, RDF.type, OWL.Restriction) in g:
                # Get property
                prop = g.value(bnode, OWL.onProperty)
                if prop in pred_map:
                    mapped_label, is_inverse_visual = pred_map[prop]

                    # Get target (allValuesFrom, someValuesFrom, or onClass for cardinality)
                    # We usually look for allValuesFrom for strong links
                    target = g.value(bnode, OWL.allValuesFrom)
                    if not target: target = g.value(bnode, OWL.someValuesFrom) # Also check someValuesFrom

                    if target:
                        if isinstance(target, BNode):
                            # Handle Anonymous Union inside Restriction (legacy/any_of)
                            # [ owl:unionOf (...) ]
                            if (target, OWL.unionOf, None) in g:
                                # It's an anonymous union, expand members
                                members = get_union_members(target)
                                for m in members:
                                     # Determine visual direction
                                    if is_inverse_visual:
                                        add_tuples(m, mapped_label, s)
                                    else:
                                        add_tuples(s, mapped_label, m)
                            continue # Skip adding the BNode itself

                        # Normal named class target
                        if is_inverse_visual:
                            # Inverse: Property is "used" (s used target), visual label is "input to"
                            # We want visual edge: Target --[input to]--> S
                            add_tuples(target, mapped_label, s)
                        else:
                            # Normal: S -> Target
                            # For normal Named Classes, we just add the tuple.
                            # But wait, if 'target' is a list? No, here target is a single value from g.value
                            add_tuples(s, mapped_label, target)

    # 2. From Attributes (Domain/Range)
    for p in g.subjects(RDF.type, OWL.ObjectProperty):
        if p in pred_map:
            label, is_inverse = pred_map[p]
            # simplified domain/range check loop
            domains = []
            for d in g.objects(p, RDFS.domain):
                if isinstance(d, BNode):
                     # handle unionOf if simple
                     union = g.value(d, OWL.unionOf)
                     if union:
                         cur = union
                         while cur != RDF.nil:
                             domains.append(g.value(cur, RDF.first))
                             cur = g.value(cur, RDF.rest)
                else:
                    domains.append(d)

            ranges = [r for r in g.objects(p, RDFS.range)]

            for d in domains:
                for r in ranges:
                     if is_inverse:
                         add_tuples(r, label, d)
                     else:
                         add_tuples(d, label, r)

    # --- Sorting Order Strategy ---
    # User requested alternating between Activities and Entities to guide layout
    combined_sort_order = [
        "QuestionFormation",
        "Question",
        "LiteratureSearch",
        "Evidence",
        "EvidenceAssessment",
        "Premise",
        "HypothesisFormation",
        "Hypothesis",
        "DesignOfExperiment",
        "ExperimentalMethod",
        "Experimentation",
        "Dataset",
        "Analysis",
        "Result",
        "ResultAssessment",
        "Conclusion"
    ]

    # Helper for sort index
    def get_sort_index(node_name):
        if node_name in combined_sort_order:
            return combined_sort_order.index(node_name)
        return 999

    # --- Sorting ---
    # Sort tuples based on:
    # 1. Source node position
    # 2. Target node position (to prioritize closer connections)
    # 3. Label
    tuples.sort(key=lambda x: (
        get_sort_index(x["src"]),
        get_sort_index(x["tgt"]),
        x["label"],
        x["src"],
        x["tgt"]
    ))

    # --- Mermaid Generation ---
    lines = ["graph TB"]
    lines.append('    %% Subgraph Definitions using Explicit Lists')

    # --- Node Definitions & Vertical Backbone ---
    lines.append('    subgraph Scimantic_Ontology ["Scimantic Ontology Flow"]')
    lines.append('    direction TB')

    # 1. Entities (Now First / Left Column)
    lines.append('    subgraph Entities ["Entities (Things)"]')
    lines.append('    direction TB')
    for e in ordered_entities:
        lines.append(f'        {e}[{e}]')
    # Vertical Backbone
    for i in range(len(ordered_entities)-1):
        lines.append(f'        {ordered_entities[i]} ~~~ {ordered_entities[i+1]}')
    lines.append('    end') # Ends Entities

    # 2. Activities (Now Second / Right Column)
    lines.append('    subgraph Activities ["Activities (Processes)"]')
    lines.append('    direction TB')
    for a in ordered_activities:
        lines.append(f'        {a}[{a}]')
    # Vertical Backbone
    for i in range(len(ordered_activities)-1):
        lines.append(f'        {ordered_activities[i]} ~~~ {ordered_activities[i+1]}')
    lines.append('    end') # Ends Activities

    lines.append('    end') # Ends Scimantic_Ontology

    # Edges
    lines.append('    %% Relationships (Sorted)')
    unique_edges = set()

    for t in tuples:
        src = t["src"]
        tgt = t["tgt"]
        label = t["label"]

        # Deduplication key
        edge_key = f"{src}-{label}-{tgt}"
        if edge_key in unique_edges: continue
        unique_edges.add(edge_key)

        # Style
        # Forward flow: Solid, Feedback/Context: Dotted
        if label in ["generates", "motivates", "derives from", "input to", "parameter", "has uncertainty"]:
             arrow = "-->"
        else:
             arrow = "-.->"

        lines.append(f'    {src} {arrow}|{label}| {tgt}')

    # Apply Styles
    lines.append('    classDef entity fill:#ffffff,stroke:#2563eb,stroke-width:2px,color:black;')
    lines.append('    classDef activity fill:#ffffff,stroke:#4b5563,stroke-width:2px,color:black,rx:5,ry:5;')

    # Subgraph Styling
    lines.append('    style Entities fill:#f0f9ff,stroke:#bae6fd,stroke-width:2px,color:black')
    lines.append('    style Activities fill:#f3f4f6,stroke:#cbd5e1,stroke-width:2px,color:black')
    lines.append('    style Scimantic_Ontology fill:#ffffff,stroke:#94a3b8,stroke-width:2px,color:black')

    if ordered_entities:
        lines.append(f'    class {",".join(ordered_entities)} entity;')
    if ordered_activities:
        lines.append(f'    class {",".join(ordered_activities)} activity;')

    mmd_content = "\n".join(lines)

    # Tighter spacing configuration
    config = """%%{
  init: {
    'theme': 'base',
    'themeVariables': {
      'primaryColor': '#ffffff',
      'edgeLabelBackground': '#ffffff',
      'tertiaryColor': '#ffffff'
    },
    'flowchart': {
      'nodeSpacing': 40,
      'rankSpacing': 40
    }
  }
}%%"""

    # Compare with existing file to avoid unnecessary IO and binary churn
    output_mmd_path = Path("ontology_graph.mmd")
    output_png_path = Path("ontology_graph.png")

    full_new_content = f"{config}\n{mmd_content}"
    if not full_new_content.endswith("\n"):
        full_new_content += "\n"

    needs_regen = True
    if output_mmd_path.exists() and output_png_path.exists():
        with open(output_mmd_path, "r") as f:
            old_content = f.read()
        if old_content == full_new_content:
            needs_regen = False
            print("Graph definition unchanged. Skipping PNG generation.")

    if needs_regen:
        with open(output_mmd_path, "w") as f:
            f.write(full_new_content)
        print("Generated ontology_graph.mmd")

        # SVG/PNG Gen
        try:
            cmd = ["npx", "@mermaid-js/mermaid-cli", "-i", "ontology_graph.mmd", "-o", "ontology_graph.png", "-b", "white", "-s", "3"]
            print("Running mmdc...")
            subprocess.run(cmd, check=True)
            print("Generated ontology_graph.png")
        except Exception as e:
            print(f"Error running mmdc: {e}")
            if not output_png_path.exists():
                print("Warning: PNG generation failed and no stale PNG exists.")


if __name__ == "__main__":
    generate_mermaid_v2()
