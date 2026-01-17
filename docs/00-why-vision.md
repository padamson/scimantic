# Scimantic Vision: Semantic Research from Day One

## Introduction: The Scientific Method as a Provenance Chain

Science advances through a systematic reasoning process - the **scientific method** - that transforms questions into validated knowledge. This process can be represented as a **provenance chain** where each step builds on the previous, with feedback loops enabling iterative refinement.

### The Reasoning Chain: Entities, Activities, and Feedback

The scientific method involves both **things** (questions, evidence, hypotheses, data, results) and **processes** (searching, assessing, designing, executing, analyzing). Following the W3C PROV-O ontology structure, we can map the scientific method to:

- **Entities**: Concrete artifacts of research (Questions, Evidence, Data)
- **Activities**: Processes that create or transform entities (Searching, Experimenting, Analyzing)
- **Agents**: Researchers, AI assistants, and software executing the work

```mermaid
graph TB
    subgraph " "
        direction TB
        subgraph "Entities (Things)"
            Q[Question]
            E[Evidence]
            H[Hypothesis]
            EM[Experimental<br/>Method]
            DS[Dataset]
            R[Result]
        end

        subgraph "Activities (Processes)"
            QF[Question<br/>Formation]
            LS[Literature<br/>Search]
            EA[Evidence<br/>Assessment]
            HF[Hypothesis<br/>Formation]
            DOE[Design Of<br/>Experiment]
            EX[Expertimentation]
            AN[Analysis]
            RA[Result<br/>Assessment]
        end
    end

    QF -.generates.-> Q
    Q -.informs.-> LS
    LS -.generates.-> E
    E -.input to.-> EA
    EA -.may generate.-> Q
    E -.input to.-> HF
    HF -.generates.-> H
    H -.input to.-> DOE
    DOE -.generates.-> EM
    EM -.input to.-> EX
    EX -.generates.-> DS
    DS -.input to.-> AN
    AN -.generates.-> R
    R -.input to.-> RA
    H -.input to.-> RA
    RA -.supports or<br/>contradicts.-> H
    RA -.may generate.-> Q

    style Q fill:#e1f5ff,stroke:#333,stroke-width:2px
    style E fill:#fff4e1,stroke:#333,stroke-width:2px
    style H fill:#ffe1f5,stroke:#333,stroke-width:2px
    style EM fill:#e1ffe1,stroke:#333,stroke-width:2px
    style DS fill:#f5e1ff,stroke:#333,stroke-width:2px
    style R fill:#ffe1e1,stroke:#333,stroke-width:2px
    style QF fill:#f0f0f0,stroke:#666,stroke-width:1px
    style LS fill:#f0f0f0,stroke:#666,stroke-width:1px
    style EA fill:#f0f0f0,stroke:#666,stroke-width:1px
    style HF fill:#f0f0f0,stroke:#666,stroke-width:1px
    style DOE fill:#f0f0f0,stroke:#666,stroke-width:1px
    style EX fill:#f0f0f0,stroke:#666,stroke-width:1px
    style AN fill:#f0f0f0,stroke:#666,stroke-width:1px
    style RA fill:#f0f0f0,stroke:#666,stroke-width:1px
```

**The Flow (with feedback loops):**

1. **Question Formation** (activity) → **Question** (entity): Research begins with a question
   - *Example*: "Can the MQDO method accurately compute differential cross sections for p + ¹²C scattering?"

2. **Literature Search** (activity) → **Evidence** (entity): Extract facts from papers
   - *Example*: "Smith 2023 reports DCS = 150 mb at E = 10 MeV"
   - *Provenance*: Who extracted? From which source? With what uncertainty?

3. **Evidence Assessment** (activity): Evaluate credibility and relevance
   - *Example*: High credibility (peer-reviewed, experimental measurement)
   - *Feedback*: May generate new questions ("What other methods exist?")

