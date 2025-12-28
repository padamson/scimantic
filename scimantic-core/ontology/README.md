# Scimantic Ontology Source

This directory contains the core ontology sources and validation shapes for Scimantic.

> **Note**: For the official specification, see [Ontology Specification v0.1.0](../../docs/03-how-specifications/ontology-spec-v0.1.0.md).
> For design rationale and feature details, see [Theory of Constraints](../../docs/00-why-vision.md) and [Architecture](../../docs/01-what-architecture.md).

## Directory Inventory

### `scimantic.ttl`
The definitive Turtle source for the Scimantic Ontology, generated from [LinkML](https://linkml.io) schema [../schema/scimantic.yaml](../schema/scimantic.yaml).
- **URI**: `http://scimantic.io`
- **Dependencies**: PROV-O, URREF, DCAT, DOAP, SOSA, Nanopub.

### `widoco.conf`
Configuration file for [Widoco](https://github.com/dgarijo/Widoco), used in the CI/CD pipeline to generate HTML documentation from `scimantic.ttl`.

### `catalog-v001.xml`
Standard OWL Catalog file that maps ontology URIs (e.g., `http://scimantic.io/shapes`) to local file paths. This ensures tools like Protégé and Widoco can find the imported SHACL shapes without needing to resolve them over the internet.

### `shacl/`
Contains [SHACL](https://www.w3.org/TR/shacl/) shapes used to validate Knowledge Graphs against the Scimantic schema. (Also generated from LinkML schema [../schema/scimantic.yaml](../schema/scimantic.yaml).)
- `shacl/scimantic-shapes.ttl`: Defines constraints for Entities, Activities, and Uncertainty.
