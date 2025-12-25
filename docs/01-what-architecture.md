# Scimantic Architecture

This document specifies the top-level technical architecture of Scimantic: semantic models, ontologies, provenance patterns, and system components. It answers **WHAT** we're building at the system level.

For **WHY** we're building it, see [the vision](./00-why-vision.md).
For **WHEN** (implementation sequence), see [the roadmap](./02-when-roadmap.md).
For **HOW** (implementation details), see code and tests.

## Core Semantic Model

Scimantic's knowledge graph is built on W3C standards (RDF, OWL, PROV-O) and extends them with domain-specific ontologies for scientific research.

### Key Ontologies

**Scimantic reuses existing W3C and community ontologies wherever possible:**

1. **W3C PROV-O** (`prov:`): Provenance (core foundation)
   - `prov:Entity`: Data, hypotheses, evidence, results
   - `prov:Activity`: Computations, experiments, extractions
   - `prov:Agent`: Researchers, AI agents, software
   - `prov:wasGeneratedBy`, `prov:used`, `prov:wasAttributedTo`, `prov:wasDerivedFrom`, etc.

2. **URREF** (`urref:`): Uncertainty Representation and Reasoning Evaluation Framework
   - `urref:UncertaintyEntity`: First-class uncertainty representation
   - `urref:AleatoricUncertainty`: Inherent randomness (irreducible)
   - `urref:EpistemicUncertainty`: Knowledge gaps (reducible with more data)
   - `urref:Ambiguity`, `urref:Randomness`, `urref:Vagueness`: Uncertainty types
   - Used to represent uncertainty as linked entities, not simple floats

3. **Nanopublication Schema** (`np:`): Minimal publishable units
   - `np:Nanopublication`: Top-level container
   - `np:hasAssertion`: Points to assertion graph
   - `np:hasProvenance`: Points to provenance graph
   - `np:hasPublicationInfo`: Points to publication info graph

4. **Dublin Core Terms** (`dcterms:`): Metadata
   - `dcterms:title`, `dcterms:creator`, `dcterms:created`, `dcterms:source`
   - `dcterms:license`, `dcterms:rights`, `dcterms:bibliographicCitation`

5. **FOAF** (`foaf:`): Agents (researchers, organizations)
   - `foaf:Person`, `foaf:Organization`, `foaf:name`, `foaf:mbox`

6. **PROV-K** (`prov:` extensions): Provenance with Knowledge (discourse ontology patterns)
   - `prov:supports`, `prov:contradicts`: Evidence linkage predicates
   - `prov:wasQuotedFrom`: Literature extraction provenance
   - Used for scientific argumentation and evidence synthesis

7. **Scimantic Ontology** (`scimantic:`): Minimal research-specific extensions
   - **Entity types** (subclasses of `prov:Entity`):
     - `scimantic:Question`: Research questions
     - `scimantic:Evidence`: Extracted facts from literature
     - `scimantic:Hypothesis`: Claims derived from evidence
     - `scimantic:Design`: Experimental/computational method specifications (subclass of `prov:Plan`)
     - `scimantic:Dataset`: Observational data or measurements
     - `scimantic:Result`: Analysis outcomes
   - **Access control**:
     - `scimantic:accessLevel`: Publishing scope ("local", "institutional", "public")
   - **Note**: Uncertainty is represented using URREF, not custom scimantic properties

### Namespace Prefixes

```turtle
@prefix rdf:       <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs:      <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:       <http://www.w3.org/2001/XMLSchema#> .
@prefix owl:       <http://www.w3.org/2002/07/owl#> .
@prefix prov:      <http://www.w3.org/ns/prov#> .
@prefix urref:     <http://www.w3.org/ns/urref#> .
@prefix np:        <http://www.nanopub.org/nschema#> .
@prefix dcterms:   <http://purl.org/dc/terms/> .
@prefix foaf:      <http://xmlns.com/foaf/0.1/> .
@prefix scimantic: <http://scimantic.io/ontology#> .
```

## Nanopublication Structure

