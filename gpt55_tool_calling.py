"""
GPT-5.5 on Amazon Bedrock - Function/Tool calling example
Ref: https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-openai-gpt-55.html

Environment variables:
  OPENAI_API_KEY      - Your Bedrock API key
  OPENAI_BASE_URL     - https://bedrock-mantle.us-east-2.api.aws/openai/v1
"""

import os
import json
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_BASE_URL", "https://bedrock-mantle.us-east-2.api.aws/openai/v1"),
)

# Responses API uses a FLAT tool schema: name/description/parameters
# sit at the top level alongside "type" (NOT nested under "function").
tools = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "Get the current weather for a location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City name"},
            },
            "required": ["location"],
        },
    }
]

response = client.responses.create(
    model="openai.gpt-5.5",
    input="What's the weather like in Seattle?",
    tools=tools,
)

for item in response.output:
    if item.type == "function_call":
        print(f"Function: {item.name}")
        print(f"Arguments: {item.arguments}")
    elif hasattr(item, "content"):
        for content in item.content:
            if hasattr(content, "text"):
                print(content.text)
