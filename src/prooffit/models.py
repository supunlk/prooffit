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


class JobFitResult(BaseModel):
    fit_score: float = Field(ge=0, le=10)
    decision: Literal["APPLY", "REVIEW", "SKIP"]
    gaps: list[str]
    red_flags: list[str]
    salary_read: SalaryRead
    which_cv: CVRecommendation