Every assertion in Scimantic is wrapped as a **nanopublication** with three named graphs:

### 1. Assertion Graph
Contains the scientific claim as RDF triples.

```turtle
:assertion_001 {
    :evidence_001 a scimantic:Evidence ;
        dcterms:title "DCS measurement from Smith 2023" ;
        rdfs:label "DCS = 150 mb at E = 10 MeV for p + 12C" ;
        dcterms:source <https://doi.org/10.1234/smith2023> ;
        scimantic:hasUncertainty :uncertainty_001 .

    :uncertainty_001 a urref:UncertaintyEntity ;
        urref:hasNature urref:EpistemicUncertainty ;
        urref:hasType urref:Ambiguity ;
        urref:quantifiedAs "0.05"^^xsd:float .
}
```

### 2. Provenance Graph
Describes how the assertion was created using W3C PROV-O.

```turtle
:provenance_001 {
    :assertion_001
        prov:wasGeneratedBy :extraction_activity_001 ;
        prov:generatedAtTime "2025-12-23T14:30:00Z"^^xsd:dateTime .

    :extraction_activity_001 a prov:Activity ;
        prov:wasAssociatedWith :researcher_emily ;
        prov:used <https://doi.org/10.1234/smith2023> .

    :researcher_emily a prov:Agent, foaf:Person ;
        foaf:name "Emily Chen" ;
        foaf:mbox <mailto:emily@example.org> .
}
```

### 3. Publication Info Graph
Metadata about the nanopublication itself.

```turtle
:pubinfo_001 {
    :np_001 a np:Nanopublication ;
        np:hasAssertion :assertion_001 ;
        np:hasProvenance :provenance_001 ;
        np:hasPublicationInfo :pubinfo_001 ;
        dcterms:created "2025-12-23T14:30:00Z"^^xsd:dateTime ;
        dcterms:creator :researcher_emily .
}
```

### Trusty URIs

Scimantic uses **Trusty URIs** for nanopublications: content-based identifiers that enable verification.

**Format**: `http://example.org/np/RA1234567890ABCDEF`

Where `RA1234567890ABCDEF` is a cryptographic hash of the nanopublication's RDF content.

**Properties**:
- **Immutable**: Same content = same URI
- **Verifiable**: Re-compute hash to verify integrity
- **Citable**: Persistent identifier for individual claims

## Research Entity Types

## Research Entity Types

### Question

Research question that motivates the investigation.

```turtle
:question_001 a scimantic:Question, prov:Entity ;
    rdfs:label "Can the MQDO method accurately compute differential cross sections?" ;
    prov:wasGeneratedBy :question_formation_001 ;
    prov:generatedAtTime "2025-12-23T13:00:00Z"^^xsd:dateTime .
```

### Evidence

Extracted facts from literature or prior results.

```turtle
:evidence_001 a scimantic:Evidence, prov:Entity ;
    dcterms:title "DCS measurement" ;
    rdfs:label "DCS = 150 mb at E = 10 MeV" ;
    dcterms:source <https://doi.org/10.1234/smith2023> ;
    scimantic:hasUncertainty :uncertainty_001 ;
    prov:wasGeneratedBy :extraction_activity ;
    prov:generatedAtTime "2025-12-23T14:00:00Z"^^xsd:dateTime .

:uncertainty_001 a urref:UncertaintyEntity ;
    urref:hasNature urref:EpistemicUncertainty ;
    urref:hasType urref:Ambiguity ;
    urref:quantifiedAs "0.05"^^xsd:float .
```

**Key properties**:
- `dcterms:source`: DOI or URI of original publication
- `scimantic:hasUncertainty`: Links to URREF uncertainty entity
- `prov:wasGeneratedBy`: Links to extraction activity (who extracted, when)

**Critical**: Evidence entities ARE nanopublications. The RDF above is the **assertion graph**; provenance and publication info graphs wrap it.

### Hypothesis

Claims derived from evidence, with explicit uncertainty.

