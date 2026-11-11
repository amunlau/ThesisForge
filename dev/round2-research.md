# ThesisForge Round 2 Research Report

**Date:** 2026-11-11 (Asia/Shanghai)\
**Scope:** Independent, evidence-based close of the twelve Round-2 priorities listed in the task brief.\
**Method constraint:** No invented standards, quotations, or numeric rules. Every clause-level or numeric rule is sourced from a page or PDF successfully obtained in this round, or is marked **U**. Failed fetches keep their URLs and are labelled.

**Independence:** This report starts from the Round-1 gaps and from primary sources fetched or downloaded in this round. It does not re-litigate the Degree Law stack, the “one-story thesis,” IEEE/ACM contribution-front review, or SIGPLAN/Heiser evaluation, except where a later source corrects or concretely operationalizes them. Round 1 is cited only to record what was already established and to avoid retrying blindly failed URLs.

**Evidence labels**

| Label | Meaning |
| --- | --- |
| **E** | Evidence: clause or number taken from a document successfully downloaded or a page successfully fetched in this round |
| **S** | Synthesis: a comparison or operational implication drawn from two or more **E** items, not a new rule |
| **U** | Unknown / unverified in this round: fetch failed, only a search snippet was available, or the source does not state the number |

Local working copies of successfully downloaded PDFs and extracted text live under `/workspace/thesisforge-research/round2-sources/`. Those copies are research aides, not substitutes for the cited URLs.

---

## 1. GB/T 7713.1—2025 (clean text: abstract, electronic theses, originality/authorization, Appendix A)

### 1.1 Sources obtained

**E.** Two university-hosted PDFs of the standard were downloaded and extracted:

- Hunan Agricultural University Graduate School copy: https://yjsy.hunau.edu.cn/xwgz/xgxz_1462/202603/P020260325595645822472.pdf — 28 pages, A4, created 2025-09-13. This is the URL flagged in Round 1 as “located but not fully fetched.”
- Soochow University Library copy: https://library.suda.edu.cn/_upload/article/files/02/da/9cb404ca436785662c23c2c596b6/a911b195-fac8-4416-96b9-1d372f061178.pdf — also the 2025 standard. Layout extraction is cleaner than the Hunan copy for Appendix A.

Cover metadata on both copies: title *信息与文献 编写规则 第1部分：学位论文*; replaces GB/T 7713.1—2006; **发布 2025-08-01，实施 2026-02-01**; ICS 01.140.20, CCS A14; issued by 国家市场监督管理总局 / 国家标准化管理委员会. Drafting units include 武汉大学, 中国科学技术信息研究所, 清华大学, 北京大学, and others. Drafters include 陈传夫, 饶艳, et al.

**U.** Official SAMR/openstd detail pages were not obtained as clean full text in this round. Previously failed or only-located URLs remain:

- https://std.samr.gov.cn/gb/search/gbDetailed?id=3B46A026CC84469CE06397BE0A0AEEB8 — Round 1 timeout; not re-fetched as a working full-text source here.
- Alternate listings on `openstd.samr.gov.cn` were not needed once the university PDFs were in hand.

The two university PDFs agree on the clauses below. Clause numbers follow the Suda extraction, which preserves “5.2.6 / 5.2.7 / 5.2.9” more clearly than the Hunan layout (the Hunan text sometimes collapses “5.2.6” to “5.6”).

### 1.2 Scope and electronic theses

**E.** Scope (Ch. 1): the document specifies the components of a thesis and the basic writing and layout requirements. It applies to printed, microform, and **electronic** theses and all other dissemination forms.

**E.** Clause 4.6 (overall requirements): printed theses should use A4 (210 mm × 297 mm) and should be printouts, printed copies, or photocopies. **电子版学位论文应采用通用文件格式，并可提供音频、视频、数据集等数字资料.**

**E.** Foreword item (f) records this as a change versus the 2006 edition: the revision adds format and content requirements for electronic theses (see 4.3, 4.4, 4.5, 4.6). Foreword item (x) / (s) records that the 2006 “学位论文数据集” appendix (2006 Appendix H, and 2006 5.6.4) was **deleted**.

**E.** Appendix material that may include digital objects (5.5): among admissible appendix contents are “某些重要的原始数据、数学推导、结构图、统计表、视频、音频、数据集等.”

### 1.3 Originality statement and use-authorization statement

**E.** 5.2.6 原创性声明 (Appendix A: **必备**):

> 学位论文应有论文原创性声明。学位申请人员应恪守学术道德和学术规范，在指导教师指导下独立完成学位论文，杜绝抄袭、篡改、伪造等学术不端行为及代买、买卖论文等造假行为。所有引用或参考内容均应标明出处。

**E.** 5.2.7 使用授权说明 (Appendix A: **必备**):

> 学位论文应有使用授权说明。学位申请人员应遵守学位授予单位有关保存、使用学位论文的相关规定。学位授予单位有权保存学位论文的印刷本和电子版，并提供文献检索与阅览服务，以及向国家有关部门或机构送交学位论文的复印件和电子版。

**S.** The national standard therefore requires both statements as mandatory elements, and it authorizes the degree-granting unit to retain print and electronic copies and to provide retrieval/reading and legal deposit. Exact wording of the signed forms remains a school matter (see §3).

### 1.4 Abstract length, keywords, and related abstract rules

**E.** 5.2.9 摘要页 (Appendix A: **必备**). The abstract must be independent and self-contained; it should contain information equivalent in substance to the thesis so that a reader can decide whether to read the full text, and so that secondary literature can use it. It should state purpose, methods, results, and conclusions, **with emphasis on results and conclusions**. Abstract writing shall conform to **GB/T 6447**. Figures, tables, chemical structural formulae, and non-standard symbols/terms should be avoided as far as possible.

**E.** Length rules in 5.2.9, quoted from the fetched PDFs:

- For a thesis written in Chinese: **中文摘要一般字数为 300 字～1000 字，如遇特殊需要字数可略多。**
- Keywords: **每篇论文应选取 3 个～8 个关键词**, placed on a new line below the abstract, in a distinctive typeface; they should be professional terms that appear in the thesis. Keyword writing shall conform to **CY/T 173**.
- An English abstract is recommended for international communication, starting on a new page after the Chinese abstract, with content corresponding to the Chinese abstract, and English keywords corresponding to the Chinese keywords.
- For a thesis written in a foreign language: write the foreign-language abstract in that language; **in addition, a Chinese abstract is required**, placed after the foreign-language abstract, with Chinese keywords. **为能完整描述学位论文的主要内容，中文摘要宜不少于 5000 字.**

**E.** Language clause in Ch. 4 (overall requirements): if the language of instruction is a foreign language, the thesis may be written in that language, but it should have a Chinese title and a Chinese abstract.

**S.** “300–1000 characters for a Chinese-language thesis” is the national default, with an explicit “may be slightly longer if specially needed.” The 5000-character floor applies to the **Chinese abstract of a foreign-language thesis**, not to ordinary Chinese PhD abstracts. School manuals often set a narrower band inside or even outside this default; those are local overlays, not replacements of the national clause (see §3 and the disagreements list).

### 1.5 Appendix A — 学位论文的构成要素 (normative)

**E.** Clause 5.1: a thesis should comprise six parts — 前置部分, 正文部分, 参考文献, 附录, 索引, 结尾部分 — and the specific elements shall conform to **Table A.1**.

**E.** Table A.1, reconstructed from the Suda PDF extraction (Hunan layout is consistent but typographically broken). “必备性” values are as printed:

| 部分的名称 | 组成 | 必备性 | 功能 (as printed) |
| --- | --- | --- | --- |
| 前置部分 | 封面 | 可选 | 提供基本信息 |
| 前置部分 | 封二 | 可选 | 提供版权信息 |
| 前置部分 | 题名页 | **必备** | 提供题名和作者信息 |
| 前置部分 | 英文题名页 | 可选 | 提供英文题名信息 |
| 前置部分 | 勘误页 | 有则必备 | 提供勘误信息 |
| 前置部分 | 原创性声明 | **必备** | 提供声明信息 |
| 前置部分 | 使用授权说明 | **必备** | 提供使用授权信息 |
| 前置部分 | 致谢 | 有则必备 | 提供致谢信息 |
| 前置部分 | 摘要页 | **必备** | 提供摘要信息 |
| 前置部分 | 序言或前言 | 有则必备 | 内容 |
| 前置部分 | 目次页 | **必备** | 内容 |
| 前置部分 | 插图和附表清单 | 有则必备 | 内容 |
| 前置部分 | 缩写和符号清单 | 有则必备 | 内容 |
| 前置部分 | 术语表 | 有则必备 | 内容 |
| 正文部分 | 引言（绪论） | **必备** | 内容 |
| 正文部分 | 主体 | **必备** | 内容 |
| 正文部分 | 结论 | **必备** | 内容 |
| 参考文献 | 参考文献 | **必备** | 内容 |
| 附录 | 附录 | 有则必备 | 内容 |
| 索引 | 索引 | 可选 | 提供内容的检索信息 |
| 结尾部分 | 作者简历 | 可选 | 提供补充作者信息 |
| 结尾部分 | 其他 | 可选 | 提供补充其他信息 |

**E.** Other 2025 changes recorded in the foreword and useful for ThesisForge encoding: the old “学位论文结构图” became this element table; “正文编排格式” became “章节编排示例”; reference examples were updated (monographs, patents) and electronic journal / e-book examples were added; the 2006 dataset appendix was deleted. Acknowledgements may stand alone before the abstract, or be placed in the preface or afterword (5.2.8). The conclusion (5.3.7) is the final, overall conclusion, not a simple repetition of chapter summaries; it should include the core claims, state limitations, and offer suggestions for future work; if a conclusion cannot be drawn, a necessary discussion may replace it. References shall follow GB/T 7714 and start on a new page; all cited works must appear in the reference list; unread-but-useful works may go in an appendix titled “参考书目.”


---

## 2. GB/T 7714—2025 (cleaner text, worked examples, 2015 vs 2025 delta for CS theses)

### 2.1 Sources obtained

**E.** The 20.2 MB OCR PDF flagged in Round 1 was downloaded: https://publishmedia.cbpt.cnki.net/portal/minio/webs/jjkj/media/web/2026/07/27/GBT%207714%E4%B8%802025%E4%BF%A1%E6%81%AF%E4%B8%8E%E6%96%87%E7%8C%AE%20%20%E5%8F%82%E8%80%83%E6%96%87%E7%8C%AE%E8%91%97%E5%BD%95%E8%A7%84%E5%88%99_OCR.pdf — 45 pages, produced by ABBYY FineReader 14 (CreationDate 2026-05-19). The OCR is usable for confirmation but typographically messy (broken punctuation, “&14” for “8.14”).

**E.** A much cleaner running text, apparently a full transcription of the same standard, was successfully fetched: https://kanhao100.github.io/GBT7714-2025-bst/standards/gbt7714-2025.html. This is a **third-party** HTML edition (GBT7714-2025-bst project), not a SAMR official page. Clauses and examples used below were cross-checked against the OCR PDF for the CS-relevant types (datasets, preprints, PIDs, computer programs). Where the two disagree, the disagreement is recorded.

**U.** Official SAMR/openstd full-text pages were not obtained. Official records remain located only: https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14 and https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F.

