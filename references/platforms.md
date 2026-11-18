# Windows 和 Linux 上的宿主与运行环境

同一份 `SKILL.md` 供 Claude Code 和 Codex 使用。以下目录均以运行宿主的操作系统为准。Windows 原生与 WSL 内的 Linux 可以有不同的用户目录、Python、工具链和权限。

| 宿主 | 项目级技能目录 | 个人技能目录 | 会话中显式调用 |
| --- | --- | --- | --- |
| Claude Code | `.claude/skills/thesisforge/` | `~/.claude/skills/thesisforge/`，配置根目录已通过 `CLAUDE_CONFIG_DIR` 更改时跟随该设置 | `/thesisforge 审查这段摘要` |
| Codex CLI / IDE，或在桌面客户端使用本地项目 | `.agents/skills/thesisforge/` | `~/.agents/skills/thesisforge/` | Codex CLI / IDE 输入 `$thesisforge` 或打开 `/skills`；ChatGPT 桌面技能选择器输入 `@` 后选 ThesisForge |

请在论文项目中打开会话。除表中的显式调用外，两个宿主也可依据技能描述匹配自然语言请求。项目级安装随项目使用，个人安装对相应用户的多个项目可用。云端 Codex 任务从实际检出的仓库读取项目级技能；需要这种用法时，将项目的技能目录一并提交。[Claude Code 技能文档](https://code.claude.com/docs/en/skills) · [OpenAI Skills 文档](https://learn.chatgpt.com/docs/build-skills)

使用 `--host both` 时，安装器先备好两份副本，再写入两个宿主的技能目录。若第二个宿主的替换操作报错，安装器会撤回本次已完成的替换。成功使用 `--update` 后，终端的 `Previous copy` 指向更新前的完整目录，需要找回本地修改时可从中取回相应文件。

## 在研究项目中运行脚本

从宿主提供的技能路径取得包含 `SKILL.md` 的实际目录。以下示例从研究项目根目录执行，以 Codex 项目级安装为例。Claude Code 项目级安装将 `.agents` 换为 `.claude`，个人安装则取上一表的个人目录。路径中的空格和中文应作为同一个参数传递。

**Windows PowerShell**

```powershell
$skillDir = (Resolve-Path -LiteralPath '.agents/skills/thesisforge').Path
py -3 -B "$skillDir/scripts/probe_environment.py" --workspace .
```

如果机器只有 `python`，将 `py -3` 换成已确认的 Python 3 命令。已有项目虚拟环境时可直接使用 `& '.\.venv\Scripts\python.exe' -B "$skillDir/scripts/probe_environment.py" --workspace .`。

**Linux Bash 或 WSL**

```bash
skill_dir="$PWD/.agents/skills/thesisforge"
python3 -B "$skill_dir/scripts/probe_environment.py" --workspace .
```

已有环境时可直接使用 `./.venv/bin/python`。Windows 上 Claude Code 采用 Git Bash 时使用其 Bash 引号与路径语法；若启动的是 Windows Python，虚拟环境解释器仍是 `.venv/Scripts/python.exe`。在 WSL、SSH 或容器中运行计算时，从该环境内验证解释器、数据和技能路径。按环境重建虚拟环境；可迁移的正式输入、代码和汇总数据可共享。保留各执行环境自己的运行记录和续跑目录。[环境探测与依赖](compute-environment.md) · [矩阵与续跑](experiment-matrix.md)

其他指南中的 `python` 表示选定环境的解释器，`<技能目录>` 表示实际加载路径。除非示例明确要求在技能根目录操作，否则研究文件按项目目录定位。传给运行器的命令和参数分别传递，JSON 清单中的路径分隔符优先用 `/`。外部软件按任务检查，NoC 的标准库回归可用于没有额外计算依赖的机器。

## 文档与研究辅助工具

只读稿件、DOCX 结构、证据记录和本地书目助手使用 Python 标准库，可在 Windows/Linux 和两个宿主中从实际安装路径运行。核心编辑无需这些脚本全部可用；选择相应任务所需工具即可。脚本写出 UTF-8 结果，管道调用者也应显式按 UTF-8 解码；解释器库导入不应改变宿主标准流。

LaTeX 构建还需项目实际引擎及 BibTeX/Biber；`build_latex.py --help` 和 [文档工作流](document-workflows.md)给出探测、独立构建目录与日志要求。Windows 的 `export_word_pdf.ps1` 是可选 Word COM 后端，Linux 不尝试创建 COM；可先完成只读 OOXML 审计与内容修订，再使用可用渲染器并说明目标端差异。不能把 LibreOffice/WPS 的预览称为已通过 Word 验收。

图形助手调用已安装的 Mermaid/draw.io，保存源、版本、命令和产物；不会下载未锁版本的 `npx` 包。简单项目依赖按已有安装授权处理，TeX 全套发行版、Word 许可、图形浏览器环境和服务器驱动等复杂缺口说明实际影响。Windows 批处理启动器与 Linux 可执行程序分别处理，不拼接跨 shell 命令。[可选制作后端](optional-workflows.md)

没有强制 Claude hook、特定模型或第三方云 API 的运行依赖。同一源码与资源由安装器装入两个宿主；测试宿主目录中资源可用不等于已经在每个宿主真实会话、每种 Office 或每个服务器运行过任务。验证记录只描述实际环境和实际结果。
