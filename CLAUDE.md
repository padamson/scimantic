# Guide for AI Assistants: Scimantic Development

This document provides context and guidelines for AI assistants (like Claude) working on the Scimantic codebase.

## Documentation Structure: Why, What, How

Scimantic uses a **multi-layered documentation approach** to separate concerns:

### 1. Vision Layer (WHY)
**File**: [VISION.md](docs/00-why-vision.md)

**Purpose**: Explains the problem we're solving and the value proposition

**Content**:
- Problem statement: What's broken in current scientific workflows?
- Scimantic's unique approach: Semantic-first, not semantic-retrofitted
- User personas and pain points
- Success metrics and guiding principles
- **Selective subset publishing**: Maintain private master KG, publish curated subsets for specific purposes
- Future vision: Collaborative extraction with publisher consent

**Audience**: Potential users, collaborators, funders

**When to read**: Before starting any new feature, to understand the "why"

### 2. Architecture Layer (WHAT - System Design)
**File**: [ARCHITECTURE.md](docs/01.1-what-architecture.md)

**Purpose**: Specifies the technical system we're building

**Content**:
- Semantic model: RDF/OWL ontologies, W3C PROV-O patterns, nanopublication structure
- Research entity types (Evidence, Hypothesis, Design, Analysis) with examples
- Provenance patterns (extraction, hypothesis formation, computation)
- Uncertainty representation and propagation rules
- **Master KG and subset publishing**: One private master KG, SPARQL-based subset generation, license-based management
- **Publishing destinations**: Nanopub servers, GitHub Pages, scimantic.io, Zenodo, institutional repos
- MCP integration architecture
- Design decisions and trade-offs

**Audience**: Developers, researchers evaluating semantic models

**When to read**: Before implementing core models or provenance logic

### 3. Roadmap Layer (WHAT - Implementation Sequence)
**File**: [ROADMAP.md](docs/02-when-roadmap.md)

**Purpose**: Defines WHEN we build capabilities, ordered to deliver value incrementally

**Content**:
- **Milestones 1-8**: Ordered by value and dependencies
- Features per milestone (linked to `docs/features/*.md`)
- Acceptance criteria (user-observable behavior)
- Current status and next steps
- **Future milestone**: Publisher partnerships for sanctioned extraction (3-5 years)

**Audience**: Developers planning work, project managers

**When to read**: To understand implementation priorities and dependencies

### 4. Feature Layer (WHAT - Individual Features)
**Files**: `docs/features/*.md`

**Purpose**: Specifies individual features using vertical slices

**Content**:
- User story: Who, what, why
- Acceptance criteria: Observable behavior
- Implementation tasks: Backend (Python/RDF), Frontend (TypeScript), Tests
- Vertical slices: End-to-end value delivery

**Audience**: Developers implementing specific features

**When to read**: Before starting work on a specific feature

### 5. Code Layer (HOW)
**Files**: `scimantic-core/src/**/*.py`, `scimantic-ext/src/**/*.ts`, tests

**Purpose**: Shows how the system actually works

**Content**:
- Tests specify behavior (executable specifications)
- Implementation is self-documenting with clear naming
- Comments explain "why" decisions were made, not "what" code does

**Audience**: Developers reading/writing code

**When to read**: Always! Code is the source of truth for "how"

## Project Philosophy

Scimantic is built on the principle that **the entire scientific research process should be machine-readable from the start**. We're not retrofitting semantics onto existing workflows; we're building a framework where semantics are native.

### Core Principles

1. **Semantic-First Design**: Every research artifact is RDF/OWL from inception
2. **Provenance is Mandatory**: W3C PROV-O tracking is not optional; it's fundamental
3. **Uncertainty is Explicit**: All measurements, hypotheses, and conclusions carry uncertainty metadata
4. **Nanopublications are Atomic**: The smallest publishable unit is a nanopublication (assertion + provenance + metadata)
5. **AI as Research Partner**: MCP integration allows AI agents to participate in the research process
6. **Selective Subset Publishing**: Researchers maintain one comprehensive private master KG and publish curated subsets for specific purposes
   - **Master KG**: Comprehensive private RDF graph (`project.ttl`), source of truth
   - **Subset Definitions**: SPARQL CONSTRUCT queries in `.scimantic/subsets/*.yaml`
   - **Generated Subsets**: Read-only snapshots in `subsets/*.ttl` (version controlled)
   - **License Management**: Every entity has `dcterms:license`, automatic analysis during generation
   - **Multi-Destination**: Publish to nanopub servers, GitHub Pages, scimantic.io, Zenodo, institutional repos

