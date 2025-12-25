import json
import uuid
from pathlib import Path
from typing import Any, Dict, cast

from mcp.server.fastmcp import FastMCP
from rdflib import Graph, Namespace
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
        PREFIX scimantic: <http://scimantic.io/ontology#>
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
    ]


def add_evidence(
    content: str,
    citation: str,
    source: str,
    agent: str,
    project_path: str = DEFAULT_PROJECT_FILE,
) -> Dict[str, Any]:
    """
    Add evidence from literature to the knowledge graph.

    Creates an Evidence entity following scimantic-core/ontology/scimantic.ttl
    and persists it to project.ttl in Turtle format. Multiple calls accumulate
    evidence in the same graph.

    Args:
        content: Summary of the finding extracted from the source paper
        citation: Formatted bibliographic citation
        source: DOI or URL of the source publication
        agent: URI of the agent (human or AI) capturing this evidence
        project_path: Path to project.ttl file (default: "project.ttl")

    Returns:
        Dictionary with status and evidence URI
    """
    # Generate unique URI for this evidence
    evidence_id = str(uuid.uuid4())[:8]
    evidence_uri = f"http://example.org/research/evidence/{evidence_id}"

    # Create Evidence instance
    evidence = Evidence(
        uri=evidence_uri, content=content, citation=citation, source=source, agent=agent
    )

    # Convert to RDF
    evidence_graph = evidence.to_rdf()

    # Load existing graph or create new one
    project_file = Path(project_path)
    if project_file.exists():
        # Load existing graph
        g = Graph()
        g.parse(str(project_file), format="turtle")
        # Merge with new evidence
        g += evidence_graph
    else:
        # Use new evidence graph
        g = evidence_graph

    # Save back to file
    project_file.parent.mkdir(parents=True, exist_ok=True)
    g.serialize(destination=str(project_file), format="turtle")

    return {
        "status": "success",
        "uri": evidence_uri,
        "message": f"Evidence added to {project_path}",
    }


if __name__ == "__main__":
    mcp.run()
