"""
Unit tests for MCP tools (add_evidence, search_literature, etc.)

Tests that MCP server exposes tools correctly and integrates with models.
"""

import tempfile
from pathlib import Path

import pytest
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF

SCIMANTIC = Namespace("http://scimantic.io/ontology#")
PROV = Namespace("http://www.w3.org/ns/prov#")


class TestAddEvidenceTool:
    """Tests for add_evidence MCP tool"""

    def test_add_evidence_tool_exists(self):
        """Test that add_evidence tool is registered in MCP server"""
        from scimantic.mcp import get_tools

        tools = get_tools()
        tool_names = [tool["name"] for tool in tools]

        assert "add_evidence" in tool_names

    def test_add_evidence_creates_and_persists(self):
        """Test add_evidence creates Evidence and writes to RDF file"""
        from scimantic.mcp import add_evidence

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
            assert SCIMANTIC.Evidence in types
            assert PROV.Entity in types

            # Verify properties
            content = g.value(uri_ref, SCIMANTIC.content)
            assert str(content) == "Nanopublications are smallest publishable units."

    def test_add_evidence_appends_to_existing_graph(self):
        """Test that multiple add_evidence calls accumulate in the same graph"""
        from scimantic.mcp import add_evidence

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
            evidence_entities = list(g.subjects(RDF.type, SCIMANTIC.Evidence))
            assert len(evidence_entities) >= 2

    def test_add_evidence_validates_required_parameters(self):
        """Test that add_evidence requires all mandatory parameters"""
        from scimantic.mcp import add_evidence

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


class TestGetProvenanceGraphTool:
    """Tests for get_provenance_graph MCP tool (JSON format for VS Code extension)"""

    def test_get_provenance_graph_tool_exists(self):
        """Test that get_provenance_graph tool is registered in MCP server"""
        from scimantic.mcp import get_tools

        tools = get_tools()
        tool_names = [tool["name"] for tool in tools]

        assert "get_provenance_graph" in tool_names

    def test_get_provenance_graph_returns_json_structure(self):
        """Test that get_provenance_graph returns JSON with evidence nodes"""
        import json

        from scimantic.mcp import add_evidence, get_provenance_graph_json

        with tempfile.TemporaryDirectory() as tmpdir:
            project_file = Path(tmpdir) / "project.ttl"

            # Add some evidence to create a graph
            add_evidence(
                content="Finding from paper A.",
                citation="Author A (2023). Title. Journal.",
                source="https://doi.org/10.example/paper-a",
                agent="http://example.org/agent/test",
                project_path=str(project_file),
            )

            add_evidence(
                content="Finding from paper B.",
                citation="Author B (2024). Another title. Conf.",
                source="https://doi.org/10.example/paper-b",
                agent="http://example.org/agent/test",
                project_path=str(project_file),
            )

            # Get graph as JSON
            result = get_provenance_graph_json(str(project_file))
            graph_data = json.loads(result)

            # Verify structure
            assert "evidence" in graph_data
            assert isinstance(graph_data["evidence"], list)
            assert len(graph_data["evidence"]) == 2

            # Verify evidence entries have required fields
            for evidence_entry in graph_data["evidence"]:
                assert "uri" in evidence_entry
                assert "content" in evidence_entry
                assert "citation" in evidence_entry
                assert "source" in evidence_entry
                assert "timestamp" in evidence_entry
                assert "agent" in evidence_entry

    def test_get_provenance_graph_empty_file(self):
        """Test get_provenance_graph with non-existent file returns empty structure"""
        import json

        from scimantic.mcp import get_provenance_graph_json

        with tempfile.TemporaryDirectory() as tmpdir:
            project_file = Path(tmpdir) / "nonexistent.ttl"

            # Should return empty structure, not error
            result = get_provenance_graph_json(str(project_file))
            graph_data = json.loads(result)

            assert "evidence" in graph_data
            assert graph_data["evidence"] == []

    def test_get_provenance_graph_preserves_metadata(self):
        """Test that JSON includes all metadata needed for VS Code tree view"""
        import json
        from datetime import datetime

        from scimantic.mcp import add_evidence, get_provenance_graph_json

        with tempfile.TemporaryDirectory() as tmpdir:
            project_file = Path(tmpdir) / "project.ttl"

            # Add evidence
            add_evidence(
                content="Specific finding about MQDO method.",
                citation="Smith et al. (2023). MQDO Analysis. J. Chem. Phys.",
                source="https://doi.org/10.1063/example",
                agent="http://example.org/agent/claude",
                project_path=str(project_file),
            )

            # Get graph
            result = get_provenance_graph_json(str(project_file))
            graph_data = json.loads(result)

            evidence = graph_data["evidence"][0]

            # Verify citation (for tree view label)
            assert "Smith et al." in evidence["citation"]

            # Verify timestamp exists and is valid ISO format
            timestamp = evidence["timestamp"]
            datetime.fromisoformat(timestamp.replace("Z", "+00:00"))  # Should not raise

            # Verify source is a valid URL
            assert evidence["source"].startswith("https://doi.org/")
