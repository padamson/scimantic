"""
Integration test for Evidence workflow: MCP → RDF → SPARQL

Tests the complete flow from AI agent adding evidence via MCP tool
through RDF persistence to SPARQL queries, validating the acceptance
criteria from docs/features/ai-assisted-literature-search.md Slice 1.
"""

import tempfile
from pathlib import Path

from rdflib import Graph, Namespace

SCIMANTIC = Namespace("http://scimantic.io/ontology#")
PROV = Namespace("http://www.w3.org/ns/prov#")
DCTERMS = Namespace("http://purl.org/dc/terms/")


class TestEvidenceWorkflow:
    """Integration test for complete evidence capture workflow"""

    def test_end_to_end_evidence_workflow(self):
        """
        Test complete workflow: add evidence → persist RDF → query with SPARQL

        This validates Slice 1 acceptance criteria:
        - AI agent can add evidence via MCP tool ✓
        - Evidence persisted to project.ttl in Turtle format ✓
        - Multiple evidence entries accumulate ✓
        - Evidence has correct RDF structure (dual typing, properties) ✓
        - Provenance captured (agent attribution, timestamp) ✓
        - SPARQL queries work ✓
        """
        from scimantic.mcp import add_evidence

        with tempfile.TemporaryDirectory() as tmpdir:
            project_file = Path(tmpdir) / "project.ttl"

            # Simulate AI agent adding evidence from Kuhn et al. 2016 nanopub paper
            result = add_evidence(
                content="Nanopublications are the smallest unit of publishable information: an assertion with provenance and publication metadata.",
                citation="Kuhn, T., et al. (2016). Decentralized provenance-aware publishing with nanopublications. PeerJ Computer Science 2:e78.",
                source="https://doi.org/10.7717/peerj-cs.78",
                agent="http://example.org/agent/claude",
                project_path=str(project_file),
            )

            assert result["status"] == "success"
            evidence_uri = result["uri"]

            # Verify file was created in Turtle format
            assert project_file.exists()
            content = project_file.read_text()
            assert "@prefix" in content  # Turtle format uses prefixes

            # Load graph for SPARQL queries
            g = Graph()
            g.parse(str(project_file), format="turtle")

            # --- ACCEPTANCE CRITERION: Evidence has dual typing ---
            query = f"""
                PREFIX scimantic: <http://scimantic.io/ontology#>
                PREFIX prov: <http://www.w3.org/ns/prov#>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

                ASK {{
                    <{evidence_uri}> rdf:type scimantic:Evidence ;
                                      rdf:type prov:Entity .
                }}
            """
            assert g.query(query).askAnswer is True

            # --- ACCEPTANCE CRITERION: Find evidence added by specific agent ---
            query = """
                PREFIX scimantic: <http://scimantic.io/ontology#>
                PREFIX prov: <http://www.w3.org/ns/prov#>
                PREFIX dcterms: <http://purl.org/dc/terms/>

                SELECT ?evidence ?citation WHERE {
                    ?evidence a scimantic:Evidence ;
                              dcterms:bibliographicCitation ?citation ;
                              prov:wasAttributedTo ?agent .
                    FILTER(CONTAINS(STR(?agent), "claude"))
                }
            """
            results = list(g.query(query))
            assert len(results) == 1
            assert "Kuhn" in str(results[0][1])

            # --- ACCEPTANCE CRITERION: Count total evidence entries ---
            query = """
                PREFIX scimantic: <http://scimantic.io/ontology#>

                SELECT (COUNT(?evidence) as ?count) WHERE {
                    ?evidence a scimantic:Evidence .
                }
            """
            results = list(g.query(query))
            count = int(results[0][0])
            assert count == 1

            # --- ACCEPTANCE CRITERION: Find recent evidence (temporal query) ---
            # Add second evidence entry to test multiple entries
            add_evidence(
                content="Another finding from a different paper.",
                citation="Author B (2025).",
                source="https://doi.org/10.example/12345",
                agent="http://example.org/agent/human",
                project_path=str(project_file),
            )

            # Reload graph after second addition
            g = Graph()
            g.parse(str(project_file), format="turtle")

            query = """
                PREFIX scimantic: <http://scimantic.io/ontology#>
                PREFIX prov: <http://www.w3.org/ns/prov#>
                PREFIX dcterms: <http://purl.org/dc/terms/>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

                SELECT ?evidence ?citation ?timestamp WHERE {
                    ?evidence a scimantic:Evidence, prov:Entity ;
                              dcterms:bibliographicCitation ?citation ;
                              prov:generatedAtTime ?timestamp .
                    FILTER(?timestamp > "2025-01-01T00:00:00Z"^^xsd:dateTime)
                }
                ORDER BY DESC(?timestamp)
            """
            results = list(g.query(query))
            assert len(results) == 2  # Both are recent

            # --- ACCEPTANCE CRITERION: Multiple evidence entries coexist ---
            query = """
                PREFIX scimantic: <http://scimantic.io/ontology#>

                SELECT (COUNT(?evidence) as ?count) WHERE {
                    ?evidence a scimantic:Evidence .
                }
            """
            results = list(g.query(query))
            count = int(results[0][0])
            assert count == 2  # Two evidence entries exist

    def test_sparql_queries_from_feature_doc(self):
        """
        Test exact SPARQL queries from feature documentation work.

        Validates queries from docs/features/ai-assisted-literature-search.md
        """
        from scimantic.mcp import add_evidence

        with tempfile.TemporaryDirectory() as tmpdir:
            project_file = Path(tmpdir) / "project.ttl"

            # Add evidence
            add_evidence(
                content="Test evidence content.",
                citation="Test citation.",
                source="https://doi.org/10.example/test",
                agent="http://example.org/agent/claude",
                project_path=str(project_file),
            )

            g = Graph()
            g.parse(str(project_file), format="turtle")

            # Query from feature doc: Find evidence by agent
            query = """
                PREFIX scimantic: <http://scimantic.io/ontology#>
                PREFIX prov: <http://www.w3.org/ns/prov#>

                SELECT ?evidence ?citation WHERE {
                    ?evidence a scimantic:Evidence ;
                              dcterms:bibliographicCitation ?citation ;
                              prov:wasAttributedTo ?agent .
                    FILTER(CONTAINS(STR(?agent), "claude"))
                }
            """

            # Add DCTERMS namespace for query to work
            from rdflib.namespace import DCTERMS as DC

            results = list(g.query(query, initNs={"dcterms": DC}))
            assert len(results) >= 1
