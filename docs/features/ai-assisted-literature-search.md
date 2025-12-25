# Feature: AI-Assisted Literature Search with Semantic Evidence Capture

## 📖 User Story
> **As a** scientist starting a new research project
> **I want to** search scientific literature with AI assistance and capture evidence as machine-readable RDF
> **So that** I can build a knowledge graph of prior work that serves as the semantic foundation for my hypotheses and is queryable throughout my research

### Narrative

**The Problem**: Traditional literature review involves manually searching databases (PubMed, Semantic Scholar, Google Scholar), reading papers, and taking notes in disconnected tools (Zotero, Mendeley, text documents). This creates several issues:
- Notes are not machine-readable
- No provenance linking evidence to later hypotheses
- Cannot query across papers programmatically
- Difficult for AI agents to assist with research

**The Vision**: Scimantic captures literature as semantic RDF from the very first search, creating:
- **Queryable knowledge graph**: SPARQL queries across all evidence
- **W3C standards-based**: Built on **nanopublications** and PROV-O, enabling interoperability
- **Provenance from day one**: Every piece of evidence linked to its source with metadata
- **Hypothesis traceability**: Later hypotheses can be explicitly derived from specific evidence nodes via `prov:wasDerivedFrom`
- **AI-assisted research**: MCP agents can search, summarize, and populate the graph
- **Visualization**: VS Code extension shows the growing evidence landscape

**Why This Matters**: This is the foundation of Scimantic's semantic publishing vision—research that is machine-readable from the very first literature search, not retrofitted at publication time.

### Scientific Method Stage
- [x] Literature Review
- [ ] Hypothesis Formation (enables this in later features)
- [ ] Experimental Design
- [ ] Experimentation
- [ ] Analysis
- [ ] Publication

---

## ✂️ Vertical Slices

### Slice 1: MCP Tool for Evidence Capture
**Goal:** Enable an AI agent to add evidence to the knowledge graph, persisting it as RDF with full provenance.

**Why This Slice:** Establishes the foundation for semantic literature review. Without machine-readable evidence capture, the rest of the workflow cannot provide provenance traceability.

**Components:**
- [ ] scimantic-core
- [ ] examples/scimantic-paper (manual validation - deferred to Slice 2/3 with UI)

**Note**: Existing code in `scimantic-core` and `scimantic-ext` is considered a **code spike**. These criteria are pending re-implementation after the formal `scimantic` ontology is defined.

#### ✅ Acceptance Criteria

**What the system does:**
- [ ] AI agent can add evidence via MCP tool with citation, content, and source
- [ ] Evidence is persisted to `project.ttl` in Turtle format
- [ ] Multiple evidence entries accumulate in the graph (append, not overwrite)

**What RDF structure exists:**
- [ ] Evidence entity (Assertion graph of a Nanopublication)
- [ ] Types `scimantic:Evidence` and `prov:Entity`
- [ ] Claim/Fact stored as `rdfs:label`
- [ ] Summary/Details stored as `scimantic:content` (optional)
- [ ] Source (DOI/URL) stored as `dcterms:source`
- [ ] Uncertainty initialized (e.g., via `scimantic:hasUncertainty`)
- [ ] Creation timestamp in Publication Info graph (`dcterms:created`)

**What provenance is captured:**
- [ ] Agent attribution via `prov:wasAttributedTo` (AI or human)
- [ ] Queryable via SPARQL: "Who added this evidence and when?"

**What queries work:**
- [ ] Find all evidence from papers published after date X
- [ ] Find all evidence added by agent Y
- [ ] Count total evidence entries in graph

#### 🛠️ Implementation Tasks

**Backend (scimantic-core)**:
- [ ] Models: `Evidence` entity with RDF persistence
- [ ] Provenance: PROV-O tracking for evidence creation
- [ ] MCP Tools: `add_evidence` tool for AI agent access
- [ ] Tests: Unit tests for Evidence model
- [ ] Tests: Integration test for MCP tool → RDF persistence

**Validation**:
- [ ] SPARQL queries return expected evidence structure
- [ ] Multiple evidence entries coexist in graph

---

### Slice 2: Extension Visualizes Evidence Graph
**Goal:** Researchers can view and explore their evidence graph in VS Code as they build their literature review.

**Why This Slice:** Visualization helps researchers understand the literature landscape they're building. Seeing evidence accumulate provides confidence and helps identify gaps or redundancies.

**Components:**
- [ ] scimantic-core (MCP graph provider)
- [ ] scimantic-ext (tree view + detail view)
- [ ] examples/scimantic-paper (validation)

#### ✅ Acceptance Criteria

