# v2 评价（对照第2轮调研清单 A1–A13）

评价标准：第2轮报告第14节必须编码的条目，以及「不把 **U** 或获取失败的数字写成规则」。v1 已通过的诚信轨道、一条主线、主张三档、SIGPLAN/Heiser 材料均应保留。

| 清单项 | v2 落点 | 判断 |
| --- | --- | --- |
| A1 7713.1—2025 条款与表 A.1 | `references/gbt-7713.1-2025.md`；`templates/front-matter-checklist.md`；`format-and-citations.md` / `dissertation-workflow.md` / `SKILL.md` 已去掉「摘要字数待核对」 | **已编码。** 4.6、5.2.6–5.2.7 引文、5.2.8、5.2.9（300–1000；关键词 3–8 与 CY/T 173；外文论文中文摘要宜不少于 5000）、5.3.7、表 A.1 必备性均写入。注明文本来自大学馆藏 PDF，非正式排印本。5000 字下限未套到中文论文。 |
| A2 7714—2025 类型、PID、差异表 | `references/gbt-7714-2025.md`；`templates/citation-examples-7714-2025.md` | **已编码。** `[PP/OL]`、`[DS/OL]`、`[CP/OL]`、PID 不重复、姓氏首字母大写、预印本/数据集/网站引用日期必备、2015→2025 差异表，以及报告中的完整示例。优先 8.11.3 的 `[CP/OL]`，B.10 `[EB/OL]` 标为未决不一致。第三方评论文章的额外说法未写成规则。正式排印本仍待第3轮。 |
| A3 学校叠加层 | `references/school-overlays.md` | **已编码。** 清华 2025-03、北大 2018/2019、东南已获取规则（摘要窗口、关键词、创新点位置、已核对排版、参考文献下限、所引旧国标）均写入。西电 2025 评阅权重 20/20/50/10 与「创新点明确凝练」已写；2014 手册明确为历史记录。国科大、北邮显式保持开放，未写入检索摘要中的未核实数字。叠加规则：学校窗口叠在 7713.1—2025 之上，不废止国标。 |
| A4 专业学位标准 | `references/moe-professional-doctorate-2024.md`；`templates/thesis-outline.md` 备选四段主体；`templates/review-checklist.md` | **已编码。** 11 个工程类专业学位类别（含电子信息）、文档形式菜单、八段结构、四段主体、质量维度。明确不默认套用到学术型计算机博士。复旦「至少三项贡献」写为评阅习惯而非国家法律。 |
| A5 中文学报卡片 | `references/journals-cn.md` | **已编码。** 计算机学报、软件学报、电子学报、通信学报的篇幅、摘要、关键词、创新点机制、参考文献下限、通信学报禁第一人称，均按报告第5节数字写入。半导体学报仅保留未核实存根。 |
| A6 通信仿真规程 | `references/experiment-design.md` 通信节及「通信链路/网络仿真规程」 | **已编码。** Pawlikowski 等 2002：事先声明相对误差/置信区间、序贯停止、暂态删除、独立重复或点名的区间方法、随机数流、报告区间。未写入事件数阈值。BER：报告观测错误数与不确定度；数字默认留作未核实。 |
| A7 器件/电路证据政策 | `references/venues-ieee-eds-cass.md`；`experiment-design.md` 器件节 | **已编码。** EDS touchstones；T-ED 默认至少部分物理验证（Ghione 社论仍 403，未编造例外）；TCAS-II 通常期望实测，特刊禁止纯仿真不写成对所有 TCAS 论文的常设规则。主张类型与证据类型对齐。 |
| A8 IEEE / Elsevier / ACM | `references/ieee-style.md`；`references/elsevier-venue-card.md` | **已编码（ACM 专刊数字推迟）。** IEEE Editorial Style Manual（2024-07-29）与 Reference Guide 中报告已列要点已写入；摘要词数不写成 IEEE 全局上限。Elsevier 按 IMRaD + 按刊填卡，不写入未归档的 Highlights 上限。ACM TOCS/TON 数字因获取失败显式推迟，只沿用第1轮已确立的 ACM 出版政策。 |
| A9 机器学习评价门禁 | `references/experiment-design.md` 机器学习节 | **已编码。** 泄漏与划分、公平超参预算、测试集复用、多种子均值、计算环境；不强制「5 个种子 / p<0.05」。 |
| A10 文献检索协议 | `references/literature-search.md`；由 `topic-and-contribution.md` 与 `SKILL.md` 的 `topic` 行指向 | **已编码。** Kitchenham & Charters PICOC、查询词族、多库检索、雪球、两轮筛查、缺口矩阵；选题用轻量变体。写明非 HCI 专用。 |
| A11 步骤级实验规程 | `references/experiment-design.md` 后半；`templates/experiment-plan.md` 指向三条规程 | **已编码。** 消融、通信仿真、器件 I–V/验证均按报告第11节，无口诀式 N。 |
| A12 中英文表述分档 | 并入 `references/writing-and-polish.md` 与 `argument-and-logic.md`，未另建第三份专文 | **已编码。** 主张写紧、范围诚实；无证据不写首次/填补空白；不堆叠限定；第一人称以学校/刊物覆盖 GB/T 6447—2025 的许可；英文贡献前置 + 事实性局限段。Zobel 只经课堂讲义转述。 |
| A13 评阅清单 | `references/review-rubric.md` 增补四轴；`templates/review-checklist.md` | **已编码。** 学术型：选题；创新点是否明确、凝练；论证与证据与主张相称；规范性。专业学位变体增加应用价值。西电 20/20/50/10 作为操作示例，不是国家法律。 |

## 有意推迟或标明未核实（与报告一致，不填口诀）

- 国科大、北邮摘要与排版数字（获取失败）
- 西电 2014 详细摘要与版式（仅历史记录）
- 半导体学报作者指南数字（获取失败）
- ACM TOCS/TON 篇幅等专刊规则（获取失败）
- Elsevier 某刊 Highlights/词数上限（未归档为稳定文本）
- Jeruchim 或任何具体 BER 事件数阈值（未合法取得一手文献）
- Ghione T-ED 社论原文及可能例外（HTTP 403）
- 7714 附录 B.10 与 8.11.3 的类型代码不一致（待正式排印本）
- 未对照条款表核实的 7714 第三方评论额外说法
- CY/T 173 关键词细则全文（5.2.9 已指向该标准，正文未展开）

## 与 v1 的连续性

诚信与证据轨道、SIGPLAN/Heiser 系统评价材料、主张三档、审查三级、一条主线和学校模板优先，均保留。`SKILL.md` 加载表列入运行任务可能用到的新参考，并仍要求不要加载 `dev/`。
