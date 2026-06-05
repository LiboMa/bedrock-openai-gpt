"""
GPT-5.4 on Amazon Bedrock - Function/Tool calling example
Ref: https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-openai-gpt-54.html

Environment variables:
  OPENAI_API_KEY      - Your Bedrock API key
  OPENAI_BASE_URL     - https://bedrock-mantle.{region}.api.aws/openai/v1
"""

import os
from openai import OpenAI

REGION = os.environ.get("AWS_REGION", "us-east-2")

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_BASE_URL", f"https://bedrock-mantle.{REGION}.api.aws/openai/v1"),
)

# Responses API uses a FLAT tool schema: name/description/parameters
# sit at the top level alongside "type" (NOT nested under "function").
tools = [
    {
        "type": "function",
        "name": "get_stock_price",
        "description": "Get the current stock price for a given ticker symbol.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {"type": "string", "description": "Stock ticker symbol, e.g. AMZN"},
            },
            "required": ["ticker"],
        },
    }
]

response = client.responses.create(
    model="openai.gpt-5.4",
    input="What's the current stock price of Amazon?",
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
