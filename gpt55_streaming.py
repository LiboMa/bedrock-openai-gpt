"""
GPT-5.5 on Amazon Bedrock - Streaming responses
Ref: https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-openai-gpt-55.html

Environment variables:
  OPENAI_API_KEY      - Your Bedrock API key
  OPENAI_BASE_URL     - https://bedrock-mantle.us-east-2.api.aws/openai/v1
"""

import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get("OPENAI_BASE_URL", "https://bedrock-mantle.us-east-2.api.aws/openai/v1"),
)

stream = client.responses.create(
    model="openai.gpt-5.5",
    input="Write a Python function to implement binary search.",
    stream=True,
)

for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)

print()
