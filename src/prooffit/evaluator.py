from openai import OpenAI
from prooffit.models import JobFitResult


INSTRUCTIONS = """
    You are a job-fit evaluator.

    Rules:
    - Use only the candidate evidence provided.
    - Do not invent experience or skills.
    - Treat missing evidence as unknown, not as experience.
    - Separate required requirements from preferred requirements.
    - Score fit from 0 to 10.
    - Return APPLY, REVIEW, or SKIP.
    - Only include genuine red flags in red_flags. If there are none, return an empty list.
"""

def evaluate_job(
    job_description: str,
    candidate_profile: str,
    available_cvs: str,
) -> JobFitResult:
    
    client = OpenAI()

    input_text = f"""
        JOB DESCRIPTION:
        {job_description}

        CANDIDATE PROFILE:
        {candidate_profile}

        {available_cvs}
    """

    response = client.responses.parse(
        model="gpt-5.6-luna",
        instructions=INSTRUCTIONS,
        input=input_text,
        text_format=JobFitResult,
    )

    return response.output_parsed

