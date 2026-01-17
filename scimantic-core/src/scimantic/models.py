# Auto generated from scimantic.yaml by pythongen.py version: 0.0.1
# Schema: scimantic
#
# id: http://scimantic.io/schema
# description: A minimal domain ontology for representing the scientific method as provenance chains.
# license: https://creativecommons.org/licenses/by/4.0/

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Boolean, Datetime, Integer, String
from linkml_runtime.utils.metamodelcore import Bool, XSDDateTime

metamodel_version = "1.7.0"
version = "0.1.3"

# Namespaces
DCAT = CurieNamespace('dcat', 'http://www.w3.org/ns/dcat#')
DCTERMS = CurieNamespace('dcterms', 'http://purl.org/dc/terms/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
NP = CurieNamespace('np', 'http://www.nanopub.org/nschema#')
OA = CurieNamespace('oa', 'http://www.w3.org/ns/oa#')
PROV = CurieNamespace('prov', 'http://www.w3.org/ns/prov#')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
SCIMANTIC = CurieNamespace('scimantic', 'http://scimantic.io/')
URREF = CurieNamespace('urref', 'https://raw.githubusercontent.com/adelphi23/urref/469137/URREF.ttl#')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = SCIMANTIC


# Types

# Class references
class IdentifiableId(extended_str):
    pass


class Entity(YAMLRoot):
    """
    A provenance entity. Identified by its RDF URI.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV["Entity"]
    class_class_curie: ClassVar[str] = "prov:Entity"
    class_name: ClassVar[str] = "Entity"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.Entity


class Activity(YAMLRoot):
    """
    A provenance activity. Identified by its RDF URI.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV["Activity"]
    class_class_curie: ClassVar[str] = "prov:Activity"
    class_name: ClassVar[str] = "Activity"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.Activity


class Agent(YAMLRoot):
    """
    A provenance agent. Identified by its RDF URI.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PROV["Agent"]
    class_class_curie: ClassVar[str] = "prov:Agent"
    class_name: ClassVar[str] = "Agent"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.Agent


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

    label: str = None
    wasGeneratedBy: Optional[Union[dict, "QuestionFormation"]] = None
    motivates: Optional[Union[Union[dict, "LiteratureSearch"], list[Union[dict, "LiteratureSearch"]]]] = empty_list()
    wasDerivedFrom: Optional[Union[str, list[str]]] = empty_list()
    wasAttributedTo: Optional[Union[dict, Agent]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.label):
            self.MissingRequiredField("label")
        if not isinstance(self.label, str):
            self.label = str(self.label)

        if self.wasGeneratedBy is not None and not isinstance(self.wasGeneratedBy, QuestionFormation):
            self.wasGeneratedBy = QuestionFormation(**as_dict(self.wasGeneratedBy))

        if not isinstance(self.motivates, list):
            self.motivates = [self.motivates] if self.motivates is not None else []
        self.motivates = [v if isinstance(v, LiteratureSearch) else LiteratureSearch(**as_dict(v)) for v in self.motivates]

        if not isinstance(self.wasDerivedFrom, list):
            self.wasDerivedFrom = [self.wasDerivedFrom] if self.wasDerivedFrom is not None else []
        self.wasDerivedFrom = [v if isinstance(v, str) else str(v) for v in self.wasDerivedFrom]

        if self.wasAttributedTo is not None and not isinstance(self.wasAttributedTo, Agent):
            self.wasAttributedTo = Agent()

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class QuestionFormation(Activity):
    """
    The activity of creating or refining a Research Question. Can be informed by prior results (iterating on findings)
    or by literature search (refining questions based on discovered evidence).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCIMANTIC["QuestionFormation"]
    class_class_curie: ClassVar[str] = "scimantic:QuestionFormation"
    class_name: ClassVar[str] = "QuestionFormation"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.QuestionFormation

    wasAssociatedWith: Optional[Union[dict, Agent]] = None
    wasInformedBy: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.wasAssociatedWith is not None and not isinstance(self.wasAssociatedWith, Agent):
            self.wasAssociatedWith = Agent()

        if self.wasInformedBy is not None and not isinstance(self.wasInformedBy, str):
            self.wasInformedBy = str(self.wasInformedBy)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class LiteratureSearch(Activity):
    """
    The activity of searching literature and creating Annotations (highlights, notes) on source text.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCIMANTIC["LiteratureSearch"]
    class_class_curie: ClassVar[str] = "scimantic:LiteratureSearch"
    class_name: ClassVar[str] = "LiteratureSearch"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.LiteratureSearch

    wasAssociatedWith: Optional[Union[dict, Agent]] = None
    wasInformedBy: Optional[Union[dict, QuestionFormation]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.wasAssociatedWith is not None and not isinstance(self.wasAssociatedWith, Agent):
            self.wasAssociatedWith = Agent()

        if self.wasInformedBy is not None and not isinstance(self.wasInformedBy, QuestionFormation):
            self.wasInformedBy = QuestionFormation(**as_dict(self.wasInformedBy))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class EvidenceExtraction(Activity):
    """
    The activity of articulating Evidence claims from one or more Annotations. Separates the act of
    reading/highlighting from the act of formulating evidence statements.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCIMANTIC["EvidenceExtraction"]
    class_class_curie: ClassVar[str] = "scimantic:EvidenceExtraction"
    class_name: ClassVar[str] = "EvidenceExtraction"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.EvidenceExtraction

    used: Optional[Union[Union[dict, "Annotation"], list[Union[dict, "Annotation"]]]] = empty_list()
    wasAssociatedWith: Optional[Union[dict, Agent]] = None
    wasInformedBy: Optional[Union[dict, LiteratureSearch]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.used, list):
            self.used = [self.used] if self.used is not None else []
        self.used = [v if isinstance(v, Annotation) else Annotation(**as_dict(v)) for v in self.used]

        if self.wasAssociatedWith is not None and not isinstance(self.wasAssociatedWith, Agent):
            self.wasAssociatedWith = Agent()

        if self.wasInformedBy is not None and not isinstance(self.wasInformedBy, LiteratureSearch):
            self.wasInformedBy = LiteratureSearch(**as_dict(self.wasInformedBy))

        super().__post_init__(**kwargs)


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

    label: str = None
    content: Optional[str] = None
    citation: Optional[str] = None
    source: Optional[str] = None
    wasGeneratedBy: Optional[Union[dict, EvidenceExtraction]] = None
    wasDerivedFrom: Optional[Union[str, list[str]]] = empty_list()
    wasAttributedTo: Optional[Union[dict, Agent]] = None
    accessLevel: Optional[str] = None
    publishable: Optional[Union[bool, Bool]] = None
    supports: Optional[Union[dict, "Hypothesis"]] = None
    contradicts: Optional[Union[dict, "Hypothesis"]] = None
    hasUncertainty: Optional[Union[dict, "UncertaintyModel"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
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

        if self.wasGeneratedBy is not None and not isinstance(self.wasGeneratedBy, EvidenceExtraction):
            self.wasGeneratedBy = EvidenceExtraction(**as_dict(self.wasGeneratedBy))

        if not isinstance(self.wasDerivedFrom, list):
            self.wasDerivedFrom = [self.wasDerivedFrom] if self.wasDerivedFrom is not None else []
        self.wasDerivedFrom = [v if isinstance(v, str) else str(v) for v in self.wasDerivedFrom]

        if self.wasAttributedTo is not None and not isinstance(self.wasAttributedTo, Agent):
            self.wasAttributedTo = Agent()

        if self.accessLevel is not None and not isinstance(self.accessLevel, str):
            self.accessLevel = str(self.accessLevel)

        if self.publishable is not None and not isinstance(self.publishable, Bool):
            self.publishable = Bool(self.publishable)

        if self.supports is not None and not isinstance(self.supports, Hypothesis):
            self.supports = Hypothesis(**as_dict(self.supports))

        if self.contradicts is not None and not isinstance(self.contradicts, Hypothesis):
            self.contradicts = Hypothesis(**as_dict(self.contradicts))

        if self.hasUncertainty is not None and not isinstance(self.hasUncertainty, UncertaintyModel):
            self.hasUncertainty = UncertaintyModel(**as_dict(self.hasUncertainty))

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

    label: str = None
    wasGeneratedBy: Optional[Union[dict, "HypothesisFormation"]] = None
    wasDerivedFrom: Optional[Union[Union[dict, "Premise"], list[Union[dict, "Premise"]]]] = empty_list()
    wasAttributedTo: Optional[Union[dict, Agent]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.label):
            self.MissingRequiredField("label")
        if not isinstance(self.label, str):
            self.label = str(self.label)

        if self.wasGeneratedBy is not None and not isinstance(self.wasGeneratedBy, HypothesisFormation):
            self.wasGeneratedBy = HypothesisFormation(**as_dict(self.wasGeneratedBy))

        if not isinstance(self.wasDerivedFrom, list):
            self.wasDerivedFrom = [self.wasDerivedFrom] if self.wasDerivedFrom is not None else []
        self.wasDerivedFrom = [v if isinstance(v, Premise) else Premise(**as_dict(v)) for v in self.wasDerivedFrom]

        if self.wasAttributedTo is not None and not isinstance(self.wasAttributedTo, Agent):
            self.wasAttributedTo = Agent()

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

    label: str = None
    method: Optional[str] = None
    parameter: Optional[Union[Union[dict, "Parameter"], list[Union[dict, "Parameter"]]]] = empty_list()
    wasGeneratedBy: Optional[Union[dict, "DesignOfExperiment"]] = None
    wasDerivedFrom: Optional[str] = None
    wasAttributedTo: Optional[Union[dict, Agent]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.label):
            self.MissingRequiredField("label")
        if not isinstance(self.label, str):
            self.label = str(self.label)

        if self.method is not None and not isinstance(self.method, str):
            self.method = str(self.method)

        if not isinstance(self.parameter, list):
            self.parameter = [self.parameter] if self.parameter is not None else []
        self.parameter = [v if isinstance(v, Parameter) else Parameter(**as_dict(v)) for v in self.parameter]

        if self.wasGeneratedBy is not None and not isinstance(self.wasGeneratedBy, DesignOfExperiment):
            self.wasGeneratedBy = DesignOfExperiment(**as_dict(self.wasGeneratedBy))

        if self.wasDerivedFrom is not None and not isinstance(self.wasDerivedFrom, str):
            self.wasDerivedFrom = str(self.wasDerivedFrom)

        if self.wasAttributedTo is not None and not isinstance(self.wasAttributedTo, Agent):
            self.wasAttributedTo = Agent()

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Premise(Entity):
    """
    An evaluated proposition or insight derived from Evidence.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCIMANTIC["Premise"]
    class_class_curie: ClassVar[str] = "scimantic:Premise"
    class_name: ClassVar[str] = "Premise"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.Premise

    label: str = None
    wasGeneratedBy: Optional[Union[dict, "EvidenceAssessment"]] = None
    wasDerivedFrom: Optional[Union[dict, Evidence]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.label):
            self.MissingRequiredField("label")
        if not isinstance(self.label, str):
            self.label = str(self.label)

        if self.wasGeneratedBy is not None and not isinstance(self.wasGeneratedBy, EvidenceAssessment):
            self.wasGeneratedBy = EvidenceAssessment(**as_dict(self.wasGeneratedBy))

        if self.wasDerivedFrom is not None and not isinstance(self.wasDerivedFrom, Evidence):
            self.wasDerivedFrom = Evidence(**as_dict(self.wasDerivedFrom))

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

    label: str = None
    wasGeneratedBy: Optional[Union[dict, "Experimentation"]] = None
    wasDerivedFrom: Optional[Union[dict, ExperimentalMethod]] = None
    hasUncertainty: Optional[Union[dict, "UncertaintyModel"]] = None
    wasAttributedTo: Optional[Union[dict, Agent]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.label):
            self.MissingRequiredField("label")
        if not isinstance(self.label, str):
            self.label = str(self.label)

        if self.wasGeneratedBy is not None and not isinstance(self.wasGeneratedBy, Experimentation):
            self.wasGeneratedBy = Experimentation(**as_dict(self.wasGeneratedBy))

        if self.wasDerivedFrom is not None and not isinstance(self.wasDerivedFrom, ExperimentalMethod):
            self.wasDerivedFrom = ExperimentalMethod(**as_dict(self.wasDerivedFrom))

        if self.hasUncertainty is not None and not isinstance(self.hasUncertainty, UncertaintyModel):
            self.hasUncertainty = UncertaintyModel(**as_dict(self.hasUncertainty))

        if self.wasAttributedTo is not None and not isinstance(self.wasAttributedTo, Agent):
            self.wasAttributedTo = Agent()

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

    label: str = None
    wasGeneratedBy: Optional[Union[dict, "Analysis"]] = None
    wasDerivedFrom: Optional[Union[dict, Dataset]] = None
    wasAttributedTo: Optional[Union[dict, Agent]] = None
    refines: Optional[Union[dict, Hypothesis]] = None
    supports: Optional[Union[dict, Hypothesis]] = None
    contradicts: Optional[Union[dict, Hypothesis]] = None
    hasUncertainty: Optional[Union[dict, "UncertaintyModel"]] = None
    value: Optional[str] = None
    unit: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.label):
            self.MissingRequiredField("label")
        if not isinstance(self.label, str):
            self.label = str(self.label)

        if self.wasGeneratedBy is not None and not isinstance(self.wasGeneratedBy, Analysis):
            self.wasGeneratedBy = Analysis(**as_dict(self.wasGeneratedBy))

        if self.wasDerivedFrom is not None and not isinstance(self.wasDerivedFrom, Dataset):
            self.wasDerivedFrom = Dataset(**as_dict(self.wasDerivedFrom))

        if self.wasAttributedTo is not None and not isinstance(self.wasAttributedTo, Agent):
            self.wasAttributedTo = Agent()

        if self.refines is not None and not isinstance(self.refines, Hypothesis):
            self.refines = Hypothesis(**as_dict(self.refines))

        if self.supports is not None and not isinstance(self.supports, Hypothesis):
            self.supports = Hypothesis(**as_dict(self.supports))

        if self.contradicts is not None and not isinstance(self.contradicts, Hypothesis):
            self.contradicts = Hypothesis(**as_dict(self.contradicts))

        if self.hasUncertainty is not None and not isinstance(self.hasUncertainty, UncertaintyModel):
            self.hasUncertainty = UncertaintyModel(**as_dict(self.hasUncertainty))

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.unit is not None and not isinstance(self.unit, str):
            self.unit = str(self.unit)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Conclusion(Entity):
    """
    The final claim or decision derived from the ResultAssessment.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCIMANTIC["Conclusion"]
    class_class_curie: ClassVar[str] = "scimantic:Conclusion"
    class_name: ClassVar[str] = "Conclusion"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.Conclusion

    label: str = None
    content: Optional[str] = None
    wasGeneratedBy: Optional[Union[dict, "ResultAssessment"]] = None
    wasDerivedFrom: Optional[Union[dict, Result]] = None
    wasAttributedTo: Optional[Union[dict, Agent]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.label):
            self.MissingRequiredField("label")
        if not isinstance(self.label, str):
            self.label = str(self.label)

        if self.content is not None and not isinstance(self.content, str):
            self.content = str(self.content)

        if self.wasGeneratedBy is not None and not isinstance(self.wasGeneratedBy, ResultAssessment):
            self.wasGeneratedBy = ResultAssessment(**as_dict(self.wasGeneratedBy))

        if self.wasDerivedFrom is not None and not isinstance(self.wasDerivedFrom, Result):
            self.wasDerivedFrom = Result(**as_dict(self.wasDerivedFrom))

        if self.wasAttributedTo is not None and not isinstance(self.wasAttributedTo, Agent):
            self.wasAttributedTo = Agent()

        super().__post_init__(**kwargs)


class Parameter(Entity):
    """
    A configured parameter within an Experimental Method.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCIMANTIC["Parameter"]
    class_class_curie: ClassVar[str] = "scimantic:Parameter"
    class_name: ClassVar[str] = "Parameter"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.Parameter


@dataclass(repr=False)
class Annotation(Entity):
    """
    A text annotation or highlight that grounds Questions or Evidence in specific source text. Follows W3C Web
    Annotation Data Model.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = OA["Annotation"]
    class_class_curie: ClassVar[str] = "oa:Annotation"
    class_name: ClassVar[str] = "Annotation"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.Annotation

    label: str = None
    hasTarget: str = None
    hasBody: Optional[str] = None
    hasSelector: Optional[Union[dict, "TextSelector"]] = None
    wasAttributedTo: Optional[Union[dict, Agent]] = None
    wasGeneratedBy: Optional[Union[dict, LiteratureSearch]] = None
    generatedAtTime: Optional[Union[str, XSDDateTime]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.label):
            self.MissingRequiredField("label")
        if not isinstance(self.label, str):
            self.label = str(self.label)

        if self._is_empty(self.hasTarget):
            self.MissingRequiredField("hasTarget")
        if not isinstance(self.hasTarget, str):
            self.hasTarget = str(self.hasTarget)

        if self.hasBody is not None and not isinstance(self.hasBody, str):
            self.hasBody = str(self.hasBody)

        if self.hasSelector is not None and not isinstance(self.hasSelector, TextSelector):
            self.hasSelector = TextSelector(**as_dict(self.hasSelector))

        if self.wasAttributedTo is not None and not isinstance(self.wasAttributedTo, Agent):
            self.wasAttributedTo = Agent()

        if self.wasGeneratedBy is not None and not isinstance(self.wasGeneratedBy, LiteratureSearch):
            self.wasGeneratedBy = LiteratureSearch(**as_dict(self.wasGeneratedBy))

        if self.generatedAtTime is not None and not isinstance(self.generatedAtTime, XSDDateTime):
            self.generatedAtTime = XSDDateTime(self.generatedAtTime)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TextSelector(Entity):
    """
    A selector that identifies text by exact quote with surrounding context. Follows W3C Web Annotation
    TextQuoteSelector.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = OA["TextQuoteSelector"]
    class_class_curie: ClassVar[str] = "oa:TextQuoteSelector"
    class_name: ClassVar[str] = "TextSelector"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.TextSelector

    exact: str = None
    prefix: Optional[str] = None
    suffix: Optional[str] = None
    startOffset: Optional[int] = None
    endOffset: Optional[int] = None
    pageNumber: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.exact):
            self.MissingRequiredField("exact")
        if not isinstance(self.exact, str):
            self.exact = str(self.exact)

        if self.prefix is not None and not isinstance(self.prefix, str):
            self.prefix = str(self.prefix)

        if self.suffix is not None and not isinstance(self.suffix, str):
            self.suffix = str(self.suffix)

        if self.startOffset is not None and not isinstance(self.startOffset, int):
            self.startOffset = int(self.startOffset)

        if self.endOffset is not None and not isinstance(self.endOffset, int):
            self.endOffset = int(self.endOffset)

        if self.pageNumber is not None and not isinstance(self.pageNumber, int):
            self.pageNumber = int(self.pageNumber)

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

    used: Optional[Union[dict, Evidence]] = None
    wasInformedBy: Optional[Union[dict, EvidenceExtraction]] = None
    wasAssociatedWith: Optional[Union[dict, Agent]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.used is not None and not isinstance(self.used, Evidence):
            self.used = Evidence(**as_dict(self.used))

        if self.wasInformedBy is not None and not isinstance(self.wasInformedBy, EvidenceExtraction):
            self.wasInformedBy = EvidenceExtraction(**as_dict(self.wasInformedBy))

        if self.wasAssociatedWith is not None and not isinstance(self.wasAssociatedWith, Agent):
            self.wasAssociatedWith = Agent()

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

    used: Optional[Union[dict, Premise]] = None
    wasInformedBy: Optional[Union[dict, EvidenceAssessment]] = None
    wasAssociatedWith: Optional[Union[dict, Agent]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.used is not None and not isinstance(self.used, Premise):
            self.used = Premise(**as_dict(self.used))

        if self.wasInformedBy is not None and not isinstance(self.wasInformedBy, EvidenceAssessment):
            self.wasInformedBy = EvidenceAssessment(**as_dict(self.wasInformedBy))

        if self.wasAssociatedWith is not None and not isinstance(self.wasAssociatedWith, Agent):
            self.wasAssociatedWith = Agent()

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

    used: Optional[str] = None
    wasInformedBy: Optional[str] = None
    wasAssociatedWith: Optional[Union[dict, Agent]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.used is not None and not isinstance(self.used, str):
            self.used = str(self.used)

        if self.wasInformedBy is not None and not isinstance(self.wasInformedBy, str):
            self.wasInformedBy = str(self.wasInformedBy)

        if self.wasAssociatedWith is not None and not isinstance(self.wasAssociatedWith, Agent):
            self.wasAssociatedWith = Agent()

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

    used: Optional[Union[dict, ExperimentalMethod]] = None
    wasInformedBy: Optional[Union[dict, DesignOfExperiment]] = None
    wasAssociatedWith: Optional[Union[dict, Agent]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.used is not None and not isinstance(self.used, ExperimentalMethod):
            self.used = ExperimentalMethod(**as_dict(self.used))

        if self.wasInformedBy is not None and not isinstance(self.wasInformedBy, DesignOfExperiment):
            self.wasInformedBy = DesignOfExperiment(**as_dict(self.wasInformedBy))

        if self.wasAssociatedWith is not None and not isinstance(self.wasAssociatedWith, Agent):
            self.wasAssociatedWith = Agent()

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

    used: Optional[Union[dict, Dataset]] = None
    wasInformedBy: Optional[Union[dict, Experimentation]] = None
    wasAssociatedWith: Optional[Union[dict, Agent]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.used is not None and not isinstance(self.used, Dataset):
            self.used = Dataset(**as_dict(self.used))

        if self.wasInformedBy is not None and not isinstance(self.wasInformedBy, Experimentation):
            self.wasInformedBy = Experimentation(**as_dict(self.wasInformedBy))

        if self.wasAssociatedWith is not None and not isinstance(self.wasAssociatedWith, Agent):
            self.wasAssociatedWith = Agent()

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

    used: Optional[Union[dict, Result]] = None
    wasInformedBy: Optional[Union[dict, Analysis]] = None
    wasAssociatedWith: Optional[Union[dict, Agent]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.used is not None and not isinstance(self.used, Result):
            self.used = Result(**as_dict(self.used))

        if self.wasInformedBy is not None and not isinstance(self.wasInformedBy, Analysis):
            self.wasInformedBy = Analysis(**as_dict(self.wasInformedBy))

        if self.wasAssociatedWith is not None and not isinstance(self.wasAssociatedWith, Agent):
            self.wasAssociatedWith = Agent()

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

    natureOfUncertainty: Union[str, "UncertaintyNature"] = None
    derivationOfUncertainty: Optional[Union[dict, "UncertaintyDerivation"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.natureOfUncertainty):
            self.MissingRequiredField("natureOfUncertainty")
        if not isinstance(self.natureOfUncertainty, UncertaintyNature):
            self.natureOfUncertainty = UncertaintyNature(self.natureOfUncertainty)

        if self.derivationOfUncertainty is not None and not isinstance(self.derivationOfUncertainty, UncertaintyDerivation):
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

    natureOfUncertainty: Union[str, "UncertaintyNature"] = None

    def __post_init__(self, *_: str, **kwargs: Any):
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

    natureOfUncertainty: Union[str, "UncertaintyNature"] = None

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

    natureOfUncertainty: Union[str, "UncertaintyNature"] = None

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

    natureOfUncertainty: Union[str, "UncertaintyNature"] = None

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


class Nanopublication(YAMLRoot):
    """
    A nanopublication object.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NP["Nanopublication"]
    class_class_curie: ClassVar[str] = "np:Nanopublication"
    class_name: ClassVar[str] = "Nanopublication"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.Nanopublication


@dataclass(repr=False)
class Identifiable(YAMLRoot):
    """
    A mixin for objects that have a unique identifier.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCIMANTIC["Identifiable"]
    class_class_curie: ClassVar[str] = "scimantic:Identifiable"
    class_name: ClassVar[str] = "Identifiable"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.Identifiable

    id: Union[str, IdentifiableId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, IdentifiableId):
            self.id = IdentifiableId(self.id)

        super().__post_init__(**kwargs)


class UncertaintySubject(YAMLRoot):
    """
    A mixin for objects that can have a reified uncertainty model.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCIMANTIC["UncertaintySubject"]
    class_class_curie: ClassVar[str] = "scimantic:UncertaintySubject"
    class_name: ClassVar[str] = "UncertaintySubject"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.UncertaintySubject


class DCATDataset(YAMLRoot):
    """
    A collection of data, published or curated by a single agent.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCAT["Dataset"]
    class_class_curie: ClassVar[str] = "dcat:Dataset"
    class_name: ClassVar[str] = "DCATDataset"
    class_model_uri: ClassVar[URIRef] = SCIMANTIC.DCATDataset


# Enumerations
class UncertaintyNature(EnumDefinitionImpl):

    Epistemic = PermissibleValue(
        text="Epistemic",
        description="Uncertainty due to lack of knowledge.")
    Aleatory = PermissibleValue(
        text="Aleatory",
        description="Uncertainty due to inherent randomness.")

    _defn = EnumDefinition(
        name="UncertaintyNature",
    )

# Slots
class slots:
    pass

slots.label = Slot(uri=RDFS.label, name="label", curie=RDFS.curie('label'),
                   model_uri=SCIMANTIC.label, domain=None, range=str)

slots.wasGeneratedBy = Slot(uri=PROV.wasGeneratedBy, name="wasGeneratedBy", curie=PROV.curie('wasGeneratedBy'),
                   model_uri=SCIMANTIC.wasGeneratedBy, domain=None, range=Optional[str])

slots.wasAssociatedWith = Slot(uri=PROV.wasAssociatedWith, name="wasAssociatedWith", curie=PROV.curie('wasAssociatedWith'),
                   model_uri=SCIMANTIC.wasAssociatedWith, domain=Activity, range=Optional[Union[dict, "Agent"]])

slots.wasAttributedTo = Slot(uri=PROV.wasAttributedTo, name="wasAttributedTo", curie=PROV.curie('wasAttributedTo'),
                   model_uri=SCIMANTIC.wasAttributedTo, domain=Entity, range=Optional[Union[dict, "Agent"]])

slots.id = Slot(uri=SCIMANTIC.id, name="id", curie=SCIMANTIC.curie('id'),
                   model_uri=SCIMANTIC.id, domain=None, range=Union[str, IdentifiableId])

slots.motivates = Slot(uri=SCIMANTIC.motivates, name="motivates", curie=SCIMANTIC.curie('motivates'),
                   model_uri=SCIMANTIC.motivates, domain=None, range=Optional[Union[str, list[str]]])

slots.used = Slot(uri=PROV.used, name="used", curie=PROV.curie('used'),
                   model_uri=SCIMANTIC.used, domain=None, range=Optional[str])

slots.wasInformedBy = Slot(uri=PROV.wasInformedBy, name="wasInformedBy", curie=PROV.curie('wasInformedBy'),
                   model_uri=SCIMANTIC.wasInformedBy, domain=None, range=Optional[str])

slots.wasDerivedFrom = Slot(uri=PROV.wasDerivedFrom, name="wasDerivedFrom", curie=PROV.curie('wasDerivedFrom'),
                   model_uri=SCIMANTIC.wasDerivedFrom, domain=None, range=Optional[str])

slots.refines = Slot(uri=SCIMANTIC.refines, name="refines", curie=SCIMANTIC.curie('refines'),
                   model_uri=SCIMANTIC.refines, domain=None, range=Optional[str])

slots.supports = Slot(uri=SCIMANTIC.supports, name="supports", curie=SCIMANTIC.curie('supports'),
                   model_uri=SCIMANTIC.supports, domain=None, range=Optional[str])

slots.contradicts = Slot(uri=SCIMANTIC.contradicts, name="contradicts", curie=SCIMANTIC.curie('contradicts'),
                   model_uri=SCIMANTIC.contradicts, domain=None, range=Optional[str])

slots.method = Slot(uri=SCIMANTIC.method, name="method", curie=SCIMANTIC.curie('method'),
                   model_uri=SCIMANTIC.method, domain=ExperimentalMethod, range=Optional[str])

slots.parameter = Slot(uri=SCIMANTIC.parameter, name="parameter", curie=SCIMANTIC.curie('parameter'),
                   model_uri=SCIMANTIC.parameter, domain=ExperimentalMethod, range=Optional[Union[Union[dict, "Parameter"], list[Union[dict, "Parameter"]]]])

slots.hasUncertainty = Slot(uri=SCIMANTIC.hasUncertainty, name="hasUncertainty", curie=SCIMANTIC.curie('hasUncertainty'),
                   model_uri=SCIMANTIC.hasUncertainty, domain=UncertaintySubject, range=Optional[Union[dict, UncertaintyModel]])

slots.natureOfUncertainty = Slot(uri=URREF.natureOfUncertainty, name="natureOfUncertainty", curie=URREF.curie('natureOfUncertainty'),
                   model_uri=SCIMANTIC.natureOfUncertainty, domain=UncertaintyModel, range=Optional[Union[str, "UncertaintyNature"]])

slots.derivationOfUncertainty = Slot(uri=URREF.derivationOfUncertainty, name="derivationOfUncertainty", curie=URREF.curie('derivationOfUncertainty'),
                   model_uri=SCIMANTIC.derivationOfUncertainty, domain=UncertaintyModel, range=Optional[Union[dict, "UncertaintyDerivation"]])

slots.value = Slot(uri=SCIMANTIC.value, name="value", curie=SCIMANTIC.curie('value'),
                   model_uri=SCIMANTIC.value, domain=Result, range=Optional[str])

slots.unit = Slot(uri=SCIMANTIC.unit, name="unit", curie=SCIMANTIC.curie('unit'),
                   model_uri=SCIMANTIC.unit, domain=Result, range=Optional[str])

slots.accessLevel = Slot(uri=SCIMANTIC.accessLevel, name="accessLevel", curie=SCIMANTIC.curie('accessLevel'),
                   model_uri=SCIMANTIC.accessLevel, domain=Nanopublication, range=Optional[str])

slots.publishable = Slot(uri=SCIMANTIC.publishable, name="publishable", curie=SCIMANTIC.curie('publishable'),
                   model_uri=SCIMANTIC.publishable, domain=Nanopublication, range=Optional[Union[bool, Bool]])

slots.content = Slot(uri=SCIMANTIC.content, name="content", curie=SCIMANTIC.curie('content'),
                   model_uri=SCIMANTIC.content, domain=Evidence, range=Optional[str])

slots.citation = Slot(uri=DCTERMS.bibliographicCitation, name="citation", curie=DCTERMS.curie('bibliographicCitation'),
                   model_uri=SCIMANTIC.citation, domain=Evidence, range=Optional[str])

slots.source = Slot(uri=DCTERMS.source, name="source", curie=DCTERMS.curie('source'),
                   model_uri=SCIMANTIC.source, domain=Evidence, range=Optional[str])

slots.generatedAtTime = Slot(uri=PROV.generatedAtTime, name="generatedAtTime", curie=PROV.curie('generatedAtTime'),
                   model_uri=SCIMANTIC.generatedAtTime, domain=Entity, range=Optional[Union[str, XSDDateTime]])

slots.hasBody = Slot(uri=OA.hasBody, name="hasBody", curie=OA.curie('hasBody'),
                   model_uri=SCIMANTIC.hasBody, domain=None, range=Optional[str])

slots.hasTarget = Slot(uri=OA.hasTarget, name="hasTarget", curie=OA.curie('hasTarget'),
                   model_uri=SCIMANTIC.hasTarget, domain=None, range=Optional[str])

slots.hasSelector = Slot(uri=OA.hasSelector, name="hasSelector", curie=OA.curie('hasSelector'),
                   model_uri=SCIMANTIC.hasSelector, domain=None, range=Optional[str])

slots.exact = Slot(uri=OA.exact, name="exact", curie=OA.curie('exact'),
                   model_uri=SCIMANTIC.exact, domain=None, range=str)

slots.prefix = Slot(uri=OA.prefix, name="prefix", curie=OA.curie('prefix'),
                   model_uri=SCIMANTIC.prefix, domain=None, range=Optional[str])

slots.suffix = Slot(uri=OA.suffix, name="suffix", curie=OA.curie('suffix'),
                   model_uri=SCIMANTIC.suffix, domain=None, range=Optional[str])

slots.startOffset = Slot(uri=OA.start, name="startOffset", curie=OA.curie('start'),
                   model_uri=SCIMANTIC.startOffset, domain=None, range=Optional[int])

slots.endOffset = Slot(uri=OA.end, name="endOffset", curie=OA.curie('end'),
                   model_uri=SCIMANTIC.endOffset, domain=None, range=Optional[int])

slots.pageNumber = Slot(uri=SCIMANTIC.pageNumber, name="pageNumber", curie=SCIMANTIC.curie('pageNumber'),
                   model_uri=SCIMANTIC.pageNumber, domain=None, range=Optional[int])

slots.Question_wasGeneratedBy = Slot(uri=PROV.wasGeneratedBy, name="Question_wasGeneratedBy", curie=PROV.curie('wasGeneratedBy'),
                   model_uri=SCIMANTIC.Question_wasGeneratedBy, domain=Question, range=Optional[Union[dict, "QuestionFormation"]])

slots.Question_motivates = Slot(uri=SCIMANTIC.motivates, name="Question_motivates", curie=SCIMANTIC.curie('motivates'),
                   model_uri=SCIMANTIC.Question_motivates, domain=Question, range=Optional[Union[Union[dict, "LiteratureSearch"], list[Union[dict, "LiteratureSearch"]]]])

slots.Question_wasDerivedFrom = Slot(uri=PROV.wasDerivedFrom, name="Question_wasDerivedFrom", curie=PROV.curie('wasDerivedFrom'),
                   model_uri=SCIMANTIC.Question_wasDerivedFrom, domain=Question, range=Optional[Union[str, list[str]]])

slots.QuestionFormation_wasInformedBy = Slot(uri=PROV.wasInformedBy, name="QuestionFormation_wasInformedBy", curie=PROV.curie('wasInformedBy'),
                   model_uri=SCIMANTIC.QuestionFormation_wasInformedBy, domain=QuestionFormation, range=Optional[str])

slots.LiteratureSearch_wasInformedBy = Slot(uri=PROV.wasInformedBy, name="LiteratureSearch_wasInformedBy", curie=PROV.curie('wasInformedBy'),
                   model_uri=SCIMANTIC.LiteratureSearch_wasInformedBy, domain=LiteratureSearch, range=Optional[Union[dict, QuestionFormation]])

slots.EvidenceExtraction_used = Slot(uri=PROV.used, name="EvidenceExtraction_used", curie=PROV.curie('used'),
                   model_uri=SCIMANTIC.EvidenceExtraction_used, domain=EvidenceExtraction, range=Optional[Union[Union[dict, "Annotation"], list[Union[dict, "Annotation"]]]])

slots.EvidenceExtraction_wasInformedBy = Slot(uri=PROV.wasInformedBy, name="EvidenceExtraction_wasInformedBy", curie=PROV.curie('wasInformedBy'),
                   model_uri=SCIMANTIC.EvidenceExtraction_wasInformedBy, domain=EvidenceExtraction, range=Optional[Union[dict, LiteratureSearch]])

slots.Evidence_wasDerivedFrom = Slot(uri=PROV.wasDerivedFrom, name="Evidence_wasDerivedFrom", curie=PROV.curie('wasDerivedFrom'),
                   model_uri=SCIMANTIC.Evidence_wasDerivedFrom, domain=Evidence, range=Optional[Union[str, list[str]]])

slots.Evidence_wasGeneratedBy = Slot(uri=PROV.wasGeneratedBy, name="Evidence_wasGeneratedBy", curie=PROV.curie('wasGeneratedBy'),
                   model_uri=SCIMANTIC.Evidence_wasGeneratedBy, domain=Evidence, range=Optional[Union[dict, EvidenceExtraction]])

slots.Evidence_supports = Slot(uri=SCIMANTIC.supports, name="Evidence_supports", curie=SCIMANTIC.curie('supports'),
                   model_uri=SCIMANTIC.Evidence_supports, domain=Evidence, range=Optional[Union[dict, "Hypothesis"]])

slots.Evidence_contradicts = Slot(uri=SCIMANTIC.contradicts, name="Evidence_contradicts", curie=SCIMANTIC.curie('contradicts'),
                   model_uri=SCIMANTIC.Evidence_contradicts, domain=Evidence, range=Optional[Union[dict, "Hypothesis"]])

slots.Hypothesis_wasGeneratedBy = Slot(uri=PROV.wasGeneratedBy, name="Hypothesis_wasGeneratedBy", curie=PROV.curie('wasGeneratedBy'),
                   model_uri=SCIMANTIC.Hypothesis_wasGeneratedBy, domain=Hypothesis, range=Optional[Union[dict, "HypothesisFormation"]])

slots.Hypothesis_wasDerivedFrom = Slot(uri=PROV.wasDerivedFrom, name="Hypothesis_wasDerivedFrom", curie=PROV.curie('wasDerivedFrom'),
                   model_uri=SCIMANTIC.Hypothesis_wasDerivedFrom, domain=Hypothesis, range=Optional[Union[Union[dict, "Premise"], list[Union[dict, "Premise"]]]])

slots.ExperimentalMethod_wasGeneratedBy = Slot(uri=PROV.wasGeneratedBy, name="ExperimentalMethod_wasGeneratedBy", curie=PROV.curie('wasGeneratedBy'),
                   model_uri=SCIMANTIC.ExperimentalMethod_wasGeneratedBy, domain=ExperimentalMethod, range=Optional[Union[dict, "DesignOfExperiment"]])

slots.ExperimentalMethod_wasDerivedFrom = Slot(uri=PROV.wasDerivedFrom, name="ExperimentalMethod_wasDerivedFrom", curie=PROV.curie('wasDerivedFrom'),
                   model_uri=SCIMANTIC.ExperimentalMethod_wasDerivedFrom, domain=ExperimentalMethod, range=Optional[str])

slots.Premise_wasGeneratedBy = Slot(uri=PROV.wasGeneratedBy, name="Premise_wasGeneratedBy", curie=PROV.curie('wasGeneratedBy'),
                   model_uri=SCIMANTIC.Premise_wasGeneratedBy, domain=Premise, range=Optional[Union[dict, "EvidenceAssessment"]])

slots.Premise_wasDerivedFrom = Slot(uri=PROV.wasDerivedFrom, name="Premise_wasDerivedFrom", curie=PROV.curie('wasDerivedFrom'),
                   model_uri=SCIMANTIC.Premise_wasDerivedFrom, domain=Premise, range=Optional[Union[dict, Evidence]])

slots.Dataset_wasGeneratedBy = Slot(uri=PROV.wasGeneratedBy, name="Dataset_wasGeneratedBy", curie=PROV.curie('wasGeneratedBy'),
                   model_uri=SCIMANTIC.Dataset_wasGeneratedBy, domain=Dataset, range=Optional[Union[dict, "Experimentation"]])

slots.Dataset_wasDerivedFrom = Slot(uri=PROV.wasDerivedFrom, name="Dataset_wasDerivedFrom", curie=PROV.curie('wasDerivedFrom'),
                   model_uri=SCIMANTIC.Dataset_wasDerivedFrom, domain=Dataset, range=Optional[Union[dict, ExperimentalMethod]])

slots.Result_wasGeneratedBy = Slot(uri=PROV.wasGeneratedBy, name="Result_wasGeneratedBy", curie=PROV.curie('wasGeneratedBy'),
                   model_uri=SCIMANTIC.Result_wasGeneratedBy, domain=Result, range=Optional[Union[dict, "Analysis"]])

slots.Result_wasDerivedFrom = Slot(uri=PROV.wasDerivedFrom, name="Result_wasDerivedFrom", curie=PROV.curie('wasDerivedFrom'),
                   model_uri=SCIMANTIC.Result_wasDerivedFrom, domain=Result, range=Optional[Union[dict, Dataset]])

slots.Result_refines = Slot(uri=SCIMANTIC.refines, name="Result_refines", curie=SCIMANTIC.curie('refines'),
                   model_uri=SCIMANTIC.Result_refines, domain=Result, range=Optional[Union[dict, Hypothesis]])

slots.Result_supports = Slot(uri=SCIMANTIC.supports, name="Result_supports", curie=SCIMANTIC.curie('supports'),
                   model_uri=SCIMANTIC.Result_supports, domain=Result, range=Optional[Union[dict, Hypothesis]])

slots.Result_contradicts = Slot(uri=SCIMANTIC.contradicts, name="Result_contradicts", curie=SCIMANTIC.curie('contradicts'),
                   model_uri=SCIMANTIC.Result_contradicts, domain=Result, range=Optional[Union[dict, Hypothesis]])

slots.Conclusion_wasGeneratedBy = Slot(uri=PROV.wasGeneratedBy, name="Conclusion_wasGeneratedBy", curie=PROV.curie('wasGeneratedBy'),
                   model_uri=SCIMANTIC.Conclusion_wasGeneratedBy, domain=Conclusion, range=Optional[Union[dict, "ResultAssessment"]])

slots.Conclusion_wasDerivedFrom = Slot(uri=PROV.wasDerivedFrom, name="Conclusion_wasDerivedFrom", curie=PROV.curie('wasDerivedFrom'),
                   model_uri=SCIMANTIC.Conclusion_wasDerivedFrom, domain=Conclusion, range=Optional[Union[dict, Result]])

slots.Annotation_hasTarget = Slot(uri=OA.hasTarget, name="Annotation_hasTarget", curie=OA.curie('hasTarget'),
                   model_uri=SCIMANTIC.Annotation_hasTarget, domain=Annotation, range=str)

slots.Annotation_hasSelector = Slot(uri=OA.hasSelector, name="Annotation_hasSelector", curie=OA.curie('hasSelector'),
                   model_uri=SCIMANTIC.Annotation_hasSelector, domain=Annotation, range=Optional[Union[dict, "TextSelector"]])

slots.Annotation_wasGeneratedBy = Slot(uri=PROV.wasGeneratedBy, name="Annotation_wasGeneratedBy", curie=PROV.curie('wasGeneratedBy'),
                   model_uri=SCIMANTIC.Annotation_wasGeneratedBy, domain=Annotation, range=Optional[Union[dict, LiteratureSearch]])

slots.EvidenceAssessment_used = Slot(uri=PROV.used, name="EvidenceAssessment_used", curie=PROV.curie('used'),
                   model_uri=SCIMANTIC.EvidenceAssessment_used, domain=EvidenceAssessment, range=Optional[Union[dict, Evidence]])

slots.EvidenceAssessment_wasInformedBy = Slot(uri=PROV.wasInformedBy, name="EvidenceAssessment_wasInformedBy", curie=PROV.curie('wasInformedBy'),
                   model_uri=SCIMANTIC.EvidenceAssessment_wasInformedBy, domain=EvidenceAssessment, range=Optional[Union[dict, EvidenceExtraction]])

slots.HypothesisFormation_used = Slot(uri=PROV.used, name="HypothesisFormation_used", curie=PROV.curie('used'),
                   model_uri=SCIMANTIC.HypothesisFormation_used, domain=HypothesisFormation, range=Optional[Union[dict, Premise]])

slots.HypothesisFormation_wasInformedBy = Slot(uri=PROV.wasInformedBy, name="HypothesisFormation_wasInformedBy", curie=PROV.curie('wasInformedBy'),
                   model_uri=SCIMANTIC.HypothesisFormation_wasInformedBy, domain=HypothesisFormation, range=Optional[Union[dict, EvidenceAssessment]])

slots.DesignOfExperiment_used = Slot(uri=PROV.used, name="DesignOfExperiment_used", curie=PROV.curie('used'),
                   model_uri=SCIMANTIC.DesignOfExperiment_used, domain=DesignOfExperiment, range=Optional[str])

slots.DesignOfExperiment_wasInformedBy = Slot(uri=PROV.wasInformedBy, name="DesignOfExperiment_wasInformedBy", curie=PROV.curie('wasInformedBy'),
                   model_uri=SCIMANTIC.DesignOfExperiment_wasInformedBy, domain=DesignOfExperiment, range=Optional[str])

slots.Experimentation_used = Slot(uri=PROV.used, name="Experimentation_used", curie=PROV.curie('used'),
                   model_uri=SCIMANTIC.Experimentation_used, domain=Experimentation, range=Optional[Union[dict, ExperimentalMethod]])

slots.Experimentation_wasInformedBy = Slot(uri=PROV.wasInformedBy, name="Experimentation_wasInformedBy", curie=PROV.curie('wasInformedBy'),
                   model_uri=SCIMANTIC.Experimentation_wasInformedBy, domain=Experimentation, range=Optional[Union[dict, DesignOfExperiment]])

slots.Analysis_used = Slot(uri=PROV.used, name="Analysis_used", curie=PROV.curie('used'),
                   model_uri=SCIMANTIC.Analysis_used, domain=Analysis, range=Optional[Union[dict, Dataset]])

slots.Analysis_wasInformedBy = Slot(uri=PROV.wasInformedBy, name="Analysis_wasInformedBy", curie=PROV.curie('wasInformedBy'),
                   model_uri=SCIMANTIC.Analysis_wasInformedBy, domain=Analysis, range=Optional[Union[dict, Experimentation]])

slots.ResultAssessment_used = Slot(uri=PROV.used, name="ResultAssessment_used", curie=PROV.curie('used'),
                   model_uri=SCIMANTIC.ResultAssessment_used, domain=ResultAssessment, range=Optional[Union[dict, Result]])

slots.ResultAssessment_wasInformedBy = Slot(uri=PROV.wasInformedBy, name="ResultAssessment_wasInformedBy", curie=PROV.curie('wasInformedBy'),
                   model_uri=SCIMANTIC.ResultAssessment_wasInformedBy, domain=ResultAssessment, range=Optional[Union[dict, Analysis]])

slots.UncertaintyModel_natureOfUncertainty = Slot(uri=URREF.natureOfUncertainty, name="UncertaintyModel_natureOfUncertainty", curie=URREF.curie('natureOfUncertainty'),
                   model_uri=SCIMANTIC.UncertaintyModel_natureOfUncertainty, domain=UncertaintyModel, range=Union[str, "UncertaintyNature"])

slots.Ambiguity_natureOfUncertainty = Slot(uri=URREF.natureOfUncertainty, name="Ambiguity_natureOfUncertainty", curie=URREF.curie('natureOfUncertainty'),
                   model_uri=SCIMANTIC.Ambiguity_natureOfUncertainty, domain=Ambiguity, range=Union[str, "UncertaintyNature"])
