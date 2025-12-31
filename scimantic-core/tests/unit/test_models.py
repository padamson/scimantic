"""
Unit tests for scimantic LinkML models (Evidence, Question, Hypothesis, etc.)

Tests model creation and validation. RDF URI assignment is handled separately
during RDF graph serialization, not in the Python model layer.
"""

import pytest


class TestEvidenceModel:
    """Tests for Evidence model"""

    def test_create_evidence_minimal(self):
        """Test creating Evidence with only required field (label)"""
        from scimantic.models import Evidence

        # Only label is required
        evidence = Evidence(label="Test evidence label")

        assert evidence is not None
        assert evidence.label == "Test evidence label"
        assert evidence.content is None
        assert evidence.citation is None

    def test_create_evidence_complete(self):
        """Test creating Evidence with all common fields"""
        from scimantic.models import Evidence, Agent

        evidence = Evidence(
            label="Nanopublications are the smallest unit...",
            content="Nanopublications are the smallest unit of publishable information.",
            citation="Kuhn, T., et al. (2016). Decentralized provenance-aware publishing.",
            source="https://doi.org/10.7717/peerj-cs.78",
            wasAttributedTo="http://example.org/agent/claude",
        )

        assert evidence.label == "Nanopublications are the smallest unit..."
        assert (
            evidence.content
            == "Nanopublications are the smallest unit of publishable information."
        )
        assert (
            evidence.citation
            == "Kuhn, T., et al. (2016). Decentralized provenance-aware publishing."
        )
        assert evidence.source == "https://doi.org/10.7717/peerj-cs.78"
        # LinkML auto-converts wasAttributedTo string to Agent object based on schema type
        assert isinstance(evidence.wasAttributedTo, Agent)
        assert evidence.wasAttributedTo is not None

    def test_evidence_validates_required_fields(self):
        """Test that Evidence requires label field"""
        from scimantic.models import Evidence

        # Should raise error if missing required label field
        with pytest.raises(ValueError, match="label"):
            Evidence()  # No arguments - missing required label


class TestQuestionModel:
    """Tests for Question model"""

    def test_create_question_minimal(self):
        """Test creating Question with only required field (label)"""
        from scimantic.models import Question

        question = Question(label="Can DCS be computed using MQDO?")

        assert question is not None
        assert question.label == "Can DCS be computed using MQDO?"
        assert question.wasAttributedTo is None

    def test_create_question_with_agent(self):
        """Test creating Question with agent attribution"""
        from scimantic.models import Question, Agent

        question = Question(
            label="Can DCS be computed using MQDO?",
            wasAttributedTo="http://example.org/agent/researcher",
        )

        assert question.label == "Can DCS be computed using MQDO?"
        # LinkML auto-converts wasAttributedTo string to Agent object based on schema type
        assert isinstance(question.wasAttributedTo, Agent)
        assert question.wasAttributedTo is not None
