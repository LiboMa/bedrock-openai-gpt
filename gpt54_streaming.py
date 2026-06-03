"""
GPT-5.4 on Amazon Bedrock - Streaming responses
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

stream = client.responses.create(
    model="openai.gpt-5.4",
    input="Explain the difference between GPT-5.5 and GPT-5.4 on Amazon Bedrock.",
    stream=True,
)

for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)

print()
