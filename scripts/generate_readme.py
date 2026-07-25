"""Regenerates the API Reference section of README.md between the marker comments."""

from __future__ import annotations

from model import Method, Resource, build_model

BEGIN = "<!-- BEGIN GENERATED REFERENCE -->"
END = "<!-- END GENERATED REFERENCE -->"


def signature(r: Resource, m: Method) -> str:
    args = list(m.path_params)
    if m.has_body:
        args.append("body" if m.body_required else "body=None")
    if m.query_params:
        args.append("query=None")
    return f"sq.{r.key}.{m.name}({', '.join(args)})"


def main() -> None:
    resources = build_model()
    lines: list[str] = []
    for r in resources:
        lines += [f"### {r.tag}", "", "| Method | Endpoint | Description |", "| --- | --- | --- |"]
        for m in r.methods:
            lines.append(f"| `{signature(r, m)}` | `{m.http_method} {m.path}` | {m.summary} |")
        lines.append("")

    with open("README.md") as f:
        readme = f.read()
    begin = readme.index(BEGIN) + len(BEGIN)
    end = readme.index(END)
    with open("README.md", "w") as f:
        f.write(readme[:begin] + "\n\n" + "\n".join(lines) + readme[end:])

    count = sum(len(r.methods) for r in resources)
    print(f"README reference updated: {len(resources)} resources, {count} methods.")


if __name__ == "__main__":
    main()