```turtle
:hypothesis_001 a scimantic:Hypothesis, prov:Entity ;
    rdfs:label "DCS for p + 12C can be computed using MQDO" ;
    scimantic:hasUncertainty :uncertainty_hyp_001 ;
    prov:wasDerivedFrom :evidence_001, :evidence_002 ;
    prov:wasGeneratedBy :hypothesis_formation_activity ;
    prov:generatedAtTime "2025-12-23T15:00:00Z"^^xsd:dateTime .

:uncertainty_hyp_001 a urref:UncertaintyEntity ;
    urref:hasNature urref:EpistemicUncertainty ;
    urref:hasType urref:Incompleteness ;
    urref:quantifiedAs "0.15"^^xsd:float ;
    urref:derivedFrom :uncertainty_001, :uncertainty_002 .
```

**Key properties**:
- `prov:wasDerivedFrom`: Links to supporting evidence
- `scimantic:hasUncertainty`: Links to URREF uncertainty entity with higher uncertainty than evidence
- Can link to multiple evidence entities (synthesis)

**Uncertainty propagation**: Hypothesis uncertainty entities use `urref:derivedFrom` to link to source uncertainties. If hypothesis derives from evidence with uncertainties `u1, u2, ...`, then:
```
hypothesis_uncertainty >= max(u1, u2, ...) + epistemic_gap
```

### Design

Specification of experimental or computational method.

```turtle
:design_001 a scimantic:Design, prov:Entity ;
    rdfs:label "MQDO calculation for p + 12C at E = 10 MeV" ;
    scimantic:method "Multi-channel quantum defect theory" ;
    scimantic:parameter [
        a scimantic:Parameter ;
        rdfs:label "Energy" ;
        scimantic:value "10.0"^^xsd:float ;
        scimantic:unit "MeV"
    ] ;
    scimantic:expectedOutcome :hypothesis_001 ;
    prov:wasDerivedFrom :hypothesis_001 ;
    prov:wasGeneratedBy :design_activity ;
    prov:generatedAtTime "2025-12-23T16:00:00Z"^^xsd:dateTime .
```

**Key properties**:
- `scimantic:method`: Textual description of method (can link to ontology of methods)
- `scimantic:parameter`: Structured parameters (enables validation)
- `scimantic:expectedOutcome`: Links to hypothesis being tested
- `prov:wasDerivedFrom`: Hypothesis that motivated the design

### Dataset

Observational data or experimental measurements.

```turtle
:dataset_001 a scimantic:Dataset, prov:Entity ;
    rdfs:label "Raw output from MQDO" ;
    dcterms:format "application/json" ;
    scimantic:hasChecksum "sha256:e3b0c442..." ;
    prov:wasGeneratedBy :execution_001 ;
    prov:wasDerivedFrom :design_001 ;
    prov:generatedAtTime "2025-12-23T16:30:00Z"^^xsd:dateTime .
```

### Result

Results of computational or statistical analysis.

```turtle
:result_001 a scimantic:Result, prov:Entity ;
    rdfs:label "MQDO result for p + 12C" ;
    scimantic:value "148.5"^^xsd:float ;
    scimantic:unit "mb" ;
    scimantic:hasUncertainty :uncertainty_result_001 ;
    prov:wasGeneratedBy :mqdo_computation ;
    prov:used :design_001, :input_data_001 ;
    prov:generatedAtTime "2025-12-23T17:00:00Z"^^xsd:dateTime .

:uncertainty_result_001 a urref:UncertaintyEntity ;
    urref:hasNature urref:EpistemicUncertainty ;
    urref:hasType urref:Incompleteness ;
    urref:quantifiedAs "0.03"^^xsd:float .
```

**Key properties**:
- `scimantic:result`: Structured results with URREF uncertainty entities
- `prov:wasGeneratedBy`: Computational activity (traceable to code)
- `prov:used`: Links to design and input data

## Activity Types

Scimantic defines 7 activity types mapping to the scientific method steps. Each is a subclass of `prov:Activity`.

### 1. Question Formation
Formulating the initial research question.
- **Input**: None (or previous Evidence/Result via feedback loop)
- **Output**: `scimantic:Question`
- **Class**: `scimantic:QuestionFormation`

