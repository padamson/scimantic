# Scimantic Implementation Roadmap

This roadmap defines **WHEN** we build capabilities, ordered to deliver value incrementally. Each capability links to feature documents that specify vertical slices.

For **WHY**, see [the vision](00-why-vision.md).
For **WHAT** (system design), see [the architecture](01-what-architecture.md).
For **HOW**, see code and tests.

## Principles

1. **Value-First**: Each milestone delivers end-to-end value to researchers
2. **Incremental**: Build thin vertical slices, not horizontal layers
3. **Testable**: Every capability has automated tests
4. **Dogfooded**: Use Scimantic to build Scimantic (examples/scimantic-paper)

## Milestone 1: Semantic Literature Review (Foundation)

**Goal**: Enable researchers to extract knowledge from legacy papers and persist it as nanopublications in a queryable knowledge graph.

**Why first**: Literature review is the starting point of all research. Without semantic evidence, there's nothing to link hypotheses to.

**Value delivered**: Researcher reads papers, extracts facts, and builds a machine-readable knowledge graph that AI agents can query.

### Capabilities

1. **Evidence Minting** → [Feature: AI-Assisted Literature Search (Revised)](docs/features/ai-assisted-literature-search.md)
   - Extract facts from legacy papers (manual or AI-assisted)
   - Create Evidence entities as nanopublications
   - Persist to `project.ttl` with PROV-O metadata
   - Assign Trusty URIs for citability

2. **Knowledge Graph Persistence**
   - RDF serialization (Turtle format)
   - Namespaces and prefixes (PROV-O, nanopub, scimantic)
   - File-based storage (`project.ttl`)

3. **MCP Server (Core)**
   - `add_evidence` tool: Create Evidence nanopublication
   - `query_graph` tool: Execute SPARQL on `project.ttl`
   - `get_provenance_graph_json` tool: Fetch graph for visualization

4. **VS Code Extension (Basic)**
   - MCP client connecting to scimantic-core
   - Tree view displaying Evidence entities
   - Refresh command to reload knowledge graph
   - Details view showing nanopublication structure

**Acceptance Criteria**:
- Researcher can extract 10+ facts from papers and see them in VS Code tree view
- AI agent (Claude via MCP) can answer "List all evidence from Smith 2023"
- Each Evidence entity has Trusty URI and PROV-O metadata
- Knowledge graph is valid RDF (verified via `rdflib.Graph().parse()`)

**Status**: Slice 1 complete (Evidence persistence), Slice 2 in progress (VS Code visualization)

---

## Milestone 2: Hypothesis Formation and Provenance

**Goal**: Link hypotheses to supporting evidence with explicit uncertainty and provenance.

**Why second**: Once evidence exists, researchers formulate hypotheses. Provenance links make the knowledge graph queryable ("What evidence supports this hypothesis?").

**Value delivered**: Researcher formulates hypotheses backed by evidence, with uncertainty quantified and lineage traceable.

### Capabilities

1. **Hypothesis Entities** → [Feature: Hypothesis Management](docs/features/hypothesis-management.md) (to be created)
   - Create Hypothesis entities linking to Evidence via `prov:wasDerivedFrom`
   - Quantify uncertainty (0.0 - 1.0 scale)
   - Auto-propagate uncertainty from evidence
   - Mint as nanopublications with Trusty URIs

2. **Provenance Tracking**
   - W3C PROV-O patterns for hypothesis formation
   - `prov:Activity` for "hypothesis_formation"
   - `prov:Agent` for researcher or AI
   - `prov:used` linking to source evidence

3. **MCP Tools**
   - `add_hypothesis` tool: Create Hypothesis with evidence links
   - `get_hypothesis_provenance` tool: Retrieve lineage back to evidence
   - `query_hypotheses` tool: SPARQL queries filtered by uncertainty

4. **VS Code Extension**
   - Hypothesis tree view (separate from Evidence)
   - Click hypothesis → show supporting evidence in provenance graph
   - Webview visualization of hypothesis-evidence graph

**Acceptance Criteria**:
- Researcher can create hypothesis linked to 2+ evidence entities
- SPARQL query "Find hypotheses with uncertainty < 0.2" works
- VS Code shows provenance graph: Hypothesis → Evidence → Source
- Uncertainty auto-calculated from evidence uncertainty + epistemic gap

