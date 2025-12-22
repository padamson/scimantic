"""
SemFlow models for scientific research entities.

Implements Evidence, Hypothesis, Design, and other research artifacts
as Python classes that serialize to RDF following the SemFlow ontology
(semflow-core/ontology/semflow.ttl) built on W3C PROV-O.
"""

from datetime import datetime, timezone
from typing import Optional
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, DCTERMS, XSD

# Define namespaces
SEMFLOW = Namespace("http://semflow.io/ontology#")
PROV = Namespace("http://www.w3.org/ns/prov#")


class Evidence:
    """
    Evidence from scientific literature.

    Represents a finding, claim, or insight extracted from a publication.
    Serializes to RDF as both semflow:Evidence and prov:Entity to enable
    provenance tracking through the research workflow.

    Schema: semflow-core/ontology/semflow.ttl
    """

    def __init__(
        self,
        uri: str,
        content: str,
        citation: str,
        source: str,
        agent: str,
        timestamp: Optional[datetime] = None,
    ):
        """
        Create an Evidence instance.

        Args:
            uri: Unique URI for this evidence (e.g., http://example.org/evidence/001)
            content: Textual summary of the finding extracted from the source
            citation: Formatted bibliographic citation
            source: DOI or URL of the source publication
            agent: URI of the agent (human or AI) who captured this evidence
            timestamp: When evidence was captured (defaults to now)
        """
        if not uri:
            raise ValueError("uri is required")
        if not content:
            raise ValueError("content is required")
        if not citation:
            raise ValueError("citation is required")
        if not source:
            raise ValueError("source is required")
        if not agent:
            raise ValueError("agent is required")

        self.uri = uri
        self.content = content
        self.citation = citation
        self.source = source
        self.agent = agent
        self.timestamp = timestamp or datetime.now(timezone.utc)

    def to_rdf(self) -> Graph:
        """
        Serialize Evidence to RDF graph following PROV-O and SemFlow ontology.

        Returns RDF graph with:
        - Dual typing: semflow:Evidence and prov:Entity
        - semflow:content for the extracted finding
        - dcterms:bibliographicCitation for formatted citation
        - dcterms:source for DOI/URL
        - prov:wasAttributedTo for agent attribution
        - prov:generatedAtTime for temporal provenance

        Returns:
            RDFLib Graph containing the Evidence triples
        """
        g = Graph()

        # Bind prefixes for readable output
        g.bind("semflow", SEMFLOW)
        g.bind("prov", PROV)
        g.bind("dcterms", DCTERMS)

        evidence_uri = URIRef(self.uri)
        agent_uri = URIRef(self.agent)
        source_uri = URIRef(self.source)

        # Dual typing: semflow:Evidence AND prov:Entity
        g.add((evidence_uri, RDF.type, SEMFLOW.Evidence))
        g.add((evidence_uri, RDF.type, PROV.Entity))

        # Content (SemFlow-specific property)
        g.add((evidence_uri, SEMFLOW.content, Literal(self.content)))

        # Citation (Dublin Core)
        g.add((evidence_uri, DCTERMS.bibliographicCitation, Literal(self.citation)))

        # Source (Dublin Core)
        g.add((evidence_uri, DCTERMS.source, source_uri))

        # Attribution (PROV-O)
        g.add((evidence_uri, PROV.wasAttributedTo, agent_uri))

        # Timestamp (PROV-O)
        timestamp_literal = Literal(
            self.timestamp.isoformat().replace("+00:00", "Z"), datatype=XSD.dateTime
        )
        g.add((evidence_uri, PROV.generatedAtTime, timestamp_literal))

        return g
