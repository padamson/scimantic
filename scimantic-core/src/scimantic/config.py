"""
Scimantic configuration constants.

Centralized location for namespace URIs and other configuration values.
"""

# RDF Namespace URIs
# When scimantic.io domain is acquired, update SCIMANTIC_ONTOLOGY_URI
# Alternative: Use GitHub Pages at http://padamson.github.io/scimantic/ontology#
SCIMANTIC_ONTOLOGY_URI = "http://scimantic.io/ontology#"
PROV_ONTOLOGY_URI = "http://www.w3.org/ns/prov#"
DCTERMS_URI = "http://purl.org/dc/terms/"
FOAF_URI = "http://xmlns.com/foaf/0.1/"

# Default file paths
DEFAULT_PROJECT_FILE = "project.ttl"
DEFAULT_ONTOLOGY_FILE = "ontology/scimantic.ttl"

# Agent URIs
DEFAULT_AGENT_URI_PREFIX = "http://example.org/agent/"
