"""
GPT-5.4 on Amazon Bedrock - Test across all available regions
Ref: https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-openai-gpt-54.html

Available Regions: us-east-2, us-west-2

Environment variables:
  OPENAI_API_KEY - Your Bedrock API key
"""

import os
from openai import OpenAI

API_KEY = os.environ.get("OPENAI_API_KEY")
REGIONS = ["us-east-2", "us-west-2"]

for region in REGIONS:
    base_url = f"https://bedrock-mantle.{region}.api.aws/openai/v1"
    print(f"--- Testing GPT-5.4 in {region} ({base_url}) ---")

    try:
        client = OpenAI(api_key=API_KEY, base_url=base_url)
        response = client.responses.create(
            model="openai.gpt-5.4",
            input="Say hello and tell me which region you are responding from.",
        )
        print(f"✅ Success: {response.output_text[:200]}")
    except Exception as e:
        print(f"❌ Failed: {e}")

    print()
