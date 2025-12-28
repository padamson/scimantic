# Auto generated from scimantic.yaml by pythongen.py version: 0.0.1
# Generation date: 2025-12-28T12:10:42
# Schema: scimantic
#
# id: http://scimantic.io/schema
# description: A minimal domain ontology for representing the scientific method as provenance chains.
# license: https://creativecommons.org/licenses/by/4.0/

from dataclasses import dataclass
from typing import Any, ClassVar, Optional, Union

from jsonasobj2 import as_dict
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.metamodelcore import empty_list
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str
from rdflib import URIRef

from linkml_runtime.utils.metamodelcore import Bool, XSDDateTime

metamodel_version = "1.7.0"
version = "0.1.1"

# Namespaces
DCTERMS = CurieNamespace("dcterms", "http://purl.org/dc/terms/")
LINKML = CurieNamespace("linkml", "https://w3id.org/linkml/")
PROV = CurieNamespace("prov", "http://www.w3.org/ns/prov#")
RDFS = CurieNamespace("rdfs", "http://www.w3.org/2000/01/rdf-schema#")
SCIMANTIC = CurieNamespace("scimantic", "http://scimantic.io/")
URREF = CurieNamespace(
    "urref", "https://raw.githubusercontent.com/adelphi23/urref/469137/URREF.ttl#"
)
XSD = CurieNamespace("xsd", "http://www.w3.org/2001/XMLSchema#")
DEFAULT_ = SCIMANTIC


# Types


# Class references
class EntityId(extended_str):
    pass


class AgentId(extended_str):
    pass


class QuestionId(EntityId):
    pass


class EvidenceId(EntityId):
    pass


class HypothesisId(EntityId):
    pass


class ExperimentalMethodId(EntityId):
    pass


class DatasetId(EntityId):
    pass


class ResultId(EntityId):
    pass


class ParameterId(EntityId):
    pass


class UncertaintyModelId(EntityId):
    pass


class AmbiguityId(UncertaintyModelId):
    pass


class VaguenessId(UncertaintyModelId):
    pass


class IncompletenessId(UncertaintyModelId):
    pass


class AleatoryId(UncertaintyModelId):
    pass


@dataclass(repr=False)
class Entity(YAMLRoot):
    """
    A provenance entity.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV["Entity"]
    class_class_curie: ClassVar[str] = "prov:Entity"
    class_name: ClassVar[str] = "Entity"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.Entity

    id: Union[str, EntityId] = None
    wasAttributedTo: Optional[Union[str, AgentId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, EntityId):
            self.id = EntityId(self.id)

        if self.wasAttributedTo is not None and not isinstance(
            self.wasAttributedTo, AgentId
        ):
            self.wasAttributedTo = AgentId(self.wasAttributedTo)

        super().__post_init__(**kwargs)


class Activity(YAMLRoot):
    """
    A provenance activity.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV["Activity"]
    class_class_curie: ClassVar[str] = "prov:Activity"
    class_name: ClassVar[str] = "Activity"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.Activity


@dataclass(repr=False)
class Agent(YAMLRoot):
    """
    A provenance agent.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV["Agent"]
    class_class_curie: ClassVar[str] = "prov:Agent"
    class_name: ClassVar[str] = "Agent"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.Agent

    id: Union[str, AgentId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AgentId):
            self.id = AgentId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Question(Entity):
    """
    An interrogative sentence representing the research query.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCIMANTIC["Question"]
    class_class_curie: ClassVar[str] = "scimantic:Question"
    class_name: ClassVar[str] = "Question"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.Question

    id: Union[str, QuestionId] = None
    label: str = None
    wasGeneratedBy: Optional[Union[dict, "QuestionFormation"]] = None
    motivates: Optional[
        Union[Union[dict, "LiteratureSearch"], list[Union[dict, "LiteratureSearch"]]]
    ] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, QuestionId):
            self.id = QuestionId(self.id)

        if self._is_empty(self.label):
            self.MissingRequiredField("label")
        if not isinstance(self.label, str):
            self.label = str(self.label)

        if self.wasGeneratedBy is not None and not isinstance(
            self.wasGeneratedBy, QuestionFormation
        ):
            self.wasGeneratedBy = QuestionFormation(**as_dict(self.wasGeneratedBy))

        if not isinstance(self.motivates, list):
            self.motivates = [self.motivates] if self.motivates is not None else []
        self.motivates = [
            v if isinstance(v, LiteratureSearch) else LiteratureSearch(**as_dict(v))
            for v in self.motivates
        ]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class QuestionFormation(Activity):
    """
    The activity of creating a Research Question.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCIMANTIC["QuestionFormation"]
    class_class_curie: ClassVar[str] = "scimantic:QuestionFormation"
    class_name: ClassVar[str] = "QuestionFormation"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.QuestionFormation

    wasAssociatedWith: Optional[Union[str, AgentId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.wasAssociatedWith is not None and not isinstance(
            self.wasAssociatedWith, AgentId
        ):
            self.wasAssociatedWith = AgentId(self.wasAssociatedWith)

        super().__post_init__(**kwargs)


class LiteratureSearch(Activity):
    """
    The activity of searching for and extracting Evidence.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCIMANTIC["LiteratureSearch"]
    class_class_curie: ClassVar[str] = "scimantic:LiteratureSearch"
    class_name: ClassVar[str] = "LiteratureSearch"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.LiteratureSearch


