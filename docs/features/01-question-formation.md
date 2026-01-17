# Feature: Question Formation

## User Story

> **As a** scientist initiating a research line
> **I want to** formulate clear, testable research questions through AI-assisted exploration of existing literature
> **So that** I can ground my research in specific, well-defined inquiries that connect to prior work and remain traceable throughout the research process

### The Problem

Scientific inquiry begins with curiosity, but curiosity alone doesn't drive systematic research. The critical first step—transforming vague interests into specific, answerable questions—is both essential and challenging:

- **Vagueness hurts focus**: "I wonder about protein folding" doesn't tell you what to measure, what literature to read, or what hypothesis to test
- **Isolated question formation**: Scientists refine questions in their heads or scratch notes, disconnected from the literature that could inform better questions
- **Lost context**: Informal notes ("why does this happen?") written months ago become meaningless when you can't remember what problem prompted them
- **Broken traceability**: When writing papers, researchers struggle to connect their evidence and conclusions back to the original questions that motivated the work
- **No grounding in source text**: Even when questions arise from reading papers, there's no link back to the specific passage that sparked the inquiry

### The Vision

Scimantic makes question formation an **iterative, literature-grounded process** where human insight and AI assistance work together:

- **Chat-based refinement**: Start with vague curiosity, collaborate with AI to sharpen into precise, answerable questions
- **Literature-informed iteration**: As you explore, relevant papers surface in real-time, helping you understand what's known and where gaps exist
- **Highlight-to-question workflow**: Read papers, highlight passages that spark questions, and capture questions with provenance linking back to the exact source text
- **Visual grounding**: See papers, highlights, and questions connected in a growing knowledge graph
- **Persistent knowledge**: Questions are stored as semantic entities that persist throughout the research lifecycle, anchoring the entire provenance tree

### Why This Matters

**For Researchers:**
- Formulate better questions by seeing what's already known
- Never lose track of why you started investigating something or what passage prompted it
- Revisit and refine questions as your understanding deepens

**For Human-AI Teaming:**
- AI surfaces relevant literature while you think through questions
- You read, highlight, and validate; AI helps organize and connect
- Multi-turn conversations maintain context across sessions
- Human judgment drives what matters; AI handles breadth and recall

**For the Scientific Method:**
- Explicit questions enforce the discipline of hypothesis-driven research
- Literature-grounded questions avoid reinventing the wheel
- Reproducibility: Other researchers see exactly what questions motivated each investigation and what source text informed them

### Position in Scientific Method

Question Formation sits at the beginning of the research cycle but **interweaves with Literature Search**—exploring literature helps refine questions, and refined questions guide further exploration:

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│   ┌──────────────────┐      ┌──────────────────┐     │
│   │ Question         │◄────►│ Literature       │     │
│   │ Formation        │      │ Search           │     │
│   └────────┬─────────┘      └────────┬─────────┘     │
│            │                         │               │
│            │ Questions inform        │ Evidence &    │
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
    Hypothesis → Design → Experiment → Analysis → Results
                                                      │
                        ┌─────────────────────────────┘
                        │ (new questions emerge)
                        ▼
                Question Formation (refined)