### 2. Literature Search
Searching and extracting evidence from existing literature.
- **Input**: `scimantic:Question` (what informs the search)
- **Output**: `scimantic:Evidence`
- **Class**: `scimantic:LiteratureSearch`

### 3. Assessment
Evaluating evidence credibility or relevance.
- **Input**: `scimantic:Evidence`
- **Output**: `scimantic:Assessment` (or metadata on Evidence)
- **Class**: `scimantic:Assessment`

### 4. Hypothesis Formation
Synthesizing evidence into testable claims.
- **Input**: `scimantic:Evidence`, `scimantic:Question`
- **Output**: `scimantic:Hypothesis`
- **Class**: `scimantic:HypothesisFormation`

### 5. Design Planning
Specifying the method to test a hypothesis.
- **Input**: `scimantic:Hypothesis`
- **Output**: `scimantic:Design`
- **Class**: `scimantic:DesignPlanning`

### 6. Execution
Running the experiment or simulation.
- **Input**: `scimantic:Design`
- **Output**: `scimantic:Dataset`
- **Class**: `scimantic:Execution`

### 7. Analysis
Processing data into findings.
- **Input**: `scimantic:Dataset`
- **Output**: `scimantic:Result`
- **Class**: `scimantic:Analysis`

## Provenance Patterns

### Pattern 1: Literature Extraction

**Scenario**: Researcher extracts fact from legacy paper.

```turtle
# Activity
:extraction_001 a prov:Activity ;
    rdfs:label "Extract DCS from Smith 2023" ;
    prov:startedAtTime "2025-12-23T14:00:00Z"^^xsd:dateTime ;
    prov:endedAtTime "2025-12-23T14:05:00Z"^^xsd:dateTime ;
    prov:wasAssociatedWith :researcher_emily ;
    prov:used <https://doi.org/10.1234/smith2023> .

# Generated Entity (Evidence)
:evidence_001 a scimantic:Evidence, prov:Entity ;
    rdfs:label "DCS = 150 mb" ;
    prov:wasGeneratedBy :extraction_001 .

# Agent
:researcher_emily a prov:Agent, foaf:Person ;
    foaf:name "Emily Chen" .
```

**Pattern**: `Activity (extraction) --used--> Source (DOI) --generatedBy--> Evidence`

### Pattern 2: Hypothesis Formation

**Scenario**: Researcher formulates hypothesis from evidence.

```turtle
# Activity
:hypothesis_formation_001 a prov:Activity ;
    rdfs:label "Formulate MQDO hypothesis" ;
    prov:startedAtTime "2025-12-23T15:00:00Z"^^xsd:dateTime ;
    prov:wasAssociatedWith :researcher_emily ;
    prov:used :evidence_001, :evidence_002 .

# Generated Entity (Hypothesis)
:hypothesis_001 a scimantic:Hypothesis, prov:Entity ;
    rdfs:label "MQDO can compute DCS" ;
    prov:wasGeneratedBy :hypothesis_formation_001 ;
    prov:wasDerivedFrom :evidence_001, :evidence_002 .
```

**Pattern**: `Activity (formation) --used--> Evidence --generatedBy--> Hypothesis`

### Pattern 3: Computational Analysis

**Scenario**: Code executes to generate results.

```turtle
# Activity
:mqdo_computation_001 a prov:Activity ;
    rdfs:label "Run MQDO code" ;
    prov:startedAtTime "2025-12-23T17:00:00Z"^^xsd:dateTime ;
    prov:endedAtTime "2025-12-23T17:30:00Z"^^xsd:dateTime ;
    prov:wasAssociatedWith :mqdo_software ;
    prov:used :design_001, :input_data_001 .

# Software Agent
:mqdo_software a prov:Agent, prov:SoftwareAgent ;
    rdfs:label "MQDO v2.1" ;
    scimantic:codeRepository <https://github.com/example/mqdo> ;
    scimantic:commitHash "a1b2c3d4" .

# Generated Entity (Result)
:result_001 a scimantic:Result, prov:Entity ;
    rdfs:label "MQDO result" ;
    prov:wasGeneratedBy :mqdo_computation_001 .
```

