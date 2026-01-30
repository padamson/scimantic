# Spec-Driven and Test-Driven Development

This document describes **HOW** Scimantic uses specification-first and test-driven development practices across its polyglot codebase (Python, TypeScript, Rust).

For **WHY** we build Scimantic, see [Vision](00-why-vision.md).
For **WHAT** we're building, see [Architecture](01.1-what-architecture.md).
For **WHEN** we build features, see [Roadmap](02-when-roadmap.md).

## Overview: Specs as Testable Artifacts

Scimantic treats specifications not as documentation, but as **testable contracts**. This enables:

1. **Multiple implementations** from a single source of truth
2. **Automated validation** that implementations match specs
3. **Code generation** to reduce boilerplate and drift
4. **Language-agnostic interoperability** across Python, TypeScript, and Rust

```
┌─────────────────────────────────────────────────────────────┐
│  Specifications (Source of Truth)                           │
│  ├── schema/scimantic.yaml (LinkML - domain model)          │
│  └── specs/scimantic-api.yaml (OpenAPI - HTTP API)          │
└─────────────────────────────────────────────────────────────┘
                              ↓ generates
┌─────────────────────────────────────────────────────────────┐
│  Derived Artifacts                                          │
│  ├── Python: dataclasses, Pydantic models, SHACL shapes     │
│  ├── TypeScript: types, API client                          │
│  └── Rust: structs, API client                              │
└─────────────────────────────────────────────────────────────┘
                              ↓ tested by
┌─────────────────────────────────────────────────────────────┐
│  Contract Tests                                             │
│  ├── Ontology: SHACL validation tests                       │
│  └── API: OpenAPI contract tests (Schemathesis, Dredd)      │
└─────────────────────────────────────────────────────────────┘
```

## Two Specification Layers

### 1. Domain Model (LinkML)

**File**: `schema/scimantic.yaml`

**Purpose**: Defines what entities exist (Evidence, Hypothesis, Question, etc.) and their relationships.

**Generates**:
- OWL ontology (for reasoning and interoperability)
- SHACL shapes (for RDF validation)
- JSON Schema (for API payload validation)
- Python dataclasses (for type-safe code)

**Testing**: Outer-loop TDD validates SHACL shapes against specification requirements.

```bash
# Generate all artifacts from LinkML schema
cd scimantic-core && uv run gen-all

# Run ontology specification tests
uv run pytest tests/test_ontology_specification.py -v
```

### 2. HTTP API (OpenAPI)

**File**: `specs/scimantic-api.yaml` (when scimantic-server is built)

**Purpose**: Defines how implementations communicate over HTTP — endpoints, request/response formats, authentication.

**Generates**:
- Server stubs (FastAPI, axum)
- Client libraries (TypeScript, Rust)
- API documentation (Swagger UI, Redoc)

**Testing**: Contract tests validate that server responses match the OpenAPI spec.

```bash
# Validate spec syntax
openapi-spec-validator specs/scimantic-api.yaml

# Run contract tests against running server
schemathesis run specs/scimantic-api.yaml --base-url http://localhost:8000
```

## Two-Loop TDD Pattern

Both specification layers use the same two-loop TDD pattern:

### Outer Loop: Specification Compliance

Tests that the implementation conforms to the spec. These are **derived from written requirements**, not from implementation details.

```
Write/Update Spec → Run Compliance Tests → FAIL → Implement → PASS
```

### Inner Loop: Behavior Testing

Tests that the implementation behaves correctly. Standard unit and integration tests.

```
Write Test → FAIL → Implement → PASS → Refactor
```

### Example: Adding a New Entity Type

