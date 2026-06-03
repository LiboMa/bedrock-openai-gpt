"""
GPT-5.4 on Amazon Bedrock via Responses API (bedrock-mantle endpoint)
Ref: https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-openai-gpt-54.html

Available Regions: us-east-2, us-west-2

Prerequisites:
  pip install openai

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

response = client.responses.create(
    model="openai.gpt-5.4",
    input="Can you explain the features of Amazon Bedrock?",
)

print(response.output_text)
