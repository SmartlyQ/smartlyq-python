import httpx
import pytest

from smartlyq import SmartlyQ, SmartlyQError


def make_client(handler, **kwargs):
    return SmartlyQ(
        "sqk_test_xxxxxxxxxxxx", transport=httpx.MockTransport(handler), **kwargs
    )


def test_sends_bearer_token():
    seen = {}

    def handler(request):
        seen["auth"] = request.headers.get("Authorization")
        return httpx.Response(200, json={"success": True})

    with make_client(handler) as sq:
        sq.account.get_me()
    assert seen["auth"] == "Bearer sqk_test_xxxxxxxxxxxx"


def test_missing_api_key(monkeypatch):
    monkeypatch.delenv("SMARTLYQ_API_KEY", raising=False)
    with pytest.raises(ValueError, match="Missing API key"):
        SmartlyQ()


def test_query_params_skip_none():
    seen = {}

    def handler(request):
        seen["url"] = str(request.url)
        return httpx.Response(200, json={"success": True})

    with make_client(handler) as sq:
        sq.articles.list(query={"page": 2, "status": "draft", "search": None})
    assert "page=2" in seen["url"] and "status=draft" in seen["url"]
    assert "search" not in seen["url"]


def test_error_envelope_parsing():
    def handler(request):
        return httpx.Response(
            402,
            json={
                "success": False,
                "error": {"code": "INSUFFICIENT_CREDITS", "message": "Not enough credits"},
                "meta": {"request_id": "req_1"},
            },
        )

    with make_client(handler, max_retries=0) as sq:
        with pytest.raises(SmartlyQError) as exc:
            sq.images.generate({"prompt": "x"})
    assert exc.value.status_code == 402
    assert exc.value.code == "INSUFFICIENT_CREDITS"
    assert exc.value.request_id == "req_1"


def test_retries_on_429_then_succeeds():
    attempts = {"n": 0}

    def handler(request):
        attempts["n"] += 1
        if attempts["n"] < 3:
            return httpx.Response(429, json={"success": False}, headers={"Retry-After": "0"})
        return httpx.Response(200, json={"success": True})

    with make_client(handler, max_retries=2) as sq:
        sq.account.get_me()
    assert attempts["n"] == 3


def test_no_retry_on_400():
    attempts = {"n": 0}

    def handler(request):
        attempts["n"] += 1
        return httpx.Response(400, json={"success": False, "error": {"message": "bad"}})

    with make_client(handler, max_retries=2) as sq:
        with pytest.raises(SmartlyQError, match="bad"):
            sq.account.get_me()
    assert attempts["n"] == 1


def test_profile_and_idempotency_headers():
    seen = {}

    def handler(request):
        seen["profile"] = request.headers.get("X-Profile-Id")
        seen["idem"] = request.headers.get("Idempotency-Key")
        return httpx.Response(200, json={"success": True})

    with make_client(handler) as sq:
        sq.social.create_post({}, profile_id="prof_1", idempotency_key="idem_1")
    assert seen == {"profile": "prof_1", "idem": "idem_1"}
