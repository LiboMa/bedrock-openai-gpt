"""
GPT-5.6 Sol on Amazon Bedrock - Chat Completions API (bedrock-mantle endpoint)
Ref: https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-openai-gpt-56-sol.html

All OpenAI GPT models on Bedrock support BOTH the Responses API and the
Chat Completions API, on BOTH the bedrock-mantle (Metal API) and the
bedrock-runtime (Runtime API) endpoints. This example shows the Chat
Completions API against the bedrock-mantle endpoint (OpenAI-compatible).

ENDPOINT / MODEL-ID PAIRING (important):
  This example uses the bedrock-mantle endpoint with the BASE model ID
  (openai.gpt-5.6-sol). If you point OPENAI_BASE_URL at bedrock-runtime you
  MUST also switch the model to a cross-Region inference (CRIS) ID with a
  us./global. prefix (e.g. us.openai.gpt-5.6-sol) -- see gpt6_bedrock_runtime.py
  for a Runtime-endpoint example. The bedrock_endpoints.resolve() helper
  enforces this pairing and fails fast with guidance on a mismatch.

Prerequisites:
  pip install openai        # openai>=1.78.0

Environment variables:
  OPENAI_API_KEY      - Your Bedrock API key (or fall back to AWS SigV4 credentials)
  OPENAI_BASE_URL     - https://bedrock-mantle.{region}.api.aws/openai/v1
  AWS_REGION          - region for the default base URL (default: us-east-1)
"""

import os
from openai import OpenAI
from bedrock_endpoints import mantle_base_url, resolve

MODEL = "openai.gpt-5.6-sol"  # base ID -> bedrock-mantle (Metal API)
BASE_URL = resolve(MODEL, mantle_base_url())

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"), base_url=BASE_URL)

# Chat Completions API: the classic messages[] format with system/user roles.
completion = client.chat.completions.create(
    model=MODEL,
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
