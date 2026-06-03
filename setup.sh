#!/bin/bash
# Quick setup for Amazon Bedrock OpenAI GPT examples

set -e

echo "=== Installing dependencies ==="
pip install -r requirements.txt

echo ""
echo "=== Setup complete ==="
echo ""
echo "Configure your environment:"
echo '  export OPENAI_API_KEY="<your-bedrock-api-key>"'
echo '  export OPENAI_BASE_URL="https://bedrock-mantle.us-east-2.api.aws/openai/v1"'
echo ""
echo "Then run:"
echo "  python gpt55_responses.py"
