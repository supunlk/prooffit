import json

from prooffit.evaluator import evaluate_job
from dotenv import load_dotenv
from prooffit.cv_options import AVAILABLE_CVS

load_dotenv()

with open("evals/cases.json", "r") as file:
    cases = json.load(file)

    passed_count = 0

    for case in cases:
        result = evaluate_job(
            case["job_description"],
            case["candidate_profile"],
            AVAILABLE_CVS
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

        passed = decision_passed and score_passed and cv_passed

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