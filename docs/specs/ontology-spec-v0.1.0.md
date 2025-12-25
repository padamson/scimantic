# Scimantic Ontology Specification (v0.1.0)

This document specifies the classes, properties, and constraints for the `scimantic` ontology version 0.1.0. It serves as the blueprint for implementing the `scimantic.ttl` file.

## 1. Metadata & Namespaces

- **URI**: `http://scimantic.io/ontology#`
- **Preferred Prefix**: `scimantic`
- **Version**: 0.1.0
- **License**: CC-BY 4.0

### External Dependencies
| Prefix | URI | Purpose |
|---|---|---|
| `prov` | `http://www.w3.org/ns/prov#` | Core provenance backbone |
| `urref` | `http://www.w3.org/ns/urref#` | Uncertainty representation |
| `dcterms` | `http://purl.org/dc/terms/` | General metadata |
| `np` | `http://www.nanopub.org/nschema#` | Nanopublication structure |
| `foaf` | `http://xmlns.com/foaf/0.1/` | Agent details |

---

## 2. Methodology & AIDA Compliance

Scimantic uses **PROV-O** as the upper ontology. Every Scimantic class is a subclass of a PROV concept.

**AIDA Principles Compliance**:
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
| `scimantic:Hypothesis` | `prov:Entity`, `np:Nanopublication` | A testable claim derived from evidence. |
| `scimantic:Design` | `prov:Entity`, `prov:Plan` | A specification of the method to be executed. |
| `scimantic:Dataset` | `prov:Entity` | Raw data/measurements produced by execution. |
| `scimantic:Result` | `prov:Entity` | The outcome of an analysis. |

### Note on Result vs Analysis
To resolve ambiguity from early architectural drafts:
*   **`scimantic:Analysis`**: The **Activity** (process) of performing the computation/analysis.
*   **`scimantic:Result`**: The **Entity** (artifact) produced by that activity.

---

## 4. Activity Classes

All are subclasses of `prov:Activity`. They represent the steps of the Scientific Method.

| Class | Subclass Of | Description |
|---|---|---|
| `scimantic:QuestionFormation` | `prov:Activity` | Creating a Question. |
| `scimantic:LiteratureSearch` | `prov:Activity` | Searching and extracting Evidence. |
| `scimantic:Assessment` | `prov:Activity` | Evaluating Evidence. |
| `scimantic:HypothesisFormation` | `prov:Activity` | Synthesizing Evidence into a Hypothesis. |
| `scimantic:DesignPlanning` | `prov:Activity` | Creating a Design from a Hypothesis. |
| `scimantic:Execution` | `prov:Activity` | running a Design to produce a Dataset. |
| `scimantic:Analysis` | `prov:Activity` | Processing a Dataset to produce a Result. |

---

## 5. Properties

### Core Domain Properties

| Property | Domain | Range | Description |
|---|---|---|---|
| `scimantic:hasUncertainty` | `prov:Entity` | `urref:UncertaintyEntity` | Links a scientific entity to its uncertainty model. |
| `scimantic:accessLevel` | `np:Nanopublication` | `xsd:string` | Publishing scope (local, institutional, public, public_essential_evidence). |
| `scimantic:publishable` | `np:Nanopublication` | `xsd:boolean` | Flag indicating if this is ready for public promotion. |

### Design & Method Properties
| Property | Domain | Range | Description |
|---|---|---|---|
| `scimantic:method` | `scimantic:Design` | `xsd:string` (or URI) | Name/description of method. |
| `scimantic:parameter` | `scimantic:Design` | `scimantic:Parameter` | Structured configuration. |
| `scimantic:expectedOutcome`| `scimantic:Design` | `scimantic:Hypothesis`| What hypothesis this design tests. |

### Result Properties
| Property | Domain | Range | Description |
|---|---|---|---|
| `scimantic:value` | `scimantic:Result` | `xsd:anySimpleType` | The numeric or categorical result. |
| `scimantic:unit` | `scimantic:Result` | `xsd:string` | Unit of measurement. |

### Software Provenance
| Property | Domain | Range | Description |
|---|---|---|---|
| `scimantic:codeRepository`| `prov:SoftwareAgent`| `xsd:anyURI` | Git repo URL. |
| `scimantic:commitHash` | `prov:SoftwareAgent`| `xsd:string` | Specific commit used. |

---

## 6. Gap Analysis Findings

### Gaps Resolved
*   **Uncertainty**: PROV has no uncertainty model. We resolve this by importing **URREF** and defininig `scimantic:hasUncertainty`.
*   **Scientific Workflow**: PROV describes generic "Activities". We subclass specific scientific steps (Hypothesis Formation, etc.) to give semantic meaning to the process.

### Open Gaps / constraints
*   **Result Structure**: `scimantic:value` is primitive. Complex tensor/matrix results may need more structure (e.g., sticking to `dcterms:format` pointing to an external file for large data).
*   **Integration with PROV-K**: We need to ensure `prov:supports`/`prov:contradicts` are correctly used between `Result` and `Hypothesis`.

---

## 7. Validation Rules (SHACL Candidates)
*   **Shape 1**: Every `scimantic:Hypothesis` MUST have at least one `prov:wasDerivedFrom` pointing to an `scimantic:Evidence`.
*   **Shape 2**: Every `scimantic:Result` MUST be `prov:wasGeneratedBy` a `scimantic:Analysis`.
*   **Shape 3**: All published Nanopubs (accessLevel != local) MUST have a `dcterms:license`.