**Pattern**: `Activity (computation) --used--> Design + Data --generatedBy--> Result`

**Critical**: Software agents have `scimantic:codeRepository` and `scimantic:commitHash` for reproducibility.

### Pattern 4: Decorated Python Function

**Scenario**: Python function auto-generates provenance via `@activity` decorator.

```python
from scimantic.provenance import provenance_tracker

@provenance_tracker.activity(name="compute_dcs")
def compute_dcs(input_file, method="MQDO"):
    # Function body
    result = do_computation(input_file, method)
    return result
```

**Generated provenance**:
- `prov:Activity` with name "compute_dcs"
- `prov:used` linking to `input_file` (as `prov:Entity`)
- `prov:wasAssociatedWith` linking to software agent (Python script)
- `prov:wasGeneratedBy` linking result to activity

## Uncertainty Representation

Scimantic uses the **URREF (Uncertainty Representation and Reasoning Evaluation Framework)** ontology for first-class uncertainty representation. Uncertainty is not a simple float property, but a linked entity with rich semantics.

### Uncertainty as Linked Entities

Every entity that represents a measurement or claim links to an `urref:UncertaintyEntity`:

```turtle
:evidence_001 scimantic:hasUncertainty :uncertainty_001 .

:uncertainty_001 a urref:UncertaintyEntity ;
    urref:hasNature urref:EpistemicUncertainty ;  # Knowledge gap (reducible)
    urref:hasType urref:Ambiguity ;               # Multiple interpretations
    urref:quantifiedAs "0.05"^^xsd:float ;         # Numeric quantification
    rdfs:comment "Uncertainty due to measurement precision limits" .
```

**URREF Nature** (epistemic vs. aleatory):
- `urref:EpistemicUncertainty`: Knowledge gaps (reducible with more data, better models)
- `urref:AleatoricUncertainty`: Inherent randomness (irreducible, fundamental to system)

**URREF Types** (specific uncertainty sources):
- `urref:Ambiguity`: Multiple valid interpretations
- `urref:Vagueness`: Imprecise definitions or boundaries
- `urref:Randomness`: Stochastic processes
- `urref:Incompleteness`: Missing information

**Quantification**:
- `urref:quantifiedAs`: Numeric value (0.0 = no confidence, 1.0 = certainty)
- Can also use `urref:qualifiedAs` for qualitative assessments ("low", "medium", "high")

### Uncertainty Propagation

When deriving new entities from existing ones, uncertainty entities are linked and propagated:

**Rule 1 - Hypothesis from Evidence**:
```turtle
:hypothesis_001 scimantic:hasUncertainty :uncertainty_hyp_001 .

:uncertainty_hyp_001 a urref:UncertaintyEntity ;
    urref:hasNature urref:EpistemicUncertainty ;
    urref:hasType urref:Ambiguity ;
    urref:quantifiedAs "0.20"^^xsd:float ;
    urref:derivedFrom :uncertainty_ev_001, :uncertainty_ev_002 ;
    rdfs:comment "Combined evidence uncertainty plus epistemic gap from inductive reasoning" .
```

Where:
```
u_hypothesis >= max(u_evidence_1, u_evidence_2, ...) + epistemic_gap
```

**Rule 2 - Analysis from Design**:
```turtle
:analysis_001 scimantic:hasUncertainty :uncertainty_analysis_001 .

:uncertainty_analysis_001 a urref:UncertaintyEntity ;
    urref:hasNature urref:EpistemicUncertainty ;  # Computational approximation
    urref:hasType urref:Incompleteness ;          # Numerical truncation
    urref:quantifiedAs "0.03"^^xsd:float ;
    urref:derivedFrom :uncertainty_design_001, :uncertainty_computational_001 ;
    rdfs:comment "Quadrature sum of design and computational uncertainties" .
```