**Dependencies**: Milestone 1 (Evidence entities must exist)

---

## Milestone 3: Computational Provenance

**Goal**: Auto-generate PROV-O metadata for computational workflows using Python decorators.

**Why third**: Computational scientists need provenance for scripts and data pipelines. This milestone enables reproducible computational research.

**Value delivered**: Researcher decorates Python functions with `@activity`, and PROV-O metadata is auto-generated (inputs, outputs, timestamps, software agents).

### Capabilities

1. **Provenance Decorators** → [Feature: Computational Provenance](docs/features/computational-provenance.md) (to be created)
   - `@activity` decorator for Python functions
   - Auto-detect input files (via function arguments)
   - Auto-detect output files (via return values)
   - Generate PROV-O triples and append to `project.ttl`

2. **Software Agent Metadata**
   - Capture script name, Git commit hash, Python version
   - Link Activity to SoftwareAgent via `prov:wasAssociatedWith`
   - Record execution environment (OS, dependencies)

3. **Dataset Entities**
   - Input/output files as `prov:Entity`
   - Checksums for verification
   - Links to Activities via `prov:used` and `prov:wasGeneratedBy`

4. **MCP Tools**
   - `run_analysis` tool: Execute decorated Python script via MCP
   - `get_analysis_provenance` tool: Retrieve full lineage for a result

**Acceptance Criteria**:
- Researcher decorates function, runs it, and PROV-O metadata appears in `project.ttl`
- SPARQL query "Which script generated dataset_001?" returns correct script and commit hash
- Uncertainty propagates from input datasets to output results
- VS Code shows computational lineage: Hypothesis → Design → Analysis → Result

**Dependencies**: Milestone 2 (Hypotheses guide computational design)

---

## Milestone 4: Experimental Design Specification

**Goal**: Specify experimental or computational methods as RDF entities with parameters and expected outcomes.

**Why fourth**: Designs bridge hypotheses and execution. Capturing them as RDF enables validation before running experiments.

**Value delivered**: Researcher specifies "I will test hypothesis X using method Y with parameters Z" as a machine-readable Design entity.

### Capabilities

1. **Design Entities** → [Feature: Experimental Design](docs/features/experimental-design.md) (to be created)
   - Create Design entities linking to Hypotheses via `prov:wasDerivedFrom`
   - Structured parameters (key-value pairs with units)
   - Expected outcomes (quantitative predictions)
   - Mint as nanopublications

2. **Design Validation**
   - Check that parameters are within valid ranges
   - Warn if expected outcome is inconsistent with hypothesis uncertainty
   - SPARQL queries: "Show designs testing hypothesis_001"

3. **MCP Tools**
   - `add_design` tool: Create Design with parameters
   - `validate_design` tool: Check parameter consistency
   - `link_design_to_hypothesis` tool: Explicit provenance linking

4. **VS Code Extension**
   - Design creation form (webview)
   - Parameter editor with unit validation
   - Design-to-hypothesis lineage visualization

**Acceptance Criteria**:
- Researcher creates design with 3+ parameters, linked to hypothesis
- Design validation catches out-of-range parameter
- SPARQL query "Find designs with expected DCS > 100 mb" works
- VS Code visualizes: Evidence → Hypothesis → Design

**Dependencies**: Milestone 2 (Hypotheses must exist to link designs)

---

## Milestone 5: Nanopublication Publishing

**Goal**: Export nanopublications to remote servers (nanopub.org) or IPFS for public sharing.

**Why fifth**: Local knowledge graphs are valuable, but sharing enables collaboration and citation.

**Value delivered**: Researcher publishes nanopublications from `project.ttl` to public servers, making them citable and discoverable.

### Capabilities

1. **Nanopub Export** → [Feature: Nanopublication Publishing](docs/features/nanopub-publishing.md) (to be created)
   - Export individual nanopublications to TriG format
   - Batch export: all nanopubs in `project.ttl`
   - Digital signatures (public/private key pairs)
   - Trusty URI generation and verification

2. **Remote Publishing**
   - HTTP POST to nanopub.org or institutional servers
   - IPFS pinning for decentralized storage
   - Publication receipt (server-assigned URIs)

