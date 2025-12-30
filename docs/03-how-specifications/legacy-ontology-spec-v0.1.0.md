# Scimantic Ontology Specification (v0.1.0)

> **NOTE**: This document is for **reference only** as it provides some historical context for the ontology. The current ontology is specified in `scimantic-core/schema/scimantic.yaml`.

This document specifies the classes, properties, and constraints for the `scimantic` ontology version 0.1.0. It serves as the blueprint for implementing the `scimantic.ttl` file.

## 1. Metadata & Namespaces

- **URI**: `http://scimantic.io`
- **Preferred Prefix**: `scimantic`
- **Version**: 0.1.0
- **License**: CC-BY 4.0

### External Dependencies
| Prefix | URI | Purpose |
|---|---|---|
| `prov` | `http://www.w3.org/ns/prov#` | Core provenance backbone |
| `urref` | `https://raw.githubusercontent.com/adelphi23/urref/469137/URREF.ttl#` | Uncertainty representation (pinned version) |
| `dcterms` | `http://purl.org/dc/terms/` | General metadata |
| `np` | `http://www.nanopub.org/nschema#` | Nanopublication structure |
| `foaf` | `http://xmlns.com/foaf/0.1/` | Agent details |
| `doap` | `http://usefulinc.com/ns/doap#` | Software projects (Description of a Project) |
| `dcat` | `http://www.w3.org/ns/dcat#` | Data Catalog Vocabulary |
| `sosa` | `http://www.w3.org/ns/sosa/` | Sensors, Observations, Samples, and Actuators |

---

## 2. Methodology & Integration Strategy

### Integration Patterns
Scimantic follows a "reuse-first" strategy with three distinct integration patterns:

1.  **Vertical Specialization (Subclassing)**: usage of `rdfs:subClassOf` to extend PROV-O for core scientific concepts (e.g., `scimantic:Evidence` extends `prov:Entity`).
2.  **Horizontal Integration (Direct Reuse)**: Direct usage of external vocabularies for non-scientific resources to avoiding reinventing the wheel.
    *   **Software** -> DOAP
    *   **Datasets** -> DCAT
    *   **Instruments** -> SOSA
3.  **Module Application (Linking)**: Linking to complex external models without redefining them.
    *   **Uncertainty** -> URREF (linked via `scimantic:hasUncertainty`)

### AIDA Compliance
Scimantic strictly adheres to the **AIDA** (Atomic, Independent, Declarative, Absolute) principles for nanopublications:
*   **Atomic**: Each Entity (Evidence, Hypothesis) is small enough to be independently valid.
*   **Independent**: Entities stand alone with their own URI and provenance.
*   **Declarative**: Expressed in RDF Turtle.
*   **Absolute**: Uses Trusty URIs for immutability.

---

## 3. Entity Classes

All are subclasses of `prov:Entity`.

| Class | Subclass Of | Description |
|---|---|---|
| `scimantic:Question` | `prov:Entity` | An interrogative sentence representing the research query. |
| `scimantic:Evidence` | `prov:Entity`, `np:Nanopublication` | A factual claim extracted from a source (literature or prior data). Enforces AIDA compliance. |
| `scimantic:Premise` | `prov:Entity` | An evaluated proposition or insight derived from Evidence. |
| `scimantic:Hypothesis` | `prov:Entity`, `np:Nanopublication` | A testable claim derived from evidence. |
| `scimantic:ExperimentalMethod` | `prov:Entity`, `prov:Plan` | A specification of the method to be executed. |
| `scimantic:Dataset` | `prov:Entity`, `dcat:Dataset`| Raw data/measurements produced by experimentation. |
| `scimantic:Result` | `prov:Entity`, `np:Nanopublication` | The outcome of an analysis. |

## 4. Uncertainty & Evidence Integration (URREF)

We rely directly on the **URREF Ontology** for uncertainty modeling and evidence classification.

| Scimantic Concept | URREF Class Used | Notes |
|---|---|---|
| **Evidence** | `urref:Evidence` | `scimantic:Evidence` inherits from this to align with URREF tools. |
| **Result** | `urref:Evidence` | `scimantic:Result` inherits from this as it serves as experimental evidence. |
| **Ambiguity** | `urref:Ambiguity` | Type of Epistemic Uncertainty. |
| **Vagueness** | `urref:Vagueness` | Type of Epistemic Uncertainty. |
| **Incompleteness**| `urref:Incompleteness` | Type of Epistemic Uncertainty. |
| **Model** | `urref:UncertaintyModel` | We bridge this to `prov:Entity` in `scimantic.ttl`. |

