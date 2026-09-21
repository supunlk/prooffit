from typing import Literal
from prooffit.models import JobRequirements, RequirementAssessment


STATUS_POINTS = {
    "MATCH": 3,
    "PARTIAL": 2,
    "WEAK": 1,
    "GAP": 0,
    "UNKNOWN": 0,
}

IMPORTANCE_WEIGHTS = {
    "REQUIRED": 2.0,
    "PREFERRED": 0.5,
}

def calculate_fit_score(
    assessments: list[RequirementAssessment],
    job_requirements: JobRequirements,
) -> float:
    importance_by_requirement = {
        requirement.requirement: requirement.importance
        for requirement in job_requirements.requirements
    }

    total_points = 0.0
    max_points = 0.0

    for assessment in assessments:
        importance = importance_by_requirement[assessment.requirement]
        status_points = STATUS_POINTS[assessment.status]
        weight = IMPORTANCE_WEIGHTS[importance]

        total_points += status_points * weight
        max_points += STATUS_POINTS["MATCH"] * weight

    if max_points == 0:
        return 0.0

    return round((total_points / max_points) * 10, 1)


def determine_decision(
    fit_score: float,
) -> Literal["APPLY", "REVIEW", "SKIP"]:
    if fit_score >= 7.5:
        return "APPLY"

    if fit_score >= 4.0:
        return "REVIEW"

    return "SKIP"