3. **Citation Management**
   - Generate BibTeX entries for nanopublications
   - LaTeX integration: `\cite{nanopub:RA1234567890}`
   - Track citations: "Which papers cite my nanopub?"

4. **MCP Tools**
   - `publish_nanopublication` tool: Export and POST to server
   - `sign_nanopublication` tool: Digital signature
   - `verify_nanopublication` tool: Check Trusty URI integrity

**Acceptance Criteria**:
- Researcher publishes 5 nanopublications to nanopub.org
- Each nanopub has Trusty URI and is queryable via nanopub.org SPARQL endpoint
- BibTeX entries generated for LaTeX citation
- VS Code shows publication status (local vs. published)

**Dependencies**: Milestones 1-4 (need content to publish)

---

## Milestone 6: Uncertainty Propagation

**Goal**: Automate uncertainty calculation as it flows from evidence → hypothesis → design → analysis.

**Why sixth**: Manual uncertainty tracking is error-prone. Automated propagation ensures scientific rigor.

**Value delivered**: Researcher sees uncertainty bounds auto-calculated throughout the workflow, with SPARQL queries like "Find results with uncertainty < 0.1".

### Capabilities

1. **Uncertainty Rules** → [Feature: Uncertainty Quantification](docs/features/uncertainty-quantification.md) (to be created)
   - Rule: `u_hypothesis >= max(u_evidence) + epistemic_gap`
   - Rule: `u_analysis = sqrt(u_design^2 + u_computational^2)`
   - Configurable epistemic gaps (default: 0.15 for hypotheses)

2. **Automated Calculation**
   - Trigger on entity creation: auto-compute uncertainty from linked entities
   - SPARQL UPDATE queries to propagate uncertainty through graph
   - Warning if uncertainty exceeds threshold (e.g., u > 0.5 for publication)

3. **Uncertainty Visualization**
   - Color-coded tree view: green (u < 0.1), yellow (0.1-0.3), red (u > 0.3)
   - Uncertainty timeline: track how confidence evolved during research
   - Provenance of uncertainty: "Why is this hypothesis u = 0.25?"

4. **MCP Tools**
   - `propagate_uncertainty` tool: Recalculate uncertainty across graph
   - `query_by_uncertainty` tool: SPARQL queries filtered by confidence

**Acceptance Criteria**:
- Hypothesis uncertainty auto-calculated from linked evidence
- Analysis uncertainty propagates from design and computational error
- SPARQL query "Find evidence with u < 0.05" returns high-confidence facts
- VS Code shows uncertainty color-coding in tree view

**Dependencies**: Milestones 1-4 (need entities with uncertainty metadata)

---

## Milestone 7: Federated Knowledge Graphs

**Goal**: Link multiple researchers' knowledge graphs via RDF links, enabling collaborative semantic research.

**Why seventh**: Once individual graphs are mature, collaboration requires federation.

**Value delivered**: Lab A's `project.ttl` can reference Lab B's nanopublications, enabling cross-lab SPARQL queries.

### Capabilities

1. **Cross-Graph References** → [Feature: Federated Graphs](docs/features/federated-graphs.md) (to be created)
   - Reference external nanopublications by Trusty URI
   - Import evidence from remote graphs (with attribution)
   - SPARQL federation: query across multiple `project.ttl` files
   - Tier-aware import: respect publishing tiers (Tier 2 requires authentication)

2. **Conflict Resolution**
   - Detect contradictory evidence (same claim, different values)
   - Uncertainty-weighted consensus (higher confidence wins)
   - Explicit disagreement entities: "Lab A says X, Lab B says Y"
   - Provenance tracking: which lab contributed which evidence

3. **Provenance of External Evidence**
   - Track source graph: "This evidence came from Lab B's project"
   - Attribution metadata: `prov:wasAttributedTo :lab_b`
   - Trust scores (optional): weight evidence by source reputation
   - License compliance: ensure imported evidence respects CC-BY/fair use

4. **Institutional Server Integration**
   - ORCID authentication for Tier 2 access
   - Access control lists (ACL) for lab servers
   - Discovery: find lab servers via ROR (Research Organization Registry)
   - Synchronization: keep local copy in sync with remote updates

5. **VS Code Extension**
   - Import evidence from remote graph via URI
   - Visualize federated graph (local + remote nodes)
   - Conflict detection warnings
   - Show evidence publishing tier (color-coded: green=public, yellow=institutional, red=local)

