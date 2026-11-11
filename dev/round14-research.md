# ThesisForge 第 14 轮独立调研报告

本轮是「新五轮独立研究 / 实验 / 数据」计划的第 5 轮，也是该计划的最后一轮。调研方法遵循本地已核对的 research-to-report-and-briefing **v3.3.0**（技能入口 `/workspace/research-to-report-and-briefing/SKILL.md`，版本字段与 CHANGELOG、README 一致；重点依据 `references/research-and-evidence.md`）。先形成研究问题与证据边界，优先原始依据，读足关键上下文，核对对象、单位、版本与比较条件，主动反向检索，观察与建议分开，缺口不填成事实。本轮不制作 PPT。

观察、原文摘录、含义和建议分开写。搜索摘要不能单独支撑准备写入技能的句子。打不开的来源标为 FAIL，不用记忆填空。前几轮报告只作背景，本轮重新检索并打开原文，不把上轮摘要当成证据。已有来源在 `round10–13-sources/` 可复用，不必重复拷贝。已结算事项（学位法硕士限度、北大两句并存与第一人称归属、清华固定行距 20 磅与篇眉、TCOM/ComSoc 无 30%、PSPB 8.1.7.F、Heiser 范围、Pawlikowski 不是 BER 事件数且不被 Hamkins 替换、T-ED generally、软件学报字段未重核、0809 文献比例不得写成默认、RBR/Unbot 默示但非硬依赖、0812 与 0854 分标互不替代、2015 年领域汇编不得覆盖现行 0854 类别页或试行版类别篇、试行版不是「学位〔〕」号颁布件也不是学位法实施细则或 2025 年强制国标、预注册可选且不能补弱理论但不撤探索/验证诚实区分、不写默认 p/k/最小 n/BER 事件数（含 4/16/400/4/w）/5% 缺失阈值/术语表 at least 30/JESD51-2A 的 15–30°C 或 ±3°C 作为通用默认；不宣称 2007 已被替代，不改写 PICOC）本轮不推翻、不顺手改写。

本轮未修改 `/workspace/ThesisForge/` 下除 `dev/` 报告副本以外的运行时技能文件，未同步用户桌面，未联系审查 bot。

## 1. 研究边界与问题

默认学科仍是计算机应用技术，兼顾通信与半导体电子。诚信约束不变。侧重点是加强独立研究、实验设计、数据处理与分析，以支撑论文工作量与创新性成果。不重做已结算的格式/版式调研，也不重做已结算的逻辑/创新点位置/一条主线调研，除非原文与现行技能直接冲突且本轮打开了原文。

- **Q1.** 能否合法取得 Kitchenham、Budgen、Brereton《Evidence-Based Software Engineering and Systematic Reviews》（Chapman & Hall/CRC，版权页 © 2016，Version Date: 20151022；常引作 2015）第 4、7、22 章**正文**（作者副本、图书馆或出版社样章；不以不清楚授权的课程盗版为唯一依据），再核对：PICO/PICOC 是否被改写、协议修订如何写、“revision of … 2007” 在后文中的具体含义，以及与 SEGRESS 的关系。未打开全文则维持第 13 版限度：不改 PICOC，不宣称 2007 已被替代，不用着陆页 citation 页码，不把术语表 “at least 30” 写入技能。
- **Q2.** 能否取得 Jeruchim 1984《Techniques for Estimating the Bit Error Rate in the Simulation of Digital Communication Systems》（*IEEE JSAC* 2(1):153–170，DOI 10.1109/JSAC.1984.1146031）合法全文。Hamkins 2015 不能代替它。打不开就维持「不写默认事件数」。不要用讲座、摘要或记忆填公式。
- **Q3.** 能否打开 JJF 1059.1-2012，或可公开的 IEC / 其他国内半导体测量规程全文。官方公开系统若仍受插件限制或 404，记为 FAIL。未打开就继续不写行业公式和最小 n，不把 15–30°C 或 ±3°C 写成通用默认，不覆盖已编码的 GUM / TN 1297 / 片上射频 / JESD51-2A（静风箱 θJA）限度。
- **Q4.** 能否找到更直接的贡献消融通论：正式发表、范围不限于单一架构，同时讨论删除后重调、因素不独立与消融表多重比较的方法论文。不用 Meyes 2019，不把 Huang 注意力头协议写成通例，不把 Ulmer 2022 升为消融通论或指定 Bonferroni 为默认。已编码的 NIST OFAT / Melis 未重调 / Huang 限度在没有更贴切通论之前保持。
- **Q5.** 直接打开 `https://www.acge.org.cn/encyclopediaFront/enterEncyclopediaIndex` 中的 0812、0854 官方条目（或学会提供的可核对官方正文），与江西农业大学转写汇编对读；并检索是否存在国务院学位委员会带「学位〔〕」号的新汇编。不要用学校授予标准填空，不要用 0812 与 0854 互代，不要把汇编里未对读的《工程类硕士专业学位基本要求》与工程教指委〔2024〕20 号互称为同一文件。

若独立检索中发现与本轮主题直接相关、且第 13 版尚未覆盖的其他有益方法，可以列入，但必须打开原文并标等级。不把范围扩到格式或已结算的法律/学校逻辑。

## 2. 对第 13 版相关运行时文件的核对

通读了现行第 13 版中与本轮焦点相关的文件。限度句大体还在，没有发现需要本轮「先删后补」的过满；本轮新证据只应在已打开范围内补充，不得假装上一轮残留已经结论。

