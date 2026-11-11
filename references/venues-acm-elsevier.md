# ACM / TON 与已填写的 Elsevier 刊卡

ACM TOCS 的专刊条款来自 2025-05-31 的[作者指南存档](https://web.archive.org/web/20250531153012/https://dl.acm.org/journal/tocs/author-guidelines)。2026-11-11 访问[现行作者页](https://dl.acm.org/journal/tocs/author-guidelines)返回 403。存档没有确认当前常规研究论文的长度、摘要窗口或匿名方式，实际提交前查当前稿约或投稿系统。其他 Elsevier 刊物按其作者指南填写[刊物卡片](elsevier-venue-card.md)。

器件与电路的 IEEE EDS / CASS 政策见 [venues-ieee-eds-cass.md](venues-ieee-eds-cass.md)。投稿检查仍走 [期刊论文流程](journal-workflow.md)。

## IEEE Transactions on Networking（ToN）

当前刊名和范围见 [IEEE Communications Society 期刊主页](https://www.comsoc.org/publications/journals/ieee-tnet)，投稿格式及前作要求见[该刊政策页](https://www.comsoc.org/publications/journals/ieee-tnet/policies-guidelines)。引用早期以 IEEE/ACM Transactions on Networking 刊名发表的文章时保留原刊名。

- **范围。** 主页明确包括片上网络、通信协议、网络系统与相应优化方法，不接收综述或教程。对社交网络主题，两页措辞不同：主页列出其中的信息传播和分布式系统问题，投稿政策将社交网络与智能电网、物理层通信列在范围之外。遇到交叉选题时应说明核心网络问题并核实范围。
- **格式：** 双栏、单倍行距、10 磅；不符合格式的稿件在送审前退回。
- **篇幅：** 投稿的**典型最大长度是 Transactions 双栏格式 16 页**。额外材料宜作为补充材料；否则须在投稿前与主编讨论，并在附信中说明理由。
- **费用。** 本刊强制超页费从第 11 页起计。开放获取另有 APC，投稿预算按当年政策及作者选用的出版路径分别核对。减免流程按 ComSoc 当期页面执行。
- **摘要：** **150–250 词**，一段、自洽；不含缩写、脚注、参考文献、显示公式或表格；宜在摘要文字中自然出现三至四个不同检索词或短语。另列关键词/Index Terms 按模板填写。图文摘要可选，提供时应一并送审。
- **前作与同时投稿：** 不得一稿两投；已在期刊或图书中发表的论文不得再投。会议论文可以投稿，但不得是原文照搬，并须按 IEEE 政策提供额外技术材料（额外材料不必是全新结果，可以是展开或证明）。附信应标明所据前作、链接、新增或扩充内容，并在稿中列入相应参考文献。arXiv、机构库或个人预印本按该刊规定允许。
- **投稿：** IEEE Author Portal（https://ieee.atyponrex.com/journal/TNET）；**所有作者须有 ORCID**。
- **审稿周期（页面当时表述）：** 自 2024 年 5 月起，主编每周处理投稿；从编辑分配到首次决定的平均与中位时间**目前约为五个月**。

## ACM 总政策中的会议扩展限度（不是 TOCS 专页）

来源：ACM《Prior Publication and Simultaneous Submissions》（https://www.acm.org/publications/policies/simultaneous-submissions，Reviewed April 2018；第 8 轮 WebFetch 打开，curl 403）。关键句：the paper has been substantially revised（this generally means that at least 25% of the paper is material not previously published; however, this is a somewhat subjective requirement that is left up to each publication to interpret）。配套页 *Conference Proceedings in ACM Journals*（Reviewed June 2018）要求期刊稿应是会议稿的 expanded version，并指向上述 Prior Publication 政策。

披露「generally … at least 25%」时，必须同时写上「subjective / left up to each publication to interpret」。会议扩展期刊仍以**该刊现行规定**为准。下面 TOCS「至少 25% 新内容」继续按既有 2025-05-31 存档专卡，不要把本总政策或 TOCS 专卡套到所有 ACM 刊物，更不要套到 IEEE 或其他出版方。不要退回百分之三十，也不要发明新百分比。本轮不重开或改写 TOCS 页数、Highlights 约 5000 词等已有卡片数字。

## ACM 论文模板（acmart）与 TOCS

来源：https://www.acm.org/publications/proceedings-template（第3轮取得）。

- 官方 LaTeX 类为 **acmart**。ACM 论文模板页给出 **Version 2.21**，并写「last update **November 3, 2026**」。同一官方页页脚另有「Document Last Revised: July 10, 2025 by Craig Rodkin and Bernadette Shade」。第 5 轮打开的官方 class 文档（https://portalparts.acm.org/hippo/latex_templates/acmart.pdf）与 CTAN 页同样给出 Version **2.21**，日期 **2026-11-01**。这与既有记录是同一版本，不是新版本。模板页上的日期与 class 文档日期一并保留，不以其中一处覆盖另一处。
- **区分评审稿和出版稿。** 先读目标期刊或会议的本轮征稿要求。ACM 通用 LaTeX 说明给出的单栏评审格式为 `\documentclass[manuscript]{acmart}`。出版阶段再用相应的期刊或会议版式，TOCS 的出版格式为 `acmsmall`。双匿名或审阅行号选项按该刊该阶段要求设置。[ACM 投稿与生产说明，第 1 页](https://authors.acm.org/binaries/content/assets/publications/taps/latex-best_practices-06-may-2020.pdf)
- 维持模板的字体、边距和页面设置。会议出版稿按会方通知选择相应版式，例如 `sigconf`。常规全文稿按要求填写 CCS Concepts、关键词与参考格式信息，短摘要、海报等按稿型核查。
- 形式方法以已打开的 class 文档为准，可对照：**2.8 Algorithms**（作者可选用文档允许的算法宏包）、**2.9 Figures and tables**、**2.18 Counting words**、**2.19 Disabled or forbidden commands**。ACM 官方作者 LaTeX 准备页第 5 轮 HTTP 403，算法宏包的允许名单不以被拦的 HTML 页补数。
- IEEEtran 的算法须放进 figure、使用 algorithmic / algorithmicx，且不要使用 algorithm2e 的浮动体，见 [ieee-style.md](ieee-style.md)。两套体例不要混用。
- **TOCS 作者指南（2025-05-31 官方 URL 存档；现场页本轮仍 HTTP 403）：** 稿件须 PDF，经 https://mc.manuscriptcentral.com/tocs 投稿；附 cover letter，说明与 journal scope 的关系。基于作者此前会议论文等已发表工作的稿件，须在首页脚注列出相关前作并说明新增贡献；ACM Journals/Transactions 的常态是至少 **25% new content**。新栏目 **Research Highlights** 面向更广读者的较短稿，仍须满足 **25–30% new material**；原文为 “we encourage authors to limit papers to **about 5000 words**, counting each figure/table for about 250 words (**although the limit will not be strictly enforced**)”。这是鼓励上限，不是硬性页数或词数门禁，编码时必须保留「encourage / although the limit will not be strictly enforced」，不得再只当作检索摘录。排版须用 ACM style（LaTeX 或 Word）；录用稿还须 ORCID 等 ACM 通行政策。上述仅说明存档当时的要求。现行匿名方式和常规稿篇幅由当期稿约确认。

## Computer Networks（ISSN 1389-1286）

来源：该刊 Guide for Authors https://www.sciencedirect.com/journal/computer-networks/publish/guide-for-authors（第3轮全文取得）。下列数字是该刊官方文本，**不要推广为所有 Elsevier 期刊的通则**。

与 Microelectronics Journal 相同、现已可写入刊卡的规则：

- **摘要：** 简明、基于事实，**不超过 250 词**。应说明目的，概述基本方法，写出主要发现（适用时含统计显著性）和主要结论，并强调新内容。摘要须能独立成篇；避免参考文献和不常见缩写（必须使用时给出定义）。
- **关键词：** **1 至 7 个**，英文；尽量避免用 and / of 拼成的多词关键词；关键词中的缩写仅在已通行时使用。
- **Highlights：鼓励**（未写成强制）。以单独可编辑文件提交，文件名含 “highlights”。**3 至 5 条，每条最多 85 个字符（含空格）**，应抓住新结果和任何新方法。
- **图文摘要：** 鼓励；图像宽度至少 1328 像素，长边水平，在 13 cm 宽度下仍可读；优先 TIFF / EPS / PDF / MS Office。
- **研究数据：Option C**——作者须把研究数据存入相关仓储并提供链接，或声明无法共享的原因（该声明将出现在正式发表的论文中）。
- 投稿时参考文献体例可先保持一致；录用后按期刊体例加工。正文引用为方括号编号。
- 使用生成式 AI 实质修改语言、结构或辅助稿件准备时，作者应按刊规在参考文献前说明工具、用途和人工核查。常规拼写、语法或标点检查可免声明。AI 用于研究方法时在方法节说明具体用途。AI 辅助制作流程等解释图时另核图注披露，生成数据图的输入与计算过程应可复核。图文摘要须核对该刊专门规则及出版方对通用生成式图像工具的限制。[Elsevier 期刊 AI 政策](https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals)

**仅本刊：** 还刊登 **Dataset Articles** 和 **Open-Source Software Articles**（描述用于获得学术结果的开放数据集或开源软件，如仿真器、模拟器、协议实现、监测工具等）。**作者简介最长 100 词**，并提供护照式照片，须为可编辑格式。

## Microelectronics Journal（ISSN 1879-2391）

来源：该刊 Guide for Authors https://www.sciencedirect.com/journal/microelectronics-journal/publish/guide-for-authors（第3轮全文取得）。摘要不超过 250 词、关键词 1–7、Highlights 鼓励且 3–5 条、每条不超过 85 个字符（含空格）、图文摘要、Option C 数据、生成式 AI 声明，与上一节 Computer Networks 的共同条款相同。同样**不要推广到未核对该刊指南的其他 Elsevier 标题**。

**仅本刊：** 文章类型包括原创论文、案例研究、会议报道、书评、快报；**综述宜先与编辑讨论**。结构上有「Theory and calculation」说明：理论部分应是对引言的延伸，计算部分应是从理论出发的实际展开。请建议审稿人（不宜是同事或近期合作者，不宜是编委会成员，最好来自不同国家）。
