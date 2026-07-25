"""Shared spec model for the generator scripts.

Parses openapi.json into resource groups with final SDK method names and
signatures. The naming rules intentionally match the other SmartlyQ SDKs
(resource per tag, stopword-stripped verbs), rendered as snake_case here.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field

HTTP_METHODS = ("get", "post", "put", "patch", "delete")

# Tag -> client attribute. New/unknown tags fall back to auto snake_case.
TAG_KEYS = {
    "Articles": "articles",
    "Images": "images",
    "Videos": "videos",
    "Social": "social",
    "Content": "content",
    "SEO": "seo",
    "Audio": "audio",
    "URLs": "urls",
    "AI Captain": "captain",
    "Chatbot": "chatbots",
    "Media": "media",
    "Analytics": "analytics",
    "Jobs": "jobs",
    "Account": "account",
    "Comments": "comments",
    "Direct Messages": "messages",
    "Webhooks": "webhooks",
    "Shorts": "shorts",
    "Presentations": "presentations",
    "CRM Contacts": "contacts",
    "CRM Opportunities": "opportunities",
    "Workspaces": "workspaces",
    "CRM Custom Fields": "custom_fields",
    "Profiles": "profiles",
}

# Extra noise words stripped from method names, per tag.
EXTRA_STOPWORDS = {
    "AI Captain": ["ai"],
    "Direct Messages": ["direct"],
    "CRM Contacts": ["crm"],
    "CRM Opportunities": ["crm"],
    "CRM Custom Fields": ["crm"],
}


@dataclass
class Method:
    name: str
    operation_id: str
    http_method: str
    path: str
    summary: str
    path_params: list[str] = field(default_factory=list)  # snake_case arg names
    raw_path_params: list[str] = field(default_factory=list)  # as in the spec
    has_body: bool = False
    body_required: bool = True
    query_params: list[str] = field(default_factory=list)


@dataclass
class Resource:
    tag: str
    key: str
    class_name: str
    methods: list[Method] = field(default_factory=list)


def camel_tokens(op_id: str) -> list[str]:
    return re.findall(r"[A-Z]?[a-z0-9]+|[A-Z]+(?![a-z])", op_id) or [op_id]


def snake(tokens: list[str]) -> str:
    return "_".join(t.lower() for t in tokens)


def _stopwords(tag: str) -> set[str]:
    words = [w.lower() for w in tag.split()] + [w.lower() for w in EXTRA_STOPWORDS.get(tag, [])]
    out: set[str] = set()
    for w in words:
        out.add(w)
        if w.endswith("ies"):
            out.add(w[:-3] + "y")
        elif w.endswith("s"):
            out.add(w[:-1])
        else:
            out.add(w + "s")
            if w.endswith("y"):
                out.add(w[:-1] + "ies")
    return out


def _method_name(tag: str, operation_id: str) -> str:
    stop = _stopwords(tag)
    kept = [t for t in camel_tokens(operation_id) if t.lower() not in stop]
    if not kept:
        return snake(camel_tokens(operation_id))
    return snake(kept)


def build_model(spec_path: str = "openapi.json") -> list[Resource]:
    with open(spec_path) as f:
        spec = json.load(f)

    def resolve_param(param: dict) -> dict:
        if "$ref" in param:
            name = param["$ref"].rsplit("/", 1)[-1]
            return spec["components"]["parameters"][name]
        return param

    by_tag: dict[str, list[Method]] = {}
    for path, methods in spec["paths"].items():
        for http_method in HTTP_METHODS:
            op = methods.get(http_method)
            if not op:
                continue
            tag = (op.get("tags") or ["Other"])[0]
            params = [resolve_param(p) for p in op.get("parameters", [])]
            body = op.get("requestBody")
            path_params = [p["name"] for p in params if p.get("in") == "path"]
            m = Method(
                name=_method_name(tag, op["operationId"]),
                operation_id=op["operationId"],
                http_method=http_method.upper(),
                path=path,
                summary=op.get("summary") or f"{http_method.upper()} {path}",
                path_params=[p.replace("-", "_") for p in path_params],
                raw_path_params=path_params,
                has_body=body is not None,
                body_required=(body or {}).get("required", True) is not False,
                query_params=[p["name"] for p in params if p.get("in") == "query"],
            )
            by_tag.setdefault(tag, []).append(m)

    # Collision guard: same short name within a resource -> keep operationIds.
    for methods_ in by_tag.values():
        counts: dict[str, int] = {}
        for m in methods_:
            counts[m.name] = counts.get(m.name, 0) + 1
        for m in methods_:
            if counts[m.name] > 1:
                m.name = snake(camel_tokens(m.operation_id))

    resources = []
    for tag in sorted(by_tag, key=str.lower):
        key = TAG_KEYS.get(tag) or snake(camel_tokens(re.sub(r"\s+", "", tag)))
        class_name = "".join(part.capitalize() for part in key.split("_")) + "Resource"
        resources.append(Resource(tag=tag, key=key, class_name=class_name, methods=by_tag[tag]))
    return resources