4. **Hypothesis Formation** (activity) → **Hypothesis** (entity): Synthesize evidence into testable claims
   - *Example*: "MQDO should predict DCS within 10% error"
   - *Provenance*: Which evidence supports this? What's the uncertainty?

5. **Design of Experiment** (activity) → **ExperimentalMethod** (entity): Specify experimental/computational method
   - *Example*: "Run MQDO code with E = 10 MeV, angular range 0-180°"
   - *Provenance*: Motivated by which hypothesis?

6. **Experimentation** (activity) → **Dataset** (entity): Run experiments/simulations
   - *Example*: MQDO computation produces numerical output
   - *Provenance*: Which code version? What input parameters? Computational environment?

7. **Analysis** (activity) → **Result** (entity): Process data into findings
   - *Example*: "Computed DCS = 148 mb ± 5 mb"
   - *Provenance*: Which analysis script? How was uncertainty calculated?

8. **Result Assessment** (activity): Compare result to hypothesis
   - *Example*: Result supports hypothesis (148 mb vs 150 mb, within error)
   - *Feedback*: May generate new questions ("Why 2 mb difference?")

### The Critical Problem: This Chain is Invisible to Machines

**Today's reality**: This reasoning chain exists only in researchers' heads and narrative text.

- **Lab notebooks**: "We hypothesized X because papers Y and Z suggest..." (unstructured prose)
- **Papers**: Methods sections describe *what* was done, not *why* (hypothesis → design linkage is implicit)
- **Workflow systems**: Track code execution (Nextflow knows which script ran), but not reasoning motivation (Nextflow doesn't know *why* you chose that analysis)
- **AI tools**: Extract facts from papers but output text summaries, not machine-readable provenance

**The consequence**:
- "How did we arrive at this conclusion?" is answerable for humans reading lab notes, but not for machines querying a knowledge graph
- Reproducibility is **computational** (can re-run code) but not **scientific** (can't trace reasoning from evidence to hypothesis to result)
- AI agents start every conversation from scratch—no persistent memory of the research process

### The Scimantic Solution: Machine-Readable Provenance from Day One

**Scimantic makes the entire reasoning chain machine-readable** using W3C standards:

- **W3C PROV-O**: Standard ontology for provenance (entities, activities, agents, relationships)
- **URREF**: Uncertainty representation (epistemic vs aleatory, ambiguity vs incompleteness)
- **Nanopublications**: Atomic publishable units with assertion + provenance + metadata
- **PROV-K**: Discourse extensions (supports, contradicts, refines relationships)

**Every stage becomes RDF**:
- Question → `scimantic:Question` entity with `rdfs:label`
- Literature search → `scimantic:LiteratureSearch` activity with `prov:used` (source DOI), `prov:wasAssociatedWith` (researcher/AI)
- Evidence → `scimantic:Evidence` entity with `prov:wasGeneratedBy` (search activity), `prov:wasQuotedFrom` (source), `scimantic:hasUncertainty` (URREF entity)
- Hypothesis → `scimantic:Hypothesis` entity with `prov:wasDerivedFrom` (evidence), uncertainty propagation
- ... (continues through all stages)

**The result**: A unified knowledge graph where queries can answer:
- "What evidence supports hypothesis X?" → Traverse the chain of support
- "Which experiments tested this hypothesis?" → Find experimental methods designed for the hypothesis
- "How was this result computed?" → Trace the analysis back to code and data
- "What's the uncertainty?" → Propagate uncertainty from evidence through the reasoning chain

### Why This Matters

**For researchers**:
- Lab notebook is a **queryable knowledge graph**, not scattered notes
- Literature review creates **persistent semantic annotations** (evidence nanopublications), not ephemeral highlights
- Hypothesis reasoning is **traceable and verifiable**, not lost after the paper is written

**For AI agents**:
- **Persistent memory**: All research artifacts stored as RDF, survives beyond single conversations
- **Collaborative research**: AI can propose hypotheses by querying evidence patterns, human validates
- **Smart assistants**: "What contradicts my hypothesis?" → AI queries PROV-K `contradicts` relations

**For science**:
- **Reproducibility by design**: Complete provenance from question → result, not just final methods
- **Living knowledge graphs**: Research builds on federated semantic graphs, not isolated PDFs
- **Transparent reasoning**: Hypothesis formation is computable, not narrative handwaving

The rest of this document shows how existing tools address *parts* of this vision (literature extraction, workflow provenance, semantic publishing) and where **Scimantic fills the gaps** by integrating all stages into a unified, standards-based semantic framework.

---

## The State of the Art: Tools for Individual Stages

The scientific community has built impressive tools for **individual stages** of the reasoning chain. However, these tools operate in isolation, without machine-readable connections between stages.

### Mapping Existing Tools to the Reasoning Chain

#### Stage 1-2: Question Formation & Literature Search

**What exists:**
- **Semantic Scholar**: 225M+ papers with structured metadata, natural language summaries, API access
- **AI extraction tools**: Elicit (99.4% extraction accuracy), Scite (citation context), Consensus (evidence summaries)
- **Citation graphs**: ResearchRabbit, Connected Papers, Litmaps for visual discovery
- **Reference managers**: Zotero with PDF annotation extraction, MCP integration for AI search

**What's missing:**
- Tools output **text**, not RDF entities
- No provenance linking Question → LiteratureSearch activity → Evidence entity
- AI extractions lost after conversation ends (no persistent graph)

#### Stage 3: Evidence Assessment & Hypothesis Formation

**What exists:**
- **Electronic Lab Notebooks**: 35% institutional adoption, 58% with AI features for structured data entry
- **Discourse ontologies**: AIDA principles (Atomic, Independent, Declarative, Absolute), argumentation models
- **PROV-K**: Support/conflict relations for evidence linkage with certainty degrees

**What's missing:**
- Evidence assessment is **narrative** ("this paper is credible because..."), not computable
- Hypothesis formation is **undocumented** - no provenance linking Evidence → Hypothesis
- Can't query "which evidence supports hypothesis X?" (relationship is implicit in text)

#### Stage 4-5: Design of Experiment & Experimentation

**What exists:**
- **Workflow systems**: Nextflow (dominant, 24% of WorkflowHub), Snakemake, Galaxy, CWL track execution
- **W3C PROV-O**: yProv ecosystem, Python prov package capture computational provenance
- **Containerization**: Docker ensures reproducible execution environments
- **Code Ocean**: Integrated into Nature peer review for computational reproducibility

**What's missing:**
- ExperimentalMethod → Hypothesis linkage is **absent** (workflows don't know *why* they exist)
- Experimentation provenance is **computational** only (which script ran), not **scientific** (which hypothesis motivated it)
- Can't query "which experiments tested this hypothesis?"

#### Stage 6-7: Analysis & Result Assessment

**What exists:**
- **Jupyter provenance**: ProvBook, MLProvLab extensions (though only 8.5% fully reproducible)
- **Research compendia**: Quarto (next-gen R Markdown), targets package for literate programming
- **FAIR principles**: 35% institutional adoption, NIH Strategic Plan 2025-2030 priority

**What's missing:**
- Result → Hypothesis comparison is **implicit** (discussed in text, not RDF)
- No `prov:supports` or `prov:contradicts` relations linking Result to Hypothesis
- Assessment activities don't generate new Questions (feedback loop is manual)

### Cross-Cutting Infrastructure (All Stages)

**What exists:**
- **RDF/Linked Data**: Life sciences maturity (UniProt, ChEBI, Gene Ontology, Reactome, Ensembl with SPARQL endpoints)
- **Nanopublications**: Nanopub.net servers with Trusty URIs for verifiable, immutable assertions
  - Active in biomedical ontologies, biodiversity data, FAIR Supporting Resources
  - Growing adoption: ESWC 2025 tutorial, Knowledge Pixels managed services
- **W3C Standards**: PROV-O, FOAF (agents), DC Terms (metadata), SKOS (taxonomies), OWL (reasoning)
- **URREF**: Uncertainty Representation and Reasoning Evaluation Framework ontology
  - Uncertainty types: Ambiguity, randomness, vagueness, inconsistency, incompleteness
  - Uncertainty nature: Aleatory (inherent) vs. epistemic (knowledge gaps)
  - Information fusion methods: Dempster-Shafer, belief entropy, credibility weighting
- **Model Context Protocol (MCP)**: Emerging standard (1-year anniversary Nov 2025)
  - Berkeley Lab pilots for cross-division data access
  - Healthcare/life sciences processing hundreds of thousands of data points

**What's missing:**
- Infrastructure exists, but **no tool uses it end-to-end** for the full reasoning chain
- RDF is siloed in final publications (nanopubs), not used **from day one** of research
- URREF defines uncertainty, but researchers store it as **narrative text**, not RDF entities
- MCP integrations produce text summaries, not persistent RDF graphs

### Summary: Strong Foundations, Missing Integration

**What's working:**
- Robust tools for **individual stages** (Semantic Scholar for literature, Nextflow for execution, Jupyter for analysis)
- Solid **semantic web standards** (PROV-O, URREF, Nanopublications, FOAF, DC Terms, PROV-K)
- Growing **AI integration** via MCP for tool access
- Domain-specific RDF in life sciences (UniProt, GO, ChEBI with SPARQL endpoints)

**What's broken:**
- **No end-to-end integration**: Tools operate in isolation, no machine-readable connections between stages
- **Entity chains invisible**: The links between Question, Evidence, Hypothesis, Method, Data, and Result exist only in researchers' heads, not as a traceable graph.
- **Activities undocumented**: Key steps like Literature Search, Assessment, and Hypothesis Formation happen but aren't captured as structural activities.
- **Feedback loops missing**: Assessment doesn't seamlessly generate new Questions; contradictory evidence doesn't formally link to the Hypothesis it challenges.
- **Uncertainty as text**: Uncertainty is written as "high confidence" text rather than structured data that can be computed.
- **Semantic publishing post-hoc**: Structured data is created only *after* research is done, not as a natural byproduct of the process.
- **No persistent AI memory**: AI extractions produce text summaries, not structured entities in a shared knowledge graph.
- **Domain gap**: Strong in life sciences (biology, medicine), weak in physical sciences (physics, chemistry, engineering)

---

## The Scimantic Solution

Scimantic **builds on existing tools** (Semantic Scholar, Elicit, Nextflow, PROV-O, nanopub.net) to create a unified semantic workflow where **research reasoning** is machine-readable from inception.

### How Scimantic Builds on Standards and Open Ecosystems

**Scimantic is built on W3C and community standards**, not proprietary tools or schemas:

**Ontology Foundation**:
- **W3C PROV-O**: Complete provenance vocabulary (`prov:Entity`, `prov:Activity`, `prov:Agent`, `prov:wasDerivedFrom`, `prov:wasGeneratedBy`)
- **URREF**: Draft international standard for uncertainty representation (`urref:AleatoricUncertainty`, `urref:EpistemicUncertainty`, uncertainty types)
- **Nanopublication schema**: Trusty URIs, assertion/provenance/pubinfo structure
- **FOAF**: Agent representation (`foaf:Person`, `foaf:Organization`)
- **DC Terms**: Metadata (`dcterms:created`, `dcterms:creator`, `dcterms:source`)
- **PROV-K**: Discourse ontology patterns for scientific argumentation (`prov:supports`, `prov:contradicts`)
- **AIDA principles**: Atomic, Independent, Declarative, Absolute nanopublication guidelines

**Development Environment**:
- **VS Code extension**: Knowledge graph visualization, nanopub editing, provenance navigation
- **MCP integration**: AI agents (e.g., Claude Code, compatible LLMs) access knowledge graph via Model Context Protocol (MCP)
- **RDFLib**: Python library for RDF manipulation, SPARQL queries, Turtle serialization
- **Existing workflow systems**: Nextflow, Snakemake, Jupyter (decorated with PROV-O tracking, not replaced)

**Scimantic provides the integration layer** that transforms these standards into a seamless research workflow:

1.  **First-Class Research Objects**: We treat questions, evidence, hypotheses, and methods as distinct, structured data objects, not just text in a document.
2.  **Explicit Relationships**: We capture the semantic connections between these objects—knowing *why* an experiment was run (to test a specific hypothesis) or *why* a hypothesis was formed (based on specific evidence).
3.  **Standardized Provenance**: As you work, the system records every action using the W3C PROV standard, creating an immutable history of the research process.
4.  **Integrated Uncertainty**: We don't just record values; we record the uncertainty and confidence associated with every piece of evidence and every result.
5.  **AI Compatibility**: By structuring research as a knowledge graph, we provide AI agents with a "persistent memory" and a structured way to reason about science, enabling true collaboration.

### How It Works: Semantic-First Research

Scimantic integrates into the researcher's workflow at every stage of the reasoning chain, capturing entities and activities as RDF through human-AI interaction:

**1. Semantic from Day One**
- **Literature extraction** creates structured Evidence objects, not just text notes.
- **Hypothesis formation** creates Hypothesis objects linked directly to the supporting Evidence.
- **Experimental design** creates Method objects linked to the Hypotheses they test.
- This happens seamlessly in the background, building a queryable graph as you work.

**2. Complete Provenance Chains**
- Every entity traces back through the reasoning chain: `Result` → `Analysis` → `Dataset` → `Experimentation` → `Method` → `Hypothesis` → `Evidence` → `Source`.
- The system captures **why** things happened, not just **what** happened.

**3. Seamless Publishing**
- Research actions are formatted as standard "Nanopublications"—atomic, citable units of knowledge.
- These can be shared internally or published globally without extra effort.

**4. AI Persistent Memory**
- AI agents access this shared knowledge graph. They don't start from scratch; they know what you've read, what you've hypothesized, and what you've tested.
- Collaboration becomes meaningful: AI can suggest hypotheses based on your evidence or identify contradictions in your results.

**5. Quantitative Uncertainty**
- Uncertainty is treated as data. If your evidence is 80% confident, the system helps propagate that uncertainty to your hypotheses and results.

**6. Iterative Refinement**
- The system naturally tracks feedback loops: evaluating evidence can trigger new questions, and analyzing results can refine hypotheses.

**7. Selective Subset Publishing**
- Maintain **one comprehensive private master KG** (your complete research database).
- Generate **curated subsets** for specific purposes (paper supplements, grant proposals, collaboration).
- Publish subsets to **multiple destinations**: nanopub servers, GitHub Pages, scimantic.io, institutional repos.
- License-based management ensures publishable entities are included, proprietary data excluded.
- Subsets are **generated from queries**, not edited directly—perfect provenance and reproducibility.

**Key Differentiator:** Other tools capture *what happened* (code ran, data produced). Scimantic captures *why it happened* (hypothesis motivated experiment, evidence supported hypothesis). The reasoning chain becomes a queryable knowledge graph, not narrative text.

---

## Next Steps

This vision document establishes **why** Scimantic exists and the value it delivers. For implementation details:

- **Technical Architecture** (WHAT we're building): See [the architecture](./01-what-architecture.md)
- **Implementation Roadmap** (WHEN we build capabilities): See [the roadmap](./02-when-roadmap.md)
- **Specifications, Code, & Tests** (HOW it works): See [specifications](./03-how-specifications/), `scimantic-core`, and `scimantic-ext`
- **Feature Specifications** (vertical slices): See [features](./features/)