- **literature-search.md：** 仍以 Kitchenham 与 Charters 2007 年为实施规程压缩来源；SEGRESS 仍只是二次研究的可选报告指南，不是宣布 2007 已被替代。2015 年书的限度句已写明：官方预览（前言、目录、术语表、第 1 章第 3–15 页、参考文献）已打开，第 4、7、22 章只有 Taylor & Francis 章节着陆页，第 22 章着陆页 22.1 开篇自称是 2007 年指南的 “a revision”，「修订」不是「废止」或「替代」；PICO/PICOC 定义与协议修订细则仍未打开；不要用着陆页 `citation_firstpage` / `citation_lastpage`，不要写入术语表 “at least 30”。本轮再次独立打开官方预览与第 22 章着陆页，结论与上述限度一致，**正文仍未打开，不改 PICOC，不宣称替代**。
- **experiment-design.md：** Hamkins 相依性警告已写入；Jeruchim 仍标明未取得合法全文，通信规程不写入数值 BER / 错误事件规则；Pawlikowski 不被 Hamkins 替换。消融规程仍以 NIST OFAT、Melis 未重调披露、Huang 预印本限度和 ASA / Simmons 披露（不指定默认校正）为界，没有更一般通论。本轮仍未打开 Jeruchim 全文，也未找到可编码的更一般消融通论。
- **data-analysis.md：** GUM、TN 1297 与 JESD51-2A（仅静风箱 θJA，且不把 15–30°C 或 ±3°C 写成通用默认）已编码；JJF 1059.1-2012 与 IEC 器件测量标准仍不得引用其公式或编造最小 n。本轮打开了官方目录记录和一份 FileOpen 加密的官方下载件，**仍不能阅读正文**，因此不覆盖已编码限度。
- **topic-and-contribution.md：** 2013/2014 年 0812 书页与试行版转写汇编并列；0854 现行教指委网页与试行版类别篇并列；官方百科条目页此前未打开；2015 年领域汇编不得覆盖现行页或试行版。本轮已经打开学会官方 0812、0854 条目正文，建议把官方条目升为试行版的直接依据，高校转写改为核对副本，但**仍未发现「学位〔〕」号颁布件**，也不用官方条目去替代 0812/0854 分标或覆盖现行教指委网页。

## 3. 已打开来源与等级

等级约定：E 表示已打开原文、可引用；S 表示有出处但须写明限度（出版社章节着陆页元数据而非全书、高校转写、转载公告、预印本、课程副本、仅目录/题录、加密而不可提取的官方 PDF 等）；U/FAIL 表示未取得可核对正文，不得编码为规则。搜索命中或摘要不等于已精读。获取时间均为 2026-11-11 Asia/Shanghai（CST）。新来源保存在 `/workspace/thesisforge-research/round14-sources/`。

### 3.1 Q1 Kitchenham 2015 年书第 4、7、22 章

| ID | 来源 | 等级 | 本轮核对 |
| --- | --- | --- | --- |
| S1 | Taylor & Francis `googlepdf` 官方预览 PDF，DOI 10.1201/b19467。URL `https://api.taylorfrancis.com/content/books/mono/download?identifierName=doi&identifierValue=10.1201%2Fb19467&type=googlepdf`。75 页，MD5 `2ea54fb0958dccb9fb7d9bd973b54aa4`（与第 12 轮已保存文件字节相同，本轮独立重下）。抽取文本 MD5 `c4fd49f4362bda8ecc5b5feb771441d7`。 | **S（出版社官方预览，不是全书，也不含第 4、7、22 章正文）** | 实际页为：书名与版权页（© 2016，Version Date: 20151022）、目录、图表目录、前言、术语表、Part I 扉页、第 1 章（约书页 3 起）以及书末参考文献。全文检索 **PICO / PICOC 为 0**。「Planning a Systematic Review」「Assessing Study Quality」「Systematic Review and Mapping Study Procedures」只出现在目录。「Chapter 4」仅在第 1 章正文中作为前瞻交叉引用出现，并不是第 4 章本身。术语表仍有 “a sample size of at least 30 is required”，不得写入技能。 |
| S2 | pageplace.de 预览 PDF。URL `https://api.pageplace.de/preview/DT0400.9781482228663_A37870126/preview-9781482228663_A37870126.pdf`。43 页，MD5 `7c77ab12dd33a0e89271ed1a67ce797c`。Rakuten Kobo / pdfTeX 生成。 | **S（更短的合法预览）** | 覆盖范围止于第 1 章约第 8 页，比 T&F `googlepdf` 更短，同样没有第 4、7、22 章正文，也没有 PICO/PICOC。 |
| S3 | Taylor & Francis 章节着陆页「Planning a Systematic Review」，DOI 10.1201/b19467-10。HTML MD5 `e6920c7104ae80261948f9447ec01192`（与第 13 轮同一页一致）。 | **S（着陆页元数据，不是第 4 章正文）** | `citation_abstract` 主要是该章目录。全文检索 PICO/PICOC 为 0。`citation_firstpage`/`lastpage` 作 73–88，与已打开官方预览目录中第 4 章始于第 39 页不一致，不得代替书页码。 |
| S4 | Taylor & Francis 章节着陆页「Assessing Study Quality」，DOI 10.1201/b19467-13。HTML MD5 `fac5edad45c50bb9f3b1f52fe78fee32`。 | **S（着陆页元数据，不是第 7 章正文）** | `citation_abstract` 只有开篇一句，未见 PICO/PICOC、协议修订细则或对 2007 年指南的定位句。`citation_firstpage`/`lastpage` 作 113–126，同样不得当作书页码。 |
| S5 | Taylor & Francis 章节着陆页「Systematic Review and Mapping Study Procedures」，DOI 10.1201/b19467-31。URL `https://www.taylorfrancis.com/chapters/mono/10.1201/b19467-31/systematic-review-mapping-study-procedures-barbara-ann-kitchenham-david-budgen-pearl-brereton`。HTML MD5 `cc3616b6d2af823183a96ce65baf1592`。向 `chapterpdf` 接口请求同一 DOI，返回的仍是该着陆页 HTML（相同 MD5），不是 PDF。 | **S（着陆页元数据；其中含 22.1 开篇一段，仍不是全章正文）** | `citation_abstract` 先是第 22 章后半目录（约 22.3–22.11），随后出现 22.1 开篇，把该章称为对 Kitchenham & Charters 2007 的 “revision”，并写可作独立指南使用、同时与前面各章有意重叠并交叉引用。未见 PICO/PICOC 定义或协议修订细则。`citation_firstpage`/`lastpage` 作 327–390，与官方预览目录中第 22 章始于约第 291/293 页不一致，不得改用。另：本轮曾误取 DOI 10.1201/b19467-28，该着陆页标题实为 “Data Mining Studies”，**不是**第 22 章。 |
| FAIL-IA | Internet Archive 高级检索 API，查询该书题名与 Kitchenham。JSON MD5 `89ce02d91d0327cb4d9a53667985a660`。 | **FAIL** | `numFound: 0`，`docs: []`。本轮未取得可出借或可下载的合法全书。Durham worktribe 书目页 HTTP 403，不是全文。 |

