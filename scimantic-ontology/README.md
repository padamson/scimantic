# Scimantic Ontology

This package contains the **Scimantic domain ontology** — a semantic specification for representing the scientific method as provenance chains.

## Structure

```
scimantic-ontology/
├── schema/
│   └── scimantic.yaml       # LinkML schema (source of truth)
├── generated/               # Generated artifacts (do not edit directly)
│   ├── scimantic.ttl        # OWL ontology
│   ├── shacl/
│   │   └── scimantic-shapes.ttl  # SHACL validation shapes
│   └── widoco.conf          # Documentation configuration
└── scripts/
    └── inject_version.py    # Version injection for releases
```

## Source of Truth

The **LinkML schema** (`schema/scimantic.yaml`) is the single source of truth for the ontology. All other artifacts are generated from it.

## Generated Artifacts

Generated artifacts are committed to version control to ensure:
- Reproducible builds
- CI validation without regeneration
- Easy inspection of changes via git diff

**Do not edit generated files directly.** Instead:
1. Edit `schema/scimantic.yaml`
2. Run `uv run gen-all` from `scimantic-core/`
3. Commit both the schema change and regenerated artifacts

## Regenerating Artifacts

From the `scimantic-core/` directory:

```bash
uv run gen-all
```

This generates:
- `generated/scimantic.ttl` — OWL ontology
- `generated/shacl/scimantic-shapes.ttl` — SHACL validation shapes
- `scimantic-core/src/scimantic/models.py` — Python dataclasses

## Documentation

Ontology documentation is generated using [Widoco](https://github.com/dgarijo/Widoco) and published to [scimantic.io](https://scimantic.io).

To build documentation locally:

```bash
./scripts/build-docs.sh
```

## Future: Panschema

This ontology package is designed to eventually be built with [panschema](https://github.com/padamson/panschema), a Rust-based tool for ontology documentation and publishing. The Python tooling (`gen-all`) will be retained until panschema supports all required features.

## License

CC-BY 4.0 — See `schema/scimantic.yaml` for details.
