# 规则维护与更新执行规范

本文件是本仓库后续所有规则更新的固定执行标准。规则集不只包含 AI，AI 只是当前已经建立的一个类别。以后新增广告、流媒体、社交、游戏、隐私或其他类别时，必须遵守同一套规范。

本规范的核心目标是：**任何一个规则集的规则内容发生变化，都必须同时维护通用 `.list`、Mihomo、sing-box JSON 和 sing-box SRS，不能只更新某一个客户端格式。**

## 一、目录结构和命名规则

每一个规则集都使用同名的四个文件：

```text
rules/<name>.list
rules/mihomo/<name>.yaml
rules/sing-box/<name>.json
rules/sing-box/<name>.srs
```

例如当前的 AI 规则集：

```text
rules/ai.list
rules/mihomo/ai.yaml
rules/sing-box/ai.json
rules/sing-box/ai.srs
```

### `<name>` 命名要求

- 只使用小写英文字母、数字和短横线；
- 不使用空格、中文、下划线或特殊符号；
- 名称应当表达规则集的用途，例如 `ai`、`ads`、`streaming`、`social`、`games`；
- 同一个 `<name>` 必须在四个位置保持一致；
- 新增一个类别时，四个文件必须一起创建；
- 删除一个类别时，四个文件必须在同一次提交中一起删除；
- 不为同一类别建立多个没有明确用途的别名文件。

### 当前和未来规则集的关系

- `ai` 只是一个规则集名称，不代表整个仓库只能维护 AI；
- 每个 `.list` 文件都是对应类别的“总规则列表”；
- 不默认创建一个把所有类别混在一起的 `all.list`，避免不同用途的规则互相污染；
- 如果以后确实需要总集合，必须把它作为一个单独、明确的规则集，并同样提供四种格式。

## 二、四种文件的职责

| 文件 | 用途 | 编辑要求 |
| --- | --- | --- |
| `rules/<name>.list` | 对应规则集的通用、可读总列表，也是日常录入入口 | 先编辑 |
| `rules/mihomo/<name>.yaml` | Mihomo 使用的 YAML 规则 | 必须同步 |
| `rules/sing-box/<name>.json` | sing-box 可读的 JSON 源规则 | 必须同步 |
| `rules/sing-box/<name>.srs` | sing-box 高效使用的二进制规则 | 由 JSON 编译，不手工编辑 |

### 总原则

1. 每个类别以 `rules/<name>.list` 作为人类可读的录入入口。
2. Mihomo YAML 和 sing-box JSON 必须表达与 `.list` 相同的域名、关键词和 IP 集合。
3. `rules/sing-box/<name>.srs` 永远以同名 JSON 为唯一输入。
4. 规则内容发生变化时，四个文件必须在同一次提交中完成更新。
5. 只修改 README、许可证、维护文档或其他非规则文件时，不要求更新四个规则文件。
6. 不允许只为 Mihomo、只为 sing-box 或只为 `.list` 临时添加规则后直接提交。
7. 如果某条规则无法在三种可读格式中保持相同语义，不能直接塞进公共规则集，必须先确认兼容方案并单独说明。

## 三、规则来源和分组标准

### 规则来源

每次新增外部规则时，先确认来源是否可靠：

- 官方域名、官方文档、官方地址清单优先；
- 其次使用项目本身的公开文档或稳定维护的上游列表；
- 不因为搜索结果中偶然出现的域名就直接加入；
- 无法确认用途的域名、IP 或 CDN 不直接加入；
- IP 规则必须记录来源和确认日期；
- 失效、弃用或用途不明的规则应及时删除，而不是无限累积。

来源注释写在 `.list` 和 Mihomo YAML 中；JSON 不支持注释，因此不能把注释写进 JSON：

```text
# SOURCE: 官方地址清单
# SOURCE-CHECKED: YYYY-MM-DD
```

### 分组规则

- 每个规则集内部按服务、厂商或功能分组；
- 分组标题使用统一格式：`# 服务名称 (stable-slug)`；
- 同一服务的网页、API、静态资源和必要的 CDN 规则放在同一组；
- 不因为一个域名就随意新建一个类别；
- 不把不同用途的服务混进同一个规则集；
- `.list` 和 YAML 保留相同的分组顺序；
- JSON 虽然不能写注释，但规则组顺序应与 `.list` 和 YAML 尽量一致。

## 四、通用规则书写标准

为了让规则可以同时转换到 Mihomo 和 sing-box，目前公共规则集优先使用以下类型：

```text
DOMAIN-SUFFIX,example.com
DOMAIN,api.example.com
DOMAIN-KEYWORD,example
IP-CIDR,203.0.113.0/24,no-resolve
IP-CIDR6,2001:db8::/32,no-resolve
```

对应关系如下：

