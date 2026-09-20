# ProofFit

**An evidence-backed AI job search agent**

ProofFit is a learning and portfolio project for evaluating job opportunities against verified candidate evidence.

Its core rule is simple:

> No unsupported career claim should be generated.

The project is being built incrementally to explore practical AI engineering, including direct LLM APIs, structured output, evaluation, retrieval, tools, agents, MCP, memory, security, and observability.

## Current status

ProofFit currently supports a basic structured job-fit evaluation flow:

```text
Job description
      +
Candidate profile
      +
Available CV options
      +
Evaluation instructions
      |
      v
OpenAI Responses API
      |
      v
Structured output
      |
      v
Pydantic validation
      |
      v
JobFitResult
```

The current evaluator returns:

- Fit score from 0 to 10
- Decision: `APPLY`, `REVIEW`, or `SKIP`
- Skill and experience gaps
- Red flags
- Structured salary assessment
- Recommended CV with a reason

## Project structure

```text
prooffit/
├── docs/
├── evals/
│   ├── cases.json
│   └── run_eval.py
├── src/
│   └── prooffit/
│       ├── __init__.py
│       ├── cv_options.py
│       ├── evaluator.py
│       └── models.py
├── tests/
│   └── test_models.py
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

The current unit tests verify model validation such as:

- Valid `JobFitResult` creation
- Fit scores above 10 are rejected
- Invalid decision values are rejected

## Run AI evaluations

```bash
uv run python evals/run_eval.py
```

The evaluation suite compares model output against human-defined expected behavior.

Current eval cases cover:

- Strong Software Architect match
- Deep Machine Learning Engineer mismatch
- Partial Backend Architect match

An eval case can check:

- Expected decision
- Expected score range
- Expected CV recommendation

Example:

```json
{
  "name": "strong_software_architect_match",
  "expected_decision": "APPLY",
  "expected_score_min": 8.0,
  "expected_score_max": 10.0,
  "expected_cv": "Software Architect CV"
}
```

Score ranges are used instead of exact values because LLM outputs can vary slightly between runs while still being correct.

## Why both tests and evals?

ProofFit separates deterministic software testing from AI behavior evaluation.

```text
Unit tests
= Is the software behaving correctly?

AI evals
= Is the model making acceptable judgments?
```

For example:

```text
Unit test:
fit_score = 92
-> Pydantic must reject it

AI eval:
Strong architect role + strong architect profile
-> Expected APPLY
-> Expected score between 8 and 10
```

## Development principles

- Use direct model APIs before adding frameworks.
- Keep prompts explicit and evidence-bound.
- Use structured outputs instead of free-form text where possible.
- Validate model output at runtime.
- Treat missing evidence as unknown.
- Do not invent candidate experience.
- Separate required requirements from preferred requirements.
- Add eval cases before making major prompt changes.
- Run the full eval suite after prompt changes to detect regressions.

## Planned learning and development

The project is intentionally being built step by step.

Planned areas include:

- Better evaluation coverage
- Evidence-backed career profiles
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
