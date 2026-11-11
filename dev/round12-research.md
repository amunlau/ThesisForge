# ThesisForge 第12轮调研报告：2015年综述书预览、Hamkins 编码误码区间、Szollosi TICS 排印本、Rubin 1976、JEDEC 热测环境、2015年专业学位汇编与教指委文号

- 调研日期：2026-11-11（Asia/Shanghai，CST，UTC+8）
- 方法：本地已核对的 research-to-report-and-briefing **v3.3.0**（`/workspace/research-to-report-and-briefing/SKILL.md` 的 `metadata.version` 为 `3.3.0`；重点遵循 `references/research-and-evidence.md`）。先形成研究问题与证据边界，优先原始依据，读足关键上下文，核对对象/单位/版本/比较条件，主动反向检索，观察与建议分开，缺口不填成事实。未制作 PPT。
- 现行工作副本：`/workspace/ThesisForge/` 第 11 版。本轮**未修改**除 `dev/` 报告副本以外的运行时技能文件，**未同步**用户桌面，**未联系**审查 bot。
- 上两轮报告只作背景，本轮独立检索并打开原文。已核对其 MD5：`round10-research.md` = `9b6ab578aebed0e35fc7e79287f332f8`；`round11-research.md` = `d286b83976ed3239f9a4f6f907884876`。已有来源在 `round10-sources/`、`round11-sources/`，本轮未改其文件，故不重复拷贝。
- 默认学科仍是计算机应用技术，兼顾通信与半导体电子。诚信约束不变。已结算事项本轮不推翻、不顺手改写。

观察、原文摘录、推导和建议分开写。搜索摘要不能单独支撑准备写入技能的句子。打不开的来源标为 FAIL，不用记忆填空。

## 1. 研究边界与问题

本轮是新五轮独立研究/实验/数据中的第 3 轮，侧重点仍是：加强技能的独立研究、实验设计、数据处理与分析，以支撑论文工作量与创新性成果。不重做已结算的格式/版式调研，也不重做已结算的逻辑/创新点位置/一条主线调研。

本轮覆盖的问题：

- **Q1.** 打开 Kitchenham、Budgen、Brereton《Evidence-based software engineering and systematic reviews》（CRC / Chapman & Hall，常引作 2015）或可合法取得的相应章节，核对它对 PICO/PICOC、质量评价、协议修订的写法，以及与 2007 年实施指南、SEGRESS 报告指南的关系。未打开不得仅凭 QAISER 二手转述改写 PICOC，也不得宣称 2007 已被替代。
- **Q2.** 合法取得 Jeruchim 1984 或真正等价全文；若取得 Hamkins 2015（IPN Progress Report 42-201）全文，可讨论编码系统下误码区间的报告方式，但仍须避免把某一种公式写成默认事件数规则。打不开就维持「不写事件数」。
- **Q3.** 取得 Szollosi 等 *Trends in Cognitive Sciences* 正式排印本，用正式页码核对预印本是否有实质性删改，再决定引用形式。打不开则保持预印本限度。
- **Q4.** 打开 JJF 1059.1、IEC、JEDEC 或国内半导体测量规程全文。未打开就继续不写行业公式和最小 n。若打开，只吸收与小样本、重复性/再现性、探针与温度报告有关的要求，并写清适用范围，不要覆盖已编码的 GUM / TN 1297 / 片上射频条款的限度。
- **Q5.** 打开 Rubin 1976 *Inference and Missing Data*（*Biometrika*）或合法作者副本，以便作页码级引用。打不开则保持「定义来自已打开转述、不写 1976 页码」。
- **Q6.** 寻找讨论「删除后重调、因素不独立、消融表多重比较」的更直接通论（正式发表、范围不限于某一架构）。不用 Meyes 2019，也不把 Huang 注意力头协议写成通例。
- **Q7.** 若出现国务院学位委员会正式汇编、明确文号的颁布本，或计算机类学术学位的新基本要求，与现行教指委网页及 2023-12 试行要求对读。仍不得用 0812 与 0854 互代。

此外，独立检索中与本轮主题直接相关、且第 11 版尚未覆盖的其他有益方法，必须打开原文并标等级后才列入。不把范围扩到格式或已结算的法律/学校逻辑。

## 2. 对第 11 版相关文件的核对或缺口

通读第 11 版中与本轮焦点相关的运行时文件后，判断如下。这些是对现行文本的观察，不是对本轮来源的预判。

**`literature-search.md`。** 仍以 Kitchenham 与 Charters 2007 实施指南为选题/系统综述规程的压缩来源；已写明 SEGRESS 是二次研究的**报告**指南，不是宣布 2007 已被替代；并写明 2015 年书本轮未打开，不能仅凭 QAISER 二手转述删除或改写 PICOC。PICOC 写法、 Wohlin 2014 雪球、选题轻量变体都还在。限度句没有写丢，但「2015 年书未打开」这一句是否仍成立，取决于本轮实际打开了哪些章节，见 Q1。

**`experiment-design.md`。** 消融限度已引用 NIST/SEMATECH OFAT 与交互、Melis 等未重调的混淆、Huang 预印本「一次切除不能自我证明因果」且标明不是通论；多重比较指向数据分析已有原则，不指定 Bonferroni。Pawlikowski 仍正确限定为电信网络随机仿真，不是 BER 事件数规则。Jeruchim 1984 仍标明未取得，通信规程不写数值事件数。这些限度应保持，除非本轮打开了可改变判断的原文。

