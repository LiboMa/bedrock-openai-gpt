"""
Test harness for the Bedrock OpenAI GPT example scripts.

Two layers of checking:
  1. Syntax check  - py_compile every example script (catches import/syntax errors).
  2. Live API test - exercise the real bedrock-mantle endpoint via AWS SigV4 (curl),
                     including a tool-calling request so the flat Responses API tool
                     schema is actually validated by the service.

Auth: uses the standard AWS credential chain (botocore). No Bedrock API key needed.
"""

import json
import os
import subprocess
import sys

# NOTE: botocore is imported lazily inside the live-test path (see _get_credentials)
# so that `python3 test_all.py --syntax-only` runs without botocore installed.

# --- Scripts to syntax-check -------------------------------------------------

SCRIPTS = [
    "gpt55_responses.py",
    "gpt55_reasoning.py",
    "gpt55_streaming.py",
    "gpt55_tool_calling.py",
    "gpt54_responses.py",
    "gpt54_streaming.py",
    "gpt54_tool_calling.py",
    "gpt54_multi_region.py",
    "gpt56_chat_completions.py",
    "gpt6_bedrock_runtime.py",
]


def syntax_check():
    print("=== Syntax check all scripts ===\n")
    all_ok = True
    for script in SCRIPTS:
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", script],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print(f"  {script}: OK")
        else:
            all_ok = False
            print(f"  {script}: FAIL\n{result.stderr.strip()}")
    return all_ok


# --- Live API test (AWS SigV4 via curl) --------------------------------------

_CREDENTIALS = None


def _get_credentials():
    """Lazily resolve AWS credentials from the standard credential chain.

    botocore is imported here (not at module top level) so that the
    syntax-only mode does not require botocore to be installed.
    """
    global _CREDENTIALS
    if _CREDENTIALS is None:
        import botocore.session

        _CREDENTIALS = botocore.session.get_session().get_credentials()
    return _CREDENTIALS


def _post(region, body, timeout=60):
    """POST a JSON body to the responses endpoint using AWS SigV4. Returns parsed JSON."""
    credentials = _get_credentials()
    if credentials is None:
        raise RuntimeError("No AWS credentials found in the standard credential chain.")
    creds = credentials.get_frozen_credentials()

    cmd = [
        "curl", "-s", "--fail-with-body",
        "--aws-sigv4", f"aws:amz:{region}:bedrock",
        "--user", f"{creds.access_key}:{creds.secret_key}",
        "-H", "Content-Type: application/json",
        "-X", "POST", f"https://bedrock-mantle.{region}.api.aws/openai/v1/responses",
        "-d", json.dumps(body),
    ]
    # Session tokens (temporary credentials) must be passed via header.
    if creds.token:
        cmd[-3:-3] = ["-H", f"x-amz-security-token: {creds.token}"]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if not result.stdout:
        raise RuntimeError(f"empty response (curl exit {result.returncode}): {result.stderr.strip()}")
    return json.loads(result.stdout)


def _extract_text(resp):
    """Pull assistant text out of a Responses API payload, skipping reasoning items."""
    for item in resp.get("output", []):
        if item.get("type") == "message":
            for content in item.get("content", []):
                if content.get("type") in ("output_text", "text") and content.get("text"):
                    return content["text"]
    return ""


def _find_function_call(resp):
    """Return the first function_call item in a Responses API payload, if any."""
    for item in resp.get("output", []):
        if item.get("type") == "function_call":
            return item
    return None


def test_text(model, region):
    """Basic text generation: expect status completed and some text back."""
    body = {"model": model, "input": "Say hello in one word."}
    resp = _post(region, body)
    if resp.get("status") != "completed":
        return False, f"status={resp.get('status')} {resp.get('error') or json.dumps(resp)[:120]}"
    text = _extract_text(resp)
    if not text:
        return False, f"no text in output: {json.dumps(resp)[:120]}"
    return True, text.strip()[:80]


def test_tools(model, region):
    """Tool calling: validates the flat Responses API tool schema end to end."""
    body = {
        "model": model,
        "input": "What's the weather like in Seattle?",
        "tools": [
            {
                "type": "function",
                "name": "get_weather",
                "description": "Get the current weather for a location.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "City name"},
                    },
                    "required": ["location"],
                },
            }
        ],
    }
    resp = _post(region, body)
    # A validation_error (e.g. the old nested schema) surfaces here as an "error" field.
    if resp.get("error"):
        return False, f"{resp['error'].get('code')}: {resp['error'].get('message')}"
    if resp.get("status") != "completed":
        return False, f"status={resp.get('status')} {json.dumps(resp)[:120]}"
    call = _find_function_call(resp)
    if call is None:
        # Model answered with text instead of calling the tool; schema still valid.
        return True, f"no tool call (text: {_extract_text(resp)[:60]!r})"
    return True, f"called {call.get('name')}({call.get('arguments')})"


def live_tests():
    print("\n=== Live API test (AWS SigV4 via curl) ===\n")
    text_targets = [
        ("openai.gpt-5.5", "us-east-2"),
        ("openai.gpt-5.4", "us-east-2"),
        ("openai.gpt-5.4", "us-west-2"),
        ("openai.gpt-5.6-sol", "us-east-1"),
    ]
    tool_targets = [
        ("openai.gpt-5.5", "us-east-2"),
        ("openai.gpt-5.4", "us-east-2"),
        ("openai.gpt-5.6-sol", "us-east-1"),
    ]

    all_ok = True
    for model, region in text_targets:
        print(f"  [text]  {model} @ {region} ... ", end="", flush=True)
        try:
            ok, msg = test_text(model, region)
        except Exception as e:
            ok, msg = False, f"{type(e).__name__}: {e}"
        all_ok &= ok
        print(f"{'PASS' if ok else 'FAIL'} {msg}")

    for model, region in tool_targets:
        print(f"  [tools] {model} @ {region} ... ", end="", flush=True)
        try:
            ok, msg = test_tools(model, region)
        except Exception as e:
            ok, msg = False, f"{type(e).__name__}: {e}"
        all_ok &= ok
        print(f"{'PASS' if ok else 'FAIL'} {msg}")

    return all_ok


def main():
    syntax_ok = syntax_check()

    if "--syntax-only" in sys.argv:
        print("\nSyntax-only mode (skipping live tests).")
        return 0 if syntax_ok else 1

    try:
        live_ok = live_tests()
    except Exception as e:
        print(f"\nLive tests could not run: {type(e).__name__}: {e}")
        live_ok = False

    print("\nDone.")
    return 0 if (syntax_ok and live_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