Where:
```
u_analysis = sqrt(u_design^2 + u_computational^2)
```

**Implementation**: Uncertainty propagation can be automated via SPARQL queries or Python decorators that create new `urref:UncertaintyEntity` instances with `urref:derivedFrom` links.

## MCP Integration Architecture

### MCP Server (scimantic-core)

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

Scimantic supports four access levels for nanopublication publishing, each with different legal/privacy implications. The **data model is access-level-agnostic**: all nanopubs use the same RDF structure, with metadata tracking publishing scope.

### Access Level 1: Local Scope (Always)

**Purpose**: Private research workspace

**Storage**: Local `project.ttl` file

**Legal Status**: Fair use for personal research (no risk)

**Content**:
- All evidence extracted from legacy papers
- Hypotheses in development (not ready to publish)
- Experimental designs (planning stage)
- Analysis results (preliminary)

**Metadata**:
```turtle
:np_001 scimantic:accessLevel "local" ;
    scimantic:publishable "false"^^xsd:boolean .
```

### Access Level 2: Institutional Scope (Controlled Sharing)

**Purpose**: Collaboration within trusted network

**Storage**: Lab-hosted nanopub server with access control

**Legal Status**: Fair use for collaborative research (low risk)

**Content**:
- Evidence shared with lab members or collaborators
- Works-in-progress requiring feedback
- Sensitive data requiring access control

**Metadata**:
```turtle
:np_001 scimantic:accessLevel "institutional" ;
    scimantic:publishedTo <https://lab.example.org/nanopubs/> ;
    scimantic:accessControl "lab_members_only" ;
    scimantic:publishable "true"^^xsd:boolean .
```

**Technical Requirements**:
- SPARQL endpoint with authentication
- Access control lists (ACL)
- Optional: ORCID-based authorization

### Access Level 3: Public Scope - Original Contributions (Standard)

**Purpose**: Publish original research to scientific community

**Storage**: Public nanopub servers (nanopub.org, institutional repositories)

**Legal Status**: No risk (original work, full rights)

**Content**:
- Hypotheses formulated by researcher (original thought)
- Experimental designs created by researcher (original methodology)
- Analysis results from computational work (original data)
- New measurements/observations (original experiments)

**NOT included**:
- Evidence extracted from legacy copyrighted papers (use Access Level 4 if essential)

**Metadata**:
```turtle
:np_001 scimantic:accessLevel "public" ;
    scimantic:publishedTo <https://nanopub.org/>, <https://zenodo.org/> ;
    dcterms:license <https://creativecommons.org/licenses/by/4.0/> ;
    scimantic:publishable "true"^^xsd:boolean .
```

### Access Level 4: Public Scope - Essential Evidence (Selective, with Care)

**Purpose**: Publish evidence when essential to validate published hypotheses

**Storage**: Public nanopub servers (same as Access Level 3)

**Legal Status**: Medium risk (fair use argument, transformative use)

**Content**:
- Evidence nanopubs **directly cited** in published hypotheses/analyses
- Minimal factual extractions (not narrative text)
- Prominent attribution with DOIs

**Criteria for Access Level 4**:
1. **Necessity Test**: Must be directly referenced in published nanopub
2. **Minimality**: Smallest factual extraction needed
3. **Transformative**: Adds uncertainty, provenance, machine-readability
4. **Attribution**: Explicit `dcterms:source`, `dcterms:bibliographicCitation`

**Risk Mitigation Metadata**:
```turtle
:np_001 scimantic:accessLevel "public_essential_evidence" ;
    scimantic:publishedTo <https://nanopub.org/> ;
    dcterms:source <https://doi.org/10.1234/smith2023> ;
    dcterms:bibliographicCitation "Smith et al., Phys. Rev. C 107, 034602 (2023)" ;
    scimantic:extractedFrom "Figure 3, page 5" ;
    scimantic:legalBasis "fair_use_research" ;
    scimantic:copyrightNotice """
        This nanopublication contains factual data extracted from a copyrighted
        source under fair use for research purposes. The original work is cited.
        If you are the copyright holder and object, contact: [email]
    """ ;
    scimantic:retractionPolicy <https://scimantic.io/retraction-policy> .
```

