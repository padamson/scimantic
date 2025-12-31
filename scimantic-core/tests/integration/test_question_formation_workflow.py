"""
Integration tests for QuestionFormation activity workflow.

Tests the complete workflow:
- QuestionFormation activity → Question entity
- Question persistence to RDF
- SHACL validation
- JSON retrieval for VS Code extension
"""

import json
import tempfile
from pathlib import Path

from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF, RDFS

from scimantic.config import SCIMANTIC_ONTOLOGY_URI

SCIMANTIC = Namespace(SCIMANTIC_ONTOLOGY_URI)
PROV = Namespace("http://www.w3.org/ns/prov#")


class TestQuestionFormationWorkflow:
    """Integration tests for QuestionFormation activity workflow"""

    def test_add_question_conforms_to_shacl(self, tmp_path, validate_with_shacl):
        """
        Test that adding a question produces a graph that conforms to Scimantic SHACL shapes.

        Workflow: add_question → RDF persistence → SHACL validation
        """
        from scimantic.mcp import add_question

        # 1. Setup
        project_ttl = tmp_path / "project.ttl"
        question_text = "What is the kinetic folding pathway of Protein X?"
        agent_uri = "urn:agent:researcher_001"

        # 2. Execute - QuestionFormation activity
        result = add_question(
            label=question_text, agent=agent_uri, project_path=str(project_ttl)
        )

        # 3. Load Data Graph
        data_graph = Graph()
        data_graph.parse(str(project_ttl), format="turtle")

        # 4. Validate using shared fixture
        validate_with_shacl(data_graph)

        # 5. Verify Question entity exists with correct properties
        question_uri = URIRef(result["uri"])
        labels = list(data_graph.objects(question_uri, RDFS.label))
        assert str(labels[0]) == question_text

    def test_add_question_creates_complete_graph(self):
        """
        Test that add_question creates Question entity with all required RDF structure.

        Workflow: add_question → RDF persistence → graph structure validation
        """
        from scimantic.mcp import add_question

        with tempfile.TemporaryDirectory() as tmpdir:
            project_file = Path(tmpdir) / "project.ttl"

            # Call add_question tool
            result = add_question(
                label="What is the kinetic folding pathway of Protein X?",
                agent="http://example.org/agent/test",
                project_path=str(project_file),
            )

            # Verify tool returned success
            assert result["status"] == "success"
            assert "uri" in result
            question_uri = result["uri"]

            # Verify file was created
            assert project_file.exists()

            # Load the RDF file
            g = Graph()
            g.parse(str(project_file), format="turtle")

            # Verify Question entity exists with dual typing
            uri_ref = URIRef(question_uri)
            types = list(g.objects(uri_ref, RDF.type))
            assert SCIMANTIC.Question in types
            assert PROV.Entity in types

            # Verify label property
            label = g.value(uri_ref, RDFS.label)
            assert str(label) == "What is the kinetic folding pathway of Protein X?"

            # Verify agent attribution
            agent = g.value(uri_ref, PROV.wasAttributedTo)
            assert str(agent) == "http://example.org/agent/test"

    def test_get_provenance_graph_returns_questions(self):
        """
        Test that get_provenance_graph_json includes questions list for VS Code extension.

        Workflow: add_question → get_provenance_graph_json → JSON structure validation
        """
        from scimantic.mcp import add_question, get_provenance_graph_json

        with tempfile.TemporaryDirectory() as tmpdir:
            project_file = Path(tmpdir) / "project.ttl"

            # Add a question
            add_question(
                label="Why does the sky turn violet?",
                agent="http://example.org/agent/test",
                project_path=str(project_file),
            )

            # Get graph JSON
            result_json = get_provenance_graph_json(str(project_file))
            data = json.loads(result_json)

            # Verify 'questions' key exists and contains our question
            assert "questions" in data, "JSON response missing 'questions' key"
            questions = data["questions"]
            assert len(questions) == 1

            q = questions[0]
            assert q["label"] == "Why does the sky turn violet?"
            assert "uri" in q
            assert "agent" in q
