# ThesisForge

ThesisForge 是面向计算机、通信与电子工程的论文研究技能，适用于 Windows 和 Linux 上的 Claude Code 与 Codex。给出一个主题，它可以检索相近工作、设计并运行对照实验，从原始数据制作图表，再把结果写成论文。已有稿件也可以只做审查、润色或返修。

## 安装

克隆或下载本仓库，进入包含 `install.py` 的目录。安装器仅需 Python 3.9 或更新版本。将下面的路径换成你的论文项目目录，选择本机对应的一条命令。

**Windows PowerShell**

```powershell
py -3 install.py --host both --project "D:\研究项目\我的论文"
```

**Linux 或 WSL**

```bash
python3 install.py --host both --project "$HOME/研究项目/我的论文"
```

- `--host both` 会把技能装入项目的 `.claude/skills/thesisforge/` 和 `.agents/skills/thesisforge/`。只使用一个宿主时，选 `--host claude` 或 `--host codex`。
- 多个项目共用时，用 `--user` 代替 `--project 路径`。在实际运行宿主的系统内安装，Windows 原生与 WSL 的个人目录各自独立。
- 更新仓库后，用同一条命令加 `--update`。若原安装内容有变化，安装器先备份旧副本，并在终端显示其位置。个人目录、手工路径和云端 Codex 的用法见[平台说明](references/platforms.md)。

纯写作也可手动部署。在上述宿主技能目录下建立 `thesisforge/`，复制 `SKILL.md`、`LICENSE`、`NOTICE`、`agents/`、`references/`、`templates/`、`scripts/` 和 `dev/noc-smoke/`，保留原目录结构。

## 如何调用

安装后在**论文项目**中打开新会话。Claude Code 输入 `/thesisforge`，Codex CLI 或 IDE 输入 `$thesisforge`，然后接上研究任务。在支持本地技能的 ChatGPT 桌面客户端，可输入 `@` 并选择 ThesisForge。[平台与调用方式](references/platforms.md)

要从一个主题直接写成论文，可以像下面这样约定实验范围、交付物和安装权限。

> 研究 NoC（片上网络）中的流量任务调度。请比较遗传算法、蚁群算法等方法与已有工作，选一个可检验的改进方向。自己设计、编写并运行仿真，分析实际结果，直接写成论文。目标是我单位认定的 SCI B 类期刊。需要特定环境时先告诉我，简单依赖在项目内安装，涉及驱动、许可证或服务器权限时告诉我如何处理。

这类任务会留下可复跑的代码、原始结果和分析。期刊分级按委托方适用的目录核对，创新点依据近邻工作及实际比较结果表述。[自主实验研究流程](references/computational-research.md)

| 任务 | 可以直接接在技能名后的委托 |
| --- | --- |
| 工程博士论文 | 根据架构说明、RTL 和测试记录重写第 3、4 章。区分我的设计贡献与团队已有实现，补一张能解释反压的时序图。 |
| 数字逻辑验证 | 设计一个带反压的 FIFO，编写 SystemVerilog 和自检测试台，实际运行边界及随机测试，交付验证结果和论文方法段。 |
| AI 训练与推理 | 在现有服务器上对分类模型做消融，使用相同的数据划分和训练预算。重载检查点做推理，报告多次独立重复的准确率差与耗时。 |
| 审稿与保真润色 | 检查摘要里的空泛措辞、突兀衔接和技术错误。标出原句，给出最小改法，保留数字、单位和结论强度。 |
| Word 博士长稿 | 先审计论文的样式、分节、编号和交叉引用，再按学校模板修正指定问题；保留原稿，核对最终 Word 与 PDF。 |
| LaTeX 与投稿返修 | 检查多文件工程的引用、标签和术语，在工作副本实际构建；逐条回复评阅意见，让回复指向本次真实修改。 |
| Benchmark 研究 | 围绕 NoC 负载或模型能力设计评测集，说明覆盖、排除项和污染风险，实际执行基线，报告分层结果及失败案例。 |
| 专家意见逐条回复 | 根据评阅书、原稿和修改稿，按学校表格写博士论文修改说明；逐条保留意见及子问题，对应真实变更和最终位置，未核实的修改明确标出。 |
| 两稿对照与覆盖核查 | 对照原稿、修改稿和回复信，生成修改对照表，检查有没有漏回、声称已改却缺证据、旧页码或未兑现的上一轮承诺。只有两稿时只做修改说明。 |

