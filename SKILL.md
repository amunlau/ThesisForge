---
name: thesisforge
license: PolyForm-Noncommercial-1.0.0 (see LICENSE and NOTICE)
description: >-
  用于计算机、通信、电子方向的自主实验研究及硕博士、期刊或会议论文写作。从一个主题出发检索相近工作、提出可反驳的假设、检查环境、编写并执行数据分析、仿真、HDL 功能验证或 AI 训练推理实验，把实际结果写成论文。适用于工程博士论文的设计取舍、创新点凝练、科研图表制作、整稿审阅与保真润色，也可逐条回复专家或审稿意见，对照原稿与修改稿制作修改说明、对照表及覆盖核查。
---

# ThesisForge

面向计算机、通信与电子工程的学位论文、期刊稿和会议稿。默认中文，成稿语言、范围和格式服从委托。先识别用户要拿到的成果，再加载相应参考。实验和稿件写入用户的研究目录。

在 Claude Code 和 Codex 中，以宿主实际加载的本文件所在目录定位 `references/`、`templates/` 和 `scripts/`。打开参考中的链接时，以该参考文件为基准。研究数据、项目环境和运行输出按研究项目定位。启动计算工具时传入脚本的实际路径，并使用运行节点上的 Python。仅委托写作、审阅或润色时，直接处理指定材料，按约定格式交稿或意见。[跨平台运行与调用](references/platforms.md)

## 选择任务与交付物

| 用户委托 | 执行到哪里 |
| --- | --- |
| 选题、开题或设计实验 | `topic`、`design`。交研究问题、与近邻工作的区别、可检验的方案及判据。拟做的实验标为计划。 |
| 自己做实验、分析结果、直接成文 | `topic → design → execute → analyze → write → review`。检查环境，运行基线与候选方法，保存原始结果，从记录重建分析，交可复跑材料与完整论文稿。已有可靠实现和数据时从相应阶段接入。 |
| 分析已有数据，或根据材料写作 | `analyze`、`write`。先查数据来源、实验单位和比较条件，再交相应的结果、图表或稿件。综述按文献综合，理论研究按定义、证明或反例组织。写作本身不触发新实验。 |
| 只审阅／只润色／直接纠错或实质返修 | `review` 交定位和意见，保留正文。`polish` 交指定范围的润色稿，保留技术含义。明确要求直接改正时，在委托范围内核实并改正文、复查关联位置。兼要审阅件和干净稿时从同一原稿起步。 |
| 回复审稿、学位论文评阅或具体抽检意见 | `rebuttal`。原意见保留原话与编号，拆分独立关切，先核真实稿件/变更，再逐条写回应、证据和修改位置。处理决定、完成状态、独立核验分别记录；按实际学校回函或刊会要求交付。 |
| 两稿修改说明、对照表或回复覆盖核查 | `revision-diff` 比较实际提供的原稿和修改稿，交有定位的修改说明与对照；`response-audit` 核原意见、回复、真实变更和最终位置。没有意见时不编造专家关切；只有修改稿时不能确认哪些内容是本轮新增。 |

材料不全时先做已有条件允许的部分。仅在缺口会改变研究对象、正式实验或交付形式时补问。深度默认为 `standard`，指定片段的快速处理用 `quick`，系统调研和通篇预审可用 `deep`。用户指定的核查深度和修改范围分别执行，包括深入审阅一段摘要。[接入与模式](references/intake-and-modes.md)

长稿和多轮研究沿用一份轻量项目记录，保存用户已定事项、实际读过的范围、关键主张与证据、当前文件身份和未解问题。源数据、脚本或稿件改变后，重新检查受影响的图表、结论和旧验收；不要重复索取已确认信息。短任务只留必要记录。[证据与恢复](references/evidence-ledger.md) · [项目记录模板](templates/project-record.md)

## 确定适用规则