**仍未打开的正文：** 第 4 章（规划 / 研究问题 / 协议）、第 7 章（研究质量评价）、第 22 章（Part III 指南程序）的完整正文，以及任何直接定义或改写 PICO/PICOC、详细规定协议修订程序、或在 22.1 之后展开 “revision” 含义的段落。因此仍不得仅凭目录、QAISER 或着陆页元数据改写 PICOC，也不得宣称 2007 年实施指南「已被替代」。SEGRESS 仍只是二次研究的报告指南，本轮未把它写成 2015 年书第 22 章的替代阅读。

### 3.2 Q2 Jeruchim 1984

| ID | 来源 | 等级 | 本轮核对 |
| --- | --- | --- | --- |
| FAIL-J | Jeruchim，*Techniques for Estimating the Bit Error Rate in the Simulation of Digital Communication Systems*，*IEEE JSAC* 2(1):153–170，1984，DOI 10.1109/JSAC.1984.1146031。本轮打开：OpenAlex 作品记录（JSON MD5 `93963a1f314bd3514cb38b596c74049f`）；Semantic Scholar Graph API（JSON MD5 `3248d9bcab6854fccd0e1692c16bb71e`）；Crossref（JSON MD5 `e72afec8ef7e2a43cacdd3773d502bc5`）；IEEE 条目页与 stamp（HTTP 202，空或非 PDF 体）；Crossref 给出的 ielx6 相似检测路径（HTTP 500，空体）；CORE 检索页（HTTP 403）。Unpaywall 因接口要求使用调用者本人邮箱返回 422，未作为开放获取证据。 | **FAIL** | OpenAlex：`is_oa: false`，`oa_status: "closed"`，`oa_url: null`，`any_repository_has_fulltext: false`。S2：`isOpenAccess: false`，`openAccessPdf.status: "CLOSED"`，`url` 为空。Crossref 版权许可指向 IEEE 许可页，不是开放许可。未发现可核对的作者副本、机构库或政府公开全文。不得用记忆、讲座、Hamkins 或他文中的「100 个错误」一类转述填入 Jeruchim 的事件数或公式。 |

### 3.3 Q3 JJF / IEC / 国内半导体测量规程

