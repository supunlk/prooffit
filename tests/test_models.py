from prooffit.models import JobFitResult
import pytest
from pydantic import ValidationError

def test_valid_job_fit_result():
    result = JobFitResult(
        fit_score=8.5,
        decision="APPLY",
        gaps=[],
        red_flags=[],
        requirements=[],
        salary_read={
            "status": "NOT_LISTED",
            "details": "No salary provided.",
        },
        which_cv={
            "name": "Software Architect CV",
            "reason": "Best match.",
        },
    )

    assert result.fit_score == 8.5


def test_fit_score_above_10_is_invalid():
    with pytest.raises(ValidationError):
        JobFitResult(
            fit_score=92,
            decision="APPLY",
            gaps=[],
            red_flags=[],
            requirements=[],
            salary_read={
                "status": "NOT_LISTED",
                "details": "No salary provided.",
            },
            which_cv={
                "name": "Software Architect CV",
                "reason": "Best match.",
            },
        )


def test_decision_yes_is_invalid():
    with pytest.raises(ValidationError):
        JobFitResult(
            fit_score=8.2,
            decision="YES",
            gaps=[],
            red_flags=[],
            requirements=[],
            salary_read={
                "status": "NOT_LISTED",
                "details": "No salary provided.",
            },
            which_cv={
                "name": "Software Architect CV",
                "reason": "Best match.",
            },
        )