## Architecture

### Monorepo Structure

```
scimantic/                   # Monorepo root
├── scimantic-ontology/      # Ontology specification (source of truth)
│   ├── schema/
│   │   └── scimantic.yaml   # LinkML schema (domain model)
│   ├── generated/           # Generated artifacts
│   │   ├── scimantic.ttl    # OWL ontology
│   │   ├── shacl/           # SHACL shapes for validation
│   │   └── widoco.conf      # Documentation config
│   └── scripts/
│       └── inject_version.py
├── scimantic-core/          # Python package workspace member
│   ├── src/               # Source layout (modern Python best practice)
│   │   └── scimantic/       # Importable package
│   │       ├── models.py      # Generated from LinkML schema
│   │       ├── provenance.py  # W3C PROV-O tracker and decorators
│   │       ├── publish.py     # Nanopublication generation
│   │       ├── subset.py      # Subset definition, generation, license analysis
│   │       └── mcp.py         # MCP server for AI agent integration
│   ├── tests/
│   │   ├── test_ontology_specification.py  # SHACL validation tests
│   │   ├── test_models.py
│   │   ├── test_provenance.py
│   │   ├── test_publish.py
│   │   ├── test_mcp.py
│   │   └── integration/
│   │       └── test_agent_flow.py  # Agent simulation tests
│   └── pyproject.toml
├── scimantic-ext/           # TypeScript VS Code extension
│   └── src/
│       ├── providers/     # MCP client, graph visualization
│       └── commands/      # Extension commands
├── examples/
│   └── scimantic-paper/     # Reference implementation (manual testing)
│       ├── project.ttl    # Scimantic knowledge graph
│       └── ...            # Additional content varies by project
└── docs/
    └── features/         # Feature specifications (vertical slices)
```

**Why src layout?**
- Prevents accidental imports from source directory
- Forces proper package installation (even in editable mode)
- Modern Python packaging best practice
- Better test isolation

### Technology Stack

**scimantic-core (Python)**:
- **RDFLib**: RDF graph manipulation, SPARQL queries, Turtle serialization
- **W3C PROV-O**: Provenance ontology (Activities, Entities, Agents)
- **Nanopublications**: Trusty URIs, signed assertions
- **MCP SDK**: Model Context Protocol server implementation
- **pytest**: Test-driven development

**scimantic-ext (TypeScript)**:
- **VS Code Extension API**: Webviews, tree views, commands
- **MCP Client**: Communication with scimantic-core MCP server
- **Visualization**: Knowledge graph rendering (consider vis.js, cytoscape, or D3)

### Key Ontologies and Vocabularies

- **PROV-O** (`http://www.w3.org/ns/prov#`): Provenance
- **DC Terms** (`http://purl.org/dc/terms/`): Metadata
- **FOAF** (`http://xmlns.com/foaf/0.1/`): Agents (researchers)
- **Custom Scimantic Ontology** (`http://scimantic.io/ontology#`): Hypothesis, Design, Evidence, etc.

## Development Workflow: Test-Driven Development

Scimantic follows **traditional Test-Driven Development** practices for both `scimantic-core` (Python) and `scimantic-ext` (TypeScript). Feature implementation is tracked in `docs/features/*.md` files, not in task lists.

### Documentation Philosophy: Why, What, How

**Feature documentation (`docs/features/*.md`) documents the WHY and WHAT:**
- **Why**: Business value, user needs, research workflow goals
- **What**: Acceptance criteria, expected outcomes, RDF structure requirements

**Code is the HOW:**
- Tests specify behavior (executable specifications)
- Implementation is self-documenting with clear naming and minimal comments
- Comments explain "why" decisions were made, not "what" the code does

**Example**:
- ❌ Don't document: "Call `add_evidence()` with citation and content parameters"
- ✅ Do document: "Evidence must be captured with provenance metadata to enable hypothesis traceability"
- ✅ Let tests show: How to call the function
- ✅ Let code show: How it's implemented

### Traditional TDD Cycle (Red-Green-Refactor)

