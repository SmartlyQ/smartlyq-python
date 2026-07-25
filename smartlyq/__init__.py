"""SmartlyQ Python SDK.

Example:
    from smartlyq import SmartlyQ

    sq = SmartlyQ(api_key="sqk_live_...")
    me = sq.account.get_me()
    post = sq.social.create_post({"text": "Hello!", "account_ids": ["acc_123"]})
"""

from __future__ import annotations

from typing import Optional

import httpx

from ._core import CoreClient, SmartlyQConnectionError, SmartlyQError
from ._version import __version__
from .resources import create_resources


class SmartlyQ:
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
        self.core = CoreClient(
            api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            default_headers=default_headers,
            transport=transport,
        )
        for key, resource in create_resources(self.core).items():
            setattr(self, key, resource)

    def close(self) -> None:
        self.core.close()

    def __enter__(self) -> "SmartlyQ":
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()


__all__ = [
    "SmartlyQ",
    "SmartlyQError",
    "SmartlyQConnectionError",
    "CoreClient",
    "__version__",
]
