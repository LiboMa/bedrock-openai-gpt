"""
GPT-6 on Amazon Bedrock - Runtime API (bedrock-runtime endpoint)
Ref: https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards-openai.html
     https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-openai-gpt-6-astra.html

Two endpoints expose the OpenAI GPT models on Bedrock:

  * bedrock-mantle  (Metal API)   https://bedrock-mantle.{region}.api.aws/openai/v1
      -> OpenAI-compatible, uses the BASE model ID (e.g. openai.gpt-6-astra)
  * bedrock-runtime (Runtime API) https://bedrock-runtime.{region}.amazonaws.com/openai/v1
      -> standard Bedrock Runtime, uses a CROSS-REGION INFERENCE (CRIS) ID
         (e.g. us.openai.gpt-6-astra / global.openai.gpt-6-astra)

AWS recommends bedrock-runtime for new applications. Both endpoints expose
the same base path /openai/v1 and both support the Responses API AND the
Chat Completions API. This example targets the bedrock-runtime endpoint.

Prerequisites:
  pip install openai        # openai>=1.78.0

Environment variables:
  OPENAI_API_KEY      - Your Bedrock API key (or fall back to AWS SigV4 credentials)
  OPENAI_BASE_URL     - https://bedrock-runtime.{region}.amazonaws.com/openai/v1
  BEDROCK_SCOPE       - CRIS scope prefix: "us" (Geo) or "global" (default: us)
  AWS_REGION          - region for the default base URL (default: us-east-1)
"""

import os
from openai import OpenAI

REGION = os.environ.get("AWS_REGION", "us-east-1")
# CRIS scope: Geo (us.) stays within the US geography; Global (global.) may
# route anywhere when there is no data-residency constraint.
SCOPE = os.environ.get("BEDROCK_SCOPE", "us")

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
    # bedrock-runtime endpoint (NOT bedrock-mantle). Base path is /openai/v1.
    base_url=os.environ.get(
        "OPENAI_BASE_URL",
        f"https://bedrock-runtime.{REGION}.amazonaws.com/openai/v1",
    ),
)

# On bedrock-runtime the model MUST be a cross-Region inference (CRIS) ID,
# i.e. prefixed with the scope: us.openai.gpt-6-astra or global.openai.gpt-6-astra.
model_id = f"{SCOPE}.openai.gpt-6-astra"

# 1) Responses API over bedrock-runtime
response = client.responses.create(
    model=model_id,
    input="Explain the main features of Amazon Bedrock in two sentences.",
)
print("--- Responses API (bedrock-runtime) ---")
print(response.output_text)

# 2) Chat Completions API over the same bedrock-runtime endpoint
completion = client.chat.completions.create(
    model=model_id,
    messages=[
        {"role": "system", "content": "You are concise."},
        {"role": "user", "content": "Name one benefit of cross-Region inference."},
    ],
)
print("\n--- Chat Completions API (bedrock-runtime) ---")
print(completion.choices[0].message.content)
