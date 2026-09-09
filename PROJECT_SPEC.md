# ROLE AND OBJECTIVE

Act as the lead consultant, senior data analyst, data engineer, Power BI developer, operational-service analyst and final quality reviewer for this project.

Your task is to BUILD, VERIFY AND PACKAGE a finished portfolio project titled:

# GB Settlement & Imbalance Service Intelligence Monitor

This is an independent portfolio project being created specifically to strengthen an application for:

**Elexon — Service Analyst, Settlement & Insight**

The objective is not merely to make an electricity-market dashboard.

The objective is to demonstrate the behaviours Elexon is seeking in the Service Analyst vacancy:

- analytical investigation;
- data visualisation;
- root-cause discipline;
- service-performance monitoring;
- data validation and accuracy;
- operational-risk awareness;
- reporting and commentary;
- SQL;
- Power BI;
- Excel/data discipline;
- stakeholder communication;
- process improvement;
- issue ownership;
- rapid learning of the Balancing and Settlement Code and GB electricity market.

Complete the project end to end.

Do not stop after providing a plan.

Do not merely tell me how I could build it.

Build the actual project and its final deliverables.

---

# AUTONOMY AND FOLLOW-THROUGH

Bias towards action and carry the intended task to completion.

Treat this prompt as authorisation to perform all reversible, read-only, analytical, coding, file-creation, local-project, browser-research and report-authoring actions needed to complete the project.

Do not stop for routine clarification.

When information is missing but a reasonable reversible decision can be made:

1. investigate;
2. choose the best supported option;
3. record the decision in `DECISIONS.md`;
4. continue.

Ask me only when:

- credentials/authentication require my intervention;
- an irreversible external action needs approval;
- a consequential decision genuinely cannot be inferred from this specification or authoritative sources.

If such a blocker occurs, complete every unaffected part of the project before requesting intervention.

Do not settle for a partial solution merely to save time, tokens or effort.

Persist until the intended deliverables are complete or genuinely blocked.

---

# PARALLEL EXECUTION

Use subagents or parallel work whenever independent tasks can be performed concurrently and doing so saves time or improves quality.

Suitable parallel tracks include:

- Elexon/BSC domain research;
- current API discovery;
- Power BI architecture;
- data-quality design;
- SOTA benchmark review;
- analytical methodology;
- presentation planning;
- independent QA.

The root agent remains responsible for reconciling all delegated outputs and ensuring they agree with authoritative documentation.

Do not accept subagent conclusions without verification.

---

# INSTRUCTION PRIORITY

The requirements in this project specification are authoritative for this task.

Skills and MCP instructions should be followed where technically required.

If an installed skill causes you to stop, request unnecessary confirmation, or diverge from the intended one-shot execution:

- identify the exact skill;
- identify the relevant requirement;
- distinguish a hard technical requirement from advisory workflow guidance;
- continue by another valid route where possible.

Do not silently abandon the project because a preferred skill or MCP is unavailable.

---

# SOURCE OF TRUTH

Use this hierarchy:

1. Official Elexon documentation.
2. Official BSC documentation.
3. Official Elexon Insights Solution APIs and developer documentation.
4. Official Microsoft Power BI / Fabric documentation.
5. Primary documentation for any technical library used.
6. Reputable public open-source projects for architecture/design benchmarking only.
7. Other sources only for secondary context.

If another source contradicts Elexon on GB electricity settlement concepts, Elexon wins.

Never infer market definitions from GitHub code when official Elexon documentation exists.

Maintain a complete `SOURCES.md`.

Every material domain claim in the final project must trace to a source.

---

# BENCHMARK BEFORE BUILDING

Before deciding that the analytical design is adequate, benchmark against:

## Elexon System Prices Analysis Report / current equivalent

Understand what Elexon already analyses, including where available:

- System Prices;
- short vs long market conditions;
- distributional statistics;
- daily behaviour;
- Settlement Period patterns;
- Net Imbalance Volume;
- System Price vs NIV relationships;
- extreme periods;
- price-calculation context.

Do not present analyses Elexon already publishes as the main innovation of this project.

They are baseline analytical competence.

## Strong public GB-power analytics repositories

Review current high-quality public GB electricity-market projects and identify useful standards for:

- reproducibility;
- provenance;
- data validation;
- methodology;
- handling of derived values;
- handling of assumptions;
- documentation;
- dashboard UX.

Do not copy their code or visual identity.

