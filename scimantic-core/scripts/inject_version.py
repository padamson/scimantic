#!/usr/bin/env python3
import re
import yaml


def get_version(schema_path):
    with open(schema_path, "r") as f:
        data = yaml.safe_load(f)
    return data.get("version", "0.0.0")


def ensure_newline(file_path):
    with open(file_path, "r") as f:
        content = f.read()
    if not content.endswith("\n"):
        content += "\n"
        with open(file_path, "w") as f:
            f.write(content)
        print(f"Added missing newline to {file_path}")


def update_widoco_conf(file_path, version):
    with open(file_path, "r") as f:
        content = f.read()

    # Update ontologyRevisionNumber
    content = re.sub(
        r"ontologyRevisionNumber=.*", f"ontologyRevisionNumber={version}", content
    )

    # Update ontologyNamespaceURI (ensure NO trailing slash as per release script expectation)
    content = re.sub(
        r"ontologyNamespaceURI=.*",
        "ontologyNamespaceURI=https://scimantic.io/",
        content,
    )

    with open(file_path, "w") as f:
        f.write(content)
    print(f"Updated {file_path} with version {version}")


def update_ttl(file_path, version, is_shacl=False):
    with open(file_path, "r") as f:
        original_content = f.read()
    content = original_content

    # Define the new properties
    if is_shacl:
        base_name = "shacl/scimantic-shapes.ttl"
    else:
        base_name = "ontology.ttl"

    version_iri = f"<http://scimantic.io/v/{version}/{base_name}>"
    version_info = f'"{version}"'

    # Check if owl:Ontology exists
    # Pattern to match the Ontology declaration block
    # It usually ends with a dot .
    # We look for 'a owl:Ontology ;'

    ontology_pattern = re.compile(r"(\s+a owl:Ontology ;)", re.MULTILINE)

    match = ontology_pattern.search(content)
    if not match:
        if is_shacl:
            print(f"Creating new owl:Ontology block for {file_path}")

            # 1. Ensure owl prefix exists
            if "@prefix owl:" not in content:
                # Insert after last prefix or at top
                prefix_def = "@prefix owl: <http://www.w3.org/2002/07/owl#> .\n"
                last_prefix = re.search(r"@prefix .*\n", content)
                if last_prefix:
                    # Insert after the last detected prefix
                    # We find the *last* occurrence of a prefix line to keep them grouped
                    all_prefixes = list(
                        re.finditer(r"^@prefix .* \.$", content, re.MULTILINE)
                    )
                    if all_prefixes:
                        end_pos = all_prefixes[-1].end()
                        content = (
                            content[:end_pos] + "\n" + prefix_def + content[end_pos:]
                        )
                    else:
                        content = prefix_def + content
                else:
                    content = prefix_def + content

            # 2. Append ontology block
            # Use specific IRI for shapes file as subject
            # This matches release-ontology.yml expectations
            ontology_subject = "<http://scimantic.io/shacl/scimantic-shapes.ttl>"

            new_block = f"""
{ontology_subject} a owl:Ontology ;
    owl:versionIRI {version_iri} ;
    owl:versionInfo {version_info} .
"""
            content += new_block

            # Write immediately and return (skip regex replacement logic)
            with open(file_path, "w") as f:
                f.write(content)
            print(
                f"Updated {file_path} with new ontology definition and version {version}"
            )
            return

        else:
            print(f"Warning: No owl:Ontology definition found in {file_path}")
            ensure_newline(file_path)
            return

    # --------------------------------------------------------------------------
    # FIX: Ensure main ontology has correct subject (e.g. <http://scimantic.io/>)
    # instead of LinkML generated default/ID-based subject
    # --------------------------------------------------------------------------
    if not is_shacl:
        # Search for subject preceding 'a owl:Ontology'
        # Generated: scimantic:schema.owl.ttl ... a owl:Ontology ;
        # Desired: <http://scimantic.io/> ... a owl:Ontology ;

        # We look for the subject token right before the owl:Ontology definition part
        # Note: In Turtle, it could be "SUBJECT a owl:Ontology" or "SUBJECT\n ... ; a owl:Ontology"
        # Ideally we replace specifically the incorrect subject.

        # Pattern to find the subject at start of the block containing version info or just 'a owl:Ontology'
        # LinkML output example provided by user:
        # scimantic:schema.owl.ttl
        #    owl:versionIRI <...>; ... a owl:Ontology ;

        # We replace the specific known bad identifier if found
        bad_subject = "scimantic:schema.owl.ttl"
        good_subject = "<http://scimantic.io/>"

        if bad_subject in content:
            content = content.replace(bad_subject, good_subject)
            print(f"Fixed ontology subject: {bad_subject} -> {good_subject}")

    # Check if versionIRI already exists
    if "owl:versionIRI" in content:
        # Update existing
        content = re.sub(
            r"owl:versionIRI\s+<[^>]+>", f"owl:versionIRI {version_iri}", content
        )
    else:
        # Insert it
        replacement = f"\n    owl:versionIRI {version_iri} ;"
        content = ontology_pattern.sub(f"{replacement}\\1", content)

    # Also ensure pav:version is correct if present
    if "pav:version" in content:
        content = re.sub(
            r'pav:version\s+"[^"]+"', f"pav:version {version_info}", content
        )

    # Ensure trailing newline for end-of-file-fixer parity
    if not content.endswith("\n"):
        content += "\n"

    if content == original_content:
        # print(f"No changes needed for {file_path}")
        return

    with open(file_path, "w") as f:
        f.write(content)
    print(f"Updated {file_path} with version {version}")


if __name__ == "__main__":
    schema_path = "schema/scimantic.yaml"
    ontology_path = "ontology/scimantic.ttl"
    shacl_path = "ontology/shacl/scimantic-shapes.ttl"
    widoco_conf_path = "ontology/widoco.conf"

    version = get_version(schema_path)
    print(f"Injecting version {version}...")

    update_ttl(ontology_path, version, is_shacl=False)
    update_ttl(shacl_path, version, is_shacl=True)
    update_widoco_conf(widoco_conf_path, version)

    # Also ensure models.py has a trailing newline
    models_path = "src/scimantic/models.py"
    ensure_newline(models_path)
