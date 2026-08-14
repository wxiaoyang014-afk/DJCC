# DJCC Amazon Keyword Library Skill

DJCC 是一个可移植的 Agent Skill，用于构建、纠正和校验 Amazon 关键词库工作簿。它强调输入文件身份校验、月度数据保真、词根复核、第四阶段否定词判定和第五阶段图片判断。

## 包含内容

- `skills/djcc-amazon-keywords/SKILL.md`：Agent 的核心工作流。
- `references/`：五阶段规则和通用字段结构。
- `scripts/inspect_xlsx.py`：无第三方依赖的 XLSX 身份检查工具。
- `tests/fixtures/`：完全虚构的 CSV 测试数据，可据此制作本地 XLSX 测试表。

真实客户数据、第三方付费数据集、产品专属词根和项目结论不属于本仓库。

## 安装到 Codex

将下面目录完整复制到 Codex 的 Skills 目录：

```text
skills/djcc-amazon-keywords
```

目标位置：

```text
$CODEX_HOME/skills/djcc-amazon-keywords
```

如果没有配置 `CODEX_HOME`，通常使用：

```text
~/.codex/skills/djcc-amazon-keywords
```

也可以在 Codex 中调用内置 `skill-installer`，让它从本 GitHub 仓库的 `skills/djcc-amazon-keywords` 子目录安装。安装后重新开启任务或重启 Agent。

## 安装到其他 Agent

支持 Agent Skills / `SKILL.md` 的平台可以直接复制同一目录。不支持该规范的平台，需要把 `SKILL.md` 转成平台的系统指令，并适配其文件和脚本调用方式。

## 快速使用

```text
使用 $djcc-amazon-keywords 检查 INPUT.xlsx 的文件身份，确认站点和产品方向，再按五阶段流程构建关键词库。
```

单独运行身份检查：

```bash
python skills/djcc-amazon-keywords/scripts/inspect_xlsx.py YOUR_TEST_WORKBOOK.xlsx
```

## 发布前验证

```bash
python /path/to/skill-creator/scripts/quick_validate.py skills/djcc-amazon-keywords
python skills/djcc-amazon-keywords/scripts/inspect_xlsx.py YOUR_TEST_WORKBOOK.xlsx
```

再检查仓库和完整 Git 历史中是否存在密钥、Cookie、账号、私人路径、真实业务 Excel 或无权分发的数据。

## 许可证

代码和通用工作流采用 MIT License。示例数据为虚构数据。Amazon 是其各自权利人的商标；本项目与 Amazon 不存在隶属或背书关系。
