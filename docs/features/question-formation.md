# Feature: Question Formation

## 📖 User Story
> **As a** scientist initiating a research line
> **I want to** formulate clear, testable research questions with AI assistance
> **So that** I can ground my subsequent literature search and hypothesis formation in specific, well-defined inquiries that remain traceable throughout the research process

### Narrative

#### The Problem

Scientific inquiry begins with curiosity, but curiosity alone doesn't drive systematic research. The critical first step—transforming vague interests into specific, answerable questions—is both essential and challenging:

- **Vagueness hurts focus**: "I wonder about protein folding" doesn't tell you what to measure, what literature to read, or what hypothesis to test
- **Lost context**: Informal notes ("why does this happen?") written months ago become meaningless when you can't remember what problem prompted them
- **Broken traceability**: When writing papers, researchers struggle to connect their evidence and conclusions back to the original questions that motivated the work
- **AI inefficiency**: Generic prompts to AI assistants yield generic results; specific questions enable targeted, valuable responses

#### The Vision

Scimantic makes research questions first-class citizens of the knowledge graph:

- **AI-assisted refinement**: Start with vague curiosity ("protein folding is weird"), collaborate with AI to refine it into precise questions ("What is the kinetic folding pathway of Protein X under heat stress conditions (T > 45°C)?")
- **Persistent knowledge**: Questions are stored as semantic entities that persist throughout the research lifecycle, not ephemeral chat messages
- **Provenance root**: Questions anchor the provenance tree—every piece of evidence, hypothesis, and result traces back to the question it helps answer
- **Workflow catalyst**: Questions motivate literature searches, which generate evidence, which informs hypotheses, creating a connected research narrative

#### Why This Matters

**For Researchers:**
- Never lose track of why you started investigating something
- Revisit and refine questions as your understanding deepens
- Generate comprehensive methods sections automatically from the provenance graph

**For AI Agents:**
- Well-defined questions provide clear search criteria for literature extraction
- Questions establish success criteria for evidence relevance
- Multi-turn conversations maintain context across sessions

**For the Scientific Method:**
- Explicit questions enforce the discipline of hypothesis-driven research
- Feedback loops: Results from one investigation can generate refined questions for the next iteration
- Reproducibility: Other researchers can see exactly what questions motivated each investigation

### Position in Scientific Method

Question Formation sits at the beginning of the research cycle but isn't strictly linear—results often prompt new questions:

```
┌──────────────────┐
│ Question         │ ← You are here
│ Formation        │
└────────┬─────────┘
         │ motivates
         ▼
┌──────────────────┐
│ Literature       │
│ Search           │
└────────┬─────────┘
         │ generates
         ▼
    Evidence
         │
         ▼
    Hypothesis → Design → Experiment → Analysis → Results
         │                                             │
         │            ┌────────────────────────────────┘
         │            │ (new questions emerge)
         │            ▼
         └──────── Question Formation (refined)
```

---

## ✂️ Vertical Slices

### Slice 1: Conversational Question Elicitation

**Goal**: User chats with AI to brainstorm and refine a research question, which is then persisted to the graph.

**Workflow**:
1.  User opens their preferred AI coding assistant (VS Code Chat, Cursor, Claude Code, etc.).
2.  User: "I'm interested in why this protein folds weirdly."
3.  AI (using **Question Formation Activity** context): "Are you focusing on the kinetic pathway or the thermodynamic stability? Specifically, are you asking about..."
4.  User: "The kinetic pathway under heat stress."
5.  AI: "Proposed Question: *What is the kinetic folding pathway of Protein X under heat stress conditions (T > 45°C)?*"
6.  User: "Yes, add that."
7.  AI calls `add_question` tool.

**Acceptance Criteria**:
- [x] User can brainstorm research questions conversationally with AI
- [x] AI refines vague prompts into specific, answerable questions
- [x] Refined questions are persisted to knowledge graph
- [x] Questions are attributed to the creating agent (human or AI)
- [x] Questions include timestamps showing when they were formulated
- [ ] Questions appear in VS Code tree view sidebar
- [ ] User can review question history across sessions

### Slice 2: Question Visualization & Context

**Goal**: Visualize the Question as the root of the research graph.

**Features**:
- [ ] **Tree View** (Sidebar): Displays Questions as top-level groupings.
- [ ] **Graph Visualization** (Webview): Renders Question nodes as the roots of the node-link diagram.
- [ ] Dashboard: "Open Questions" vs "Answered Questions".

### Slice 3: Graph Interaction & Refinement

**Goal**: Users can explore and refine the graph visually.

**Features**:
- [ ] **Hover Details**: Hovering over a Question node shows full text, date, and status.
- [ ] **Label Toggles**: Toggle edge labels (e.g., `prov:wasDerivedFrom`) on/off to reduce clutter.
- [ ] **Node Filtering**: Filter graph to show only Questions matching keywords or date ranges.
- [ ] **Interactive Layout**: Drag nodes to rearrange the visualization (force-directed graph).

### Slice 4: Question Management & Editing

**Goal**: Users can maintain the quality of their research questions over time.

**Features**:
- [ ] **Edit Question**: Context menu on node -> "Edit Question". Updates `rdfs:label` and adds versioning provenance.
- [ ] **Archive/Delete**: "Archive" questions that are no longer relevant (status change, not deletion).
- [ ] **Merge Questions**: Combine duplicate questions into a single node with multiple `prov:wasDerivedFrom` sources.

---

## 🎯 Success Metrics

**Qualitative:**
- **Clarity**: Questions stored in the graph are more specific and actionable than user's initial prompts
- **Connectivity**: Evidence and Hypotheses link back to Questions, creating traceable research narratives
- **Persistence**: Questions remain accessible across sessions, maintaining research context
- **Refinement**: Users iteratively improve questions based on preliminary findings

**Quantitative:**
- Reduction in "what was I investigating?" moments (tracked via user surveys)
- Number of Questions that successfully motivate Literature Searches
- Percentage of Evidence entities that trace back to a Question
