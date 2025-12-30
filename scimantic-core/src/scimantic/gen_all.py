import subprocess
import sys
import os
from pathlib import Path

# Constants
SCHEMA_PATH = Path("schema/scimantic.yaml")
PYTHON_DEST = Path("src/scimantic/models.py")
ONTOLOGY_DEST = Path("ontology/scimantic.ttl")
SHACL_DEST = Path("ontology/shacl/scimantic-shapes.ttl")
WIDOCO_CONF = Path("ontology/widoco.conf")


def run_command(command, cwd=None, env=None, shell=True):
    """
    Runs a shell command and raises an error if it fails.
    """
    try:
        subprocess.run(
            command,
            cwd=cwd,
            env=env,
            shell=shell,
            check=True,
            capture_output=False,  # Stream output to stdout
        )
    except subprocess.CalledProcessError:
        print(f"❌ Command failed: {command}")
        sys.exit(1)


def remove_timestamp(file_path: Path):
    """
    Removes the generation timestamp from the file to ensure deterministic content.
    """
    if not file_path.exists():
        return

    with open(file_path, "r") as f:
        content = f.read()

    lines = content.splitlines(keepends=True)

    # Filter out the specific generation date line produced by gen-python
    new_lines = [
        line for line in lines if not line.strip().startswith("# Generation date:")
    ]

    # Reconstruct content with strictly one newline at end
    new_content = "".join(new_lines).rstrip() + "\n"

    # Only write if changed
    if content != new_content:
        print(f"Removed timestamp from {file_path}")
        with open(file_path, "w") as f:
            f.write(new_content)


def determinize_ttl(file_path: Path):
    """
    Parses a TTL file, canonicalizes BNodes, and re-serializes deterministically.
    Uses a fresh graph to ensure clean namespace bindings.
    """
    try:
        import rdflib
        from rdflib.compare import to_canonical_graph
    except ImportError:
        print("⚠️  Warning: rdflib not installed. Skipping deterministic serialization.")
        return

    print(f"Determinizing {file_path}...")
    g = rdflib.Graph()
    try:
        g.parse(file_path, format="turtle")

        # 1. Canonicalize (Stable BNodes)
        g_canonical = to_canonical_graph(g)

        # 2. Fresh Graph (Clean Namespaces)
        # We copy triples to a new graph to drop all random 'ns1', 'ns2' bindings from recursion/LinkML
        g_final = rdflib.Graph()
        for triple in g_canonical:
            g_final.add(triple)

        # 3. Explicit Bindings (Consistent Prefixes)
        g_final.bind("scimantic", "http://scimantic.io/")
        g_final.bind("owl", "http://www.w3.org/2002/07/owl#")
        g_final.bind("prov", "http://www.w3.org/ns/prov#")
        g_final.bind("dcterms", "http://purl.org/dc/terms/")
        g_final.bind("sh", "http://www.w3.org/ns/shacl#")
        g_final.bind("linkml", "https://w3id.org/linkml/")
        g_final.bind("pav", "http://purl.org/pav/")
        g_final.bind("xsd", "http://www.w3.org/2001/XMLSchema#")
        g_final.bind(
            "urref",
            "https://raw.githubusercontent.com/adelphi23/urref/469137/URREF.ttl#",
        )

        # 4. Sort SHACL Lists (sh:ignoredProperties)
        # LinkML output has random order for ignoredProperties lists.
        # We must sort them in the graph to ensure structural determinism.
        SH_IGNORED = rdflib.URIRef("http://www.w3.org/ns/shacl#ignoredProperties")

        # Find all ignoredProperties lists
        list_triples = []
        for s, p, o in g_final.triples((None, SH_IGNORED, None)):
            list_triples.append((s, p, o))

        for s, p, o in list_triples:
            try:
                # Extract items
                c = rdflib.collection.Collection(g_final, o)
                items = list(c)
                if not items:
                    continue

                # Sort items by their string representation/URI
                sorted_items = sorted(items, key=lambda x: str(x))

                # If order changed, reconstruct
                if items != sorted_items:
                    c.clear()
                    for item in sorted_items:
                        c.append(item)
            except Exception:
                # List sorting might fail if list is malformed, just ignore
                pass

        # 5. Serialize
        ttl_content = g_final.serialize(format="turtle", sort_keys=True)

        # Strict newline enforcement
        ttl_content = ttl_content.rstrip() + "\n"

        with open(file_path, "w") as f:
            f.write(ttl_content)
    except Exception as e:
        print(f"⚠️  Warning: Failed to determinize {file_path}: {e}")


def main():
    """
    Generates all ontology artifacts: Python models, OWL, and SHACL.
    Acts as a python entry point for `gen-all`.
    """

    # Check if we are in the right directory
    if not SCHEMA_PATH.exists():
        print(
            "Error: schema/scimantic.yaml not found. Please run this command from the scimantic-core directory."
        )
        sys.exit(1)

    print("Generating artifacts...")

    # 1. Generate Python Models
    print("Running gen-python...")
    run_command(f"uv run gen-python {SCHEMA_PATH} > {PYTHON_DEST}")
    # Remove timestamp immediately
    remove_timestamp(PYTHON_DEST)

    # 2. Generate OWL Ontology
    print("Running gen-owl...")
    run_command(f"uv run gen-owl --no-metadata {SCHEMA_PATH} > {ONTOLOGY_DEST}")

    # 3. Generate SHACL Shapes
    print("Running gen-shacl...")
    run_command(f"uv run gen-shacl --no-metadata {SCHEMA_PATH} > {SHACL_DEST}")

    # 4. Determinize (Fixes random ordering)
    # This must happen BEFORE version injection if version injection relies on regex,
    # OR AFTER if we want to ensure the injected version isn't re-serialized strangely.
    # However, since inject_version does simple regex replacement, it's safer to determinize first
    # so the structure is stable, then inject the specific strings.
    determinize_ttl(ONTOLOGY_DEST)
    determinize_ttl(SHACL_DEST)

    # 5. Inject Version (Updates IRIs / headers)
    print("Injecting version...")
    run_command(f"{sys.executable} scripts/inject_version.py")

    # 6. Generate Ontology Graph
    print("Generating ontology graph...")
    root_dir = Path("..").resolve()
    script_path = root_dir / "scripts" / "visualize_ontology.py"

    if script_path.exists():
        # RUN in the root dir because visualize_ontology.py expects that context
        subprocess.run([sys.executable, str(script_path)], cwd=root_dir, check=True)
    else:
        print(f"⚠️  Warning: {script_path} not found. Skipping graph generation.")

    # 7. Generate Documentation (Public Folder)
    # Only run if not skipping
    if os.environ.get("SKIP_GEN_doc") != "true":
        print("Generating documentation (public folder)...")
        docs_script = root_dir / "scripts" / "build-docs.sh"
        if docs_script.exists():
            # Set environment variable to prevent recursion in case build-docs calls gen-all
            env = os.environ.copy()
            env["SKIP_GEN_ALL"] = "true"
            subprocess.run([str(docs_script)], cwd=root_dir, env=env, check=True)
        else:
            print(
                f"⚠️  Warning: {docs_script} not found. Skipping documentation generation."
            )

    print("✅ Successfully generated all artifacts.")


if __name__ == "__main__":
    main()
