"""
GPT-5.4 on Amazon Bedrock - Function/Tool calling example (bedrock-mantle)
Ref: https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-openai-gpt-54.html

Uses the bedrock-mantle (Metal API) endpoint with the BASE model ID
(openai.gpt-5.4). Point OPENAI_BASE_URL at bedrock-runtime only if you also
switch the model to a CRIS ID (us./global. prefix); resolve() enforces this.

Environment variables:
  OPENAI_API_KEY      - Your Bedrock API key (or fall back to AWS SigV4 credentials)
  OPENAI_BASE_URL     - https://bedrock-mantle.{region}.api.aws/openai/v1
  AWS_REGION          - region for the default base URL (default: us-east-1)
"""

import os
from openai import OpenAI
from bedrock_endpoints import mantle_base_url, resolve

MODEL = "openai.gpt-5.4"  # base ID -> bedrock-mantle (Metal API)
BASE_URL = resolve(MODEL, mantle_base_url())

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"), base_url=BASE_URL)

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
    model=MODEL,
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
