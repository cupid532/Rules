# 自动同步工具

仓库固定使用四种同名文件：.list、Mihomo .yaml、sing-box .json 和 .srs。

- python3 scripts/build.py build：从每个 .list 生成另外三份文件。
- python3 scripts/build.py check：检查四份文件是否同步，并重新编译 SRS 比较结果。
- make check：执行同一检查，供 CI 使用。
- .list 中的 DOMAIN-REGEX 映射为 Mihomo DOMAIN-REGEX 和 sing-box domain_regex。