Use them as quality benchmarks.

---

# CORE PROJECT DIFFERENTIATION

The project must demonstrate:

# CONTROL → DETECT → INVESTIGATE → COMMUNICATE → RECOMMEND

The primary value is not predicting electricity prices.

The primary value is demonstrating how a Service Analyst could:

1. establish whether data/service behaviour is normal;
2. identify unusual Settlement Periods or data-quality exceptions;
3. investigate available evidence;
4. separate observed evidence from derived calculations and hypotheses;
5. communicate what is known and unknown;
6. recommend the next appropriate analytical check.

---

# INTEGRITY / PROVENANCE MODEL

Use these explicit evidence classes throughout the project:

**OBSERVED**
Directly returned by an authoritative source.

**DERIVED**
Calculated deterministically from observed data.

**FLAG**
An analytically generated exception or threshold result.

**HYPOTHESIS**
A possible explanation that has not been established by available evidence.

Never silently convert a HYPOTHESIS into an OBSERVED fact.

Never claim causality from correlation alone.

Where practical, encode provenance in data/model metadata rather than only describing it in prose.

---

# PROJECT DIRECTORY

Create approximately:

elexon-service-intelligence/
├── AGENTS.md
├── PROJECT_SPEC.md
├── PROJECT_STATE.md
├── DECISIONS.md
├── SOURCES.md
├── METHODOLOGY.md
├── README.md
├── requirements.txt
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── quality/
│   └── README.md
│
├── src/
│   ├── ingest/
│   ├── transform/
│   ├── validate/
│   └── analysis/
│
├── sql/
│   └── analysis.sql
│
├── powerbi/
│   └── project/
│
├── reports/
│   ├── service-insight-note.pdf
│   └── presentation/
│
├── screenshots/
│
└── tests/

Modify the structure if a materially better implementation requires it, but keep clear separation between raw data, transformed data, analysis, BI artifacts, documentation and presentation assets.

---

# STATE PERSISTENCE

Create `PROJECT_STATE.md` immediately.

Update it after every material phase.

It must always contain:

- objective;
- completed work;
- current work;
- outstanding work;
- important findings;
- decisions made;
- known issues;
- blockers;
- important file paths;
- exact commands needed to reproduce the current state;
- next recommended action.

This file must enable another capable agent with zero chat history to continue the project.

Also maintain `DECISIONS.md`.

Record meaningful decisions including:

- date window;
- datasets selected;
- transformations;
- threshold methodology;
- model design;
- rejected alternatives;
- report architecture;
- presentation decisions;
- limitations.

If model or usage limits become imminent, prioritise updating these files before interruption.

---

# AGENTS.MD

Create a concise `AGENTS.md` containing persistent project rules.

At minimum:

ELEXON OFFICIAL DOCUMENTATION IS THE DOMAIN SOURCE OF TRUTH.

Never fabricate data.

Never fabricate project results.

Never claim causality without supporting evidence.

Never convert a hypothesis into a confirmed finding.

Keep raw and processed data separate.

Use interview-defensible code.

Prefer analytical clarity and reproducibility over unnecessary technical complexity.

Record meaningful assumptions.

Validate important calculations independently.

Update PROJECT_STATE.md after each major phase.

Never claim a deliverable exists until it has been produced and verified.

---

# DOMAIN LEARNING

Before interpreting results, understand enough of the Elexon/BSC environment to explain correctly:

- Elexon's role;
- Balancing and Settlement Code at a high level;
- Settlement Day;
- Settlement Period;
- System Price;
- System Buy Price / System Sell Price terminology where applicable;
- Net Imbalance Volume;
- system short;
- system long;
- imbalance settlement at a high level;
- indicative/current versus subsequently refreshed or settled data;
- relevant time conventions;
- clock-change implications.

The project is not expected to reproduce the entire BSC.

Learn only the parts required to analyse and explain the project accurately.

Document essential definitions and sources in `METHODOLOGY.md`.

---

# DATA ACQUISITION

Use current official Elexon Insights Solution APIs.

Confirm endpoint names and schemas from current official documentation.

Do not guess endpoint URLs based on old BMRS libraries or historic blog posts.

Do not scrape the Elexon website when an API exists.

Use real production data.

Choose a historical analysis window that is:

- long enough to show meaningful variation;
- manageable;
- reproducible;
- analytically defensible.

Choose the exact period after inspecting data availability and record the rationale in `DECISIONS.md`.

