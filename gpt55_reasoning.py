"""
GPT-5.5 on Amazon Bedrock - Multi-turn with reasoning effort control (bedrock-mantle)
Ref: https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-openai-gpt-55.html

Uses the bedrock-mantle (Metal API) endpoint with the BASE model ID
(openai.gpt-5.5). Point OPENAI_BASE_URL at bedrock-runtime only if you also
switch the model to a CRIS ID (us./global. prefix); resolve() enforces this.

Environment variables:
  OPENAI_API_KEY      - Your Bedrock API key (or fall back to AWS SigV4 credentials)
  OPENAI_BASE_URL     - https://bedrock-mantle.{region}.api.aws/openai/v1
  AWS_REGION          - region for the default base URL (default: us-east-1)
"""

import os
from openai import OpenAI
from bedrock_endpoints import mantle_base_url, resolve

MODEL = "openai.gpt-5.5"  # base ID -> bedrock-mantle (Metal API)
BASE_URL = resolve(MODEL, mantle_base_url())

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"), base_url=BASE_URL)

response = client.responses.create(
    model=MODEL,
    input=[
        {
            "role": "developer",
            "content": "You are a senior AWS solutions architect. Be concise and practical.",
        },
        {
            "role": "user",
            "content": "Design a serverless architecture for a real-time chat application that handles 50k concurrent users.",
        },
    ],
    reasoning={"effort": "medium"},
)

print(response.output_text)
