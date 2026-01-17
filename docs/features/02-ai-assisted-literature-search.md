# Feature: AI-Assisted Literature Search with Semantic Evidence Capture

## User Story

> **As a** scientist building on prior work
> **I want to** search, read, and annotate scientific literature with AI assistance, capturing evidence as machine-readable RDF
> **So that** I can build a queryable knowledge graph of prior work that grounds my hypotheses in traceable, semantically-rich evidence

### The Problem

Traditional literature review involves manually searching databases (PubMed, Semantic Scholar, Google Scholar), reading papers, and taking notes in disconnected tools (Zotero, Mendeley, text documents). This creates several issues:

- **Notes are not machine-readable**: Highlights and annotations live in PDF readers or text files, disconnected from research workflows
- **No provenance to source text**: When you extract a fact from a paper, you lose the link to the exact passage it came from
- **Cannot query across papers**: No way to ask "what do all my sources say about X?"
- **Difficult for AI to assist**: AI agents can't access or build on your literature notes
- **Evidence-hypothesis gap**: When forming hypotheses later, you can't trace back to which specific evidence informed them

### The Vision

Scimantic captures literature as semantic RDF from the very first search, with annotations grounding evidence in source text:

- **Read and annotate in context**: View papers (PDF or web), highlight passages, chat with selected text
- **Highlight-to-evidence workflow**: Select text → AI extracts the claim → evidence is created with provenance linking to the exact passage
- **Queryable knowledge graph**: SPARQL queries across all evidence ("What do my sources say about protein folding kinetics?")
- **License-aware capture**: Track whether evidence comes from open-access (CC-BY) or restricted sources
- **AI-assisted extraction**: AI agents can search literature, summarize findings, and help populate the graph
- **Visual feedback**: Watch your evidence landscape grow in the knowledge graph visualization

### Why This Matters

**For Researchers:**
- Never lose the connection between a claim and its source passage
- Query your literature review programmatically
- Build on prior work with full traceability

**For Human-AI Teaming:**
- AI searches and summarizes; you read, validate, and highlight
- Highlights become evidence with AI helping to articulate the claim
- Human judgment drives what's important; AI handles scale

**For the Scientific Method:**
- Evidence-based hypothesis formation becomes explicit and traceable
- Reproducibility: Others can see exactly what literature informed your work
- License awareness enables responsible subset publishing

### Position in Scientific Method

Literature Search **interweaves with Question Formation**—questions guide searches, and discovered evidence informs question refinement:

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│   ┌──────────────────┐      ┌──────────────────┐     │
│   │ Question         │◄────►│ Literature       │     │
│   │ Formation        │      │ Search           │ ← You are here
│   └────────┬─────────┘      └────────┬─────────┘     │
│            │                         │               │
│            │ Questions motivate      │ Evidence &    │
│            │ literature search       │ Annotations   │
│            │                         │ inform        │
│            │                         │ questions     │
│            └──────────┬──────────────┘               │
│                       │                              │
│              motivates & generates                   │
│                       ▼                              │
└──────────────────────────────────────────────────────┘
                        │
                        ▼
                   Evidence
                        │
                        ▼
               EvidenceAssessment → Premise
                        │
                        ▼
               HypothesisFormation → Hypothesis
