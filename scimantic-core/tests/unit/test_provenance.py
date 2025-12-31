from rdflib import RDF, Literal
from rdflib.namespace import PROV, RDFS

from scimantic.provenance import provenance_tracker


def test_activity_decorator():
    """Test that the activity decorator captures execution."""

    @provenance_tracker.activity(name="test_calculation")
    def calculate_sum(a, b):
        return a + b

    result = calculate_sum(5, 3)
    assert result == 8

    # Check RDF Graph
    g = provenance_tracker.graph

    # Needs 1 activity
    activities = list(g.subjects(RDF.type, PROV.Activity))
    assert len(activities) == 1

    activity = activities[0]

    # Check Label
    assert (activity, RDFS.label, Literal("test_calculation")) in g

    # Check Start/End time existence
    assert (activity, PROV.startedAtTime, None) in g
    assert (activity, PROV.endedAtTime, None) in g


def test_export_turtle():
    """Test that we can export valid turtle."""
    ttl = provenance_tracker.export_turtle()
    assert "@prefix prov: <http://www.w3.org/ns/prov#> ." in ttl
