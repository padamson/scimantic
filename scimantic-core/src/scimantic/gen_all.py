import subprocess
import sys
from pathlib import Path


def main():
    """
    Generates all ontology artifacts: Python models, OWL, and SHACL.
    Acts as a python entry point for `gen-all`.
    """

    # Check if we are in the right directory
    if not Path("schema/scimantic.yaml").exists():
        print(
            "Error: schema/scimantic.yaml not found. Please run this command from the scimantic-core directory."
        )
        sys.exit(1)

    print("Generating artifacts...")

    try:
        # 1. Generate Python Models
        # Using gen-python as observed in models.py header
        print("Running gen-python...")
        with open("src/scimantic/models.py", "w") as f:
            subprocess.run(
                ["gen-python", "schema/scimantic.yaml"], stdout=f, check=True
            )

        # 2. Generate OWL Ontology
        print("Running gen-owl...")
        with open("ontology/scimantic.ttl", "w") as f:
            subprocess.run(
                ["gen-owl", "--no-metadata", "schema/scimantic.yaml"],
                stdout=f,
                check=True,
            )

        # 3. Generate SHACL Shapes
        print("Running gen-shacl...")
        with open("ontology/shacl/scimantic-shapes.ttl", "w") as f:
            subprocess.run(
                ["gen-shacl", "--no-metadata", "schema/scimantic.yaml"],
                stdout=f,
                check=True,
            )

        # 4. Inject Version
        print("Injecting version...")
        subprocess.run([sys.executable, "scripts/inject_version.py"], check=True)

        # 5. Generate Ontology Graph
        print("Generating ontology graph...")
        # Note: visualize_ontology.py expects to run from the root scimantic/ directory
        # and looks for 'scimantic-core/ontology/scimantic.ttl'.
        # We assume gen_all.py runs from scimantic-core/, so we go up one level.
        root_dir = Path("..").resolve()
        script_path = root_dir / "scripts" / "visualize_ontology.py"

        if script_path.exists():
            subprocess.run([sys.executable, str(script_path)], cwd=root_dir, check=True)
        else:
            print(f"⚠️  Warning: {script_path} not found. Skipping graph generation.")

        print("✅ Successfully generated all artifacts.")

    except subprocess.CalledProcessError as e:
        print(f"❌ Error during generation: {e}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"❌ Command not found: {e}")
        print(
            "Ensure you are running in an environment with LinkML installed (uv run ...)."
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
