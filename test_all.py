"""Run all GPT scripts using AWS credentials (SigV4 via botocore)."""
import subprocess, sys, os

os.environ["OPENAI_BASE_URL"] = "https://bedrock-mantle.us-east-2.api.aws/openai/v1"

# Generate a temporary bearer token using AWS credentials
import botocore.session
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest

session = botocore.session.get_session()
credentials = session.get_credentials().get_frozen_credentials()

# For bedrock-mantle, we can use the access key directly as a workaround
# But the scripts need OPENAI_API_KEY, so let's create a signed request approach
# Actually, let's test with a simple wrapper

scripts = [
    "gpt55_responses.py",
    "gpt55_reasoning.py",
    "gpt55_streaming.py",
    "gpt55_tool_calling.py",
    "gpt54_responses.py",
    "gpt54_streaming.py",
    "gpt54_tool_calling.py",
    "gpt54_multi_region.py",
]

# Use a dummy key - the SigV4 curl test worked, so we need to adapt scripts
# to use botocore auth. For now, test syntax validity.
print("=== Syntax check all scripts ===\n")
for s in scripts:
    result = subprocess.run([sys.executable, "-m", "py_compile", s], capture_output=True, text=True)
    status = "✅ OK" if result.returncode == 0 else f"❌ {result.stderr.strip()}"
    print(f"  {s}: {status}")

print("\n=== Live API test (using AWS SigV4 via curl) ===\n")

import json

def test_model(model, region):
    ak = credentials.access_key
    sk = credentials.secret_key
    cmd = [
        "curl", "-s", "--aws-sigv4", f"aws:amz:{region}:bedrock",
        "--user", f"{ak}:{sk}",
        "-H", "Content-Type: application/json",
        "-X", "POST", f"https://bedrock-mantle.{region}.api.aws/openai/v1/responses",
        "-d", json.dumps({"model": model, "input": "Say hello in one word."})
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    try:
        resp = json.loads(result.stdout)
        if resp.get("status") == "completed":
            text = resp["output"][0]["content"][0]["text"]
            return True, text[:100]
        else:
            return False, resp.get("error", result.stdout[:100])
    except:
        return False, result.stdout[:100] + result.stderr[:100]

tests = [
    ("openai.gpt-5.5", "us-east-2"),
    ("openai.gpt-5.4", "us-east-2"),
    ("openai.gpt-5.4", "us-west-2"),
]

for model, region in tests:
    print(f"  {model} @ {region} ... ", end="", flush=True)
    ok, msg = test_model(model, region)
    print(f"{'✅' if ok else '❌'} {msg}")

print("\nDone.")
