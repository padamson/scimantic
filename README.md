# Scimantic

**Scimantic** is a Semantic Research Orchestration framework that enables machine-readable scientific research from inception through publication.

## Vision

Scimantic transforms the traditional scientific workflow into a fully semantic, machine-readable process by capturing the complete research lifecycle as linked data. By integrating nanopublications, RDF/OWL ontologies, W3C PROV provenance, and uncertainty quantification from the very beginning of research, Scimantic enables:

- **Semantic Publishing from Day One**: Every research artifact (literature notes, hypotheses, experimental designs, data, analyses) is captured as machine-readable linked data
- **Complete Provenance**: Full traceability from initial literature review through final publication using W3C PROV-O
- **Uncertainty Quantification**: Explicit representation of uncertainties in hypotheses, measurements, and conclusions
- **AI-Assisted Research**: MCP-based AI agents that understand and interact with the semantic graph
- **Reproducible Science**: Machine-readable workflows that can be validated, reproduced, and extended

## The Scientific Method as Linked Data

Scimantic maps the scientific method to semantic web standards:

1. **Literature Review** → Evidence entities linked via nanopublications
2. **Hypothesis Formation** → Hypothesis entities derived from evidence with uncertainty bounds
3. **Experimental Design** → Design entities specifying methods, parameters, and expected outcomes
4. **Experimentation** → PROV Activities generating datasets with full lineage
5. **Analysis** → Analysis entities with statistical measures and uncertainty propagation
6. **Publication** → Nanopublications packaging assertions with provenance and metadata

## Components

*   **[scimantic-core](./scimantic-core)**: Python framework for semantic workflow orchestration
    - RDF/OWL-based knowledge graph (RDFLib)
    - W3C PROV-O provenance tracking
    - Nanopublication generation and management
    - Uncertainty representation and propagation
    - MCP server for AI agent integration

*   **[scimantic-ext](./scimantic-ext)**: VS Code Extension for research visualization
    - Interactive knowledge graph visualization
    - Real-time provenance graph updates
    - AI-assisted literature search (MCP client)
    - Hypothesis minting and design specification UI

*   **[examples](./examples)**: Reference implementations
    - **scimantic-paper**: Dogfooding Scimantic by researching design and implementation of Scimantic itself

## Key Technologies

- **RDF/OWL**: W3C standards for linked data and ontologies
- **Nanopublications**: Minimal publishable units with provenance
- **W3C PROV-O**: Provenance ontology for complete lineage tracking
- **MCP (Model Context Protocol)**: AI agent integration for research assistance
- **RDFLib**: Python RDF manipulation and SPARQL querying

## Development

This repository is a `uv` workspace.

```bash
# Install dependencies for core
uv sync

# Run tests
cd scimantic-core && uv run pytest

# Start MCP server (for VS Code extension)
cd scimantic-core && uv run python -m scimantic.mcp
```

## Documentation

- [Feature Specifications](./docs/features/): Vertical slice planning and implementation tracking
- [CLAUDE.md](./CLAUDE.md): Guide for AI assistants working on this codebase

## License

[Add license information]
