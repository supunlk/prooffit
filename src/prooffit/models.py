from pydantic import BaseModel, Field
from typing import Literal

class SalaryRead(BaseModel):
    status: Literal[
        "NOT_LISTED",
        "BELOW_TARGET",
        "MEETS_TARGET",
        "ABOVE_TARGET",
        "UNCLEAR",
    ]   
    details: str

class CVRecommendation(BaseModel):
    name: Literal[
        "Software Architect CV",
        "Tech Lead CV",
        "General CV",
        "Senior Software Engineer CV",
        "Engineering Manager CV",
        "Engineering Lead CV",
    ]
    reason: str

class JobRequirement(BaseModel):
    requirement: str
    importance: Literal["REQUIRED", "PREFERRED"]

class JobRequirements(BaseModel):
    requirements: list[JobRequirement]

class RequirementAssessment(BaseModel):
    requirement: str
    status: Literal["MATCH", "PARTIAL", "WEAK", "GAP", "UNKNOWN"]
    evidence: str | None = None
    reason: str
    evidence_ids: list[str]

class JobFitEvaluation(BaseModel):
    requirements: list[RequirementAssessment]
    gaps: list[str]
    red_flags: list[str]
    salary_read: SalaryRead
    which_cv: CVRecommendation

class JobFitResult(BaseModel):
    fit_score: float = Field(ge=0, le=10)
    decision: Literal["APPLY", "REVIEW", "SKIP"]
    gaps: list[str]
    red_flags: list[str]
    requirements: list[RequirementAssessment]
    salary_read: SalaryRead
    which_cv: CVRecommendation

class CareerEvidence(BaseModel):
    id: str
    category: Literal["SKILL", "RESPONSIBILITY", "OUTCOME", "EDUCATION"]
    statement: str
    topics: list[str]
    context: Literal[
        "PRODUCTION",
        "LIMITED_PRODUCTION",
        "LEARNING",
        "EDUCATION",
        "NEGATIVE",
    ]