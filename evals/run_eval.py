import json

from dotenv import load_dotenv

from prooffit.cv_options import AVAILABLE_CVS
from prooffit.evaluator import evaluate_job
from prooffit.requirement_extractor import extract_requirements

load_dotenv()

with open("evals/cases.json", "r") as file:
    cases = json.load(file)

    passed_count = 0

    for case in cases:
        job_requirements = extract_requirements(case["job_description"])

        result = evaluate_job(
            case["job_description"],
            case["candidate_profile"],
            AVAILABLE_CVS,
            job_requirements,
        )

        decision_passed = result.decision == case["expected_decision"]

        score_passed = (
            case["expected_score_min"]
            <= result.fit_score
            <= case["expected_score_max"]
        )

        expected_cv = case.get("expected_cv")
        cv_passed = True

        if expected_cv is not None:
            cv_passed = result.which_cv.name == expected_cv

        expected_requirement = case.get("expected_requirement")
        requirement_passed = True

        if expected_requirement is not None:
            requirement_passed = any(
                expected_requirement["requirement_contains"]
                in requirement.requirement
                and requirement.status == expected_requirement["status"]
                for requirement in result.requirements
            )

        passed = (
            decision_passed
            and score_passed
            and cv_passed
            and requirement_passed
        )

        if passed:
            passed_count += 1

        print(
            f"{case['name']}: "
            f"{'PASS' if passed else 'FAIL'} "
            f"| decision={result.decision} "
            f"| score={result.fit_score} "
            f"| cv={result.which_cv.name}"
        )

    print(f"\nOverall: {passed_count}/{len(cases)} passed")