**What the user sees:**
- [ ] "Knowledge Graph" panel appears in VS Code sidebar
- [ ] Tree view lists all Evidence nodes from `project.ttl`
- [ ] Each entry shows citation (label) and timestamp (description)
- [ ] Clicking an entry opens detail view with full content and source link
- [ ] Link to DOI/URL opens in browser

**What updates automatically:**
- [ ] Graph refreshes when `project.ttl` is modified
- [ ] New evidence appears in tree view without manual refresh

**What queries are supported:**
- [ ] **Group by Source**: Toggle to group evidence by `dcterms:source` (Paper/URL).
- [ ] **Paper Visualization**: Graph view renders "Paper" nodes linking to multiple "Evidence" nodes.
- [ ] Filter evidence by date range (deferred to future enhancement)
- [ ] Filter evidence by source (deferred to future enhancement)

**What user confirmation workflow exists:**
- [ ] Before adding evidence, show preview modal with citation, content, and source (deferred to Slice 3)
- [ ] User can edit suggested evidence content, citation, or source before accepting (deferred to Slice 3)
- [ ] User can cancel without adding to knowledge graph (deferred to Slice 3)
- [ ] Only after user clicks "Add to Graph" does `add_evidence()` get called (deferred to Slice 3)
- [ ] Similar to Claude Code's "ask before edits" - human approval required for all graph modifications (deferred to Slice 3)

**Note:** User confirmation workflow is deferred to Slice 3 (Agentic Literature Search) where AI agent interactions make it most relevant.

#### 🛠️ Implementation Tasks

**Backend (scimantic-core)**:
- [ ] MCP Tools: `get_provenance_graph_json()` function returns graph as JSON
- [ ] Tests: MCP tool returns correct graph structure
- [ ] Configuration: Centralized namespace URIs in `config.py`

**Frontend (scimantic-ext)**:
- [ ] UI: Evidence tree view provider (`EvidenceTreeDataProvider`)
- [ ] UI: Detail view webview for selected evidence
- [ ] UI: Evidence preview/edit modal for user confirmation before adding (deferred to Slice 3)
- [ ] MCP Client: Connection to scimantic-core subprocess via `uv run python`
- [ ] Commands: `scimantic.refreshGraph`, `scimantic.showEvidence`, `scimantic.openSource`
- [ ] Tests: Tree view renders correctly
- [ ] Tests: MCP client integration tests

**Validation**:
- [ ] Manual testing shows evidence from examples/scimantic-paper/project.ttl
- [ ] Adding new evidence updates view automatically

#### 📋 Manual Testing Instructions

**Prerequisites:**
1. Ensure `uv` is installed and scimantic-core dependencies are installed
2. Open VS Code in the scimantic monorepo workspace
3. Have the scimantic-ext extension loaded in development mode

**Test 1: View existing evidence**
```bash
# From monorepo root
cd examples/scimantic-paper

# Add some test evidence using scimantic-core
uv run python -c "
from scimantic.mcp import add_evidence
add_evidence(
    content='Nanopublications are the smallest unit of publishable information.',
    citation='Kuhn, T., et al. (2016). Decentralized provenance-aware publishing with nanopublications.',
    source='https://doi.org/10.7717/peerj-cs.78',
    agent='http://example.org/agent/manual-test',
    project_path='project.ttl'
)
"
```

**Expected:**
- Scimantic panel appears in VS Code activity bar (graph icon)
- "Knowledge Graph" tree view shows the evidence entry
- Citation is displayed as the label
- Timestamp is shown as description
- Clicking the entry opens a webview with full content and clickable source link

**Test 2: Auto-refresh on file change**
```bash
# Add another evidence entry
uv run python -c "
from scimantic.mcp import add_evidence
add_evidence(
    content='RDF provides a semantic framework for knowledge representation.',
    citation='Lassila, O., & Swick, R. R. (1999). Resource Description Framework.',
    source='https://www.w3.org/TR/rdf-primer/',
    agent='http://example.org/agent/manual-test',
    project_path='project.ttl'
)
"
```

**Expected:**
- Tree view automatically refreshes
- New evidence appears without manual action
- File watcher detects change to project.ttl

**Test 3: Manual refresh**
- Click the refresh icon in the tree view toolbar

**Expected:**
- Tree view reloads from project.ttl
- All evidence entries are displayed correctly

**Test 4: Detail view**
- Click on any evidence entry in the tree

**Expected:**
- Webview panel opens showing:
  - Citation as heading
  - Full content text
  - Clickable source URL
  - Metadata (URI, timestamp, agent)
- Clicking source URL opens in external browser