**Why Reification?**
We model uncertainty as a distinct Object (`urref:UncertaintyModel`) rather than a simple property (e.g., `hasConfidence: 0.8`). This "reification" allows us to:
1.  **Trace Provenance**: Who assessed this uncertainty? When? Using what criteria (`urref:UncertaintyDerivation`)?
2.  **Rich Characterization**: Describe complex uncertainty (e.g. probability distributions, conflicting sources) that cannot fit in a single scalar value.

---

## 5. Activity Classes

All are subclasses of `prov:Activity`. They represent the steps of the Scientific Method.

| Class | Subclass Of | Description |
|---|---|---|
| `scimantic:QuestionFormation` | `prov:Activity` | Creating a Question. |
| `scimantic:LiteratureSearch` | `prov:Activity` | Searching and extracting Evidence. |
| `scimantic:EvidenceAssessment` | `prov:Activity` | Evaluating Evidence credibility and relevance. |
| `scimantic:HypothesisFormation` | `prov:Activity` | Synthesizing Evidence into a Hypothesis. |
| `scimantic:DesignOfExperiment` | `prov:Activity` | Creating an ExperimentalMethod from a Hypothesis. |
| `scimantic:Experimentation` | `prov:Activity` | running an ExperimentalMethod to produce a Dataset. |
| `scimantic:Analysis` | `prov:Activity` | Processing a Dataset to produce a Result. |
| `scimantic:ResultAssessment` | `prov:Activity` | Comparing a Result to the original Hypothesis. |

---

## 6. Relationships & Flow

These properties define the potential connections between entities and activities, mapping the Scimantic Vision flow to PROV-O predicates.

| Relationship (Vision) | Domain | Range | Predicate (Ontology) | Description |
|---|---|---|---|---|
| **Generates** | `prov:Activity` | `prov:Entity` | `prov:wasGeneratedBy` (inverse) | Activity creates an Entity. **Strictly constrained pairs**: <br>1. `QuestionFormation` -> `Question`<br>2. `LiteratureSearch` -> `Evidence`<br>3. `HypothesisFormation` -> `Hypothesis`<br>4. `DesignOfExperiment` -> `ExperimentalMethod`<br>5. `Experimentation` -> `Dataset`<br>6. `Analysis` -> `Result` |
| **Input To** | `prov:Entity` | `prov:Activity` | `prov:used` | Activity uses an Entity as input. **Strictly constrained pairs**: <br>1. `Question` -> `LiteratureSearch` (motivates)<br>2. `Evidence` -> `EvidenceAssessment`<br>3. `Evidence` -> `HypothesisFormation`<br>4. `Hypothesis` -> `DesignOfExperiment`<br>5. `ExperimentalMethod` -> `Experimentation` (as plan)<br>6. `Dataset` -> `Analysis`<br>7. `Result` -> `ResultAssessment` |
| **Informs** | `prov:Activity` | `prov:Activity` | `prov:wasInformedBy` | One Activity triggers or informs another. **Strictly constrained pairs**: <br>1. `LiteratureSearch` -> `EvidenceAssessment`<br>2. `EvidenceAssessment` -> `HypothesisFormation`<br>3. `HypothesisFormation` -> `DesignOfExperiment`<br>4. `DesignOfExperiment` -> `Experimentation`<br>5. `Experimentation` -> `Analysis`<br>6. `Analysis` -> `ResultAssessment` |
| **Derives From** | `prov:Entity` | `prov:Entity` | `prov:wasDerivedFrom` | An Entity is based on a prior Entity. **Strictly constrained pairs**: <br>1. `Hypothesis` -> `Evidence`<br>2. `ExperimentalMethod` -> `Hypothesis`<br>3. `Dataset` -> `ExperimentalMethod`<br>4. `Result` -> `Dataset` |
| **Supports** | `scimantic:Evidence`, `scimantic:Result` | `scimantic:Hypothesis` | `scimantic:supports` | Positive evidence or result for a hypothesis. |
| **Contradicts** | `scimantic:Evidence`, `scimantic:Result` | `scimantic:Hypothesis` | `scimantic:contradicts` | Negative evidence or result for a hypothesis. |
| **Motivates** | `scimantic:Question` | `scimantic:LiteratureSearch` | `scimantic:motivates` | A Question that triggers/motivates a specific scientific activity. **Strictly constrained pairs**: <br>1. `Question` -> `LiteratureSearch` |
| **Refines** | `scimantic:Result` | `scimantic:Hypothesis` | `scimantic:refines` | A Result suggesting a specific modification to a Hypothesis. Subproperty of `prov:wasDerivedFrom`. **Strictly constrained pairs**: <br>1. `Result` -> `Hypothesis` |

---

## 7. Properties

### Core Domain Properties