**`data-analysis.md`。** 缺失数据已用 van Buuren / Schafer 转述 Rubin 分类，并明确「Rubin 1976 原文未打开、不写 1976 年页码」。GUM / TN 1297 / 片上射频条款及「不规定最小 n、不写 k 默认」仍在。IEC / JEDEC / JJF 1059.1 全文本标明未打开。若本轮打开 Rubin 或某份行业规程，只应在已打开范围内补页码或补有范围的报告要求，不得发明公式或最小 n。

**`independent-research.md`。** Szollosi 已按 PsyArXiv 预印本写入限度，并写明 TICS 排印本未打开、不得冒充正式刊出页码。预注册可选、不能补弱理论、不撤探索/验证诚实区分，这些实质判断本轮若打开排印本，应核对其是否被删改，而不是预先改写。

**`topic-and-contribution.md` 0854 专节。** 依据是教指委网站现行页（`meng.tsinghua.edu.cn` 6328.htm）以及 2023 年 12 月试行硕士论文要求（门户 PDF，文件名日期 20240508）。专节已写明页面本身未见单独的发布文号或发布日期，也写明不能把征求意见稿与现行页混称同一具名版本，除非另找到颁布件。0812 与 0854 分标互不替代的限度还在。本轮若找到正式汇编或明确文号，应与现行页及该试行 PDF 对读，而不是用新文件覆盖分标。

未见把已结算事项（学位法硕士限度、北大两句并存、清华行距、TCOM 无 30%、Pawlikowski 不是 BER 事件数、T-ED generally、不写默认 p/k/最小 n/BER 事件数/5% 缺失阈值等）写丢或偷偷改掉。

## 3. 已打开来源与等级

等级约定：E 表示已打开原文、可引用；S 表示有出处但须写明限度（预印本、转载、课程副本、官方预览而非全书、机构库排印本的 Wayback 副本、活仓库、领域外指南等）；U/FAIL 表示未取得可核对正文，不得编码为规则。搜索命中或摘要不等于已精读。获取时间均为 2026-11-11 Asia/Shanghai（CST）。

### 3.1 Q1 Kitchenham 2015 年书

| ID | 来源 | 等级 | 说明 |
| --- | --- | --- | --- |
| E1 | Taylor & Francis / CRC 官方 `googlepdf` 预览：Kitchenham, Budgen, Brereton，*Evidence-Based Software Engineering and Systematic Reviews*，Chapman & Hall/CRC。版权页写 © 2016 by Taylor & Francis Group, LLC；Version Date: 20151022；eBook ISBN-13 978-1-4822-2866-3。URL `https://api.taylorfrancis.com/content/books/mono/download?identifierName=doi&identifierValue=10.1201%2Fb19467&type=googlepdf`；75 页 PDF，MD5 `2ea54fb0958dccb9fb7d9bd973b54aa4`。 | **E（预览范围）/ 对未包含章节则为未打开** | 合法出版社预览。实际包含：扉页与版权页、目录（至附录与参考文献）、图/表目录、前言（pp. xix–xxi）、术语表、第 1 章正文第 3–15 页、参考文献第 367–389 页。**不包含**第 4 章（规划/研究问题/协议/质量评价，目录始于第 39 页）、第 7 章（研究质量评价，目录始于第 79 页）、第 22 章（Part III 指南程序，目录始于第 291 页）的正文。预览全文检索 **PICO / PICOC / PICOS 出现次数为 0**。 |
| S1 | Durham EBSE 书目页 `https://ebse.webspace.durham.ac.uk/ebse-bibliography/evidence-based-software-engineering-and-systematic-reviews/`（2026-11-11 打开，书目写作 2016 Chapman & Hall/CRC Press，399 pages）；Keele 研究页 `https://www.keele.ac.uk/research/ourresearch/computerscienceandmathematics/evidence-basedsoftwareengineering/`（把该书写作 2015，CRC Press，并称 updated guidelines form part of the book）。 | **S** | 作者机构书目/介绍，不是书的章节正文。可与版权页对照年代（2015/2016），不能代替未打开章节。 |
| 未采用 | Unicamp 课程站点 `https://ic.unicamp.br/~cafeo/onboarding/files/cap_1-3.pdf`（35 页，文件名标 cap 1–3）。 | **未作为合法证据采用** | 已下载以核对其覆盖范围，但授权关系不清楚，且即使采用也只到第 1–3 章，仍不含第 4、7 章。本轮判断不以该副本改写技能。 |

**FAIL / 未打开的章节：** 第 4 章「Planning a Systematic Review」、第 7 章「Assessing Study Quality」、第 22 章「Systematic Review and Mapping Study Procedures」正文，以及任何直接定义或改写 PICO/PICOC 的段落。因此仍不得仅凭 QAISER 转述改写 PICOC，也不得宣称 2007 年实施指南已被该书替代。

### 3.2 Q2 通信误码分析

| ID | 来源 | 等级 | 说明 |
| --- | --- | --- | --- |
| E2 | Hamkins, Jon，*Confidence Intervals for Error Rates Observed in Coded Communications Systems*，*The Interplanetary Network Progress Report*，Volume 42-201，2015-05-15，pp. 1–17。官方 URL `https://ipnpr.jpl.nasa.gov/progress_report/42-201/201C.pdf` 本轮 TLS 失败（curl 35）；本轮打开的是 Wayback 原始字节：`https://web.archive.org/web/20240310091330id_/https://ipnpr.jpl.nasa.gov/progress_report/42-201/201C.pdf`（与 2023-10-17 快照 MD5 相同）。17 页官方 PDF，MD5 `5b2073ef9d139ec3a31b047b4db4dfe8`。版权页：JPL / Caltech，NASA 合同，© 2015 California Institute of Technology，Government sponsorship acknowledged。 | **E** | 美国政府资助的 JPL 进度报告全文，合法公开。讨论的是**编码（及高阶调制）系统**的码字错误率与误码率置信区间，**不是** Jeruchim 1984 的等价全文。 |
| FAIL-J | Jeruchim，*Techniques for Estimating the Bit Error Rate in the Simulation of Digital Communication Systems*，*IEEE JSAC* 2(1):153–170，1984（DOI 10.1109/JSAC.1984.1146031）。本轮仍未取得合法公开全文；IEEE stamp 未取得正文。未发现可核对的作者副本或真正等价全文。 | **FAIL** | 不得用记忆、讲座或 Hamkins 填入 Jeruchim 的事件数或公式。 |

