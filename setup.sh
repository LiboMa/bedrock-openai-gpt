#!/bin/bash
# Quick setup for Amazon Bedrock OpenAI GPT examples

set -e

echo "=== Installing dependencies ==="
pip install -r requirements.txt

echo ""
echo "=== Setup complete ==="
echo ""
echo "Configure your environment (choose ONE endpoint):"
echo '  export OPENAI_API_KEY="<your-bedrock-api-key>"'
echo ""
echo "  # Option A (recommended): bedrock-runtime (Runtime API)"
echo "  #   Use a cross-Region inference ID, e.g. us.openai.gpt-5.5 / global.openai.gpt-5.5"
echo '  export OPENAI_BASE_URL="https://bedrock-runtime.us-east-1.amazonaws.com/openai/v1"'
echo ""
echo "  # Option B: bedrock-mantle (Metal API, OpenAI-compatible)"
echo "  #   Use the base model ID, e.g. openai.gpt-5.5"
echo '  # export OPENAI_BASE_URL="https://bedrock-mantle.us-east-1.api.aws/openai/v1"'
echo ""
echo "Both endpoints support the Responses API and the Chat Completions API (base path /openai/v1)."
echo "AWS recommends bedrock-runtime for new applications."
echo ""
echo "Then run:"
echo "  python gpt55_responses.py"