| ID | 来源 | 等级 | 本轮核对 |
| --- | --- | --- | --- |
| E1 | 「国家计量技术规范全文公开系统」现行站点（本轮首页、高级检索、帮助中心均可打开；旧路径 `/resmea/standard/JJF%201059.1-2012/` 仍 404）。官方检索 API `https://jjg.spc.org.cn/resmea/api/standard/search/page?keyword=JJF%201059.1-2012&pageNum=1&pageSize=10`（与 `advanced/page?code=` 返回同一条；JSON MD5 `46591ab52f4692fc1870c222391a7926`）及详情页 `https://jjg.spc.org.cn/resmea/standard/detail.html?standno=JJF%201059.1-2012&pageindex=1&rows=10`（HTML MD5 `7aa426332dab6c81a524309794d9da26`）。帮助中心 `https://jjg.spc.org.cn/resmea/system/instruction.html`。 | **E（仅目录 / 详情元数据与系统说明，不是规范正文）** | 目录记录：id 15751，规范编号 JJF 1059.1-2012，中文名称「测量不确定度评定与表示」，类型「其他计量技术规范」，状态「现行」，发布 2012-12-03，实施 2013-06-03，替代 JJF 1059-1999。详情页还给出主要起草人（叶德培、赵峰、施昌彦、原遵东、沙定国、周桃庚、陈红）、起草单位与发布部门（国家质量监督检验检疫总局）。页面配置 `hasPdf: 1`。帮助中心写明：下载阅读需安装 Adobe Reader 以及「阅读插件（FileOpen 客户端）」。这些元数据可以说明该规范存在且现行，**不能**据以写入公式或最小 n。 |
| S6 | 同一官方系统的下载件 `https://jjg.spc.org.cn/resmea/standard/downPdf?stdno=JJF%201059.1-2012`。HTTP 200，`Content-Type: application/octet-stream`，1 112 326 字节，MD5 `d8bbbdba8c8fbe858294047f5854c555`。文件头为 `%PDF-1.5`，体内有 `Encrypt` 与安全处理器名 `FOPN_foweb`。`pdfinfo` 报错：`Couldn't find the 'FOPN_foweb' security handler`。已放在 `round14-sources/fail/`。 | **S / 实质 FAIL（官方文件已下载，但 FileOpen 加密，无法提取或阅读正文）** | 证实官方全文以加密 PDF 提供，本环境无法打开。不得绕过插件去「恢复」正文，也不得改用来源不明的「免费标准」站点。因此 JJF 1059.1-2012 **正文仍视为未打开**。 |
| E2 | 国家标准全文公开系统对 GB/T 27418-2017《测量不确定度评定和表示》的官方条目。URL `https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=4BAEA7D58DD78FD31710D69E0F9CDCF7`（`/bzgk/gb/newGbInfo` 同页，HTML MD5 `240fd4d00cc5fd8d518d511fb38d011f`）；全国标准信息公共服务平台 `https://std.samr.gov.cn/gb/search/gbDetailed?id=71F772D8230BD3A7E05397BE0A0AB82A`。 | **E（官方条目关于「不提供全文」的说明，不是标准正文）** | SAMR 页写明：该标准采用了 ISO、IEC 等国际国外组织的标准，「由于涉及版权保护问题，本系统不提供文本阅读服务」。std.samr 页写明本标准修改采用 ISO/IEC Guide 98-3:2008。因此不能把 GB/T 27418-2017 当成已打开的 JJF 替代全文，也不能用它覆盖已编码的 BIPM GUM。 |
| S7 | 国家标准馆 / 国家数字标准馆 JJF 1059.1-2012 条目 `https://ndls.cnis.ac.cn/standard/detail/5f8eb3f61fc08aa034745ddd36dee19e`。HTML MD5 `f0b8e3b2ca5556e307087ce3567cce7e`。 | **S（条目与适用范围摘述，购买入口，不是可核对全文）** | 页内有适用范围与采用关系的介绍，并导向中国标准服务网「购买正版」。摘述不足以支撑写入公式或最小 n。 |

**FAIL / 未打开的正文：** JJF 1059.1-2012 规范全文、IEC 器件测量标准全文，以及其他未打开的 JEDEC 程序（如 JESD51-1）。不得写未打开标准中的公式或最小 n，不把 15–30°C 或 ±3°C 写成通用默认。

### 3.4 Q4 贡献消融通论

| ID | 来源 | 等级 | 本轮核对 |
| --- | --- | --- | --- |
| E3 | Abramovich 与 Chechik，*AblationBench: Evaluating Automated Planning of Ablations in Empirical AI Research*，*Findings of the Association for Computational Linguistics: EMNLP 2026*，pp. 30612–30651，2026-10-24–29。ACL Anthology `https://aclanthology.org/2026.findings-emnlp.1436/` 与官方 PDF（MD5 `a7c2184827f67f4a4914ce5ca6eb54b3`）。 | **E（已打开正式发表本，但题目不是贡献消融通论）** | 这是评价语言模型智能体「规划消融实验」能力的基准，含 AuthorAblation 与 ReviewerAblation 两项任务。开篇把消融定义为把方法拆成部件并评估贡献，并引用了 Meyes 等 2019。正文关注的是自动规划、评测框架与模型表现，**不是**同时讨论删除后重调、因素不独立和消融表多重比较的方法通论。不得把它升为技能中的消融通论，也不得借其引用把 Meyes 2019 写回技能。 |

本轮还检索了 SIGSOFT Empirical Standards、Raschka 的模型选择综述等相邻文献，但未打开任何一篇同时满足「正式发表、范围不限于单一架构、并且同时讨论删除后重调、因素不独立与消融表多重比较」的方法论文。已编码的 NIST OFAT / Melis 未重调 / Huang 限度保持不变。

### 3.5 Q5 学会百科官方条目与「学位〔〕」号颁布件

