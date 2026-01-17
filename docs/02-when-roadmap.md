# Scimantic Implementation Roadmap

This roadmap defines **HOW and WHEN** we build Scimantic using incremental, dogfooded development.

For **WHY**, see [the vision](00-why-vision.md).
For **WHAT** (system design), see [the architecture](01-what-architecture.md).
For **FEATURES** (detailed user stories), see [features](features/).

---

## Development Approach

### Core Principles

1. **Feature-Driven**: Work in vertical slices defined in `docs/features/*.md`, not horizontal layers
2. **Dogfooding from Day One**: Use Scimantic to research Scimantic itself (`examples/scimantic-paper`)
3. **Incremental Subset Generation**: Build subset publishing capabilities alongside each entity/activity
4. **CI/CD from Day One**: GitHub Actions validate and publish scimantic-paper subsets automatically
5. **Test-Driven**: Every capability has automated tests before implementation
6. **No Workarounds**: Follow the master KG → generated subset → publish workflow from the start

### Workflow for Each Entity/Activity

When implementing a new entity or activity (Question, Evidence, Hypothesis, etc.):

1. **Define Feature** (`docs/features/*.md`):
   - User story: WHY this entity matters to researchers
   - Acceptance criteria: WHAT observable behavior defines success
   - Implementation tasks: WHICH components need work (not HOW to build them)

2. **Extend Subset Generation** (`scimantic-core/src/scimantic/subset.py`):
   - Add capability to generate subsets containing the new entity type
   - Example: Implementing Evidence? Add license analysis capability.
   - Example: Implementing Hypotheses? Add provenance closure capability.
   - No shortcuts—use real SPARQL CONSTRUCT queries from day one

3. **Dogfood with scimantic-paper**:
   - Add real research content to `examples/scimantic-paper/project.ttl`
   - Create subset definition in `.scimantic/subsets/*.yaml`
   - Generate subset: `uv run scimantic subset generate <name>`
   - Result: `subsets/<name>.ttl` created and version controlled

4. **Automate Publishing** (GitHub Actions):
   - CI/CD validates `project.ttl` on every commit
   - CI/CD generates all defined subsets
   - CI/CD publishes to GitHub Pages
   - Result: Live demo at https://padamson.github.io/scimantic-paper/

5. **Tests Validate Workflow**:
   - Unit tests: Entity model, subset generation logic
   - Integration tests: Full workflow (add entity → generate subset → validate)
   - Specification tests: SHACL validation of generated RDF

### Incremental Subset Generation Capabilities

As we implement each entity/activity from the [scimantic schema](../scimantic-core/schema/scimantic.yaml), we add corresponding subset capabilities:

#### Question
- ✅ Basic SPARQL CONSTRUCT queries for filtering by question
- ✅ Simple subset definitions (YAML)
- ✅ GitHub Pages CI/CD pipeline
- ✅ Temporal filtering (questions created in a date range)

#### Annotation
- W3C Web Annotation Data Model compliance (`oa:Annotation`, `oa:TextQuoteSelector`)
- Source document tracking (`oa:hasTarget` for DOI, URL, or local file)
- Text selection with context (`exact`, `prefix`, `suffix`, `pageNumber`)
- Activity tracking (link to `LiteratureSearch` via `wasGeneratedBy`)
- Filter by source document or date range
- Bidirectional navigation (annotation ↔ derived evidence/questions)

#### Evidence
- License metadata tracking (`dcterms:license`)
- License analysis during subset generation
- Warning system for restricted licenses (AllRightsReserved with fair use)
- Filter by license type (CC-BY, CC0, etc.)
- Nanopublication structure validation
- Source tracking (`dcterms:source`, `dcterms:bibliographicCitation`)

#### Premise
- Provenance closure (include originating Evidence)
- Quality/credibility filtering
- Link to originating EvidenceAssessment activity

#### Hypothesis
- Provenance closure (include supporting Evidence and Premises)
- Multi-entity subsets (hypotheses + premises + evidence)
- Filter by confidence/support level
- Nanopublication structure validation

#### ExperimentalMethod
- Parameter filtering in SPARQL (include/exclude by parameter values)
- Method type filtering (computational vs experimental)
- Multi-layer closure (method → hypothesis → evidence)
- Include/exclude Parameter entities based on criteria