@dataclass(repr=False)
class Evidence(Entity):
    """
    A factual claim extracted from a source.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCIMANTIC["Evidence"]
    class_class_curie: ClassVar[str] = "scimantic:Evidence"
    class_name: ClassVar[str] = "Evidence"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.Evidence

    id: Union[str, EvidenceId] = None
    label: str = None
    content: Optional[str] = None
    citation: Optional[str] = None
    source: Optional[str] = None
    wasGeneratedBy: Optional[Union[dict, LiteratureSearch]] = None
    accessLevel: Optional[str] = None
    publishable: Optional[Union[bool, Bool]] = None
    supports: Optional[Union[str, HypothesisId]] = None
    contradicts: Optional[Union[str, HypothesisId]] = None
    hasUncertainty: Optional[Union[str, UncertaintyModelId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, EvidenceId):
            self.id = EvidenceId(self.id)

        if self._is_empty(self.label):
            self.MissingRequiredField("label")
        if not isinstance(self.label, str):
            self.label = str(self.label)

        if self.content is not None and not isinstance(self.content, str):
            self.content = str(self.content)

        if self.citation is not None and not isinstance(self.citation, str):
            self.citation = str(self.citation)

        if self.source is not None and not isinstance(self.source, str):
            self.source = str(self.source)

        if self.wasGeneratedBy is not None and not isinstance(
            self.wasGeneratedBy, LiteratureSearch
        ):
            self.wasGeneratedBy = LiteratureSearch()

        if self.accessLevel is not None and not isinstance(self.accessLevel, str):
            self.accessLevel = str(self.accessLevel)

        if self.publishable is not None and not isinstance(self.publishable, Bool):
            self.publishable = Bool(self.publishable)

        if self.supports is not None and not isinstance(self.supports, HypothesisId):
            self.supports = HypothesisId(self.supports)

        if self.contradicts is not None and not isinstance(
            self.contradicts, HypothesisId
        ):
            self.contradicts = HypothesisId(self.contradicts)

        if self.hasUncertainty is not None and not isinstance(
            self.hasUncertainty, UncertaintyModelId
        ):
            self.hasUncertainty = UncertaintyModelId(self.hasUncertainty)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Hypothesis(Entity):
    """
    A testable claim derived from evidence.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCIMANTIC["Hypothesis"]
    class_class_curie: ClassVar[str] = "scimantic:Hypothesis"
    class_name: ClassVar[str] = "Hypothesis"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.Hypothesis

    id: Union[str, HypothesisId] = None
    label: str = None
    wasGeneratedBy: Optional[Union[dict, "HypothesisFormation"]] = None
    wasDerivedFrom: Optional[
        Union[Union[str, EvidenceId], list[Union[str, EvidenceId]]]
    ] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, HypothesisId):
            self.id = HypothesisId(self.id)

        if self._is_empty(self.label):
            self.MissingRequiredField("label")
        if not isinstance(self.label, str):
            self.label = str(self.label)

        if self.wasGeneratedBy is not None and not isinstance(
            self.wasGeneratedBy, HypothesisFormation
        ):
            self.wasGeneratedBy = HypothesisFormation(**as_dict(self.wasGeneratedBy))

        if not isinstance(self.wasDerivedFrom, list):
            self.wasDerivedFrom = (
                [self.wasDerivedFrom] if self.wasDerivedFrom is not None else []
            )
        self.wasDerivedFrom = [
            v if isinstance(v, EvidenceId) else EvidenceId(v)
            for v in self.wasDerivedFrom
        ]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ExperimentalMethod(Entity):
    """
    A specification of the experimental or computational method.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCIMANTIC["ExperimentalMethod"]
    class_class_curie: ClassVar[str] = "scimantic:ExperimentalMethod"
    class_name: ClassVar[str] = "ExperimentalMethod"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.ExperimentalMethod

    id: Union[str, ExperimentalMethodId] = None
    label: str = None
    method: Optional[str] = None
    parameter: Optional[
        Union[Union[str, ParameterId], list[Union[str, ParameterId]]]
    ] = empty_list()
    wasGeneratedBy: Optional[Union[dict, "DesignOfExperiment"]] = None
    wasDerivedFrom: Optional[Union[str, HypothesisId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ExperimentalMethodId):
            self.id = ExperimentalMethodId(self.id)

        if self._is_empty(self.label):
            self.MissingRequiredField("label")
        if not isinstance(self.label, str):
            self.label = str(self.label)

        if self.method is not None and not isinstance(self.method, str):
            self.method = str(self.method)

        if not isinstance(self.parameter, list):
            self.parameter = [self.parameter] if self.parameter is not None else []
        self.parameter = [
            v if isinstance(v, ParameterId) else ParameterId(v) for v in self.parameter
        ]

        if self.wasGeneratedBy is not None and not isinstance(
            self.wasGeneratedBy, DesignOfExperiment
        ):
            self.wasGeneratedBy = DesignOfExperiment(**as_dict(self.wasGeneratedBy))

        if self.wasDerivedFrom is not None and not isinstance(
            self.wasDerivedFrom, HypothesisId
        ):
            self.wasDerivedFrom = HypothesisId(self.wasDerivedFrom)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Dataset(Entity):
    """
    Raw data, observations, or measurements produced by experimentation.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCIMANTIC["Dataset"]
    class_class_curie: ClassVar[str] = "scimantic:Dataset"
    class_name: ClassVar[str] = "Dataset"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.Dataset

    id: Union[str, DatasetId] = None
    label: str = None
    wasGeneratedBy: Optional[Union[dict, "Experimentation"]] = None
    wasDerivedFrom: Optional[Union[str, ExperimentalMethodId]] = None
    hasUncertainty: Optional[Union[str, UncertaintyModelId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DatasetId):
            self.id = DatasetId(self.id)

        if self._is_empty(self.label):
            self.MissingRequiredField("label")
        if not isinstance(self.label, str):
            self.label = str(self.label)

        if self.wasGeneratedBy is not None and not isinstance(
            self.wasGeneratedBy, Experimentation
        ):
            self.wasGeneratedBy = Experimentation(**as_dict(self.wasGeneratedBy))

        if self.wasDerivedFrom is not None and not isinstance(
            self.wasDerivedFrom, ExperimentalMethodId
        ):
            self.wasDerivedFrom = ExperimentalMethodId(self.wasDerivedFrom)

        if self.hasUncertainty is not None and not isinstance(
            self.hasUncertainty, UncertaintyModelId
        ):
            self.hasUncertainty = UncertaintyModelId(self.hasUncertainty)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Result(Entity):
    """
    The outcome of an analysis activity.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCIMANTIC["Result"]
    class_class_curie: ClassVar[str] = "scimantic:Result"
    class_name: ClassVar[str] = "Result"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.Result

    id: Union[str, ResultId] = None
    label: str = None
    wasGeneratedBy: Optional[Union[dict, "Analysis"]] = None
    wasDerivedFrom: Optional[Union[str, DatasetId]] = None
    refines: Optional[Union[str, HypothesisId]] = None
    supports: Optional[Union[str, HypothesisId]] = None
    contradicts: Optional[Union[str, HypothesisId]] = None
    hasUncertainty: Optional[Union[str, UncertaintyModelId]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ResultId):
            self.id = ResultId(self.id)

        if self._is_empty(self.label):
            self.MissingRequiredField("label")
        if not isinstance(self.label, str):
            self.label = str(self.label)

        if self.wasGeneratedBy is not None and not isinstance(
            self.wasGeneratedBy, Analysis
        ):
            self.wasGeneratedBy = Analysis(**as_dict(self.wasGeneratedBy))

        if self.wasDerivedFrom is not None and not isinstance(
            self.wasDerivedFrom, DatasetId
        ):
            self.wasDerivedFrom = DatasetId(self.wasDerivedFrom)

        if self.refines is not None and not isinstance(self.refines, HypothesisId):
            self.refines = HypothesisId(self.refines)

        if self.supports is not None and not isinstance(self.supports, HypothesisId):
            self.supports = HypothesisId(self.supports)

        if self.contradicts is not None and not isinstance(
            self.contradicts, HypothesisId
        ):
            self.contradicts = HypothesisId(self.contradicts)

        if self.hasUncertainty is not None and not isinstance(
            self.hasUncertainty, UncertaintyModelId
        ):
            self.hasUncertainty = UncertaintyModelId(self.hasUncertainty)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Parameter(Entity):
    """
    A configured parameter within an Experimental Method.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCIMANTIC["Parameter"]
    class_class_curie: ClassVar[str] = "scimantic:Parameter"
    class_name: ClassVar[str] = "Parameter"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.Parameter

    id: Union[str, ParameterId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ParameterId):
            self.id = ParameterId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class EvidenceAssessment(Activity):
    """
    The activity of evaluating credibility or relevance of Evidence.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCIMANTIC["EvidenceAssessment"]
    class_class_curie: ClassVar[str] = "scimantic:EvidenceAssessment"
    class_name: ClassVar[str] = "EvidenceAssessment"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.EvidenceAssessment

    used: Optional[Union[str, EvidenceId]] = None
    wasInformedBy: Optional[Union[dict, LiteratureSearch]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.used is not None and not isinstance(self.used, EvidenceId):
            self.used = EvidenceId(self.used)

        if self.wasInformedBy is not None and not isinstance(
            self.wasInformedBy, LiteratureSearch
        ):
            self.wasInformedBy = LiteratureSearch()

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class HypothesisFormation(Activity):
    """
    The activity of synthesizing Evidence into a Hypothesis.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCIMANTIC["HypothesisFormation"]
    class_class_curie: ClassVar[str] = "scimantic:HypothesisFormation"
    class_name: ClassVar[str] = "HypothesisFormation"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.HypothesisFormation

    used: Optional[Union[str, EvidenceId]] = None
    wasInformedBy: Optional[Union[dict, EvidenceAssessment]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.used is not None and not isinstance(self.used, EvidenceId):
            self.used = EvidenceId(self.used)

        if self.wasInformedBy is not None and not isinstance(
            self.wasInformedBy, EvidenceAssessment
        ):
            self.wasInformedBy = EvidenceAssessment(**as_dict(self.wasInformedBy))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DesignOfExperiment(Activity):
    """
    The activity of creating an ExperimentalMethod from a Hypothesis.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCIMANTIC["DesignOfExperiment"]
    class_class_curie: ClassVar[str] = "scimantic:DesignOfExperiment"
    class_name: ClassVar[str] = "DesignOfExperiment"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.DesignOfExperiment

    used: Optional[Union[str, HypothesisId]] = None
    wasInformedBy: Optional[Union[dict, HypothesisFormation]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.used is not None and not isinstance(self.used, HypothesisId):
            self.used = HypothesisId(self.used)

        if self.wasInformedBy is not None and not isinstance(
            self.wasInformedBy, HypothesisFormation
        ):
            self.wasInformedBy = HypothesisFormation(**as_dict(self.wasInformedBy))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Experimentation(Activity):
    """
    The activity of running an ExperimentalMethod to produce a Dataset.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCIMANTIC["Experimentation"]
    class_class_curie: ClassVar[str] = "scimantic:Experimentation"
    class_name: ClassVar[str] = "Experimentation"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.Experimentation

    used: Optional[Union[str, ExperimentalMethodId]] = None
    wasInformedBy: Optional[Union[dict, DesignOfExperiment]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.used is not None and not isinstance(self.used, ExperimentalMethodId):
            self.used = ExperimentalMethodId(self.used)

        if self.wasInformedBy is not None and not isinstance(
            self.wasInformedBy, DesignOfExperiment
        ):
            self.wasInformedBy = DesignOfExperiment(**as_dict(self.wasInformedBy))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Analysis(Activity):
    """
    The activity of processing a Dataset to produce a Result.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCIMANTIC["Analysis"]
    class_class_curie: ClassVar[str] = "scimantic:Analysis"
    class_name: ClassVar[str] = "Analysis"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.Analysis

    used: Optional[Union[str, DatasetId]] = None
    wasInformedBy: Optional[Union[dict, Experimentation]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.used is not None and not isinstance(self.used, DatasetId):
            self.used = DatasetId(self.used)

        if self.wasInformedBy is not None and not isinstance(
            self.wasInformedBy, Experimentation
        ):
            self.wasInformedBy = Experimentation(**as_dict(self.wasInformedBy))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ResultAssessment(Activity):
    """
    The activity of comparing a Result to the original Hypothesis.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCIMANTIC["ResultAssessment"]
    class_class_curie: ClassVar[str] = "scimantic:ResultAssessment"
    class_name: ClassVar[str] = "ResultAssessment"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.ResultAssessment

    used: Optional[Union[str, ResultId]] = None
    wasInformedBy: Optional[Union[dict, Analysis]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.used is not None and not isinstance(self.used, ResultId):
            self.used = ResultId(self.used)

        if self.wasInformedBy is not None and not isinstance(
            self.wasInformedBy, Analysis
        ):
            self.wasInformedBy = Analysis(**as_dict(self.wasInformedBy))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class UncertaintyModel(Entity):
    """
    A reified uncertainty model.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = URREF["UncertaintyModel"]
    class_class_curie: ClassVar[str] = "urref:UncertaintyModel"
    class_name: ClassVar[str] = "UncertaintyModel"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.UncertaintyModel

    id: Union[str, UncertaintyModelId] = None
    natureOfUncertainty: Union[str, "UncertaintyNature"] = None
    derivationOfUncertainty: Optional[Union[dict, "UncertaintyDerivation"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, UncertaintyModelId):
            self.id = UncertaintyModelId(self.id)

        if self._is_empty(self.natureOfUncertainty):
            self.MissingRequiredField("natureOfUncertainty")
        if not isinstance(self.natureOfUncertainty, UncertaintyNature):
            self.natureOfUncertainty = UncertaintyNature(self.natureOfUncertainty)

        if self.derivationOfUncertainty is not None and not isinstance(
            self.derivationOfUncertainty, UncertaintyDerivation
        ):
            self.derivationOfUncertainty = UncertaintyDerivation()

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Ambiguity(UncertaintyModel):
    """
    Ambiguity is inherently Epistemic uncertainty.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = URREF["Ambiguity"]
    class_class_curie: ClassVar[str] = "urref:Ambiguity"
    class_name: ClassVar[str] = "Ambiguity"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.Ambiguity

    id: Union[str, AmbiguityId] = None
    natureOfUncertainty: Union[str, "UncertaintyNature"] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AmbiguityId):
            self.id = AmbiguityId(self.id)

        if self._is_empty(self.natureOfUncertainty):
            self.MissingRequiredField("natureOfUncertainty")
        if not isinstance(self.natureOfUncertainty, UncertaintyNature):
            self.natureOfUncertainty = UncertaintyNature(self.natureOfUncertainty)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Vagueness(UncertaintyModel):
    """
    Vagueness is inherently Epistemic uncertainty.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = URREF["Vagueness"]
    class_class_curie: ClassVar[str] = "urref:Vagueness"
    class_name: ClassVar[str] = "Vagueness"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.Vagueness

    id: Union[str, VaguenessId] = None
    natureOfUncertainty: Union[str, "UncertaintyNature"] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, VaguenessId):
            self.id = VaguenessId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Incompleteness(UncertaintyModel):
    """
    Incompleteness is inherently Epistemic uncertainty.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = URREF["Incompleteness"]
    class_class_curie: ClassVar[str] = "urref:Incompleteness"
    class_name: ClassVar[str] = "Incompleteness"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.Incompleteness

    id: Union[str, IncompletenessId] = None
    natureOfUncertainty: Union[str, "UncertaintyNature"] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, IncompletenessId):
            self.id = IncompletenessId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Aleatory(UncertaintyModel):
    """
    Aleatory uncertainty entities must have nature Aleatory.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = URREF["Aleatory"]
    class_class_curie: ClassVar[str] = "urref:Aleatory"
    class_name: ClassVar[str] = "Aleatory"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.Aleatory

    id: Union[str, AleatoryId] = None
    natureOfUncertainty: Union[str, "UncertaintyNature"] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AleatoryId):
            self.id = AleatoryId(self.id)

        super().__post_init__(**kwargs)


class URREFEvidence(YAMLRoot):
    """
    Root evidence class from URREF ontology.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = URREF["Evidence"]
    class_class_curie: ClassVar[str] = "urref:Evidence"
    class_name: ClassVar[str] = "URREFEvidence"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.URREFEvidence


class UncertaintyDerivation(YAMLRoot):
    """
    Describes how the uncertainty was assessed.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = URREF["UncertaintyDerivation"]
    class_class_curie: ClassVar[str] = "urref:UncertaintyDerivation"
    class_name: ClassVar[str] = "UncertaintyDerivation"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.UncertaintyDerivation


# Enumerations
class UncertaintyNature(EnumDefinitionImpl):
    Epistemic = PermissibleValue(
        text="Epistemic", description="Uncertainty due to lack of knowledge."
    )
    Aleatory = PermissibleValue(
        text="Aleatory", description="Uncertainty due to inherent randomness."
    )

    _defn = EnumDefinition(
        name="UncertaintyNature",
    )


# Slots
class slots:
    pass


slots.label = Slot(
    uri=RDFS.label,
    name="label",
    curie=RDFS.curie("label"),
    model_uri=SCIMANTIC.label,
    domain=None,
    range=str,
)

slots.wasGeneratedBy = Slot(
    uri=PROV.wasGeneratedBy,
    name="wasGeneratedBy",
    curie=PROV.curie("wasGeneratedBy"),
    model_uri=SCIMANTIC.wasGeneratedBy,
    domain=None,
    range=Optional[Union[dict, Activity]],
)

slots.wasAssociatedWith = Slot(
    uri=PROV.wasAssociatedWith,
    name="wasAssociatedWith",
    curie=PROV.curie("wasAssociatedWith"),
    model_uri=SCIMANTIC.wasAssociatedWith,
    domain=None,
    range=Optional[Union[str, AgentId]],
)

slots.wasAttributedTo = Slot(
    uri=PROV.wasAttributedTo,
    name="wasAttributedTo",
    curie=PROV.curie("wasAttributedTo"),
    model_uri=SCIMANTIC.wasAttributedTo,
    domain=None,
    range=Optional[Union[str, AgentId]],
)

slots.id = Slot(
    uri=SCIMANTIC.id,
    name="id",
    curie=SCIMANTIC.curie("id"),
    model_uri=SCIMANTIC.id,
    domain=None,
    range=URIRef,
)

slots.motivates = Slot(
    uri=SCIMANTIC.motivates,
    name="motivates",
    curie=SCIMANTIC.curie("motivates"),
    model_uri=SCIMANTIC.motivates,
    domain=None,
    range=Optional[Union[Union[dict, Activity], list[Union[dict, Activity]]]],
)

slots.used = Slot(
    uri=PROV.used,
    name="used",
    curie=PROV.curie("used"),
    model_uri=SCIMANTIC.used,
    domain=None,
    range=Optional[Union[str, EntityId]],
)

slots.wasInformedBy = Slot(
    uri=PROV.wasInformedBy,
    name="wasInformedBy",
    curie=PROV.curie("wasInformedBy"),
    model_uri=SCIMANTIC.wasInformedBy,
    domain=None,
    range=Optional[Union[dict, Activity]],
)

slots.wasDerivedFrom = Slot(
    uri=PROV.wasDerivedFrom,
    name="wasDerivedFrom",
    curie=PROV.curie("wasDerivedFrom"),
    model_uri=SCIMANTIC.wasDerivedFrom,
    domain=None,
    range=Optional[Union[str, EntityId]],
)

slots.refines = Slot(
    uri=SCIMANTIC.refines,
    name="refines",
    curie=SCIMANTIC.curie("refines"),
    model_uri=SCIMANTIC.refines,
    domain=None,
    range=Optional[Union[str, HypothesisId]],
)

slots.supports = Slot(
    uri=SCIMANTIC.supports,
    name="supports",
    curie=SCIMANTIC.curie("supports"),
    model_uri=SCIMANTIC.supports,
    domain=Entity,
    range=Optional[Union[str, HypothesisId]],
)

slots.contradicts = Slot(
    uri=SCIMANTIC.contradicts,
    name="contradicts",
    curie=SCIMANTIC.curie("contradicts"),
    model_uri=SCIMANTIC.contradicts,
    domain=Entity,
    range=Optional[Union[str, HypothesisId]],
)

slots.method = Slot(
    uri=SCIMANTIC.method,
    name="method",
    curie=SCIMANTIC.curie("method"),
    model_uri=SCIMANTIC.method,
    domain=None,
    range=Optional[str],
)

slots.parameter = Slot(
    uri=SCIMANTIC.parameter,
    name="parameter",
    curie=SCIMANTIC.curie("parameter"),
    model_uri=SCIMANTIC.parameter,
    domain=None,
    range=Optional[Union[Union[str, ParameterId], list[Union[str, ParameterId]]]],
)

slots.hasUncertainty = Slot(
    uri=SCIMANTIC.hasUncertainty,
    name="hasUncertainty",
    curie=SCIMANTIC.curie("hasUncertainty"),
    model_uri=SCIMANTIC.hasUncertainty,
    domain=None,
    range=Optional[Union[str, UncertaintyModelId]],
)

slots.natureOfUncertainty = Slot(
    uri=URREF.natureOfUncertainty,
    name="natureOfUncertainty",
    curie=URREF.curie("natureOfUncertainty"),
    model_uri=SCIMANTIC.natureOfUncertainty,
    domain=None,
    range=Optional[Union[str, "UncertaintyNature"]],
)

slots.derivationOfUncertainty = Slot(
    uri=URREF.derivationOfUncertainty,
    name="derivationOfUncertainty",
    curie=URREF.curie("derivationOfUncertainty"),
    model_uri=SCIMANTIC.derivationOfUncertainty,
    domain=None,
    range=Optional[Union[dict, UncertaintyDerivation]],
)

slots.value = Slot(
    uri=SCIMANTIC.value,
    name="value",
    curie=SCIMANTIC.curie("value"),
    model_uri=SCIMANTIC.value,
    domain=None,
    range=Optional[str],
)

slots.unit = Slot(
    uri=SCIMANTIC.unit,
    name="unit",
    curie=SCIMANTIC.curie("unit"),
    model_uri=SCIMANTIC.unit,
    domain=None,
    range=Optional[str],
)

slots.accessLevel = Slot(
    uri=SCIMANTIC.accessLevel,
    name="accessLevel",
    curie=SCIMANTIC.curie("accessLevel"),
    model_uri=SCIMANTIC.accessLevel,
    domain=None,
    range=Optional[str],
)

slots.publishable = Slot(
    uri=SCIMANTIC.publishable,
    name="publishable",
    curie=SCIMANTIC.curie("publishable"),
    model_uri=SCIMANTIC.publishable,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.content = Slot(
    uri=SCIMANTIC.content,
    name="content",
    curie=SCIMANTIC.curie("content"),
    model_uri=SCIMANTIC.content,
    domain=None,
    range=Optional[str],
)

slots.citation = Slot(
    uri=DCTERMS.bibliographicCitation,
    name="citation",
    curie=DCTERMS.curie("bibliographicCitation"),
    model_uri=SCIMANTIC.citation,
    domain=None,
    range=Optional[str],
)

slots.source = Slot(
    uri=DCTERMS.source,
    name="source",
    curie=DCTERMS.curie("source"),
    model_uri=SCIMANTIC.source,
    domain=None,
    range=Optional[str],
)

slots.generatedAtTime = Slot(
    uri=PROV.generatedAtTime,
    name="generatedAtTime",
    curie=PROV.curie("generatedAtTime"),
    model_uri=SCIMANTIC.generatedAtTime,
    domain=None,
    range=Optional[Union[str, XSDDateTime]],
)

slots.Question_wasGeneratedBy = Slot(
    uri=PROV.wasGeneratedBy,
    name="Question_wasGeneratedBy",
    curie=PROV.curie("wasGeneratedBy"),
    model_uri=SCIMANTIC.Question_wasGeneratedBy,
    domain=Question,
    range=Optional[Union[dict, "QuestionFormation"]],
)

slots.Question_motivates = Slot(
    uri=SCIMANTIC.motivates,
    name="Question_motivates",
    curie=SCIMANTIC.curie("motivates"),
    model_uri=SCIMANTIC.Question_motivates,
    domain=Question,
    range=Optional[
        Union[Union[dict, "LiteratureSearch"], list[Union[dict, "LiteratureSearch"]]]
    ],
)

slots.Evidence_wasGeneratedBy = Slot(
    uri=PROV.wasGeneratedBy,
    name="Evidence_wasGeneratedBy",
    curie=PROV.curie("wasGeneratedBy"),
    model_uri=SCIMANTIC.Evidence_wasGeneratedBy,
    domain=Evidence,
    range=Optional[Union[dict, LiteratureSearch]],
)

slots.Hypothesis_wasGeneratedBy = Slot(
    uri=PROV.wasGeneratedBy,
    name="Hypothesis_wasGeneratedBy",
    curie=PROV.curie("wasGeneratedBy"),
    model_uri=SCIMANTIC.Hypothesis_wasGeneratedBy,
    domain=Hypothesis,
    range=Optional[Union[dict, "HypothesisFormation"]],
)

slots.Hypothesis_wasDerivedFrom = Slot(
    uri=PROV.wasDerivedFrom,
    name="Hypothesis_wasDerivedFrom",
    curie=PROV.curie("wasDerivedFrom"),
    model_uri=SCIMANTIC.Hypothesis_wasDerivedFrom,
    domain=Hypothesis,
    range=Optional[Union[Union[str, EvidenceId], list[Union[str, EvidenceId]]]],
)

slots.ExperimentalMethod_wasGeneratedBy = Slot(
    uri=PROV.wasGeneratedBy,
    name="ExperimentalMethod_wasGeneratedBy",
    curie=PROV.curie("wasGeneratedBy"),
    model_uri=SCIMANTIC.ExperimentalMethod_wasGeneratedBy,
    domain=ExperimentalMethod,
    range=Optional[Union[dict, "DesignOfExperiment"]],
)

slots.ExperimentalMethod_wasDerivedFrom = Slot(
    uri=PROV.wasDerivedFrom,
    name="ExperimentalMethod_wasDerivedFrom",
    curie=PROV.curie("wasDerivedFrom"),
    model_uri=SCIMANTIC.ExperimentalMethod_wasDerivedFrom,
    domain=ExperimentalMethod,
    range=Optional[Union[str, HypothesisId]],
)

slots.Dataset_wasGeneratedBy = Slot(
    uri=PROV.wasGeneratedBy,
    name="Dataset_wasGeneratedBy",
    curie=PROV.curie("wasGeneratedBy"),
    model_uri=SCIMANTIC.Dataset_wasGeneratedBy,
    domain=Dataset,
    range=Optional[Union[dict, "Experimentation"]],
)

slots.Dataset_wasDerivedFrom = Slot(
    uri=PROV.wasDerivedFrom,
    name="Dataset_wasDerivedFrom",
    curie=PROV.curie("wasDerivedFrom"),
    model_uri=SCIMANTIC.Dataset_wasDerivedFrom,
    domain=Dataset,
    range=Optional[Union[str, ExperimentalMethodId]],
)

slots.Result_wasGeneratedBy = Slot(
    uri=PROV.wasGeneratedBy,
    name="Result_wasGeneratedBy",
    curie=PROV.curie("wasGeneratedBy"),
    model_uri=SCIMANTIC.Result_wasGeneratedBy,
    domain=Result,
    range=Optional[Union[dict, "Analysis"]],
)

slots.Result_wasDerivedFrom = Slot(
    uri=PROV.wasDerivedFrom,
    name="Result_wasDerivedFrom",
    curie=PROV.curie("wasDerivedFrom"),
    model_uri=SCIMANTIC.Result_wasDerivedFrom,
    domain=Result,
    range=Optional[Union[str, DatasetId]],
)

slots.Result_refines = Slot(
    uri=SCIMANTIC.refines,
    name="Result_refines",
    curie=SCIMANTIC.curie("refines"),
    model_uri=SCIMANTIC.Result_refines,
    domain=Result,
    range=Optional[Union[str, HypothesisId]],
)

slots.EvidenceAssessment_used = Slot(
    uri=PROV.used,
    name="EvidenceAssessment_used",
    curie=PROV.curie("used"),
    model_uri=SCIMANTIC.EvidenceAssessment_used,
    domain=EvidenceAssessment,
    range=Optional[Union[str, EvidenceId]],
)

slots.EvidenceAssessment_wasInformedBy = Slot(
    uri=PROV.wasInformedBy,
    name="EvidenceAssessment_wasInformedBy",
    curie=PROV.curie("wasInformedBy"),
    model_uri=SCIMANTIC.EvidenceAssessment_wasInformedBy,
    domain=EvidenceAssessment,
    range=Optional[Union[dict, LiteratureSearch]],
)

slots.HypothesisFormation_used = Slot(
    uri=PROV.used,
    name="HypothesisFormation_used",
    curie=PROV.curie("used"),
    model_uri=SCIMANTIC.HypothesisFormation_used,
    domain=HypothesisFormation,
    range=Optional[Union[str, EvidenceId]],
)

slots.HypothesisFormation_wasInformedBy = Slot(
    uri=PROV.wasInformedBy,
    name="HypothesisFormation_wasInformedBy",
    curie=PROV.curie("wasInformedBy"),
    model_uri=SCIMANTIC.HypothesisFormation_wasInformedBy,
    domain=HypothesisFormation,
    range=Optional[Union[dict, EvidenceAssessment]],
)

slots.DesignOfExperiment_used = Slot(
    uri=PROV.used,
    name="DesignOfExperiment_used",
    curie=PROV.curie("used"),
    model_uri=SCIMANTIC.DesignOfExperiment_used,
    domain=DesignOfExperiment,
    range=Optional[Union[str, HypothesisId]],
)

slots.DesignOfExperiment_wasInformedBy = Slot(
    uri=PROV.wasInformedBy,
    name="DesignOfExperiment_wasInformedBy",
    curie=PROV.curie("wasInformedBy"),
    model_uri=SCIMANTIC.DesignOfExperiment_wasInformedBy,
    domain=DesignOfExperiment,
    range=Optional[Union[dict, HypothesisFormation]],
)

slots.Experimentation_used = Slot(
    uri=PROV.used,
    name="Experimentation_used",
    curie=PROV.curie("used"),
    model_uri=SCIMANTIC.Experimentation_used,
    domain=Experimentation,
    range=Optional[Union[str, ExperimentalMethodId]],
)

slots.Experimentation_wasInformedBy = Slot(
    uri=PROV.wasInformedBy,
    name="Experimentation_wasInformedBy",
    curie=PROV.curie("wasInformedBy"),
    model_uri=SCIMANTIC.Experimentation_wasInformedBy,
    domain=Experimentation,
    range=Optional[Union[dict, DesignOfExperiment]],
)

slots.Analysis_used = Slot(
    uri=PROV.used,
    name="Analysis_used",
    curie=PROV.curie("used"),
    model_uri=SCIMANTIC.Analysis_used,
    domain=Analysis,
    range=Optional[Union[str, DatasetId]],
)

slots.Analysis_wasInformedBy = Slot(
    uri=PROV.wasInformedBy,
    name="Analysis_wasInformedBy",
    curie=PROV.curie("wasInformedBy"),
    model_uri=SCIMANTIC.Analysis_wasInformedBy,
    domain=Analysis,
    range=Optional[Union[dict, Experimentation]],
)

slots.ResultAssessment_used = Slot(
    uri=PROV.used,
    name="ResultAssessment_used",
    curie=PROV.curie("used"),
    model_uri=SCIMANTIC.ResultAssessment_used,
    domain=ResultAssessment,
    range=Optional[Union[str, ResultId]],
)

slots.ResultAssessment_wasInformedBy = Slot(
    uri=PROV.wasInformedBy,
    name="ResultAssessment_wasInformedBy",
    curie=PROV.curie("wasInformedBy"),
    model_uri=SCIMANTIC.ResultAssessment_wasInformedBy,
    domain=ResultAssessment,
    range=Optional[Union[dict, Analysis]],
)

slots.UncertaintyModel_natureOfUncertainty = Slot(
    uri=URREF.natureOfUncertainty,
    name="UncertaintyModel_natureOfUncertainty",
    curie=URREF.curie("natureOfUncertainty"),
    model_uri=SCIMANTIC.UncertaintyModel_natureOfUncertainty,
    domain=UncertaintyModel,
    range=Union[str, "UncertaintyNature"],
)

slots.Ambiguity_natureOfUncertainty = Slot(
    uri=URREF.natureOfUncertainty,
    name="Ambiguity_natureOfUncertainty",
    curie=URREF.curie("natureOfUncertainty"),
    model_uri=SCIMANTIC.Ambiguity_natureOfUncertainty,
    domain=Ambiguity,
    range=Union[str, "UncertaintyNature"],
)