| ID | 来源 | 等级 | 本轮核对 |
| --- | --- | --- | --- |
| E4 | 中国学位与研究生教育学会「研教百科」索引内容页 `https://www.acge.org.cn/encyclopediaFront/enterEncyclopediaIndexContent`（空关键词返回全部学科树，HTML MD5 `3c8bba3d1067ed94a32c97c319ddba8f`；`keyWord=0812` / `0854` 返回过滤后的同一前言与菜单）。官方外壳 `enterEncyclopediaIndex` HTML MD5 `884cef87f1296b388725b5cef65e4074`（与第 13 轮外壳相同）。 | **E（官方前言与条目目录，还不是各学科正文）** | 页内前言与已编码的试行版公布说明同向：由国务院学位委员会第八届学科评议组、全国专业学位研究生教育指导委员会编修，配合《研究生教育学科专业目录（2022年）》实施，目的是参考依据，本次公布为试行版，内容将调整完善。菜单给出官方 `subjectId`：0812 为 `402a8137577ab56fjg5774d92ba70077`，0854 为 `402a8137577ab56fjg5774d92ba70106`。空关键词页可列出 167 个四位代码条目。页面本身**没有**「学位〔〕」号。 |
| E5 | 学会官方 0812 计算机科学与技术条目。数据容器 `enterEncyclopediaSubjectDataContainerIndex?subjectId=402a8137577ab56fjg5774d92ba70077&…`（HTML MD5 `97b96f0836c89cf530edd3300cbcce37`）给出中文名称、英文名称（Computer Science and Technology）和编写成员「计算机科学与技术学科评议组」。正文不在该容器的占位句里，而在两个标签接口：简介 `https://www.acge.org.cn/encyclopediaFront/enterSubjectIntro?subjectId=402a8137577ab56fjg5774d92ba70077&type=encyclopedia_subject_intro`（HTML MD5 `f42459de5e7c9140731123e38312df3c`，抽取文本 MD5 `18d2126d3e68cb49cb2b764e517d11b8`）；学位基本要求 `https://www.acge.org.cn/encyclopediaFront/enterDegreeStandard?subjectId=402a8137577ab56fjg5774d92ba70077&type=encyclopedia_degree_standard`（HTML MD5 `e02e916277d435f90b0585a2d3fc6e7d`，抽取文本 MD5 `1df71cf34aad89b7c59a0b51e5d68882`）。缺少 `type` 参数时接口返回 HTTP 500。 | **E（学会官方条目正文）** | 容器里的「简介暂未维护……」「学位基本要求暂未维护……」只是标签页加载前的占位，**不得写成官方条目尚未维护**。实际标签接口返回了可核对的一级学科简介与硕、博士学位基本要求全文。页面没有「学位〔〕」号，也不是学位法实施细则或某校授予标准。 |
| E6 | 学会官方 0854 电子信息条目。数据容器 `subjectId=402a8137577ab56fjg5774d92ba70106`（HTML MD5 `b68708aa3aa062a596e08ddc8cd16019`）给出中文名称、英文名称（Electronic and Information Engineering）和编写成员「全国工程专业学位研究生教育指导委员会」。简介 `enterSubjectIntro?…&type=encyclopedia_subject_intro`（HTML MD5 `8b0a846bbb60d037a2b79472879e89a9`，文本 MD5 `fa00754da65adb4c7394764b42f58be5`）；学位基本要求 `enterDegreeStandard?…&type=encyclopedia_degree_standard`（HTML MD5 `b96c99f63a7ec288613c7bc93d93afac`，文本 MD5 `669e90116fbe3f12fdf60142cd11bce0`）。 | **E（学会官方条目正文）** | 同样，占位句不能当成「未维护」。官方正文可与现行教指委网页、江西农业大学转写汇编并列核对。页面没有「学位〔〕」号。五种论文形式后写「详见《工程类硕士专业学位基本要求》」，本轮仍未对读该被指向文件与工程教指委〔2024〕20 号是否为同一件，不得互称替代。 |
| S8 | 江西农业大学转写汇编中的 0812、0854 篇（第 13 轮已保存，本轮复用，不重复拷贝）。 | **S（高校 Word 转写，现可作为官方条目的核对副本，不再当作唯一正文来源）** | 将官方条目各段作去空白、统一标点后的规范化比对：0812 学位基本要求 41 个较长段落中，35 段可完整回找到转写本，其余 6 段为部分匹配（转写有换行切断），没有找不到的段落；0854 简介与学位基本要求 52 段完整回找、7 段部分匹配，同样没有缺失段。关键延续句（「假造」、硕士「研究开发或实验工作充足」、对照实验假说、五类创造性成果、实践半年与免修、选题、五种形式、「工作量饱满」等）在官方页与转写本中同向出现。 |
| S9 | 西安交通大学研究生院网页，标题作「教育部发布《研究生教育学科专业简介及其学位基本要求（试行版）》」。URL `https://gs.xjtu.edu.cn/info/1189/10787.htm`，HTML MD5 `f736bc639c4edab346725abd37e0abb0`。安徽中医药大学、南京中医药大学等转载页（本轮已打开）正文与官方前言同向，并指向学会百科入口。本轮重下的 `https://www.acge.org.cn/acge/doc/2024/1-24/6cda4133975c4ca0b07c4f8bd1459ca6.pdf`（MD5 `f3d7a738bff424651cbdb9f212f1afed`）是梁传杰讨论 2022 年目录调整的期刊文章（DOI 10.16750/j.adge.2023.02.001），不是试行版基本要求的颁布件。 | **S（学校转载或期刊论文，不是「学位〔〕」号颁布件）** | 西交大**标题**写「教育部发布」，正文却仍是试行版前言的转写，并出现「研究生教育学考专业目录（2022年））」一类笔误；正文给出「2024年1月22日」，但没有「学位〔〕」或教育部发文号。不得用该标题把试行版写成教育部或国务院学位委员会的颁布件。安徽中医药大学、南京中医药大学页正确指向学会入口，同样没有「学位〔〕」号。 |

**仍未打开 / 未找到：** 带「学位〔〕」号的国务院学位委员会颁布件；《工程类硕士专业学位基本要求》与工程教指委〔2024〕20 号的原文对读。学校授予标准仍不得填空。

## 4. 按问题组织的发现

### 4.1 Q1 第 4、7、22 章正文仍未打开；官方预览与着陆页只再次确认既有限度

**摘录与定位。** 第 22 章着陆页 `citation_abstract` 末段（本轮独立打开的 DOI 10.1201/b19467-31 页）写：

> 22.1 Introduction This rather long chapter is a revision of our previous guidelines for systematic reviews for software engineering research (Kitchenham & Charters 2007). There are deliberate overlaps with information provided in the preceding chapters of this book, so that this chapter can be used as a self-standing set of guidelines. However, we do cross-reference sections of the book where more detailed information about specific topics can be found.

官方预览术语表（T&F `googlepdf` 抽文本）在 “sampling” 附近写：

> As a rule of thumb, if any statistical analysis is to be employed, even at the level of calculating means and averages, a sample size of at least 30 is required.