| `.list` | Mihomo YAML | sing-box JSON |
| --- | --- | --- |
| `DOMAIN-SUFFIX,example.com` | `DOMAIN-SUFFIX,example.com` | `domain_suffix` |
| `DOMAIN,api.example.com` | `DOMAIN,api.example.com` | `domain` |
| `DOMAIN-KEYWORD,example` | `DOMAIN-KEYWORD,example` | `domain_keyword` |
| `IP-CIDR,203.0.113.0/24,no-resolve` | `IP-CIDR,203.0.113.0/24,no-resolve` | `ip_cidr` |
| `IP-CIDR6,2001:db8::/32,no-resolve` | `IP-CIDR6,2001:db8::/32,no-resolve` | `ip_cidr` |

暂不直接引入以下内容：

- `https://`、完整 URL、路径、端口或查询参数；
- `*` 等通配符；
- 只被某一个客户端支持的专用语法；
- 未确认转换关系的正则表达式；
- AdGuard、hosts、Surge 或其他格式的原始语法；
- 不能在 Mihomo 和 sing-box 中保持相同含义的特殊规则。

确实需要加入新类型时，必须先补充三种格式的转换方法和验证方法，再使用该类型。

## 五、单条规则书写标准

### 域名规则

- 统一使用小写域名；
- 不写协议头，例如不要写 `https://example.com`；
- 不写路径、端口、查询参数或通配符；
- 不以 `/` 结尾；
- `DOMAIN-SUFFIX` 用于一个服务及其所有子域名；
- `DOMAIN` 只用于确实需要精确匹配的完整域名；
- `DOMAIN-KEYWORD` 只在后缀匹配无法覆盖且关键词匹配确有必要时使用；
- 已有父域名后，通常不再重复添加其子域名，除非有明确的兼容性原因；
- 添加前必须在四个文件中搜索，避免重复录入。

正确示例：

```text
DOMAIN-SUFFIX,example.com
DOMAIN,api.example.com
DOMAIN-KEYWORD,example
```

错误示例：

```text
https://example.com
*.example.com
example.com/path
api.example.com:443
```

### IP 规则

- 必须使用 CIDR 表示法；
- 单个 IPv4 使用 `/32`，单个 IPv6 使用 `/128`；
- IPv4 使用 `IP-CIDR`，IPv6 使用 `IP-CIDR6`；
- 公共规则集中的 IP 规则统一保留 `no-resolve`；
- IP 来源必须写注释，注明来源和确认日期；
- IP 可能变化，不能因为短期可用就认为它是永久规则；
- 大范围网段必须确认不会误伤大量无关服务后再加入。

示例：

```text
# SOURCE: 官方地址清单
# SOURCE-CHECKED: YYYY-MM-DD
IP-CIDR,203.0.113.10/32,no-resolve
```

## 六、每次更新的固定执行顺序

以下流程适用于新增、删除、修正、替换和更新任何类别的规则。

### 第 1 步：确定规则集名称和变更范围

先确认本次修改属于哪个 `<name>`，例如：

```text
ai
ads
streaming
social
```

然后明确变更类型：

- 新增服务或厂商；
- 新增域名、关键词或 API 域名；
- 删除失效、重复或误加入的规则；
- 修正规则类型；
- 更新 IP 地址或网段；
- 调整服务分组；
- 只修改来源注释。

如果只是修改注释或分组，也必须确认没有误删或误改实际规则内容。

### 第 2 步：先修改对应 `.list`

例如更新 AI 规则时，先修改：

```text
rules/ai.list
```

更新其他类别时，先修改对应的：

```text
rules/<name>.list
```

操作要求：

1. 放到正确的服务分组下面；
2. 使用公共规则类型和统一语法；
3. 先搜索四个对应文件，确认没有重复项；
4. 新增 IP 时补充来源和日期；
5. 删除规则时确认不是其他服务仍在使用的共享域名；
6. 不要先修改 SRS，也不要只在某一个客户端文件里临时添加规则。

### 第 3 步：同步 Mihomo YAML

将对应 `.list` 的内容完整同步到：

```text
rules/mihomo/<name>.yaml
```

要求：

- 每条公共规则都能在 YAML 中找到对应项；
- 保持服务分组和大致顺序一致；
- 保留必要的来源注释；
- 不把代理策略名称写进规则集；
- 不遗漏域名、关键词、IPv4 或 IPv6 规则；
- 不加入只属于 Mihomo 的额外规则，除非该规则同时补齐其他格式。

### 第 4 步：同步 sing-box JSON

将相同内容同步到：

```text
rules/sing-box/<name>.json
```

要求：

- 顶层保持 `"version": 2`；
- `DOMAIN-SUFFIX` 放入 `domain_suffix`；
- `DOMAIN` 放入 `domain`；
- `DOMAIN-KEYWORD` 放入 `domain_keyword`；
- IPv4 和 IPv6 网段放入 `ip_cidr`；
- 规则分组顺序尽量与 `.list`、YAML 一致；
- JSON 必须是有效 JSON，不添加注释或尾随逗号；
- 不加入只属于 sing-box 的额外规则，除非其他格式也同步支持。

### 第 5 步：由 JSON 编译 SRS

使用固定版本的 sing-box 编译同名 SRS，不手工编辑二进制文件：

