from openai import OpenAI
from dotenv import load_dotenv

from prooffit.tools import (
    TOOL_HANDLERS,
    TOOLS
)

from prooffit.tool_runner import run_tool_loop

load_dotenv()

client = OpenAI()

response = client.responses.create(
    model="gpt-5.6-luna",
    input="Find the candidate's evidence for Kubernetes experience and tell me what CV versions are available.",
    tools=TOOLS,
)

max_steps = 5
step = 0

response = run_tool_loop(
    client=client,
    response=response,
    tools=TOOLS,
    tool_handlers=TOOL_HANDLERS,
)

print(response.output_text)