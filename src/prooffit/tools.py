from prooffit.models import CareerEvidence
import re

CANDIDATE_EVIDENCE = [
    CareerEvidence(
        id="evidence-001",
        category="SKILL",
        statement="Production experience with Kubernetes.",
        topics=["Kubernetes", "cloud"],
        context="PRODUCTION",
    ),
    CareerEvidence(
        id="evidence-002",
        category="SKILL",
        statement="Worked with Kubernetes-based cloud systems.",
        topics=["Kubernetes", "cloud"],
        context="PRODUCTION",
    ),
    CareerEvidence(
        id="evidence-003",
        category="SKILL",
        statement="Limited production AWS experience.",
        topics=["AWS", "cloud"],
        context="LIMITED_PRODUCTION",
    ),
    CareerEvidence(
        id="evidence-004",
        category="SKILL",
        statement="Production experience with Node.js and NestJS.",
        topics=["Node.js", "NestJS", "backend"],
        context="PRODUCTION",
    ),
]


def get_candidate_evidence(query: str) -> list[dict]:
    matches = [
        evidence
        for evidence in CANDIDATE_EVIDENCE
        if any(
            topic.lower() in query.lower()
            for topic in evidence.topics
        )
    ]

    return [evidence.model_dump() for evidence in matches]

def get_available_cvs() -> list[str]:
    return [
        "Software Architect CV",
        "Tech Lead CV",
        "General CV",
        "Senior Software Engineer CV",
        "Engineering Manager CV",
        "Engineering Lead CV",
    ]

def topic_matches_query(topic: str, query: str) -> bool:
    pattern = rf"(?<!\w){re.escape(topic)}(?!\w)"
    return re.search(pattern, query, re.IGNORECASE) is not None

def build_tool_handlers(candidate_evidence: list[CareerEvidence]):
    def get_candidate_evidence_for_candidate(query: str) -> list[dict]:
        matches = [
            evidence
            for evidence in candidate_evidence
            if any(
                topic_matches_query(topic, query)
                for topic in evidence.topics
            )
        ]

        return [evidence.model_dump() for evidence in matches]

    return {
        "get_candidate_evidence": get_candidate_evidence_for_candidate,
        "get_available_cvs": get_available_cvs,
    }


TOOL_HANDLERS = {
    "get_candidate_evidence": get_candidate_evidence,
    "get_available_cvs": get_available_cvs,
}

TOOLS = [
    {
        "type": "function",
        "name": "get_candidate_evidence",
        "description": "Get candidate career evidence for a specific skill or topic.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The skill or topic to search for, such as Kubernetes or AWS.",
                }
            },
            "required": ["query"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "get_available_cvs",
        "description": "Get the list of CV versions available for the candidate.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
        "strict": True,
    }
]