1. **Red - Write a Failing Test**: Write a unit or integration test that specifies desired behavior
2. **Green - Make it Pass**: Implement minimal code to make the test pass
3. **Refactor - Improve**: Clean up code while keeping tests green
4. **Repeat**: Continue for next piece of functionality

### Two-Loop TDD for Scimantic Ontology Development

Scimantic uses a **two-loop TDD approach** for ontology-driven development:

**Outer Loop - Specification Testing** (`test_ontology_specification.py`):
- **Purpose**: Validate that SHACL shapes correctly implement the ontology specification
- **Source of Truth**: `scimantic-ontology/schema/scimantic.yaml` (LinkML schema) and specification docs
- **Tests Are**: Executable specifications based on requirements, NOT derived from SHACL output
- **Avoids**: Circular testing (testing pyshacl by auto-generating tests from SHACL)
- **When Complete**: SHACL shapes correctly enforce ontology constraints

**Inner Loop - Implementation Testing** (unit/integration tests):
- **Purpose**: Validate that Python code (MCP tools, models) produces valid RDF
- **Source of Truth**: SHACL shapes and functional requirements
- **Tests Are**: Standard unit/integration tests for code behavior
- **When Complete**: MCP tools work correctly and produce ontology-compliant RDF

**Workflow for Implementing a Research Activity** (e.g., QuestionFormation):

1. **Review Specification**:
   - Read `scimantic-ontology/schema/scimantic.yaml` for the activity definition
   - Review legacy spec docs for context and examples
   - Understand constraints (e.g., "Question must be generated by QuestionFormation")

2. **Outer Loop - Write Specification Tests**:
   - Add tests to `test_ontology_specification.py`
   - Write positive tests: Valid graphs should pass SHACL validation
   - Write negative tests: Constraint violations should fail SHACL validation
   - Run tests → they should fail (SHACL shapes not yet implemented)

3. **Outer Loop - Implement SHACL Shapes**:
   - Update `scimantic-ontology/schema/scimantic.yaml` to add constraints
   - Run `uv run gen-all` to regenerate SHACL shapes
   - Run specification tests → they should pass
   - **Checkpoint**: Ontology specification is now correctly implemented

4. **Inner Loop - Implement MCP Tools**:
   - Write unit tests for new MCP tool (e.g., `add_question`)
   - Implement the tool to produce RDF that validates against SHACL
   - Write integration tests for end-to-end workflow
   - **Checkpoint**: Feature is complete and ontology-compliant

**Why This Matters**:
- Prevents specification drift: Tests are based on written requirements, not generated code
- Avoids circular testing: Don't test pyshacl by generating tests from SHACL output
- Clear separation: Ontology correctness vs. implementation correctness
- Tests become source of truth for specification behavior

### Python Package Testing (scimantic-core)

**Test Organization by TDD Loop**:

```
scimantic-core/tests/
├── conftest.py                          # Shared fixtures (validate_with_shacl, etc.)
├── test_ontology_specification.py       # OUTER LOOP: SHACL shape validation
│
├── unit/                                # INNER LOOP: Unit tests
│   ├── test_models.py                   # LinkML model classes
│   ├── test_provenance.py               # PROV-O tracking decorators
│   ├── test_publish.py                  # Nanopublication generation
│   └── test_mcp.py                      # MCP tool functions
│
└── integration/                         # INNER LOOP: Ontology workflow tests
    ├── test_question_formation.py       # QuestionFormation activity workflow
    └── ...                              # Additional activity workflows
```

**Outer Loop Tests** (`test_ontology_specification.py`):
- Validate SHACL shapes correctly implement ontology specification
- Source of truth: `scimantic-ontology/schema/scimantic.yaml` and specification docs
- Test both positive cases (valid graphs pass) and negative cases (invalid graphs fail)
- Organized by activity with test classes (e.g., `TestQuestionFormationPositive`, `TestQuestionFormationNegative`)
- Grows as new activities are added to the ontology

**Unit Tests** (`unit/`):
- Test individual classes and functions in isolation
- Mock external dependencies (RDFLib graphs, file I/O)
- Fast execution (milliseconds per test)
- All MCP tools tested in `unit/test_mcp.py`

