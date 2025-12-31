# Scimantic Core

Python framework for semantic scientific research workflows with MCP server integration.

## Features

- **Semantic-First Architecture**: RDF/OWL ontologies from inception, not retrofitted
- **W3C PROV-O Provenance**: Automatic provenance tracking for all research activities
- **MCP Server**: Model Context Protocol interface for AI agent integration
- **LinkML Schema**: Ontology defined in LinkML with automatic artifact generation
- **Nanopublication Support**: First-class support for signed, immutable scientific assertions

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
# Install dependencies
cd scimantic-core
uv sync

# Install with dev dependencies (for testing, linting, type checking)
uv sync --extra dev
```

## Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=scimantic --cov-report=html

# Run specific test file
uv run pytest tests/test_mcp.py

# Run with verbose output
uv run pytest -v
```

### Code Quality

```bash
# Type checking with mypy
uv run mypy src/scimantic

# Linting with ruff
uv run ruff check src/scimantic

# Format code with ruff
uv run ruff format src/scimantic
```

### MCP Server

Start the MCP server for VS Code extension or Claude Code integration:

```bash
uv run python -m scimantic.mcp
```

The server exposes these tools:
- `add_question` - Add research question to knowledge graph
- `add_evidence` - Capture evidence with provenance
- `mint_hypothesis` - Form hypothesis from evidence
- `mint_design` - Create experiment design
- `get_provenance_graph` - Query the knowledge graph

## Architecture

```
scimantic-core/
├── src/scimantic/          # Source layout (modern Python best practice)
│   ├── models.py           # Evidence, Question, Hypothesis (LinkML generated)
│   ├── provenance.py       # W3C PROV-O tracker
│   ├── mcp.py              # MCP server implementation
│   └── config.py           # Configuration and constants
├── tests/                  # Test suite
├── schema/                 # LinkML schema source
│   └── scimantic.yaml      # Ontology schema (generates ontology/, models.py)
└── ontology/              # Generated ontology artifacts
    ├── scimantic.ttl      # Turtle serialization
    └── shacl/             # SHACL validation shapes
```

## Ontology Development

The Scimantic ontology is defined using [LinkML](https://linkml.io) and stored in `schema/scimantic.yaml`.

### Regenerating Ontology Artifacts

When you modify `schema/scimantic.yaml`, regenerate artifacts:

```bash
# Regenerate all artifacts (OWL, SHACL, Python models, etc.)
uv run gen-all
```

This generates:
- `ontology/scimantic.ttl` - Turtle ontology
- `ontology/shacl/scimantic-shapes.ttl` - SHACL validation shapes
- `src/scimantic/models.py` - Python dataclasses
- `../public/` - local ontology documentation
- `../ontology_graph.png` - simplified mermaid diagram of Scimantic ontology flow

### Validating Ontology

```bash
# Validate ontology with SHACL
uv run pyshacl -s ontology/shacl/scimantic-shapes.ttl ontology/scimantic.ttl
```

See [ontology/README.md](ontology/README.md) for detailed ontology documentation.

## Testing Strategy

Following TDD principles from [CLAUDE.md](../CLAUDE.md):

- **Unit Tests**: Test individual functions and classes (models, provenance)
- **Integration Tests**: Test MCP server with RDF persistence
- **Test Coverage**: Monitor for untested high-risk areas

Tests specify behavior (executable specifications). Implementation is self-documenting with clear naming.

## Pre-commit Hooks

This project uses pre-commit hooks for quality assurance:

```bash
# Install hooks (from repository root)
pre-commit install

# Run manually
pre-commit run --all-files
```

Hooks include:
- Ontology regeneration (when schema changes)
- SHACL validation
- Ruff linting and formatting
- mypy type checking
- pytest test suite

## Contributing

See the [monorepo README](../README.md) for overall project structure and contribution guidelines.

## Links

- [Scimantic Documentation](../docs/)
- [LinkML Documentation](https://linkml.io/)
- [W3C PROV-O](https://www.w3.org/TR/prov-o/)
- [MCP Specification](https://modelcontextprotocol.io/)
