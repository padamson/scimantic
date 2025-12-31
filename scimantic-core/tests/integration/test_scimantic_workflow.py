import pytest
import tempfile
from pathlib import Path
from rdflib import Graph, Namespace, URIRef

SCIMANTIC = Namespace("http://scimantic.io/")
PROV = Namespace("http://www.w3.org/ns/prov#")


class TestAgentWorkflowRegression:
    """
    Regression tests for "Human-AI Teaming" workflows.
    Simulates the sequence of tool calls an agent makes to ensure ontology consistency.
    """

    def test_agent_question_evidence_workflow(self):
        """
        Scenario: Agent helps user formulate a question, then finds evidence for it.
        1. Agent calls add_question()
        2. Agent calls add_evidence() referencing that question
        """
        from scimantic.mcp import add_question, add_evidence

        with tempfile.TemporaryDirectory() as tmpdir:
            project_file = Path(tmpdir) / "project.ttl"
            agent_uri = "http://example.org/agent/claude-3-5-sonnet"

            # 1. Agent creates question (Refined based on "Common Enzyme" scenario)
            q_result = add_question(
                label="Does Donepezil inhibit Acetylcholinesterase?",
                agent=agent_uri,
                project_path=str(project_file),
            )
            question_uri = q_result["uri"]

            # 2. Agent adds evidence linked to question
            # Note: The add_evidence signature in mcp.py currently doesn't support 'wasDerivedFrom' or 'questions' directly in arguments
            # We will need to update add_evidence to support linking to a question!
            # For this expectation to pass, the tool must change.

            # This call is expected to FAIL or need updating once we implement the linking capability.
            # For now, we simulate the agent trying to pass this context.
            # If the tool signature doesn't support it, this test acts as a spec for the required change.

            # Currently add_evidence signature is:
            # def add_evidence(content, citation, source, agent, project_path)

            # We want:
            # def add_evidence(..., relates_to_question=None)

            try:
                e_result = add_evidence(
                    content="Donepezil creates a non-covalent, reversible inhibition of Acetylcholinesterase with an IC50 of 5.7 nM.",
                    citation="Sugimoto et al. (2000)",
                    source="https://doi.org/10.example/ache-inhibition",
                    agent=agent_uri,
                    project_path=str(project_file),
                    # HYPOTHETICAL ARGUMENT - expected to crash until implemented
                    relates_to_question=question_uri,
                )
            except TypeError:
                pytest.fail(
                    "add_evidence() does not yet support linking to a question (relates_to_question argument missing)"
                )

            # Verify Graph Structure
            g = Graph()
            g.parse(str(project_file), format="turtle")

            ev_node = URIRef(e_result["uri"])
            q_node = URIRef(question_uri)

            # Check for prov:wasDerivedFrom relationship (or scimantic equivalent)
            assert (ev_node, PROV.wasDerivedFrom, q_node) in g, (
                "Evidence should be derived from the Question"
            )
