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

为每个 PICOC 要素列出同义词与领域用语（IEEE 用语与中文用语、缩写与全称、器件名称与结构名称）。词族内部用 OR，词族之间用 AND。按对象选择具有互补覆盖的来源：例如 IEEE Xplore、ACM Digital Library、Web of Science / Scopus / EI；中文研究可用 CNKI、万方、原刊和高校机构库。器件或通信方向按相关性补 IET、Elsevier、IEICE 和中文刊源。具体数据库、语言与文献类型由研究问题、协议和访问条件决定，不要求每个题目都查同一组库。保存**确切查询式**、检索日期和访问限制；某库不可用时继续可查来源并注明覆盖缺口。

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
2. 根据核心问题、机制和失败条件准备查询词族，在相关且可用的来源中检索；数量随范围确定。
3. 做第一张缺口矩阵。
4. 写明「什么样的结果才算一项贡献」，再进入创新点卡片。

不要把一次浏览式检索写成「系统综述」。

检索停在缺口矩阵之后，还要走独立研究步骤：批判性评价文献、形成可用合适对照验证的假说、区分探索与验证、按主张与证据是否相称衡量工作是否充足。见 [独立研究](independent-research.md)。对决定结论的关键文献做前后向追踪后，反向检索见 [诚信与证据](integrity-and-evidence.md)。

## 来源身份、阅读范围与主张支持

元数据核验、内容阅读和论断支持分开记录。来源表保留真实题名、作者、年份、标识符、出版页/机构页、所读版本和已读页节；证据行再关联具体主张、短摘录或表/图定位、必要条件、能支持及不能支持的部分。复合句分别核证，例如“延迟降低且方差减小”需要各自的依据。只有题录或摘要时，不写成已检查完整方法。

| 状态 | 处理方式 |
|---|---|
| 题录相符、内容支持 | 写明实际核对的位置、版本与支持范围。 |
| 题录相符、全文暂不可得 | 保留可核部分；核心结论依赖未读内容时说明限制，另找可读证据。 |
| 内容可读但不支持当前主张 | 定位不符的对象、条件或含义，改引用关系或收窄主张。 |
| 题录/版本冲突 | 回原出版方、DOI 注册信息或机构存档核对，不凭相似标题合并。 |
| 本次未检索到或工具失败 | 保留查过的路径和失败原因，不据此断言虚构或撤稿。 |

中文 DOI 不应只查一个国际题录 API。先用 DOI 解析和原出版页核题名、作者与出处；必要时查相应注册机构（包括 ISTIC、CNKI 等提供的服务）和机构库。某接口不覆盖、返回不完整字段或访问被限制，表示该路径未完成核验。是否使用具体 API、端点、认证和限速按当次官方资料核实；本技能不预置未经验证的请求接口，也不绕过付费或访问限制。没有 DOI 的正式文献仍可由真实刊期、卷页及出版来源核验。

预印本和正式版分别记录，引用哪一版就核该版的表、页码和结论。更正、撤稿或更新信号要保留来源与核对日期，再查正式说明；不因索引标签就推断所有使用方式无效。重要经典工作不因年代久远自动排除，自引是否恰当取决于用途与覆盖，而非固定比例。

## 合并检索、导入与恢复

长调研按实际缺口分配主流路线、批评/失败、相邻领域、方法学和应用条件等视角；分工检索可并行或顺序完成。合并后检查遗漏视角、高频被引但未读的来源，以及排除材料暴露的新问题。按研究问题、机制与条件综合不同工作；结果冲突时先查指标、数据、预算和版本是否一致，无法对齐就并列说明，不强行平均。

导入本地 BibTeX、RIS、JSON 或文献文件夹时，保留来源文件和原条目 ID、重复/合并映射、拒绝/解析失败清单。去重不能静默丢失不同版本。已有 Zotero/Obsidian 导出可作为输入；直接连接软件或外部服务只在实际需要时使用，缺连接器仍可处理本地导出。

可用 [`scripts/import_bibliography.py`](../scripts/import_bibliography.py) 导入明确选定的本地题录文件；文件夹先列出并挑选实际题录，它不递归扫描附件。跨平台命令为 `python scripts/import_bibliography.py "library.bib" "export.ris" --output "bibliography-import.json"`（Linux 按环境使用 `python3`）。输出必须是新文件。默认严格 UTF-8/UTF-8 BOM，旧中文文件可显式加 `--encoding gb18030`；不猜编码。返回码 0 表示已按支持范围完整导入，1 表示拒绝项、警告或重复键待复核，2 表示输入/输出错误。检查结果中的原条目、来源文件哈希、位置、拒绝日志与重复组后再整理引用。静态 BibTeX 支持花括号/引号字面值和数字；宏、字符串拼接及畸形项显式拒绝。JSON 支持 CSL 列表或 Better BibTeX 的 `items` 列表；保留解析对象与来源身份，不承诺逐字还原 JSON。此工具不查网络、不判断文献真假、不证明引用支持论断，也不自动修改稿件。

核心主张较多时，可用[项目证据记录](evidence-ledger.md)登记已查项目和未查范围。报告“已核查 X/Y”须说明 Y 是登记主张、引文还是全文自动提取项；登记项全部通过不意味着论文所有事实已认证。外部模型复核不得因机器上存在密钥就自动上传稿件；同宿主独立复核可按任务选择，其他供应商需要相应材料范围和成本授权。

本地筛选可在同一命令后加 `--query "NoC" --field title --author "Wang" --year-from 2022 --year-to 2026`，或用 `--year 2024` 指定单年。关键词、作者按忽略大小写的字面子串匹配，各条件取交集；不做模糊检索、TeX 重音/宏展开或作者身份归并。`--field` 是原字段或标签名称（如 BibTeX 的 `title`、RIS 的 `TI`），不填时查所有字段值；作者仅查实际作者字段及 BBT 中标为 author 的 creators。年份按 CSL `issued.date-parts` 或 `year/PY/Y1/date` 的首个四位年份提取，无法解析则明确排除为 year_unavailable，不推测日期。结果另列匹配 ID、排除原因和提取年份依据，全部原条目仍保留在 entries；零命中写 NO_MATCHES，空字符串筛选或反向年份区间报输入错误。该筛选只面向已成功导入项，拒绝项仍要单独处理。

系统综述的独立筛选、排除计数与元分析入口见[专项指南](benchmark-and-synthesis.md)。持续监测先交查询词、来源、更新判据与记录位置；只有用户明确要求定期跟踪时，才确定频率、期限和通知方式后使用可用的任务工具，不默认建立后台服务。
