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
1.  **Update Version**: Update `version` in `scimantic-core/schema/scimantic.yaml` (e.g., to `0.1.0`).
2.  **Commit**:
    -   Stage `scimantic.yaml`.
    -   The `pre-commit` hook will auto-generate `scimantic.ttl`, `models.py`, and `scimantic-shapes.ttl` with the correct IRIs.
    -   Stage these generated files as well.
    -   Push changes to `main`.
3.  **Tag**:
    ```bash
    git tag ontology-v0.1.0
    git push origin ontology-v0.1.0
    ```
4.  **Verification**: The `Release Ontology` workflow will check that the tagged version matches the IRIs in the committed artifacts.

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