| Property | Domain | Range | Description |
|---|---|---|---|
| `scimantic:accessLevel` | `np:Nanopublication` | `xsd:string` | Publishing scope (local, institutional, public, public_essential_evidence). |
| `scimantic:publishable` | `np:Nanopublication` | `xsd:boolean` | Flag indicating if this is ready for public promotion. |

### Experimental Method Properties
| Property | Domain | Range | Description |
|---|---|---|---|
| `scimantic:method` | `scimantic:ExperimentalMethod` | `xsd:string` (or URI) | Name/description of method. |
| `scimantic:parameter` | `scimantic:ExperimentalMethod` | `scimantic:Parameter` | Structured configuration. |


### Uncertainty Model Properties (URREF Integration)
| Property | Domain | Range | Description |
|---|---|---|---|
| `scimantic:hasUncertainty` | `scimantic:Evidence`, `scimantic:Result`, `scimantic:Dataset` | `urref:UncertaintyModel` | Links a scientific entity to its reified uncertainty model. |
| `urref:natureOfUncertainty`| `scimantic:Uncertainty`| `urref:UncertaintyNature` | Nature of the uncertainty (`urref:Epistemic`, `urref:Aleatory`). |
| `urref:hasImperfection` | `scimantic:Uncertainty`| `urref:UncertaintyType` | Specific type (`scimantic:Ambiguity`, `scimantic:Vagueness`). |
| `urref:derivationOfUncertainty`| `scimantic:Uncertainty` | `urref:UncertaintyDerivation`| How the uncertainty was derived. |

### Result Properties
| Property | Domain | Range | Description |
|---|---|---|---|
| `scimantic:value` | `scimantic:Result` | `xsd:anySimpleType` | The numeric or categorical result. |
| `scimantic:unit` | `scimantic:Result` | `xsd:string` | Unit of measurement. |

### Resource & Agent Provenance
We avoid custom properties by leveraging specific external ontologies for each resource type:

#### Software (DOAP)
For `prov:SoftwareAgent`:
| Property | Domain | Range | Description |
|---|---|---|---|
| `doap:repository` | `prov:SoftwareAgent` | `doap:GitRepository` | Link to the code repository. |
| `doap:revision` | `prov:SoftwareAgent` | `xsd:string` | Specific commit hash or version tag. |
| `doap:file-release` | `prov:SoftwareAgent` | `xsd:anyURI` | Direct link to the release artifact (e.g., PyPI). |

#### Datasets (DCAT)
For `scimantic:Dataset` (which is also a `dcat:Dataset`):
| Property | Domain | Range | Description |
|---|---|---|---|
| `dcat:downloadURL` | `scimantic:Dataset` | `xsd:anyURI` | Direct download link. |
| `dcat:mediaType` | `scimantic:Dataset` | `xsd:string` | MIME type (e.g., "application/json"). |
| `dcat:byteSize` | `scimantic:Dataset` | `xsd:integer` | Size in bytes. |

#### Equipment & Facilities (SOSA)
For Experimental Facilities and Instruments (treated as `prov:Agent`):
| Property | Domain | Range | Description |
|---|---|---|---|
| `sosa:isHostedBy` | `sosa:Sensor` | `sosa:Platform` | Relates a specific instrument (Sensor) to the Facility (Platform). |
| `sosa:usedProcedure`| `sosa:Sensor` | `prov:Plan` | Links equipment to the standard operating procedure. |
| `sosa:madeObservation`| `sosa:Sensor` | `scimantic:Dataset`| Inverse of `prov:wasGeneratedBy` for sensor data. |

---

## 8. Gap Analysis Findings

### Gaps Resolved
*   **Uncertainty**: PROV has no uncertainty model. We resolve this by importing **URREF** and defininig `scimantic:hasUncertainty`.
*   **Scientific Workflow**: PROV describes generic "Activities". We subclass specific scientific steps (Hypothesis Formation, etc.) to give semantic meaning to the process.

### Open Gaps / constraints
*   **Result Structure**: `scimantic:value` is primitive. Complex tensor/matrix results may need more structure (e.g., sticking to `dcterms:format` pointing to an external file for large data).
*   **Integration with PROV-K**: We need to ensure `prov:supports`/`prov:contradicts` are correctly used between `Result` and `Hypothesis`.

---

## 9. Validation Rules (SHACL Candidates)
*   **Shape 1**: Every `scimantic:Hypothesis` MUST have at least one `prov:wasDerivedFrom` pointing to an `scimantic:Evidence`.
*   **Shape 2**: Every `scimantic:Result` MUST be `prov:wasGeneratedBy` a `scimantic:Analysis`.
*   **Shape 3**: All published Nanopubs (accessLevel != local) MUST have a `dcterms:license`.