At minimum obtain the data required for:

- Settlement Date;
- Settlement Period;
- System Price;
- Net Imbalance Volume.

Preserve:

- original source values;
- retrieval timestamps;
- source endpoint;
- raw response/data.

For selected unusual periods, investigate whether additional official Elexon datasets materially improve explanation, such as:

- detailed System Price calculation;
- accepted balancing actions;
- balancing-service adjustment actions;
- relevant demand/generation context;
- other authoritative contextual series.

Do not indiscriminately ingest every available Elexon dataset.

Add additional data only where it improves investigation quality.

---

# RAW DATA POLICY

Raw source data must remain immutable after retrieval.

Transformations belong in processed layers.

Do not manually alter raw source records.

If an API returns revised observations over time, document the revision behaviour.

---

# DATA-QUALITY FRAMEWORK

Build explicit, executable controls for:

- HTTP/API failures;
- retries where appropriate;
- empty responses;
- malformed responses;
- schema changes;
- missing expected columns;
- invalid data types;
- invalid numeric values;
- null values;
- duplicate records;
- duplicate Settlement Date × Settlement Period keys;
- unexpected Settlement Period coverage;
- stale data;
- retrieval failures;
- timestamp/time-zone inconsistencies.

Handle GB clock-change behaviour correctly.

Do NOT encode:

`expected periods = 48`

as a universal rule.

Correctly handle days where clock changes alter the number of Settlement Periods.

Produce:

`data/quality/exceptions.*`

containing machine-readable quality exceptions.

Create an audit-friendly summary of all controls.

---

# ANALYTICAL QUESTIONS

At minimum answer:

1. When were the largest absolute system imbalances?
2. When were the highest and lowest System Prices?
3. How do short and long system conditions differ?
4. What relationship is observable between NIV direction/magnitude and System Price?
5. What intraday/Settlement-Period patterns are visible?
6. Which observations are statistically unusual?
7. Which unusual Settlement Periods warrant deeper investigation?
8. Were any apparent anomalies actually data-quality problems?
9. What additional evidence would be required to explain the strongest exceptions?
10. What can and cannot legitimately be concluded from the available evidence?

---

# BASELINE ELEXON-LEVEL ANALYSIS

Implement enough baseline analysis to demonstrate domain competence.

Where supported by the data, include:

- count;
- mean;
- median;
- standard deviation;
- min/max;
- appropriate percentiles;
- short vs long comparison;
- System Price distribution;
- intraday pattern by Settlement Period;
- daily pattern where meaningful;
- NIV distribution;
- NIV vs System Price relationship;
- extreme-period table.

Do not confuse this baseline with the project's differentiating contribution.

---

# EXCEPTION DETECTION

Use simple, explainable and defensible techniques.

Prefer:

- percentile thresholds;
- IQR;
- Median Absolute Deviation;
- other robust descriptive approaches.

Avoid adding sophisticated machine learning merely to make the project appear advanced.

Do not use neural networks, Isolation Forest, LSTM or other complex anomaly detection unless analysis demonstrates a genuine need and the method materially improves the result.

Any threshold must be:

- derived from the data;
- supported by authoritative rules; or
- explicitly justified.

Never invent a threshold because a dashboard requires one.

---

# INVESTIGATION FRAMEWORK

Implement a structured investigation workflow.

## LEVEL 1 — DETECTION

Use:

- System Price;
- NIV;
- Settlement Period;
- system length;
- historical percentile / robust anomaly score;
- data-quality status.

Purpose:

determine whether something unusual occurred.

## LEVEL 2 — CONTEXT

Where warranted, inspect:

- relevant demand context;
- generation context;
- balancing volumes;
- other available official market context.

Purpose:

form plausible hypotheses.

## LEVEL 3 — PRICE / BALANCING EVIDENCE

For the most material cases, where available, inspect official detailed price/balancing data.

Purpose:

determine whether stronger evidence supports or rejects a hypothesis.

Do not skip directly from Level 1 detection to a causal claim.

---

# SERVICE-ANALYST EXCEPTION RECORD

For each selected high-value exception, create a structured record containing:

- Settlement Date;
- Settlement Period;
- System Price;
- NIV;
- system length;
- price percentile;
- |NIV| percentile;
- quality-control result;
- reason flagged;
- evidence available;
- what is known;
- what is not established;
- possible hypotheses;
- recommended next checks;
- investigation status.

This should become the conceptual core of the project.

