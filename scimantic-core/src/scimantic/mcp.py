import json
import uuid
from pathlib import Path
from typing import Any, Dict, cast

from datetime import datetime, timezone

from mcp.server.fastmcp import FastMCP
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, DCTERMS, XSD
from rdflib.query import ResultRow

from scimantic.config import (
    DEFAULT_PROJECT_FILE,
    PROV_ONTOLOGY_URI,
    SCIMANTIC_ONTOLOGY_URI,
)
from scimantic.models import Evidence
from scimantic.provenance import provenance_tracker

# Initialize the MCP Server
mcp = FastMCP("Scimantic Framework")

# RDF Namespaces
SCIMANTIC = Namespace(SCIMANTIC_ONTOLOGY_URI)
PROV = Namespace(PROV_ONTOLOGY_URI)


@mcp.tool()
def get_provenance_graph() -> str:
    """Returns the current provenance graph in Turtle format."""
    return provenance_tracker.export_turtle()


def get_provenance_graph_json(project_path: str = DEFAULT_PROJECT_FILE) -> str:
    """
    Returns the provenance graph as JSON for VS Code extension consumption.

    Queries the RDF graph for all Evidence entities and returns them as JSON
    with the structure needed for tree view rendering.

    Args:
        project_path: Path to project.ttl file (default: "project.ttl")

    Returns:
        JSON string with structure: {"evidence": [{uri, content, citation, source, timestamp, agent}, ...]}
    """
    project_file = Path(project_path)

    # Handle non-existent file
    if not project_file.exists():
        return json.dumps({"evidence": []})

    # Load RDF graph
    g = Graph()
    g.parse(str(project_file), format="turtle")

    # Query for all Evidence entities
    evidence_list = []
    query = """
        PREFIX scimantic: <http://scimantic.io/>
        PREFIX prov: <http://www.w3.org/ns/prov#>
        PREFIX dcterms: <http://purl.org/dc/terms/>

        SELECT ?uri ?content ?citation ?source ?timestamp ?agent
        WHERE {
            ?uri a scimantic:Evidence .
            ?uri scimantic:content ?content .
            ?uri dcterms:bibliographicCitation ?citation .
            ?uri dcterms:source ?source .
            ?uri prov:generatedAtTime ?timestamp .
            ?uri prov:wasAttributedTo ?agent .
        }
        ORDER BY DESC(?timestamp)
    """

    results = g.query(query)

    for row in results:
        # Cast to ResultRow to ensure we access attributes safely
        r = cast(ResultRow, row)
        evidence_list.append(
            {
                "uri": str(r.uri),
                "content": str(r.content),
                "citation": str(r.citation),
                "source": str(r.source),
                "timestamp": str(r.timestamp),
                "agent": str(r.agent),
            }
        )

    return json.dumps({"evidence": evidence_list})


@mcp.tool()
def mint_hypothesis(statement: str, evidence_uris: list[str] = []) -> str:
    """
    Creates a new Hypothesis Nanopublication.

    Args:
        statement: The scientific hypothesis text.
        evidence_uris: List of URIs (e.g., from literature) supporting this hypothesis.
    """
    # Logic to create a Nanopub would go here
    # For now, we mock it and return a placeholder URI
    hypothesis_uri = f"http://padamson.github.io/nanopubs/hypothesis/{statement[:10].replace(' ', '_')}"
    return f"Minted Hypothesis: {hypothesis_uri}"


@mcp.tool()
def mint_design(parameters: dict, methodology: str) -> str:
    """
    Creates a Study Design Nanopublication.

    Args:
        parameters: Key-value pairs of experimental parameters (e.g. basis_set: 'cc-pVQZ')
        methodology: Description of the method (e.g. 'GAMESS MRCI')
    """
    return "Minted Design: http://padamson.github.io/nanopubs/design/123"


def get_tools() -> list[Dict[str, Any]]:
    """
    Return list of registered MCP tools.

    For testing purposes, returns tool metadata.
    """
    return [
        {"name": "get_provenance_graph"},
        {"name": "mint_hypothesis"},
        {"name": "mint_design"},
        {"name": "add_evidence"},
        {"name": "add_question"},
    ]


