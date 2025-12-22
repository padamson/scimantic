# Guide for AI Assistants: SemFlow Development

This document provides context and guidelines for AI assistants (like Claude) working on the SemFlow codebase.

## Project Philosophy

SemFlow is built on the principle that **the entire scientific research process should be machine-readable from the start**. We're not retrofitting semantics onto existing workflows; we're building a framework where semantics are native.

### Core Principles

1. **Semantic-First Design**: Every research artifact is RDF/OWL from inception
2. **Provenance is Mandatory**: W3C PROV-O tracking is not optional; it's fundamental
3. **Uncertainty is Explicit**: All measurements, hypotheses, and conclusions carry uncertainty metadata
4. **Nanopublications are Atomic**: The smallest publishable unit is a nanopublication (assertion + provenance + metadata)
5. **AI as Research Partner**: MCP integration allows AI agents to participate in the research process

## Architecture

### Monorepo Structure

```
semflow/                   # Monorepo root
├── semflow-core/          # Python package workspace member
│   ├── src/               # Source layout (modern Python best practice)
│   │   └── semflow/       # Importable package
│   │       ├── models.py      # Evidence, Hypothesis, Design, Entity classes
│   │       ├── provenance.py  # W3C PROV-O tracker and decorators
│   │       ├── publish.py     # Nanopublication generation
│   │       └── mcp.py         # MCP server for AI agent integration
│   ├── tests/
│   │   ├── test_models.py
│   │   ├── test_provenance.py
│   │   ├── test_publish.py
│   │   ├── test_mcp.py
│   │   └── integration/
│   │       └── test_agent_flow.py  # Agent simulation tests
│   └── pyproject.toml
├── semflow-ext/           # TypeScript VS Code extension
│   └── src/
│       ├── providers/     # MCP client, graph visualization
│       └── commands/      # Extension commands
├── examples/
│   └── semflow-paper/     # Reference implementation (manual testing)
│       ├── project.ttl    # SemFlow knowledge graph
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

**semflow-core (Python)**:
- **RDFLib**: RDF graph manipulation, SPARQL queries, Turtle serialization
- **W3C PROV-O**: Provenance ontology (Activities, Entities, Agents)
- **Nanopublications**: Trusty URIs, signed assertions
- **MCP SDK**: Model Context Protocol server implementation
- **pytest**: Test-driven development

**semflow-ext (TypeScript)**:
- **VS Code Extension API**: Webviews, tree views, commands
- **MCP Client**: Communication with semflow-core MCP server
- **Visualization**: Knowledge graph rendering (consider vis.js, cytoscape, or D3)

### Key Ontologies and Vocabularies

- **PROV-O** (`http://www.w3.org/ns/prov#`): Provenance
- **DC Terms** (`http://purl.org/dc/terms/`): Metadata
- **FOAF** (`http://xmlns.com/foaf/0.1/`): Agents (researchers)
- **Custom SemFlow Ontology** (`http://semflow.io/ontology#`): Hypothesis, Design, Evidence, etc.

## Development Workflow: Test-Driven Development

SemFlow follows **traditional Test-Driven Development** practices for both `semflow-core` (Python) and `semflow-ext` (TypeScript). Feature implementation is tracked in `docs/features/*.md` files, not in task lists.

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

### Python Package Testing (semflow-core)

**Unit Tests**:
- Test individual classes and functions in isolation
- Mock external dependencies (RDFLib graphs, MCP clients, file I/O)
- Fast execution (milliseconds per test)
- Location: `semflow-core/tests/test_*.py`

**Integration Tests**:
- Test component interactions (models + provenance, MCP tools + RDF persistence)
- Use temporary directories for file I/O
- Location: `semflow-core/tests/integration/test_*.py`

**Test Organization**:
```
semflow-core/tests/
├── test_models.py          # Unit tests for Evidence, Hypothesis, etc.
├── test_provenance.py      # Unit tests for PROV-O tracking
├── test_publish.py         # Unit tests for nanopublication generation
├── test_mcp.py             # Unit tests for MCP tools
└── integration/
    └── test_agent_flow.py  # Integration test: MCP → models → RDF persistence
```

**What TDD looks like:**
- Write a test that specifies what behavior you need
- Implement minimal code to make it pass
- Refactor while keeping tests green
- The tests and code document the "how"

### TypeScript Extension Testing (semflow-ext)

**Unit Tests**:
- Test individual functions and classes (providers, commands)
- Mock VS Code API and MCP client
- Use Jest or VS Code's test framework
- Location: `semflow-ext/src/test/unit/`

**Integration Tests**:
- Test extension activation, command execution, MCP communication
- Use VS Code Extension Test Runner
- Location: `semflow-ext/src/test/integration/`

### Manual Testing with examples/semflow-paper

The `examples/semflow-paper` directory contains **example usage** and serves as a **manual testing** playground:
- Demonstrates real-world usage of semflow-core APIs
- Used to verify end-to-end workflows manually
- NOT a substitute for automated tests
- Dogfooding of SemFlow through researching design and implementation of SemFlow itself

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

- **semflow-core**: Aim for >80% code coverage
- **semflow-ext**: Aim for >70% code coverage (UI testing is harder)
- All public APIs must have unit tests
- All MCP tools must have integration tests

## Semantic Web Patterns

### Nanopublication Structure

Every assertion in SemFlow should be wrapped as a nanopublication:

```turtle
@prefix : <http://example.org/np/> .
@prefix np: <http://www.nanopub.org/nschema#> .
@prefix prov: <http://www.w3.org/ns/prov#> .

:assertion_graph {
    :hypothesis_001 a semflow:Hypothesis ;
        rdfs:label "DCS can be computed using MQDO" ;
        semflow:uncertainty "0.15"^^xsd:float ;
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
from semflow.provenance import provenance_tracker

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
- Components: semflow-core models, MCP tools, integration tests

**Slice 2 - What**: Researchers visualize evidence in VS Code
- Acceptance: Tree view displays evidence, updates automatically
- Components: semflow-ext UI, MCP client

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
g.parse("examples/semflow-paper/project.ttl", format="turtle")

# SPARQL query
results = g.query("""
    SELECT ?s ?p ?o WHERE {
        ?s a semflow:Hypothesis .
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
    serverArgs: ['run', 'python', '-m', 'semflow.mcp']
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
2. **Use Meaningful URIs**: `http://example.org/research/semflow-paper/hypothesis_001`, not generic IDs
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
1. Check existing patterns in `src/semflow/models.py` and `src/semflow/provenance.py`
2. Refer to W3C PROV-O examples
3. Consider: "Is this machine-readable and queryable via SPARQL?"
4. Ask: "Can an AI agent understand this without human interpretation?"

## Development Commands

```bash
# From monorepo root: Install all workspace members
uv sync

# From semflow-core: Install with dev dependencies
cd semflow-core && uv sync --extra dev

# Run tests
cd semflow-core && uv run pytest -v

# Run tests with coverage
cd semflow-core && uv run pytest --cov=semflow --cov-report=html

# Start MCP server
cd semflow-core && uv run python -m semflow.mcp

# Format code
cd semflow-core && uv run black src/semflow tests/

# Lint code
cd semflow-core && uv run flake8 src/semflow tests/
```