文风审查借鉴 Unbot 的编辑方法。它会指出哪句话缺少依据、哪个转折跳过了推理步骤，以及怎样在保留技术含义的前提下改写。“AI 味”意见针对文字本身，不给出作者身份或生成概率判断。仅要求审查时交定位和意见，要求修改时交相应稿件。[自然写作与终检](references/natural-writing-and-review.md)

## 长稿、证据与文档工具

长项目沿用一份记录，连接研究问题、证据、图表、正文主张与返修意见。文件或依赖改变后，旧结论和验收需要重新核对。短段落润色保持轻量；判断文风时也保护否定、条件、比较对象与结论强度，既不无据增强，也不无据弱化。

以下工具按任务使用。文本、DOCX、书目和证据记录的 Python 工具使用标准库；PDF 提取、回复中的 PDF 定位核查与图稿检查需要可选的 PyMuPDF，绘图和排版另需实际可用后端。以技能安装目录中的真实脚本路径运行，输入和产物放在论文项目中。

| 工具 | 用途与边界 |
| --- | --- |
| [稿件静态审计](scripts/audit_manuscript.py) | 多文件 LaTeX、引用/标签、术语及数值关系疑点；只读扫描，有定位和覆盖说明，不能自动证明语义保真。 |
| [DOCX 结构审计](scripts/audit_docx.py) | 动态样式继承、段落/表格/文本框、分节、编号、域及修订；Windows/Linux 可用，分页和图中字仍需实际渲染。 |
| [LaTeX 构建](scripts/build_latex.py) | 探测工具，在新工作副本构建并记录日志、文献失败和未解引用；需要对应引擎与模板。 |
| [Word 导出](scripts/export_word_pdf.ps1) | Windows 已有 Word 时更新工作副本的域并导出 PDF，可同时交付 DOCX；不改原稿，不把导出成功当版式通过。 |
| [证据记录与局部补丁](scripts/research_ledger.py) | 记录文件指纹及依赖，识别失效证据和检查；精确补丁先核原稿身份，再写新文件。不会认证论文事实。 |
| [本地题录导入](scripts/import_bibliography.py) | BibTeX/RIS/JSON 导入，保留来源、重复项与拒绝日志；不会把导入成功当引用已核实。 |
| [图形导出适配器](scripts/render_diagram.py) | 调用现有 Mermaid/draw.io CLI，保留图源、日志及输出身份；可编辑性、图义和最终尺寸另行检查。 |
| [两稿提取与比较](scripts/compare_manuscripts.py) | 从 Word、文本/LaTeX 源文件或 PDF 提取带版本身份的文本与评论，生成两稿字面对照；PDF 需要可选 PyMuPDF，Word 修订视图与实际页面另核。 |
| [逐条回复核查](scripts/audit_reviewer_response.py) | 核登记意见及子问题、回复、证据与定位的对应关系；区分已报告完成、文件证据和未独立核实，不将覆盖率当作问题解决率。 |

操作方式见[文档工作流](references/document-workflows.md)、[证据记录](references/evidence-ledger.md)、[本地题录](references/literature-search.md)和[可选工作流](references/optional-workflows.md)。科研图表按论证需要规划数量与信息密度，检查最终栏宽下的文字、线条、误差含义与读序；不靠统一图数或缩字堆密度。[图稿计划](templates/figure-plan.md)

工程能力整合阶段从五套参考技能吸收工程论证、保真编辑和文档审计等方法，以独立实现接入现有实验流程。逐项去向、已采纳的决策和该阶段验证范围见[整合记录](dev/reference-integration.md)。Typst、答辩演示、外部文献连接器等按需调用已有能力，不宣称本包已经内建全部后端。