### 3.3 Q3 Szollosi TICS 排印本

| ID | 来源 | 等级 | 说明 |
| --- | --- | --- | --- |
| E3 | Szollosi, Kellen, Navarro, Shiffrin, van Rooij, Van Zandt, Donkin，*Is Preregistration Worthwhile?*，*Trends in Cognitive Sciences* 24(2):94–95，2020 年 2 月（在线 2019-12-28），DOI 10.1016/j.tics.2019.11.009。Radboud 机构库 Publisher’s version 现网页与 bitstream 本轮均 HTTP 403。本轮打开的是 Wayback 于 2025-10-22 捕获的同一机构库 Publisher’s version：`https://web.archive.org/web/20251022225553id_/https://repository.ubn.ru.nl/bitstream/handle/2066/215861/215861.pdf`。3 页 PDF（封面页 + 刊出第 94–95 页），MD5 `381eaab29febd89d2601d7ca38c47b83`。封面标明 Version of the following full text: Publisher’s version；Published under the terms of article 25fa of the Dutch copyright act；hdl.handle.net/2066/215861。 | **E（机构库排印本的 Wayback 副本）** | 可核对立式页码 94–95。引用应标 *TICS* 24(2):94–95（2020），并说明打开的是 Radboud 按荷兰版权法第 25fa 条保存的出版社版本之 Wayback 副本，不是从 Cell 官网直接取得。已与第 11 轮打开的 PsyArXiv 预印本（DOI 10.31234/osf.io/x36pz）对读。 |

### 3.4 Q4 测量规程

| ID | 来源 | 等级 | 说明 |
| --- | --- | --- | --- |
| E4 | JEDEC，*Integrated Circuits Thermal Test Method Environmental Conditions — Natural Convection (Still Air)*，JESD51-2A（Revision of JESD51-2, December 1995），January 2008。官方现站点 `https://www.jedec.org/sites/default/files/docs/JESD51-2A.pdf` 本轮 HTTP 403（文件头写明该文件可免费下载，JEDEC 保留版权）。本轮打开 Wayback 2013-07-18 / 2016-09-10 两份官方 PDF，MD5 均为 `a3babfb36b2658109f6af97a8515e251`，22 页。 | **E** | 官方免费 JEDEC 标准的历史快照，正文可核对。适用范围是集成电路封装在标准测试板上、自然对流（静风箱）下的结到环境热阻 θJA 测量环境，**不是**通用直流 I–V、也不是片上射频/探针规程。 |
| FAIL-JJF | JJF 1059.1-2012《测量不确定度评定与表示》。国家计量技术规范全文公开系统有条目，本轮仍未能打开可核对、无 FileOpen 插件限制的正文。商业「免费标准」站点不作为合法来源使用。 | **FAIL** | 不得写该规范中的行业公式或最小 n。 |
| FAIL-IEC | IEC 器件测量标准全文本轮未打开（检索到的多为目录或付费预览）。 | **FAIL** | 同上。 |
| FAIL-JESD51-1 等 | JESD51-1 等同期 JEDEC 热测方法本轮 Wayback 无成功的 PDF 快照，现站 403。 | **FAIL** | 不把未打开的系列标准写进技能。 |

### 3.5 Q5 Rubin 1976

| ID | 来源 | 等级 | 说明 |
| --- | --- | --- | --- |
| S2 | Rubin, Donald B.，*Inference and missing data*，*Biometrika* 63(3):581–592，1976 年 12 月。本轮打开的是 MIT CSAIL 课程转载的 JSTOR 刊出页扫描件：`https://people.csail.mit.edu/jrennie/trg/papers/rubin-missing-76.pdf`，13 页（第 1 页为 JSTOR 封面说明，第 2–12 页为 581–591，第 13 页为 592 后的扫描余页），MD5 `fb28f77a374bf927e1a212be2f7d404a`。OUP 官方 article-pdf 本轮 HTTP 403；Harvard DASH 记录页 429。 | **S** | 是该刊论文的 JSTOR 版面扫描，页码可核对；不是出版社 HTML，也不是作者手稿。引用须标明「JSTOR 扫描件的课程转载」。可用于页码级引用原文定义，不得假装打开了 OUP/JSTOR 订阅版。 |

### 3.6 Q6 消融方法文献

| ID | 来源 | 等级 | 说明 |
| --- | --- | --- | --- |
| E5 | Ulmer, Bassignana, Müller-Eberstein, Varab, Zhang, van der Goot, Hardmeier, Plank，*Experimental Standards for Deep Learning in Natural Language Processing Research*，*Findings of the Association for Computational Linguistics: EMNLP 2022*，pp. 2673–2692，2022-12。本轮打开 ACL Anthology 正式 PDF `https://aclanthology.org/2022.findings-emnlp.196.pdf`，MD5 `b8332e33559f515d66d701070ba3d196`。 | **E** | 正式发表，但范围是深度学习/自然语言处理的实验与报告标准，**不是**「贡献主张式消融」的通论，文中几乎不出现 ablation 一词。可引用其超参搜索报告与多重比较调整的**有范围**说法；不得写成通用消融法令，也不得把文中「例如 Bonferroni」写成技能默认校正。 |
| 未找到 | 讨论「删除后重调、因素不独立、消融表多重比较」且范围不限于某一架构的更直接通论。 | **本轮未打开此类通论** | 不使用 Meyes 2019。不把 Huang 注意力头协议写成通例。已编码的 NIST OFAT / Melis 未重调 / Huang 限度仍是现有最贴切依据。 |

