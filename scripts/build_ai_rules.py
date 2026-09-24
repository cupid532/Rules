#!/usr/bin/env python3
"""Generate Mihomo and sing-box AI rule files from data/ai-domains.json."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "ai-domains.json"
MIHOMO = ROOT / "rules" / "mihomo"
SINGBOX = ROOT / "rules" / "sing-box"


def load() -> dict[str, Any]:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    seen: dict[str, str] = {}
    for service in data["services"]:
        for domain in service["domains"]:
            if domain != domain.lower() or domain.startswith(".") or " " in domain:
                raise ValueError(f"invalid domain: {domain}")
            previous = seen.setdefault(domain, service["id"])
            if previous != service["id"]:
                raise ValueError(f"duplicate domain {domain}: {previous}, {service['id']}")
    return data


def grouped(data: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = {key: [] for key in data["categories"]}
    for service in data["services"]:
        out[service["category"]].append(service)
    return out


def mihomo_text(data: dict[str, Any], services: list[dict[str, Any]], title: str) -> str:
    lines = [
        f"# NAME: {title}",
        "# FORMAT: Mihomo rule-provider / classical",
        "# GENERATED: scripts/build_ai_rules.py",
        "# SOURCE: data/ai-domains.json",
        "payload:",
    ]
    for service in services:
        lines.append(f"  # {service['name']} ({service['id']})")
        for domain in service["domains"]:
            lines.append(f"  - DOMAIN-SUFFIX,{domain}")
    return "\n".join(lines) + "\n"


def singbox_obj(services: list[dict[str, Any]]) -> dict[str, Any]:
    rules: list[dict[str, list[str]]] = []
    for service in services:
        rules.append({"domain_suffix": service["domains"]})
    return {"version": 2, "rules": rules}


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="regenerate in memory and verify checked-in files")
    args = parser.parse_args()
    data = load()
    categories = grouped(data)
    all_services = [service for services in categories.values() for service in services]

    outputs: dict[Path, str] = {}
    outputs[MIHOMO / "ai.yaml"] = mihomo_text(data, all_services, "AI / all")
    outputs[SINGBOX / "ai.json"] = json.dumps(singbox_obj(all_services), ensure_ascii=False, indent=2) + "\n"
    for category, services in categories.items():
        outputs[MIHOMO / f"ai-{category}.yaml"] = mihomo_text(data, services, f"AI / {category}")
        outputs[SINGBOX / f"ai-{category}.json"] = json.dumps(singbox_obj(services), ensure_ascii=False, indent=2) + "\n"

    ip_source = data["ip_sources"]["openai_voice"]
    ip_lines = [
        "# NAME: OpenAI ChatGPT Voice IP",
        "# FORMAT: Mihomo rule-provider / classical",
        f"# SOURCE: {ip_source['url']}",
        f"# SOURCE-CREATION-TIME: {ip_source['creation_time']}",
        "# SCOPE: ChatGPT Voice published IPv4 prefixes only; not all OpenAI traffic.",
        "payload:",
    ] + [f"  - IP-CIDR,{cidr},no-resolve" for cidr in ip_source["ipv4"]]
    outputs[MIHOMO / "ai-openai-voice-ip.yaml"] = "\n".join(ip_lines) + "\n"
    outputs[SINGBOX / "ai-openai-voice-ip.json"] = json.dumps(
        {"version": 2, "rules": [{"ip_cidr": ip_source["ipv4"]}]}, indent=2
    ) + "\n"

    if args.check:
        bad = [str(path.relative_to(ROOT)) for path, text in outputs.items() if not path.exists() or path.read_text(encoding="utf-8") != text]
        if bad:
            raise SystemExit("generated files are stale or missing:\n" + "\n".join(bad))
        print(f"OK: {len(outputs)} generated files are up to date")
    else:
        for path, text in outputs.items():
            write(path, text)
        print(f"Wrote {len(outputs)} generated files")


if __name__ == "__main__":
    main()
