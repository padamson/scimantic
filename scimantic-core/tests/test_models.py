"""
Unit tests for scimantic models (Evidence, Hypothesis, etc.)

Tests that model creation, validation, and RDF serialization work correctly.
"""

import pytest
from rdflib import Namespace

# Scimantic namespaces
SCIMANTIC = Namespace("http://scimantic.io/")
PROV = Namespace("http://www.w3.org/ns/prov#")


class TestEvidenceModel:
    """Tests for Evidence model following scimantic-core/ontology/scimantic.ttl"""

    def test_create_evidence(self):
        """Test creating an Evidence instance with required fields"""
        from scimantic.models import Evidence

        # Create evidence with minimal required fields
        evidence = Evidence(
            id="http://example.org/research/scimantic-paper/evidence/001",
            content="Nanopublications are the smallest unit of publishable information.",
            citation="Kuhn, T., et al. (2016). Decentralized provenance-aware publishing.",
            source="https://doi.org/10.7717/peerj-cs.78",
            wasAttributedTo="http://example.org/agent/claude",
            label="Nanopublications are the smallest unit...",
        )

        # Verify instance was created
        assert evidence is not None
        assert evidence.id == "http://example.org/research/scimantic-paper/evidence/001"
        assert (
            evidence.content
            == "Nanopublications are the smallest unit of publishable information."
        )
        assert (
            evidence.citation
            == "Kuhn, T., et al. (2016). Decentralized provenance-aware publishing."
        )
        assert evidence.source == "https://doi.org/10.7717/peerj-cs.78"
        assert evidence.wasAttributedTo == "http://example.org/agent/claude"

    def test_evidence_validates_required_fields(self):
        """Test that Evidence requires all mandatory fields"""
        from scimantic.models import Evidence

        # Should raise error if missing required fields
        with pytest.raises((TypeError, ValueError)):
            Evidence()  # No arguments

        with pytest.raises((TypeError, ValueError)):
            Evidence(
                id="http://example.org/evidence/001"
            )  # Missing content (if required)
            # Note: LinkML default is optional unless required: true.
            # If generated code marks them as Optional, this test might need adjustment.
