#!/bin/bash
# Quick setup for Amazon Bedrock OpenAI GPT examples

set -e

echo "=== Installing dependencies ==="
pip install -r requirements.txt

echo ""
echo "=== Setup complete ==="
echo ""
echo "Configure your environment (choose ONE endpoint)."
echo "IMPORTANT: the endpoint and the model-ID form must MATCH:"
echo "  * bedrock-runtime (Runtime API) -> cross-Region inference (CRIS) IDs"
echo "    with a us./global. prefix, e.g. us.openai.gpt-6-astra"
echo "  * bedrock-mantle  (Metal API)   -> BASE model IDs, e.g. openai.gpt-5.5"
echo "Do NOT point one OPENAI_BASE_URL at both kinds of script; the demos will"
echo "fail fast with guidance if an incompatible endpoint/ID pair is detected."
echo ""
echo '  export OPENAI_API_KEY="<your-bedrock-api-key>"'
echo ""
echo "  # Option A (recommended by AWS for new apps): bedrock-runtime (Runtime API)"
echo "  #   Pair with a CRIS ID, e.g. us.openai.gpt-6-astra / global.openai.gpt-6-astra"
echo '  export OPENAI_BASE_URL="https://bedrock-runtime.us-east-1.amazonaws.com/openai/v1"'
echo ""
echo "  # Option B: bedrock-mantle (Metal API, OpenAI-compatible)"
echo "  #   Pair with the base ID, e.g. openai.gpt-5.5 / openai.gpt-5.6-sol"
echo '  # export OPENAI_BASE_URL="https://bedrock-mantle.us-east-1.api.aws/openai/v1"'
echo ""
echo "Both endpoints support the Responses API and the Chat Completions API (base path /openai/v1)."
echo ""
echo "Then run an example that MATCHES your chosen endpoint:"
echo "  # Option A (bedrock-runtime, CRIS IDs):"
echo "  python gpt6_bedrock_runtime.py"
echo "  # Option B (bedrock-mantle, base IDs):"
echo "  #   python gpt55_responses.py        # Responses API"
echo "  #   python gpt56_chat_completions.py # Chat Completions API"