---

# SQL

Create clear SQL analysis demonstrating genuine capability.

SQL must perform meaningful analytical work rather than existing simply to put “SQL” on a CV.

Include queries such as, where appropriate:

- highest/lowest prices;
- largest |NIV|;
- daily summaries;
- Settlement-Period summaries;
- short vs long comparisons;
- exception selection;
- data-quality checks.

Keep queries understandable to an early-career analyst.

Use appropriate CTEs/window functions only where they improve clarity.

Comment non-obvious logic.

---

# PYTHON / ENGINEERING STANDARD

Keep the engineering professional but restrained.

Use:

- modular functions;
- clear names;
- type hints where useful;
- appropriate logging;
- sensible error handling;
- configuration rather than repeated magic values;
- deterministic transformations;
- reproducible commands.

Do NOT add unnecessary:

- microservices;
- Kubernetes;
- Kafka;
- Airflow;
- dbt;
- Spark;
- cloud infrastructure;
- message queues;
- databases;
- machine-learning pipelines.

unless a genuine requirement emerges.

The candidate must be able to explain the code in an interview.

---

# POWER BI TOOL PRE-FLIGHT

Inspect the environment before Power BI implementation.

Look for Microsoft's current official Power BI agentic stack.

Preferred structured tools:

- `semantic-model-authoring`
- `powerbi-report-design`
- `powerbi-report-authoring`
- `powerbi-report-management` if publishing is needed
- Power BI Modeling MCP server

Do NOT use `powerbi-report-planning` merely to recreate requirements gathering. This specification already defines the report requirements.

If Power BI agentic tools are not installed:

1. inspect Microsoft's current official installation instructions;
2. use the supported Codex-compatible setup where practical;
3. do not invent installation steps.

If structured Power BI tooling becomes a disproportionate setup burden, switch to the fastest valid implementation route.

Do not allow Power BI tooling installation to become the project.

---

# POWER BI FALLBACK POLICY

Preferred route:

Power BI agentic skills + Modeling MCP.

If unavailable:

Fabric / Power BI Service + browser/computer use.

If Windows + Power BI Desktop is available:

use Desktop/PBIP/PBIR and Desktop verification where beneficial.

If macOS prevents Desktop usage:

do not stop the project.

Use available Fabric/Power BI web authoring, PBIR/PBIP tooling and browser rendering instead.

Record any limitation in PROJECT_STATE.md.

---

# POWER BI SEMANTIC MODEL

Use an appropriate star-schema-style model rather than an uncontrolled flat-table report.

A suitable conceptual design may include:

DIM_DATE

DIM_SETTLEMENT_PERIOD

FACT_SETTLEMENT

FACT_DATA_QUALITY

and only additional dimensions/facts that materially improve the report.

Do not over-model the dataset.

Define explicit measures.

Every important measure should have:

- clear name;
- definition;
- unit;
- purpose;
- correct formatting.

Candidate measures may include:

Average System Price

Median System Price

Maximum System Price

Minimum System Price

Average Absolute NIV

Maximum Absolute NIV

Short Settlement Periods

Long Settlement Periods

Extreme Price Periods

Extreme Imbalance Periods

Data Completeness %

Missing Settlement Periods

Duplicate Settlement Periods

Validation Exceptions

Do not create measures that do not serve a report question.

---

# CROSS-SYSTEM VALIDATION

Material numbers shown in Power BI must be cross-checked against Python and/or SQL.

Examples:

- record counts;
- maximum price;
- median price;
- maximum |NIV|;
- exception count;
- completeness;
- short/long count.

Do not trust a DAX measure merely because it renders.

---

# POWER BI REPORT

Build FOUR purposeful pages.

Use professional operational analytics design.

Default to approximately 16:9 / 1920×1080-style composition where supported.

Use a consistent grid.

No decorative SaaS-dashboard styling.

Avoid:

- gradients;
- glowing elements;
- giant rounded cards;
- excessive icons;
- gauge charts;
- meaningless donut charts;
- unnecessary colour;
- clutter.

Use colour sparingly and consistently.

Prioritise:

- hierarchy;
- information density;
- readability;
- analytical clarity;
- accessibility.

---

# POWER BI PAGE 1 — SETTLEMENT SERVICE MONITOR

Archetype:

OPERATIONAL MONITOR.

Primary question:

“Is the monitored data/service behaving normally and what currently requires attention?”

Include an appropriate top status band with items such as:

