from datetime import datetime
import uuid
from functools import wraps
from rdflib import Graph, Literal, RDF, Namespace
from rdflib.namespace import PROV, XSD, RDFS

SEMFLOW = Namespace("http://padamson.github.io/semflow/")


class SemProvenance:
    def __init__(self):
        self.graph = Graph()
        self.graph.bind("prov", PROV)
        self.graph.bind("semflow", SEMFLOW)

    def activity(self, name=None):
        """Decorator to track function execution as a PROV Activity."""

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                activity_id = SEMFLOW[f"activity/{uuid.uuid4()}"]
                start_time = datetime.now()

                # Record Activity Start
                self.graph.add((activity_id, RDF.type, PROV.Activity))
                self.graph.add(
                    (
                        activity_id,
                        PROV.startedAtTime,
                        Literal(start_time, datatype=XSD.dateTime),
                    )
                )
                label = name or func.__name__
                self.graph.add((activity_id, RDFS.label, Literal(label)))

                # TODO: Record Input Entities (arguments)

                try:
                    result = func(*args, **kwargs)

                    # TODO: Record Output Entities (result)

                    return result
                finally:
                    end_time = datetime.now()
                    self.graph.add(
                        (
                            activity_id,
                            PROV.endedAtTime,
                            Literal(end_time, datatype=XSD.dateTime),
                        )
                    )

            return wrapper

        return decorator

    def export_turtle(self):
        return self.graph.serialize(format="turtle")


# Global Instance
provenance_tracker = SemProvenance()
