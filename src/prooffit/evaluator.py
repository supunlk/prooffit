from openai import OpenAI
from prooffit.models import (
    CareerEvidence,
    JobFitEvaluation,
    JobFitResult,
    JobRequirements,
)
from prooffit.scoring import calculate_fit_score, determine_decision
from prooffit.tool_runner import run_tool_loop
from prooffit.tools import TOOLS, build_tool_handlers

INSTRUCTIONS = """
    You are a job-fit evaluator.

    Rules:
    - Use EXTRACTED JOB REQUIREMENTS as the complete requirement list for assessment.
    - Assess every extracted requirement exactly once.
    - Do not add, remove, merge, rename, or replace extracted requirements.
    - Copy the requirement wording exactly into each RequirementAssessment.

    - Candidate evidence may come only from results returned by the get_candidate_evidence tool.
    - Do not use the job description, extracted requirements, CV names, or CV descriptions as candidate evidence.
    - You must use get_candidate_evidence to look for evidence before assessing a requirement.
    - If the tool returns no relevant evidence, treat the requirement as UNKNOWN.
    - AVAILABLE CVS may be used only to choose which CV to recommend.
    - Do not invent experience, skills, responsibilities, achievements, or terminology.
    - Treat missing evidence as unknown, not as experience.
    - Do not infer an action or responsibility from related skills alone.
    - If there is no relevant candidate evidence for a requirement, set evidence to null.

    Requirement grading rubric:
    - MATCH: Direct, explicit evidence fully supports the same requirement, including its required level, responsibility, or context.
    - PARTIAL: Direct evidence exists for the same skill, responsibility, or domain, but part of the requirement such as depth, scale, context, duration, or responsibility is not proven.
    - WEAK: Evidence is only adjacent, academic, experimental, learning-based, or limited exposure and does not demonstrate the requirement in comparable real-world work.
    - GAP: Tool evidence explicitly states or clearly demonstrates that the candidate does not meet the requirement.
    - UNKNOWN: There is no relevant evidence available to assess the requirement.

    - GAP requires explicit negative evidence returned by the tool. Missing evidence must never be classified as GAP.
    - If the tool returns no relevant evidence for a requirement, classify it as UNKNOWN.
    - Academic, coursework, experimental, or small learning-project evidence for a production requirement must be classified as WEAK, not GAP.
    - Do not classify a responsibility as MATCH based only on evidence of a related skill or role. For example, software architecture experience alone does not prove leading architecture decisions.

    Important distinctions:
    - Related professional experience should not be UNKNOWN. Use PARTIAL or WEAK depending on how directly it supports the requirement.
    - Coursework, tutorials, experiments, and small learning projects do not count as production experience. Use WEAK when they are the only supporting evidence for a production requirement.

    Additional rules:
    - Separate required requirements from preferred requirements.
    - Only include genuine red flags in red_flags. If there are none, return an empty list.
    - For every RequirementAssessment, include evidence_ids containing the exact IDs of the tool evidence records used for that assessment.
    - If no evidence was used, return an empty evidence_ids list.
    - Do not invent evidence IDs.
"""

def evaluate_job(
    job_description: str,
    candidate_evidence: list[CareerEvidence],
    available_cvs: str,
    job_requirements: JobRequirements,
) -> JobFitResult:
    
    client = OpenAI()

    tool_handlers = build_tool_handlers(candidate_evidence)

    input_text = f"""
        JOB DESCRIPTION:
        {job_description}

        EXTRACTED JOB REQUIREMENTS:
        {job_requirements.model_dump_json(indent=2)}

        {available_cvs}
    """

    response = client.responses.parse(
        model="gpt-5.6-luna",
        instructions=INSTRUCTIONS,
        input=input_text,
        tools=TOOLS,
        text_format=JobFitEvaluation,
    )

    response = run_tool_loop(
        client=client,
        response=response,
        tools=TOOLS,
        tool_handlers=tool_handlers,
        text_format=JobFitEvaluation,
    )

    evaluation = response.output_parsed
    evidence_by_id = {
        evidence.id: evidence
        for evidence in candidate_evidence
    }

    for assessment in evaluation.requirements:
        used_evidence = [
            evidence_by_id[evidence_id]
            for evidence_id in assessment.evidence_ids
            if evidence_id in evidence_by_id
        ]

        if assessment.status == "GAP" and assessment.evidence is None:
            assessment.status = "UNKNOWN"

        if used_evidence and all(
            evidence.context in {"EDUCATION", "LEARNING"}
            for evidence in used_evidence
        ):
            assessment.status = "WEAK"

    fit_score = calculate_fit_score(
        evaluation.requirements,
        job_requirements,
    )

    decision = determine_decision(fit_score)

    result = JobFitResult(
        fit_score=fit_score,
        decision=decision,
        gaps=evaluation.gaps,
        red_flags=evaluation.red_flags,
        requirements=evaluation.requirements,
        salary_read=evaluation.salary_read,
        which_cv=evaluation.which_cv,
    )

    return result

