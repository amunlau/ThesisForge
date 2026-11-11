# 工程博士论文专项调研与验收

2026-11-11。围绕工程论文写作中三种会改变结论的问题独立检索。第一轮从项目证据和学位类型入手，第二轮从图表所需表达的技术关系及出版规格入手，第三轮从工程稿件和导师评阅经验入手。每轮分别记录检索词、已读出处、取用意见和适用边界，再将三组意见依次落实到技能。

| 调研与逐条出处 | 条目 | 采用 | 条件采用 | 舍弃 | 改动位置 |
| --- | ---: | ---: | ---: | ---: | --- |
| [工程贡献与论证，E01–E46](round1.md) | 46 | 32 | 11 | 3 | [工程论文论证](../../references/engineering-argument.md)、[贡献卡](../../templates/contribution-card.md)、[专业博士要求](../../references/moe-professional-doctorate-2024.md) |
| [科研图表，V01–V52](round2.md) | 52 | 33 | 16 | 3 | [科研图表指南](../../references/engineering-figures-tables.md)、[大纲](../../templates/thesis-outline.md)、[图稿检查工具](../../scripts/check_figure_pdf.py) |
| [写作与实质修订，W01–W48](round3.md) | 48 | 29 | 13 | 6 | [修稿与保真](../../references/engineering-revision.md)、[自然写作终检](../../references/natural-writing-and-review.md)、[章与图表审查清单](../../templates/review-checklist.md) |
| 合计 | **146** | **94** | **40** | **12** | [技能入口及按阶段加载表](../../SKILL.md) |

条数按可操作意见计。同一出处可以支持数条做法，不同来源重复提出同一问题时合并到运行指南。三份台账分别列 15、24、19 组来源，组内可以有同一文件的多个版本或章节，各轮之间也有共同来源。正式制度与投稿规格回到适用文件和模板核对。中外导师、科学网作者、研究生访谈和论坛原帖用于发现写稿难点及反例。相关技能里借鉴了机制解释、原始材料归属、相邻专业读者能否读懂等方法。页数、演示字号和自动确认流程均按材料原本的使用场景甄别。

## 三轮怎样修改及复核

1. **把创新点落到设计决策。** 工作章从实际瓶颈追到备选方案、作者负责的改动、支持该改动的观测及失效边界。E01–E06 用于区分工程性强的学术博士与专业博士，以及专业博士的两条申请路线。对照原件纠正了旧技能中的类别数和强制章节说法。E31、E36 用于核查选择何时会翻转、其他机制能否解释同一结果。NoC 案例中，进化策略较 FIFO 的两个均差为 −0.245 和 −0.311 周期/包。换为等预算随机搜索，差值变成 +0.077 和 +0.004。两类对照共同决定创新句能写到哪里。[通知及正式附件](https://grd.bit.edu.cn/docs/2024-09/90e1c97fad0a4e4aae8860970c78b1b5.pdf) · [归档比较表](../noc-smoke/results/summary.csv)
2. **在刊载尺寸下检查图表。** V01、V06–V11、V16–V21 和 V31–V36 分别进入按章规划、工程机制图、统计图和实际版面验收。为 NoC 短文补齐表题，从两类负载各 12 条留出轨迹重绘同预算逐轨迹差，显示热点负载中的持平与反向观测。预览时发现密集点与均值标记靠得太近，调整了标记的垂直距离后重新渲染。单页矢量 PDF 的画布为 88.9 × 50.8 mm，中文字形已嵌入。按 88.9 mm 放置，最小可提取文字为 9 pt；按 44.45 mm 放置为 4.5 pt，指定 9 pt 门槛时工具返回失败。这个门槛取自本次制图选择。其他目标刊及学校按各自模板执行。[NoC 结果、原始数据入口与题注](../noc-smoke/article.md) · [IEEE 图中文字说明](https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/create-graphics-for-your-article/file-formatting/)
3. **让润色保住事实，让返修能改动论证。** W01–W04、W22、W30–W33、W40–W44 用于章节之间的真实依赖、正文解读图意、实测与机理推测的区分，以及数字与事件的归属。FIFO 例中六组参考队列共运行 892 个周期，391 次入队、375 次出队、16 项被复位清除。特意保留全部数字并把原因改成“拥塞丢失”，逐事件回核才发现错误。本轮重新计算了参考队列，RTL 结果取自此前独立仿真验收。[FIFO 检查程序](../compute-smoke/fifo/check.py) · [RTL 验收记录](../compute-execution-validation.md)

另外请独立读者只带改稿委托和原始稿，从技能入口走一次整章返修和一次单句润色。在“首次实现通用工业部署价值”这一错例上，实质返修得到可替换段落，分别写出了相对 FIFO 的平均收益与相对随机搜索的比较，标明固定 XY 路由、搜索预算及留出轨迹。单句润色只处理主语歧义，把原判断同记录冲突的证据另列。两次均从正常入口找到适用指南。

## 复核图表与数据

在项目根目录运行下列命令。NoC 的六项回归使用 Python 标准库，其中一项从零重跑两种搜索与全部留出轨迹，并与归档 CSV 核对。检查图稿的解释器另需 PyMuPDF。其三项测试覆盖缩放字号、非等比放置的旋转位图和没有可提取文字的轮廓图。

```text
python -B dev/noc-smoke/test_mesh.py -v
python -B dev/test_check_figure_pdf.py -v
python scripts/check_figure_pdf.py dev/noc-smoke/paired-search-effects.pdf --placed-width-mm 88.9 --min-text-pt 9
python scripts/check_figure_pdf.py dev/noc-smoke/paired-search-effects.pdf --placed-width-mm 44.45 --min-text-pt 9
```

最后一条是故意缩小的反例，预期退出码为 1。检查原生文字和内嵌位图的报告不能判断箭头交叉、图例遮挡、配色可读性以及轮廓化汉字，仍须查看渲染成品。图稿的源数据、绘图代码与重新导出步骤见 [NoC 用例](../noc-smoke/README.md)。

同时从逐轨迹记录独立核对成稿两张表的全部均值、配对标准差、胜平负和三位小数显示，检查矢量稿含 24 个数据点及一个图例圆点。机制图以同源双包回归为依据，展示选包顺序能改变各包的交付时刻，而该双包例中的平均时延仍为 2.5 周期/包。[带图的工程机制示例](../../references/engineering-figures-tables.md) · [可重跑测试](../noc-smoke/test_mesh.py)