**含义。** 「revision」出现在 22.1 开篇元数据中，意思是该章把自己写成对 2007 年指南的修订，并可独立使用，同时与书中前面各章有意重叠并交叉引用。这仍然只是开篇一句，不是全章对 2007 年文本逐条修订的说明，也不是「废止」或「已被替代」。PICO/PICOC 在已打开的官方预览和三章着陆页中均未出现，因此不能判断 2015 年书是否改写了 PICOC，也不能改写技能中的 PICOC。协议修订的细则仍只出现在目录标题（如 4.4 Developing the protocol、4.5 Validating the protocol、22.4.3–22.4.4），没有正文。术语表 “at least 30” 仍是经验口诀，不得写入技能。着陆页 citation 页码与书页目录不一致，不得改用。

**不要写成什么。** 不要宣称已经打开第 4、7、22 章正文；不要改写 PICOC；不要宣称 2007 年实施指南已被替代；不要把 SEGRESS 写成第 22 章的替代阅读；不要写入 “at least 30”；不要使用 73–88、113–126、327–390 这组着陆页页码。

### 4.2 Q2 Jeruchim 1984 仍 FAIL，维持「不写默认事件数」

**摘录与定位。** OpenAlex 对该 DOI 的开放获取字段为 `is_oa: false`，`oa_status: "closed"`，`any_repository_has_fulltext: false`。Semantic Scholar 为 `isOpenAccess: false`，`openAccessPdf.status: "CLOSED"`。IEEE stamp 仍为 HTTP 202 且未得到 PDF。

**含义。** 书目身份可核对，合法全文仍不可得。Hamkins 2015 不能填补这一缺口。

**不要写成什么。** 不要写入默认误码事件数或数值置信区间公式（包括 4、16、400、4/w 等）；不要用讲座、摘要或记忆冒充 Jeruchim 1984。

### 4.3 Q3 官方系统现已给出 JJF 1059.1-2012 的现行目录与加密下载件，正文仍不可读

**摘录与定位。** 官方检索 API 返回：

> `"code":"JJF 1059.1-2012","stdType":"其他计量技术规范","title":"测量不确定度评定与表示","status":"现行","publishDate":"2012-12-03","implementDate":"2013-06-03"`

详情页可见「替代以下规范：JJF 1059-1999」，以及起草人、起草单位与发布部门。帮助中心写：「下载阅读需要安装两个应用程序」「1. PDF阅读器（ Adobe Reader ）」「2. 阅读插件（ FileOpen客户端 ）」。本轮下载的官方 PDF 能识别为 `%PDF-1.5`，但含 `FOPN_foweb` 加密，无法提取正文。

SAMR 对 GB/T 27418-2017 的官方条目写：

> 该标准采用了ISO、IEC等国际国外组织的标准，由于涉及版权保护问题，本系统不提供文本阅读服务。

**含义。** 与旧版 404 路径不同，现行公开系统可以检索到该规范的目录身份，也可以下载到官方加密文件，但这仍不等于已经打开可引用的规范正文。GB/T 27418-2017 在国家标准全文公开系统上因采用 ISO/IEC Guide 98-3 而被明确不提供阅读，不能拿来代替 JJF 或已打开的 BIPM GUM。

**不要写成什么。** 不要引用 JJF 或未打开 IEC 中的公式或最小 n；不要把 15–30°C 或 ±3°C 写成通用默认；不要覆盖 GUM / TN 1297 / 片上射频 / JESD51-2A 限度；不要把「官方可以下载」写成「正文已打开」；不要用来源不明的解密件或商业「免费标准」站补空。

### 4.4 Q4 仍未找到更直接的贡献消融通论

**摘录与定位。** AblationBench 摘要开篇：

> Language model agents are increasingly used to automate scientific research, yet evaluating their scientific contributions remains a challenge. A key mechanism to obtain such insights is through ablation experiments.

随后把消融过程分成「规划」与「执行」，并声明本文关注规划、而不是代码执行；数据集用于评价智能体能否提出与原论文或审稿意见相符的消融计划。

**含义。** 这是一篇正式发表的基准论文，可以说明「消融常被用来评估部件贡献」，但它既不是贡献主张式消融的方法通论，也不讨论删除后重调、因素不独立或消融表多重比较的统计处理。它还引用了本技能明确不用的 Meyes 2019。因此只作为本轮已读、不编码的对照文献。

**不要写成什么。** 不要把 AblationBench 升为消融通论；不要写回 Meyes 2019；不要把 Huang 注意力头协议写成通例；不要指定 Bonferroni 为默认；在没有更贴切通论之前，保持 NIST OFAT、Melis 未重调披露和已有多重比较披露原则。

### 4.5 Q5 学会官方 0812、0854 条目正文已经打开；仍未发现「学位〔〕」号颁布件

**摘录与定位。** 官方索引内容页前言：

> 为深入贯彻落实党的二十大精神，配合《研究生教育学科专业目录（2022年）》实施，国务院学位委员会第八届学科评议组 、全国专业学位研究生教育指导委员会在《授予博士硕士学位和培养研究生的学科专业简介》《学位授予和人才培养一级学科简介》《一级学科博士、硕士学位基本要求》《专业学位类别（领域）博士、硕士学位基本要求》基础上，根据经济社会发展变化和知识体系更新演化，编修了《研究生教育学科专业简介及其学位基本要求（试行版）》。主要目的是为各级教育主管部门和学位授予单位开展学科专业管理、规范研究生培养、加强学科专业建设、制订培养方案、开展学位授予等提供参考依据，为社会各界了解我国学科专业设置、监督研究生培养质量提供渠道。本次公布的《研究生教育学科专业简介及其学位基本要求》为试行版，有关内容将根据各学科专业建设、发展进程不断调整完善。