**Known Limitations (to be addressed in Slice 3):**
- No filtering by date or source yet
- No user confirmation workflow for adding evidence
- MCP client uses direct subprocess instead of proper MCP protocol

---

### Slice 3: Agentic Literature Search
**Goal:** Researchers use their preferred AI agent (Claude, Cursor, etc.) to search literature and populate the evidence graph.

**Why This Slice:** Leveraging existing powerful agents via MCP avoids building a custom chat interface while enabling complex reasoning and search workflows.

**Components:**
- [ ] scimantic-core (literature search MCP tool)
- [ ] scimantic-ext (passive visualization only)
- [ ] examples/scimantic-paper (validation)

#### ✅ Acceptance Criteria

**What the user does:**
- [ ] Prompts their agent: "Find papers on O2 ionization cross sections and add the key evidence."
- [ ] Agent performs search, summarizes findings, and calls `add_evidence` tool.

**What the agent does (via MCP):**
- [ ] Calls `search_literature` (Semantic Scholar API).
- [ ] Summarizes findings into RDF-compatible text.
- [ ] Calls `add_evidence` for selected items.

**What appears in the graph:**
- [ ] Evidence nodes appear in the "Knowledge Graph" panel in real-time.
- [ ] Provenance tracks the Agent URI (e.g., `urn:agent:claude`).

**Visual Feedback / User Confirmation:**
- [ ] Since the Chat UI is external, Scimantic does not control the "preview card".
- [ ] Scimantic provides a `preview_evidence_batch` tool that agents CAN use to show structured data if they choose.
- [ ] Primary feedback is the **Knowledge Graph Panel** updating in real-time.

#### 🛠️ Implementation Tasks

**Backend (scimantic-core)**:
- [ ] MCP Tools: `search_literature` tool integrates with Semantic Scholar API.
- [ ] MCP Tools: `preview_knowledge_graph_update` (dry run).
- [ ] Dependencies: `requests` or `httpx` for API calls.

**Frontend (scimantic-ext)**:
- [ ] UI: Ensure Graph View handles rapid batch updates smoothly.
- [ ] No custom chat UI required.

**Validation**:
- [ ] End-to-end test using an MCP client (e.g. Claude Desktop or a mock script) to drive the search-and-add loop.

---

### Slice 4: PDF Visualization & Retrieval (Advanced)
**Goal**: Visualizing the source PDF directly within the IDE, enabling researchers to verify evidence in its original context.

**Features**:
- [ ] **PDF Viewer**: Embed a PDF viewer (e.g., PDF.js) in a VS Code Webview.
- [ ] **Document Retrieval**: Download/cache PDFs from open access sources (ArXiv, etc.) linked to the Evidence.
- [ ] **Page Navigation**: Clicking evidence in the Graph Panel jumps to the specific page in the PDF.

### Slice 5: Human-AI Grounding (Advanced)
**Goal**: Bi-directional linking between the structured Knowledge Graph and the unstructured PDF text.

**Features**:
- [ ] **Visual Grounding**: Highlight the specific sentence/paragraph in the PDF that corresponds to the `scimantic:Evidence`.
- [ ] **Coordinate Mapping**: Store PDF coordinates (page, bounding box) in the RDF data (e.g., using Web Annotation Data Model).
- [ ] **Contextual Verification**: User approves AI extraction by seeing the highlighted text in the source PDF.
- [ ] **Highlight-to-Evidence Workflow**: User highlights text in PDF -> "Add as Evidence" context menu -> Agent drafts `scimantic:Evidence` with citation and content pre-filled from highlight.

---

## 🎯 Success Metrics

- **Semantic Completeness**: Can SPARQL queries extract all citations, authors, and sources without ambiguity?
  - Example query: "Find all evidence from papers published after 2020"
- **Provenance Coverage**: Is it clear who (human or AI) added each evidence and when?
- **AI Agent Usability**: Can an AI agent autonomously populate the evidence graph given a research topic?
- **User Productivity**: Does the integrated search reduce time spent manually organizing literature?
- **Reproducibility**: Can another researcher understand the literature foundation by querying `project.ttl` alone?
- **Graph Quality**: Are evidence nodes later successfully linked to hypotheses in Phase 1?

**Quantitative Metrics** (after deployment):
- Number of evidence entries added per research project
- Time from project start to first hypothesis (should decrease with good evidence)
- Percentage of hypotheses with explicit `prov:wasDerivedFrom` links to evidence

---

## 🔗 Dependencies

**RDF/OWL Libraries**:
- RDFLib (Python) for graph manipulation
- Turtle serialization format for `project.ttl`

