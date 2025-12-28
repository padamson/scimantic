# Scimantic Architecture

This document specifies the top-level technical architecture of Scimantic: semantic models, ontologies, provenance patterns, and system components. It answers **WHAT** we're building at the system level.

For **WHY** we're building it, see [the vision](./00-why-vision.md).
For **WHEN** (implementation sequence), see [the roadmap](./02-when-roadmap.md).
For **HOW** (implementation details), see [specifications](./03-how-specifications/), `scimantic-core`, and `scimantic-ext`.
For **FEATURES** (vertical slices), see [features](./features/).

## Core Semantic Model

Scimantic's knowledge graph is built on W3C standards (RDF, OWL, PROV-O) and extends them with domain-specific ontologies for scientific research.

### Key Ontologies

Scimantic reuses existing W3C and community ontologies wherever possible:

1.  **W3C PROV-O** (`prov:`): Provides the core backbone for tracking provenance (Entity, Activity, Agent).
2.  **URREF** (`urref:`): Enables first-class representation of uncertainty (Epistemic vs Aleatory, Ambiguity, Vagueness).
3.  **Nanopublication Schema** (`np:`): Defines the structure for atomic, publishable units of knowledge.
4.  **Dublin Core Terms** (`dcterms:`): Provides standard metadata for citation and attribution.
5.  **FOAF** (`foaf:`): Represents researchers and organizations.
6.  **PROV-K** (`prov:` extensions): Adds support for scientific discourse (supports, contradicts).
7.  **Scimantic Ontology** (`scimantic:`): Adds minimal domain-specific extensions for scientific concepts (Hypothesis, ExperimentalMethod, etc.).

For full specification details, see [Ontology Specifications](../docs/03-how-specifications/ontology-spec-v0.1.0.md).

## Nanopublication Structure

Every assertion in Scimantic is wrapped as a **nanopublication**, a secure and verifiable data container with three parts:

1.  **Assertion Graph**: The actual scientific claim (evidence, hypothesis, result).
2.  **Provenance Graph**: The history of how this claim was created (who, when, using what source).
3.  **Publication Info Graph**: Metadata about the nanopublication itself (license, creator, digital signature).

Scimantic uses **Trusty URIs** to ensure content integrity, making every claim immutable and verifiable.

## Research Entity Types

