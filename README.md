# Rules

个人使用的 Mihomo / sing-box 分流规则集。

## AI 规则

AI 规则的唯一维护入口是 [`data/ai-domains.json`](data/ai-domains.json)，生成文件不要手工编辑。当前收录 **43 个 AI 服务、99 个域名**，按用途分为：

| 分类 | 用途 | Mihomo | sing-box |
| --- | --- | --- | --- |
| `chat` | 通用对话、模型服务和 AI 助手 | [`ai-chat.yaml`](rules/mihomo/ai-chat.yaml) | [`ai-chat.json`](rules/sing-box/ai-chat.json) |
| `search` | AI 搜索和答案引擎 | [`ai-search.yaml`](rules/mihomo/ai-search.yaml) | [`ai-search.json`](rules/sing-box/ai-search.json) |
| `developer` | 模型 API、模型平台和 AI 编程工具 | [`ai-developer.yaml`](rules/mihomo/ai-developer.yaml) | [`ai-developer.json`](rules/sing-box/ai-developer.json) |
| `creative` | 图像、视频、音频和创作工具 | [`ai-creative.yaml`](rules/mihomo/ai-creative.yaml) | [`ai-creative.json`](rules/sing-box/ai-creative.json) |
| `all` | 上述分类的合并规则 | [`ai.yaml`](rules/mihomo/ai.yaml) | [`ai.json`](rules/sing-box/ai.json) |

### Mihomo

远程引用合并规则：

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

也可以把 `ai.yaml` 换成 `ai-chat.yaml`、`ai-search.yaml`、`ai-developer.yaml` 或 `ai-creative.yaml`，分别使用单一分类。

### sing-box

你只使用 sing-box 时，**只引入一个聚合文件即可**：

```text
rules/sing-box/ai.json
```

这个文件已经包含 `chat`、`search`、`developer`、`creative` 四类 AI 域名；分类文件只是给需要精细拆分的人使用，不需要全部引入。sing-box 的 source rule-set 文件采用 `{"version": 2, "rules": [...]}` 结构。

#### 远程引入（推荐）

把下面内容合并到你的 `route` 配置中，并把 `proxy` 换成你自己的代理出站标签：

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

如果你的客户端只接受本地规则文件，也可以使用：

```json
{
  "tag": "ai",
  "type": "local",
  "format": "source",
  "path": "./rules/sing-box/ai.json"
}
```

将这个对象放到 `route.rule_set`，并在 `route.rules` 中加入：

```json
{
  "rule_set": ["ai"],
  "outbound": "proxy"
}
```

规则要放在最终的直连兜底规则之前，否则可能已经被前面的规则匹配。sing-box 官方文档定义了 `remote` / `local` source rule-set，以及在路由规则中通过 `rule_set` 引用它。

### IP 规则说明

AI 厂商大多使用 CDN、云负载均衡或共享 IP，静态 IP 很容易过期；因此本仓库不会把解析得到的临时 IP 当成长期规则。当前只收录 OpenAI 官方发布的 **ChatGPT Voice IPv4 前缀**快照：

- Mihomo: [`ai-openai-voice-ip.yaml`](rules/mihomo/ai-openai-voice-ip.yaml)
- sing-box: [`ai-openai-voice-ip.json`](rules/sing-box/ai-openai-voice-ip.json)
- 来源：<https://openai.com/chatgpt-voice.json>
- 快照来源时间：`2026-03-26T20:12:45.451356+00:00`
- 注意：这只覆盖 ChatGPT Voice 公布的前缀，不代表全部 OpenAI / ChatGPT 流量。

## 维护和生成

只编辑 `data/ai-domains.json`，然后运行：

```bash
python3 scripts/build_ai_rules.py
python3 scripts/build_ai_rules.py --check
```

生成器会同时更新 Mihomo YAML、sing-box source JSON 以及 OpenAI Voice IP 文件，并检查域名重复、大小写和基本格式。提交前建议确认没有把 `google.com`、`microsoft.com`、`github.com` 这类过宽的基础域名加入规则，以免产生不必要的代理流量。

> 规则只负责匹配并交给你的 `PROXY` / `proxy` 出站；实际是否能访问，还取决于节点、DNS、TLS、地区限制和客户端版本。