### 3.7 Q7 专业学位正式文本与文号

| ID | 来源 | 等级 | 说明 |
| --- | --- | --- | --- |
| E6 | 河北大学研究生院转载扫描件：《专业学位类别（领域）博士、硕士学位基本要求》上/中/下册。上册 95 页，MD5 `63173ffec8f9c6d0e372c0d5702cfb48`；中册 222 页，MD5 `66334b4436d2a7922d59159f4be7a23e`；下册 182 页，MD5 `66720d4283d04e9f39914ed05e713c7a`。扫描设备 TOSHIBA e-STUDIO555，创建时间 2015-06-24。URL 见 `yjsy.hbu.edu.cn/__local/...`。本轮精读了全书目录、中册书页 132–136（085208 电子与通信工程）、147–150（085211 计算机技术），并核对该扫描下册末页为书页 498。该扫描省略了封面/版权页。 | **E（高校转载扫描件；书页码可核对）** | 版心书眉为「专业学位类别（领域）博士、硕士学位基本要求」。这是 2015 年专业学位**类别/领域**汇编，不是 2014 年《一级学科博士、硕士学位基本要求》上册，也不是现行 0854 教指委网页。 |
| E7 | 高等教育出版社官方产品页「专业学位类别(领域) 博士、硕士学位基本要求」：`https://xuanshu.hep.com.cn/front/h5Mobile/bookDetails?bookId=59ceed5aba9eb884cf81f914`（2026-11-11 打开）。作者：全国专业学位研究生教育指导委员会；出版时间：2015 年 3 月；ISBN 978-7-04-042441-6；页数 498；16 开。书介写：由全国专业学位研究生教育指导委员会依据专业学位博士、硕士学位基本要求按专业学位类别（或领域）制定，包括 97 个类别或领域。 | **E** | 用来核对书目身份（编著者、ISBN、出版年、页数与打开的扫描末页 498 一致）。本轮未打开纸书版权页本身。 |
| S3 | 中国矿业大学（北京）研究生院转载页，标题写作「9.国务院学位委员会《专业学位类别（领域）博士、硕士学位基本要求》[2015-06]」，https://yjs.cumtb.edu.cn/info/1021/1499.htm（页内时间 2024-01-06）。附件为上/中/下册，但下载接口需要验证码，本轮得到的是 3829 字节 HTML，未能打开 PDF。 | **S（书目线索，正文未打开）** | 「国务院学位委员会 / 2015-06」是该校栏目表述，比已打开的高教社产品页（教指委编，2015 年 3 月）更粗。不得把未打开的附件或该校栏目用语写成版权页原文。 |
| E8 | 全国工程专业学位研究生教育指导委员会，*关于发布〈工程类专业学位类别硕士学位论文基本要求（试行）〉的通知*，工程教指委〔2024〕20 号，2024-05-08。现行页 `https://meng.tsinghua.edu.cn/xxfb/tzgg/6290.htm`，MD5 `00f8f3e64ba931f41b6370f8fd820b80`。北京大学研究生院转载页（2024-05-10 发布）文本一致，并指向同一附件 `https://meng.tsinghua.edu.cn/docs/20240508133731877935.pdf`。该附件与第 11 轮已打开 PDF、以及本轮哈工大转载 PDF 的 MD5 均为 `c7789fab37e905e1c94456f2e164912e`。附件封面署「2023 年 12 月」。 | **E** | 为已打开试行要求补上正式发布文号与发布日期。不是一份新的、内容不同的国家标准，也不是 0854 类别基本要求本身，更不是 0812。 |
| 未作为全国文本 | 海南大学《研究生学位申请科研成果基本条件》（2019 年 10 月校内文件）。检索时 URL 易被误认为 2015 年汇编。 | **排除** | 这是学校科研成果条件，不是国务院或教指委颁布的专业学位基本要求全书。 |

**未打开：** 带「学位〔xxxx〕号」的国务院学位委员会颁布件；计算机科学与技术（0812）一级学科基本要求的 2024/2025/2026 年全国新文本。本轮检索未见可打开的新学术学位基本要求全书。

## 4. 按问题组织的发现

### 4.1 Q1 2015 年书：官方预览已打开，但还不够改写 PICOC 或宣布替代 2007

**观察。** 官方预览可以确定书目与结构。版权页：

> © 2016 by Taylor & Francis Group, LLC […] Version Date: 20151022 / International Standard Book Number-13: 978-1-4822-2866-3 (eBook - PDF)

Keele 研究页把同一著作写作 2015 年 CRC Press，Durham 书目写作 2016。这是常见的「完稿/版权年」并存，引用时可同时披露，不必在 2015 与 2016 之间代选。预览目录把全书分为三部分，第 III 部分标题就是 “Guidelines for Systematic Reviews”，始于第 291 页；第 4 章为 “Planning a Systematic Review”（第 39 页起），其中 4.3 Specifying the research questions、4.4 Developing the protocol（含 4.4.5 Assessing the quality of the primary studies）、4.5 Validating the protocol；第 7 章为 “Assessing Study Quality”（第 79 页起）；第 22 章目录有 22.4.2 Specifying research questions、22.4.3 Developing the protocol、22.4.4 Validating the protocol。这些只是**目录条目**，相应正文不在预览中。

