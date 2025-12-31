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

    return json.dumps({"evidence": evidence_list, "questions": get_questions_list(g)})


def get_questions_list(g: Graph) -> list[Dict[str, Any]]:
    """Helper to query questions from the graph."""
    questions = []
    query = """
        PREFIX scimantic: <http://scimantic.io/>
        PREFIX prov: <http://www.w3.org/ns/prov#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?uri ?label ?agent
        WHERE {
            ?uri a scimantic:Question .
            ?uri rdfs:label ?label .
            OPTIONAL { ?uri prov:wasAttributedTo ?agent }
        }
    """
    results = g.query(query)
    for row in results:
        r = cast(ResultRow, row)
        questions.append(
            {
                "uri": str(r.uri),
                "label": str(r.label),
                "agent": str(r.agent) if r.agent else None,
            }
        )
    return questions


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


@mcp.tool()
def add_evidence(
    content: str,
    citation: str,
    source: str,
    agent: str,
    project_path: str = DEFAULT_PROJECT_FILE,
    relates_to_question: str | None = None,
) -> Dict[str, Any]:
    """
    Add evidence from literature to the knowledge graph.
    """
    # TODO: Replace with LinkML rdf_dumper once schema packaging and context generation are fully automated.
    # Currently using manual RDF construction for stability.

    # Generate unique URI for this evidence
    evidence_id = str(uuid.uuid4())[:8]
    evidence_uri = f"http://example.org/research/evidence/{evidence_id}"

    # Generate label from content if not provided (truncate for readability)
    label = content[:50] + "..." if len(content) > 50 else content

    # Create Evidence model instance for validation only
    # Note: We use the model just to validate required fields
    _ = Evidence(
        label=label,
        content=content,
        citation=citation,
        source=source,
    )

    # Manually construct RDF graph using raw parameters
    # TODO: Replace with LinkML rdf_dumper once context generation is automated
    g = Graph()
    g.bind("scimantic", SCIMANTIC)
    g.bind("prov", PROV)

    # Create Evidence entity with URI as subject
    evidence_node = URIRef(evidence_uri)
    g.add((evidence_node, RDF.type, SCIMANTIC.Evidence))
    g.add((evidence_node, RDF.type, PROV.Entity))
    g.add((evidence_node, RDFS.label, Literal(label)))
    g.add((evidence_node, SCIMANTIC.content, Literal(content)))
    g.add((evidence_node, DCTERMS.bibliographicCitation, Literal(citation)))
    g.add((evidence_node, DCTERMS.source, Literal(source)))

    # Create Agent entity
    agent_node = URIRef(agent)
    g.add((evidence_node, PROV.wasAttributedTo, agent_node))
    g.add((agent_node, RDF.type, PROV.Agent))

    # Add timestamp
    timestamp = datetime.now(timezone.utc)
    g.add(
        (evidence_node, PROV.generatedAtTime, Literal(timestamp, datatype=XSD.dateTime))
    )

    if relates_to_question:
        question_node = URIRef(relates_to_question)
        g.add((evidence_node, PROV.wasDerivedFrom, question_node))

    _persist_graph(g, project_path)

    return {
        "status": "success",
        "uri": evidence_uri,
        "message": f"Evidence added to {project_path}",
    }


@mcp.tool()
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

    # Create model instance for validation only
    _ = Question(label=label)

    # Manually construct RDF graph using raw parameters
    # TODO: Replace with LinkML rdf_dumper once context generation is automated
    g = Graph()
    g.bind("scimantic", SCIMANTIC)
    g.bind("prov", PROV)

    # Create Question entity with URI as subject
    q_node = URIRef(question_uri)
    g.add((q_node, RDF.type, SCIMANTIC.Question))
    g.add((q_node, RDF.type, PROV.Entity))
    g.add((q_node, RDFS.label, Literal(label)))

    # Create Agent entity if provided
    if agent:
        agent_node = URIRef(agent)
        g.add((q_node, PROV.wasAttributedTo, agent_node))
        g.add((agent_node, RDF.type, PROV.Agent))

    # Create associated QuestionFormation activity
    # Note: The model doesn't enforce this creation automatically, business logic does.
    activity_uri = URIRef(f"{question_uri}/generation")
    g.add((activity_uri, RDF.type, SCIMANTIC.QuestionFormation))
    g.add((activity_uri, RDF.type, PROV.Activity))
    g.add((q_node, PROV.wasGeneratedBy, activity_uri))

    _persist_graph(g, project_path)

    return {
        "status": "success",
        "uri": question_uri,
        "message": f"Question added to {project_path}",
    }


if __name__ == "__main__":
    mcp.run()
