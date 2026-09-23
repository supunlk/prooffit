CANDIDATE_EVIDENCE = {
    "Kubernetes": [
        "Production experience with Kubernetes.",
        "Worked with Kubernetes-based cloud systems.",
    ],
    "AWS": [
        "Limited production AWS experience.",
    ],
    "Node.js": [
        "Production experience with Node.js and NestJS.",
    ],
}

def get_candidate_evidence(query: str) -> list[str]:
    return CANDIDATE_EVIDENCE.get(query, [])

def get_available_cvs() -> list[str]:
    return [
        "Software Architect CV",
        "Tech Lead CV",
        "General CV",
        "Senior Software Engineer CV",
        "Engineering Manager CV",
        "Engineering Lead CV",
    ]