**Acceptance Criteria**:
- Researcher imports 5 evidence entities from colleague's Tier 2 (institutional) graph via ORCID auth
- SPARQL federation query: "Find all hypotheses (local and remote) about DCS"
- Conflict detection: "Evidence_001 (local, u=0.05) contradicts Evidence_042 (remote, u=0.10)"
- VS Code shows imported evidence with source attribution and tier badge
- License compliance check: warn if importing evidence with incompatible license

**Dependencies**: Milestone 5 (nanopublication publishing enables sharing)

---

## Milestone 8: AI Hypothesis Generation

**Goal**: AI agents autonomously propose hypotheses based on evidence patterns in the knowledge graph.

**Why eighth**: Once the graph is rich, AI can assist with hypothesis formation, not just literature extraction.

**Value delivered**: Researcher asks AI "What hypotheses are supported by recent DCS evidence?" and receives SPARQL-backed suggestions.

### Capabilities

1. **Pattern Detection** → [Feature: AI Hypothesis Suggestion](docs/features/ai-hypothesis-suggestion.md) (to be created)
   - SPARQL queries to find evidence clusters (e.g., "All DCS measurements at E = 10 MeV")
   - AI analyzes patterns and suggests hypotheses
   - Uncertainty estimation based on evidence quality

2. **Hypothesis Ranking**
   - Score hypotheses by evidence support (more evidence = higher score)
   - Penalize high uncertainty in evidence
   - Novelty detection: "This hypothesis hasn't been tested before"

3. **Interactive Refinement**
   - Researcher accepts/rejects AI-suggested hypotheses
   - Feedback loop: rejections train AI to avoid similar suggestions
   - Collaborative editing: AI suggests, researcher refines wording

4. **MCP Tools**
   - `suggest_hypothesis` tool: AI generates hypothesis from evidence
   - `rank_hypotheses` tool: Score by evidence support
   - `explain_hypothesis` tool: "Why did you suggest this?"

**Acceptance Criteria**:
- AI suggests 3 hypotheses based on 10+ evidence entities
- Researcher accepts 1, rejects 2, and AI learns from feedback
- SPARQL query explains suggestion: "Hypothesis_X is supported by Evidence_A, B, C"
- VS Code shows suggestion UI with accept/reject buttons

**Dependencies**: Milestones 1-2 (rich evidence and hypothesis graphs)

---

## Cross-Cutting Concerns

These are ongoing efforts across all milestones:

### Testing
- **Unit tests**: Each module (models, provenance, publish, mcp) has >80% coverage
- **Integration tests**: End-to-end workflows (evidence → hypothesis → design → analysis)
- **Manual testing**: Dogfooding with examples/scimantic-paper

