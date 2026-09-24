import json


def run_tool_loop(
    client,
    response,
    tools,
    tool_handlers,
    max_steps: int = 5,
    text_format=None,
):
    step = 0

    while True:
        step += 1

        if step > max_steps:
            raise RuntimeError("Maximum tool steps reached.")

        function_calls = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

        if not function_calls:
            return response

        tool_outputs = []

        for function_call in function_calls:
            arguments = json.loads(function_call.arguments)

            handler = tool_handlers[function_call.name]
            tool_result = handler(**arguments)

            tool_outputs.append(
                {
                    "type": "function_call_output",
                    "call_id": function_call.call_id,
                    "output": json.dumps(tool_result),
                }
            )

        if text_format is not None:
            response = client.responses.parse(
                model="gpt-5.6-luna",
                previous_response_id=response.id,
                input=tool_outputs,
                tools=tools,
                text_format=text_format,
            )
        else:
            response = client.responses.create(
                model="gpt-5.6-luna",
                previous_response_id=response.id,
                input=tool_outputs,
                tools=tools,
            )