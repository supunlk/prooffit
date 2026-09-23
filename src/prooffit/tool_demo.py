from openai import OpenAI
from dotenv import load_dotenv
import json

from prooffit.tools import get_available_cvs, get_candidate_evidence

load_dotenv()

client = OpenAI()

TOOL_HANDLERS = {
    "get_candidate_evidence": get_candidate_evidence,
    "get_available_cvs": get_available_cvs,
}

tools = [
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

response = client.responses.create(
    model="gpt-5.6-luna",
    input="Find the candidate's evidence for Kubernetes experience and tell me what CV versions are available.",
    tools=tools,
)

max_steps = 5
step = 0

while True:

    step += 1
    print(f"\nSTEP {step}")

    if step > max_steps:
        print("Maximum tool steps reached.")
        break

    function_calls = [
        item
        for item in response.output
        if item.type == "function_call"
    ]

    if not function_calls:
        print(response.output_text)
        break

    tool_outputs = []

    for function_call in function_calls:

        print("Tool requested:", function_call.name)

        arguments = json.loads(function_call.arguments)

        handler = TOOL_HANDLERS[function_call.name]
        tool_result = handler(**arguments)

        tool_outputs.append(
            {
                "type": "function_call_output",
                "call_id": function_call.call_id,
                "output": json.dumps(tool_result),
            }
        )

    response = client.responses.create(
        model="gpt-5.6-luna",
        previous_response_id=response.id,
        input=tool_outputs,
        tools=tools,
    )