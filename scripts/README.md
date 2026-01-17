# Scimantic Scripts

Utility scripts for development and documentation.

## Documentation Scripts

### `build-docs.sh`

Builds ontology documentation using [Widoco](https://github.com/dgarijo/Widoco).

```bash
./scripts/build-docs.sh
```

- Downloads Widoco JAR if not present (requires Java 17+)
- Generates HTML documentation from `scimantic-core/ontology/scimantic.ttl`
- Outputs to `public/` directory
- Uses configuration from `scimantic-core/ontology/widoco.conf`

### `preview-docs.sh`

Builds documentation and serves it locally for preview.

```bash
./scripts/preview-docs.sh
```

- Runs `build-docs.sh`
- Starts HTTP server at `http://localhost:8000`
- Press `Ctrl+C` to stop

### `watch-docs.sh`

Watches for schema changes and auto-rebuilds documentation.

```bash
./scripts/watch-docs.sh
```

- Monitors `scimantic-core/schema/` for changes
- Auto-rebuilds documentation when files change
- Serves at `http://localhost:8000`
- Useful during ontology development

## Visualization Scripts

### `visualize_ontology.py`

Generates a Mermaid diagram of the ontology.

```bash
cd scimantic-core && uv run python ../scripts/visualize_ontology.py
```

- Parses `scimantic-core/ontology/scimantic.ttl`
- Generates Mermaid class diagram showing entities, activities, and relationships
- Output can be rendered in Mermaid-compatible viewers

## Prerequisites

- **Java 17+**: Required for Widoco (documentation generation)
- **Python 3**: Required for HTTP server and visualization
- **uv**: Required for running Python scripts with dependencies