前言（p. xx）对 Part III 的自我定位是：

> Lastly, the third part provides a practical guide to conducting systematic reviews (the guidelines), drawing together accumulated experiences to guide researchers and students when they are planning and conducting their own studies.

已打开的参考文献中列有：

> Kitchenham, B. & Charters, S. (2007), Guidelines for performing systematic literature reviews in software engineering, Technical report, Keele University and …

预览正文（含第 1 章第 3–15 页、术语表、前言）中，PICO / PICOC / PICOS 一次都未出现。术语表有 research question 与 protocol 的一般定义（协议应在研究开始前写下，偏离应记录；研究问题为研究提供理由），这与技能里「协议或纳入标准若有改动必须记录」同向，但不是对 PICO 要素的重新立法。术语表还有一句抽样「经验规则」：“a sample size of at least 30 is required”——这与已结算的「不写默认最小 n」冲突，**不得**写入技能。

**含义。** 这本书确实包含被作者称为 “the guidelines” 的第三部分，并且 2007 年技术报告出现在该书参考文献中；仅凭已打开文本，看不出「2007 已被替代」或「PICOC 应删改」的原句。SEGRESS 仍是报告指南，2015 年书的规划/质量评价/协议修订章节仍未打开。

**不要写成什么。** 不要宣称「第 12 轮已打开 2015 年书，因此 2007 已被替代」。不要仅凭目录或 QAISER 转述改写或删除 PICOC。不要把术语表里的 “at least 30” 写成学位论文或系统综述的默认样本量。不要把 SEGRESS 与未打开的第 22 章混称为同一文本。

### 4.2 Q2 Jeruchim 仍 FAIL；Hamkins 2015 全文可讨论编码系统的区间报告，但不得写成默认事件数

**观察。** Jeruchim 1984 本轮仍无合法全文，维持「不写事件数」。Hamkins 2015 已打开，对象是编码通信链路的码字错误率（CWER）与误码率（BER）。摘要与第 2 页明确：

> Since bit errors in systems that use coding or higher-order modulation do not occur independently, blind application of a method that assumes independence leads to inappropriately narrow confidence intervals. We present a new method to compute the confidence interval properly, using the first and second sample moments of the number of bit errors per codeword.

第 10 页引用 Massey 1976：帧内比特译码高度相关，因此不能断言对观察到的误码率比对帧错误率有「更多的独立判决」。第 16 页的例子显示，若错误地假定比特独立，得到的 95% 区间会过窄，以至于真值落在区间外。

该文在第 2 页列出若干 “Rules of Thumb”（均标明 95% 置信水平），例如无错误的 w 个码字试验可将真 CWER 上界定在 4/w 以下；至少观察到 4 个码字错误才能把 CWER 定到一个数量级以内；相对误差 ±100γ% 大约需要 4/γ² 个码字错误（文中举例 16 个对应 ±50%，400 个对应 10%）。第 5 页说明 Rule of Thumb 1 来自无错误时 95% 上限约 3.69/w 的取整。第 12 页 Theorem 1 给出编码 BER 的类似停止准则，并写 “with 95% confidence”。这些是该报告在设定 β=95%、并在二项/高斯近似下推出的工程师口诀，不是跨领域默认事件数，也不是 Jeruchim 1984 的公式。

**含义。** 对**编码或高阶调制**系统，技能可以（有限度地）吸收一条报告原则：比特错误不独立，不要盲目套用独立伯努利误码区间；应报告与相依结构相称的不确定度（该文用每码字误比特数的一、二阶样本矩）。通信仿真的停止与区间，合法可用的网络仿真规程仍是已编码的 Pawlikowski；Hamkins 补充的是编码误码区间，不替代 Pawlikowski，也不填补未打开的 Jeruchim。

**不要写成什么。** 不要写入「必须观察到 4 / 16 / 100 / 400 个错误」。不要把 4/w、4/γ² 或 95% 写成技能默认。不要把 Hamkins 说成 Jeruchim 的等价全文。不要把编码 BER 的相依警告套到独立无编码二元信道上，以致禁止后者使用本来适用的独立事件方法。不要用该文改写 Pawlikowski 的事先精度与序贯停止。

### 4.3 Q3 TICS 排印本已打开：核心论点与预印本一致，可用正式页码

**观察。** 排印本页码为 *Trends in Cognitive Sciences*, February 2020, Vol. 24, No. 2, pp. 94–95。开篇与第 11 轮已打开预印本一致：反对把预注册当成（强版本）解决族错误率等统计问题、或（弱版本）自发推动理论变好的装置；统计检验的诊断力取决于模型与理论的映射；预注册不能补偿弱理论。第 94 页写：

> Solving problems of poor statistical practice with preregistration does not compensate for weak theory [6].

第 94 页右侧栏写：当理论足够强时，事后的**科学**推断并无固有问题；关键是事后解释须像事先解释一样被严格检验。第 95 页结论与预印本同一句：

> We conclude that, although preregistration should be an option for anyone who thinks it improves their research, requiring, rewarding, or promoting it (e.g., with badges, research funding, etc.) is not worthwhile.

排印本声明其批评聚焦于把预注册当作改进科学推理与理论发展的手段，并不深入讨论它在提高研究与方法透明度方面的作用。致谢中提及预印本曾题为 “Preregistration is redundant, at best”。对读后，本轮未见足以改变第 11 版已编码限度的实质性删改；改变的是**可以改用正式刊出页码**，而不再只标预印本、也不得再写「排印本未打开」。

