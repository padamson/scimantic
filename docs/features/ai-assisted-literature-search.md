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

**The Vision**: SemFlow captures literature as semantic RDF from the very first search, creating:
- **Queryable knowledge graph**: SPARQL queries across all evidence
- **W3C standards-based**: Built on PROV-O for provenance, enabling interoperability with existing semantic web tools
- **Provenance from day one**: Every piece of evidence linked to its source with metadata
- **Hypothesis traceability**: Later hypotheses can be explicitly derived from specific evidence nodes via `prov:wasDerivedFrom`
- **AI-assisted research**: MCP agents can search, summarize, and populate the graph
- **Visualization**: VS Code extension shows the growing evidence landscape

**Why This Matters**: This is the foundation of SemFlow's semantic publishing vision—research that is machine-readable from the very first literature search, not retrofitted at publication time.

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
- [x] semflow-core
- [ ] examples/semflow-paper (manual validation - deferred to Slice 2/3 with UI)

#### ✅ Acceptance Criteria

**What the system does:**
- [x] AI agent can add evidence via MCP tool with citation, content, and source
- [x] Evidence is persisted to `project.ttl` in Turtle format
- [x] Multiple evidence entries accumulate in the graph (append, not overwrite)

**What RDF structure exists:**
- [x] Evidence entity with types `semflow:Evidence` and `prov:Entity` (PROV-O provenance)
- [x] Citation stored as `dcterms:bibliographicCitation`
- [x] Content (summary/findings) stored as `semflow:content`
- [x] Source (DOI/URL) stored as `dcterms:source`
- [x] Creation timestamp stored as `prov:generatedAtTime` (PROV-O standard)

**What provenance is captured:**
- [x] Agent attribution via `prov:wasAttributedTo` (AI or human)
- [x] Queryable via SPARQL: "Who added this evidence and when?"

**What queries work:**
- [x] Find all evidence from papers published after date X
- [x] Find all evidence added by agent Y
- [x] Count total evidence entries in graph

#### 🛠️ Implementation Tasks

**Backend (semflow-core)**:
- [x] Models: `Evidence` entity with RDF persistence
- [x] Provenance: PROV-O tracking for evidence creation
- [x] MCP Tools: `add_evidence` tool for AI agent access
- [x] Tests: Unit tests for Evidence model
- [x] Tests: Integration test for MCP tool → RDF persistence

**Validation**:
- [x] SPARQL queries return expected evidence structure
- [x] Multiple evidence entries coexist in graph

---

### Slice 2: Extension Visualizes Evidence Graph
**Goal:** Researchers can view and explore their evidence graph in VS Code as they build their literature review.

**Why This Slice:** Visualization helps researchers understand the literature landscape they're building. Seeing evidence accumulate provides confidence and helps identify gaps or redundancies.

**Components:**
- [ ] semflow-core (MCP graph provider)
- [ ] semflow-ext
- [ ] examples/semflow-paper (validation)

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
- [ ] Filter evidence by date range
- [ ] Filter evidence by source

**What user confirmation workflow exists:**
- [ ] Before adding evidence, show preview modal with citation, content, and source
- [ ] User can edit suggested evidence content, citation, or source before accepting
- [ ] User can cancel without adding to knowledge graph
- [ ] Only after user clicks "Add to Graph" does `add_evidence()` get called
- [ ] Similar to Claude Code's "ask before edits" - human approval required for all graph modifications

#### 🛠️ Implementation Tasks

**Backend (semflow-core)**:
- [ ] MCP Tools: `get_provenance_graph` tool returns graph as JSON
- [ ] Tests: MCP tool returns correct graph structure

**Frontend (semflow-ext)**:
- [ ] UI: Evidence tree view provider
- [ ] UI: Detail view webview for selected evidence
- [ ] UI: Evidence preview/edit modal for user confirmation before adding
- [ ] MCP Client: Connection to semflow-core subprocess
- [ ] Commands: `semflow.refreshGraph`, `semflow.showEvidence`, `semflow.addEvidenceWithConfirmation`
- [ ] Tests: Tree view renders correctly
- [ ] Tests: Confirmation modal shows and allows editing

**Validation**:
- [ ] Manual testing shows evidence from examples/semflow-paper/project.ttl
- [ ] Adding new evidence updates view automatically

---

### Slice 3: Conversational Literature Search
**Goal:** Researchers converse with an AI agent to search literature and automatically populate the evidence graph.

**Why This Slice:** Conversational search drastically reduces the manual effort of literature review. The AI agent searches, summarizes, and populates the graph—all while maintaining full provenance.

**Components:**
- [ ] semflow-core (literature search MCP tool)
- [ ] semflow-ext (chat interface)
- [ ] examples/semflow-paper (validation)

#### ✅ Acceptance Criteria

**What the user does:**
- [ ] Types natural language query in VS Code chat (e.g., "Find papers on O2 ionization cross sections")
- [ ] Sees progress updates: "Searching... Found 5 papers... Adding 3 to graph..."
- [ ] Refines search with follow-up: "Focus on DCS calculations"

