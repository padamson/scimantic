# SemFlow Ontology

This directory contains the formal ontology definition for SemFlow.

## Files

- **semflow.ttl**: The SemFlow ontology in Turtle format
  - Defines domain-specific classes (Evidence, Hypothesis, Design, etc.)
  - Built on W3C PROV-O for provenance tracking
  - Uses Dublin Core for metadata
  - References nanopublication schema for publication

## Design Principles

1. **Reuse Before Create**: Extend W3C PROV-O and Dublin Core instead of creating new concepts
2. **Standards-First**: Use official schemas (PROV-O, nanopub, QUDT) wherever possible
3. **Minimal Extension**: Only define SemFlow-specific concepts not in existing ontologies
4. **Provenance Built-In**: All research artifacts are PROV-O Entities/Activities

## Key Design Decisions

### All Research Artifacts are PROV-O Entities

Every scientific artifact (Evidence, Hypothesis, Dataset, Result) is a subclass of `prov:Entity`. This enables:
- Full provenance tracking via `prov:wasDerivedFrom`, `prov:wasGeneratedBy`
- Agent attribution via `prov:wasAttributedTo`
- Temporal tracking via `prov:generatedAtTime`
- Standard PROV-O queries work automatically

### Activities Follow PROV-O Pattern

Experimental activities and analyses are `prov:Activity` instances:
- Link to inputs via `prov:used`
- Link to outputs via `prov:generated`
- Track who performed it via `prov:wasAssociatedWith`
- Track when via `prov:startedAtTime`, `prov:endedAtTime`

### Designs are PROV-O Plans

Experimental designs and methods are `prov:Plan` instances:
- Can be used by activities via `prov:used`
- Link back to hypotheses via `prov:wasDerivedFrom`

### Publications Use Dublin Core

Publication metadata uses standard Dublin Core terms:
- `dcterms:title`, `dcterms:creator`, `dcterms:date`
- `dcterms:bibliographicCitation` for formatted citations
- `dcterms:identifier` for DOIs

### Nanopublications Use Official Schema

For publication, we use the official nanopub schema:
- `np:Nanopublication` with `np:hasAssertion`, `np:hasProvenance`, `np:hasPublicationInfo`
- See: http://nanopub.org/nschema#

### Uncertainty Uses External Ontologies

For uncertainty quantification, SemFlow recommends:
- **QUDT** (http://www.qudt.org/) for statistical uncertainties, confidence intervals
- **Uncertainty Ontology** (http://purl.org/uncertainty#) for general uncertainty concepts

## Validation

The ontology can be validated using standard RDF/OWL tools:

```bash
# Using rapper (part of raptor2-utils)
rapper -i turtle -o ntriples semflow.ttl

# Using Protégé
# Open semflow.ttl in Protégé and run the reasoner
```

## Usage in Code

Python code should reference this ontology:

```python
from rdflib import Graph, Namespace

SEMFLOW = Namespace("http://semflow.io/ontology#")
PROV = Namespace("http://www.w3.org/ns/prov#")

# Evidence is a PROV-O Entity
evidence_uri = URIRef("http://example.org/evidence/001")
g.add((evidence_uri, RDF.type, SEMFLOW.Evidence))
g.add((evidence_uri, RDF.type, PROV.Entity))  # Also mark as PROV Entity
```

## References

- [W3C PROV-O](https://www.w3.org/TR/prov-o/)
- [Dublin Core Metadata Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/)
- [Nanopublication Schema](http://nanopub.org/nschema#)
- [QUDT](http://www.qudt.org/)
- [FOAF](http://xmlns.com/foaf/spec/)