def _persist_graph(graph: Graph, project_path: str = DEFAULT_PROJECT_FILE):
    """Helper to persist RDF graph to disk."""
    project_file = Path(project_path)
    if project_file.exists():
        existing_g = Graph()
        existing_g.parse(str(project_file), format="turtle")
        existing_g += graph
        graph = existing_g

    project_file.parent.mkdir(parents=True, exist_ok=True)
    graph.serialize(destination=str(project_file), format="turtle")


def add_evidence(
    content: str,
    citation: str,
    source: str,
    agent: str,
    project_path: str = DEFAULT_PROJECT_FILE,
) -> Dict[str, Any]:
    """
    Add evidence from literature to the knowledge graph.
    """
    # TODO: Replace with LinkML rdf_dumper once schema packaging and context generation are fully automated.
    # Currently using manual RDF construction for stability.

    # Generate unique URI for this evidence
    evidence_id = str(uuid.uuid4())[:8]
    evidence_uri = f"http://example.org/research/evidence/{evidence_id}"

    # Create Evidence instance (note: id field)
    # Generate a label from content if not provided (assume full content for now, or truncated)
    label = content[:50] + "..." if len(content) > 50 else content

    evidence = Evidence(
        id=evidence_uri,
        label=label,
        content=content,
        citation=citation,
        source=source,
        wasAttributedTo=agent,
    )

    g = Graph()
    g.bind("scimantic", SCIMANTIC)
    g.bind("prov", PROV)

    evidence_node = URIRef(evidence.id)
    g.add((evidence_node, RDF.type, SCIMANTIC.Evidence))
    g.add((evidence_node, RDF.type, PROV.Entity))
    g.add((evidence_node, SCIMANTIC.id, Literal(evidence.id)))
    g.add((evidence_node, SCIMANTIC.content, Literal(evidence.content)))  # type: ignore
    g.add((evidence_node, DCTERMS.bibliographicCitation, Literal(evidence.citation)))  # type: ignore
    g.add((evidence_node, DCTERMS.source, Literal(evidence.source)))  # type: ignore

    agent_node = URIRef(evidence.wasAttributedTo)  # type: ignore
    g.add((evidence_node, PROV.wasAttributedTo, agent_node))  # type: ignore
    g.add((agent_node, RDF.type, PROV.Agent))
    g.add((agent_node, SCIMANTIC.id, Literal(evidence.wasAttributedTo)))  # type: ignore

    # Add timestamp
    timestamp = datetime.now(timezone.utc)
    g.add(
        (evidence_node, PROV.generatedAtTime, Literal(timestamp, datatype=XSD.dateTime))
    )

    _persist_graph(g, project_path)

    return {
        "status": "success",
        "uri": evidence_uri,
        "message": f"Evidence added to {project_path}",
    }


def add_question(
    label: str,
    agent: str,
    project_path: str = DEFAULT_PROJECT_FILE,
) -> Dict[str, Any]:
    """
    Add a research question to the knowledge graph.
    """
    from scimantic.models import Question

    # Generate unique URI
    unique_id = str(uuid.uuid4())[:8]
    question_uri = f"http://example.org/research/question/{unique_id}"

    # Create model
    question = Question(id=question_uri, label=label, wasAttributedTo=agent)

    # Manual RDF (Temporary)
    g = Graph()
    g.bind("scimantic", SCIMANTIC)
    g.bind("prov", PROV)

    q_node = URIRef(question.id)
    g.add((q_node, RDF.type, SCIMANTIC.Question))
    g.add((q_node, SCIMANTIC.id, Literal(question.id)))
    g.add((q_node, RDFS.label, Literal(question.label)))
    if question.wasAttributedTo:
        agent_node = URIRef(question.wasAttributedTo)
        g.add((q_node, PROV.wasAttributedTo, agent_node))
        g.add((agent_node, RDF.type, PROV.Agent))
        g.add((agent_node, SCIMANTIC.id, Literal(question.wasAttributedTo)))

    # Create associated Activity (QuestionFormation)
    # Note: The model doesn't enforce this creation automatically, business logic does.
    activity_uri = URIRef(f"{question_uri}/generation")
    g.add((activity_uri, RDF.type, SCIMANTIC.QuestionFormation))
    g.add((activity_uri, SCIMANTIC.id, Literal(str(activity_uri))))
    g.add((q_node, PROV.wasGeneratedBy, activity_uri))

    _persist_graph(g, project_path)

    return {
        "status": "success",
        "uri": question_uri,
        "message": f"Question added to {project_path}",
    }


if __name__ == "__main__":
    mcp.run()
