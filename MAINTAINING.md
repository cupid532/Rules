# 规则维护与更新执行规范

本文件是本仓库后续所有规则更新的固定执行标准。目标只有一个：**任何一次规则内容更新，都必须同时兼顾 Mihomo、sing-box 和通用 `.list`，不能只改其中一个文件。**

## 一、固定文件和职责

当前这套 AI 聚合规则固定维护以下四个文件：

| 文件 | 用途 | 是否手工编辑 |
| --- | --- | --- |
| `rules/ai.list` | 通用、可读的总规则列表；日常新增规则的首要入口 | 是 |
| `rules/mihomo/ai.yaml` | Mihomo 使用的 YAML 规则 | 是，必须同步 |
| `rules/sing-box/ai.json` | sing-box 可读的 JSON 源规则 | 是，必须同步 |
| `rules/sing-box/ai.srs` | sing-box 高效使用的二进制规则 | 否，必须由 `ai.json` 编译生成 |

### 核心原则

1. `rules/ai.list` 是人阅读和录入规则的第一入口。
2. `rules/mihomo/ai.yaml`、`rules/sing-box/ai.json` 必须表达与 `.list` 完全相同的域名和 IP 集合。
3. `rules/sing-box/ai.srs` 永远以 `ai.json` 为唯一输入，不直接修改二进制文件。
4. 规则内容发生变化时，四个文件必须在同一次提交中完成更新。
5. 只改 README、许可证或维护文档时，不要求更新四个规则文件。
6. 除非明确决定拆分规则，否则不新增零散的 AI 子文件；所有 AI 规则继续汇总在这四个固定位置。

## 二、允许使用的规则类型

为了确保三种格式可以互相转换，目前统一使用以下规则类型：

```text
DOMAIN-SUFFIX,example.com
DOMAIN,api.example.com
IP-CIDR,203.0.113.0/24,no-resolve
```

对应关系如下：

| `rules/ai.list` | Mihomo YAML | sing-box JSON |
| --- | --- | --- |
| `DOMAIN-SUFFIX,example.com` | `DOMAIN-SUFFIX,example.com` | `domain_suffix: ["example.com"]` |
| `DOMAIN,api.example.com` | `DOMAIN,api.example.com` | `domain: ["api.example.com"]` |
| `IP-CIDR,203.0.113.0/24,no-resolve` | `IP-CIDR,203.0.113.0/24,no-resolve` | `ip_cidr: ["203.0.113.0/24"]` |

暂不随意引入需要特殊转换逻辑的类型，例如正则表达式、通配符、AdGuard 专用语法或客户端独占语法。确实需要时，必须先确认三种格式都能正确表达，再决定是否加入。

## 三、单条规则的书写标准

### 域名规则

- 统一使用小写域名；
- 不写协议头，例如不要写 `https://example.com`；
- 不写路径、端口、查询参数或通配符；
- 不以 `/` 结尾；
- `DOMAIN-SUFFIX` 用于一个服务及其所有子域名；
- `DOMAIN` 只用于确实需要精确匹配的完整域名；
- 已有父域名后，通常不再重复添加其子域名，除非有明确的兼容性原因；
- 添加前先搜索四个文件，避免重复录入。

正确示例：

```text
DOMAIN-SUFFIX,example.com
DOMAIN,api.example.com
```

错误示例：

```text
https://example.com
*.example.com
example.com/path
```

### IP 规则

- 必须使用 CIDR 表示法，例如 `1.2.3.4/32`；
- 单个 IP 使用 `/32`，不要只写裸 IP；
- IPv6 使用合法 CIDR；
- 目前 IP 规则统一保留 `no-resolve`；
- IP 来源必须写注释，注明来源和抓取或确认日期；
- IP 可能变化，不能因为短期可用就认为它是永久规则。

示例：

```text
# SOURCE: 官方地址清单
# SOURCE-CREATION-TIME: 2026-09-24
IP-CIDR,203.0.113.10/32,no-resolve
```

## 四、每次更新的固定执行顺序

### 第 1 步：确认更新对象

先明确本次更新属于以下哪一种：

- 新增 AI 服务；
- 新增服务域名或 API 域名；
- 删除失效域名；
- 修正域名类型；
- 更新 IP 地址；
- 只修改注释或分组名称。

如果只是修改注释，也要确认没有误删或误改规则内容。

### 第 2 步：先修改 `rules/ai.list`

这是唯一的日常录入入口。新增规则时：

