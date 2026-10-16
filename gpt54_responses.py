"""
GPT-5.4 on Amazon Bedrock via Responses API (bedrock-mantle endpoint)
Ref: https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-openai-gpt-54.html

Uses the bedrock-mantle (Metal API) endpoint with the BASE model ID
(openai.gpt-5.4). GPT-5.4 is also available in GovCloud (US-West); set
AWS_REGION=us-gov-west-1 to target it. Point OPENAI_BASE_URL at bedrock-runtime
only if you also switch the model to a CRIS ID (us./global. prefix);
resolve() enforces this pairing.

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

MODEL = "openai.gpt-5.4"  # base ID -> bedrock-mantle (Metal API)
BASE_URL = resolve(MODEL, mantle_base_url())

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"), base_url=BASE_URL)

response = client.responses.create(
    model=MODEL,
    input="Can you explain the features of Amazon Bedrock?",
)

print(response.output_text)
