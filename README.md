# Scimantic

**Scimantic** is a VS Code extension and semantic framework that enables **human-AI teaming** for scientific research. It transforms the scientific process into a machine-readable workflow from inception through publication.

## Vision

Scimantic transforms the traditional scientific workflow into a fully semantic, machine-readable process by capturing the complete research lifecycle as linked data. By integrating nanopublications, RDF/OWL ontologies, W3C PROV provenance, and uncertainty quantification from the very beginning of research, Scimantic enables:

- **Semantic Publishing from Day One**: Every research artifact (literature notes, hypotheses, experimental designs, data, analyses) is captured as machine-readable linked data
- **Complete Provenance**: Full traceability from initial literature review through final publication using W3C PROV-O
- **Uncertainty Quantification**: Explicit representation of uncertainties in hypotheses, measurements, and conclusions
- **AI-Assisted Research**: MCP-based AI agents that understand and interact with the semantic graph
- **Reproducible Science**: Machine-readable workflows that can be validated, reproduced, and extended

## The Scientific Method as Linked Data

Scimantic maps the activities in the scientific method to semantic web standards:

1. **Question Formation** → Generating a *Question*
2. **Literature Search** → Extracting *Evidence* from sources
3. **Evidence Assessment** → Evaluating *Evidence* credibility
4. **Hypothesis Formation** → Deriving a *Hypothesis* from evidence
5. **Design of Experiment** → Defining an *Experimental Method* to test the *Hypothesis*
6. **Experimentation** → Executing the *Experimental Method* to produce a *Dataset*
7. **Analysis** → Processing the *Dataset* to produce *Results*
8. **Result Assessment** → Comparing *Results* with *Hypothesis* to generate *Conclusions*

![Scimantic Ontology Graph](./ontology_graph.png)

## Documentation

For a deeper dive into Scimantic's rationale and design, please refer to the core documentation:

- **[Vision (Why)](./docs/00-why-vision.md)**: The philosophy of semantic research and the reasoning behind Scimantic.
- **[Architecture (What)](./docs/01-what-architecture.md)**: High-level system design and component breakdown.
- **[Roadmap (When)](./docs/02-when-roadmap.md)**: Planned features and milestones.
- **[Specifications (How)](./docs/03-how-specifications/)**: Detailed ontology and technical specifications.
- **[Features](./docs/features/)**: Vertical slice implementation plans.
- **[Release Guide](./docs/releasing.md)**: How to release Ontology, Core, and Extension versions.

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

### Quality Assurance & Automation

This project uses `pre-commit` to ensure code quality, consistency, and documentation accuracy.

To enable the automation:
```bash
# Install git hooks
pre-commit install
```

This includes ontology validation:

- **Syntax**: Validates `scimantic.ttl` format
- **Visualization**: **Auto-generates** `ontology_graph.png` (Mermaid) whenever the ontology changes

## License

[Add license information]