**Integration Tests** (`integration/`):
- End-to-end happy path workflows for ontology activities
- Test complete activity flows: MCP tool → RDF graph → SHACL validation → persistence
- Each test file corresponds to an activity in the Scimantic ontology flow
- Use temporary directories for file I/O
- **Focus**: Validate that activities produce valid, compliant RDF graphs
- **Not included**: Generic infrastructure tests (e.g., "does MCP server start?")

**Running Tests**:
```bash
# Outer loop - specification tests
uv run pytest tests/test_ontology_specification.py -v

# Inner loop - all unit tests
uv run pytest tests/unit/ -v

# Inner loop - all integration tests
uv run pytest tests/integration/ -v

# All tests
uv run pytest tests/ -v
```

### TypeScript Extension Testing (scimantic-ext)

**Unit Tests**:
- Test individual functions and classes (providers, commands)
- Mock VS Code API and MCP client
- Use Jest or VS Code's test framework
- Location: `scimantic-ext/src/test/unit/`

**Integration Tests**:
- Test extension activation, command execution, MCP communication
- Use VS Code Extension Test Runner
- Location: `scimantic-ext/src/test/integration/`

### Manual Testing with examples/scimantic-paper

The `examples/scimantic-paper` directory contains **example usage** and serves as a **manual testing** playground:
- Demonstrates real-world usage of scimantic-core APIs
- Used to verify end-to-end workflows manually
- NOT a substitute for automated tests
- Dogfooding of Scimantic through researching design and implementation of Scimantic itself

### Feature Implementation Tracking

All implementation work is tracked in `docs/features/*.md` files using vertical slices:
- Each slice defines **What** to build (acceptance criteria, outcomes)
- Each slice explains **Why** it's valuable (user needs, research goals)
- Implementation tasks list components to modify, NOT how to modify them
- Check off tasks as they're completed
- DO NOT use separate task.md or similar files

The feature docs are a roadmap, not a cookbook. They answer:
- What problem are we solving?
- What does success look like?
- Which components need work?

The tests and code answer:
- How does it work?
- How do I use it?

### Test Coverage Goals

- **scimantic-core**: Aim for >80% code coverage
- **scimantic-ext**: Aim for >70% code coverage (UI testing is harder)
- All public APIs must have unit tests
- All MCP tools must have integration tests

## Semantic Web Patterns

### Nanopublication Structure

Every assertion in Scimantic should be wrapped as a nanopublication:

```turtle
@prefix : <http://example.org/np/> .
@prefix np: <http://www.nanopub.org/nschema#> .
@prefix prov: <http://www.w3.org/ns/prov#> .

:assertion_graph {
    :hypothesis_001 a scimantic:Hypothesis ;
        rdfs:label "DCS can be computed using MQDO" ;
        scimantic:uncertainty "0.15"^^xsd:float ;
        prov:wasDerivedFrom :evidence_001 .
}

:provenance_graph {
    :assertion_graph prov:wasAttributedTo :researcher_001 ;
        prov:generatedAtTime "2025-12-21T10:00:00Z"^^xsd:dateTime .
}

:pubinfo_graph {
    : a np:Nanopublication ;
        np:hasAssertion :assertion_graph ;
        np:hasProvenance :provenance_graph ;
        np:hasPublicationInfo :pubinfo_graph .
}
```

### Provenance Tracking Pattern

Use the `@activity` decorator for all computational steps:

```python
from scimantic.provenance import provenance_tracker

@provenance_tracker.activity(name="compute_dcs")
def compute_cross_section(input_file, method="MQDO"):
    # Automatically tracked as prov:Activity
    # Input file → prov:Entity (prov:used)
    # Output → prov:Entity (prov:wasGeneratedBy)
    return result
```

## Feature Development: Vertical Slices

New features are specified in `docs/features/*.md` using vertical slices. Each slice delivers end-to-end value.

### Slice Structure

1. **User Story**: Who, what, why
2. **Acceptance Criteria**: User-observable behavior
3. **Implementation Tasks**: Backend (Python/RDF), Frontend (TypeScript/VS Code), Tests

### Example: AI-Assisted Literature Search

**Why**: Enable semantic capture of literature from day one, creating a queryable knowledge graph that can be traced through to hypotheses.

**Slice 1 - What**: AI agent can add evidence to knowledge graph
- Acceptance: Evidence persisted as RDF with provenance metadata
- Components: scimantic-core models, MCP tools, integration tests