**不要写成什么。** 不要写成「Szollosi 反对区分探索与验证」。不要禁止可选的预注册。不要用这篇短评要求取消「事先写清主指标、事后探索必须标明」。不要把预印本页码冒充 *TICS* 页码；反之，既已打开排印本，也不必继续只引预印本来回避页码。

### 4.4 Q4 打开了 JESD51-2A，但只覆盖静风箱中的封装 θJA；JJF / IEC 仍 FAIL

**观察。** JESD51-2A（2008-01）目的（标准前页）写明：

> The purpose of this document is to outline the environmental conditions necessary to ensure accuracy and repeatability for a standard junction-to-ambient (θJA) thermal resistance measurement in natural convection. […] The intent of θJA measurements is solely for a thermal performance comparison of one package to another in a standardized environment. This methodology is not meant to and will not predict the performance of a package in an application-specific environment.

§1 Scope（印页第 1 页）：环境条件**只适用于**安装在标准测试板上、水平放置（封装朝上）、在抑制外来气流的箱体内、仅由被测封装产生自然对流的 θJA 测量。§4.6.1.1（印页第 6 页）：

> The room ambient temperature when the tests are conducted shall be between 15°C and 30°C. If the room in which the testing occurs suffers from drastic temperature changes (>±3°C), then placement of a larger box over the test enclosure should be considered.

文中有热电偶、夹具与稳态程序，但没有「必须测 N 只器件」的一般最小样本量，也不是 GUM 的不确定度评定手册，更不是片上射频探针规程。

JJF 1059.1-2012 与 IEC 器件测量标准全文仍未打开。

**含义。** 若主张的是集成电路封装在静风箱中的结到环境热阻比较，可以要求报告该标准意义上的环境控制（并写清范围）。15°C–30°C 与 ±3°C 是该标准对自己试验室环境的规定，不得写成技能对所有器件测量的默认。已编码的 GUM Type A/B、TN 1297、片上射频/探针条款不被这份热测环境标准覆盖或取代。

**不要写成什么。** 不要写「必须在 15–30°C 测量」或「温度变化必须小于 ±3°C」作为通用器件规则。不要把 θJA 静风比较说成「预测实际应用中的结温」。不要引用未打开的 JJF / IEC 公式。不要编造最小 n。不要把通信仿真或机器学习测试分数改称按 JESD51-2A 计算的测量不确定度。

### 4.5 Q5 Rubin 1976 原文已打开，可用 1976 页码引用其原术语

**观察。** 刊出首页为 *Biometrika* (1976), 63, 3, pp. 581–92。第 582 页给出后文所用的形式定义（原文没有使用后来通行的缩写 MCAR；此处的 “missing at random” 与 “observed at random” 是 1976 年的用语）：

> The missing data are missing at random if for each possible value of the parameter φ, the conditional probability of the observed pattern of missing data, given the missing data and the value of the observed data, is the same for all possible values of the missing data.
>
> The observed data are observed at random if for each possible value of the missing data and the parameter φ, the conditional probability of the observed pattern of missing data, given the missing data and the observed data, is the same for all possible values of the observed data.

同页说明：在作抽样分布推断时，若缺失数据为 missing at random 且观测数据为 observed at random，则忽略缺失机制是适当的；而作直接似然或贝叶斯推断时，在 missing at random 且 φ 与 θ 可分的条件下，忽略缺失机制是适当的。第 581 页摘要把这些条件称作 “the weakest general conditions under which ignoring the process that causes missing data always leads to correct inferences”。

**含义。** 现在可以对 1976 年定义作页码级引用。但 1976 年的成对用语（missing at random / observed at random）与后来 van Buuren、Schafer 所转述的 MCAR / MAR / MNAR 三分法不是同一套标签；后者仍以已打开的转述为准，不要把 1976 年第 582 页的 “missing at random” 直接改写成今天口语中的 MAR，而不加说明。完整案例、多重插补「不是唯一合法选择」、不写 5% 阈值等已编码原则，并不被 1976 年这篇推断论文改写成新的数值规则。

**不要写成什么。** 不要写「Rubin 1976 已经规定缺失不到 5% 就可以列表删除」。不要把 1976 年的 “missing at random” 无说明地等同于现行技能里来自 van Buuren 的 MAR 一句定义。不要假装打开的是 OUP 官方 HTML。不要用 1976 年论文发明最小样本量。

### 4.6 Q6 未找到更直接的消融通论；Ulmer 2022 只是 NLP/DL 实验报告标准

**观察。** 本轮打开的正式发表文献中，最接近「实验报告与多重比较」的是 Ulmer 等 2022（EMNLP Findings，pp. 2673–2692）。它把实践分成数据、代码与模型、实验与分析、发表，并用⋄标出「应被视为最低要求」的条目，例如报告超参搜索的范围、最终设置、试验次数与搜索程序；报告多次运行的均值与标准差；进行比较时做显著性或贝叶斯分析并说明方法选择。关于多个模型或数据集的比较，第 5 节写：

> We also want to draw attention to the fact that comparisons between multiple models and/or datasets, require an adjustment of the confidence level, for instance using the Bonferroni correction (Bonferroni, 1936), which is a safe and conservative choice and easily implemented for most tests.

文中没有系统讨论「去掉模块后是否必须重调」「因素不独立时不能把单因素差值写成主效应」，也几乎不以 ablation 为对象。因此它不能取代已编码的 NIST OFAT / Melis / Huang 限度，也不能把 Bonferroni 从「文中举例的保守选择」升为技能默认。

**不要写成什么。** 不要把 Ulmer 写成贡献消融通论或学位论文法令。不要指定 Bonferroni 为默认校正。不要用它回改 Huang「不是通论」的限度，也不要用它重新引入 Meyes 2019。

