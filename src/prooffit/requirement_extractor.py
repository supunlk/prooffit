from openai import OpenAI

from prooffit.models import JobRequirements

INSTRUCTIONS = """
    You extract explicit job requirements from a job description.

    Rules:
    - Extract each requirement separately.
    - Do not merge distinct requirements.
    - Keep the requirement wording close to the job description.
    - Mark a requirement as REQUIRED when the job states or strongly implies it is required.
    - Mark it as PREFERRED only when the job clearly describes it as preferred, optional, or nice to have.
    - Do not assess the candidate.
    - Do not invent requirements that are not present in the job description.
"""


def extract_requirements(job_description: str) -> JobRequirements:
    client = OpenAI()

    response = client.responses.parse(
        model="gpt-5.6-luna",
        instructions=INSTRUCTIONS,
        input=job_description,
        text_format=JobRequirements,
    )

    return response.output_parsed