- data through;
- service/data status;
- completeness;
- active analytical exceptions.

Include only useful KPIs.

Provide aligned System Price and NIV time views.

Avoid misleading dual-axis presentation where separate aligned charts are clearer.

Include an operational exception queue.

Example columns:

Date

Settlement Period

System Length

NIV

System Price

Flag

Severity

Quality Status

The page should feel analyst-operated rather than decorative.

---

# POWER BI PAGE 2 — MARKET & SETTLEMENT ANALYSIS

Archetype:

ANALYTICAL CANVAS.

Use this page for analytical exploration.

Where supported include:

- short vs long price comparison;
- price distributions;
- average price by Settlement Period;
- NIV distribution;
- NIV versus System Price;
- historical percentile/context.

Use slicers only where useful.

Do not overload the page.

---

# POWER BI PAGE 3 — EXCEPTION INVESTIGATION

Archetype:

INVESTIGATION / NARRATIVE DRILL.

Allow selection of a flagged Settlement Period.

Display:

EVENT

WHAT HAPPENED

WHY IT WAS FLAGGED

DATA QUALITY

KNOWN

NOT ESTABLISHED

HYPOTHESES

RECOMMENDED NEXT CHECKS

Use contextual visuals where helpful.

This is the project's most important Service Analyst page.

The difference between KNOWN and NOT ESTABLISHED must be visually obvious.

Never imply a causal explanation merely because two variables moved together.

---

# POWER BI PAGE 4 — DATA QUALITY & CONTROLS

Archetype:

CONTROL MONITOR.

Include:

- API/data retrieval status;
- records expected;
- records received;
- completeness;
- duplicates;
- null values;
- schema exceptions;
- clock-change handling;
- retrieval timestamp;
- validation status.

Include an audit-friendly validation table/log.

The page should demonstrate the same control mindset required for operational settlement data.

---

# ACCESSIBILITY / DESIGN QA

Check:

- contrast;
- font sizes;
- meaningful titles;
- units;
- alignment;
- whitespace;
- chart sorting;
- data labels;
- legends;
- colour consistency;
- accessibility independent of colour alone;
- slicer consistency;
- clipping;
- empty states;
- responsive behaviour where relevant.

Use restrained professional styling.

---

# PERFORMANCE QA

Where Power BI tooling permits:

run Performance Analyzer or equivalent inspection.

Look for obviously disproportionate visual/query load times.

Optimise only where needed.

Do not prematurely engineer for enterprise-scale performance.

---

# METHODOLOGY.MD

Create a high-quality methodology document.

Include:

- project scope;
- sources;
- field definitions;
- units;
- timestamps;
- System Price definition;
- NIV definition;
- system short/long interpretation;
- raw vs processed data;
- OBSERVED / DERIVED / FLAG / HYPOTHESIS framework;
- transformations;
- threshold methodology;
- revision/timeliness considerations;
- Settlement Period coverage;
- clock-change logic;
- analytical assumptions;
- limitations;
- important judgement calls;
- validation rules.

Treat `METHODOLOGY.md` as a canonical reviewer document, not an afterthought.

---

# README

Create a polished case-study README.

The first screen should allow a recruiter to understand the project quickly.

Include:

# GB Settlement & Imbalance Service Intelligence Monitor

Short description:

An independent operational analytics project using public Elexon data to validate Settlement Period information, identify unusual market conditions and structure evidence-led investigation.

Then show:

- hero dashboard screenshot;
- problem;
- why it matters;
- solution;
- architecture;
- key controls;
- key analytical findings;
- exception-investigation example;
- Power BI screenshots;
- methodology;
- limitations;
- repository structure;
- reproduction steps;
- source links.

Clearly state:

**This is an independent portfolio project and is not affiliated with or endorsed by Elexon.**

Do not make marketing claims unsupported by the project.

---

# SERVICE INSIGHT NOTE

Create:

`reports/service-insight-note.pdf`

One page.

Professional internal-analyst style.

Title:

# Service Insight Note — GB Imbalance & System Price Monitoring

Include:

ANALYTICAL QUESTION

DATA / SOURCE

SERVICE / DATA STATUS

KEY FINDINGS

MATERIAL EXCEPTION

WHAT IS KNOWN

WHAT IS NOT ESTABLISHED

RECOMMENDED NEXT CHECKS

LIMITATIONS

Write in clear plain English suitable for an internal stakeholder.