```bash
NAME=ai
sing-box rule-set compile \
  "rules/sing-box/${NAME}.json" \
  -o "rules/sing-box/${NAME}.srs"
```

如果本机没有将 sing-box 加入 PATH，可使用本机实际的 sing-box 二进制路径替换 `sing-box`。当前仓库已确认的维护基准为 sing-box `v1.14.2`；更换编译版本时，应在提交说明中注明。

### 第 6 步：四文件一起检查

本次规则内容更新完成后，必须确认对应的四个文件都已经修改或重新生成：

```text
rules/<name>.list
rules/mihomo/<name>.yaml
rules/sing-box/<name>.json
rules/sing-box/<name>.srs
```

如果缺少任意一个文件，更新就没有完成，不能提交。

## 七、提交前强制检查清单

### 文件检查

```text
[ ] 对应的 rules/<name>.list 已更新
[ ] 对应的 rules/mihomo/<name>.yaml 已同步
[ ] 对应的 rules/sing-box/<name>.json 已同步
[ ] 对应的 rules/sing-box/<name>.srs 已由最新 JSON 重新编译
[ ] 没有只修改某一个客户端文件的遗漏
[ ] 没有把其他类别的规则误放进当前类别
```

### 内容检查

```text
[ ] 没有重复域名、关键词或 IP
[ ] 没有 https://、路径、端口或通配符
[ ] 域名大小写和规则类型正确
[ ] IPv4 / IPv6 CIDR 格式正确
[ ] IP 规则保留 no-resolve
[ ] 新规则放在正确的服务分组下
[ ] 来源和日期信息完整
[ ] 三种可读格式表达的规则集合一致
```

### 命令检查

在仓库根目录执行，将 `NAME` 替换为本次实际更新的规则集名称：

```bash
NAME=ai

# 检查 Git 补丁和空白字符
git diff --check

# 检查 sing-box JSON 是否有效
python3 -m json.tool "rules/sing-box/${NAME}.json" >/dev/null

# 检查 Mihomo YAML 是否能被解析
ruby -e 'require "yaml"; YAML.load_file(ARGV.fetch(0)); puts "YAML OK"' \
  "rules/mihomo/${NAME}.yaml"

# 检查 SRS 能否反向解码
sing-box rule-set decompile \
  "rules/sing-box/${NAME}.srs" \
  -o "/tmp/${NAME}.srs.json"
python3 -m json.tool "/tmp/${NAME}.srs.json" >/dev/null

# 检查工作区和变更范围
git status --short
git diff --stat
```

反向解码只用于验证，不要把 `/tmp/${NAME}.srs.json` 放回仓库，也不要用反向解码结果覆盖源 JSON。

### 差异检查

凡是规则内容发生变化，`git status --short` 中原则上应同时看到本类别的四个文件：

```text
rules/<name>.list
rules/mihomo/<name>.yaml
rules/sing-box/<name>.json
rules/sing-box/<name>.srs
```

如果缺少其中任何一个，先不要提交，回到同步步骤补齐。

## 八、特殊情况处理

### 只修改注释

如果只修改来源、分组标题或维护说明，没有改变任何规则值，可以不重新编译 SRS。但提交前必须确认规则集合没有变化。

### 只更新 sing-box 编译版本

如果规则内容没有变化，只是为了升级 sing-box 编译器，可以只更新 SRS，但必须在提交说明中写明编译版本变化，并验证 SRS 可以正常加载。

### 某客户端需要专用规则

如果某条规则只能被 Mihomo 或 sing-box 表达：

1. 不要悄悄塞入公共规则集；
2. 先确认是否可以转换为公共语义；
3. 如果确实不能转换，单独建立专用文件并在 README 或维护记录中说明；
4. 公共 `.list`、Mihomo 和 sing-box 三套规则仍然保持一致。

### 删除规则

删除前必须确认：

- 服务已经停用或域名已经失效；
- 不是误把 API、静态资源或登录域名删掉；
- 不是其他服务仍然共用的域名；
- 四种格式全部删除；
- 删除后重新编译 SRS 并完成检查。

## 九、提交规范

规则更新建议使用以下格式：

```text
feat(<name>): add <service> rules
fix(<name>): remove expired <service> rules
fix(<name>): update <service> IP ranges
refactor(<name>): reorganize rule groups
```

例如：

```text
feat(ai): add new AI service domains
fix(streaming): remove expired CDN rules
fix(ads): update tracker domains
```

一次提交只做一组相关规则变更。不要在同一次提交中混入无关的目录重构、格式化或客户端配置修改。

## 十、给后续维护者的最终判断标准

一次规则更新只有同时满足以下条件，才算完成：

```text
规则来源已确认
    ↓
对应的 <name>.list 已更新
    ↓
Mihomo <name>.yaml 已同步
    ↓
sing-box <name>.json 已同步
    ↓
sing-box <name>.srs 已重新编译
    ↓
JSON、YAML、SRS 和规则集合检查通过
    ↓
四个文件在同一次提交中提交
```

**任何一个环节缺失，都视为本次更新未完成。**
