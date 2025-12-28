from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDFS

from scimantic.config import SCIMANTIC_ONTOLOGY_URI
from scimantic.mcp import add_question
from scimantic.models import Question

# Namespaces (matching config.py logic)
SCIMANTIC = Namespace(SCIMANTIC_ONTOLOGY_URI)


def test_question_model_instantiation():
    """Test that we can create a Question model."""
    q = Question(
        id="http://example.org/q1", label="Why?", wasAttributedTo="urn:agent:1"
    )
    assert q.label == "Why?"
    assert q.id == "http://example.org/q1"


def test_add_question_conforms_to_shacl(tmp_path, validate_with_shacl):
    """
    Test that adding a question produces a graph that conforms to Scimantic SHACL shapes.
    """
    # 1. Setup
    project_ttl = tmp_path / "project.ttl"
    question_text = "What is the kinetic folding pathway of Protein X?"
    agent_uri = "urn:agent:researcher_001"

    # 2. Execute
    result = add_question(
        label=question_text, agent=agent_uri, project_path=str(project_ttl)
    )

    # 3. Load Data Graph
    data_graph = Graph()
    data_graph.parse(str(project_ttl), format="turtle")

    # 4. Validate using shared fixture
    validate_with_shacl(data_graph)

    # 5. Minimal Value Checks
    question_uri = URIRef(result["uri"])
    labels = list(data_graph.objects(question_uri, RDFS.label))
    assert str(labels[0]) == question_text