**Publisher Whitelist** (preferential extraction):
```turtle
:evidence_001 scimantic:sourcePublisher <https://ror.org/01j7nq853> ;  # APS (open to TDM)
    scimantic:sourceLicense <https://creativecommons.org/licenses/by/4.0/> ;  # CC-BY (safe)
    scimantic:publishingRisk "low"^^scimantic:RiskLevel .
```

### Access-Level Mobility: Moving Between Scopes

**Key Design Principle**: Evidence can move between access levels as contexts change. The **data model stays constant**; only metadata changes.

**Scenario 1: Promotion (Local → Public Essential Evidence)**
- Researcher extracts evidence locally (Local scope)
- Formulates hypothesis referencing that evidence
- Publishes hypothesis (Public scope) + essential evidence (Public essential evidence scope)
- Metadata update: `scimantic:accessLevel "local"` → `"public_essential_evidence"`

**Scenario 2: Sharing (Local → Institutional)**
- Researcher shares evidence with collaborator
- Evidence uploaded to lab server
- Metadata update: Add `scimantic:publishedTo <https://lab.example.org/>`

**Scenario 3: Retraction (Public Essential Evidence → Institutional)**
- Publisher objects to evidence extraction
- Evidence removed from public server, moved to institutional server
- Metadata update: `scimantic:accessLevel "public_essential_evidence"` → `"institutional"`
- Published hypothesis remains (cites DOI instead of semantic evidence)

**Scenario 4: Open Access Upgrade (Local → Public)**
- Original paper released under CC-BY (open access)
- Evidence can now be published as original contribution (no copyright issues)
- Metadata update: `scimantic:accessLevel "local"` → `"public"`

### Data Model: Access-Level-Agnostic Schema

**Core Insight**: All nanopubs use the same RDF structure (assertion + provenance + pubinfo). Access level is determined by **metadata**, not schema.

**Shared Schema** (all access levels):
```turtle
# Assertion Graph (identical across access levels)
:assertion_001 {
    :evidence_001 a scimantic:Evidence ;
        rdfs:label "DCS = 150 mb at E = 10 MeV" ;
        dcterms:source <https://doi.org/10.1234/smith2023> ;
        scimantic:hasUncertainty :uncertainty_001 .

    :uncertainty_001 a urref:UncertaintyEntity ;
        urref:hasNature urref:EpistemicUncertainty ;
        urref:hasType urref:Ambiguity ;
        urref:quantifiedAs "0.05"^^xsd:float .
}

# Provenance Graph (identical across access levels)
:provenance_001 {
    :assertion_001 prov:wasGeneratedBy :extraction_001 ;
        prov:generatedAtTime "2025-12-23T14:00:00Z"^^xsd:dateTime .
    :extraction_001 prov:wasAssociatedWith :researcher_emily .
}

# Publication Info Graph (VARIES by access level)
:pubinfo_001 {
    :np_001 a np:Nanopublication ;
        np:hasAssertion :assertion_001 ;
        np:hasProvenance :provenance_001 ;
        np:hasPublicationInfo :pubinfo_001 ;

        # ACCESS LEVEL METADATA (changes when moving between scopes)
        scimantic:accessLevel "local" ;  # or "institutional", "public", "public_essential_evidence"
        scimantic:publishable "false"^^xsd:boolean ;

        # SCOPE-SPECIFIC METADATA (added when published)
        # scimantic:publishedTo <https://nanopub.org/> ;
        # dcterms:license <https://creativecommons.org/licenses/by/4.0/> ;
        # scimantic:copyrightNotice "..." ;
}
```

**Access-Level Transition Workflow**:
1. Evidence created (Local scope)
2. User publishes hypothesis → Scimantic checks `prov:wasDerivedFrom` links
3. UI shows: "Evidence_001 is cited. Publish to public essential evidence scope?"
4. User confirms → `scimantic:accessLevel` updated to `"public_essential_evidence"`
5. Nanopub serialized and POSTed to public server
6. Metadata added: `scimantic:publishedTo`, `dcterms:license`, `scimantic:copyrightNotice`

