"""
GPT-5.5 on Amazon Bedrock via Responses API (bedrock-mantle endpoint)
Ref: https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-openai-gpt-55.html

ENDPOINT / MODEL-ID PAIRING (important):
  This example uses the bedrock-mantle (Metal API) endpoint together with the
  BASE model ID (openai.gpt-5.5). If you switch OPENAI_BASE_URL to a
  bedrock-runtime URL you MUST also switch the model to a cross-Region
  inference (CRIS) ID with a us./global. prefix (e.g. us.openai.gpt-5.5) --
  see gpt6_bedrock_runtime.py. The bedrock_endpoints.resolve() helper enforces
  this pairing and fails fast with guidance on a mismatch.

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

MODEL = "openai.gpt-5.5"  # base ID -> bedrock-mantle (Metal API)
BASE_URL = resolve(MODEL, mantle_base_url())

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"), base_url=BASE_URL)

response = client.responses.create(
    model=MODEL,
    input="Can you explain the features of Amazon Bedrock?",
)

print(response.output_text)