#### Dataset
- Uncertainty metadata inclusion (`hasUncertainty`)
- DCAT-compliant metadata (`dcat:Dataset` mixin)
- Filter by data source or experimental method
- Size/complexity filtering for large datasets

#### Result
- Uncertainty propagation tracking
- URREF Evidence mixin support
- Filter by significance or confidence interval
- Multi-layer closure (result → dataset → method → hypothesis → evidence)
- Nanopublication structure validation

#### Conclusion
- Full provenance tree inclusion (conclusion → results → datasets → methods → hypotheses → evidence)
- Nanopublication structure validation
- Filter by decision outcome or confidence

#### Advanced Publishing Capabilities
(Added as publishing features mature, not tied to specific entities)
- Multi-destination publishing (nanopub servers, GitHub Pages, Zenodo, scimantic.io)
- Trusty URI generation for nanopublications
- Version management and tagging
- VS Code UI for subset management
- Access level control (`accessLevel`: local, institutional, public)
- Publishable flag filtering (`publishable: true/false`)

---

## Current Status

### Completed

**Core Ontology (v0.1.0)**
- ✅ LinkML schema defined ([scimantic-core/schema/scimantic.yaml](../scimantic-core/schema/scimantic.yaml))
- ✅ SHACL validation shapes
- ✅ CI/CD pipeline (Test, Release, Docs)
- ✅ Published at scimantic.io

**Question Formation**
- ✅ Question entity implementation
- ✅ QuestionFormation activity
- ✅ `add_question` MCP tool
- ✅ SHACL validation for Questions
- ✅ Integration tests
- ✅ Basic subset generation for Questions

### In Progress

**Literature Review (Annotations → Evidence)**
- ⏳ Annotation entity with W3C Web Annotation compliance
- ⏳ EvidenceExtraction activity (separates highlighting from claim articulation)
- ⏳ Evidence entity with nanopublications
- ⏳ License metadata integration (`dcterms:license`)
- ⏳ VS Code tree view for knowledge graph
- ⏳ Subset generation with license analysis

### Next Up

**Complete Annotation → Evidence Implementation:**
1. Implement `add_annotation` MCP tool (W3C Web Annotation compliant)
2. Implement `extract_evidence` MCP tool (links to source annotations)
3. Finish VS Code visualization of Questions/Annotations/Evidence
4. Add dogfooding content to scimantic-paper:
   - Annotations from reading nanopublication and provenance literature
   - Evidence extracted from those annotations
   - Questions derived from annotations and evidence
5. Create subset definitions (`.scimantic/subsets/annotations.yaml`, `.scimantic/subsets/evidence.yaml`)
6. Set up GitHub Pages CI/CD for automated publishing
7. Publish first public demo: https://padamson.github.io/scimantic-paper/

**Begin Hypothesis Management:**
- Define feature in `docs/features/hypothesis-management.md`
- Implement Hypothesis entity with Premise support
- Extend subset generation with provenance closure (hypothesis → premise → evidence)
- Dogfood: Add hypotheses about Scimantic architecture
- Generate subsets showcasing hypothesis → evidence lineage

---

## Feature Development Sequence

Features are implemented in order of research workflow dependency:

1. ✅ **Ontology Development** → Foundation for all entities
2. ✅ **Question Formation** → Starting point of research
3. ⏳ **AI-Assisted Literature Search** → Annotation capture → Evidence extraction
4. 📋 **Hypothesis Management** → Link evidence to testable claims
5. 📋 **Experimental Design** → Specify methods for testing hypotheses
6. 📋 **Computational Provenance** → Track analysis workflows
7. 📋 **Subset Publishing (Complete)** → Multi-destination, production-ready
8. 📋 **Federated Graphs** → Cross-lab collaboration
9. 📋 **Uncertainty Propagation** → Automated confidence tracking
10. 📋 **AI Hypothesis Generation** → AI-assisted research

See [features/](features/) for detailed specifications.

---

## Infrastructure Timeline

### GitHub Pages Publishing (Current)
**Goal**: Public demo from day one

**Status**: Setting up with first subsets (Questions, Evidence)
**What**: GitHub Actions workflow validates + publishes subsets automatically
**Demo**: https://padamson.github.io/scimantic-paper/

### scimantic-server Development (Future)
**Goal**: Dynamic server for discovery, federation, institutional hosting

**When**: After subset publishing capabilities are complete and validated
**Why Later**: Need working subset generation first; GitHub Pages validates the model
**Dependency**: Complete implementation of advanced publishing capabilities (Trusty URIs, multi-destination, version management)