**Outer Loop (Ontology Spec)**:
1. Add entity definition to `schema/scimantic.yaml`
2. Write specification test in `test_ontology_specification.py`
3. Run test → FAIL (SHACL shapes don't exist yet)
4. Run `uv run gen-all` to generate SHACL shapes
5. Run test → PASS

**Inner Loop (Implementation)**:
1. Write unit test for MCP tool that creates the entity
2. Run test → FAIL
3. Implement MCP tool
4. Run test → PASS
5. Refactor

**Outer Loop (API Spec)** — when building server:
1. Add endpoint to `specs/scimantic-api.yaml`
2. Run contract tests → FAIL
3. Implement endpoint
4. Run contract tests → PASS

## Language-Specific Tooling

### Python

| Task | Tool | Command |
|------|------|---------|
| Generate models from LinkML | `gen-python` | `uv run gen-python schema/scimantic.yaml` |
| Generate models from OpenAPI | `datamodel-codegen` | `datamodel-codegen --input specs/api.yaml --output models.py` |
| Contract testing | Schemathesis | `schemathesis run specs/api.yaml --base-url http://localhost:8000` |
| SHACL validation | pyshacl | `from pyshacl import validate` |
| Unit testing | pytest | `uv run pytest tests/ -v` |

**Schemathesis example**:
```python
# tests/test_api_contract.py
import schemathesis

schema = schemathesis.from_path("specs/scimantic-api.yaml")

@schema.parametrize()
def test_api_conforms_to_spec(case):
    """Generated tests for every endpoint in the spec."""
    response = case.call_and_validate()
```

### TypeScript

| Task | Tool | Command |
|------|------|---------|
| Generate types from OpenAPI | `openapi-typescript` | `npx openapi-typescript specs/api.yaml -o src/types/api.ts` |
| Generate client from OpenAPI | `openapi-fetch` | Use with generated types |
| Mock server from spec | Prism | `npx @stoplight/prism-cli mock specs/api.yaml` |
| Contract testing | Dredd | `npx dredd specs/api.yaml http://localhost:8000` |
| Unit testing | vitest/jest | `npm test` |

**Type generation example**:
```bash
# Generate TypeScript types from OpenAPI spec
npx openapi-typescript specs/scimantic-api.yaml -o src/types/api.ts
```

```typescript
// src/api/client.ts
import createClient from 'openapi-fetch';
import type { paths } from './types/api';

const client = createClient<paths>({ baseUrl: 'https://api.scimantic.io' });

// Fully typed - IDE knows request/response shapes
const { data, error } = await client.POST('/api/projects/{projectId}/evidence', {
  params: { path: { projectId: '123' } },
  body: { citation: 'Smith 2024', content: '...' }
});
```

### Rust

| Task | Tool | Command |
|------|------|---------|
| Generate client from OpenAPI | `progenitor` | Custom build script |
| Generate server stubs | `openapi-generator` | `openapi-generator generate -i specs/api.yaml -g rust-axum` |
| Contract testing | Dredd (external) | `npx dredd specs/api.yaml http://localhost:8000` |
| Unit testing | cargo test | `cargo test` |

**Note**: Rust's OpenAPI ecosystem is less mature. For servers, consider writing the OpenAPI spec first, then implementing manually in axum/actix with the spec as your guide. Use Dredd for contract testing.

**Progenitor example** (client generation):
```rust
// build.rs
use progenitor::GenerationSettings;

fn main() {
    let spec = std::fs::read_to_string("../specs/scimantic-api.yaml").unwrap();
    let settings = GenerationSettings::default();
    progenitor::generate_text(&spec, settings).unwrap();
}
```

## Contract Testing (Language-Agnostic)

Contract tests validate that a running server matches the OpenAPI spec. They don't care what language the server is written in.

### Dredd (Node.js)

Works with any HTTP server:

```bash
# Install
npm install -g dredd

# Run against any server
dredd specs/scimantic-api.yaml http://localhost:8000

# With hooks for setup/teardown (JavaScript)
dredd specs/scimantic-api.yaml http://localhost:8000 --hookfiles=./test/hooks.js
```

### Schemathesis (Python)

More powerful than Dredd — generates edge cases, fuzzes inputs:

```bash
# Install
pip install schemathesis

# Run against any server
schemathesis run specs/scimantic-api.yaml --base-url http://localhost:8000

# Stateful testing (tests sequences of requests)
schemathesis run specs/scimantic-api.yaml --base-url http://localhost:8000 --stateful=links
```

### Prism (Mock Server)

Run a mock server from your spec for frontend development:

```bash
# Install
npm install -g @stoplight/prism-cli

# Start mock server
prism mock specs/scimantic-api.yaml

# Mock server now running at http://localhost:4010
# Returns example responses from your spec
```

## Workflow: Adding a New API Endpoint

1. **Design**: Add endpoint to `specs/scimantic-api.yaml`

```yaml
paths:
  /api/projects/{projectId}/hypotheses:
    post:
      summary: Create a hypothesis
      operationId: createHypothesis
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/HypothesisCreate'
      responses:
        '201':
          description: Hypothesis created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Hypothesis'
```

2. **Contract Test**: Run Schemathesis/Dredd → FAIL (endpoint doesn't exist)

```bash
schemathesis run specs/scimantic-api.yaml --base-url http://localhost:8000
# FAILED: POST /api/projects/{projectId}/hypotheses - 404 Not Found
```

3. **Behavior Test**: Write unit test for the endpoint logic

```python
# tests/test_hypothesis_endpoint.py
def test_create_hypothesis_links_to_evidence(client, project_with_evidence):
    response = client.post(
        f"/api/projects/{project_with_evidence.id}/hypotheses",
        json={
            "statement": "X causes Y",
            "confidence": 0.75,
            "supporting_evidence": [str(evidence_uri)]
        }
    )

    assert response.status_code == 201
    hypothesis = response.json()
    assert hypothesis["supporting_evidence"] == [str(evidence_uri)]
```

4. **Implement**: Write the endpoint

```python
# src/scimantic_server/routes/hypotheses.py
@router.post("/projects/{project_id}/hypotheses", status_code=201)
def create_hypothesis(
    project_id: str,
    hypothesis: HypothesisCreate,
    db: Session = Depends(get_db)
) -> Hypothesis:
    # Implementation
    ...
```

5. **Verify**: Run contract tests → PASS

```bash
schemathesis run specs/scimantic-api.yaml --base-url http://localhost:8000
# PASSED: All endpoints conform to spec
```

6. **Generate Client**: Update TypeScript types

```bash
npx openapi-typescript specs/scimantic-api.yaml -o src/types/api.ts
# TypeScript client now has createHypothesis method with full types
```

## CI/CD Integration

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  spec-validation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Validate OpenAPI spec
        run: npx @stoplight/spectral-cli lint specs/scimantic-api.yaml

      - name: Validate LinkML schema
        run: |
          cd scimantic-core
          uv run linkml-validate schema/scimantic.yaml

  contract-tests:
    runs-on: ubuntu-latest
    needs: spec-validation
    steps:
      - uses: actions/checkout@v4

      - name: Start server
        run: |
          cd scimantic-server
          docker-compose up -d
          sleep 10  # Wait for server to start

      - name: Run contract tests
        run: |
          pip install schemathesis
          schemathesis run specs/scimantic-api.yaml --base-url http://localhost:8000

  ontology-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run ontology specification tests
        run: |
          cd scimantic-core
          uv sync
          uv run pytest tests/test_ontology_specification.py -v

  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Python tests
        run: |
          cd scimantic-core
          uv sync
          uv run pytest tests/unit tests/integration -v

      - name: Run TypeScript tests
        run: |
          cd scimantic-ext
          npm ci
          npm test
```

## Summary: Spec-First + TDD

| Layer | Spec Format | Test Tool | Generated Artifacts |
|-------|-------------|-----------|---------------------|
| Domain Model | LinkML | pyshacl + pytest | SHACL, Python classes, JSON Schema |
| HTTP API | OpenAPI 3.x | Schemathesis, Dredd | Server stubs, clients, docs |
| RDF Data | SHACL shapes | pyshacl | Validation reports |

**Key principles**:

1. **Specs are contracts**, not documentation — they're testable
2. **Generate, don't handwrite** — reduces drift between spec and implementation
3. **Contract tests are language-agnostic** — test any server against the same spec
4. **Two loops**: outer (spec compliance) + inner (behavior)

**When to use each approach**:

| Situation | Approach |
|-----------|----------|
| Rapid prototyping, single implementation | Code-first (generate spec from code) |
| Multiple implementations, external consumers | Spec-first (generate code from spec) |
| Polyglot codebase | Spec-first (one spec, multiple language implementations) |

Scimantic uses **spec-first for shared contracts** (LinkML schema, future OpenAPI) and **code-first for internal implementation** (MCP tools during iteration).
