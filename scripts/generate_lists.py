#!/usr/bin/env python3
from pathlib import Path
import ipaddress
src=Path("/tmp/oldboards/rules"); dst=Path("rules")
for b in ["Ads","Dev","GeoCN","GitHub","Google","Media","Microsoft","STUN","Telegram"]:
    vals={k:set() for k in ["DOMAIN-SUFFIX","DOMAIN","DOMAIN-KEYWORD","DOMAIN-REGEX","IP-CIDR","IP-CIDR6"]}
    for line in (src/b/"upstream.txt").read_text().splitlines():
        line=line.strip()
        if not line or line.startswith("#") or ":" not in line: continue
        k,v=line.split(":",1); v=v.strip()
        if k=="suffix": vals["DOMAIN-SUFFIX"].add(v.lower())
        elif k=="full": vals["DOMAIN"].add(v.lower())
        elif k=="keyword": vals["DOMAIN-KEYWORD"].add(v.lower())
        elif k=="regex": vals["DOMAIN-REGEX"].add(v)
        elif k=="ip":
            try: ver=ipaddress.ip_network(v,strict=False).version
            except ValueError: continue
            vals["IP-CIDR" if ver==4 else "IP-CIDR6"].add(v)
    name=b.lower(); lines=[f"# {name} rule list","# Generated from the synchronized upstream snapshot.","# DOMAIN-REGEX is retained where the source requires it; see AUTOMATION.md."]
    for kind,label,slug in [("DOMAIN-SUFFIX","Domain suffixes","domain-suffix"),("DOMAIN","Exact domains","domain"),("DOMAIN-KEYWORD","Domain keywords","domain-keyword"),("DOMAIN-REGEX","Domain regex","domain-regex"),("IP-CIDR","IPv4 ranges","ip-cidr"),("IP-CIDR6","IPv6 ranges","ip-cidr6")]:
        items=sorted(vals[kind])
        if not items: continue
        lines += ["",f"# {label} ({slug})"]
        if kind.startswith("IP-"): lines += ["# SOURCE: MetaCubeX upstream snapshot","# SOURCE-CHECKED: 2026-09-25"]
        for v in items: lines.append(f"{kind},{v}"+(",no-resolve" if kind.startswith("IP-") else ""))
    (dst/f"{name}.list").write_text("\n".join(lines)+"\n"); print(name,sum(map(len,vals.values())))