### 4.7 Q7 2015 年专业学位汇编已打开，且试行要求已有明确文号；二者都不能与 0812 或现行 0854 页互代

**观察（2015 年汇编）。** 河北大学转载扫描件的书眉为《专业学位类别（领域）博士、硕士学位基本要求》。高教社官方产品页：全国专业学位研究生教育指导委员会编，2015 年 3 月，ISBN 978-7-04-042441-6，498 页，与扫描下册末页书码 498 一致。矿大研究生院栏目写作「国务院学位委员会……[2015-06]」，但本轮未打开该校附件，也未打开纸书版权页；书目身份以已打开扫描书眉 + 高教社产品页为准，同时披露该校栏目的不同署法。全书按**当时的专业学位类别或工程硕士领域**分篇，目录中 085208 电子与通信工程始于第 132 页，085209 集成电路工程始于第 137 页，085211 计算机技术始于第 147 页，085212 软件工程始于第 151 页。这是 2018 年目录调整、将原工程硕士若干领域统筹到 0854 电子信息**之前**的领域文本，不是现行 0854 类别基本要求，也不是 0812 学术基本要求。

085211「计算机技术领域工程硕士专业学位基本要求」第 147 页把该专业学位定义为「与本工程领域任职资格相联系的专业性学位」，硕士生应成为「基础扎实、素质全面、工程实践能力强，并具有一定创新能力的应用型、复合型高层次工程技术和工程管理人才」。第 148–149 页：学术上「杜绝抄袭与剽窃、伪造与篡改等学术不端行为」；实践时间「不少于半年」，实践类学分约占总学分 20% 左右，实践成果直接服务于实践单位。第 149–150 页：选题应直接来源于应用课题、工程实际或具有明确的工程背景，研究成果要有实际或潜在的应用价值，选题要有一定的技术难度和工作量，要具有一定的理论深度。论文形式可以是研究类（如应用研究）或设计类和产品开发类。水平要求第（2）条：

> 学位论文工作应在导师指导下独立完成，论文工作量饱满。

085208 电子与通信工程第 135 页有平行的「论文工作量饱满」，同样没有页数、章数或实验组数。第 134 页同样要求实践时间不少于半年。这些与现行技能里「专业学位文本里的『工作量饱满』同样没有定量定义，不得发明页数或实验组数」同向，只是现在可以引用 2015 年汇编的具体书页。

**观察（试行要求的文号）。** 已打开的试行 PDF 封面仍署「全国工程专业学位研究生教育指导委员会 / 2023 年 12 月」。教指委 2024-05-08 通知（工程教指委〔2024〕20 号）称：受国务院学位委员会办公室委托组织编制该《基本要求》，适用于电子信息等 8 个专业学位类别，现予发布，请各单位补充完善并制定实施细则。附件 PDF 与第 11 轮已打开文件为同一份（MD5 相同）。因此：封面起草月份是 2023 年 12 月，正式发布文号和日期是工程教指委〔2024〕20 号、2024-05-08。这不是 0854 类别基本要求网页的「颁布件」，也不能代替 0812。

**未见到的。** 本轮未打开带「学位〔xxxx〕号」的国务院学位委员会颁布全书，也未打开 0812 或计算机类学术学位基本要求的全国新文本。

**不要写成什么。** 不要用 2015 年的 085211 / 085208 **领域**文本替换现行 0854 **类别**网页，或回改 0812。不要把 2015 年汇编写成 2025 年新国标或学位法实施细则。不要把「工作量饱满」「实践不少于半年」写成学术型计算机论文的默认规则，也不要发明「饱满 = 若干页 / 若干组实验」。不要把工程教指委〔2024〕20 号说成一份与 2023 年 12 月试行文本不同的新标准，也不要把该文号写成国务院学位委员会的「学位〔〕」号。不要用某校 2025 版授予标准或海南大学校内科研成果条件冒充全国汇编。

## 5. 建议编码的 A 项，以及明确不要编码的残留

下列 A 项只包含 E，或限度已经写明的 S。它们是给后续编码轮的建议，不是本轮对运行时文件的修改。

**A1. 用已打开的 TICS 排印本更新 Szollosi 的引用形式，不改已编码的实质限度。** 引用改为 Szollosi 等，*Is Preregistration Worthwhile?*，*Trends in Cognitive Sciences* 24(2):94–95，2020（打开的是 Radboud 出版社版本的 Wayback 副本）。预注册不能补偿弱理论，也不能被当成要求、奖励或推广（如徽章、资助）的装置；它仍应是可选项。与预印本对读未见实质性删改。继续不要写成「反对区分探索与验证」，不要禁止可选预注册，不要取消「事先写清主指标、事后探索必须标明」。

**A2. 通信误码：维持「不写默认事件数」；仅对编码或高阶调制系统补充相依性警告。** Jeruchim 1984 仍 FAIL。若讨论编码系统的 BER 区间，可写明：比特错误通常不独立，不要盲目套用独立事件公式，应报告与相依结构相称的不确定度（Hamkins 2015 用每码字误比特数的一、二阶样本矩，并给出了该文自己的 95% 口诀）。**不要**把 4、16、400、4/w 或 95% 写入技能默认。Pawlikowski 规程不因此被替换。

**A3. 缺失数据：可以开始用 Rubin 1976 第 582 页做页码级引用，但必须保留其原术语，并继续以 van Buuren / Schafer 为后来三分法的出处。** 注明打开的是 JSTOR 扫描件的课程转载。不要把 1976 年的 “missing at random / observed at random” 无说明地改写成现行 MCAR/MAR 标签。不写 5% 阈值，不指定某种插补为唯一合法选择。

