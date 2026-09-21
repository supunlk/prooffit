from openai import OpenAI
from prooffit.models import JobFitEvaluation, JobFitResult, JobRequirements
from prooffit.scoring import calculate_fit_score, determine_decision

INSTRUCTIONS = """
    You are a job-fit evaluator.

    Rules:
    - Use EXTRACTED JOB REQUIREMENTS as the complete requirement list for assessment.
    - Assess every extracted requirement exactly once.
    - Do not add, remove, merge, rename, or replace extracted requirements.
    - Copy the requirement wording exactly into each RequirementAssessment.

    - Candidate evidence may come only from CANDIDATE PROFILE.
    - Do not use the job description, extracted requirements, CV names, or CV descriptions as candidate evidence.
    - AVAILABLE CVS may be used only to choose which CV to recommend.
    - Do not invent experience, skills, responsibilities, achievements, or terminology.
    - Treat missing evidence as unknown, not as experience.
    - Do not infer an action or responsibility from related skills alone.
    - If there is no relevant candidate evidence for a requirement, set evidence to null.

    Requirement grading rubric:
    - MATCH: Direct, explicit evidence fully supports the same requirement, including its required level, responsibility, or context.
    - PARTIAL: Direct evidence exists for the same skill, responsibility, or domain, but part of the requirement such as depth, scale, context, duration, or responsibility is not proven.
    - WEAK: Evidence is only adjacent, academic, experimental, learning-based, or limited exposure and does not demonstrate the requirement in comparable real-world work.
    - GAP: The candidate profile explicitly states or clearly demonstrates that the candidate does not meet the requirement.
    - UNKNOWN: There is no relevant evidence available to assess the requirement.

    Important distinctions:
    - Related professional experience should not be UNKNOWN. Use PARTIAL or WEAK depending on how directly it supports the requirement.
    - Coursework, tutorials, experiments, and small learning projects do not count as production experience. Use WEAK when they are the only supporting evidence for a production requirement.

    Additional rules:
    - Separate required requirements from preferred requirements.
    - Only include genuine red flags in red_flags. If there are none, return an empty list.
"""

def evaluate_job(
    job_description: str,
    candidate_profile: str,
    available_cvs: str,
    job_requirements: JobRequirements,
) -> JobFitResult:
    
    client = OpenAI()

    input_text = f"""
        JOB DESCRIPTION:
        {job_description}

        EXTRACTED JOB REQUIREMENTS:
        {job_requirements.model_dump_json(indent=2)}

        CANDIDATE PROFILE:
        {candidate_profile}

        {available_cvs}
    """

    response = client.responses.parse(
        model="gpt-5.6-luna",
        instructions=INSTRUCTIONS,
        input=input_text,
        text_format=JobFitEvaluation,
    )

    evaluation = response.output_parsed

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

