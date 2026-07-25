"""SmartlyQ SDK core HTTP client.

Hand-written; the resource surface in ``resources.py`` is generated on top of it.
"""

from __future__ import annotations

import os
import random
import time
from typing import Any, Optional

import httpx

from ._version import __version__

RETRYABLE_STATUSES = {429, 500, 502, 503, 504}


class SmartlyQError(Exception):
    """Raised for any non-2xx API response."""

    def __init__(self, status_code: int, envelope: Optional[dict], fallback: str):
        error = (envelope or {}).get("error") or {}
        meta = (envelope or {}).get("meta") or {}
        super().__init__(error.get("message") or fallback)
        self.status_code: int = status_code
        self.code: Optional[str] = error.get("code")
        self.details: Optional[dict] = error.get("details")
        self.request_id: Optional[str] = meta.get("request_id")


class SmartlyQConnectionError(Exception):
    """Raised when a request cannot reach the API (network failure, timeout)."""


class CoreClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        base_url: str = "https://api.smartlyq.com/v1",
        timeout: float = 60.0,
        max_retries: int = 2,
        default_headers: Optional[dict[str, str]] = None,
        transport: Optional[httpx.BaseTransport] = None,
    ):
        api_key = api_key or os.environ.get("SMARTLYQ_API_KEY")
        if not api_key:
            raise ValueError(
                "Missing API key. Pass api_key to the client or set the "
                "SMARTLYQ_API_KEY environment variable."
            )
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries
        self._default_headers = default_headers or {}
        self._client = httpx.Client(transport=transport, timeout=timeout)

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "CoreClient":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def request(
        self,
        method: str,
        path: str,
        *,
        body: Optional[dict] = None,
        query: Optional[dict] = None,
        profile_id: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        timeout: Optional[float] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> Any:
        url = self._base_url + path
        request_headers: dict[str, str] = {
            "Authorization": f"Bearer {self._api_key}",
            "Accept": "application/json",
            "User-Agent": f"smartlyq-python/{__version__}",
            **self._default_headers,
            **(headers or {}),
        }
        if profile_id:
            request_headers["X-Profile-Id"] = profile_id
        if idempotency_key:
            request_headers["Idempotency-Key"] = idempotency_key

        params = {k: v for k, v in (query or {}).items() if v is not None}
        last_exc: Optional[Exception] = None

        for attempt in range(self._max_retries + 1):
            try:
                response = self._client.request(
                    method,
                    url,
                    json=body,
                    params=params or None,
                    headers=request_headers,
                    timeout=timeout if timeout is not None else self._timeout,
                )
            except httpx.HTTPError as exc:
                last_exc = exc
                if attempt < self._max_retries:
                    time.sleep(_backoff(attempt))
                    continue
                raise SmartlyQConnectionError(f"Request failed: {exc}") from exc

            if response.is_success:
                if response.status_code == 204 or not response.content:
                    return None
                return response.json()

            try:
                envelope = response.json()
            except ValueError:
                envelope = None

            if response.status_code in RETRYABLE_STATUSES and attempt < self._max_retries:
                retry_after = _parse_retry_after(response.headers.get("Retry-After"))
                time.sleep(retry_after if retry_after is not None else _backoff(attempt))
                continue

            raise SmartlyQError(response.status_code, envelope, f"HTTP {response.status_code}")

        raise SmartlyQConnectionError(f"Request failed: {last_exc}")


def _backoff(attempt: int) -> float:
    base = 0.5 * (2**attempt)
    return base + random.random() * base * 0.25


def _parse_retry_after(value: Optional[str]) -> Optional[float]:
    if not value:
        return None
    try:
        seconds = float(value)
    except ValueError:
        return None
    return seconds if seconds > 0 else None
