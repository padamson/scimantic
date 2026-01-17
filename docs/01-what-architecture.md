# Scimantic Architecture

This document specifies the top-level technical architecture of Scimantic: semantic models, ontologies, provenance patterns, and system components. It answers **WHAT** we're building at the system level.

For **WHY** we're building it, see [the vision](./00-why-vision.md).
For **WHEN** (implementation sequence), see [the roadmap](./02-when-roadmap.md).
For **HOW** (implementation details), see [specifications](./03-how-specifications/), `scimantic-core`, `scimantic-ext`, and `scimantic-server`.
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

For full specification details, see [Ontology Specifications](../docs/03-how-specifications/ontology-spec-v0.1.0.md) and [scimantic-core ontolology specification test](../scimantic-core/tests/test_ontology_specification.py).

## Nanopublication Structure

Every publishable assertion in Scimantic is wrapped as a **nanopublication**, a secure and verifiable data container with three parts:

1.  **Assertion Graph**: The actual scientific claim (evidence, hypothesis, result).
2.  **Provenance Graph**: The history of how this claim was created (who, when, using what source).
3.  **Publication Info Graph**: Metadata about the nanopublication itself (license, creator, digital signature).

Scimantic uses **Trusty URIs** to ensure content integrity, making every claim immutable and verifiable.

## Research Entity Types

