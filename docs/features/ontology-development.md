# Feature: Scimantic Ontology Development

## 📖 User Story
> **As a** developer and meta-researcher
> **I want to** define a minimal, rigorous domain ontology (`scimantic`) aligned with standard upper/mid-level ontologies
> **So that** Scimantic produces data that is interoperable, scientifically valid, and sustainable

### Narrative

**The Problem**: Ad-hoc RDF schemas ("just add a property called 'summary'") lead to data silos and poor reasoning capabilities. Over-engineering (importing massive ontologies) leads to complexity and usability issues.

**The Vision**: A "Goldilocks" ontology:
*   **Minimal**: Only define what isn't available elsewhere.
*   **Grounded**: Strictly subclass W3C PROV-O (`prov:Entity`, `prov:Activity`).
*   **Compatible**: Play nicely with URREF (Uncertainty), AIDA (Nanopubs), and DC Terms.
*   **Versioned**: Semantic versioning (v0.1.0) with publication to a persistent URL (w3id.org).

---

## ✂️ Vertical Slices

### Slice 1: Ontology Review & Gap Analysis

**Goal**: Review candidate ontologies and define the exact scope of `scimantic`.

**Tasks**:
1.  **PROV-O Deep Dive**: Map every proposed Scimantic concept to a PROV concept.
2.  **URREF Integration**: Verify how to attach URREF entities to PROV entities.
3.  **AIDA/Nanopub Review**: Ensure `scimantic` entities fit the assertion graph model.
4.  **Gap Analysis**: List exactly which classes/properties are missing.

**Deliverable**: A specification document listing the required classes and properties for `scimantic-ontology-v0.1.0`.

### Slice 2: Ontology Implementation (v0.1.0)

**Goal**: Create the physical TTL file and validate it.

**Tasks**:
1.  Create `scimantic.ttl`.
2.  Define Classes: `Question`, `Evidence`, `Hypothesis`, `Design`, `Dataset`, `Result`.
3.  Define Activities: `QuestionFormation`, `LiteratureSearch`, `Assessment`, `HypothesisFormation`, `DesignPlanning`, `Execution`, `Analysis`.
4.  Define Properties: `accessLevel`, `content` (or `label`), domain-specific relations not covered by PROV.
5.  **Local Validation**: Configure `pre-commit` hooks to run syntax validation (riot/jena) and simplistic SHACL checks locally, mirroring the CI pipeline.

### Slice 3: Automated Publication (CI/CD)

**Goal**: Fully automate the validation, documentation generation, and publication of the ontology via CI/CD.

**Tasks**:
1.  **Validation Pipeline**: GitHub Action triggers on push to Validate syntax (riot/jena) and SHACL compliance.
2.  **Documentation Pipeline**: GitHub Action generates static HTML documentation (using Widoco or similar) from the `.ttl` source.
3.  **Deployment Pipeline**:
    - Deploys both `.ttl` and HTML to GitHub Pages.
    - Configures `w3id` redirects (if applicable) to point to the new version.
4.  **Content Negotiation**: Configure hosting to serve correct representation (HTML vs Turtle) based on client request.

---

## 🎯 Success Metrics

- **Valid RDF**: Passes syntax checkers.
- **PROV Compliance**: All classes are valid PROV subclasses.
- **Coverage**: Covers all 6 entities and 7 activities defined in Architecture.

## 🔗 Dependencies

- **Standards**: PROV-O, URREF, DC Terms, Nanopub Schema.
