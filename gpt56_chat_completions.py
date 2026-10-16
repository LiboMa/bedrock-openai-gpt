"""
GPT-5.6 Sol on Amazon Bedrock - Chat Completions API (bedrock-mantle endpoint)
Ref: https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-openai-gpt-56-sol.html

All OpenAI GPT models on Bedrock support BOTH the Responses API and the
Chat Completions API, on BOTH the bedrock-mantle (Metal API) and the
bedrock-runtime (Runtime API) endpoints. This example shows the Chat
Completions API against the bedrock-mantle endpoint (OpenAI-compatible,
base model ID).

Prerequisites:
  pip install openai        # openai>=1.78.0

Environment variables:
  OPENAI_API_KEY      - Your Bedrock API key (or fall back to AWS SigV4 credentials)
  OPENAI_BASE_URL     - https://bedrock-mantle.{region}.api.aws/openai/v1
"""

import os
from openai import OpenAI

REGION = os.environ.get("AWS_REGION", "us-east-1")

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    base_url=os.environ.get(
        "OPENAI_BASE_URL",
        f"https://bedrock-mantle.{REGION}.api.aws/openai/v1",
    ),
)

# Chat Completions API: the classic messages[] format with system/user roles.
# On bedrock-mantle use the base model ID (e.g. openai.gpt-5.6-sol).
completion = client.chat.completions.create(
    model="openai.gpt-5.6-sol",
    messages=[
        {
            "role": "system",
            "content": "You are a senior AWS solutions architect. Be concise and practical.",
        },
        {
            "role": "user",
            "content": "List three best practices for a serverless architecture.",
        },
    ],
)

print(completion.choices[0].message.content)