No unnecessary technical detail.

No unsupported causality.

---

# PRESENTATION — FIRST-CLASS DELIVERABLE

Create a polished approximately 8-slide presentation.

Do NOT treat presentation creation as a final formatting task.

The deck must communicate the analytical story independently of the repository.

Use decision-oriented titles.

Use real project charts, diagrams, dashboard screenshots and results.

Do not fill slides with text.

Do not use decorative stock imagery unless there is a compelling reason.

Use a restrained analytical / regulatory / professional style.

The deck should be suitable for an Elexon hiring manager or analytical panel.

Recommended narrative:

## SLIDE 1

Settlement services depend on accurate half-hourly data and disciplined exception investigation

Explain the problem in one visual workflow:

Elexon data
→ Validation
→ Monitoring
→ Exception
→ Investigation
→ Resolution / escalation

## SLIDE 2

The monitor turns public Elexon data into a controlled analytical workflow

Show architecture:

Elexon Insights API
→ immutable raw layer
→ validation
→ processed data / SQL
→ semantic model
→ Power BI
→ investigation / reporting

## SLIDE 3

Data is validated before analytical conclusions are produced

Show major controls:

completeness

duplicates

nulls

schema

Settlement Period coverage

clock changes

retrieval/revision status

Use actual pass/fail results.

## SLIDE 4

Present the strongest real market/settlement analytical finding

Use actual project results.

Potential structure:

short vs long behaviour;

distribution;

intraday pattern;

or another stronger supported finding.

Do not decide the conclusion before analysing the data.

## SLIDE 5

Show the real exception population

Use actual thresholds/results.

Display an exception queue or concise summary.

Highlight one selected case.

## SLIDE 6

The selected period is unusual, but evidence must be separated from explanation

Two-column structure:

KNOWN

versus

NOT ESTABLISHED

Show supporting evidence and context.

This slide should demonstrate analytical judgement.

## SLIDE 7

Recommended next checks prioritise evidence before escalation

Show a concise evidence ladder.

For example, where appropriate:

detailed price stack

balancing actions

demand/generation context

service/data incident context

additional verification

Do not present these as Elexon's official internal procedure unless documented.

## SLIDE 8

The project demonstrates the core behaviours required of a Service Analyst

Map:

ELEXON REQUIREMENT → PROJECT EVIDENCE

Examples:

Data analysis → Python / SQL / Power BI

Data validation → automated controls

Issue investigation → exception workflow

Reporting → dashboard + insight note

Communication → known / unknown / next-action structure

Process improvement → repeatable monitor

Market learning → real Elexon settlement analysis

Add repository/report links.

---

# PRESENTATION DESIGN

Use consistent visual language with Power BI.

Prefer:

- white / light neutral background;
- near-black typography;
- restrained accent colours;
- strong grid;
- crisp charts;
- clear hierarchy;
- generous but intentional whitespace.

No:

- gradients;
- glossy corporate imagery;
- abstract AI artwork;
- decorative icons everywhere;
- rounded-card overload;
- meaningless animations.

Add small source references on slides containing externally sourced context.

The deck must remain understandable when exported to PDF.

Create both an editable presentation format where possible and PDF export.

---

# PRESENTATION QA

Inspect every slide visually.

Check:

- clipping;
- font size;
- alignment;
- source placement;
- chart legibility;
- titles;
- page density;
- consistency;
- narrative flow;
- factual accuracy.

Do not deliver an uninspected auto-generated deck.

---

# INCIDENT / SERVICE CONTEXT

Check whether Elexon provides a current official incident/status/issue source relevant to Insights Solution.

If a material data exception coincides with an officially reported service incident, record that context.

If no incident exists, do not invent one.

Do not confuse market anomalies with platform/service incidents.

---

# TESTING

Write meaningful tests only for logic that could materially invalidate analysis.

Prioritise:

- Settlement Period completeness logic;
- clock-change handling;
- duplicate detection;
- null handling;
- NIV sign/system-length logic;
- timestamp conversion;
- percentile/robust threshold calculations;
- transformation integrity;
- expected schema;
- key summary calculations.

Avoid test-count vanity.

Do not test trivial formatting simply because tests can be written.

Run the appropriate test suite.

Once meaningful checks pass, continue to completion unless new failures justify broader testing.

---

# REPRODUCIBILITY

The repository should be reproducible from a clean environment.

Document:

