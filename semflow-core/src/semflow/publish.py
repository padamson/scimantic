import nanopub
from typing import Union
from rdflib import Graph, Literal, URIRef


class NanopubClient:
    def __init__(self, profile_name=None):
        self.profile = (
            nanopub.profile.load_profile(profile_name) if profile_name else None
        )

    def mint_assertion(
        self, subject: str, predicate: str, object_value: Union[str, float, int]
    ) -> str:
        """
        Mints a single triple assertion as a Nanopublication.
        """
        assertion = Graph()

        # Convert simplistic primitives to Literals/URIs
        s = URIRef(subject)
        p = URIRef(predicate)
        o: Union[Literal, URIRef]
        if isinstance(object_value, (str, float, int)):
            o = Literal(object_value)
        else:
            o = URIRef(str(object_value))

        assertion.add((s, p, o))

        # Create Nanopub - profile parameter not supported in current nanopub library
        # TODO: Implement actual nanopub creation and publishing
        # _np = Nanopub(assertion=assertion)
        # _np.publish()  <-- This would actually publish to the network

        # For now we return a placeholder URI
        return "http://purl.org/np/placeholder"