```

---

## Vertical Slices

### Slice 1: Annotation Capture via MCP Tool

**Why**: The foundation for semantic literature review. Annotations (highlights, notes) capture the specific passages in source documents that will later become evidence or spawn questions. This separates the act of reading/highlighting from the act of articulating claims.

**What the scientist experiences**:
- Uses AI assistant while reading a paper
- Highlights a passage that seems important
- AI creates an annotation with the exact text, surrounding context, and source reference
- Annotations accumulate as the scientist reads, creating a trail of source material

**Acceptance Criteria**:
- [ ] Annotation capture: AI can create annotations via MCP tool with exact text, prefix/suffix context, and source
- [ ] Persistence: Annotations stored as `oa:Annotation` entities in `project.ttl`
- [ ] W3C compliance: Annotations use `oa:TextQuoteSelector` for text selection
- [ ] Attribution: Annotations linked to creating agent via `prov:wasAttributedTo`
- [ ] Activity tracking: `LiteratureSearch` activity recorded with timestamp
- [ ] Queryable: SPARQL can retrieve annotations by source, date, or agent

**Dogfooding**: Add annotations from reading nanopublication and provenance literature to `examples/scimantic-paper/project.ttl`

**Dependencies**: None (foundational slice)

---

### Slice 1.5: Evidence Extraction from Annotations

**Why**: Evidence claims should be articulated separately from source annotation. A single evidence claim may synthesize multiple annotations from different sources, and the same annotation might inform multiple evidence claims. This separation provides more degrees of freedom in the research process.

**What the scientist experiences**:
- Reviews accumulated annotations from reading
- AI helps articulate a specific evidence claim based on one or more annotations
- Evidence is created with provenance linking to source annotations
- Can combine insights from multiple papers into a single evidence statement

**Acceptance Criteria**:
- [ ] Evidence extraction: AI can create evidence via MCP tool with content, citation, source, and license
- [ ] Multi-annotation support: Evidence can derive from multiple annotations (`prov:wasDerivedFrom`)
- [ ] Persistence: Evidence stored as `scimantic:Evidence` entities in `project.ttl`
- [ ] Nanopublication structure: Evidence wrapped in Assertion/Provenance/PubInfo graphs
- [ ] Activity tracking: `EvidenceExtraction` activity links to source `LiteratureSearch` via `wasInformedBy`
- [ ] License tracking: `dcterms:license` captured (CC-BY, AllRightsReserved, etc.)
- [ ] Queryable: SPARQL can retrieve evidence by source annotation, date, agent, or license

**Dogfooding**: Extract evidence about nanopublications and provenance from annotations in `examples/scimantic-paper/project.ttl`

**Dependencies**: Slice 1 (annotations must exist to extract evidence from)

---

### Slice 2: Annotation and Evidence Visualization in Knowledge Graph

**Why**: Visualization helps researchers understand the literature landscape they're building. Seeing annotations and evidence accumulate provides confidence and helps identify gaps or clusters. The visual distinction between "raw" annotations and "articulated" evidence helps track the extraction workflow.

**What the scientist experiences**:
- Annotations and evidence appear in the knowledge graph panel as they're added
- Can browse by source (grouped by paper), by type (annotation vs evidence), or chronologically
- Clicking an annotation shows: exact text, surrounding context, source link
- Clicking evidence shows: content, citation, source annotations, license
- Can navigate from evidence to source annotations and vice versa

**Acceptance Criteria**:
- [ ] Tree view: Annotations and evidence displayed in sidebar, grouped by source or date
- [ ] Type distinction: Visual differentiation between annotations (highlights) and evidence (claims)
- [ ] Detail view: Full metadata shown for both annotations and evidence
- [ ] Provenance navigation: From evidence, can see source annotations; from annotations, can see derived evidence
- [ ] Auto-refresh: Graph updates when `project.ttl` is modified
- [ ] Source navigation: Clicking source URL opens the paper
- [ ] License visibility: Clear indication of evidence license status

**Dependencies**: Slice 1 and 1.5 (annotations and evidence must exist to visualize)

**Enables**: Question Formation Slice 3 (literature surfacing during question formation)

---

### Slice 3: Literature Reading (PDF and Web)

**Why**: Scientists need to read papers in context to extract meaningful evidence. Viewing literature within the research environment enables seamless annotation and evidence capture.

**What the scientist experiences**:
- Opens a paper (PDF or web URL) within VS Code
- Reads the paper with standard navigation (scroll, page jump, zoom)
- Papers are cached locally for offline access and to minimize accessing the same paper multiple times (when permitted by license)
- Can switch between multiple open papers

**Acceptance Criteria**:
- [ ] PDF viewing: Embedded PDF viewer (PDF.js or similar) in VS Code webview
- [ ] Web viewing: Render web articles in embedded browser
- [ ] Navigation: Page navigation, zoom, scroll, search within document
- [ ] Caching: Downloaded papers cached locally (respecting license)
- [ ] Source linking: Papers linked to evidence that cites them

**Dependencies**: Slice 1-2 (evidence system to connect papers to)

---

### Slice 4: Interactive Highlight-to-Evidence Workflow

**Why**: The best evidence extraction happens while reading. Scientists need to capture the moment of insight—highlighting a passage and immediately extracting evidence grounded in that specific text. This slice combines annotation capture (Slice 1) and evidence extraction (Slice 1.5) into a seamless interactive workflow.

**What the scientist experiences**:
- While reading a paper, highlights a passage containing a key claim
- Right-click or chat: "Extract this as evidence"
- AI creates the annotation automatically, then helps articulate the evidence claim
- Can combine multiple highlights into a single evidence statement
- Evidence is created with provenance linking to the annotation(s)
- The connection between evidence and source passage is permanently traceable

**Acceptance Criteria**:
- [ ] Text selection: User can select/highlight text in PDF or web view
- [ ] Inline annotation: Selection creates an `oa:Annotation` entity with `TextSelector` (reuses Slice 1)
- [ ] Evidence extraction: `Evidence --wasDerivedFrom--> Annotation` links evidence to source text (reuses Slice 1.5)
- [ ] Multi-highlight support: Can select multiple passages before articulating evidence
- [ ] Context preservation: Annotation stores exact text, prefix/suffix, page number
- [ ] AI assistance: Chat with highlighted text to refine the evidence articulation
- [ ] Bidirectional navigation: From evidence, navigate to source passage; from annotation, see derived evidence

**Ontology alignment**:
- `oa:Annotation` entity with `oa:TextQuoteSelector` (W3C Web Annotation Data Model)
- `scimantic:EvidenceExtraction` activity links `LiteratureSearch` to `Evidence`
- `Evidence.wasDerivedFrom` includes `Annotation` as valid range

**Dependencies**: Slice 1, 1.5, 3 (annotation + evidence extraction + literature reading)

**Enables**: Question Formation Slice 4 (highlight-to-question workflow uses same annotation infrastructure)

---

### Slice 5: Agentic Literature Search

**Why**: AI agents excel at breadth—searching across databases, summarizing findings, identifying relevant papers. Scientists guide the search; AI handles scale.

**What the scientist experiences**:
- Prompts AI: "Find papers on O₂ ionization cross sections and summarize what methods they use"
- AI searches literature databases (Semantic Scholar, etc.), summarizes findings
- AI offers to add key evidence from discovered papers
- Scientist reviews and approves evidence additions
- Evidence accumulates in the graph with provenance tracking the AI agent

**Acceptance Criteria**:
- [ ] Search capability: AI can search literature databases via MCP tool
- [ ] Summarization: AI summarizes findings before offering to add evidence
- [ ] Human approval: Scientist reviews AI-proposed evidence before addition
- [ ] Agent attribution: Evidence tracks which AI agent added it (`prov:wasAttributedTo`)
- [ ] Batch operations: Can add multiple evidence entries from a search session

**Dependencies**: Slice 1, 1.5, 2 (annotation capture, evidence extraction, and visualization)

---

## Cross-Feature Dependencies

This feature provides capabilities that **Question Formation** depends on:

| Literature Search Slice | Enables Question Formation |
|------------------------|---------------------------|
| Slice 1, 1.5, 2 (Annotation, evidence extraction & viz) | Slice 3 (Literature surfacing during question formation) |
| Slice 3-4 (Reading & interactive highlight workflow) | Slice 4 (Highlight-to-question workflow) |

Both features share the **Annotation** infrastructure from the ontology.

### Activity Flow

```
LiteratureSearch ──generates──► Annotation
                                    │
                                    ▼
                           EvidenceExtraction ──generates──► Evidence
                                    │
                                    ▼
                           EvidenceAssessment ──generates──► Premise
```

---

## Success Metrics

**Qualitative:**
- **Source traceability**: Evidence can be traced back to specific passages in source documents
- **Semantic completeness**: SPARQL queries extract all citations, sources, and claims without ambiguity
- **Human-AI collaboration**: Scientists guide extraction; AI handles articulation and organization
- **License awareness**: Clear visibility into what evidence can be published in subsets