**W3C Standards**:
- PROV-O: `prov:wasAttributedTo`, `prov:generatedAtTime`
- Dublin Core Terms: `dcterms:bibliographicCitation`, `dcterms:source`, `dcterms:created`

**MCP Integration**:
- Model Context Protocol SDK (Python) for server
- MCP Client SDK (TypeScript) for VS Code extension

**VS Code Extension APIs**:
- TreeDataProvider for evidence list
- Webview for detail view
- Chat API (optional for Slice 3)

**External Services**:
- Semantic Scholar API (free tier): https://www.semanticscholar.org/product/api
- Alternative: OpenAlex, CrossRef, PubMed E-utilities
- DOI resolution via doi.org

**Scientific Computing**:
- None for this feature (literature search only)

---

## 📚 Reference Materials

**W3C Standards**:
- [PROV-O Specification](https://www.w3.org/TR/prov-o/) - Provenance ontology
- [Dublin Core Metadata](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/) - Citation metadata

**APIs**:
- [Semantic Scholar API Docs](https://api.semanticscholar.org/)
- [CrossRef REST API](https://www.crossref.org/documentation/retrieve-metadata/rest-api/)

**Scimantic Documentation**:
- [CLAUDE.md](../../CLAUDE.md) - Developer guide, TDD patterns
- [README.md](../../README.md) - Project overview

**Related Features**:
- (Future) `hypothesis-formation.md` - Will build on evidence graph from this feature

**Nanopublications**:
- [Nanopub Guidelines](http://nanopub.org/guidelines/) - For future enhancement: wrap evidence as nanopubs

---

## Expected RDF Structure

### Evidence Entity Schema

**What RDF triples should exist** for each Evidence entity:

```turtle
@prefix scimantic: <http://scimantic.io/ontology#> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix np: <http://www.nanopub.org/nschema#> .

# 1. Assertion Graph
:assertion_001 {
    :evidence_001 a scimantic:Evidence, prov:Entity ;
        rdfs:label "Nanopublications are the smallest unit of publishable information." ;
        scimantic:content "Nanopublications allow for decentralized provenance-aware publishing..." ;
        dcterms:source <https://doi.org/10.7717/peerj-cs.78> ;
        scimantic:hasUncertainty :uncertainty_001 .
}

# 2. Provenance Graph
:provenance_001 {
    :assertion_001 prov:wasGeneratedBy :literature_search_001 .
    :literature_search_001 a scimantic:LiteratureSearch, prov:Activity ;
        prov:wasAssociatedWith :ai_agent_claude .
}

# 3. PubInfo Graph
:pubinfo_001 {
    :np_001 a np:Nanopublication ;
        np:hasAssertion :assertion_001 ;
        np:hasProvenance :provenance_001 ;
        dcterms:created "2025-12-21T10:30:00Z"^^xsd:dateTime ;
        dcterms:bibliographicCitation "Kuhn, T. (2016)..." .
}
```

**Why these properties:**
- **Nanopub Structure**: Architecture mandates Nanopublications (Assertion/Provenance/PubInfo).
- `scimantic:Evidence`: The core entity in the assertion.
- `rdfs:label`: The primary claim/fact (compatible with standard display tools).
- `scimantic:LiteratureSearch`: The specific activity type (subclass of `prov:Activity`).

### Expected SPARQL Queries

**What queries should work** once evidence is in the graph:

```sparql
# Find recent evidence
PREFIX scimantic: <http://scimantic.io/ontology#>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?evidence ?citation ?timestamp WHERE {
    ?evidence a scimantic:Evidence, prov:Entity ;
              dcterms:bibliographicCitation ?citation ;
              prov:generatedAtTime ?timestamp .
    FILTER(?timestamp > "2025-01-01T00:00:00Z"^^xsd:dateTime)
}
ORDER BY DESC(?timestamp)
```

```sparql
# Find evidence by agent
PREFIX scimantic: <http://scimantic.io/ontology#>
PREFIX prov: <http://www.w3.org/ns/prov#>

SELECT ?evidence ?citation WHERE {
    ?evidence a scimantic:Evidence ;
              dcterms:bibliographicCitation ?citation ;
              prov:wasAttributedTo ?agent .
    FILTER(CONTAINS(STR(?agent), "claude"))
}
```

**Why these queries matter:**
- Temporal filtering supports "what evidence informed this hypothesis?"
- Agent filtering supports "what did AI contribute vs. manual entry?"
- PROV-O compatibility enables standard provenance tools to understand Scimantic graphs
- These queries validate that the RDF structure follows W3C standards while supporting research workflows

**Schema Reference**: See [scimantic-core/ontology/scimantic.ttl](../../scimantic-core/ontology/scimantic.ttl) for the complete ontology definition.
