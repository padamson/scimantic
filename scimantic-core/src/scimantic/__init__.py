"""
Scimantic: Semantic Research Orchestration Framework

A framework for conducting machine-readable scientific research from
literature review through publication, built on W3C PROV-O and nanopublications.
"""

__version__ = "0.1.0"

# Export main classes for convenient imports
from scimantic.models import (
    Question,
    QuestionFormation,
    LiteratureSearch,
    Evidence,
    Hypothesis,
    ExperimentalMethod,
    Dataset,
    Result,
    Analysis,
    Agent,
)

__all__ = [
    "Question",
    "QuestionFormation",
    "LiteratureSearch",
    "Evidence",
    "Hypothesis",
    "ExperimentalMethod",
    "Dataset",
    "Result",
    "Analysis",
    "Agent",
]