### Implementation: Access-Level Vocabulary

**Ontology**:
```turtle
@prefix scimantic: <http://scimantic.io/ontology#> .

scimantic:accessLevel a owl:DatatypeProperty ;
    rdfs:label "Access level" ;
    rdfs:comment "Indicates the scope at which this nanopublication is accessible" ;
    rdfs:domain np:Nanopublication ;
    rdfs:range scimantic:AccessLevel .

scimantic:AccessLevel a owl:Class ;
    owl:oneOf ( "local" "institutional" "public" "public_essential_evidence" ) .

scimantic:publishable a owl:DatatypeProperty ;
    rdfs:label "Publishable" ;
    rdfs:comment "Whether this nanopub can be published to broader access levels" ;
    rdfs:domain np:Nanopublication ;
    rdfs:range xsd:boolean .

scimantic:publishedTo a owl:ObjectProperty ;
    rdfs:label "Published to" ;
    rdfs:comment "URIs of servers where this nanopub is published" ;
    rdfs:domain np:Nanopublication ;
    rdfs:range rdfs:Resource .

scimantic:legalBasis a owl:DatatypeProperty ;
    rdfs:label "Legal basis" ;
    rdfs:comment "Legal justification for publishing (e.g., fair_use_research, cc_by_license, original_work)" ;
    rdfs:domain np:Nanopublication ;
    rdfs:range xsd:string .

scimantic:copyrightNotice a owl:DatatypeProperty ;
    rdfs:label "Copyright notice" ;
    rdfs:comment "Legal notice for extracted evidence" ;
    rdfs:domain np:Nanopublication ;
    rdfs:range xsd:string .

scimantic:publishingRisk a owl:DatatypeProperty ;
    rdfs:label "Publishing risk" ;
    rdfs:comment "Legal risk assessment (low, medium, high)" ;
    rdfs:domain np:Nanopublication ;
    rdfs:range scimantic:RiskLevel .

scimantic:RiskLevel a owl:Class ;
    owl:oneOf ( "low" "medium" "high" ) .
```

### SPARQL Queries for Access-Level Management

**Find unpublished evidence cited by published hypotheses**:
```sparql
PREFIX scimantic: <http://scimantic.io/ontology#>
PREFIX prov: <http://www.w3.org/ns/prov#>

SELECT ?evidence ?hypothesis WHERE {
    ?hypothesis scimantic:accessLevel "public" .
    ?hypothesis prov:wasDerivedFrom ?evidence .
    ?evidence scimantic:accessLevel "local" .
}
```

**Find evidence eligible for public essential evidence scope** (open access, low risk):
```sparql
SELECT ?evidence WHERE {
    ?evidence a scimantic:Evidence ;
        scimantic:accessLevel "local" ;
        scimantic:sourceLicense <https://creativecommons.org/licenses/by/4.0/> ;
        scimantic:publishingRisk "low" .

    # Cited by published hypothesis
    ?hypothesis prov:wasDerivedFrom ?evidence ;
        scimantic:accessLevel "public" .
}
```

**Audit trail: What's published where?**:
```sparql
SELECT ?np ?accessLevel ?server WHERE {
    ?np scimantic:accessLevel ?accessLevel .
    OPTIONAL { ?np scimantic:publishedTo ?server }
}
ORDER BY ?accessLevel
```

## References

- [W3C PROV-O](https://www.w3.org/TR/prov-o/)
- [Nanopublications](http://nanopub.org/)
- [RDFLib Documentation](https://rdflib.readthedocs.io/)
- [MCP Specification](https://modelcontextprotocol.io/)
- [Trusty URIs](http://trustyuri.net/)
- [AIDA Principles for Nanopublications](https://www.tkuhn.org/pub/kuhn2013eswc.pdf)
- [Whyis Use Cases](http://tetherless-world.github.io/whyis/usecases.html)
