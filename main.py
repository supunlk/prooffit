from prooffit.evaluator import evaluate_job
from dotenv import load_dotenv
from prooffit.cv_options import AVAILABLE_CVS
from prooffit.requirement_extractor import extract_requirements

load_dotenv()


job_description = """
Software Architect

We are looking for an experienced software architect with strong skills in
TypeScript, Angular, Node.js, microservices, Kubernetes, and cloud architecture.

The role includes:
- Designing scalable SaaS systems
- Leading architecture decisions
- Mentoring engineers
- Building Node.js services
- Working with Kubernetes and CI/CD

AWS experience is preferred.
"""

requirements = extract_requirements(job_description)

candidate_profile = """
Candidate has 15+ years of software engineering experience.

Skills and experience:
- Software architecture
- Angular and TypeScript
- Node.js and NestJS
- Microservices
- Kubernetes
- CI/CD
- Engineering leadership and mentoring
- Production cloud systems

Limited production AWS experience.
"""

job_fit_result = evaluate_job(
    job_description,
    candidate_profile,
    AVAILABLE_CVS,
    requirements,
)

print(job_fit_result)