# ProofFit

**An evidence-backed AI job search agent**

ProofFit is a learning and portfolio project for evaluating job opportunities against verified candidate evidence.

Its core rule is simple:

> No unsupported career claim should be generated.

The project is being built incrementally to explore practical AI engineering, including direct LLM APIs, structured output, evaluation, retrieval, tools, agents, MCP, memory, security, and observability.

## Current status

ProofFit currently uses a two-stage AI pipeline followed by deterministic Python scoring:

```text
Job description
      |
      v
Requirement extractor
      |
      v
Structured JobRequirements
      |
      +----------------------+
      |                      |
      v                      v
Candidate profile      Available CV options
      |                      |
      +----------+-----------+
                 |
                 v
          Job-fit evaluator
                 |
                 v
      RequirementAssessment[]
                 |
                 v
       Rubric-based grading
                 |
                 v
     Deterministic Python score
                 |
                 v
    Deterministic Python decision
                 |
                 v
            JobFitResult
```

The LLM is responsible for:

- Extracting explicit job requirements
- Classifying requirements as `REQUIRED` or `PREFERRED`
- Assessing candidate evidence against each requirement
- Producing evidence-backed requirement grades
- Identifying gaps and red flags
- Reading salary information
- Recommending the most appropriate CV

Python is responsible for:

- Calculating the final fit score
- Applying requirement weights
- Converting the score into `APPLY`, `REVIEW`, or `SKIP`

This separation keeps fuzzy judgment with the LLM while keeping scoring and decision rules deterministic.

## Requirement grading rubric

Each extracted requirement is assessed using the following rubric:

```text
MATCH
Direct, explicit evidence fully supports the requirement.

PARTIAL
Meaningful evidence exists for the same skill, responsibility, or domain,
but part of the requirement is not proven.

WEAK
Evidence is only adjacent, academic, experimental, learning-based,
or limited exposure.

GAP
The candidate profile explicitly shows that the requirement is not met.

UNKNOWN
There is not enough relevant evidence to judge the requirement.
```

`GAP` and `UNKNOWN` are intentionally different.

```text
Terraform not mentioned
-> UNKNOWN

"No Terraform experience"
-> GAP
```

Absence of evidence is not treated as evidence of absence.

## Deterministic scoring

Requirement grades are converted into rubric points:

```text
MATCH   = 3
PARTIAL = 2
WEAK    = 1
GAP     = 0
UNKNOWN = 0
```

Job requirement importance is also weighted:

```text
REQUIRED  = 2.0
PREFERRED = 0.5
```

A required requirement therefore has much more influence on the final score than a preferred one.

Example:

```text
Required Kubernetes -> MATCH
3 x 2.0 = 6.0 points

Preferred AWS -> GAP
0 x 0.5 = 0 points

Maximum possible:
6.0 + 1.5 = 7.5

Fit score:
6.0 / 7.5 x 10 = 8.0
```

The final decision is calculated in Python:

```text
7.5 - 10.0 -> APPLY
4.0 - 7.49 -> REVIEW
0.0 - 3.99 -> SKIP
```

## Evidence boundaries

ProofFit keeps different prompt inputs separate:

```text
CANDIDATE PROFILE
-> the only source of candidate evidence

EXTRACTED JOB REQUIREMENTS
-> defines what must be assessed

AVAILABLE CVS
-> used only for CV recommendation
```

CV names and CV descriptions are never allowed to become evidence for a requirement assessment.

## Project structure

```text
prooffit/
├── docs/
│   └── adr/
├── evals/
│   ├── cases.json
│   └── run_eval.py
├── src/
│   └── prooffit/
│       ├── __init__.py
│       ├── cv_options.py
│       ├── evaluator.py
│       ├── models.py
│       ├── requirement_extractor.py
│       └── scoring.py
├── tests/
│   ├── test_models.py
│   └── test_scoring.py
├── .gitignore
├── main.py
├── pyproject.toml
└── uv.lock
```

## Tech stack

- Python 3.12+
- OpenAI Python SDK
- Pydantic
- python-dotenv
- pytest
- uv
- Hatchling