官方 0812 学位基本要求中的延续句与新写出的表述（摘自 `enterDegreeStandard` 抽取文本）包括：

> 恪守学术道德与规范，不以任何方式剽窃他人成果，不篡改、假造、选择性使用实验和观测数据。

> （2）学位论文具有新的见解，基本观点正确，论据充分，数据可靠，研究开发或实验工作充足；

> 能鉴别有意义的科学问题、提出可通过合适的对照实验进行验证的科学假说

> 学术创新包含三个方面的内容，一是原有知识的创新性运用，即用已有知识解决新问题；二是用新知识解决已有的科学问题并取得显而易见的成果，即用新知识解决老问题；三是运用原创性的科学思维或创新性的研究方法创立新理论、新技术、新系统，解决新问题……

> 本学科博士学位论文的相关研究工作应着眼于面向世界科技前沿、面向经济主战场、面向国家重大需求、面向人民生命健康

> 博士学位论文应在学科或专门技术上取得了创造性成果。凡属下列情况之一，可认为属于创造性成果：（1）发现计算机科学与技术领域的新问题，并给出具有参考价值的解决方案；（2）发现有价值的新现象、新规律，提出新的合理假说、观点、理论，证明前人提出的假说等；（3）对前人提出的理论、技术及方法有重要改进或革新，或者在计算机系统及算法设计、实验技术、交叉学科研究上有重要的创造或革新；（4）提出具有一定科学水平的新方法和新工艺，在生产中有望获得较大的经济效益；（5）创造性地运用现有知识，解决前人未曾解决过的科学技术、工程技术或社会科学等方面的关键问题。

知识结构中，「计算机网络与安全」「人工智能」出现在硕士、博士应掌握的基本知识列举里。

官方 0854 学位基本要求写：

> 具有2年及以上企业工作经历的全日制工程类硕士专业学位研究生可以申请免修专业实践，不具有2年企业工作经历的工程类硕士专业学位研究生专业实践时间应不少于半年。

> 形式可为专题研究类论文、调研报告、案例分析报告、产品设计（作品创作）报告或方案设计报告等。……五种形式的学位论文基本要求及评价指标详见《工程类硕士专业学位基本要求》。

> 工作量饱满，应在导师组指导下独立完成；

> 选题直接来源于生产实际或具有明确的工程背景

简介中再次出现工程教指委〔2021〕1 号与十二个领域方向，并有「截至2022年底」的培养单位数据。博士实践「累计时间不少于1年」。官方页面把「工作量饱满」写成定性要求，没有页数或实验组数。

**含义。** 试行版 0812、0854 现在可以引用学会官方条目页，而不必把高校转写当作唯一正文。转写本与官方页在规范化比对下同向，此前已编码的延续句和新写出的表述得到官方页印证。官方条目仍自称为试行版参考依据，不是「学位〔〕」号颁布件，不是学位法实施细则，不是 2025 年强制国标，也不是某校授予标准。西交大网页标题中的「教育部发布」与正文不符，不能当成颁布依据。0854 官方页确认五种形式并指向《工程类硕士专业学位基本要求》；在未对读前，仍不得与工程教指委〔2024〕20 号互称为同一文件。0812 与 0854 仍须分标，互不替代；2013/2014 年书页与现行教指委 0854 网页仍应并列保留，不能用官方百科条目静默删除它们，也不能用 2015 年领域汇编覆盖现行页或试行版类别篇。

**不要写成什么。** 不要说官方条目「暂未维护」；不要发明「学位〔〕」号；不要用西交大标题或某校授予标准填空；不要把五类创造性成果写成所有计算机应用技术论文必须对号入座的菜单；不要用试行版给硕士增加法定义务；不要发明「工作量饱满」的页数或实验组数；不要把「实践不少于半年」套到学术型论文；不要用 0812 与 0854 互代。

## 5. 建议编码的 A 项，以及明确不要编码的残留

**A1. 把学会官方百科的 0812、0854 条目正文升为试行版的直接依据，并写清限度。**（E；转写汇编改为核对用的 S）选题文件中关于试行版的书目与身份保持不变：国务院学位委员会第八届学科评议组、全国专业学位研究生教育指导委员会编修，中国学位与研究生教育学会公布，试行版，配合 2022 年目录实施，目的是参考依据，内容将调整完善。官方入口仍是 `https://www.acge.org.cn/encyclopediaFront/enterEncyclopediaIndex`。本轮已打开官方条目正文，建议改写出处如下：

- 0812：编写成员为计算机科学与技术学科评议组；简介接口 `encyclopediaFront/enterSubjectIntro?subjectId=402a8137577ab56fjg5774d92ba70077&type=encyclopedia_subject_intro`；学位基本要求接口 `encyclopediaFront/enterDegreeStandard?subjectId=402a8137577ab56fjg5774d92ba70077&type=encyclopedia_degree_standard`。
- 0854：编写成员为全国工程专业学位研究生教育指导委员会；相应接口使用 `subjectId=402a8137577ab56fjg5774d92ba70106`。
- 数据容器中的「简介暂未维护……」「学位基本要求暂未维护……」只是标签加载前的占位，不要写进技能当成条目状态。
- 江西农业大学转写汇编可保留为核对副本，不再作为唯一正文来源。已与官方页核对的延续句和新写出表述（假造、硕士工作充足、对照实验假说、五类创造性成果、知识结构中的「计算机网络与安全」「人工智能」、学术创新三个方面、「四个面向」、0854 实践半年及两年免修、选题、五种论文形式、「工作量饱满」无定量、博士实践不少于 1 年、十二个领域方向与工程教指委〔2021〕1 号）改为优先引用官方条目，并继续与 2013/2014 年 0812 书页、现行 0854 教指委网页分标并列。
- 这仍然**不是**「学位〔〕」号颁布件，不是学位法实施细则，不是 2025 年强制国标，也不是某校授予标准。西安交通大学研究生院标题中的「教育部发布」不得写入技能。五种形式所指向的《工程类硕士专业学位基本要求》仍未与工程教指委〔2024〕20 号对读，不得互称同一文件或互相替代。不要用官方条目覆盖或替代 2013/2014 年书页、现行教指委网页，也不要用 2015 年领域汇编覆盖试行版或现行页。不要把五类创造性成果写成必选菜单，不要给硕士增加法定义务，不要发明「工作量饱满」的定量。

