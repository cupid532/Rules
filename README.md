# Rules

> **个人自用 · Mihomo / sing-box 分流规则 · 禁止传播**

这是一套按个人使用习惯维护的 Mihomo、sing-box 分流规则，当前以 AI 服务规则为主。规则内容以仓库中的实际文件为准。

## 规则文件

```text
rules/ai.list           # 通用、可读的总规则列表，也是日常编辑入口
rules/mihomo/ai.yaml    # Mihomo 规则
rules/sing-box/ai.json  # sing-box JSON 源规则
rules/sing-box/ai.srs   # sing-box 二进制规则
```

同一套规则会同步维护以上四个文件：

- 日常新增、删除或修正规则，先修改 `rules/ai.list`；
- 再同步到 `rules/mihomo/ai.yaml` 和 `rules/sing-box/ai.json`；
- 最后由 `ai.json` 编译生成 `rules/sing-box/ai.srs`；
- 详细维护流程和检查清单见 [MAINTAINING.md](MAINTAINING.md)。

远程引用时请使用 Raw 地址，不要使用 GitHub 的 `/blob/` 页面地址。

### sing-box

可读源规则：

```text
https://raw.githubusercontent.com/cupid532/Rules/main/rules/sing-box/ai.json
```

二进制规则：

```text
https://raw.githubusercontent.com/cupid532/Rules/main/rules/sing-box/ai.srs
```

在 sing-box 中使用 `ai.srs` 时，格式选择 `binary`。`ai.srs` 是二进制文件，GitHub 网页不会显示可读文本；需要查看内容时，请打开 `ai.json` 或 `ai.list`。

## 使用声明

- 本仓库仅供个人使用和学习参考；
- 未经许可，禁止转载、复制、镜像、二次分发或用于商业用途；
- 规则可能随服务域名、网络环境和客户端版本变化，请自行判断和维护；
- 使用本仓库内容所产生的任何问题，由使用者自行承担。
