# Contributing

Thanks for your interest in the SmartlyQ Python SDK!

## How this repo works

Most of this SDK is **generated** from the [SmartlyQ OpenAPI spec](https://docs.smartlyq.com):

- `smartlyq/resources.py` - emitted by `scripts/generate_client.py`. Never edit by hand.
- `tests/test_endpoints_gen.py` - emitted by `scripts/generate_tests.py`. Never edit by hand.
- The README's API Reference section - emitted by `scripts/generate_readme.py`.

Hand-written code lives in `smartlyq/_core.py`, `smartlyq/__init__.py`, `scripts/`, and `tests/test_core.py`. Fixes to generated output belong in the generator scripts, or in the OpenAPI spec itself.

```bash
pip install httpx pytest build
python scripts/generate_client.py && python scripts/generate_readme.py && python scripts/generate_tests.py
python -m pytest
```

## Never commit secrets

This is a **public** repository. Never commit real API keys (`sqk_live_...` / `sqk_test_...`), credentials, tokens, internal hostnames, or customer data. Use placeholders like `sqk_live_xxxxxxxxxxxx` or `YOUR_API_KEY` in examples.

Enable the local pre-commit scan once per clone:

```bash
git config core.hooksPath .githooks
```

CI also runs a gitleaks scan on every push and pull request. If you believe a secret has been exposed, rotate it immediately in your Developer Dashboard.