**Slice 2 - What**: Researchers visualize evidence in VS Code
- Acceptance: Tree view displays evidence, updates automatically
- Components: scimantic-ext UI, MCP client

The feature document describes what these slices deliver. The code shows how.

## Common Tasks

### Working on a Feature

1. **Read the feature doc**: Understand WHY and WHAT
2. **Write a failing test**: Specify expected behavior
3. **Implement**: Make the test pass
4. **Refactor**: Improve clarity while keeping tests green
5. **Update feature doc**: Check off completed tasks

The code itself shows HOW to:
- Add semantic entities (see existing models)
- Add MCP tools (see existing tools)
- Structure tests (see existing tests)

Learn by reading the code, not documentation.

## Debugging Tips

### Inspecting the RDF Graph

```python
# Load project.ttl
from rdflib import Graph
g = Graph()
g.parse("examples/scimantic-paper/project.ttl", format="turtle")

# SPARQL query
results = g.query("""
    SELECT ?s ?p ?o WHERE {
        ?s a scimantic:Hypothesis .
        ?s ?p ?o .
    }
""")
for row in results:
    print(row)
```

### Verifying Provenance

```python
# Check that Activity → Entity link exists
results = g.query("""
    PREFIX prov: <http://www.w3.org/ns/prov#>
    SELECT ?activity ?entity WHERE {
        ?entity prov:wasGeneratedBy ?activity .
    }
""")
```

## VS Code Extension Development

### MCP Client Pattern

```typescript
import { MCPClient } from '@modelcontextprotocol/client';

const client = new MCPClient({
    serverPath: 'uv',
    serverArgs: ['run', 'python', '-m', 'scimantic.mcp']
});

// Call MCP tool
const result = await client.callTool('add_evidence', {
    citation: 'Smith 2023',
    content: '...'
});
```

### Visualization

Use webviews to render the RDF graph. Fetch data via MCP `get_provenance_graph` tool.

## Best Practices

1. **Always Write Tests First**: TDD is non-negotiable
2. **Use Meaningful URIs**: `http://example.org/research/scimantic-paper/hypothesis_001`, not generic IDs
3. **Annotate Uncertainty**: Every hypothesis and measurement should have uncertainty metadata
4. **Link Everything**: Use PROV-O to connect all entities and activities
5. **Validate RDF**: Use `rdflib.Graph().serialize()` to ensure valid Turtle syntax
6. **Document Ontology Choices**: Comment why you chose specific predicates

## Resources

- [W3C PROV-O Specification](https://www.w3.org/TR/prov-o/)
- [Nanopublications](http://nanopub.org/)
- [RDFLib Documentation](https://rdflib.readthedocs.io/)
- [MCP Specification](https://modelcontextprotocol.io/)
- [VS Code Extension API](https://code.visualstudio.com/api)

## Questions?

When uncertain about design decisions:
1. Check existing patterns in `src/scimantic/models.py` and `src/scimantic/provenance.py`
2. Refer to W3C PROV-O examples
3. Consider: "Is this machine-readable and queryable via SPARQL?"
4. Ask: "Can an AI agent understand this without human interpretation?"

## Development Commands

```bash
# From monorepo root: Install all workspace members
uv sync

# From scimantic-core: Install with dev dependencies
cd scimantic-core && uv sync --extra dev

# Run tests
cd scimantic-core && uv run pytest -v

# Run tests with coverage
cd scimantic-core && uv run pytest --cov=scimantic --cov-report=html

# Start MCP server
cd scimantic-core && uv run python -m scimantic.mcp

# Format code
cd scimantic-core && uv run black src/scimantic tests/

# Lint code
cd scimantic-core && uv run flake8 src/scimantic tests/

# Generate ontology artifacts (TTL, SHACL shapes)
cd scimantic-core && uv run gen-all
```

### Documentation & Visualization Scripts

See [scripts/README.md](scripts/README.md) for full details.

```bash
# Build ontology documentation (requires Java 17+)
./scripts/build-docs.sh

# Build and preview documentation at http://localhost:8000
./scripts/preview-docs.sh

# Watch for schema changes, auto-rebuild, and serve
./scripts/watch-docs.sh

# Generate Mermaid diagram of ontology
cd scimantic-core && uv run python ../scripts/visualize_ontology.py
```