Cover data (HTML + OCR): replaces GB/T 7714—2015; **发布 2025-12-02，实施 2026-07-01**; non-library-catalog use; drafters include 黄如花, 刘霞, and 陈浩元, 曾建勋, et al.

### 2.2 Terms and general rules that matter for CS/通信/器件 theses

**E.** New or rewritten terms (Ch. 3):

- 3.6 数据集: “相似或相关数据合乎逻辑的集合或分组。” Note: usually used as a record or for research.
- 3.10 永久标识符 (PID): a unique identifier that provides access independent of the object’s physical location or current ownership. Note: includes **DOI**, **URN**, etc. (source note: GB/T 4894—2024, 3.2.5.25, modified).
- 3.11 预印本: “尚未通过同行评审但仍可广泛使用的文稿。”

**E.** 7.9 Permanent identifiers:

- 7.9.1 If the access path already contains the PID, the PID need not be repeated. Examples include a Wiley URL that already embeds the DOI, and a University of Helsinki thesis URL that is already a URN.
- 7.9.2 If the access path does not contain the PID, the PID may be recorded as in the source (DOI example; a UCAS thesis example in 8.7 uses **CSTR**).

**E.** 7.6 Dates for electronic resources (created / published or modified, and date cited) use `YYYY-MM-DD`. 7.1.1 Latin personal names: surname in full, **initial capital only** (example: `Einstein A`), not all-caps surnames. 7.7: if there is no page number but there is an article number, record the article number in the page position.

**S.** For CS theses this means: arXiv / bioRxiv / ChinaXiv items are no longer forced into `[EB/OL]` or `[J/OL]`; datasets have a first-class type; DOIs, URNs, and CSTR-style identifiers are all in scope; Latin surnames in ALL CAPS are a 2015-era habit that 2025 explicitly moves away from.

### 2.3 Worked examples: preprints, datasets, software/programs, PIDs

**E. Datasets (8.14).** Format:

`主要责任者. 题名: 其他题名信息[文献类型标识/文献载体标识]. 版本. 发布平台(发布或修改日期)[引用日期]. 获取和访问路径. 永久标识符.`

Examples from 8.14.3 / Appendix B.13 include:

- `[DS/OL]` with version `V1.0`, a Chinese data centre, a date pair, and a URL that itself contains a **CSTR**.
- `[DS/OL]` with a DOI after the URL (`DOI:10.12041/geodata.58691800703558.ver1.db`).
- `IHME. Global burden of disease study 2019 (GBD 2019) data resources[DS/OL]. Global Health Data Exchange (2021) [2025-07-15]. https://ghdx.healthdata.org/gbd-2019.`

Citation date is **必备** for datasets (Table 14). Release platform is optional for electronic resources.

**E. Preprints (8.15).** Format:

`主要责任者. 题名: 其他题名信息[文献类型标识/文献载体标识]. 版本. 出版平台(创建或修改日期)[引用日期]. 获取和访问路径. 永久标识符.`

Examples from 8.15.2 / Appendix B.14 include:

- ChinaXiv and PSSXiv items with `[PP/OL]` and **CSTR**.
- `Jenkins S D, Ruostekoski J. Controlled manipulation of light by cooperative response of atoms in an optical lattice[PP/OL]. V2. arXiv (2012-03-18) [2020-06-24]. https://doi.org/10.48550/arXiv.1112.6136.`
- A bioRxiv item with `https://doi.org/10.1101/029983`.

**E. Software / computer programs.** The standard does **not** add a dedicated “software” chapter. Appendix A.1 still lists **计算机程序 = CP** (and 数据库 = DB). In clause 8.11.3 (webpage examples), both the HTML transcription and the OCR PDF give:

- `[5] Zotero. [Zotero download][CP/OL]. [2024-04-08]. https://www.zotero.org/download/.`

**Disagreement (internal to the HTML transcription):** Appendix B.10 example [13] of the same HTML edition records the same Zotero item as `[EB/OL]`. The OCR is messy in the appendix, but 8.11.3 in both sources uses `[CP/OL]`. **S.** Until an official typeset copy is compared, ThesisForge should: (i) treat **CP** as the type code for computer programs; (ii) prefer `[CP/OL]` when the cited object is the program/download itself; (iii) flag the B.10 `[EB/OL]` variant as an unresolved internal inconsistency, not as a second official rule.

**E.** Other CS-relevant examples already in the standard: an IEEE conference paper as `[C/OL]` with DOI (8.6.3 ex. [2]); a CVPR paper as `[C/OL]` (8.6.3 ex. [3]); a UCAS dissertation with `CSTR:` (8.7.2 ex. [3]); an article-number journal paper (7.7 ex. 6); an online-first journal article recorded by date before the version-of-record volume/issue appears (8.5.3 ex. [4] vs [5]).

### 2.4 2015 vs 2025 delta relevant to CS theses

**E.** The official “main technical changes” list in the 2025 foreword (items a–o) includes, as they bear on CS writing:

- New terms and types: 会议录, 数据集, 永久标识符, 预印本; type code **PP**; carrier code **MM** (microform); **EB** is redefined as 网站、网页 (no longer a vague “electronic bulletin” label in the type table).
- “数字对象唯一标识符 (DOI)” generalized to **永久标识符 (PID)**.
- “公告日期、更新日期、引用日期” renamed to “创建/发布或修改日期、引用日期.”
- Monograph to 图书; 舆图 to 地图.
- Electronic-resource rules are no longer a single catch-all chapter; they are folded into each type (so `[J/OL]`, `[DS/OL]`, `[PP/OL]`, `[D/OL]`, `[C/OL]` each have their own required/optional elements).
- Dissertations, reports, standards, websites, archives, maps, datasets, and preprints now have explicit item tables and formats.

**S. Practical delta sheet for a 计算机应用技术 thesis** (derived only from the official change list plus the clause tables, not from unofficial commentary sites):

| Topic | 2015 practice (as the 2025 foreword describes it) | 2025 rule to encode |
| --- | --- | --- |
| arXiv / ChinaXiv / bioRxiv | No dedicated type; typically forced into EB or J/OL | `[PP/OL]` + platform + created/modified date + citation date + URL/PID |
| Dataset (GitHub release, data centre, Zenodo, etc.) | Type code DS existed, but no 8.x format | 8.14 format; citation date mandatory; PID optional if not already in the URL |
| Software | Type code CP exists | Still CP; no dedicated chapter; example uses `[CP/OL]` for a download page |
| DOI / CSTR / URN | DOI-centred | PID family; do not repeat a PID already inside the URL |
| Latin surnames | 2015-era tools often used ALL CAPS | Initial capital only (`Caplan P`, not `CAPLAN P`) |
| Citation dates | Broadly used on many electronic items | Still mandatory for websites, datasets, and preprints (Tables 10, 11, 14, 15) |
| Theses as cited works | Present | 8.7 format; 引文页码 is 有则必备; online theses get URL and optional PID/CSTR |
| Conference papers not in a formal book | Weaker typification | 8.6.3 format without book-style imprint when the item is not published as a book/serial |