1. 放到对应服务分组下面；
2. 分组注释保持统一，例如 `# OpenAI / ChatGPT (openai)`；
3. 域名和 IP 按固定语法书写；
4. 先检查重复项；
5. 如果是 IP，补充来源和日期注释。

不要先改 `ai.srs`，也不要只在某一个客户端文件里临时添加规则。

### 第 3 步：同步 `rules/mihomo/ai.yaml`

将 `.list` 中的规则完整同步到 Mihomo 文件：

- 每条 `.list` 规则对应一条 YAML 列表项；
- 保留同样的服务分组顺序；
- 保留必要的来源注释；
- 不要把 Mihomo 的代理策略名称写进规则集，规则集只负责匹配；
- 不要遗漏 IP 规则。

### 第 4 步：同步 `rules/sing-box/ai.json`

将相同规则同步到 sing-box JSON：

- 顶层保持 `"version": 2`；
- 域名后缀放入 `domain_suffix`；
- 精确域名放入 `domain`；
- IP 网段放入 `ip_cidr`；
- 服务分组顺序与 `.list`、Mihomo 文件保持一致；
- JSON 不支持注释，来源信息需要在 `.list` 和 YAML 中保留。

### 第 5 步：由 JSON 编译 `ai.srs`

使用固定版本的 sing-box 编译，不手工编辑二进制文件。当前维护基准为 sing-box `v1.14.2`：

```bash
sing-box rule-set compile \
  rules/sing-box/ai.json \
  -o rules/sing-box/ai.srs
```

如果本机没有加入 PATH，可使用本机实际的 sing-box 二进制路径替换 `sing-box`。编译完成后，必须确认 `ai.srs` 的修改时间和 Git 差异都已更新。

## 五、提交前强制检查清单

一次规则更新只有在以下项目全部完成后，才允许提交：

### 文件检查

```text
[ ] rules/ai.list 已更新
[ ] rules/mihomo/ai.yaml 已同步
[ ] rules/sing-box/ai.json 已同步
[ ] rules/sing-box/ai.srs 已由最新 ai.json 重新编译
[ ] 没有只修改某一个客户端文件的遗漏
```

### 内容检查

```text
[ ] 没有重复域名或重复 IP
[ ] 没有 https://、路径、端口或通配符
[ ] 域名大小写和规则类型正确
[ ] IP 使用 CIDR，并保留 no-resolve
[ ] 新规则放在正确的服务分组下
[ ] 三种可读格式表达的规则集合一致
```

### 命令检查

在仓库根目录执行：

```bash
# 检查 Git 补丁和空白字符

git diff --check

# 检查 sing-box JSON 是否有效
python3 -m json.tool rules/sing-box/ai.json >/dev/null

# 检查 Mihomo YAML 是否能被解析
ruby -e 'require "yaml"; YAML.load_file("rules/mihomo/ai.yaml"); puts "YAML OK"'

# 检查 SRS 能否反向解码
sing-box rule-set decompile \
  rules/sing-box/ai.srs \
  -o /tmp/ai.srs.json
python3 -m json.tool /tmp/ai.srs.json >/dev/null
```

反向解码只用于验证，不要把 `/tmp/ai.srs.json` 放回仓库，也不要用反向解码结果覆盖源 JSON。

### 差异检查

```bash
git status --short
git diff --stat
git diff -- rules/ai.list rules/mihomo/ai.yaml rules/sing-box/ai.json
```

凡是规则内容发生变化，`git status --short` 中原则上应同时看到：

```text
rules/ai.list
rules/mihomo/ai.yaml
rules/sing-box/ai.json
rules/sing-box/ai.srs
```

如果缺少其中任何一个，先不要提交，回到同步步骤补齐。

## 六、提交规范

规则更新建议使用以下提交格式：

```text
feat(ai): add <service> domains
fix(ai): remove expired <service> rules
fix(ai): update <service> IP ranges
```

一次提交只做一组相关规则变更。不要在同一次提交里混入无关的格式化、目录重构或客户端配置修改。

## 七、以后新增其他规则类别时

如果以后从 `ai` 扩展到广告、流媒体、社交或其他类别，必须沿用同样的四文件结构：

```text
rules/<name>.list
rules/mihomo/<name>.yaml
rules/sing-box/<name>.json
rules/sing-box/<name>.srs
```

新增类别也必须执行“`.list` → Mihomo YAML → sing-box JSON → SRS 编译 → 四文件检查”的完整流程，不能只提供某一个客户端格式。
