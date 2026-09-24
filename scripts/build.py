#!/usr/bin/env python3
"""Build and validate the four synchronized rule-set files."""
from __future__ import annotations
import argparse, ipaddress, json, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
RULES=ROOT/'rules'; MIHOMO=RULES/'mihomo'; SING=RULES/'sing-box'; META=ROOT/'scripts/boards.json'
FIELDS={'DOMAIN-SUFFIX':'domain_suffix','DOMAIN':'domain','DOMAIN-KEYWORD':'domain_keyword','DOMAIN-REGEX':'domain_regex','IP-CIDR':'ip_cidr','IP-CIDR6':'ip_cidr'}
IPS={'IP-CIDR','IP-CIDR6'}

def boards(): return json.loads(META.read_text())
def names(): return sorted({p.stem for p in RULES.glob('*.list')} | set(boards()))
def fail(msg): raise ValueError(msg)
def parse(name):
    path=RULES/f'{name}.list'; items=[]
    if not path.exists(): fail(f'missing {path}')
    for no,line in enumerate(path.read_text().splitlines(),1):
        s=line.rstrip()
        if not s.strip(): items.append(('blank',)); continue
        if s.lstrip().startswith('#'): items.append(('comment',s)); continue
        kind,sep,rest=s.partition(','); kind=kind.strip().upper(); rest=rest.strip()
        if not sep or kind not in FIELDS: fail(f'{path}:{no}: unsupported rule: {s}')
        if kind in IPS:
            parts=[x.strip() for x in rest.split(',')]
            if len(parts)!=2 or parts[1]!='no-resolve': fail(f'{path}:{no}: IP rule needs no-resolve')
            try: net=ipaddress.ip_network(parts[0],strict=False)
            except ValueError as e: fail(f'{path}:{no}: {e}')
            if (kind=='IP-CIDR' and net.version!=4) or (kind=='IP-CIDR6' and net.version!=6): fail(f'{path}:{no}: wrong IP family')
            items.append(('rule',kind,parts[0],s))
        else:
            if not rest: fail(f'{path}:{no}: empty value')
            if kind!='DOMAIN-REGEX' and (rest!=rest.lower() or any(x in rest for x in ('://','*','/','\\',':'))): fail(f'{path}:{no}: invalid domain value')
            items.append(('rule',kind,rest,s))
    return items

def yaml_text(name,meta,items):
    out=[f"# NAME: {meta.get('name',name)}",'# FORMAT: Mihomo rule-provider / classical',f"# SCOPE: {meta.get('scope','')}",'payload:']
    for i,x in enumerate(items):
        if x[0]=='blank':
            # Preserve meaningful separators, but omit the list's initial header gap.
            if i and i + 1 < len(items): out.append('')
        elif x[0]=='comment':
            # The .list header is documentation; YAML keeps service/source comments only.
            if i < 3 and x[1].startswith('# '): continue
            if x[1].startswith('# OpenAI ChatGPT Voice IP') and out and out[-1].strip(): out.append('')
            out.append('  '+x[1])
        else: out.append('  - '+x[3])
    return '\n'.join(out)+'\n'

def json_text(items):
    groups=[]; field=None; vals=[]
    def flush():
        nonlocal field,vals
        if field and vals: groups.append({field:vals})
        field=None; vals=[]
    for x in items:
        if x[0]!='rule': flush(); continue
        f=FIELDS[x[1]]; v=x[2]
        if f!=field: flush(); field=f
        vals.append(v)
    flush(); return json.dumps({'version':2,'rules':groups},indent=2,ensure_ascii=False)+'\n'

def sb():
    p=ROOT/'.tools/sing-box'
    return str(p) if p.exists() else 'sing-box'
def compile_srs(name,json_path=None,out=None):
    jp=json_path or SING/f'{name}.json'; op=out or SING/f'{name}.srs'
    subprocess.run([sb(),'rule-set','compile',str(jp),'-o',str(op)],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
def build(which=None):
    meta=boards(); targets=which or names()
    for name in targets:
        items=parse(name); m=meta.get(name,{})
        (MIHOMO/f'{name}.yaml').write_text(yaml_text(name,m,items))
        jp=SING/f'{name}.json'; jp.write_text(json_text(items)); compile_srs(name)
        print(f'built {name}')
def check(which=None):
    meta=boards(); problems=[]
    for name in (which or names()):
        try: items=parse(name); m=meta.get(name,{})
        except Exception as e: problems.append(str(e)); continue
        expected=[(MIHOMO/f'{name}.yaml',yaml_text(name,m,items)),(SING/f'{name}.json',json_text(items))]
        for p,v in expected:
            if not p.exists() or p.read_text()!=v: problems.append(f'out of sync: {p}')
        target=SING/f'{name}.srs'
        with tempfile.TemporaryDirectory() as d:
            tmp=Path(d)/'x.srs';
            try: compile_srs(name,SING/f'{name}.json',tmp)
            except Exception as e: problems.append(f'compile failed {name}: {e}'); continue
            if not target.exists() or target.read_bytes()!=tmp.read_bytes(): problems.append(f'out of sync: {target}')
    if problems:
        print('\n'.join(problems),file=sys.stderr); return 1
    print(f'checked {len(which or names())} rule sets'); return 0
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('command',choices=['build','check','list']); ap.add_argument('names',nargs='*'); a=ap.parse_args()
    try:
        if a.command=='build': build(a.names); return 0
        if a.command=='check': return check(a.names)
        for n in names(): print(n)
        return 0
    except Exception as e: print(e,file=sys.stderr); return 1
if __name__=='__main__': raise SystemExit(main())
