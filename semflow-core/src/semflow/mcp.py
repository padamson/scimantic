from mcp.server.fastmcp import FastMCP
from semflow.provenance import provenance_tracker
from semflow.models import Evidence
from rdflib import Graph
from pathlib import Path
from typing import Dict, Any
import uuid

# Initialize the MCP Server
mcp = FastMCP("SemFlow Framework")


@mcp.tool()
def get_provenance_graph() -> str:
    """Returns the current provenance graph in Turtle format."""
    return provenance_tracker.export_turtle()


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
    project_path: str = "project.ttl",
) -> Dict[str, Any]:
    """
    Add evidence from literature to the knowledge graph.

    Creates an Evidence entity following semflow-core/ontology/semflow.ttl
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
