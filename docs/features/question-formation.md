# Feature: Question Formation

## 📖 User Story
> **As a** scientist initiating a research line
> **I want to** formulate clear, testable research questions with AI assistance
> **So that** I can ground my subsequent literature search and hypothesis formation in specific, well-defined inquiries

### Narrative

**The Problem**: Research often starts with vague curiosity. Refining this into specific, answerable scientific questions is a critical but difficult creative step. Informal notes about "what I'm wondering" don't connect to the evidence or results that eventually answer them.

**The Vision**: Scimantic helps the user brainstorm and refine questions. These questions become first-class entities (`scimantic:Question`) in the knowledge graph, serving as the root of the provenance tree.

**Why This Matters**:
*   Anchors the research: "Why did we gather this evidence? To answer Question X."
*   Feedback loops: Results can generate *new* Questions (refinement).
*   AI Context: Clearly defined questions help AI agents filter literature more effectively.

### Scientific Method Stage
- [ ] Literature Review
- [x] Question Formation (Root of the cycle, often concurrent with Lit Review)
- [ ] Hypothesis Formation
- [ ] Experimental Design
- [ ] Experimentation
- [ ] Analysis
- [ ] Publication

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

45: **Acceptance Criteria**:
46: - [x] User can brainstorm via chat.
47: - [x] AI suggests refined, precise questions.
48: - [x] `scimantic:Question` entity created in `project.ttl`.
49: - [ ] Tree view displays the Question.

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

- **Clarity**: Questions stored in the graph are more specific than user's initial prompt.
- **Connectivity**: Future Evidence and Hypotheses link back to these Questions.

## 🔗 Dependencies

- **Ontology**: `scimantic:Question` class, `scimantic:QuestionFormation` activity.
- **MCP**: `add_question` tool.

## Expected RDF Structure

```turtle
@prefix scimantic: <http://scimantic.io/ontology#> .
@prefix prov: <http://www.w3.org/ns/prov#> .

:question_001 a scimantic:Question, prov:Entity ;
    rdfs:label "What is the kinetic folding pathway of Protein X under heat stress?" ;
    prov:wasGeneratedBy :question_formation_001 ;
    prov:generatedAtTime "2025-10-27T10:00:00Z"^^xsd:dateTime .

:question_formation_001 a scimantic:QuestionFormation, prov:Activity ;
    prov:wasAssociatedWith :researcher, :ai_assistant .
```
