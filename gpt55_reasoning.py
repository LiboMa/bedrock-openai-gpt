"""
GPT-5.5 on Amazon Bedrock - Multi-turn with reasoning effort control
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

response = client.responses.create(
    model="openai.gpt-5.5",
    input=[
        {
            "role": "developer",
            "content": "You are a senior AWS solutions architect. Be concise and practical.",
        },
        {
            "role": "user",
            "content": "Design a serverless architecture for a real-time chat application that handles 50k concurrent users.",
        },
    ],
    reasoning={"effort": "medium"},
)

print(response.output_text)