**A2. 在数据分析文件中补充 JJF 1059.1-2012 的官方目录身份与「正文仍不可读」限度，以及 GB/T 27418-2017 官方不提供全文的说明；不要写入公式或最小 n。**（E 的目录 / 系统说明 + 明确限度的 S）可写：国家计量技术规范全文公开系统现行站点可以检索到 JJF 1059.1-2012《测量不确定度评定与表示》，状态为现行，发布 2012-12-03，实施 2013-06-03，替代 JJF 1059-1999；官方详情还列出起草人与发布部门。系统帮助要求使用 Adobe Reader 与 FileOpen 插件阅读下载文本；本轮取得的官方 `downPdf` 文件为 FileOpen（`FOPN_foweb`）加密 PDF，无法提取正文，因此**仍不得引用该规范中的公式或最小 n**。GB/T 27418-2017 在国家标准全文公开系统上因采用 ISO/IEC Guide 98-3:2008，官方条目明确「不提供文本阅读服务」，不得当作已打开的替代全文，也不得覆盖已编码的 GUM / TN 1297 / 片上射频 / JESD51-2A 限度。不要把 15–30°C 或 ±3°C 写成通用默认。

**明确不要编码的残留：**

- 2015 年书第 4、7、22 章正文、PICO/PICOC 是否被改写、协议修订细则，以及 22.1 之后对 “revision” 的展开。维持第 13 版已写入的限度句即可，不必因本轮再次打开同一预览和着陆页而改写 PICOC 或宣称 2007 已被替代。
- Jeruchim 1984 全文及任何默认误码事件数 / 数值置信区间公式。
- JJF 1059.1-2012、IEC 器件测量标准及其他未打开规程中的公式与最小 n。
- 把 AblationBench、Meyes 2019、Huang 注意力头协议或 Ulmer 2022 写成贡献消融通论，或指定 Bonferroni 为默认。
- 「学位〔〕」号颁布件；把西交大标题「教育部发布」写成全国颁布依据；把《工程类硕士专业学位基本要求》与工程教指委〔2024〕20 号互称同一文件。
- 上轮已列出、本轮仍成立的其他残留（0809 文献比例、p<0.05、徽章强制、T-ED 删 generally、软件学报字段未在投稿系统重核等）。

## 6. 本计划结束后若再迭代可优先补的焦点

本轮是该五轮计划的最后一轮，下列项目不是已经安排的「第 6 轮任务」，只是若计划结束后仍要继续补证，可优先考虑的残留：

1. **Kitchenham 2015 第 4、7、22 章正文。** 合法作者副本、图书馆借阅或出版社授权样章仍是打开 PICO/PICOC 定义、协议修订细则，以及 22.1 之后如何展开 “revision of … 2007” 的关键缺口。着陆页和官方预览已经不够。
2. **Jeruchim 1984 合法全文。** 仍是写入（或不写）误码事件数规则的关键缺口。Hamkins 2015 不能代替它。
3. **JJF 1059.1-2012 或可公开的 IEC / 国内半导体测量规程的可阅读全文。** 官方目录和 FileOpen 加密件已经见到；若能在不绕过技术保护的前提下取得可提取正文（例如授权阅读环境），再考虑是否引用公式。未打开就继续不写行业公式和最小 n。
4. **更直接的贡献消融通论。** 仍需要正式发表、范围不限于单一架构，并且同时讨论删除后重调、因素不独立与消融表多重比较的方法论文。
5. **「学位〔〕」号颁布件，以及《工程类硕士专业学位基本要求》与工程教指委〔2024〕20 号的原文对读。** 官方百科条目现已打开，这两项仍缺。

本轮在未改运行时技能、未同步桌面、未联系审查 bot 的前提下，打开了学会官方百科中 0812、0854 的简介与学位基本要求正文，并与高校转写汇编核对为同向；还取得了 JJF 1059.1-2012 的官方现行目录身份和一份无法阅读的 FileOpen 加密下载件，以及 GB/T 27418-2017「因采用 ISO/IEC 标准而不提供全文」的官方说明。第 13 版已经写好的独立研究步骤、主张—证据式工作量、预注册限度、消融不能自动等于因果、「不写默认事件数」、JESD51-2A 的有范围环境报告，以及 0812/0854 分标和「试行版不是学位〔〕号颁布件」，不需要推翻。需要补的是：把官方百科条目升为试行版直接依据，并写明 JJF / GB/T 27418 的「目录可见、正文仍不可读 / 官方不提供全文」限度。Jeruchim 1984、Kitchenham 书中第 4、7、22 章正文、可阅读的 JJF/IEC 全文、消融通论，以及带「学位〔〕」号的颁布件，仍未打开，相应规则必须保持残留，不能用着陆页、加密件、基准论文或学校标题填成事实。