- dependencies;
- installation;
- commands;
- data-fetch process;
- transformation process;
- SQL execution;
- report dependencies;
- Power BI/Fabric requirements.

Do not depend on undocumented manual edits.

Do not commit secrets.

Avoid committing unnecessarily large raw datasets if they can be re-downloaded reliably.

---

# GITHUB

Initialise a clean Git repository.

Use meaningful commits at major milestones.

Do not commit:

- credentials;
- tokens;
- local environment secrets;
- giant temporary artifacts.

Prepare the repository as if a hiring manager may browse it.

If authenticated GitHub access is available and publishing is authorised, publish the repository.

Otherwise leave it fully prepared locally and provide the exact final publish step.

---

# FINAL CLAIM AUDIT

Before completion, review every claim that appears in:

- README;
- Power BI;
- Service Insight Note;
- presentation;
- CV recommendation.

Classify every material claim as:

SUPPORTED

DERIVED

HYPOTHESIS

UNSUPPORTED

Remove or correct UNSUPPORTED claims.

Do not say:

production-grade

real-time monitoring

automated root-cause analysis

official Elexon tool

operationally deployed

unless objectively true.

---

# FINAL TECHNICAL QA

Before declaring completion:

1. Re-run the ingestion pipeline from a clean state.
2. Confirm Elexon API retrieval succeeds.
3. Run data-quality controls.
4. Run meaningful automated tests.
5. Run SQL analysis.
6. Cross-check material statistics.
7. Verify Power BI measures independently.
8. Inspect all four Power BI pages visually.
9. Test filters/slicers/interactions.
10. Check Power BI performance where possible.
11. Review METHODOLOGY.md.
12. Review README.
13. Review Service Insight Note.
14. Inspect all presentation slides.
15. Check source links.
16. Audit domain statements against SOURCES.md.
17. Confirm reproducibility instructions.
18. Confirm no credentials/secrets are present.
19. Update PROJECT_STATE.md.

Do not call the project finished simply because all files exist.

It is finished only when the outputs are coherent, accurate, visually reviewed and mutually consistent.

---

# ADVERSARIAL SELF-REVIEW

Before final delivery, perform an independent critic pass.

Attempt to identify:

- unsupported market interpretation;
- causal overclaiming;
- incorrect BSC terminology;
- weak exception thresholds;
- faulty time handling;
- Power BI calculation mismatch;
- misleading visuals;
- data leakage between raw/processed layers;
- incorrect units;
- inconsistent numbers across Python/SQL/Power BI/deck;
- claims an Elexon interviewer could challenge;
- unnecessary complexity;
- obvious AI-generated portfolio patterns.

Fix material issues.

---

# CV OUTPUT

Only AFTER the project has been completed and verified, propose two concise CV bullets for the project.

They must describe only what actually exists.

Target the Elexon Service Analyst vacancy.

Do not exaggerate.

Also provide:

- a 30-second interview explanation;
- a 90-second interview explanation;
- 10 likely questions an Elexon interviewer could ask about the project;
- concise, evidence-defensible answer points.

---

# HANDOFF / MODEL LIMITS

If model quota, context or tool availability becomes a risk:

update immediately:

`PROJECT_STATE.md`

`DECISIONS.md`

`SOURCES.md`

Include enough detail for another agent to continue without this chat.

Do not restart completed work.

If another agent continues the project, it must first read:

AGENTS.md

PROJECT_SPEC.md

PROJECT_STATE.md

DECISIONS.md

SOURCES.md

METHODOLOGY.md

and inspect the repository status before making changes.

---

# FINAL RESPONSE

Do not provide a lengthy diary of everything you did.

Complete the work.

Then return a concise project completion report containing:

PROJECT STATUS

WHAT WAS BUILT

KEY VERIFIED FINDINGS

POWER BI STATUS

DATA-QUALITY STATUS

PRESENTATION STATUS

FILES / LINKS

TESTS AND QA PERFORMED

MATERIAL ASSUMPTIONS

LIMITATIONS

WHAT I MUST PERSONALLY UNDERSTAND BEFORE AN ELEXON INTERVIEW

CV BULLETS

If any component could not be completed due authentication, permissions, Power BI licensing, Fabric access, OS constraints or another external dependency:

- complete every unaffected component first;
- preserve all intermediate work;
- explain precisely what remains;
- give me the smallest exact action needed to unblock it.

Begin now.

Do not respond with a plan.

Carry the project through to the furthest complete, verified state the environment permits.