### Documentation
- **Vision**: Why we're building Scimantic (VISION.md)
- **Architecture**: What we're building (ARCHITECTURE.md)
- **Features**: Vertical slices (docs/features/*.md)
- **Code**: How it works (tests + implementation)

### Performance
- **RDF parsing**: Optimize for graphs with 10K+ triples
- **SPARQL queries**: Index common patterns (evidence by source, hypotheses by uncertainty)
- **MCP latency**: Keep tool calls <500ms for responsive UI

### Security
- **Input validation**: Sanitize SPARQL queries to prevent injection
- **Signature verification**: Validate Trusty URIs before importing external nanopubs
- **Access control**: (Future) multi-user projects with permissions

---

## Future Milestone: Publisher Partnerships for Sanctioned Extraction

**Goal**: Establish formal partnerships with academic publishers for legal, sanctioned semantic extraction of legacy literature.

**Why future** (3-5 years): Requires demonstrating value with Tier 4 extractions, building community adoption, and negotiating with publishers.

**Value delivered**: Researchers can extract knowledge from copyrighted papers without legal risk, with publisher cooperation and validation.

### Capabilities

1. **Publisher API Integration** → [Feature: Publisher Extraction APIs](docs/features/publisher-extraction.md) (future)
   - Integrate with Elsevier, Springer, Wiley APIs for structured data access
   - Authentication via institutional subscriptions
   - Rate limiting and terms-of-service compliance
   - Automated metadata extraction (DOI, authors, citations)

2. **Co-Branded Nanopublications**
   - Evidence nanopubs include publisher attribution
   - Format: "Extracted by [Researcher] from [Publisher] source [DOI]"
   - Publisher logo/branding in nanopub metadata
   - Quality validation: publishers verify accuracy of extractions

3. **Revenue Sharing / Licensing Models**
   - Option 1: Free extraction for non-commercial research (publisher goodwill)
   - Option 2: Licensing fees for commercial use (pharma, biotech)
   - Option 3: Revenue sharing based on increased citations/usage
   - Track metrics: citation impact, paper views driven by semantic extractions

4. **Community Extraction Platform**
   - Crowd-sourced semantic annotation of legacy literature
   - Quality control: multiple researchers extract same fact, consensus voting
   - Publisher oversight: approve/reject extractions before publication
   - Gamification: badges, leaderboards for top extractors

5. **Precedent Partnerships**
   - **Europe PMC**: Already provides text mining APIs for biomedical literature (free for researchers)
   - **Crossref**: Metadata APIs with publisher cooperation
   - **OpenCitations**: Open citation data with publisher buy-in
   - **Semantic Scholar**: Full-text access via publisher agreements

### Implementation Strategy

**Phase 1: Demonstrate Value (Years 1-2)**
- Build community with Tier 4 extractions (fair use)
- Collect metrics: citations to original papers, increased visibility
- Build case study: "Scimantic drove 1000+ citations to partner papers"

**Phase 2: Approach Publishers (Year 3)**
- Present value proposition: semantic extractions increase paper impact
- Offer pilot program with open-access journals first (low risk)
- Negotiate API access for participating publishers

**Phase 3: Scale (Years 4-5)**
- Expand to major publishers (Elsevier, Springer, Wiley)
- Integrate publisher validation into Scimantic UI
- Build federated nanopub network with publisher-sanctioned evidence

### Acceptance Criteria (Future)
- Scimantic has formal API agreements with 3+ major publishers
- Researchers can extract evidence from 50%+ of literature without legal risk
- Publishers report increased citation impact from semantic extractions
- Community platform has 100+ active extractors, 10K+ validated nanopubs

### Why Publishers Might Cooperate

**Benefits for publishers**:
1. **Increased visibility**: Semantic extractions drive traffic to original papers
2. **Better metrics**: Track usage beyond traditional citations (e.g., "cited in 50 knowledge graphs")
3. **Quality control**: Publishers ensure accuracy of extracted data (brand protection)
4. **New revenue**: Licensing semantic derivatives (if needed)
5. **Community good**: Addressing reproducibility crisis benefits entire ecosystem
6. **Competitive advantage**: Publishers with APIs attract more citations

**Risks for publishers** (must address):
1. **Revenue loss**: Concern that extractions reduce subscriptions → Counter: semantic extractions are additive, not substitutive
2. **Copyright**: Loss of control over content → Counter: extractions are factual, not narrative; provenance links back to source
3. **Quality**: Inaccurate extractions damage reputation → Counter: publisher validation layer

**Mitigations**:
- Start with open-access publishers (CC-BY license, no risk)
- Collect data showing increased citations (mutual benefit)
- Offer publisher veto power over extractions (opt-out)

---

## Deferred Capabilities

These are valuable but not critical for initial adoption:

1. **OWL Reasoning**: Infer relationships (e.g., transitivity of `prov:wasDerivedFrom`)
2. **Blockchain Registry**: Immutable timestamps for scientific claims
3. **Bayesian Uncertainty**: Probabilistic graphical models for uncertainty propagation
4. **GUI Editor**: Standalone desktop app (vs. VS Code extension)
5. **Mobile App**: Literature review on tablets/phones

---

## Current Status

- **Milestone 1**: Slice 1 complete (Evidence persistence with nanopubs and PROV-O)
- **Milestone 1**: Slice 2 in progress (VS Code tree view, needs nanopub integration)
- **Milestones 2-8**: Not started

## Next Steps

1. **Revise Milestone 1, Slice 2** to align with nanopublication-first approach
2. **Implement nanopublication minting** in `add_evidence` MCP tool
3. **Update VS Code extension** to display nanopub structure (assertion + provenance)
4. **Complete Milestone 1** before moving to Milestone 2
