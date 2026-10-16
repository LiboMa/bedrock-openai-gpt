"""
Shared endpoint/model-ID helpers for the Bedrock OpenAI GPT examples.

Why this exists
---------------
Amazon Bedrock exposes the OpenAI GPT models through two endpoints:

  * bedrock-mantle  (Metal API)   https://bedrock-mantle.{region}.api.aws/openai/v1
      -> OpenAI-compatible, uses the BASE model ID        (e.g. openai.gpt-5.5)
  * bedrock-runtime (Runtime API) https://bedrock-runtime.{region}.amazonaws.com/openai/v1
      -> standard Bedrock Runtime; GPT models need a CROSS-REGION
         INFERENCE (CRIS) ID with a us./global. prefix
         (e.g. us.openai.gpt-5.5 / global.openai.gpt-5.5; GPT-5.6 Terra/Luna
         also have an in. Geo ID for the India Regions)

The endpoint and the model-ID form MUST match. Sending a base ID to
bedrock-runtime (or a CRIS ID to bedrock-mantle) is a configuration error the
service rejects. These helpers let every example pick a self-consistent
base_url + model ID and fail fast with a clear message if OPENAI_BASE_URL is
pointed at an incompatible endpoint.

Note: the GPT OSS models (gpt-oss-*, gpt-oss-safeguard-*) are an exception --
they use In-Region base IDs on bedrock-runtime and the /v1 base path on
bedrock-mantle. None of the examples here target them, so resolve() applies
the GPT-family rule only.
"""

import os

# us./global. are the GPT CRIS scopes; in. is the India Geo scope (GPT-5.6
# Terra/Luna); us-gov. is the GovCloud Geo scope; eu./apac. are kept so that
# CRIS IDs of other Bedrock model families are still recognised.
CRIS_PREFIXES = ("us.", "global.", "in.", "us-gov.", "eu.", "apac.")


def is_cris_id(model_id):
    """True if model_id is a cross-Region inference ID (see CRIS_PREFIXES)."""
    return model_id.startswith(CRIS_PREFIXES)


def mantle_base_url(region=None):
    """bedrock-mantle (Metal API) base URL for the given region (default from AWS_REGION)."""
    region = region or os.environ.get("AWS_REGION", "us-east-1")
    return f"https://bedrock-mantle.{region}.api.aws/openai/v1"


def runtime_base_url(region=None):
    """bedrock-runtime (Runtime API) base URL for the given region (default from AWS_REGION)."""
    region = region or os.environ.get("AWS_REGION", "us-east-1")
    return f"https://bedrock-runtime.{region}.amazonaws.com/openai/v1"


def resolve(model_id, default_base_url):
    """Resolve the effective base_url and verify it is compatible with model_id.

    OPENAI_BASE_URL (if set) overrides default_base_url. We then check that a
    base ID is paired with bedrock-mantle and a CRIS ID with bedrock-runtime,
    raising SystemExit with actionable guidance on a mismatch rather than
    letting the request silently hit the wrong endpoint.
    """
    base_url = os.environ.get("OPENAI_BASE_URL", default_base_url)
    cris = is_cris_id(model_id)

    if "bedrock-runtime" in base_url and not cris:
        raise SystemExit(
            f"OPENAI_BASE_URL points at bedrock-runtime but model '{model_id}' is a "
            f"base ID.\nUse bedrock-mantle for base IDs, or switch the model to a CRIS "
            f"ID such as us.{model_id} / global.{model_id} (see gpt6_bedrock_runtime.py)."
        )
    if "bedrock-mantle" in base_url and cris:
        base = model_id.split(".", 1)[1]
        raise SystemExit(
            f"OPENAI_BASE_URL points at bedrock-mantle but model '{model_id}' is a CRIS "
            f"ID.\nUse bedrock-runtime for CRIS IDs, or switch the model to the base ID "
            f"'{base}' for the Mantle endpoint."
        )
    return base_url