- **学位论文。** 先确认国家或地区、学位类型、专业类别和授予单位。工程课题也可属于学术学位。中国工程类专业学位申请要核对本校及学院的实施细则。八类工程专业硕士按工程教指委〔2026〕10号区分应用研究型专题论文和规定的实践成果，八类工程专业博士按学位办〔2024〕18号核对相应路线。0854 类别要求适用于电子信息专业学位。《学位法》对博士另有创新性成果要求。[学位论文流程](references/dissertation-workflow.md) · [工程类专业硕士通知](https://meng.tsinghua.edu.cn/xxfb/tzgg/6347.htm) · [工程类专业博士要求](references/moe-professional-doctorate-2024.md)
- **编写与排版。** 中文学位论文按学校采用的规范和模板，缺项可参照 GB/T 7713.1。期刊或会议稿先查具体稿约、文种和投稿阶段，中文学术论文可参照 GB/T 7713.2。GB/T 是推荐性国家标准，被明确采用时按相应文件执行。查清“应”“宜”“资料性示例”的差别。摘要字数、版芯、图字、参考文献体例随所交文稿确定。模板未知时先完成内容，注明待核格式。[格式与引用](references/format-and-citations.md) · [学位论文编写](references/gbt-7713.1-2025.md) · [期刊论文编写](references/gbt-7713.2-2022.md)
- **投稿范围。** 具体刊物、文章类型和当前作者指南决定投稿要求。“SCI B 类”等机构分级需要对应学科、目录和年份，未知时可继续做研究并注明期刊匹配待核。扩展会议版须按目标出版方规则引用及披露前作。[期刊论文流程](references/journal-workflow.md)

## 从问题到可交付的论文

1. **锁定研究对象和可检验的贡献。** 找到最接近的工作及真实约束，说明本文改变了哪个设计、推导或测量，以及什么证据能区分这个改变。方法、系统、评测和理论贡献各自匹配证据；按需要说明模块的输入、处理、输出、接口和设计代价，核对训练/推理或控制/数据关系。对学位论文，组织各章共同回答的总问题，交代真实的章间依赖或并行关系。已有发表成果能否并入及如何注明作者分工，按本校规定。“首次”“最优”需要与其范围相称的检索、比较或证明。[选题与创新点](references/topic-and-contribution.md) · [论证与逻辑](references/argument-and-logic.md)
2. **按委托执行。** 做计算实验时，在实际执行节点验证环境与最小已知答案，明确基线、预算、重复单位与停止条件后再正式运行。普通依赖在项目隔离环境内解决。要求先告知时说明用途和位置，明确要求同意后安装时等待同意。遇驱动、许可证、付费或权限缺口时说明受影响的实验、需用户完成的操作和复验命令，继续可独立完成的工作。[自主实验研究](references/computational-research.md) · [实验设计](references/experiment-design.md)
3. **从证据写结果。** 分清现场测量、原型测试、仿真、文献数据与推导。逐条核主张与对应的基线、分母、单位、不确定度和失败条件；图中展示的子集与实际统计总体分开记录。收益、无优势与反向结果都如实报告。若只能支持部分条件，把条件写在判断旁；机制仍属解释时明示。结果表、正文、章小结和摘要/结论引用同一事实时保持口径一致。[数据分析](references/data-analysis.md) · [诚信与证据](references/integrity-and-evidence.md)
4. **按章组织图表。** 工程整稿按主张决定哪些机制、设计取舍和关键数据值得展示。用真实设计或记录制作原创图和可编辑表，配题注、正文解读和可回查的源材料；在最终栏宽查看字、线、符号、灰度和布局。局部润色按用户限定的范围处理。[工程论证](references/engineering-argument.md) · [工程科研图表](references/engineering-figures-tables.md)
5. **回读真实交付版本。** 所有生成或审阅的实质文字均检查原意、突兀衔接、空泛评价、技术错误与依据归属。只润色时保护数值/公式/引用和条件/否定/比较关系，不无据加强或削弱结论；重要结构或主张变化留可定位的说明。已发现但会改变结论的事实冲突另列。有权实质订正时改稿并核对受影响的摘要、题注和结论。只审阅时，按六类说明问题性质，按阻断、主要、次要说明影响。可交零项意见，并注明审查范围。排版文件按实际成品核对，结构扫描与最终视觉验收分别记录。[自然写作与终检](references/natural-writing-and-review.md) · [工程写作与修订](references/engineering-revision.md) · [文档验收](references/document-workflows.md)

文献、数据、DOI、结果、应用证明和个人贡献均须可追溯。无结果的工作写为计划，已知的局限随结论交代。审阅区分资料不足与已核实错误。“AI 味”审阅定位具体语言或推理问题，保留准确自然的原文，不推断作者身份或生成概率。学校或刊物要求的 AI 使用披露随稿保留。

## 按阶段加载

| 当前任务 | 参考与可填写材料 |
| --- | --- |
| 选题、独立研究与文献对照 | [检索协议](references/literature-search.md)、[独立研究](references/independent-research.md)、[学科与领域差异](references/domain-cs-app.md)、[贡献卡](templates/contribution-card.md)、[研究问题矩阵](templates/rq-matrix.md) |
| 数据、仿真、HDL 或 AI 实验 | [环境探测与依赖](references/compute-environment.md)、[矩阵运行与接续](references/experiment-matrix.md)、[仿真及数字逻辑验证](references/simulation-and-hdl.md)、[数据与 AI 分析](references/data-analysis.md)、[实验方案](templates/experiment-plan.md) |
| Benchmark、数据集论文或明确委托系统综述 | [评测与文献综合](references/benchmark-and-synthesis.md)、[评测计划](templates/benchmark-plan.md)。普通相关工作沿用检索协议；元分析先核可合并性，不假称本包有通用统计合成引擎 |
| 学位论文结构、摘要、著录或预审 | [学位论文大纲](templates/thesis-outline.md)、[学校细则与材料日期](references/school-overlays.md)、[前置要素清单](templates/front-matter-checklist.md)、[文摘](references/gbt-6447-2025.md)、[关键词](references/cyt-173-2019.md)、[参考文献著录](references/gbt-7714-2025.md)。复旦自然科学学术博士的具体表格见[该校评阅书](references/fudan-review-2025.md) |
| 期刊、会议或扩展已有稿件 | [期刊大纲](templates/journal-outline.md)、[中文期刊](references/journals-cn.md)、[IEEE 体例](references/ieee-style.md)、[器件与电路期刊](references/venues-ieee-eds-cass.md)、[网络、ACM 与 Elsevier 期刊](references/venues-acm-elsevier.md)、[其他 Elsevier 稿约核对](references/elsevier-venue-card.md) |
| 写作、整稿或限定润色 | [中英文写作与润色](references/writing-and-polish.md)、[工程论文修订](references/engineering-revision.md)。按需用[字面量检查](scripts/check_literals.py)及[稿件静态审计](scripts/audit_manuscript.py)，仍须回读单位、归属和语义 |
| Word 排版、LaTeX 工程构建与文档交付 | [文档工作流](references/document-workflows.md)。先审计模板与原稿，限定修改范围，保存实际构建/导出记录；没有目标端渲染不宣称版面已验收 |
| 科研图表规划与制作 | [工程图表](references/engineering-figures-tables.md)、[图稿计划](templates/figure-plan.md)、[可选图形后端](references/optional-workflows.md#图形制作与复刻) |
| 审阅、预答辩、返修、盲审稿与投稿材料 | [审查量表](references/review-rubric.md)、[审查清单](templates/review-checklist.md)、[审查报告](templates/review-report.md)、[修订与提交](references/revision-and-submission.md)。按委托采用对应栏目，只报告真实发现和待核事项 |
| 专家/审稿逐条回复、双稿说明与覆盖核查 | [专用回复流程](references/reviewer-response-workflow.md)、[回复模板](templates/reviewer-response.md)、[修改对照模板](templates/revision-comparison.md)。按需用[两稿提取与比较](scripts/compare_manuscripts.py)和[回复核查](scripts/audit_reviewer_response.py)；字面差异与登记覆盖不等于意见已解决 |
| 长稿恢复、检查失效与局部补丁 | [证据记录](references/evidence-ledger.md)、[记录助手](scripts/research_ledger.py)。记录检查范围和文件身份，不把元数据完整或登记项通过称作全文科学认证 |
| 教学式辅导、跨模型复核、答辩、其他文档后端 | [可选工作流](references/optional-workflows.md)。按用户任务和实际可用能力启用，保持普通研究和润色轻量 |

需要补证或深度调研时，可使用已安装的 research-to-report-and-briefing；Unbot 的编辑方法已内置，原生批注可借助相应的文档工具。外部技能可用时按任务调用，未安装时仍按本技能完成。研究材料在获准范围内使用。按需加载参考。工程指南所引的 NoC 示例随安装提供，开发调研记录在源仓库的 `dev/` 中。
