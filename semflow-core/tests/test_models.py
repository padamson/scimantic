"""
Unit tests for semflow models (Evidence, Hypothesis, etc.)

Tests that model creation, validation, and RDF serialization work correctly.
"""

import pytest
from datetime import datetime
from rdflib import Graph, URIRef, Namespace, Literal
from rdflib.namespace import RDF, DCTERMS, XSD

# SemFlow namespaces
SEMFLOW = Namespace("http://semflow.io/ontology#")
PROV = Namespace("http://www.w3.org/ns/prov#")


class TestEvidenceModel:
    """Tests for Evidence model following semflow-core/ontology/semflow.ttl"""

    def test_create_evidence(self):
        """Test creating an Evidence instance with required fields"""
        from semflow.models import Evidence

        # Create evidence with minimal required fields
        evidence = Evidence(
            uri="http://example.org/research/semflow-paper/evidence/001",
            content="Nanopublications are the smallest unit of publishable information.",
            citation="Kuhn, T., et al. (2016). Decentralized provenance-aware publishing.",
            source="https://doi.org/10.7717/peerj-cs.78",
            agent="http://example.org/agent/claude",
        )

        # Verify instance was created
        assert evidence is not None
        assert evidence.uri == "http://example.org/research/semflow-paper/evidence/001"
        assert (
            evidence.content
            == "Nanopublications are the smallest unit of publishable information."
        )
        assert (
            evidence.citation
            == "Kuhn, T., et al. (2016). Decentralized provenance-aware publishing."
        )
        assert evidence.source == "https://doi.org/10.7717/peerj-cs.78"
        assert evidence.agent == "http://example.org/agent/claude"

    def test_evidence_to_rdf(self):
        """Test Evidence serialization to RDF following PROV-O standards"""
        from semflow.models import Evidence

        evidence = Evidence(
            uri="http://example.org/research/semflow-paper/evidence/001",
            content="Nanopublications are the smallest unit of publishable information.",
            citation="Kuhn, T., et al. (2016). Decentralized provenance-aware publishing.",
            source="https://doi.org/10.7717/peerj-cs.78",
            agent="http://example.org/agent/claude",
        )

        # Convert to RDF graph
        graph = evidence.to_rdf()

        # Verify it's a graph
        assert isinstance(graph, Graph)

        # Create URIRefs for verification
        evidence_uri = URIRef(evidence.uri)
        agent_uri = URIRef(evidence.agent)
        source_uri = URIRef(evidence.source)

        # Verify dual typing: semflow:Evidence AND prov:Entity
        types = list(graph.objects(evidence_uri, RDF.type))
        assert SEMFLOW.Evidence in types
        assert PROV.Entity in types

        # Verify semflow:content
        content = graph.value(evidence_uri, SEMFLOW.content)
        assert content == Literal(evidence.content)

        # Verify dcterms:bibliographicCitation
        citation = graph.value(evidence_uri, DCTERMS.bibliographicCitation)
        assert citation == Literal(evidence.citation)

        # Verify dcterms:source
        source = graph.value(evidence_uri, DCTERMS.source)
        assert source == source_uri

        # Verify prov:wasAttributedTo
        attributed_to = graph.value(evidence_uri, PROV.wasAttributedTo)
        assert attributed_to == agent_uri

        # Verify prov:generatedAtTime exists and is a datetime
        generated_at = graph.value(evidence_uri, PROV.generatedAtTime)
        assert generated_at is not None
        assert generated_at.datatype == XSD.dateTime

    def test_evidence_validates_required_fields(self):
        """Test that Evidence requires all mandatory fields"""
        from semflow.models import Evidence

        # Should raise error if missing required fields
        with pytest.raises((TypeError, ValueError)):
            Evidence()  # No arguments

        with pytest.raises((TypeError, ValueError)):
            Evidence(uri="http://example.org/evidence/001")  # Missing content

    def test_evidence_generates_timestamp(self):
        """Test that Evidence automatically generates prov:generatedAtTime"""
        from semflow.models import Evidence
        from datetime import timezone

        before = datetime.now(timezone.utc)

        evidence = Evidence(
            uri="http://example.org/evidence/001",
            content="Test content",
            citation="Test citation",
            source="https://example.org/paper",
            agent="http://example.org/agent/test",
        )

        after = datetime.now(timezone.utc)

        # Verify timestamp attribute exists
        assert evidence.timestamp is not None
        assert isinstance(evidence.timestamp, datetime)

        # Verify timestamp is within the before/after window
        assert before <= evidence.timestamp <= after

        # Convert to RDF and verify timestamp serialization
        graph = evidence.to_rdf()
        evidence_uri = URIRef(evidence.uri)
        generated_at = graph.value(evidence_uri, PROV.generatedAtTime)

        # Verify timestamp was serialized to RDF
        assert generated_at is not None
        assert generated_at.datatype == XSD.dateTime