**A4. 在测量不确定度节为「集成电路封装静风箱 θJA」补一条有范围的环境报告要求。** 依据 JESD51-2A（2008）。只适用于该标准的自然对流结到环境热阻比较，目的是标准化环境下的封装之间比较，不是预测应用结温。不要把 15°C–30°C 或 ±3°C 写成通用器件默认，不要覆盖 GUM / TN 1297 / 片上射频条款，不要发明最小 n。JJF / IEC 仍未打开，继续不写那些文件中的公式。

**A5. 把 2015 年《专业学位类别（领域）博士、硕士学位基本要求》作为与 0812、现行 0854 网页分标的历史汇编写入 0854 专节。** 书目：全国专业学位研究生教育指导委员会编，高等教育出版社，产品页署 2015 年 3 月，ISBN 978-7-04-042441-6；依据为河北大学研究生院转载扫描件（书眉可核对；扫描省略版权页，ISBN/出版月以高教社产品页核对）。只引用与计算机/通信/电子相关的领域篇（至少 085211、085208）：「工作量饱满」无定量定义；实践时间不少于半年（这是该领域专业学位条款，不是学术型默认）；选题来自工程实际或明确工程背景；杜绝伪造与篡改。明确这是目录调整前的工程硕士**领域**文本，不得代替现行 0854 电子信息类别网页，不得回改 0812。

**A6. 为已打开的工程类硕士论文试行要求补上发布文号。** 文件封面仍为 2023 年 12 月；正式发布为工程教指委〔2024〕20 号，2024-05-08，受国务院学位委员会办公室委托。与 0854 教指委基本要求页、学位办〔2024〕18 号、0812 继续分标，互不替代。不要把它写成新的类别基本要求颁布件。

**A7. 更新文献检索文件中「2015 年书未打开」的限度句，但不要改 PICOC。** 改为：已打开出版社官方预览（前言、目录、术语表、第 1 章第 3–15 页、参考文献）；规划、质量评价与协议修订各章正文以及 PICO/PICOC 定义仍未打开。因此仍不能宣称 2007 年实施指南已被替代，也不能仅凭 QAISER 或目录改写 PICOC。前言仅把 Part III 称为 “the guidelines”。

**明确不要编码的残留：**

- Jeruchim 1984 全文，以及任何默认 BER / 错误事件数或数值置信区间公式。
- Kitchenham 2015 第 4、7、22 章正文中的 PICO/PICOC、质量评价程序与协议修订细节；「2007 已被该书替代」。
- JJF 1059.1-2012、IEC 器件测量标准全文中的公式；任何最小器件数；把 15–30°C 或 ±3°C 写成通用默认。
- 把 2015 年 085211/085208 与现行 0854 或 0812 互代；把「工作量饱满」定量化；把「实践不少于半年」套到学术型论文。
- 把工程教指委〔2024〕20 号说成学位〔〕号或与试行 PDF 不同的新标准。
- 计算机类学术学位基本要求的「新国标」（本轮未见可打开文本）。
- Ulmer 或任何来源中的默认 Bonferroni、默认 p、默认最小 n。
- Meyes 2019；把 Huang 注意力头检查项写成通例。
- 术语表或 Hamkins 口诀中的样本量/事件数经验规则。
- 上轮已列出、本轮仍成立的其他残留（0809 文献比例、p<0.05、徽章强制、T-ED 删 generally、软件学报字段未在投稿系统重核等）。

## 6. 给第 4–5 轮的线索

1. **Kitchenham 2015 第 4、7、22 章正文。** 官方预览不够。若能合法取得这些章节（作者副本、图书馆或出版社样章），再核对 PICO/PICOC 是否被改写、协议修订如何写、以及正文如何定位 2007 年指南。未打开就维持 A7 的限度。
2. **Jeruchim 1984 合法全文。** 仍是写入（或不写）误码事件数规则的关键缺口。Hamkins 不能代替它。
3. **JJF 1059.1 或可公开的 IEC 器件测量正文。** 官方公开系统仍受插件限制。未打开就继续不写行业公式和最小 n。
4. **更直接的贡献消融通论。** 仍缺一篇正式发表、不限于单一架构、同时讨论删除后重调、因素不独立与消融表多重比较的方法论文。
5. **0854 类别基本要求的「颁布件」与 0812 新文本。** 2015 年汇编是领域文本；现行 0854 仍主要依据教指委网页。若出现国务院学位委员会带文号的新汇编，或计算机类学术学位新基本要求，再与现行页对读。不要用学校授予标准填空。

本轮在未改运行时技能、未同步桌面、未联系审查 bot 的前提下，打开了 2015 年综述书的官方预览（但关键章节仍缺）、Hamkins 2015 编码误码区间全文、Szollosi 的 *TICS* 排印本、Rubin 1976 刊出页、JESD51-2A、2015 年专业学位类别/领域汇编中与电子信息相关的领域篇，以及工程教指委〔2024〕20 号发布通知。第 11 版已经写好的独立研究步骤、主张—证据式工作量、预注册限度、消融不能自动等于因果、「不写默认事件数」和 0812/0854 分标，不需要推翻；需要补的是引用形式、编码误码的相依性警告、Rubin 原术语的页码、有范围的 θJA 环境报告、2015 年领域汇编的历史位置，以及试行要求的文号。Jeruchim 1984、Kitchenham 书中 PICO/质量评价/协议各章、JJF/IEC 全文仍未打开，相应规则必须保持残留，不能用预览、目录、口诀或记忆填成事实。第 4–5 轮应优先补这些仍 FAIL 或仅有预览的原文，而不是重开已结算的格式与法律判断。
