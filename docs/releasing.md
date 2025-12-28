# Scimantic Release Guide

This repository manages releases for three distinct components using **Scoped Tags**.

## Release Channels

| Component | Tag Pattern | Content | Validated Against | Output |
|---|---|---|---|---|
| **Ontology** | `ontology-v*` | `scimantic.ttl`, SHACL shapes | `scimantic.ttl`<br>`scimantic-shapes.ttl`<br>`urref-shapes.ttl` | Deployment to `scimantic.io`<br>GitHub Release |
| **Core (Python)** | `core-v*` | `scimantic-core` package | `pyproject.toml` | GitHub Release (Wheel)<br>*(PyPI Future)* |
| **Extension** | `ext-v*` | `scimantic-ext` VSIX | `package.json` | GitHub Release (.vsix)<br>*(Marketplace Future)* |

## How to Release

### 1. Ontology Release
1.  **Update Version Headers**: Manually update `owl:versionInfo` (and `owl:versionIRI`) in:
    *   `scimantic-core/ontology/scimantic.ttl`
    *   `scimantic-core/ontology/shacl/scimantic-shapes.ttl`
    *   `scimantic-core/ontology/shacl/urref-shapes.ttl`

    **Requirement**: All 3 files MUST have:
    *   `owl:versionInfo "X.Y.Z"`
    *   `owl:versionIRI <http://scimantic.io/v/X.Y.Z/scimantic>` (for ontology)
    *   `owl:versionIRI <http://scimantic.io/v/X.Y.Z/shapes>` (for shapes)
    *   `owl:versionIRI <http://scimantic.io/v/X.Y.Z/shapes/urref>` (for urref-shapes)

2.  **Commit**: Push changes to `main`.
3.  **Tag**:
    ```bash
    git tag ontology-v0.1.0
    git push origin ontology-v0.1.0
    ```
4.  **Verification**: The `Release Ontology` workflow will fail if any file version does not match `0.1.0`.

### 2. Core Release (Python)
1.  **Update Version**: Update `version` in `scimantic-core/pyproject.toml`.
2.  **Commit**: Push changes.
3.  **Tag**:
    ```bash
    git tag core-v0.1.0
    git push origin core-v0.1.0
    ```

### 3. Extension Release (VS Code)
1.  **Update Version**: Update `version` in `scimantic-ext/package.json`.
2.  **Commit**: Push changes.
3.  **Tag**:
    ```bash
    git tag ext-v0.1.0
    git push origin ext-v0.1.0
    ```

## Deployment Structure

Releases are permanently archived at:
```
https://scimantic.io/v/X.Y.Z/
```
The "latest" version is always available at the root:
```
https://scimantic.io/
```