Unofficial commentaries (e.g. https://kanhao100.github.io/GBT7714-2025-bst/docs/2015-vs-2025.html, https://thesis.org.cn/changes/) repeat many of these points and add claims such as “citation dates cancelled for non-network types” or “dissertations must now carry page numbers for the first time.” Those extra claims were **not** independently verified against a clean official typeset copy beyond what the clause tables already show, and are **U** if used as bright-line rules.


---

## 3. Elite-university / EE-CS school manuals (Tsinghua, PKU, UCAS, BUPT / Xidian / SEU)

### 3.1 Tsinghua University (fetched)

**E.** Official current writing guide downloaded: 《清华大学研究生学位论文写作指南（试行）》2025年3月修订, https://www.tsinghua.edu.cn/__local/A/A3/A8/948F85164440B1073B73B3BAA9D_1AF5B731_137B8F.pdf (linked from https://www.tsinghua.edu.cn/info/1492/122142.htm). 53 pages. Local copy: `round2-sources/tsinghua-thesis-guide-202503.pdf`.

Verified rules (not typography unless stated in the guide):

- **Standard stack cited by Tsinghua itself (still the old editions):** GB/T 7713.1—2006, GB/T 7714—2015, and GB/T 16159—2012, plus school regulations. This is a concrete illustration of the Round-1 finding that school templates lag the 2025 national stack.
- **Length:** no school-wide page/word floor in the guide. The guide says length “无明确要求,” and that it should match the research; it explicitly says it is acceptable to write a short, tight thesis rather than pad the text. Liberal-arts theses are noted as often 6–10 万字, but that is descriptive, not a CS rule.
- **Abstract length:** 中文摘要 **800～1000 字，以一页为宜**; 英文摘要 **300～400 词**. Keywords: **3–5**.
- **Abstract content:** 3–5 sentences on background/purpose, then methods/results/conclusions; **highlight innovation and practical value**; no first-person, no figures/tables/citations/formulae in the abstract (the 5000-character foreign-language-thesis rule of 7713.1—2025 is not in this 2025-03 Tsinghua guide).
- **创新点 placement:** 创新点 is a **required section at the end of Chapter 1 (绪论)**. The guide says it is “必要组成部分,” and that many reviewers/committees start here. Each point should state the **existing problem, the proposed method, and the achieved effect**, and should be **supported by publications or other outcomes**. The same themes should already have been introduced as a 3–5-item “拟解决的科学问题” list earlier in Chapter 1; 创新点 then answers those problems, rather than appearing as an unheralded list.
- **Recommended CS/engineering body order (示例):** 绪论 → 相关工作 / 文献综述 (may be part of Ch. 1 or a separate chapter) → 理论/算法/系统/方法设计 → 实验与结果分析 (or 实验设计 / 系统实现 / 仿真实验) → 结论与展望. After 创新点, Chapter 1 should end with a 论文结构说明. Literature review should be critical, not a pile of abstracts, and should close with a **research-gap** statement. Chapter 2 is often “related work” rather than the first method chapter.
- **Typography verified in this guide:** body 小四号; 1.25–1.5 line spacing; 段首缩进 2 字符 (not 2 汉字 explicitly as a different rule); heading levels 三号 / 四号 / 小四; page numbers 五号, bottom centre, roman vs arabic; main text typically starts around page 11 after front matter; header “清华大学××××学位论文” 小五号. These are school rules, not national typography.
- **Reference style:** GB/T 7714—**2015**, numeric or author-year; **一般不少于 100 篇，其中近 5 年文献不少于 1/3**; prefer journals and formal conference papers; cap informal web sources.
- **Other:** 隐名评阅 (盲审) copies omit supervisor name, acknowledgements, and identifying publications; the 独创性声明 / 授权书 use school wording; a 指导教师评语 may appear after the authorization; reproducibility language appears in the experimental-chapter advice (enough detail for a 本领域专业人士 to repeat the work).

### 3.2 Peking University (fetched)

**E.** Official writing guide downloaded: 《北京大学研究生学位论文写作指南》, 研究生院, **2018年2月28日**, https://xkb.pku.edu.cn/docs/2019-10/20191016174319619362.pdf (page title dates the file as 2019-10; the cover date is 2018-02-28). Local copy: `round2-sources/pku-thesis-guide-2019.pdf`.

Verified rules:

- **Cited national standards are even older:** GB 7713—**1987** and GB/T 7714—**2005**. The School of Chinese as a Second Language is given as an example of a unit that still used GB/T 7713—1987 as of this guide.
- **Abstract length:** 博士 **800–1000 字**, 硕士 **约 600 字**; 中英文摘要以 **1 页**为宜, 最多 **2 页**; 英文摘要 **300–400 词（博士）**.
- **Abstract content:** 独立成篇; 目的、方法、结果、结论; 突出创新性结果和结论; 不用图表、公式、非公知符号; 不用第一人称. Keywords **3–5**.
- **创新点 placement:** Chapter 1 must include 论文的主要创新点; later chapters may have a short mid-chapter 小结. The conclusion restates core results, innovation, limitations, and future work.
- **Typography verified:** A4; 上空 3.8 cm, 下 3.8, 左 3.4, 右 3.2 (binding 0.5 cm, so 3.4+0.5); header 2.8 cm 宋体小五, footer 2.5 cm; body 小四 宋体 / Times New Roman, 固定行距 **20 磅**, 段首缩进 2 字符; 章标题 三号黑体居中; 图题表题 五号黑体.
- **References:** 博士 **不少于 80 篇（特殊学科除外）**, 硕士 **不少于 40 篇**; **近五年文献不少于 1/3**. Conference papers are acceptable in some fields. The guide also states a controversial circulation rule: a thesis may cite literature **“一般应是从公开渠道获取的，不引用非公开出版物”** — this is a school-era formulation, not a 7714—2025 rule, and is recorded as a local overlay.
- The guide itself notes that academic norms were still being revised after 学位条例修订 and 学术规范相关文件, and that **具体规定以各培养单位通知为准**.

### 3.3 UCAS (not fully fetched this round)

**U.** The previously used engineering-style PDF, https://ce.ucas.ac.cn/index.php/zh-CN/xsyjssgl/gzzd/index.php?option=com_content&view=article&id=2516, returned **HTTP 500** when downloaded. The older `https://las.cas.cn/...` link had expired SSL in earlier attempts and HTTP 500 in Round 1.

Search-index snippets (not full text, therefore **U**, not to be encoded as numbers) still suggest an older UCAS “编写规定 / 撰写指南2021”: 硕士 500–1000 字 / 博士 1000–1500 字, 英文约 300–600 词, 关键词 3–5; 博士参考文献不少于 80 篇. **Do not treat these figures as verified in Round 2.** They remain a Round-3 fetch target (library.ucas.ac.cn or a current 学位办公室 notice).

### 3.4 BUPT (not fetched)

**U.** https://grs.bupt.edu.cn/info/1035/3071.htm returned **HTTP 412** (download blocked). A BUPT “写作手册” listing appears at https://ss.bupt.edu.cn/__local/4/EF/C3/9F29E101C6154126A16EF5B6689_AC6C57CE_12939C.docx, also not obtained. BUPT typography and abstract rules remain **U**.

### 3.5 Xidian (partial: 2025 review form and 2014 writing handbook)

**E / U mixed.** A current *writing* handbook PDF was not obtained. Two official pages were fetched:

- 2025-04-28 评阅送审通知, https://gr.xidian.edu.cn/info/1073/13806.htm (**E**, HTML): 学术学位 doctoral 评阅书 is organized as 选题 / 创新性 / 科研能力 / 规范性 / 不足, with a **百分制** and the four weights **20% / 20% / 50% / 10%** (不足 is narrative). Reviewers also answer yes/no plus comments on 创新点是否明确、凝练. 工程类 professional doctorates use a different form: 选题 / 创新性 / 应用价值 / 科研能力 / 规范性 / 不足. The same notice describes 论文评阅 (学位论文质量监督) and 答辩资格审查, and it lists 08 电子信息 among the professional-doctorate categories.
- 2014-04-01 writing-handbook notice, https://gr.xidian.edu.cn/info/1069/1878.htm (**E** as a historical official page, **U** as a current rule): 简短摘要 **300 字 / 100 词**; 详细摘要 **博士 3000 汉字 / 1000 词, 硕士 1000 汉字 / 500 词**; typography in the page text includes 章标题 黑体三号居中, 正文 宋体小四, 页边距 上2.7 / 下2.7 / 左3.5 / 右2.7 cm, 页眉 2.2 / 页脚 2.0, 章标题上空 2.4 cm / 下空 1.8 cm, and “理论分析 + 实验验证” as the science/engineering body pattern. Because the handbook is from **2014**, these typography and “detailed abstract” figures must not be encoded as 2025 Xidian defaults without a later official confirmation.

### 3.6 Southeast University (fetched)

**E.** Current format specification downloaded: 《东南大学研究生学位论文格式规定》, https://seugs.seu.edu.cn/_upload/article/files/c4/04/6784c6fe4c7c8096aaf8d68cc248/644d870b-2c8c-4c4d-bc7a-cf71061b536e.pdf. Local copy: `round2-sources/seu-thesis-format.pdf`.

Verified rules:

- Abstract: **中文约 500 个汉字，英文约 200–300 个实词**; 中英文内容一致; 目的、方法、结果、结论, 重点是结果和结论; no figures, tables, or unusual abbreviations; do not repeat the title. Keywords **3–8**, Chinese and English in correspondence, placed two lines below the abstract, **左对齐**. The English abstract starts on a **new page**.
- **创新点 placement in this document is not a separate required Ch. 1 heading.** The conclusion (最后一章) should be explicit, concentrated, and complete, **着重阐述作者的创造性工作及所取得的研究成果**, and may outline research that still needs to be done. So SEU encodes “creative work” primarily in the conclusion, whereas Tsinghua and PKU require a Chapter-1 创新点 list.
- References follow GB/T 7714 (edition not named in the extracted passages used here).
- Typography verified: A4; 页边距 上、下 3.0 cm, 左 3.0, 右 2.5; 页眉 2.2 / 页脚 2.0; 正文 宋体小四, 两端对齐, 段首缩进 2 个汉字符, 固定值行距 **20 磅**; 章标题 黑体小二居中, 上下各空 1 行; 节标题 黑体四号 / 小四左对齐; 页码 五号, 前言部分罗马数字, 正文阿拉伯数字, 均底部居中; 封面中文学位论文标题 黑体一号; 论文题目不超过 **20 字**（过长用副标题）; 分类号 and 密级 at the top of the cover.
- The specified reference stack in SEU’s opening clauses was not fully re-typed here; Round 3 should record whether SEU has updated 7713.1 / 7714 citations to the 2025 editions.

### 3.7 Cross-school comparison (**S**)

| Item | GB/T 7713.1—2025 | Tsinghua 2025-03 | PKU 2018/2019 | SEU (fetched) | Xidian 2014 page (historical) | UCAS / BUPT |
| --- | --- | --- | --- | --- | --- | --- |
| 中文摘要 | 300–1000 字（特殊可略多）; 外文论文的中文摘要宜不少于 5000 字 | 800–1000 字, 一页为宜 | 博士 800–1000, 硕士约 600, 最多 2 页 | 约 500 汉字 | 简短约 300; 详细 博士 3000 / 硕士 1000 | **U** |
| 英文摘要 | 与中文对应 | 300–400 词 | 博士 300–400 词 | 约 200–300 实词 | 简短 100 词; 详细 博士 1000 / 硕士 500 | **U** |
| 关键词 | 3–8, CY/T 173 | 3–5 | 3–5 | 3–8 | not re-verified | **U** |
| 创新点位置 | not a named mandatory heading in Table A.1 | **必备, 第一章末** | 第一章须写主要创新点 | 创造性工作 mainly in 结论 | not in the 2014 page extract | **U** |
| Cited GB stack | 7713.1—2025, 7714—2025 (from 2026) | still 7713.1—2006, 7714—2015 | still 7713—1987, 7714—2005 | 7714 cited, edition **U** | 2014-era | **U** |

**S.** ThesisForge must treat school abstract windows as **overlays** on 7713.1—2025, not as replacements. A Tsinghua CS PhD abstract of 800–1000 characters is inside the national band. An SEU abstract of “约 500 汉字” is also inside the national 300–1000 band, but is tighter. Xidian’s 2014 “详细摘要 3000 字” is a different genre (a long abstract booklet) and must not be mixed with the short abstract page. The 5000-character floor is only for the Chinese abstract of a **foreign-language** thesis under the 2025 national standard; none of the fetched school manuals has yet absorbed that clause.


---

## 4. 盲审 / 评阅书 templates and the MOE professional-doctorate quality standard

### 4.1 MOE / 国务院学位委员会 工程类专业学位研究生学位论文质量标准

**E.** The MOE news item that Round 1 located but did not fetch was fetched in this round: http://www.moe.gov.cn/jyb_xwfb/s7600/202410/t20241030_1159900.html (2024-10-30). It reports the issuance of 学位办〔2024〕18号, 《关于转发〈工程类专业学位研究生学位论文质量标准（试行）〉的通知》, drafted over three years by the engineering professional-degree education steering committees, and effective for quality control, review, and evaluation.

**E.** Authoritative full text of the standard was obtained from Xidian’s official reprint of the same notice and attachment: https://gr.xidian.edu.cn/info/1073/13116.htm (2024-11-04). The standard covers **11** engineering professional-degree categories, including **电子信息**. It is a quality standard for professional-degree theses, not a replacement of GB/T 7713.1.

**E.** Document-type menu (the student chooses one, with the supervisor): 产品设计, 工程规划或工程设计, 专题研究, 调研报告, 案例分析, 发明专利, 管理或技术方案, 技术标准, 工程软件, 产品研发, 工艺研发, 工程/项目管理. For 电子信息, typical types include 产品设计 / 产品研发, 专题研究, 工程软件, 技术方案, 专利, 技术标准.

**E.** Mandatory thesis structure (eight parts, in order):

1. 封面、题名页 (Cover and Title Page) — 中英文题目、作者、导师、专业学位类别、领域、日期; 专业学位类别 and 领域 must be correct.
2. 原创性声明、使用授权、版权、保密 (Declarations and Copyright) — 独创性/原创性声明、使用授权、版权约定、保密评审申请 (如需); signatures complete.
3. 摘要 (Abstract) — 中英文; 工作背景或问题、方法、结果及结论; 突出实际贡献和应用价值; 关键词准确、专业.
4. 目录 (Contents) — 三级标题为宜, 页码准确.
5. 主体 (Main Body) — 见 the four-chapter outline below.
6. 参考文献 (References) — 充分、准确, 格式规范, 引文真实可追溯.
7. 致谢 (Acknowledgements).
8. 必要的附录 (Appendices if needed) — 图纸、源码、数据、标准文本, etc.

**E.** Required main-body outline:

- 绪论: 工程或产业背景, 问题来源与研究意义, 国内外现状, **研究目标, 主要研究内容**.
- 研究或设计的主要内容: 需求、技术路线、总体方案, 理论/方法/技术/设计/实现过程; figures, tables, and data complete and clearly annotated.
- 试验（或仿真、分析等）: 方案合理, 过程可追溯, 数据真实, 结果可信; 达到预期或有合理偏差分析.
- 总结与展望: 工作与贡献, 应用价值, 不足与后续建议.

**E.** Quality dimensions used in review: 政治方向; 选题（来源于实际、目标明确、难度与工作量匹配）; 内容（方案合理、方法正确、工作饱满）; 创新性与成果（针对实际问题的新思想、新方法、新技术、新工艺, 或集成创新, 或明显的应用效果）; 规范性（结构、图表、参考文献、术语）; 撰写质量（逻辑清楚, 用语规范, 可读）. The standard also requires 全过程质量控制 (proposal, mid-term, pre-defence, defence) and 学术诚信 (no fabrication, falsification, plagiarism, ghostwriting).

**S.** For ThesisForge, an 电子信息 professional doctorate should be able to switch from the academic-degree “one-story + 创新点” template to this eight-part / four-chapter body, with 创新性 framed as engineering application or integration, not only as a scientific gap. Academic CS PhDs should not be forced into this professional-degree outline.

### 4.2 Review-form evidence actually fetched

**E. Xidian 2025 academic-doctorate score table** (https://gr.xidian.edu.cn/info/1073/13806.htm): 选题 20% / 创新性 20% / 科研能力 50% / 规范性 10%, plus a narrative 不足, plus a yes/no judgement on whether 创新点 are 明确、凝练. Professional-doctorate forms add 应用价值 as a separate dimension. This is an operationalization of “expert rigor”: reviewers are asked whether the claimed points are clear and compact, not whether every sentence is hedged.

**E. Fudan University 博士学位论文评阅书** downloaded: https://gsas.fudan.edu.cn/jzg/_upload/tpl/08/4d/2125/template2125/files/%E5%8D%9A%E5%A3%AB%E5%AD%A6%E4%BD%8D%E8%AE%BA%E6%96%87%E8%AF%84%E9%98%85%E4%B9%A6.pdf. Local copy: `round2-sources/fudan-review-form.pdf`. The form asks the reviewer to list **至少三项主要创新点或贡献** (至少 3 项, 或 无). Separate scored items include: 选题的前沿性和创新性; 论文的创新性; 论文的学术性或应用价值; 论文体现的理论基础、专门知识及科学研究能力; 论文的条理性、逻辑性及文笔; plus 总体评价 and 是否同意答辩. This is a humanities-and-sciences-wide Fudan form, not EE-specific, but it confirms the “state three compact contributions” review habit.

**U.** A Zhejiang University CS-college doctoral review form (https://cs.zju.edu.cn/_upload/article/files/c6/1b/ce73afe1471caa5aab9e581d4ae4/e496d7db-ab58-4cdc-81d7-5b77b537ec1e.pdf) returned **HTTP 500**. A Tsinghua 隐名评阅 description in the 2025 writing guide (omitting supervisor, acknowledgements, and identifying papers) is procedural, not a filled-in score sheet.

**S.** Encode a default academic-degree review checklist with four blocks — 选题, 创新点是否明确凝练, 论证与证据（含实验/仿真/验证）, 规范性与表述 — and a professional-degree variant that adds 应用价值 and maps onto 学位办〔2024〕18号. Do not invent a national percentage table; when a school table exists (Xidian 20/20/50/10), use that school’s weights.

---

## 5. Chinese journal author guides (计算机学报, 软件学报, 电子学报, 通信学报, 半导体学报)

All numeric limits below are from pages or PDFs fetched or downloaded in this round, unless marked **U**.

### 5.1 计算机学报 (Journal of Computer Science and Technology / 计算机学报)

**E.** Author notice and two official PDFs:

- https://www.cjc.ict.ac.cn/zzjsyy/index_2.htm?mod=info&act=view&id=34
- 2025 年年审通知 PDF: https://cjc.ict.ac.cn/attached/file/20260121/20260121204611_758.pdf
- 稿件撰写要求 PDF: https://cjc.ict.ac.cn/attached/file/20231126/20231126173911_237.pdf

Verified rules:

- Scope: 计算机科学与技术 and 交叉领域; 创新性研究成果; 中英文均可.
- **中文稿一般不超过 1.2 万字（约 10 页）; 综述不超过 2 万字; 短文/技术报告/学术来鸿约 0.8 万字（约 6 页）.** English papers follow JCST length practice (the Chinese site defers to JCST, exact English page caps **U** here).
- **摘要 200–300 字**, 英语 200–300 词; 综述摘要可稍长. Abstract should include 研究目的、方法、结果、结论, and **体现创新性**. Keywords **3–8**.
- Structure: 引言应说明研究背景、意义、国内外现状、本文工作及创新点; 结论避免简单重复结果, 应概括、升华, 可给后续工作. 图题表题中英文对照; 公式按章编号.
- References: **GB/T 7714**, numbered in citation order; **近五年文献应占一定比例**; 未正式发表的文献一般不列; 尽可能引用原始文献. English papers: IEEE / JCST style.
- Review: 初审约 **15 天**; 外审 **1–2 个月**（可延）; 录用到出版约 **6–10 个月**. 一稿多投 is forbidden. A 2024–2025 integrity notice forbids 第三方代写代投, 伪造审稿人, 不当署名, etc. Post-review rejected resubmissions need an explanation of revisions.

### 5.2 软件学报 (Journal of Software)

**E.** Full 投稿指南 fetched: http://www.jos.org.cn/ch/reader/news_content.aspx?id=20251 (also linked as “修改稿件撰写要求及常见问题”). Additional pages: 稿件录用标准 http://www.jos.org.cn/news/news.aspx?id=20dc1b96-8ca8-4546-a4d1-43ce8e2f1b5a; 投稿模板信息 on the same site.

Verified rules:

- Scope: 计算机软件与理论, 系统软件, 软件工程, 数据/知识, 网络, 信息安全, 相关交叉.
- **投稿时暂无页数限制; 出版时一般 10–18 页.** The official 投稿模板 is 18 pages “以便作者掌握篇幅.”
- **中文摘要 200–300 字，英文 100–150 词.** Keywords: **中文 4–6, 英文 3–5**, with correspondence. CLC / 中图分类号 required.
- **创新性 / 要点:** 投稿必须填写 **中英文创新点** (explicit form fields, not just an implicit abstract claim). The 录用标准 emphasizes 创新性, 科学性, 实用性, and 可读性. 引言应给出问题、相关工作、本文工作与创新. 结论对创新进行概括, 指出不足和未来工作.
- Structure: 引言, 相关工作 (可并入引言或独立成章), 方法/模型/系统, 实验与分析, 结论. 实验须可核对: 数据集、环境、参数、对比方法, 统计分析要充分.
- References: **GB/T 7714**, 顺序编码; 一般 **不少于 20 篇**, 近五年应有相当比例; 作者本人文献不自引过度; 未发表文献不作为正式参考文献. English items keep English typography.
- Review: 初审约 **1 个月**, 外审 **2–3 个月**; 一稿多投 forbidden; 在线投稿.

### 5.3 电子学报 (Acta Electronica Sinica / 电子学报)

**E.** Official pages fetched: 投稿须知 https://www.ejournal.org.cn/CN/column/item104.shtml; 论文模板 https://www.ejournal.org.cn/CN/column/item105.shtml; 期刊介绍 https://www.ejournal.org.cn/CN/column/column11.shtml.

Verified rules:

- Scope: 电子信息科学与工程, including 信息与通信, 信号与信息处理, 计算机, 微电子与固体电子, 电磁场与微波, 电路与系统, etc. 中英文均可.
- **一般不超过 8 页 (约 8000 字); 综述可到 10 页; 研究快报 4 页以内.**
- **中文摘要 200–300 字，英文约 200 词**; 应包括目的、方法、结果、结论, **突出创新点**. Keywords **4–8**.
- 引言: 背景、意义、现状, **本文主要工作和创新点**. 结论: 概括主要结果与创新, 指出不足与展望. 图题表题中英对照.
- References: **GB/T 7714**, 顺序编码; **一般不少于 15 篇**, 近五年应有一定比例. English papers may use IEEE style (the site’s English instructions were not fully re-fetched as a separate PDF; treat IEEE-for-English as **E** only to the extent the Chinese 须知 already says so, otherwise **U**).
- 对基金论文优先; 审稿周期约 **3–6 个月** (site language; not independently timed). 一稿多投 forbidden.

### 5.4 通信学报 (Journal on Communications)

**E.** 投稿须知 fetched: https://www.joconline.com.cn/zh/tougao.shtml and related 写作要求 / 模板 pages on the same host (including https://www.joconline.com.cn and the “论文写作注意事项” material linked there).

Verified rules:

- Scope: 通信与信息领域 学术论文、技术报告、综述.
- **一般 8000 字左右 (约 8 页); 综述可到 10000 字.**
- **中文摘要 200–300 字，英文 150–200 词**; 四要素 (目的、方法、结果、结论), 突出创新和结论; **不要简单重复题名**; **避免“本文”“作者”等第一人称表述** (this conflicts with GB/T 6447—2025’s permission for author-written abstracts to use 本文/我们 — see §12 and the disagreements list).
- Keywords **4–8**, 中英对照; 中图分类号.
- 引言写出背景、问题、相关工作、本文工作和创新点. 结论避免罗列, 要有提炼, 可给后续工作.
- References: **GB/T 7714**, 顺序编码; **一般不少于 20 篇**; 近五年文献应占相当比例; 内部资料、未公开文献不列.
- 图题表题中英对照; 公式按出现顺序或按章编号. 审稿约 **3–6 个月** (site language).

### 5.5 半导体学报 / Journal of Semiconductors

**U.** Official site fetches failed or were insufficient:

- Journal of Semiconductors English site and “Preparing Your Manuscript” (IOP / jos.ac.cn paths, including a previously used PreparingYourManuscript URL) returned **502** or **500** in this round.
- Chinese 半导体学报 pages were not obtained as a stable full 投稿须知.

Search-index remnants (not encoded as rules) suggest an English IOP-style guide (length, highlights, etc.) and a Chinese sister journal, but **all numeric author-guide figures for 半导体学报 are U** until a successful fetch in Round 3. Nearest related **E** items are the IEEE T-ED / EDS materials in §7, which are not a substitute for this journal’s own guide.

### 5.6 Cross-journal card (**S**, from the four fetched guides only)

| Journal | Typical length | Abstract | Keywords | 创新点 mechanism | References |
| --- | --- | --- | --- | --- | --- |
| 计算机学报 | 中文一般 ≤1.2 万字 / 约 10 页; 综述 ≤2 万; 短文约 0.8 万 / 6 页 | 200–300 字 / 200–300 词 | 3–8 | 摘要体现创新; 引言写本文工作及创新点 | GB/T 7714; 近五年应有一定比例 |
| 软件学报 | 投稿不限页; 出版一般 10–18 页 | 200–300 字; 英文 100–150 词 | 中文 4–6, 英文 3–5 | **必须填写中英文创新点** | GB/T 7714; 一般不少于 20 篇 |
| 电子学报 | 一般 ≤8 页 / 约 8000 字; 综述 ≤10; 快报 ≤4 | 200–300 字; 英文约 200 词 | 4–8 | 摘要突出创新点; 引言写主要工作和创新点 | GB/T 7714; 一般不少于 15 篇 |
| 通信学报 | 一般约 8000 字 / 8 页; 综述可到 10000 字 | 200–300 字; 英文 150–200 词; **禁第一人称** | 4–8 | 引言写本文工作和创新点 | GB/T 7714; 一般不少于 20 篇 |
| 半导体学报 | **U** | **U** | **U** | **U** | **U** |

**S.** ThesisForge journal mode should load a per-venue card and write the abstract, keyword count, length, and 创新点 field to that card. Do not invent a single “Chinese journal” length. GB/T 7714 is the default Chinese reference style for all four fetched venues; English versions may switch to IEEE.


---

## 6. Communications evaluation: Pawlikowski, Jeong, Lee 2002, and BER / Monte Carlo error estimation

### 6.1 Pawlikowski, Jeong, Lee 2002 (legal PDF fetched)

**E.** Legal university copy downloaded from the authors’ host, as requested: https://akaroa.canterbury.ac.nz/pdf/PJL2002.pdf. The paper is K. Pawlikowski, H.-D.J. Jeong, J.-S.R. Lee, “On credibility of simulation studies of telecommunication networks,” *IEEE Communications Magazine*, vol. 40, no. 1, pp. 132–139, Jan. 2002. Local copy: `round2-sources/pjl2002.pdf`.

Operational procedures actually stated in the paper (no event-count numbers invented):

- The paper’s starting claim is that a large fraction of published teletraffic/network simulation studies in the late 1990s were not statistically credible, mainly because they used arbitrary run lengths and reported no precision.
- **Do not fix the simulation run length in advance.** Use **sequential** simulation: continue until a precision criterion is met.
- **Precision is defined as relative error**, i.e. the half-width of a confidence interval divided by the point estimate, at a stated confidence level (typical textbook CI construction; the paper discusses 95% confidence intervals in its exposition). Stop when the relative error falls below a **pre-declared** threshold. The paper argues for tight, pre-declared accuracy rather than “long enough” runs.
- **Transient / warm-up removal is mandatory** for steady-state measures. The paper discusses initialization bias and refers to well-known transient-deletion and batch methods; it does not, in the pages extracted, anoint a single numeric warm-up rule (such as “discard the first N packets”). **U** any invented warm-up packet count.
- **Independent replications** (or an equivalent method for constructing a valid CI: batch means, regenerative methods, etc.) are required so that the CI is statistically meaningful. One long arbitrary run with no interval is treated as inadequate.
- **Random-number issues:** use well-tested generators and independent streams; do not seed carelessly so that model variants share accidental correlation.
- **Report**, at minimum: the estimated performance measure, the **confidence interval or relative error**, the confidence level, the treatment of transients, and enough workload/model detail for repetition.
- The paper is about **stochastic discrete-event simulation of networks**, not about Monte Carlo bit-error counting as such. It must not be cited as a source of BER event-count rules.

**S.** ThesisForge communications-simulation plans should implement: declare the performance metrics and the relative-error / CI target *before* running; sequential stopping; transient deletion with the method named; independent replications or another CI method named; generator/stream disclosure; no “we ran it for a long time” as a substitute. Leave specific ε (e.g. 5% vs 1%) to the author or the venue, unless a later fetched source sets one.

### 6.2 BER / Monte Carlo error-estimation source

**U.** A clean, legal, full-text source that states a numeric “number of error events” rule was **not** obtained in this round.

- M. C. Jeruchim, “Techniques for estimating the bit error rate in the simulation of digital communication systems,” *IEEE Journal on Selected Areas in Communications*, vol. 2, no. 1, pp. 153–170, Jan. 1984, is the classical reference. IEEE Xplore / DOI https://doi.org/10.1109/JSAC.1984.1146031 is paywalled; it was **not** downloaded from pirate mirrors.
- Other commonly cited tutorial pages and course notes were not treated as primary sources for a numeric rule.

**S / constraint for v2:** ThesisForge may describe, as a qualitative method, that Monte Carlo BER is an estimator whose uncertainty shrinks as the number of observed error events grows, and that authors should report the counting window, the number of observed errors, and a confidence statement. **It must not encode a specific folklore number** (including the widely repeated “100 error events” rule of thumb) until a primary, legally obtained source that actually states that number is in hand. Round 3 should try: an IEEE-accessible copy of Jeruchim 1984, or an open tutorial that derives the CI from a binomial / Poisson model and states its own assumptions.

---

## 7. Semiconductor / electron-device venues (EDS touchstones, T-ED simulation-only policy, TCAS)

### 7.1 EDS TouCHSTONES (fetched)

**E.** Official PDF downloaded: https://eds.ieee.org/images/files/Publications/touchstones.pdf. Local copy: `round2-sources/eds-touchstones.pdf`.

The document is a set of **reviewer/author touchstones** for IEEE Electron Device Society journals (it is used around *IEEE Transactions on Electron Devices* and related EDS titles). Extracted expectations, without inventing a scoring rubric:

- A paper should make a **clear technical contribution** (new device, mechanism, model, process, or a substantial, non-incremental advance).
- Claims must be **supported by evidence** commensurate with the claim: measurement, simulation, or both, with methods disclosed at a repeatable level.
- When simulation is used, models, calibration, and limitations should be stated; simulation should not be presented as a drop-in substitute for a physical claim the data do not support.
- Related work and prior art should be treated fairly; over-claiming “first” is discouraged.
- Presentation should be clear: figures readable, units consistent, English adequate for review.

(The PDF’s section headings and bullets should be cited in the skill at the level of these touchstones, not as a hidden numeric checklist the PDF does not contain.)

### 7.2 T-ED policy on simulation-only papers

**E / already established, confirmed where fetched.** Round 1 established that T-ED generally wants **at least partial direct physical validation**. In this round:

- The EDS touchstones PDF is consistent with that stance (evidence must match the claim; simulation alone is not automatically sufficient for a physical-device claim).
- **U / fetch failed:** Giovanni Ghione’s T-ED editorial on simulation-only manuscripts (IEEE Xplore / EDS page previously located) returned **HTTP 403** and was not obtained. The exact editorial wording — including any stated exceptions for purely theoretical or TCAD-methodology papers — remains a Round-3 target.
- Until that editorial is fetched, ThesisForge should keep the Round-1 rule as the default **E** from Round 1, and should not invent additional exceptions. A v2 warning is justified: “for T-ED-class device papers, plan at least partial physical validation; do not promise a simulation-only T-ED submission as if it were standard.”

### 7.3 TCAS-I / TCAS-II: measurement vs simulation

**E.** IEEE CASS / TCAS-II author and call-for-papers pages fetched in this round (TCAS-II “Information for Authors” and a special-issue CFP that discusses experimental results) support the following, at the level of official language actually seen:

- *IEEE Transactions on Circuits and Systems II: Express Briefs* **commonly expects measured results** for circuit papers, i.e. experimental validation is the normal standard for claims about implemented circuits.
- A special-issue call (ISICAS and related CASS events, as reflected on official CFP pages) has in at least one cycle **explicitly barred simulation-only** submissions. That bar is a **special-issue rule**, not automatically a standing TCAS-II bylaw for every paper type; it is recorded as evidence of venue culture, not as a universal TCAS statute.
- TCAS-I (regular papers) similarly emphasizes contribution plus experimental evidence for circuit-implementation claims; a single sentence that “TCAS-I never accepts simulation” was **not** found and must not be invented. Theory / algorithm papers in the circuits-and-systems scope may rely on simulation or analysis when the claim is not an implemented-circuit claim (**S**, cautious).

**U.** Exact current wording of the standing TCAS-I and TCAS-II “Information for Authors” on simulation-only regular papers should be re-fetched as PDFs in Round 3 (pages can rotate). Do not encode a hard “no simulation-only TCAS paper” rule beyond what the special-issue CFP and the “commonly measured” language support.

**S.** Encode three device/circuit experiment tracks: (i) T-ED-class electron devices — measurement, or simulation plus at least partial physical validation; (ii) TCAS circuit implementation — plan measurement; (iii) method-only TCAD / modelling papers — simulation may be the contribution, but then the claim must be about the method, not about an unmeasured fabricated device.

---

## 8. Elsevier CS/engineering guides, ACM Transactions, IEEE Editorial Style Manual

### 8.1 IEEE Editorial Style Manual and Reference Guide (fetched)

**E.** IEEE Editorial Style Manual (effective **29 July 2024**) downloaded from IEEE Author Center: local copy `round2-sources/ieee-editorial-style-manual.pdf`. IEEE Reference Guide also downloaded: `round2-sources/ieee-reference-guide.pdf`. (Author Center entry points: https://ieeeauthorcenter.ieee.org/ and the style-manual / reference-guide PDFs served from that site.)

Verified, non-invented points relevant to ThesisForge:

- IEEE journal/conference papers use **numbered citations in square brackets**, in citation order, typographically as set in the Reference Guide (author initials, abbreviated journal titles, vol., no., pp., month and year, DOI where available).
- The Style Manual governs spelling, hyphenation, SI units, abbreviation of common technical terms, capitalization of titles (IEEE uses a defined headline/sentence style — follow the manual rather than inventing a house style), figure/table captions, and the treatment of displayed mathematics.
- Abstracts: the Manual and Author Center material treat the abstract as a **standalone** summary of purpose, methods, results, and conclusions, **without citations** (and typically without displayed mathematics or informal language). A numeric “abstract word cap” is **venue-specific** and is **not** treated here as a single IEEE-wide number unless a specific society’s guide, fetched separately, states one (**U** as a universal IEEE cap).
- Hedging / tone: the Manual is a style and typography reference, not a rhetoric manual. It does not, in the portions used, provide a graded list of English hedges. Do not invent an “IEEE hedging band” from this document.
- For a 计算机应用技术 thesis that will later be split into IEEE papers, ThesisForge should be able to **switch the reference and typographic layer** from GB/T 7714 to the IEEE Reference Guide without changing the scientific claims.

### 8.2 Elsevier CS / engineering journal guides

**E.** Elsevier Author / Journal guides were consulted via official journal pages (Computer Networks; and the generic Elsevier “Guide for Authors” pattern used by Engineering journals such as Microelectronics Journal). Successfully fetched author-information pages support this common Elsevier CS/engineering pattern:

- Structure typically follows IMRaD plus highlights / graphical abstract when the journal requires them: title, authors, abstract, keywords, highlights (if required), introduction, related work or background, methods, results, discussion, conclusions, acknowledgements, references, appendices / data availability.
- **Highlights**, where required, are short bullet claims of the contribution (Elsevier’s generic guide describes them as a small number of short bullets; **exact word or bullet caps vary by journal** and must be read from that journal’s Guide for Authors). Do not encode a single invented “3–5 highlights of 85 characters” rule unless the specific journal page fetched in a later pass states it for that title.
- Reference style is journal-specific (often a numbered or Harvard/Elsevier style specified in the Guide for Authors, or handled by the production template).
- Data and code availability, conflict of interest, and AI-use disclosure follow Elsevier’s current policy pages; exact wording should be copied from the target journal’s current Guide for Authors at write time.

**U.** A single, fully downloaded “Computer Networks Guide for Authors” PDF with every numeric cap (word count, highlight character limit, etc.) was not archived as a stable local file in this round. v2 should therefore implement Elsevier mode as: “open the target journal’s current Guide for Authors and fill the venue card,” plus the structural pattern above, rather than hard-coding Computer Networks numbers that were not captured.

### 8.3 ACM Transactions (beyond the Publications Board policy)

**U.** An ACM *Transactions on Computer Systems* (TOCS) or *Transactions on Networking* (TON) author guideline page **timed out or failed** in this round (ACM DL / TOCS author page WebFetch timeout). The ACM Publications Board policy was already in scope in Round 1 and is not re-litigated here.

**S.** Until TOCS/TON-specific pages are fetched, ThesisForge may only reuse ACM-wide, already-established policy (contribution-front review, authorship, artefact, simultaneous-submission rules from Round 1). It must not invent TOCS/TON page limits, abstract lengths, or e-system artefact requirements. Round 3 should fetch https://dl.acm.org/journal/tocs (Author Guidelines) and the TON equivalent, plus any current ACM Master Article Template instructions that those journals point to.


---

## 9. ML / AI evaluation subset for 计算机应用技术

### 9.1 Sources obtained

**E.** NeurIPS 2022 Paper Checklist (official): the NeurIPS 2022 (and subsequent) reproducibility / paper checklist, as published on the conference site and in checklist instructions, was used as the community checklist. Entry points include the NeurIPS author-checklist pages (2022 vintage is the commonly cited starting version; later years refine wording but keep the same axes).

**E.** Related community items already in the Round-1 stack and not re-litigated: SIGPLAN empirical-evaluation checklist and Gernot Heiser’s “Systems Research — What We Want to Hear” (systems, not ML-specific). They remain the systems complement to the ML checklist below.

**U.** A separately downloaded “ML Reproducibility Checklist” (Pineau et al.) PDF was not archived as a local file in this round; where NeurIPS 2022 already incorporates those questions, the NeurIPS wording is the **E** source.

### 9.2 Operational items to encode (from the checklist axes, not invented numbers)

**E / S.** The following are the evaluation practices ThesisForge should require in ML / 智能方法 chapters, each corresponding to a NeurIPS-style checklist question rather than to a numeric folklore rule:

1. **Data leakage / split integrity.** State how train / validation / test (or pretrain / finetune / test) splits were constructed; whether any pre-processing, feature selection, normalization, or augmentation was fit only on training data; whether subjects, sessions, devices, or time windows can leak across splits (especially in communications, sensing, and semiconductor-test datasets). If a public benchmark has an official split, say whether it was used.
2. **Fair hyperparameter budgets.** Disclose the search space, the budget (number of trials, search method), and whether baselines received a **comparable** tuning budget. Do not report a carefully tuned proposed method against default-hyperparameter baselines without saying so.
3. **Test-set reuse.** The test set is for final evaluation. Repeated peeking, early-stopping on test, or model selection on test must be reported if it happened; the preferred practice is to freeze the test set and select only on validation.
4. **Means over seeds (and other randomness).** Report the number of runs / random seeds, the aggregation (mean, standard deviation or another stated interval), and what was randomized (initialization, data order, split, if any). A single-seed point estimate is not enough when the claim is about typical performance.
5. **Compute and environment.** Record hardware, software versions, and, when the claim depends on it, training time or compute. This is a reporting item, not a “must use GPU X” rule.
6. **Error bars and statistical claims.** If a significance statement is made, name the test and the unit of independence; do not invent a default p-threshold as a skill rule.
7. **Assets and limitations.** Data licence, code availability, and known negative results or failure cases, as asked by the checklist.

**S.** Do not encode a universal “always 5 seeds” or “always t-test at 0.05” rule: those numbers are not in the fetched checklist as mandates. Encode the *obligation to report* seeds, budgets, and splits, and treat “one unofficial test-set number” as a review risk.

### 9.3 Intersection with CS / comm / devices

**S.** For 计算机应用技术 topics that only *use* ML as a component (e.g. a detector, a channel estimator, a yield model):

- Apply this section to the ML component.
- Apply §6 (simulation credibility) to the communications or network experiment.
- Apply §7 (physical validation) to device claims.
- Do not let an ML ablation on a public benchmark stand in for a claimed communications or device improvement that was not measured or simulated under the relevant protocol.

---

## 10. Operational topic-discovery and literature-search protocol (CS / comm / devices)

### 10.1 Source

**E.** Kitchenham, B., and Charters, S., *Guidelines for performing Systematic Literature Reviews in Software Engineering*, EBSE Technical Report EBSE-2007-01, Keele University and Durham University, 2007. Legal technical-report copy downloaded (Keele / researchgate / university-hosted copies circulating as EBSE-2007-01). Local copy: `round2-sources/kitchenham-slr-2007.pdf`.

This is a software-engineering SLR protocol, not an HCI-only method and not a medical-grade Cochrane handbook. It is sufficient, and appropriately scoped, for CS / software / systems topic discovery. Communications and device topics can use the same protocol with field-specific databases and PICOC values.

### 10.2 Protocol to encode (PICOC, query families, screening, gap matrix)

**E.** Kitchenham & Charters operational steps, compressed into a ThesisForge-usable protocol:

1. **State the review question in PICOC** (or a stated subset): Population, Intervention, Comparison, Outcome, Context. Example mappings:
   - CS systems: Population = system/workload class; Intervention = proposed mechanism; Comparison = baselines; Outcome = stated metrics; Context = deployment assumptions.
   - Communications: Population = link/network scenario; Intervention = coding / MAC / resource allocation / simulation model; Comparison = standards or prior schemes; Outcome = BER, throughput, latency, energy, etc.; Context = channel and traffic assumptions.
   - Devices: Population = device/process class; Intervention = structure / process / model; Comparison = prior device or compact model; Outcome = I–V, transconductance, reliability, RF figures; Context = node, temperature, bias.
2. **Write a protocol before searching:** inclusion/exclusion criteria, date window, language, venue types (journal, conference, arXiv/preprint policy), and the quality-appraisal questions. Do not change inclusion criteria after seeing the results without recording the change.
3. **Query families, not one lucky string.** For each PICOC element, list synonyms and field terms (IEEE vs Chinese, acronym vs expanded form, device name vs structure). Combine with Boolean OR within a family and AND across families. Run the same family on **more than one index**: at minimum IEEE Xplore, ACM Digital Library, and a general index (Web of Science / Scopus / EI, plus CNKI or 中国知网 / 万方 for Chinese literature). For devices, add relevant IET / Elsevier titles as needed; for comms, add IEICE or 通信学报 indexes when the topic is domestic. Save the exact query and the date it was run.
4. **Snowball.** Backward (references of included papers) and forward (citations) are part of the method, not optional colour.
5. **Screen in two passes:** title/abstract, then full text, applying the pre-declared criteria. Record counts at each stage (a simplified PRISMA-style flow is enough; the 2007 report predates later PRISMA revisions, so do not invent a 2020 PRISMA mandate from this source).
6. **Extract a gap matrix**, not a pile of abstracts. Columns that follow naturally from the protocol: problem / setting, method family, assumptions, datasets or process node, metrics, what is **not** yet done. The research-gap sentence of a CS thesis (Tsinghua’s “critical review that ends in a gap,” §3.1) should be a reading of this matrix, not a rhetorical flourish.
7. **Quality appraisal** of included sources (venue is not a substitute for checking whether evaluation is credible — link to §§6, 7, 9).

**S.** For *topic discovery* (before a full SLR), use a lighter pass of the same protocol: PICOC sketch, two or three query families, a first gap matrix, and an explicit “what would count as a contribution.” Do not claim a systematic review unless the protocol was actually executed and documented.

---

## 11. Runnable experiment-design procedures (step level, sourced)

This section only states steps that can be tied to sources already fetched in Rounds 1–2. Lab folklore (unreferenced “always sweep 50 devices,” “always use 100 errors,” “always ablate this one module”) is omitted.

### 11.1 ML / systems ablation plan

**Sources:** NeurIPS 2022 checklist (§9); SIGPLAN empirical checklist and Heiser (Round 1, not re-litigated).

**Steps (S, sourced):**

1. Write the **claim** to be tested in one sentence (performance, resource, robustness, or a mechanism claim).
2. List **factors** that the paper says are responsible for the claim (modules, losses, features, system components). An ablation is a planned removal or replacement of those factors, not a random deletion.
3. Freeze the **protocol**: dataset or workload and official splits (§9); hardware and software; hyperparameter budget for the proposed method **and** for each baseline / ablated variant; random seeds and aggregation; metrics and, if used, statistical test and unit of independence.
4. Run the **full model / full system** and each planned ablated variant under that protocol. Do not retune only the full model after seeing test results.
5. Report a **table** of variant vs metric (mean and variation over seeds or over workloads), plus negative results if a factor did not matter.
6. For systems papers, add the SIGPLAN/Heiser questions: is the workload representative; is the baseline a real system rather than a weakened straw man; are overheads included; is the comparison repeatable from the paper.

### 11.2 Communications link / network simulation plan

**Sources:** Pawlikowski, Jeong, Lee 2002 (§6). BER event-count: **U**, omitted as a numeric step.

**Steps (E / S):**

1. State the **scenario**: topology or link model, traffic or source model, channel, protocol stack layer under study, and the **performance measures** (throughput, delay, loss, BER, etc.).
2. Declare, *before* production runs, the **precision target** (relative error and confidence level) and the **CI method** (independent replications, batch means, etc.).
3. Choose a **verified RNG** and independent streams; record seeds.
4. Perform **pilot runs** to estimate variance and to study transients. Apply a **named** warm-up / transient-deletion method. Do not invent a packet-count default.
5. Run **sequential** replications (or an equivalent sequential procedure) until the pre-declared relative error is met, or until a pre-declared computational budget is exhausted — in which case report the error actually achieved, do not hide it.
6. For Monte Carlo BER or rare-event measures, report the observation window and the **number of observed error events** together with an uncertainty statement. **Do not fill in a default event count.** If importance sampling or another rare-event method is used, name it and its assumptions.
7. Report enough model, parameter, and seed information for repetition; include failure cases (e.g. a metric that did not meet the precision target).

### 11.3 Device I–V / validation plan

**Sources:** EDS touchstones and the T-ED physical-validation stance (§7); no fabricated “typical sample size” from folklore.

**Steps (E / S):**

1. State the **claim type**: new structure or process, new mechanism, compact model, TCAD methodology, or circuit using the device. The evidence plan must match the claim (touchstones).
2. If the claim is about a **physical device**, plan **at least partial direct physical validation** (T-ED default). Simulation-only is acceptable only when the claim is about a method or model, and even then calibration and limitations must be stated.
3. Specify the **measurement or simulation protocol**: structure/process node, bias conditions, temperature, instrument or TCAD deck, calibration to which measured data (if any). For I–V, state what will be swept (VGS, VDS, etc.) and what will be extracted (threshold, subthreshold swing, on/off, transconductance, breakdown, …) — these are measurands, not a mandatory list for every paper.
4. Disclose **sample and repeatability** information actually collected (number of devices or dies, die-to-die or wafer variation, hysteresis or sweep direction) **if** such data exist. Do not invent a required N.
5. For circuit papers aimed at TCAS-class venues, plan **measurement of the implemented circuit** as the default path (§7.3).
6. In the paper, separate **measured**, **calibrated simulation**, and **predictive simulation**, and keep claims inside the evidence type.


---

## 12. EN/ZH hedging and stance bands (from fetched style guides only)

### 12.1 What was fetched, and what was not used

**E.** GB/T 6447—2025 (文摘编写规则) university PDF downloaded (Shandong University / library-hosted copy of the 2025 standard): local copies `round2-sources/gbt6447-2025-sdu.pdf` and an identical alternate PDF. Cover data: current abstract-writing standard, used by 7713.1—2025 5.2.9 as a normative reference.

**E.** Tsinghua 2025 writing guide, PKU 2018/2019 guide, and the four Chinese journal author guides (§§3, 5) contain explicit stance rules for abstracts and claims.

**E.** Fair university lecture material related to Zobel, *Writing for Computer Science*: UMBC course slides / handouts on writing for computer science were downloaded (`round2-sources/zobel-umbc-writing.pdf`, `writing3.pdf`). These are **lecture summaries used in teaching**, not a substitute for quoting the book. **No pirated ebook of Zobel was used, and no distinctive long quotation from the book is reproduced here.**

**U.** 陈浩元 monographs and cjstp (中国科技期刊研究) essays on Chinese STM hedging were not obtained as stable full texts in this round. They remain Round-3 targets. IEEE Editorial Style Manual (§8.1) is typographic and does not supply a hedge lexicon.

### 12.2 Chinese stance band (enough vs too much)

**E. From GB/T 6447—2025 (abstracts):**

- An abstract should report 目的、方法、结果、结论, with emphasis on results and conclusions (this is also restated in 7713.1—2025 5.2.9).
- **Author-written abstracts may use 本文 / 我们.** This is an explicit permission in the 2025 abstract standard.
- Abstracts should be self-contained, should avoid figures, tables, and uncommon symbols, and should not be a repeated title.

**E. Venue overlays that tighten this:**

- Tsinghua 2025 and PKU 2018/2019: thesis abstracts should **not** use the first person; they should highlight innovation without hanging a citation or formula in the abstract.
- 通信学报: abstracts should **avoid “本文”“作者”** and should not merely repeat the title (§5.4). This is a **direct clash** with GB/T 6447—2025’s permission. Encode as a venue override, not as a national ban.
- 计算机学报 / 电子学报 / 软件学报: abstracts should **体现 / 突出创新**, but none of the fetched guides instruct authors to write “首次 / 填补空白 / 国际领先.”
- Tsinghua 2025 on 创新点: each point should state the **problem, the method, and the effect**, and should be **tied to evidence** (papers, data, systems). That is a “tight claim” rule, not a licence for promotional adjectives.

**S. Chinese band to encode:**

- **Enough:** 目的—方法—结果—结论; 创新点写成“针对何种不足，提出何种方法，得到何种可核验结果”; limitations and future work in the conclusion (7713.1 5.3.7; school guides; 学位办〔2024〕18号 总结与展望).
- **Too much:** “首次提出 / 填补国内空白 / 达到国际领先 / 完美解决” without a sourced, checkable claim; piling 可能、也许、似乎、在一定程度上 on every sentence of a result that was actually measured; also the opposite vice — deleting all scope limitations.
- **First person:** default to the venue or school card. National abstract standard allows 本文/我们; Tsinghua, PKU, and 通信学报 abstracts do not.

### 12.3 English stance band (enough vs too much)

**E / S from the UMBC lecture summaries of Zobel-type CS writing advice, plus IEEE/ACM contribution-front review already established:**

- State the contribution early and **specifically**; prefer precise verbs and measurable outcomes over “novel, robust, efficient” as unearned adjectives.
- Report **what was actually done** (datasets, assumptions, what failed) rather than insulating every claim with stacked hedges (“may perhaps suggest the possibility that”).
- Scope limitations belong in a short, factual limitations / threats paragraph, not as a hedge attached to every result sentence.
- “First” / “best” claims need a scoped comparison (under which protocol, against which baselines, as of which literature cutoff).

The lecture notes do not provide a numbered “maximum hedges per paragraph” rule, and none is invented.

**S. English band to encode:**

- **Enough:** contribution sentence; factual results with the protocol attached; a compact limitations paragraph; confidence intervals or multi-seed variation where the evaluation section requires them (§§6, 9).
- **Too much:** decorative hedging; unearned superlatives; or, conversely, claims that outrun the evidence (simulation spoken of as measurement; test-set numbers spoken of as general performance).

---

## 13. Disagreements and corrections (recorded, not smoothed over)

1. **Abstract length is not one number.** GB/T 7713.1—2025 gives 300–1000 Chinese characters (with “special needs may be slightly more”) for a Chinese-language thesis, and “宜不少于 5000 字” only for the **Chinese abstract of a foreign-language thesis**. Tsinghua 800–1000 (one page), PKU PhD 800–1000 / master’s ~600, SEU ~500 / 200–300 English words, Xidian 2014 short ~300 vs detailed 3000/1000, and journal abstracts of 200–300 characters, all coexist. **Correction to a possible misreading:** do not apply the 5000-character floor to ordinary Chinese PhD abstracts.
2. **School manuals lag the 2025 national stack** (confirms Round 1, now with documents): Tsinghua’s **2025-03** guide still cites 7713.1—2006 and 7714—2015; PKU’s current official PDF still cites 7713—1987 and 7714—2005. ThesisForge should implement “national default + school overlay + warn when the school cites a superseded GB.”
3. **创新点 placement differs.** Tsinghua: required at the **end of Chapter 1**, echoing a 3–5 item problem list. PKU: Chapter 1 must include main innovation points. SEU format spec: creative work is emphasized in the **conclusion**, with no mandatory Ch. 1 创新点 heading. Fudan review form: reviewers list **at least three** contributions. Xidian 2025: reviewers judge whether 创新点 are 明确、凝练. Do not force one structural slot on every school.
4. **First person in abstracts.** GB/T 6447—2025 allows 本文/我们 in author-written abstracts; Tsinghua, PKU, and 通信学报 forbid or avoid first person. Venue/school wins for the document being written.
5. **GB/T 7714—2025 software type:** clause 8.11.3 example uses `[CP/OL]` for Zotero; Appendix B.10 of the HTML transcription uses `[EB/OL]` for the same item. Prefer the clause; flag the appendix inconsistency until an official typeset copy is checked.
6. **Professional vs academic doctorates.** 学位办〔2024〕18号 is mandatory quality structure for **engineering professional** degrees (including 电子信息), not for academic CS PhDs. Mixing the two outlines would be a skill error.
7. **Simulation-only papers.** T-ED: generally at least partial physical validation (Round 1, Ghione editorial still 403). TCAS-II: measured results are common; at least one special issue barred simulation-only papers — not shown to be a standing rule for every TCAS paper type. Pawlikowski does not set device-validation policy.
8. **BER event counts.** No legally fetched primary source in this round states a numeric event-count rule. Any “100 errors” type number would be an invention here.
9. **UCAS and BUPT numbers** that circulate in search snippets are **U** (fetches failed) and must not be encoded from memory of Round 1 snippets either.

---

## 14. (A) Concrete additions ThesisForge v2 MUST encode

Suggested file targets assume the existing skill layout (`SKILL.md`, `references/`, `templates/`, `agents/`) but **this report does not edit those files**.

| ID | Addition | Suggested file target |
| --- | --- | --- |
| A1 | Encode GB/T 7713.1—2025 clauses 4.6 (electronic theses, generic formats, audio/video/datasets), 5.2.6–5.2.7 (originality + authorization wording), 5.2.9 (abstract 300–1000; keywords 3–8, CY/T 173; foreign-language thesis Chinese abstract 宜不少于 5000), 5.3.7 (conclusion = core claims + limitations + future work, not a recap), and Table A.1 mandatory/optional/有则必备 elements. | `references/gbt-7713.1-2025.md`; front-matter checklist in `templates/` |
| A2 | Encode GB/T 7714—2025 worked patterns: `[PP/OL]`, `[DS/OL]`, `[CP/OL]`, PID rules (do not repeat a PID already in the URL; CSTR/DOI/URN all in scope), Latin surnames initial-capital only, citation dates mandatory for preprints/datasets/websites, 2015→2025 CS delta sheet. Note the Zotero `[CP/OL]` vs B.10 `[EB/OL]` inconsistency. | `references/gbt-7714-2025.md` plus citation examples in `templates/` |
| A3 | School overlay cards: Tsinghua 2025-03 (abstract 800–1000 / 300–400 words, keywords 3–5, 创新点 required at end of Ch. 1, ≥100 refs with ≥1/3 from last 5 years, still cites 2006/2015); PKU 2018/2019 (PhD 800–1000, master’s ~600, keywords 3–5, Ch. 1 创新点, ≥80 / ≥40 refs, typography as verified, still cites 1987/2005); SEU (abstract ~500 / 200–300 words, keywords 3–8, typography as verified, creative work in 结论). Xidian 2025 **review weights** 20/20/50/10 plus 创新点 明确凝练; Xidian 2014 handbook typography/detailed-abstract figures marked historical only. UCAS/BUPT left open. | `references/school-overlays.md` or per-school cards under `references/schools/` |
| A4 | Professional-doctorate mode from 学位办〔2024〕18号: eight-part document, four-part body, 11 document types, 电子信息 included; do not apply to academic PhDs by default. Fudan “至少三项创新点” as a review habit, not a national law. | `references/moe-professional-doctorate-2024.md`; `templates/review-checklist.md` |
| A5 | Venue cards for 计算机学报, 软件学报, 电子学报, 通信学报 (length, abstract, keywords, 创新点 field, reference minima, first-person abstract rule). 半导体学报 stub marked **U**. | `references/journals-cn.md` |
| A6 | Communications simulation procedure from Pawlikowski et al. 2002: pre-declare relative-error / CI, sequential stopping, transient deletion, independent replications or named CI method, RNG/streams, report CI. **No invented event-count.** BER: report observed errors and uncertainty; numeric default left **U**. | `references/experiment-design.md` (comms subsection) |
| A7 | Device / circuit evidence policy: EDS touchstones; T-ED default = at least partial physical validation; TCAS-II commonly measured, some special issues ban simulation-only; keep claim type aligned with evidence type. | `references/experiment-design.md` (devices subsection); `references/venues-ieee-eds-cass.md` |
| A8 | IEEE Editorial Style Manual (29 July 2024) + IEEE Reference Guide as the English typographic/reference switch; Elsevier mode = IMRaD + journal-specific Guide for Authors / highlights card, no invented highlight caps; ACM TOCS/TON specifics deferred (**U**). | `references/ieee-style.md`; `references/elsevier-venue-card.md` (template) |
| A9 | ML evaluation gate: leakage/splits, fair hyperparameter budgets, test-set reuse, means over seeds, compute, no universal “5 seeds / p<0.05” mandate. | `references/experiment-design.md` (ML subsection); optional checklist prompt in `agents/` |
| A10 | Literature protocol: Kitchenham & Charters PICOC, query families, multi-database search, snowball, two-pass screening, gap matrix; light variant for topic discovery. Not HCI-only. | `references/literature-search.md` |
| A11 | Runnable experiment-design procedures at the step granularity of §11 (ablation, comms sim, device I–V / validation), sourced, no folklore N. | `references/experiment-design.md` |
| A12 | Stance bands from §12: tight claims + honest scope; no 首次/填补空白 without evidence; no stacked hedges; first-person abstract governed by venue/school vs GB/T 6447 clash; English contribution-front + factual limitations paragraph. Zobel only via fair lecture summary, not quoted from a pirated book. | `references/style-and-stance.md` |
| A13 | Reviewer-mode checklist for academic theses: 选题; 创新点是否明确、凝练 (not pedantic hedging); 论证与证据 (eval/simulation/measurement matched to claim); 规范性. Professional variant adds 应用价值. | `templates/review-checklist.md` |

---

## 15. (B) Remaining gaps for Round 3

1. Official SAMR / openstd **typeset** full texts of GB/T 7713.1—2025, 7714—2025, and 6447—2025 (to retire the third-party HTML transcription and to resolve the 7714 Zotero `[CP/OL]` vs `[EB/OL]` inconsistency).
2. **UCAS** current writing regulations (previous engineering PDF HTTP 500; las.cas.cn SSL/500). Need a working library.ucas.ac.cn or 学位办 file before encoding 1000–1500-character rumour figures.
3. **BUPT** graduate-school writing manual (grs.bupt.edu.cn HTTP 412; DOCX mirror not obtained).
4. A **current** Xidian *writing* handbook (the 2014 page cannot be the 2026 default). SEU’s cited GB edition should be confirmed.
5. Zhejiang University (or another EE/CS) 评阅书 PDF (cs.zju.edu.cn HTTP 500) and any MOE-wide academic-degree (非专业学位) review template, if one exists beyond school forms.
6. **半导体学报 / Journal of Semiconductors** author guide (jos.ac.cn 500/502).
7. **Ghione T-ED editorial** on simulation-only papers (HTTP 403). Standing **TCAS-I/II Information for Authors** PDFs.
8. Legal, complete **Jeruchim 1984** (or another primary BER/Monte Carlo CI derivation) so a numeric or formula-level error-event rule can be encoded or permanently rejected.
9. **ACM TOCS / TON** (and current ACM Master Article Template) author guidelines; a saved **Computer Networks** or **Microelectronics Journal** Guide for Authors with that journal’s actual highlight/word caps.
10. 陈浩元 / cjstp Chinese STM writing essays, if legally fetchable, to thicken the ZH stance band.
11. Optional: CY/T 173 (keywords) full text, because 7713.1—2025 5.2.9 points to it.
12. Optional: confirm whether any 2025–2026 Tsinghua/PKU notice has started pointing at 7713.1—2025 / 7714—2025, given implementation dates in 2026.

---

## 16. (C) Source list (URLs and fetch status)

Status key: **OK** = full page or PDF obtained and used; **FAIL** = attempted, failure mode recorded; **LOCATED** = official record found but full text not obtained; **NOT USED** = avoided (paywall/pirate).

| # | Source | URL | Status |
| --- | --- | --- | --- |
| 1 | GB/T 7713.1—2025, Hunan Agricultural University copy | https://yjsy.hunau.edu.cn/xwgz/xgxz_1462/202603/P020260325595645822472.pdf | OK (PDF, 28 pp) |
| 2 | GB/T 7713.1—2025, Soochow University Library copy | https://library.suda.edu.cn/_upload/article/files/02/da/9cb404ca436785662c23c2c596b6/a911b195-fac8-4416-96b9-1d372f061178.pdf | OK (PDF; cleaner Appendix A) |
| 3 | GB/T 7713.1—2025, SAMR detail | https://std.samr.gov.cn/gb/search/gbDetailed?id=3B46A026CC84469CE06397BE0A0AEEB8 | FAIL (Round 1 timeout; not a working full-text source this round) |
| 4 | GB/T 7714—2025, CNKI-hosted OCR PDF | https://publishmedia.cbpt.cnki.net/portal/minio/webs/jjkj/media/web/2026/07/27/GBT%207714%E4%B8%802025%E4%BF%A1%E6%81%AF%E4%B8%8E%E6%96%87%E7%8C%AE%20%20%E5%8F%82%E8%80%83%E6%96%87%E7%8C%AE%E8%91%97%E5%BD%95%E8%A7%84%E5%88%99_OCR.pdf | OK (PDF, 45 pp, messy OCR; used for cross-check) |
| 5 | GB/T 7714—2025, third-party HTML transcription | https://kanhao100.github.io/GBT7714-2025-bst/standards/gbt7714-2025.html | OK (HTML; not official typeset) |
| 6 | GB/T 7714—2025, openstd record | https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14 | LOCATED (no official full text) |
| 7 | GB/T 7714—2025, SAMR detail | https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F | LOCATED (no official full text) |
| 8 | Unofficial 2015 vs 2025 commentaries | https://kanhao100.github.io/GBT7714-2025-bst/docs/2015-vs-2025.html ; https://thesis.org.cn/changes/ | OK as commentary only; extra claims treated **U** |
| 9 | Tsinghua writing guide, 2025-03 | https://www.tsinghua.edu.cn/__local/A/A3/A8/948F85164440B1073B73B3BAA9D_1AF5B731_137B8F.pdf (page: https://www.tsinghua.edu.cn/info/1492/122142.htm) | OK (PDF, 53 pp) |
| 10 | PKU writing guide, cover date 2018-02-28 | https://xkb.pku.edu.cn/docs/2019-10/20191016174319619362.pdf | OK (PDF) |
| 11 | UCAS engineering writing PDF | https://ce.ucas.ac.cn/index.php/zh-CN/xsyjssgl/gzzd/index.php?option=com_content&view=article&id=2516 | FAIL (HTTP 500) |
| 12 | UCAS / CAS library older link | https://las.cas.cn/ (paths used in Round 1) | FAIL (expired SSL / HTTP 500) |
| 13 | BUPT graduate-school notice | https://grs.bupt.edu.cn/info/1035/3071.htm | FAIL (HTTP 412) |
| 14 | BUPT writing-manual DOCX listing | https://ss.bupt.edu.cn/__local/4/EF/C3/9F29E101C6154126A16EF5B6689_AC6C57CE_12939C.docx | FAIL (not obtained) |
| 15 | SEU thesis format specification | https://seugs.seu.edu.cn/_upload/article/files/c4/04/6784c6fe4c7c8096aaf8d68cc248/644d870b-2c8c-4c4d-bc7a-cf71061b536e.pdf | OK (PDF) |
| 16 | Xidian 2025 review-and-submission notice | https://gr.xidian.edu.cn/info/1073/13806.htm | OK (HTML) |
| 17 | Xidian 2014 writing-handbook notice | https://gr.xidian.edu.cn/info/1069/1878.htm | OK (HTML; historical) |
| 18 | MOE news on 学位办〔2024〕18号 | http://www.moe.gov.cn/jyb_xwfb/s7600/202410/t20241030_1159900.html | OK (HTML, 2024-10-30) |
| 19 | Xidian reprint of the professional-doctorate quality standard | https://gr.xidian.edu.cn/info/1073/13116.htm | OK (HTML, full standard) |
| 20 | Fudan PhD thesis review form | https://gsas.fudan.edu.cn/jzg/_upload/tpl/08/4d/2125/template2125/files/%E5%8D%9A%E5%A3%AB%E5%AD%A6%E4%BD%8D%E8%AE%BA%E6%96%87%E8%AF%84%E9%98%85%E4%B9%A6.pdf | OK (PDF) |
| 21 | ZJU CS doctoral review form | https://cs.zju.edu.cn/_upload/article/files/c6/1b/ce73afe1471caa5aab9e581d4ae4/e496d7db-ab58-4cdc-81d7-5b77b537ec1e.pdf | FAIL (HTTP 500) |
| 22 | 计算机学报 作者须知 | https://www.cjc.ict.ac.cn/zzjsyy/index_2.htm?mod=info&act=view&id=34 | OK |
| 23 | 计算机学报 2025 年审通知 PDF | https://cjc.ict.ac.cn/attached/file/20260121/20260121204611_758.pdf | OK (PDF) |
| 24 | 计算机学报 稿件撰写要求 PDF | https://cjc.ict.ac.cn/attached/file/20231126/20231126173911_237.pdf | OK (PDF) |
| 25 | 软件学报 投稿指南 | http://www.jos.org.cn/ch/reader/news_content.aspx?id=20251 | OK |
| 26 | 软件学报 稿件录用标准 | http://www.jos.org.cn/news/news.aspx?id=20dc1b96-8ca8-4546-a4d1-43ce8e2f1b5a | OK |
| 27 | 电子学报 投稿须知 | https://www.ejournal.org.cn/CN/column/item104.shtml | OK |
| 28 | 电子学报 论文模板栏 | https://www.ejournal.org.cn/CN/column/item105.shtml | OK |
| 29 | 通信学报 投稿须知 | https://www.joconline.com.cn/zh/tougao.shtml | OK |
| 30 | 半导体学报 / Journal of Semiconductors author pages | jos.ac.cn / IOP “Preparing Your Manuscript” URLs | FAIL (HTTP 500 / 502) |
| 31 | Pawlikowski, Jeong, Lee 2002, Canterbury legal copy | https://akaroa.canterbury.ac.nz/pdf/PJL2002.pdf | OK (PDF) |
| 32 | Jeruchim 1984 JSAC | https://doi.org/10.1109/JSAC.1984.1146031 | NOT USED (paywalled; no pirate copy) |
| 33 | IEEE EDS TouCHSTONES | https://eds.ieee.org/images/files/Publications/touchstones.pdf | OK (PDF) |
| 34 | Ghione T-ED editorial on simulation-only papers | IEEE Xplore / EDS editorial URL previously located | FAIL (HTTP 403) |
| 35 | IEEE Editorial Style Manual, 29 July 2024 | IEEE Author Center PDF (ieeeauthorcenter.ieee.org) | OK (PDF) |
| 36 | IEEE Reference Guide | IEEE Author Center PDF | OK (PDF) |
| 37 | Elsevier journal Guides for Authors (Computer Networks / Microelectronics Journal pattern) | Official Elsevier journal “Guide for Authors” pages | OK as a structural pattern; specific numeric caps not archived, treated with care |
| 38 | ACM TOCS / TON author guidelines | ACM DL journal author pages | FAIL (timeout / not obtained) |
| 39 | NeurIPS 2022 (and successor) paper checklist | Official NeurIPS checklist / author-instructions pages | OK (checklist axes) |
| 40 | Kitchenham & Charters, EBSE-2007-01 | University-hosted EBSE-2007-01 PDF | OK (PDF) |
| 41 | GB/T 6447—2025, Shandong University copy | university / library-hosted PDF of 6447—2025 | OK (PDF) |
| 42 | UMBC lecture material on writing for computer science (Zobel-related) | UMBC course PDFs | OK as fair lecture summary; book itself not quoted from a pirate source |
| 43 | 陈浩元 / cjstp Chinese STM style essays | various cjstp / book pages | FAIL / not obtained as full text |

Local aides (not official URLs): `/workspace/thesisforge-research/round2-sources/` contains the successfully downloaded PDFs and extracted `.txt` files named in the summary of this report.

---

## 17. Round 2 conclusion

Round 2 closed the highest-value documentation gaps with primary or university-hosted texts: a usable clean text of GB/T 7713.1—2025 (including Table A.1 and the abstract / electronic-thesis / declaration clauses), a CS-relevant 7714—2025 example set and 2015–2025 delta (pending an official typeset copy), three elite-school manuals actually in hand (Tsinghua 2025, PKU, SEU) plus Xidian’s 2025 review form, the MOE professional-doctorate standard that Round 1 only located, four Chinese journal author cards, a legal Pawlikowski 2002 procedure, EDS touchstones, the IEEE style manuals, a Kitchenham SLR protocol, a NeurIPS-style ML evaluation gate, and stance rules that are traced to fetched guides rather than to invented psychology.

What remains honestly **U** — official SAMR typesets, UCAS and BUPT manuals, 半导体学报, Ghione’s editorial, Jeruchim’s BER numbers, ACM Transactions specifics, and 陈浩元/cjstp — is listed for Round 3 and was not filled with folklore. ThesisForge skill files were not edited in this round.
