from prooffit.models import JobRequirement, JobRequirements, RequirementAssessment
from prooffit.scoring import calculate_fit_score, determine_decision


def test_determine_decision():
    assert determine_decision(8.0) == "APPLY"
    assert determine_decision(5.0) == "REVIEW"
    assert determine_decision(2.0) == "SKIP"


def test_partial_required_requirement_scores_6_7():
    job_requirements = JobRequirements(
        requirements=[
            JobRequirement(
                requirement="AWS experience",
                importance="REQUIRED",
            )
        ]
    )

    assessments = [
        RequirementAssessment(
            requirement="AWS experience",
            status="PARTIAL",
            evidence="Some AWS experience.",
            evidence_ids=["evidence-001"],
            reason="Relevant experience exists but does not fully meet the requirement.",
        )
    ]

    score = calculate_fit_score(
        assessments,
        job_requirements,
    )

    assert score == 6.7


def test_preferred_gap_has_lower_weight():
    job_requirements = JobRequirements(
        requirements=[
            JobRequirement(
                requirement="Kubernetes",
                importance="REQUIRED",
            ),
            JobRequirement(
                requirement="AWS",
                importance="PREFERRED",
            ),
        ]
    )

    assessments = [
        RequirementAssessment(
            requirement="Kubernetes",
            status="MATCH",
            evidence="Production Kubernetes experience.",
            evidence_ids=["evidence-001"],
            reason="Direct match.",
        ),
        RequirementAssessment(
            requirement="AWS",
            status="GAP",
            evidence="No AWS experience.",
            evidence_ids=["evidence-002"],
            reason="Preferred requirement is not met.",
        ),
    ]

    score = calculate_fit_score(
        assessments,
        job_requirements,
    )

    assert score == 8.0


def test_required_gap_has_strong_impact():
    job_requirements = JobRequirements(
        requirements=[
            JobRequirement(
                requirement="Kubernetes",
                importance="REQUIRED",
            ),
            JobRequirement(
                requirement="AWS",
                importance="PREFERRED",
            ),
        ]
    )

    assessments = [
        RequirementAssessment(
            requirement="Kubernetes",
            status="GAP",
            evidence="No Kubernetes experience.",
            evidence_ids=["evidence-001"],
            reason="Required requirement is not met.",
        ),
        RequirementAssessment(
            requirement="AWS",
            status="MATCH",
            evidence="Production AWS experience.",
            evidence_ids=["evidence-002"],
            reason="Preferred requirement is fully met.",
        ),
    ]

    score = calculate_fit_score(
        assessments,
        job_requirements,
    )

    assert score == 2.0