```

---

## Vertical Slices

### Slice 1: Question Capture via Chat

**Why**: Scientists need to capture research questions as persistent, traceable entities rather than ephemeral chat messages or scattered notes. This is the foundation—questions can be created through conversation without any literature integration.

**What the scientist experiences**:
- Engages with AI assistant (Claude Code, Cursor, VS Code Chat) to brainstorm and refine a vague curiosity into a specific question
- AI helps sharpen focus: "Are you asking about the kinetic pathway or thermodynamic stability?"
- Refined question is persisted to the knowledge graph with attribution and timestamp
- Question becomes the anchor for subsequent literature search and evidence collection

**Acceptance Criteria**:
- [ ] Conversational refinement: AI transforms vague prompts into specific, answerable questions
- [ ] Persistence: Questions stored as `scimantic:Question` entities in `project.ttl`
- [ ] Attribution: Questions linked to creating agent via `prov:wasAttributedTo`
- [ ] Provenance: `QuestionFormation` activity recorded with timestamp
- [ ] Queryable: SPARQL can retrieve questions by date, agent, or keyword

**Dogfooding**: Add questions about Scimantic's own design to `examples/scimantic-paper/project.ttl`

**Dependencies**: None (standalone slice)

---

### Slice 2: Question Visualization in Knowledge Graph

**Why**: Scientists need to see their questions as the roots of their research narrative, connected to the evidence and hypotheses that flow from them.

**What the scientist experiences**:
- Questions appear as top-level nodes in the knowledge graph visualization
- Can see which questions have motivated literature searches and evidence collection
- Can distinguish "open questions" (actively being investigated) from "answered" or "archived" questions
- Hovering or clicking shows full question text, creation date, and status

**Acceptance Criteria**:
- [ ] Tree view: Questions displayed as top-level groupings in sidebar
- [ ] Graph view: Questions rendered as root nodes with edges to motivated activities
- [ ] Status visibility: Visual distinction between open, answered, and archived questions
- [ ] Navigation: Clicking a question filters/focuses the graph to show related entities

**Dependencies**: Slice 1 (questions must exist to visualize)

---

### Slice 3: Literature Surfacing During Question Formation

**Why**: Scientists formulate better questions when they can see what's already known. Discovering existing research prevents reinventing the wheel and reveals genuine gaps worth investigating.

**What the scientist experiences**:
- While refining a question via chat, AI proactively surfaces relevant papers and findings
- Scientist sees paper titles, abstracts, and key claims that relate to their emerging question
- Can click through to read papers, helping inform whether the question is novel or needs refinement
- Question formation and literature exploration happen in the same flow, not as separate sequential steps

**Acceptance Criteria**:
- [ ] Contextual surfacing: AI brings relevant literature into view during question refinement
- [ ] Clickable sources: Scientist can open papers/URLs to verify relevance
- [ ] Informed refinement: Seeing existing work helps scientist sharpen or redirect questions
- [ ] Provenance linkage: `QuestionFormation --wasInformedBy--> LiteratureSearch` recorded when applicable

**Ontology alignment**: Uses `QuestionFormation.wasInformedBy` with range `LiteratureSearch`

**Dependencies**:
- Slice 1 (basic question capture)
- Literature Search Slice 1-2 (evidence capture and visualization must exist for surfacing to work)

---

### Slice 4: Highlight-to-Question Workflow

**Why**: The best research questions often arise while reading papers. Scientists need to capture the moment of insight—highlighting a passage and immediately formulating a question grounded in that specific text.

**What the scientist experiences**:
- While reading a paper (PDF or web), scientist highlights a passage that sparks a question
- Right-click or chat: "What question does this raise?"
- AI helps formulate a question based on the highlighted text
- Question is created with provenance linking to the annotation (exact text, page, source)
- The connection between question and source text is permanently traceable

**Acceptance Criteria**:
- [ ] Highlight capture: Selected text creates an `oa:Annotation` entity with `TextSelector`
- [ ] Question derivation: `Question --wasDerivedFrom--> Annotation` links question to source text
- [ ] Source context preserved: Annotation stores exact text, prefix/suffix, page number
- [ ] Bidirectional navigation: From question, can navigate to source passage; from highlight, can see derived questions
- [ ] AI assistance: Chat with highlighted text to refine the question formulation

**Ontology alignment**:
- `oa:Annotation` entity with `oa:TextQuoteSelector` (W3C Web Annotation Data Model)
- `Question.wasDerivedFrom` includes `Annotation` as valid range

**Dependencies**:
- Slice 1 (basic question capture)
- Literature Search Slice 3-4 (literature reading and annotation capabilities)

---

### Slice 4.5: Question Derivation from Evidence

**Why**: Questions don't only arise from raw highlights—they also emerge from articulated evidence claims. After extracting evidence from literature, a scientist might realize they have a follow-up question that the evidence raises but doesn't answer.

**What the scientist experiences**:
- Reviews evidence accumulated from literature search
- A particular evidence claim raises a new question
- AI helps formulate a question grounded in that evidence
- Question is created with provenance linking to the evidence
- Can trace from question back to evidence, and further to source annotations

**Acceptance Criteria**:
- [ ] Evidence-based questions: `Question --wasDerivedFrom--> Evidence` links question to evidence
- [ ] Multi-hop traceability: Can navigate Question → Evidence → Annotation → Source
- [ ] AI assistance: Chat about evidence to formulate questions it raises
- [ ] Distinction from annotation-based: Clear difference between "this passage raises a question" and "this claim raises a question"

**Ontology alignment**:
- `Question.wasDerivedFrom` includes `Evidence` as valid range (alongside `Question` and `Annotation`)

**Dependencies**:
- Slice 1 (basic question capture)
- Literature Search Slice 1.5 (evidence extraction must exist)

---

### Slice 5: Question Refinement and Versioning

**Why**: Research questions evolve as understanding deepens. Scientists need to refine questions while maintaining the provenance trail showing how their thinking developed—including what literature or highlights prompted changes.

**What the scientist experiences**:
- Can edit a question's text while preserving the original version
- Refinement creates a new question entity with `prov:wasDerivedFrom` linking to the original
- When refinement is prompted by reading literature, the annotation that sparked the change is also linked
- Can archive questions that are no longer relevant (soft delete)
- Can see the evolution of a question over time through the provenance graph

**Acceptance Criteria**:
- [ ] Edit with versioning: Updating a question creates a new version linked via `wasDerivedFrom`
- [ ] Multiple derivation sources: Refined question can link to both original question AND annotation that prompted change
- [ ] Archive capability: Questions can be marked inactive without deletion
- [ ] History visible: Provenance graph shows question evolution over time
- [ ] Informed by literature: `QuestionFormation --wasInformedBy--> LiteratureSearch` captures when refinement was prompted by literature discovery

**Dependencies**:
- Slice 1 (basic questions)
- Slice 2 (visualization to see history)
- Slice 4/4.5 (annotation/evidence-based derivation, optional but enriches provenance)

---

## Success Metrics

**Qualitative:**
- **Clarity**: Questions in the graph are more specific and actionable than initial prompts
- **Literature grounding**: Questions reflect awareness of existing work, not naive curiosity
- **Source traceability**: Questions can be traced back to specific passages that inspired them
- **Connectivity**: Evidence and hypotheses link back to questions, creating traceable research narratives
- **Iterative refinement**: Scientists naturally refine questions as they discover relevant literature

**Quantitative:**
- Percentage of questions that link to at least one literature search
- Percentage of questions that derive from annotations (highlight-to-question workflow adoption)
- Number of question refinement cycles per research project
- Percentage of evidence entities that trace back to a motivating question