专家/审稿回复专项参考了另行核对的 15 个条目。任务可从原始意见、已有回复、两版稿件或部分材料接入；处理决定、实际完成和核验状态分别记录。学校评阅、盲审修改说明、具体抽检回函、期刊返修信和会议短回复各按实际要求组织，不假设存在通用抽检表格。见[专用流程](references/reviewer-response-workflow.md)和[来源与取舍](参考skills/审稿回复调研/README.md)。

## 可复跑的 NoC 示例

在 4×4 XY 网格仿真中，进化搜索与随机搜索各评估 24 个候选注入策略。冻结策略后，用 12 条均匀流量轨迹和 12 条热点流量轨迹测试。下表为平均时延，单位是周期/包。

| 留出负载 | FIFO | 固定启发式 | 随机搜索 | 进化搜索 |
| --- | ---: | ---: | ---: | ---: |
| 均匀 | 5.919 | 5.632 | 5.597 | 5.674 |
| 热点 | 31.851 | 31.697 | 31.536 | 31.540 |

在这两组负载上，进化策略平均都快于 FIFO，但均未优于等预算随机搜索。归档保留每条轨迹的原始结果、训练评分和配对差值，可随时查证论文中的结论。[研究短文](dev/noc-smoke/article.md) · [逐轨迹数据](dev/noc-smoke/results/paired.csv) · [配对差值图](dev/noc-smoke/paired-search-effects.pdf)

在仓库根目录执行 `python3 -B dev/noc-smoke/test_mesh.py -v`，即可仅用标准库从头复跑仿真、逐字节比对归档 CSV，并检查汇总能否识别不可能的时延记录。开发回归使用 `python3 -B -m unittest discover -s dev -v`。Windows PowerShell 将 `python3` 换为 `py -3`。PDF 提取、定位与图稿检查需要 PyMuPDF，缺少该依赖时对应测试会跳过。[实验与复跑说明](dev/noc-smoke/README.md) · [计算后端验收](dev/compute-execution-validation.md)

## 项目导航

最近一次[系统审计与提交前复核](dev/systematic-audit-2026-11-18.md)记录了规则冲突、证据与文档工具修复、拟提交快照验证、跨平台回归及尚未验证的范围。

- 技能从 `SKILL.md` 加载相应阶段的规则。`agents/openai.yaml` 提供 Codex 的显示名称和默认提示。[技能入口](SKILL.md)
- `references/` 收录按任务使用的指南，涵盖工程创新点、科研图表、论文结构与实质修订。[工程论证](references/engineering-argument.md) · [科研图表](references/engineering-figures-tables.md) · [工程论文修订](references/engineering-revision.md)
- `templates/` 提供可填写的研究问题矩阵、实验计划、贡献说明及审查清单。[实验方案](templates/experiment-plan.md) · [贡献卡](templates/contribution-card.md) · [审查清单](templates/review-checklist.md)
- `scripts/` 提供环境探测、实验运行与续跑、配对分析、文字保真及图稿检查工具。[实验环境](references/compute-environment.md) · [实验矩阵](references/experiment-matrix.md) · [数据分析](references/data-analysis.md)
- `dev/` 保存回归测试、可复现实验和技能的调研依据。[五轮实验能力迭代](dev/experimental-execution-five-rounds.md) · [工程博士论文专项调研](dev/engineering-research/README.md)

## 许可证与来源

本仓库的原创代码、技能规则、文档、模板和示例按 **PolyForm Noncommercial License 1.0.0** 提供。该许可证允许非商业用途，并明确列出教育机构、公共研究机构等组织的允许用途。超出许可范围的商业使用需另行取得授权。[许可证全文](LICENSE) · [PolyForm 官方条款](https://polyformproject.org/licenses/noncommercial/1.0.0)

分发本技能、修改版或其中任何部分时，应向接收方提供许可条款或其官方网址，并原样保留来源声明中的每一行 `Required Notice:`。直接随包附上 `LICENSE` 和 `NOTICE` 即可。仅使用工具写成的原创论文、用自己的数据得到的实验结果，无须因此给本项目署名。若作品实际复制了包内材料，分发相应部分时仍按许可证处理。[来源声明](NOTICE)
