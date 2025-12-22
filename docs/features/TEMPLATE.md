# Feature: [Feature Name]

> **Documentation Philosophy**: This document describes **WHY** we're building this feature and **WHAT** it should deliver. The **HOW** is in the code itself (tests and implementation). Focus on user value, acceptance criteria, and expected outcomes—not implementation details.

## 📖 User Story
> **As a** [role - e.g., computational chemist, research scientist, graduate student]
> **I want to** [action - e.g., search literature with AI assistance, mint hypotheses from evidence, track experimental provenance]
> **So that** [benefit - e.g., build machine-readable research from day one, ensure reproducibility, enable semantic publishing]

### Narrative
[Brief description of the user journey and context. Explain WHY this feature matters to researchers executing the scientific method. Focus on the problem being solved and the value delivered, not on how it will be implemented.]

### Scientific Method Stage
[Which stage(s) of the scientific method does this feature support?]
- [ ] Literature Review
- [ ] Hypothesis Formation
- [ ] Experimental Design
- [ ] Experimentation
- [ ] Analysis
- [ ] Publication

---

## ✂️ Vertical Slices

### Slice 1: [Slice Name]
**Goal:** [WHAT value does this slice deliver? WHAT can the user accomplish after this slice is complete? Focus on outcomes, not implementation.]

**Why This Slice:** [WHY is this valuable? How does it support the research workflow or enable semantic publishing?]

**Components:** [Which parts of the monorepo need work?]
- [ ] semflow-core
- [ ] semflow-ext
- [ ] examples/semflow-paper

#### ✅ Acceptance Criteria
[Describe WHAT the system should do from the user's perspective. Be specific about observable behavior and outcomes.]

- [ ] [Observable behavior 1: What the user can see/do in VS Code or CLI]
- [ ] [Semantic artifact 2: What RDF structure exists, queryable how?]
- [ ] [Provenance requirement 3: What lineage is captured?]
- [ ] [Uncertainty requirement 4: What uncertainties are quantified?]

#### 🛠️ Implementation Tasks
[List WHAT needs to be built, not HOW to build it. The tests and code will show the how.]

**Backend (semflow-core)**:
- [ ] Models: Evidence/Hypothesis/Design entity with RDF persistence
- [ ] Provenance: PROV-O tracking for entity creation
- [ ] MCP Tools: Agent-accessible tool for [operation]
- [ ] Tests: Unit and integration tests for [component]

**Frontend (semflow-ext)**:
- [ ] UI: [What view/panel] displaying [what information]
- [ ] MCP Client: Integration with semflow-core
- [ ] Visualization: [What graph/tree] rendering [what data]
- [ ] Commands: VS Code command for [what action]

**Validation**:
- [ ] Manual testing with examples/semflow-paper demonstrates [what workflow]
- [ ] RDF output validates with SPARQL queries for [what structure]

---

### Slice 2: [Slice Name]
**Goal:** [What value does this slice deliver?]

**Components:**
- [ ] semflow-core
- [ ] semflow-ext
- [ ] examples/scics

#### ✅ Acceptance Criteria
- [ ] [User-facing requirement 1]
- [ ] [Semantic requirement: RDF structure, SPARQL queryability]
- [ ] [Provenance requirement: PROV-O compliance]

#### 🛠️ Implementation Tasks
- [ ] **Backend**: [Task description]
- [ ] **Frontend**: [Task description]
- [ ] **Testing**: [Task description]

---

## 🎯 Success Metrics
[How will we know this feature is successful? Focus on WHY it matters and WHAT outcomes we expect.]

- **Semantic Completeness**: Can SPARQL queries extract all relevant information? Why does this matter for the research workflow?
- **Provenance Coverage**: Is the full lineage from source to conclusion captured? What scientific claims does this enable?
- **Uncertainty Transparency**: Are uncertainties explicitly represented? How does this support reproducibility?
- **AI Agent Usability**: Can an MCP agent interact with the feature? What research tasks does this automate?
- **Reproducibility**: Can another researcher reproduce the workflow from RDF alone? What trust does this build?
- **User Productivity**: What time is saved or quality improved? What research activities are accelerated?

## 🔗 Dependencies
[List any dependencies on:]
- **RDF/OWL Libraries**: RDFLib, OWL-RL reasoner
- **W3C Standards**: PROV-O, Dublin Core, FOAF
- **Nanopublication Infrastructure**: Trusty URI generation, signature schemes
- **MCP Integration**: Model Context Protocol SDK (Python/TypeScript)
- **VS Code Extension APIs**: Webview, TreeView, FileSystemProvider
- **External Services**: DOI resolution, literature APIs (e.g., Semantic Scholar, CrossRef)
- **Scientific Computing**: NumPy, SciPy, cclib (for computational chemistry)

## 📚 Reference Materials
[Link to relevant documentation and standards:]
- [W3C PROV-O Specification](https://www.w3.org/TR/prov-o/)
- [Nanopublications](http://nanopub.org/)
- [RDFLib Documentation](https://rdflib.readthedocs.io/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [VS Code Extension API](https://code.visualstudio.com/api)
- [SemFlow Ontology Documentation](../../semflow-core/ontology/) (if applicable)
- [CLAUDE.md](../../CLAUDE.md) (Developer guide)
- Related features in [docs/features/](./)
