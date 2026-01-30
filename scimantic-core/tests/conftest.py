import pytest
from pathlib import Path
from rdflib import Graph
from pyshacl import validate


@pytest.fixture(scope="session")
def ontology_graph():
    """Load the Scimantic ontology once per session."""
    # Path to scimantic-ontology sibling package
    ontology_path = (
        Path(__file__).parent.parent.parent
        / "scimantic-ontology"
        / "generated"
        / "scimantic.ttl"
    )
    if not ontology_path.exists():
        pytest.fail(f"Ontology file not found at {ontology_path}")

    g = Graph()
    g.parse(str(ontology_path), format="turtle")
    return g


@pytest.fixture(scope="session")
def shacl_graph():
    """Load the SHACL shapes once per session."""
    shapes_path = (
        Path(__file__).parent.parent.parent
        / "scimantic-ontology"
        / "generated"
        / "shacl"
        / "scimantic-shapes.ttl"
    )
    if not shapes_path.exists():
        pytest.fail(f"SHACL shapes file not found at {shapes_path}")

    g = Graph()
    g.parse(str(shapes_path), format="turtle")
    return g


@pytest.fixture
def validate_with_shacl(ontology_graph, shacl_graph):
    """
    Returns a callable that validates a given data graph against the loaded shapes.
    Usage:
        def test_foo(validate_with_shacl):
            ...
            validate_with_shacl(data_graph)
    """

    def _validate(data_graph):
        conforms, results_graph, results_text = validate(
            data_graph,
            shacl_graph=shacl_graph,
            ont_graph=ontology_graph,
            inference="rdfs",
            abort_on_first=False,
            meta_shacl=False,
            debug=False,
        )
        assert conforms, f"SHACL Validation Failed:\n{results_text}"
        return True

    return _validate