**What the agent does:**
- [ ] Searches Semantic Scholar API (or similar) for top N papers
- [ ] For each relevant paper, calls `add_evidence` with citation and summary
- [ ] Skips irrelevant results based on abstract content

**What appears in the graph:**
- [ ] Evidence nodes appear in tree view in real-time
- [ ] Each evidence has provenance: agent attribution, search query source
- [ ] Queryable: "Find all evidence from search query X"

**What queries work:**
- [ ] Find all evidence added during a specific chat session
- [ ] Find all evidence from papers on topic Y

**What user confirmation workflow exists:**
- [ ] Agent finds papers and extracts evidence, but does NOT automatically add to graph
- [ ] Shows user preview: "I found 5 papers. Here's evidence from the first: [citation/content preview]"
- [ ] User can review, edit suggested evidence, or skip individual papers
- [ ] User explicitly approves each addition: "Add this evidence" or "Add all 5"
- [ ] Conversational editing: User can say "Change the summary to..." and agent updates before adding
- [ ] Human-in-the-loop: All graph modifications require explicit user approval

#### 🛠️ Implementation Tasks

**Backend (semflow-core)**:
- [ ] MCP Tools: `search_literature` tool integrates with Semantic Scholar API
- [ ] Dependencies: HTTP client for API calls
- [ ] Tests: Mocked API responses for unit tests

**Frontend (semflow-ext)**:
- [ ] UI: Chat panel with input and message history
- [ ] UI: Evidence preview cards in chat with "Add" / "Edit" / "Skip" buttons
- [ ] MCP Client: Multi-tool orchestration (search → preview → user approval → add_evidence)
- [ ] UI: Progress indicators during search
- [ ] Commands: `semflow.startLiteratureSearch`, `semflow.previewEvidence`
- [ ] Tests: Chat workflow integration test
- [ ] Tests: User can edit evidence before approval

**Validation**:
- [ ] End-to-end test: user query → agent search → evidence in graph
- [ ] Manual testing with real Semantic Scholar queries

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

**SemFlow Documentation**:
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
@prefix semflow: <http://semflow.io/ontology#> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# Example Evidence entity (following semflow-core/ontology/semflow.ttl)
<http://example.org/research/semflow-paper/evidence/001> a semflow:Evidence, prov:Entity ;
    semflow:content "Nanopublications are the smallest unit of publishable information: an assertion with provenance and publication metadata." ;
    dcterms:bibliographicCitation "Kuhn, T., et al. (2016). Decentralized provenance-aware publishing with nanopublications. PeerJ Computer Science 2:e78." ;
    dcterms:source <https://doi.org/10.7717/peerj-cs.78> ;
    prov:generatedAtTime "2025-12-21T10:30:00Z"^^xsd:dateTime ;
    prov:wasAttributedTo <http://example.org/agent/claude> .
```

**Why these properties:**
- `semflow:Evidence`, `prov:Entity`: Dual typing enables both SemFlow-specific queries and standard PROV-O provenance tracking
- `semflow:content`: Searchable summary extracted from paper (SemFlow-specific property)
- `dcterms:bibliographicCitation`: Standard formatted citation for interoperability
- `dcterms:source`: DOI/URL linking to original publication
- `prov:generatedAtTime`: W3C PROV-O standard for temporal provenance
- `prov:wasAttributedTo`: W3C PROV-O standard for agent attribution

**Design note**: Evidence is a `prov:Entity` subclass (see `semflow-core/ontology/semflow.ttl`), enabling full PROV-O provenance chains from evidence → hypothesis → design → results.

### Expected SPARQL Queries

**What queries should work** once evidence is in the graph:

```sparql
# Find recent evidence
PREFIX semflow: <http://semflow.io/ontology#>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX dcterms: <http://purl.org/dc/terms/>

SELECT ?evidence ?citation ?timestamp WHERE {
    ?evidence a semflow:Evidence, prov:Entity ;
              dcterms:bibliographicCitation ?citation ;
              prov:generatedAtTime ?timestamp .
    FILTER(?timestamp > "2025-01-01T00:00:00Z"^^xsd:dateTime)
}
ORDER BY DESC(?timestamp)
```

```sparql
# Find evidence by agent
PREFIX semflow: <http://semflow.io/ontology#>
PREFIX prov: <http://www.w3.org/ns/prov#>

SELECT ?evidence ?citation WHERE {
    ?evidence a semflow:Evidence ;
              dcterms:bibliographicCitation ?citation ;
              prov:wasAttributedTo ?agent .
    FILTER(CONTAINS(STR(?agent), "claude"))
}
```

**Why these queries matter:**
- Temporal filtering supports "what evidence informed this hypothesis?"
- Agent filtering supports "what did AI contribute vs. manual entry?"
- PROV-O compatibility enables standard provenance tools to understand SemFlow graphs
- These queries validate that the RDF structure follows W3C standards while supporting research workflows

**Schema Reference**: See [semflow-core/ontology/semflow.ttl](../../semflow-core/ontology/semflow.ttl) for the complete ontology definition.
