# Rules

个人使用的 Mihomo / sing-box 分流规则集。

## AI 规则集

本仓库只维护两份完整的 AI 聚合规则，分别对应两个客户端：

```text
Mihomo   rules/mihomo/ai.yaml
sing-box rules/sing-box/ai.json
```

分类只保留在文件内部的注释中，不拆成多个需要分别引入的文件。以后新增或删除 AI 服务，直接修改对应的聚合文件即可。

### Mihomo

```yaml
rule-providers:
  ai:
    type: http
    behavior: classical
    format: yaml
    url: https://raw.githubusercontent.com/cupid532/Rules/main/rules/mihomo/ai.yaml
    path: ./ruleset/ai.yaml
    interval: 86400

rules:
  - RULE-SET,ai,PROXY
```

### sing-box

```json
{
  "route": {
    "rule_set": [
      {
        "tag": "ai",
        "type": "remote",
        "format": "source",
        "url": "https://raw.githubusercontent.com/cupid532/Rules/main/rules/sing-box/ai.json",
        "update_interval": "1d"
      }
    ],
    "rules": [
      {
        "rule_set": ["ai"],
        "outbound": "proxy"
      }
    ]
  }
}
```

把示例中的 `proxy` 换成你自己的代理出站标签，并确保这条 AI 规则位于直连兜底规则之前。

如果客户端只支持本地规则文件，则下载 `rules/sing-box/ai.json`，配置为：

```json
{
  "tag": "ai",
  "type": "local",
  "format": "source",
  "path": "./rules/sing-box/ai.json"
}
```

## IP 规则说明

AI 服务大多使用 CDN、云负载均衡或共享 IP，静态 IP 容易变化。本次只把 OpenAI 官方公布的 ChatGPT Voice IPv4 快照合并进两份完整规则中，并在文件内保留来源和快照时间；它不代表全部 OpenAI / ChatGPT 流量。

规则只负责匹配并交给你的代理出站，实际访问效果还取决于节点、DNS、TLS、地区限制和客户端版本。