Scimantic defines six core entity types that subclass `prov:Entity`, representing the major artifacts of the scientific method. **These entities, along with the activities and patterns below, directly implement the [scientific reasoning flow described in the Vision](../docs/00-why-vision.md#the-reasoning-chain-entities-activities-and-feedback).**

*   **Question**: The research query motivating the work.
*   **Evidence**: Factual claims extracted from literature or external sources.
*   **Hypothesis**: Testable claims derived from synthesizing evidence.
*   **ExperimentalMethod**: Specifications for experiments or simulations (maps to `prov:Plan`).
*   **Dataset**: Raw outputs or measurements from experimentation.
*   **Result**: Analyzed findings supporting or contradicting hypotheses.

For detailed property definitions and SHACL validation shapes, see [Ontology Specifications](../docs/03-how-specifications/ontology-spec-v0.1.0.md).

## Activity Types

Scimantic maps research processes to subclasses of `prov:Activity`. These activities link the entities together into a traceable provenance chain:

1.  **QuestionFormation**: Creation of the research query.
2.  **LiteratureSearch**: Extraction of evidence from existing knowledge.
3.  **EvidenceAssessment**: Evaluation of evidence credibility.
4.  **HypothesisFormation**: Synthesis of evidence into new claims.
5.  **DesignOfExperiment**: Planning the method to test the hypothesis.
6.  **Experimentation**: Execution of the plan to produce datasets.
7.  **Analysis**: Computational processing of data into results.
8.  **ResultAssessment**: Comparison against original hypotheses.

## Provenance Patterns

The system enforces specific provenance patterns to ensure every result is traceable:

*   **Extraction Pattern**: Trace evidence back to the source document and the person/agent who extracted it.
*   **Synthesis Pattern**: Trace hypotheses back to the multiple pieces of evidence that motivated them.
*   **Execution Pattern**: Trace datasets back to the experimental method and the software code/environment used.
*   **Analysis Pattern**: Trace results back to the dataset and the analysis logic.

These patterns are implemented automatically by the system's decorators and tools.

## Uncertainty Architecture

Scimantic leverages the **URREF** ontology to treat uncertainty as a first-class citizen. Rather than simple error bars, uncertainty is represented as linked entities that capture:
1.  **Nature**: Is it inherent randomness (Aleatory) or lack of knowledge (Epistemic)?
2.  **Type**: Is it ambiguity, vagueness, incompleteness, or inconsistency?
3.  **Propagation**: How does the uncertainty flow from evidence to hypothesis to result?

This architecture allows the system to compute confidence scores across the entire knowledge graph.

## MCP Integration Architecture

Scimantic provides an MCP server that exposes research operations as tools:

**Tools**:
1. `add_evidence`: Create Evidence entity as nanopublication
2. `add_hypothesis`: Create Hypothesis entity linking to evidence
3. `add_design`: Create Design entity specifying method
4. `query_graph`: Execute SPARQL queries on knowledge graph
5. `get_provenance`: Retrieve PROV lineage for an entity
6. `mint_nanopublication`: Wrap assertion as nanopublication with Trusty URI
7. `publish_nanopublication`: Export to remote nanopub server (optional)

**Architecture**:
```
AI Agent (Claude via MCP)
    ↓ (MCP protocol)
MCP Server (Python)
    ↓ (function calls)
scimantic-core (models.py, provenance.py, publish.py)
    ↓ (RDFLib)
RDF Knowledge Graph (project.ttl)
```

### MCP Client (scimantic-ext)

VS Code extension acts as MCP client:

**Operations**:
1. Fetch provenance graph for visualization
2. Trigger AI-assisted literature extraction
3. Display evidence/hypothesis tree view
4. Show nanopublication details in webview

**Architecture**:
```
VS Code Extension (TypeScript)
    ↓ (MCP client)
MCP Server (Python subprocess via uv)
    ↓ (JSON-RPC)
scimantic-core (Python)
```

## File Structure and Persistence

### Project Knowledge Graph

Each research project has a `project.ttl` file (RDF Turtle format):

```
examples/scimantic-paper/
├── project.ttl          # Main knowledge graph
├── data/                # Raw data files (referenced from RDF)
├── scripts/             # Analysis scripts (decorated for PROV)
└── nanopubs/            # Exported nanopublications (optional)
```

**project.ttl** contains:
- All Evidence, Hypothesis, Design, Analysis entities
- All PROV-O provenance metadata
- All nanopublications (as named graphs)

**Size consideration**: For large projects, `project.ttl` can be split into multiple files (e.g., `evidence.ttl`, `hypotheses.ttl`) and loaded as a dataset.

### Nanopublication Export

Nanopublications can be exported to:
1. **Local files** (`nanopubs/*.trig`): One file per nanopublication in TriG format
2. **Remote server** (http://nanopub.org or institutional server): HTTP POST
3. **IPFS**: Content-addressed storage for permanence

## System Components

### scimantic-core (Python)

**Modules**:
1. `models.py`: Entity classes (Evidence, Hypothesis, Design, Analysis)
2. `provenance.py`: PROV-O tracker, `@activity` decorator
3. `publish.py`: Nanopublication generation, Trusty URIs
4. `mcp.py`: MCP server exposing research tools
5. `config.py`: Configuration (namespaces, default uncertainty values)

**Dependencies**:
- `rdflib`: RDF graph manipulation, SPARQL, serialization
- `mcp` (Anthropic SDK): MCP server implementation
- `pytest`: Testing

### scimantic-ext (TypeScript)

**Modules**:
1. `extension.ts`: VS Code extension entry point
2. `services/mcpClient.ts`: MCP client communicating with scimantic-core
3. `providers/evidenceTreeProvider.ts`: Tree view for knowledge graph
4. `providers/graphVisualization.ts`: Webview for graph rendering (future)
5. `commands/*.ts`: Extension commands (refresh, show details, etc.)

**Dependencies**:
- `vscode`: VS Code extension API
- (future) `vis.js` or `cytoscape`: Graph visualization

### examples/scimantic-paper

**Purpose**: Dogfooding Scimantic by using it to research Scimantic itself.

**Contents**:
- `project.ttl`: Knowledge graph for Scimantic research
- Evidence from papers on nanopublications, PROV-O, scientific workflows
- Hypotheses about Scimantic's design
- Designs for Scimantic features
- Analyses of implementation trade-offs

## Access-Level Publishing Model

Scimantic supports four access levels for nanopublication publishing, enabling detailed control over what is shared. The access level is determined by metadata properties, allowing data to move between levels without changing structure.

### Access Levels

1.  **Local Scope** (Private Workspace): All data starts here. Safe for fair use of copyrighted materials. Stored in local `project.ttl`.
2.  **Institutional Scope** (Lab/Team): Shared within a trusted group via a private nanopub server. Good for works-in-progress.
3.  **Public Scope** (Global Knowledge): Original contributions (hypotheses, results) published to global servers like `nanopub.org`.
4.  **Public Essential Evidence Scope** (Selective): Minimal evidence necessary to support a claim, published with strict attribution and "fair use" metadata.

### Mobility Principle

Data is not locked to one level. Examples of mobility:
*   **Promotion**: A private hypothesis becomes public when the paper is submitted.
*   **Retraction**: If a publisher objects to open evidence, it can be retracted to institutional scope while the derived hypothesis remains public (citing the DOI).
*   **Sharing**: Works-in-progress can be promoted from local to institutional for collaboration.

Use the VS Code extension to manage these transitions seamlessly.

## References

- [W3C PROV-O](https://www.w3.org/TR/prov-o/)
- [Nanopublications](http://nanopub.org/)
- [RDFLib Documentation](https://rdflib.readthedocs.io/)
- [MCP Specification](https://modelcontextprotocol.io/)
- [Trusty URIs](http://trustyuri.net/)
- [AIDA Principles for Nanopublications](https://www.tkuhn.org/pub/kuhn2013eswc.pdf)
- [Whyis Use Cases](http://tetherless-world.github.io/whyis/usecases.html)
