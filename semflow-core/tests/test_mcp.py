"""
Unit tests for MCP tools (add_evidence, search_literature, etc.)

Tests that MCP server exposes tools correctly and integrates with models.
"""

import pytest
import tempfile
from pathlib import Path
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF

SEMFLOW = Namespace("http://semflow.io/ontology#")
PROV = Namespace("http://www.w3.org/ns/prov#")


class TestAddEvidenceTool:
    """Tests for add_evidence MCP tool"""

    def test_add_evidence_tool_exists(self):
        """Test that add_evidence tool is registered in MCP server"""
        from semflow.mcp import get_tools

        tools = get_tools()
        tool_names = [tool["name"] for tool in tools]

        assert "add_evidence" in tool_names

    def test_add_evidence_creates_and_persists(self):
        """Test add_evidence creates Evidence and writes to RDF file"""
        from semflow.mcp import add_evidence

        # Use temporary directory for test
        with tempfile.TemporaryDirectory() as tmpdir:
            project_file = Path(tmpdir) / "project.ttl"

            # Call add_evidence tool
            result = add_evidence(
                content="Nanopublications are smallest publishable units.",
                citation="Kuhn, T., et al. (2016).",
                source="https://doi.org/10.7717/peerj-cs.78",
                agent="http://example.org/agent/test",
                project_path=str(project_file),
            )

            # Verify tool returned success
            assert result["status"] == "success"
            assert "uri" in result
            evidence_uri = result["uri"]

            # Verify file was created
            assert project_file.exists()

            # Load the RDF file
            g = Graph()
            g.parse(str(project_file), format="turtle")

            # Verify Evidence entity exists with correct types
            uri_ref = URIRef(evidence_uri)
            types = list(g.objects(uri_ref, RDF.type))
            assert SEMFLOW.Evidence in types
            assert PROV.Entity in types

            # Verify properties
            content = g.value(uri_ref, SEMFLOW.content)
            assert str(content) == "Nanopublications are smallest publishable units."

    def test_add_evidence_appends_to_existing_graph(self):
        """Test that multiple add_evidence calls accumulate in the same graph"""
        from semflow.mcp import add_evidence

        with tempfile.TemporaryDirectory() as tmpdir:
            project_file = Path(tmpdir) / "project.ttl"

            # Add first evidence
            result1 = add_evidence(
                content="First finding.",
                citation="Author A (2020).",
                source="https://doi.org/10.example/1",
                agent="http://example.org/agent/test",
                project_path=str(project_file),
            )

            # Add second evidence
            result2 = add_evidence(
                content="Second finding.",
                citation="Author B (2021).",
                source="https://doi.org/10.example/2",
                agent="http://example.org/agent/test",
                project_path=str(project_file),
            )

            # Both should succeed with different URIs
            assert result1["status"] == "success"
            assert result2["status"] == "success"
            assert result1["uri"] != result2["uri"]

            # Load the graph
            g = Graph()
            g.parse(str(project_file), format="turtle")

            # Verify both Evidence entities exist
            evidence_entities = list(g.subjects(RDF.type, SEMFLOW.Evidence))
            assert len(evidence_entities) >= 2

    def test_add_evidence_validates_required_parameters(self):
        """Test that add_evidence requires all mandatory parameters"""
        from semflow.mcp import add_evidence

        with tempfile.TemporaryDirectory() as tmpdir:
            project_file = Path(tmpdir) / "project.ttl"

            # Missing content should fail
            with pytest.raises((TypeError, ValueError)):
                add_evidence(
                    citation="Test citation",
                    source="https://example.org",
                    agent="http://example.org/agent/test",
                    project_path=str(project_file),
                )

            # Missing citation should fail
            with pytest.raises((TypeError, ValueError)):
                add_evidence(
                    content="Test content",
                    source="https://example.org",
                    agent="http://example.org/agent/test",
                    project_path=str(project_file),
                )
