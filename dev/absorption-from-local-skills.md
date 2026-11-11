# ThesisForge 设计备忘：从本机技能吸收的方法

来源：本机 `research-to-report-and-briefing`（深度调研、报告与专业汇报，v3.3.0）、
`academic-topic-research-agent`、`technical-writing`、`research-deep`。
本文件是编写 ThesisForge 的内部依据，不作为对外 skill 正文。

## 必须吸收

1. **渐进加载**：SKILL.md 只保留入口、模式、主流程和「当前阶段读哪份参考」对照表；细则放在 `references/`，禁止一次读完全部文件。
2. **证据与断言分级**：观察 / 推导 / 解释 / 假设分开；`supported` / `qualified` / `disputed` / `unverified`。未核实内容不得写成既定事实，不得编造文献、数据、实验、引用、指标。
3. **安全的创新点表述**：写清检索范围与对照对象，用「已有工作覆盖 A/B，较少同时满足 A+B+C 并落在某具体条件」；禁止「没人研究过」。
4. **问题—主张—证据—反证**：每条核心主张写清会削弱它的事实；覆盖度用问题是否被解释衡量，不用文献数量冒充充分。
5. **先校准判断，再改句段**：先核对象、条件、基线、断言强度，再补因果、调结构、删空话。限定语只放在决定判断的位置，不给每句叠「可能 / 一定程度 / 总体而言」。
6. **去空话而不是禁词**：靠补机制、条件和证据，不靠替换列表或故意口语化。术语全文统一；同级分类用同一维度。
7. **质量分三级**：S1 事实/因果/引用错误必须修；S2 逻辑断层、创新点与证据不匹配、格式关键项缺失必须修；S3 局部措辞集中处理，不吹毛求疵、不无限扩大审阅。
8. **模块化而不是死流水线**：按任务选用模块（选题、综述、设计实验、分析、撰写、审查、润色）；缺关键输入时一次问清，能推进则推进。
9. **选题锁定与漂移警告**：用户原意优先；后续检索或设计明显跑题时先标明再继续。
10. **创新点可被区分**：贡献必须能指出邻居工作抓不到的具体配置/维度/条件，而不是换一个名称。
11. **RQ 要带失败条件**：每个研究问题对应实验/指标/证据目标/何种结果会推翻或改写主张。
12. **摘要与标题安全**：没有结果时不得写「实验表明 / 显著提升 / 我们证明」；已有结果则按证据强度直书，不必故意写弱。
13. **审稿攻击表是内部工具**：用来预判并在正文该出现的位置补证据（基线、消融、局限），不要把防御性措辞堆进全文。
14. **期刊/学位适配优先于通用模板**：学校格式、目标期刊作者指南覆盖默认结构。
15. **默认学科**：计算机应用技术，覆盖计算机、通信、半导体电子；默认中文，英文稿按用户或期刊要求。

## 与用户要求对齐的写作立场

- 严密度：对标人类专家审稿，够硬、够闭合即可。
- 不吹毛求疵：不因无关小疵阻断交付，不把可选风格偏好写成错误。
- 避免过度防御：证据够就写够；局限集中在范围/讨论/局限性，不把每句改成「在某种意义上也许」。
- 实验与数据：可设计可执行方案，可基于真实测量、用户数据或诚实跑出的仿真/实现结果写作；禁止编造数字来撑稿。

## 建议的对外目录（初稿，待三轮调研修订）

```
ThesisForge/
  SKILL.md
  README.md
  references/
    intake-and-modes.md
    integrity-and-evidence.md
    dissertation-workflow.md
    journal-workflow.md
    topic-and-contribution.md
    experiment-design.md
    data-analysis.md
    argument-and-logic.md
    writing-and-polish.md
    format-and-citations.md
    review-rubric.md
    domain-cs-app.md
  templates/
    thesis-outline.md
    journal-outline.md
    contribution-card.md
    experiment-plan.md
    rq-matrix.md
    review-report.md
  dev/
    iteration-log.md
```

`dev/` 只保留迭代记录，运行 skill 时不加载。

## Unbot 核心能力整合（2026-11-11）

按用户本次要求，将 Unbot 从可选外援推进为内置编辑能力。读取本机 `unbot/SKILL.md` 及 `references/style-review.md`、`coherence-review.md`、`review-protocol.md`、`chinese-english-style.md`、`scripts/check_literals.py`；不宣称已核对远端最新版，不改写 Unbot 本体。

- 规则落在 `references/natural-writing-and-review.md`，入口对所有文字输出加载；写作、逻辑、接入、诚信、审查量表、学位/期刊流程及审查模板均有接入。核心能力无需额外安装。
- 吸收自然专业书面语、信息增量判断、按读者顺序查突兀、固定语义约束、中英事实对照、六类有定位的意见、最终版本双向终检和长稿轻量恢复记录。六类性质与原三级严重度正交，不替代学校评阅轴。
- 初次本地试验使用了 Unbot 字面量核对脚本的副本，原文件 SHA-256 为 `4823f5bb52e2eaf6ac943cc12b4ba768f49adfabcd62d4fb701051412c597abf`。本地版本未附分发许可，公开仓库改为依据命令行契约和回归用例独立实现。项目保留对 Unbot 编辑方法的来源说明。
- 脚本计数不能证明语义不变；数值归属、单位、条件、否定、因果和引用仍人工核验。原生批注或版面须在实际文件回读，不能凭提取文本声称完成。
- 不凭文风推断作者身份，不输出无依据 AI 率、不承诺检测器通过；不靠口语、编经历、错字或删限定制造“人味”，不隐藏按学校/刊物要求应披露的 AI 使用。

早期验收记录描述当时的本地版本。公开版的授权范围见仓库根目录的 [LICENSE](../LICENSE) 与 [NOTICE](../NOTICE)。
