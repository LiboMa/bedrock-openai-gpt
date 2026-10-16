"""
GPT-5.4 on Amazon Bedrock - Test across multiple bedrock-mantle regions
Ref: https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-openai-gpt-54.html

This example sweeps the bedrock-mantle (Metal API) endpoint across several
regions using the BASE model ID (openai.gpt-5.4) -- endpoint and ID stay
consistent (base ID + Mantle). GPT-5.4 is also offered in GovCloud (US-West,
us-gov-west-1); add it to REGIONS if your account/credentials target GovCloud.
For the full regional matrix, see the model card's
"Regional availability at a glance" and the Regions page:
  https://docs.aws.amazon.com/bedrock/latest/userguide/models-region-compatibility.html

Environment variables:
  OPENAI_API_KEY - Your Bedrock API key
"""

import os
from openai import OpenAI

API_KEY = os.environ.get("OPENAI_API_KEY")
MODEL = "openai.gpt-5.4"  # base ID -> bedrock-mantle (Metal API)

# bedrock-mantle (Metal API) regions for GPT-5.4. GovCloud (us-gov-west-1) is
# also supported but uses a separate partition; add it if applicable.
REGIONS = ["us-east-1", "us-east-2", "us-west-2"]

for region in REGIONS:
    base_url = f"https://bedrock-mantle.{region}.api.aws/openai/v1"
    print(f"--- Testing GPT-5.4 in {region} ({base_url}) ---")

    try:
        client = OpenAI(api_key=API_KEY, base_url=base_url)
        response = client.responses.create(
            model=MODEL,
            input="Say hello and tell me which region you are responding from.",
        )
        print(f"✅ Success: {response.output_text[:200]}")
    except Exception as e:
        print(f"❌ Failed: {e}")

    print()