See [scimantic-server roadmap](02.1-when-scimantic-server-roadmap.md) for details.

### scimantic.io Deployment (Future)
**Goal**: Community-hosted service for subset discovery and collaboration

**When**: After scimantic-server MVP is stable
**Why Later**: Server must be stable first; scimantic-paper stays on GitHub Pages for transparency
**Value**: Discovery, SPARQL federation, institutional subsets with ORCID authentication

---

## Principles in Action

### Example: Implementing Evidence Entity

**1. Feature Definition** (`docs/features/ai-assisted-literature-search.md`):
```markdown
**Why**: Researchers need to capture literature as semantic RDF from day one
**What**: Evidence entities with license metadata, nanopublication structure
**Acceptance**: Can add 10+ facts with license tracking, query by license
```

**2. Extend Subset Generation**:
```python
# scimantic-core/src/scimantic/subset.py
def analyze_licenses(graph: Graph) -> dict:
    """NEW capability added with Evidence"""
    licenses = {}
    for s, o in graph.subject_objects(DCTERMS.license):
        license_type = classify_license(o)
        licenses[license_type] = licenses.get(license_type, 0) + 1
    return licenses
```

**3. Subset Definition**:
```yaml
# .scimantic/subsets/evidence.yaml
name: evidence
title: "Scimantic Design Evidence"
license_filter:
  allow: [CC-BY-4.0, CC0]
  warn: [AllRightsReserved]
query: |
  CONSTRUCT { ?s ?p ?o } WHERE {
    ?s a scimantic:Evidence .
    ?s ?p ?o .
  }
```

**4. Dogfooding**:
```bash
# First, create annotation while reading a paper
uv run scimantic add-annotation \
  --source "https://doi.org/10.7717/peerj-cs.387" \
  --exact "Nanopublications are minimal units of publishable information" \
  --prefix "In this paper, we argue that " \
  --suffix " that can be uniquely identified."

# Then, extract evidence from the annotation
uv run scimantic extract-evidence \
  --from-annotation annotation_001 \
  --citation "Kuhn 2016" \
  --license CC-BY-4.0 \
  --content "Nanopubs enable decentralized provenance"

# Generate subset
uv run scimantic subset generate evidence
# Output: ✓ 5 entities (5 CC-BY, 0 restricted)
```

**5. CI/CD** (`.github/workflows/publish-scimantic-paper.yml`):
```yaml
- name: Generate subsets
  run: |
    cd examples/scimantic-paper
    uv run scimantic subset generate --all

- name: Publish to GitHub Pages
  uses: peaceiris/actions-gh-pages@v3
```

**Result**: Working end-to-end workflow with no manual steps, validated incrementally.

---

## Success Criteria

We know we're on track when:

1. **Every feature works in scimantic-paper**: If we can't dogfood it, it's not ready
2. **Subsets publish automatically**: CI/CD runs on every commit without manual intervention
3. **Tests pass before merge**: Pre-commit hooks + GitHub Actions enforce quality
4. **Public demos exist**: https://padamson.github.io/scimantic-paper/ always shows current capabilities
5. **No workarounds**: We use the proper master KG → subset → publish workflow from day one

---

## Next Steps

1. **Complete Evidence Implementation**:
   - Finish VS Code extension (tree view, detail view)
   - Add Questions + Evidence to scimantic-paper
   - Create subset definitions for both entity types
   - Set up GitHub Pages CI/CD
   - Publish first demo

2. **Begin Hypothesis Management**:
   - Write feature specification (`docs/features/hypothesis-management.md`)
   - Implement Hypothesis and Premise entities
   - Extend subset generation with provenance closure
   - Dogfood with hypotheses about Scimantic design

3. **Continue Through Schema**:
   - Repeat this workflow for each entity/activity in the schema
   - Build subset capabilities incrementally as we go
   - Maintain dogfooding and CI/CD throughout

---

## References

- [Vision](00-why-vision.md) - WHY we're building Scimantic
- [Architecture](01-what-architecture.md) - WHAT the system looks like
- [Features](features/) - Detailed specifications for each capability
- [CLAUDE.md](../CLAUDE.md) - Developer guide for AI assistants
- [scimantic-server Roadmap](02.1-when-scimantic-server-roadmap.md) - Server infrastructure plan