## Setup

Clone the repository:

```bash
git clone https://github.com/supunlk/prooffit.git
cd prooffit
```

Install and sync dependencies:

```bash
uv sync
```

Create a `.env` file in the project root:

```text
OPENAI_API_KEY=your_api_key_here
```

Do not commit `.env`.

## Run the evaluator

```bash
uv run python main.py
```

## Run unit tests

```bash
uv run pytest
```

The current unit tests cover:

- Valid `JobFitResult` creation
- Fit score validation
- Decision validation
- Required requirement scoring
- Preferred requirement weighting
- Required gap impact
- Deterministic decision mapping

Current result:

```text
7 passed
```

## Run AI evaluations

```bash
uv run python evals/run_eval.py
```

The evaluation suite compares model behavior against human-defined expected behavior.

Current eval cases cover:

- Strong Software Architect match
- Deep Machine Learning Engineer mismatch
- Partial Backend Architect match
- Weak AWS exposure

An eval case can check:

- Expected decision
- Expected score range
- Expected CV recommendation
- Expected requirement status

Example:

```json
{
  "name": "strong_software_architect_match",
  "expected_decision": "APPLY",
  "expected_score_min": 7.5,
  "expected_score_max": 10.0,
  "expected_cv": "Software Architect CV",
  "expected_requirement": {
    "requirement_contains": "architecture decisions",
    "status": "PARTIAL"
  }
}
```

Current result:

```text
Overall: 4/4 passed
```

Score ranges are still useful in AI evals because the LLM can vary slightly in requirement grading between runs. The final score itself is deterministic once the requirement assessments are fixed.

## Why both tests and evals?

ProofFit separates deterministic software testing from AI behavior evaluation.

```text
Unit tests
= Is the software logic behaving correctly?

AI evals
= Is the model making acceptable evidence-backed judgments?
```

For example:

```text
Unit test:
Required Kubernetes -> MATCH
Preferred AWS -> GAP
Expected deterministic score -> 8.0

AI eval:
Candidate has AWS coursework and small learning projects
Requirement asks for strong production AWS architecture
Expected assessment -> WEAK
```

This distinction is important because Pydantic can validate that an output has the correct shape, but that does not mean the model's judgment is correct.

## Development principles

- Use direct model APIs before adding frameworks.
- Give each AI component one clear responsibility.
- Keep prompts explicit and evidence-bound.
- Use structured outputs instead of free-form text where possible.
- Validate model output at runtime.
- Treat missing evidence as unknown.
- Do not invent candidate experience.
- Do not infer responsibilities from related skills alone.
- Separate required requirements from preferred requirements.
- Use rubric-based grading instead of binary matching.
- Keep deterministic business logic in normal Python code.
- Add eval cases for important AI behaviors.
- Run the full eval suite after prompt or rubric changes.
- Inspect eval failures before changing prompts or expected results.

## What we have learned so far

Several failures shaped the current architecture:

- Structured output guarantees shape, not truth.
- An LLM can produce plausible but unsupported evidence.
- Prompt rules alone do not guarantee that every job requirement is preserved.
- Separating requirement extraction from candidate assessment reduces responsibility per model call.
- Different prompt sections can accidentally leak into each other if evidence boundaries are not explicit.
- AI-generated numeric scores can vary even when the underlying reasoning is similar.
- Deterministic scoring is better handled in normal code.
- Evals can be wrong too, so a failing eval should be investigated rather than blindly fixed.
- Rubric-based grading gives more useful information than simple yes/no matching.

## Planned learning and development

The project is intentionally being built step by step.

Planned areas include:

- More evaluation coverage
- Evidence-backed career profiles
- Better scoring policies
- Embeddings
- Retrieval-Augmented Generation
- Vector search
- Tool and function calling
- MCP
- Agent memory
- Multi-step agent workflows
- Human approval flows
- AI tracing and observability
- Security and access control
- Production deployment

Frameworks such as LangChain or LangGraph may be introduced later only where they provide a clear benefit.

## License

MIT

Copyright (c) 2026 Supun De Silva
