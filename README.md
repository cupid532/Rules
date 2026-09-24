# Rules

> **个人自用 · Mihomo / sing-box 分流规则 · 禁止传播**

这是一套为个人网络环境和使用习惯整理的 Mihomo、sing-box 分流规则，持续收录和维护常用服务规则，具体内容以规则文件为准。

## 规则文件

```text
rules/mihomo/ai.yaml    # Mihomo 可读规则
rules/sing-box/ai.json  # sing-box 可读源文件
rules/sing-box/ai.srs   # sing-box 二进制规则
rules/ai.list           # 可读的通用规则列表
```

两份文件分别对应不同客户端，均为完整的 AI 聚合规则，按需引用即可。

## 规则搜索器

[打开规则搜索器](https://cupid532.github.io/Rules/) · [查看搜索器源码](docs/index.html)

搜索器会自动同步 `rules/` 目录，支持按关键词、客户端和文件格式筛选，并按“数字 → 字母 → 特殊字符”排列。

> `ai.srs` 是 sing-box 的二进制规则文件，GitHub 网页不会显示可读文本；需要查看规则内容时，请打开 `ai.json` 或 `ai.list`。远程引用时请使用 Raw 地址，不要使用 GitHub 的 `/blob/` 页面地址。

### sing-box SRS Raw 地址

[点击获取 sing-box SRS Raw 文件](https://raw.githubusercontent.com/cupid532/Rules/main/rules/sing-box/ai.srs)

```text
https://raw.githubusercontent.com/cupid532/Rules/main/rules/sing-box/ai.srs
```

在 sing-box 中使用时，格式选择 `binary`。

## 使用声明

- 本仓库仅供个人使用和学习参考；
- 未经许可，禁止转载、复制、镜像、二次分发或用于商业用途；
- 规则可能随服务域名、网络环境和客户端版本变化，请自行判断和维护；
- 使用本仓库内容所产生的任何问题，由使用者自行承担。