Scimantic defines six core entity types that subclass `prov:Entity`, representing the major artifacts of the scientific method. **These entities, along with the activities and patterns below, directly implement the [scientific reasoning flow described in the Vision](../docs/00-why-vision.md#the-reasoning-chain-entities-activities-and-feedback).**

*   **Question**: The research query motivating the work.
*   **Evidence**: Factual claims extracted from literature or external sources.
*   **Premise**: An evaluated proposition or insight derived from Evidence.
*   **Hypothesis**: Testable claims derived from synthesizing evidence.
*   **ExperimentalMethod**: Specifications for experiments or simulations (maps to `prov:Plan`).
*   **Dataset**: Raw outputs or measurements from experimentation.
*   **Result**: Analyzed findings supporting or contradicting hypotheses.

For detailed property definitions and SHACL validation shapes, see [Ontology Specifications](../docs/03-how-specifications/ontology-spec-v0.1.0.md) and [scimantic-core ontolology specification test](../scimantic-core/tests/test_ontology_specification.py).

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

Scimantic provides an MCP server that exposes research operations as tools. As the implementation evolves, these may look like:

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

## Master Knowledge Graph and Subset Publishing

Each research project has a master knowledge graph file (`project.ttl` in RDF Turtle format). Scimantic separates **research data collection** (comprehensive, private) from **selective publishing** (curated subsets for specific audiences). This enables researchers to maintain complete provenance while controlling what they share.

### Master Knowledge Graph (Private)

**Purpose**: Researcher's comprehensive research database, source of truth for all work.

**Characteristics**:
- **Location**: Local file system (`project.ttl`), institutional server
- **Access**: Private by default (researcher controls)
- **Content**: All entities (questions, evidence, hypotheses, designs, datasets, results)
- **Editability**: Actively maintained, entities added/updated/removed
- **Provenance**: Complete PROV-O chains for entire research process
- **License metadata**: Each entity has `dcterms:license` property

**Example structure**:
```turtle
# Master KG includes everything
:evidence_001 a scimantic:Evidence ;
    dcterms:license <http://creativecommons.org/licenses/by/4.0/> .

:evidence_002 a scimantic:Evidence ;
    dcterms:license <http://scimantic.io/license#AllRightsReserved> ;  # Extracted from copyrighted paper
    scimantic:fairUseJustification "Factual data extraction" .

:evidence_003 a scimantic:Evidence ;
    dcterms:license <http://scimantic.io/license#Proprietary> ;  # Collaborator data, cannot publish
    scimantic:sharingRestriction "Lab B consent required" .
```

### Subset Definitions (Configuration)

**Purpose**: Specify which parts of master KG to publish for specific purposes.

**Storage**: `.scimantic/subsets/*.yaml` files (version controlled)

**Definition methods**:
1. **SPARQL CONSTRUCT queries**: Flexible, powerful selection
2. **Entity tags**: Tag entities with project/purpose IDs
3. **License filters**: Include only entities with compatible licenses
4. **Provenance closure**: Automatically include supporting evidence

**Example definition** (`.scimantic/subsets/nature-2025.yaml`):
```yaml
name: nature-2025
title: "Supporting Data: Protein X Folding"
description: "Complete provenance for Nature paper DOI:10.1038/..."
license: CC-BY-4.0

# SPARQL query defining subset
query: |
  CONSTRUCT { ?s ?p ?o } WHERE {
    ?s scimantic:project 'nature-2025' .
    ?s (prov:wasDerivedFrom|prov:used)* ?supporting .
    ?supporting ?p ?o .
    ?s ?p ?o .
  }

# License requirements
license_filter:
  allow: [CC-BY-4.0, CC0, AllRightsReserved]  # With fair use justification
  block: [Proprietary]

# Publishing destinations
destinations:
  - nanopub_server: https://collaboratory.semanticscience.org
  - github_pages: padamson/nature-2025-data
  - zenodo:
      doi: true
      communities: [computational-chemistry]
```

### Generated Subsets (Read-Only Snapshots)

**Purpose**: Executable output of subset definition applied to master KG.

**Storage**: `subsets/*.ttl` files (generated files under version control, DO NOT EDIT)

**Generation workflow**:
1. Execute SPARQL query against master KG
2. Analyze licenses (warn about incompatibilities)
3. Include provenance metadata (when generated, from which master KG commit)
4. Write to `subsets/name.ttl`
5. Commit snapshot to version control

**Provenance of generated subset**:
```turtle
:subset_nature_2025_v1.0 a scimantic:PublishedSubset ;
    prov:wasGeneratedBy [
        a prov:Activity ;
        prov:used :master_kg_commit_abc123 ;  # Git commit SHA
        prov:used :subset_definition_nature_2025 ;  # SPARQL query
        prov:startedAtTime "2026-01-15T10:30:00Z"^^xsd:dateTime
    ] ;
    scimantic:licenseAnalysis [
        scimantic:openLicensedEntities 41 ;
        scimantic:restrictedLicensedEntities 1 ;
        scimantic:publishable true
    ] .
```

**Key principle**: Subsets are **generated artifacts** (like compiled code), not manually edited. Always regenerate from master KG + query.

### License-Based Subset Management

**Every entity carries license metadata**:
```turtle
:hypothesis_042 dcterms:license <http://creativecommons.org/licenses/by/4.0/> .
:evidence_101 dcterms:license <http://scimantic.io/license#AllRightsReserved> ;
    scimantic:fairUseJustification "Factual extraction for research" .
```

**Automatic license analysis during subset generation**:
- Count entities by license type
- Warn if proprietary data included
- Block publication if incompatible licenses present
- Recommend safeguards for copyrighted material

**Output**:
```
License Analysis:
  ✓ 38 entities: CC-BY-4.0 (publishable)
  ✓ 3 entities: CC0 (publishable)
  ⚠ 1 entity: All Rights Reserved (requires fair use justification)
  ✗ 0 entities: Proprietary (would block)
Overall: PUBLISHABLE with fair use attribution
```

### Publishing Destinations

Subsets can be published to **multiple destinations** simultaneously.

#### Preconfigured Destinations

1. **Nanopublication Servers** (PRIMARY for semantic web)
   - **Examples**: https://collaboratory.semanticscience.org, https://nanopub.org
   - **Benefits**: Trusty URIs, SPARQL federation, semantic web native
   - **Access**: Public or institutional (ORCID auth)

2. **GitHub Pages** (Static HTML viewer)
   - **Benefits**: Free hosting, version control, custom domains
   - **CI/CD**: GitHub Actions generate viewer from subset RDF
   - **Access**: Public (or private repo with auth)

3. **Scimantic.io** (Interactive web platform)
   - **Benefits**: SPARQL playground, graph visualization, discovery
   - **Access**: Public or private (ORCID auth, time-limited links)

4. **Zenodo/Figshare** (Archival with DOI)
   - **Benefits**: Long-term preservation, DOI for citation
   - **Access**: Public or embargoed

#### Configurable Destinations

1. **Self-Hosted Scimantic-Server**
   - **Use case**: Institutional deployment, compliance requirements
   - **Benefits**: Full control, unlimited scale, SSO integration
   - **Access**: Configurable (public, institutional, private)

2. **Institutional Repositories**
   - **Examples**: DSpace, Fedora, Samvera
   - **Benefits**: Library archival mandates, local discovery
   - **Access**: Varies by institution

3. **Custom RDF Endpoints**
   - **Use case**: Custom triple stores, research platforms
   - **Requirements**: HTTP API for RDF upload
   - **Access**: Configured per endpoint

### Publishing Workflow Example

```bash
# 1. Maintain master KG (private)
scimantic add-evidence --citation "Smith 2024" --license CC-BY-4.0

# 2. Define subset for paper
scimantic subset define nature-2025 \
  --query "CONSTRUCT { ... }" \
  --destinations nanopub-server,github-pages,zenodo

# 3. Generate subset (includes license analysis)
scimantic subset generate nature-2025
# Output: ✓ Generated subsets/nature-2025.ttl (42 entities, license: OK)

# 4. Review and commit snapshot
git add subsets/nature-2025.ttl
git commit -m "Generate nature-2025 subset v1.0"
git tag subset-nature-2025-v1.0

# 5. Publish to destinations
scimantic subset publish nature-2025 --version v1.0
# Output:
#   ✓ https://collaboratory.semanticscience.org/np/RAabc123
#   ✓ https://padamson.github.io/nature-2025-data
#   ✓ https://doi.org/10.5281/zenodo.7654321
```

### Access Control Patterns

**Public Destinations**: Anyone can access (GitHub Pages, public nanopub servers)

**Private Destinations**: Authentication required
- **ORCID**: Researcher identity verification
- **Institutional SSO**: SAML, LDAP for organization access
- **Time-Limited Links**: Temporary access for reviewers (grant panels, peer review)
- **Collaborator Lists**: Explicit ORCID-based access control

**Hybrid**: Same subset published to both public and private destinations
- Public nanopub server for open science community
- Private scimantic.io project for collaboration with specific colleagues

## System Components

### scimantic-core (Python)

**Modules**:
1. `models.py`: Entity classes (Evidence, Hypothesis, Design, Analysis)
2. `provenance.py`: PROV-O tracker, `@activity` decorator
3. `publish.py`: Nanopublication generation, Trusty URIs
4. `subset.py`: Subset definition, generation, license analysis (NEW)
5. `mcp.py`: MCP server exposing research tools
6. `config.py`: Configuration (namespaces, default uncertainty values)

**Dependencies**:
- `rdflib`: RDF graph manipulation, SPARQL, serialization
- `mcp` (Anthropic SDK): MCP server implementation
- `pytest`: Testing

### scimantic-ext (TypeScript)

**Modules**:
1. `extension.ts`: VS Code extension entry point
2. `services/mcpClient.ts`: MCP client communicating with scimantic-core
3. `providers/knowledgeGraphTreeProvider.ts`: Tree view for knowledge graph
4. `providers/graphVisualization.ts`: Webview for graph rendering (future)
5. `commands/*.ts`: Extension commands (refresh, show details, generate subset, etc.)

**Dependencies**:
- `vscode`: VS Code extension API
- (future) `vis.js` or `cytoscape`: Graph visualization

### scimantic-server (Python/TypeScript)

**Purpose**: Host and share subsets (public or private), enable collaboration.

**Components**:
1. `scimantic-server-api` (Python FastAPI): REST API for subset hosting
2. `scimantic-server-web` (TypeScript React/Svelte): Interactive viewer
3. `scimantic-cli` (Python): Git-like commands (`scimantic push`, `pull`, `clone`)

See [scimantic-server roadmap](./02.1-when-scimantic-server-roadmap.md) for details.

### examples/scimantic-paper

**Purpose**: Dogfooding Scimantic by using it to research Scimantic itself.

**Contents**:
- `project.ttl`: Knowledge graph for Scimantic research
- Evidence from papers on nanopublications, PROV-O, scientific workflows
- Hypotheses about Scimantic's design
- Designs for Scimantic features
- Analyses of implementation trade-offs

## References

- [W3C PROV-O](https://www.w3.org/TR/prov-o/)
- [Nanopublications](http://nanopub.org/)
- [RDFLib Documentation](https://rdflib.readthedocs.io/)
- [MCP Specification](https://modelcontextprotocol.io/)
- [Trusty URIs](http://trustyuri.net/)
- [AIDA Principles for Nanopublications](https://www.tkuhn.org/pub/kuhn2013eswc.pdf)
- [Whyis Use Cases](http://tetherless-world.github.io/whyis/usecases.html)
