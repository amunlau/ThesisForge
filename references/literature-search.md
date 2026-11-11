# 文献检索与选题协议

把「从文献到缺口」做成可执行步骤，而不是只写原则。协议压缩自 Kitchenham 与 Charters，《Guidelines for performing Systematic Literature Reviews in Software Engineering》，EBSE Technical Report EBSE-2007-01，Keele University and Durham University，2007。这是软件工程系统综述规程，**不是**只适用于人机交互，也不是医学 Cochrane 手册。通信与器件题目可用同一规程，替换为领域数据库和 PICOC 取值。

系统综述只有在真正执行并记录了协议之后才能声称；选题阶段用下方的轻量变体。题目锁定与创新点写法见 [选题与创新点](topic-and-contribution.md)。

## 1. 用 PICOC 写出问题（或声明采用的子集）

Population，Intervention，Comparison，Outcome，Context。领域对应示例：

- **计算机系统：** Population = 系统或负载类别；Intervention = 拟采用的机制；Comparison = 基线；Outcome = 声明的指标；Context = 部署假设。
- **通信：** Population = 链路或网络场景；Intervention = 编码 / MAC / 资源分配 / 仿真模型等；Comparison = 标准或已有方案；Outcome = 误码、吞吐、时延、能耗等；Context = 信道与业务假设。
- **器件：** Population = 器件或工艺类别；Intervention = 结构 / 工艺 / 模型；Comparison = 已有器件或紧凑模型；Outcome = I–V、跨导、可靠性、射频指标等；Context = 节点、温度、偏置。

## 2. 检索前写下协议

预先规定纳入/排除标准、时间窗口、语言、文献类型（期刊、会议、预印本政策），以及质量评价问题。协议或纳入标准若有改动，必须记录并解释，不能偷偷改口。真正做系统综述时，可把 Kitchenham、Madeyski、Budgen，*SEGRESS: Software Engineering Guidelines for REporting Secondary Studies*，《IEEE TSE》49(3):1273–1298，2023（在线 2022-05-10，DOI 10.1109/TSE.2022.3174092，CC BY 4.0；本轮作者站点 PDF 因 TLS 未保存本地页码，引用用条目号）及 PRISMA 2020 条目 24c 作为可选**报告**参考。SEGRESS 是二次研究的报告指南，不是宣布 Kitchenham 与 Charters 2007 年实施指南已被替代。

## 3. 查询词族，而不是碰一条幸运字符串

为每个 PICOC 要素列出同义词与领域用语（IEEE 用语与中文用语、缩写与全称、器件名称与结构名称）。词族内部用 OR，词族之间用 AND。同一词族至少跑**多于一个**索引：最低限度包括 IEEE Xplore、ACM Digital Library，以及一个综合索引（Web of Science / Scopus / EI），中文文献加 CNKI（中国知网）或万方。器件题目需要时再补相关 IET / Elsevier 刊源；国内通信题目可补 IEICE 或通信学报等索引。保存**确切查询式**和检索日期。

## 4. 雪球

压缩自 Wohlin，《Guidelines for Snowballing in Systematic Literature Studies and a Replication in Software Engineering》，EASE 2014（作者站点 PDF）。该文把 snowballing 写成系统文献研究的一种检索策略，并区分 backward（参考文献）与 forward（引证）。选题阶段仍用下方轻量变体；系统综述只有真正执行并记录了协议之后才能声称。不要把所有学位论文写成必须先做系统综述。

可执行步骤：

1. 选定起始集，并记录纳入理由（例如已知的关键论文，或上一轮检索已纳入的文献）。
2. 逐轮做后向（其参考文献）与前向（谁引用了它）。
3. 每轮记录候选，以及纳入或排除的原因。
4. 直到预先声明的停止条件（例如新一轮不再产生符合标准的文献，或达到预先声明的轮次或预算）。看到结果后再改停止条件，必须记录。

这是方法的一部分，不是点缀。不要把 PRISMA 2020 或 SEGRESS 写成学位论文或选题轻量检索的强制流程。Kitchenham、Budgen、Brereton，《Evidence-Based Software Engineering and Systematic Reviews》，Chapman & Hall/CRC：已打开 Taylor & Francis / CRC 官方预览（版权页 © 2016 by Taylor & Francis Group, LLC，Version Date: 20151022；Keele 研究页写作 2015，Durham 书目写作 2016，引用时可同时披露，不必代选年代）。预览含前言、目录、术语表、第 1 章第 3–15 页、参考文献。本轮还打开了第 4、7、22 章的 Taylor & Francis 章节着陆页（元数据，不是全章正文）。第 22 章着陆页元数据中的 22.1 开篇，把该章称为 Kitchenham & Charters 2007 年指南的 “a revision”，并写它可作独立指南使用，同时与书中前面各章有意重叠并交叉引用。「修订」不是「废止」或「替代」。第 4、7、22 章正文，以及 PICO / PICOC 的定义与协议修订细则，仍未打开。因此仍不能宣称 2007 年实施指南已被替代，也不能仅凭 Usman、Ali、Wohlin，*A Quality Assessment Instrument for Systematic Literature Reviews in Software Engineering*（QAISER），*e-Informatica Software Engineering Journal* 2023，对该书的二手转述，或仅凭目录或着陆页，删除或改写 PICOC。前言仅把 Part III 称为 “the guidelines”；2007 年技术报告出现在该书已打开的参考文献中。不要把术语表里 “a sample size of at least 30 is required” 写入技能。不要使用着陆页的 `citation_firstpage` / `citation_lastpage` 代替书页码（这些元数据页码与已打开官方预览目录不一致）。SEGRESS 仍是二次研究的可选报告指南，不要把它写成 2015 年书第 22 章的替代阅读。雪球仍以已打开的 Wohlin 2014 为准。QAISER 是评估已完成系统综述的 15 项工具，不是撰写法令；不要把它的 15 项、AMSTAR 2「最近一次检索宜在 24 个月内」，或「可接受的雪球轮次」写成学位论文或选题轻量检索的强制规则。

## 5. 两轮筛查

先看题名/摘要，再看全文，套用预先声明的标准。记录各阶段数量。有一份简化的流程计数即可。不要把 PRISMA 2020 写成所有计算机应用技术论文或选题轻量检索的强制流程。

## 6. 抽出缺口矩阵，不要只堆摘要

列表示例（由协议自然导出）：问题/场景，方法族，假设，数据集或工艺节点，指标，**尚未做成的事**。学位论文里那句研究缺口（清华 2025-03 指南要求文献综述有「评」，并指出尚待解决的问题），应该是读这张矩阵的结果，而不是修辞。纳入文献的质量评价不能只用刊物级别代替：评价是否可信，分别对照 [实验设计](experiment-design.md) 中的通信仿真、器件验证与机器学习检查项。

## 选题用的轻量变体

正式开题或系统调研之前，用同一规程的瘦身版：

1. 草拟 PICOC。
2. 准备两到三组查询词族，在上述多库中检索。
3. 做第一张缺口矩阵。
4. 写明「什么样的结果才算一项贡献」，再进入创新点卡片。

不要把一次浏览式检索写成「系统综述」。

检索停在缺口矩阵之后，还要走独立研究步骤：批判性评价文献、形成可用合适对照验证的假说、区分探索与验证、按主张与证据是否相称衡量工作是否充足。见 [独立研究](independent-research.md)。对决定结论的关键文献做前后向追踪后，反向检索见 [诚信与证据](integrity-and-evidence.md)。
