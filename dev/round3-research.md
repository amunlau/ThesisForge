# ThesisForge Round 3 Research Report

**Date:** 2026-11-11 (Asia/Shanghai)\
**Scope:** Independent, evidence-based close of the twelve Round-3 priorities listed in the task brief.\
**Method constraint:** Primary or official-equivalent sources only. No invented standards, quotations, or numeric rules. Search snippets are not encoded as numbers unless a full official text was in hand. Failed fetches are kept with the failure mode. ThesisForge skill files under `/workspace/ThesisForge` were not edited.

**Independence:** This report starts from the Round-3 gaps and from primary sources fetched or downloaded in this round. Round-1 and Round-2 reports were consulted only to avoid retrying blindly failed URLs and to know what was already established. Already-established findings (Degree Law; GB/T 7713.1—2025 in force 2026-02-01; GB/T 7714—2025 in force 2026-07-01; fetched Tsinghua 2025-03 / PKU 2018–2019 / SEU / Xidian 2025 review-form overlays; 学位办〔2024〕18号 as a professional-doctorate standard only; four Chinese CS/EE journal cards; Pawlikowski 2002; EDS touchstones; IEEE style manuals; NeurIPS 2022 checklist; Kitchenham PICOC) are not re-litigated unless a later source corrects them.

**Evidence labels:**

| Label | Meaning |
| --- | --- |
| **E** | Evidence: a full official or official-equivalent page/PDF was obtained this round and the claim is taken from that text |
| **S** | Synthesis: a cautious reading that combines obtained sources, labelled as such |
| **U** | Unknown / unverified this round: fetch failed, only a search snippet was available, or the source does not state the number |

---

## 1. Official SAMR / openstd typeset texts of GB/T 7713.1—2025, 7714—2025, and 6447—2025; the Zotero type-code inconsistency

### 1.1 Official platforms still do not give free typeset full text for 7713.1 or 7714

**E.** The national open-standard record for GB/T 7713.1—2025, https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=36C05B5738C54D42B4B262525320B52F, states that the standard is 现行, published 2025-08-01, in force **2026-02-01**, and is marked 采 (adoption). The same page states that because the standard adopts ISO/IEC (or other foreign) standards, **the system does not provide text-reading service** for copyright reasons. The SAMR detail page https://std.samr.gov.cn/gb/search/gbDetailed?id=3B46A026CC84469CE06397BE0A0AEEB8 confirms the bibliographic data and that the standard **non-equivalently adopts ISO 7144:1986**.

**E.** The open-standard record for GB/T 7714—2025, https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14, likewise marks the standard 采, published 2025-12-02, in force **2026-07-01**, and withholds text-reading service for the same copyright reason. The SAMR detail page https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F confirms that the standard non-equivalently adopts **ISO 690:2021**. The National Digital Standards Library record https://ndls.cnis.ac.cn/standard/detail/5ff4aa78a1e9a5952b78c2ea5490177b lists a purchase price and in-person reading at 国家标准馆; it is not a free official PDF.

**S.** Official SAMR / openstd **typeset full texts of 7713.1—2025 and 7714—2025 are not legally downloadable from those platforms**. University-hosted copies remain the practical working texts. This is a standing copyright constraint, not a transient fetch failure.

**E.** By contrast, the open-standard record for GB/T 6447—2025, https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=F70F4968628FFF58FF5AE7414A815CC8, is **not** marked 采 in the way 7713.1 / 7714 are, and the record offers “在线预览” and “下载标准”. Published 2025-08-01, in force **2026-02-01**. An official-equivalent typeset PDF was obtained this round from a CNKI-hosted copy (see §1.5 and §10).

### 1.2 A typeset, university-purchased copy of GB/T 7714—2025 (not SAMR, but cleaner than the Round-2 HTML/OCR)

**E.** A typeset PDF of GB/T 7714—2025 was downloaded from Capital University of Economics and Business: https://rem.cueb.edu.cn/docs/2026-04/ab13582039564d9090a722f17cfcbf2e.pdf (local: `round3-sources/gbt7714-2025-cueb.pdf`, 48 pages, A4, 1 274 510 bytes). Cover data match the official record: ICS 01.140.20, CCS A14; 代替 GB/T 7714—2015; 2025-12-02 发布, 2026-07-01 实施; issued by 国家市场监督管理总局 / 国家标准化管理委员会. The file is a purchased China Standards Press copy, watermarked **“首都经济贸易大学 专用”**, with an order number and anti-counterfeit number on each page. Text extraction requires collapsing inter-character spaces; the extracted text was used only after that normalisation. This is an official-equivalent typeset edition, **not** a SAMR open download.

**E.** Huaqiao University Graduate School posted both 7713.1—2025 and 7714—2025 on a public “国家标准及政策性文件” page dated **2026-03-01**, https://grs.hqu.edu.cn/info/1078/17770.htm. Attachment URLs of the form `https://grs.hqu.edu.cn/system/_content/download.jsp?urltype=news.DownloadAttachUrl&owner=2084472036&wbfileid=…` were obtained from the HTML. Direct download this round returned a 3 829-byte HTML stub titled “附件下载”, not a PDF. **FAIL (not a PDF).** The page itself is evidence that at least one graduate school had begun posting the 2025 editions by March 2026 (see also §11).

**U.** No official-equivalent typeset of GB/T 7713.1—2025 newer than the Round-2 Hunan Agricultural University and Soochow University Library copies was obtained. Those Round-2 PDFs remain the working texts for 7713.1 clauses already encoded.

### 1.3 Correction to the Round-2 characterisation of clause 8.11, and confirmation of the Zotero inconsistency

**E. From the CUEB typeset GB/T 7714—2025 table of contents and body:**

- Chapter 8 literature-type clauses are: 8.1 通用要求; 8.2 图书; 8.3 图书中的析出文献; 8.4 连续出版物; 8.5 连续出版物中的析出文献; 8.6 会议录; 8.7 学位论文; 8.8 报告; 8.9 标准; 8.10 专利; **8.11 网站、网页**; 8.12 档案; 8.13 地图; 8.14 数据集; 8.15 预印本.
- Appendix B follows the same inventory: **B.10 网站、网页**, B.11 档案, B.12 地图, B.13 数据集, B.14 预印本.
- **There is no dedicated chapter for 计算机程序 or 数据库.** Those types appear only in normative Appendix Table A.1: 计算机程序 = **CP**; 数据库 = **DB**; 网站、网页 = **EB**; 数据集 = **DS**; 预印本 = **PP**. Table A.2 still has 联机网络 = **OL** (and adds 缩微资料 = **MM**, as already noted in Round 2).

**Correction (to Round 2):** the Round-2 HTML/OCR transcription described “clause 8.11.3” as a computer-program example using `[CP/OL]`. In the typeset official-equivalent, **8.11 is “网站、网页”** and **8.11.3 is “网页”**. Computer programs have a type code but no chapter of their own. ThesisForge v3 must not describe 8.11.3 as a software-citation clause.

**E. Clause 8.11.3.2 网页 examples, typeset text (punctuation restored for readability):**

The examples in 8.11.3.2 are: [1] 高等教育文献保障系统. 馆际互借与文献传递服务[EB/OL]. [2025-06-21]. plus a CALIS URL; [2] [《昨日之歌》图书封面][EB/OL]. (2015-09-18)[2023-03-06]. plus a luxunmuseum image URL; [3] 许振超: “好好干, 当一个好工人”[EB/OL]. (2025-02-17)[2025-06-22]. plus a people.com.cn URL; [4] Antonio M, Pepper L. Historias de Portugal: livros caidos[EB/OL]. (2019-07-13)[2025-01-02]. plus an arquivo.pt URL; **[5] Zotero. [Zotero download][CP/OL]. [2024-04-08]. https://www.zotero.org/download/.**

Examples [1]–[4] in the same clause use `[EB/OL]`. Only example [5] uses `[CP/OL]`.

**E. Appendix B.10 网站、网页 example [13], same typeset copy:**

`[13] Zotero. [Zotero download][EB/OL]. [2024-04-08]. https://www.zotero.org/down-load/.`

The same Zotero download item is tagged **`[CP/OL]` in 8.11.3** and **`[EB/OL]` in B.10**. The appendix heading is also “网站、网页”, not “计算机程序”. The inconsistency is therefore **confirmed in a typeset official-equivalent PDF**, not an artefact of the Round-2 HTML transcription. (The B.10 URL is line-broken as `down-load` in the extracted text; that hyphenation should not be treated as a second official URL.)

**S. How ThesisForge should encode this, until an official SAMR typeset or an erratum appears:**

1. Treat **CP** as the Table A.1 type code for a computer program, and **EB** as the type code for a website or webpage.
2. Do **not** invent a “computer-program chapter 8.11”.
3. Flag the Zotero item as an **unresolved internal inconsistency** of the 2025 standard itself: a software download page is given once as `[CP/OL]` (in a webpage-clause example list) and once as `[EB/OL]` (in the webpage appendix). Prefer neither as “the” official rule for that one example. A prudent author practice, labelled as synthesis not as a hidden official rule, is: cite the *program* with `[CP/OL]` when the cited object is the software itself; cite a *web page about it* with `[EB/OL]`. Do not silently “correct” one example into the other.
4. Continue to encode the already-established worked patterns that this typeset copy confirms: `[PP/OL]` (8.15, ChinaXiv / arXiv / PSSXiv examples, with CSTR or DOI), `[DS/OL]` (8.14), PID rule 7.9.1 (if the access URL already contains the PID, do not repeat the PID), 7.9.2 (otherwise the PID may be recorded as in the source, DOI and URN examples), and Latin / pinyin name capitalisation in 7.1.1 (see below).

### 1.4 Other 7714—2025 clauses confirmed from the typeset copy (useful for v3, not a re-litigation)

**E. 7.1.1 个人责任者 (typeset):** 姓在前、名在后. For Western names recorded in a Western language: “姓应全部著录, 首字母应大写, 名可缩写为首字母, 如用首字母无法识别该人名时, 可著录全名”. For names in Hanyu Pinyin: “姓应全部著录, 首字母应大写, 名宜用全称”. Worked examples include `Einstein A` (from Albert Einstein) and `Li Jiangning`. **This is not an all-caps surname rule.** It confirms the Round-2 reading that 2025 moves away from the 2015-era habit of Latin surnames in ALL CAPS. Clause 5.6 adds: “著录西文文献时, 大写字母的使用应符合信息资源本身文种的习惯用法.”

**E. 7.1.2 (typeset):** “著作方式相同的责任者不超过 3 个时, 应全部照录。超过 3 个时, **可**著录前 3 个责任者, 其后加 ‘, 等’ 或与之相应的词.” The “可” is permissive, not “应”. This is the same three-then-等 band that SEU’s format spec also uses (§4).

**E. 8.14 数据集 and 8.15 预印本 formats (typeset, condensed):**

- Dataset: `主要责任者. 题名: 其他题名信息[文献类型标识/文献载体标识]. 版本. 发布平台 (发布或修改日期)[引用日期]. 获取和访问路径. 永久标识符.` Examples use `[DS/OL]` and include CSTR and DOI.
- Preprint: `主要责任者. 题名: 其他题名信息[文献类型标识/文献载体标识]. 版本. 出版平台 (创建或修改日期)[引用日期]. 获取和访问路径. 永久标识符.` Examples use `[PP/OL]` for PSSXiv, ChinaXiv (with CSTR), and arXiv (`https://doi.org/10.48550/arXiv.1112.6136`).

**E. 7.9 永久标识符 (typeset):** 7.9.1 “获取和访问路径中含永久标识符时, 可不重复著录永久标识符” (DOI-in-URL and URN-in-URL examples). 7.9.2 “获取和访问路径中不含永久标识符时, 可按照原文如实著录永久标识符” (a USTC dissertation with a Wanfang URL plus a separate `DOI:`).

### 1.5 GB/T 6447—2025 typeset confirmation

**E.** A typeset 11-page PDF of GB/T 6447—2025 was downloaded from https://publishmedia.cbpt.cnki.net/portal/minio/webs/wuji/media/web/2026/05/14/GBT6447-2025%E6%96%87%E7%8C%AE%E6%91%98%E8%A6%81%E7%BC%96%E5%86%99%E8%A7%84%E5%88%99-2025.pdf (local: `round3-sources/gbt6447-2025-cnki.pdf`). Cover: 代替 GB/T 6447—1986; 2025-08-01 发布, 2026-02-01 实施. Drafters include 张品纯, **陈浩元**, and others (this is the same standard already used in Round 2 from a Shandong University copy; this fetch is a cleaner cross-check, not a new standard). An identical-looking file is also hosted at https://lxbwk.njournal.sdu.edu.cn/fileup/1671-9352/ITEM/20250813124422.pdf (not re-downloaded once the CNKI copy was in hand).

Key clauses confirmed from this typeset text are recorded in §10, together with CY/T 173, because both feed the Chinese stance / abstract / keyword band.

---

## 2. UCAS current writing regulations

**E.** UCAS official college pages currently present the writing instrument as **《中国科学院大学研究生学位论文撰写规范指导意见》（校发学位字〔2022〕40号）**, described as a **2024年10月更新版**, with later template notes:

- School of Electronic, Electrical and Communication Engineering: https://eece.ucas.ac.cn/index.php/zh-cn/2014-06-13-06-47-02/2014-06-13-06-48-14/1535-2018-10-22-02-11-12 — attachments named: 附件1 校发学位字〔2022〕40号; LaTeX sample 2024.5.21; LaTeX template 2023.7.20; “Word模板和LaTex模板更新说明2024.10.23”.
- School of Artificial Intelligence: https://ai.ucas.ac.cn/index.php/zh-cn/jxjy/fzpy1/7293-2022-40 — “附件1学位论文撰写具体要求（2024年10月更新）.zip” (page dated 2024-05-11).
- Hangzhou Institute for Advanced Study (life sciences) lists “各学科群分会学位论文撰写具体要求（2024年6月更新）”: http://hias.ucas.ac.cn/life/info/1515/2088.htm.
- An English-facing SDC page, https://sdc.ucas.ac.cn/index.php/international-students/degree-information/1306-university-of-chinese-academy-of-sciences-degree-thesis-dissertation-guidelines, states that the Guide is a general reference, that discipline-group committees may make specific regulations, that UCAS provides only the Chinese version for each group, and that the page was “Updated in 2024.1”.

**FAIL.** The eece.ucas.ac.cn page HTML contains `/up/` and `?task=down&fid=` download links for the 40号 DOC. URL-encoded `/up/` downloads returned **HTTP 404**. The `task=down&fid=` URL returned **HTTP 500**. The 2024-10-23 template-update DOCX returned **404**. The Round-2 engineering PDF at ce.ucas.ac.cn and the older las.cas.cn paths were not blindly retried as working full-text sources.

**U.** Because the 40号 document and the 2024-10 “具体要求” zip were not obtained as full text, **the circulating figures (硕士 500–1000 字 / 博士 1000–1500 字, 英文约 300–600 词, 关键词 3–5, 博士参考文献不少于 80 篇, etc.) remain unverified and must not be encoded.** The only facts that may be encoded are: the current named instrument is 校发学位字〔2022〕40号; it is still being issued in 2024-updated form; discipline-group overlays exist; the full typography and abstract numbers are still **U**.

**S.** Nothing fetched this round shows a UCAS 学位办 notice that already points at GB/T 7713.1—2025 or GB/T 7714—2025 (see §11).

---

## 3. BUPT graduate-school writing manual

**FAIL.** https://grs.bupt.edu.cn/info/1035/3071.htm again returned **HTTP 412** to both curl and WebFetch (same failure mode as Round 2). The previously listed DOCX mirror on ss.bupt.edu.cn was not retried as a working path after the earlier miss. No official DOC was obtained.

**Located, but not independently re-fetched as HTML this round.** WebSearch returned the official notice text of that same grs.bupt.edu.cn URL: title **《关于发布研究生学位论文写作规范要求的通知》**, dated **2024-01-02**, Graduate School; it names **《北京邮电大学研究生学位论文写作与制作规范》** as 附件1, plus STEM and humanities Word templates, a foreign-language-and-literature reference-format annex, a format-check platform (`https://bupt.lun51.com/GRS`), and a statement that theses submitted after **2024-04-10** must follow the new 制作规范. The same official page text, as returned by the search index, records a **2025-01-15** revision of that 制作规范 and of the Word templates, and lists the 2025-01-15 DOC/RAR attachments by filename.

**S / caution.** The *existence and date* of a current BUPT writing-and-production specification, last revised **2025-01-15**, is reasonably established from the official notice title and attachment names. The 2025-01-15 changelog items that appear in the search-retrieved page text (odd-page starts for each part and chapter; addition of “作者学习经历”; “培养方式” renamed “学习方式”) should be treated as **provisionally located** until the page or the DOC can be fetched without HTTP 412. **Typography, abstract length, keyword counts, and the GB edition BUPT cites remain U and must not be encoded from secondary GitHub templates or from memory of older 2017/2023 format rules.**

Unofficial GitHub Word/LaTeX templates and a third-party styles issue that attaches a user-uploaded copy of the 2025-01-15 DOC were **not used** as primary sources.

---

## 4. Current Xidian writing handbook; the GB edition SEU currently cites

### 4.1 Xidian

**E.** The Graduate School notice **《关于做好2026年研究生学位申请工作的通知》**, published **2026-01-05**, https://gr.xidian.edu.cn/info/1044/17974.htm, states explicitly that the thesis template to be used this time is the **2015 revised edition**, and that the practice-outcome report template is the 2025 revised edition, and that applicants must follow those templates strictly.

The same notice gives 2026 degree-application windows, similarity-detection thresholds (STEM PhD: overall coincidence **不高于 10%**, each chapter **不高于 20%**; STEM master’s: overall **不高于 15%**, each chapter **不高于 30%**; humanities/economics thresholds are higher, as stated on the page), and points applicants to the “学位授予 / 资料下载” packs. It does not publish a new prose writing handbook.

**E.** The academic-master’s materials page, https://gr.xidian.edu.cn/info/1047/5087.htm (page originally dated 2016-03-21, with a 2019-03 note about cover/title-page updates), currently lists among its attachments:

- `西安电子科技大学研究生学位论文模板（2015年修订版）-2025.01修订.docx`
- LaTeX templates revised 2024.04
- `研究生学位论文详细摘要的撰写要求.doc`
- `关于发布研究生学位论文模板（2015年修订版）的通知.doc`

**S.** For 2026 Xidian degree applications, the in-force *writing template* is still branded **“2015年修订版”**, with a further **2025-01** file-date on the Word template (the materials page’s own 2019 note says recent edits were mainly college/discipline information on the title and cover pages — that note is older than the 2025-01 filename and should not be assumed to describe the 2025-01 edit). The 2014 writing-handbook page already fetched in Round 2 remains **historical**. The 2025-01 `.docx` and the “详细摘要的撰写要求” DOC were **not downloaded** this round, so 2014 typography and “详细摘要 博士 3000 / 硕士 1000” figures must still not be encoded as 2026 defaults. The 2025 review-form weights 20/20/50/10 from Round 2 are untouched.

### 4.2 SEU — which GB edition is cited?

**E.** The Graduate School regulations page https://seugs.seu.edu.cn/2023/0424/c28878a442680/page.htm, dated **2023-04-24**, still offers the official format-specification PDF. The file at https://seugs.seu.edu.cn/_upload/article/files/5d/c2/abe9785f44c8b3ea4823f14bfb92/cd829a73-1b86-400d-9bce-2c4b4fdb85b7.pdf was downloaded this round (12 pages). Its MD5 is **identical** to the Round-2 SEU file. It is the current official format specification, not a newer 2025/2026 edition.

**E.** In that specification, a search of the full extracted text finds **no occurrence of “GB/T 7714” or “GB/T 7713” and no year 2005 / 2015 / 2025 attached to a reference standard**. What the document *does* cite:

- GB/T 15835 for numerals and units.
- “根据 **GB3469** 规定” for single-letter literature-type codes (J, M, C, D, P, S, N, R, Z, etc.).
- Older electronic-type vocabulary: DB / CP / EB, with **EB explicitly glossed as “电子公告 (Electronic bulletin board)”**, plus carrier codes MT / DK / CD / OL, and examples such as `[EB/OL]` “网上电子公告”, `[CP/DK]` “磁盘软件”.
- Author rule: 3 or fewer authors all listed; more than 3, first 3 plus “, 等” / “, et al”; page numbers must not be omitted; in-text citations are superscript `[n]`.

**S.** SEU’s current format spec is a **local overlay** that implements a 7714-family sequential-coding style but **does not name a 7714 edition**. Its “EB = 电子公告” wording is the pre-2025 vocabulary. Under GB/T 7714—2025 Table A.1 (typeset, §1.3), **EB means 网站、网页**. The three-author band happens to match 7714—2025 clause 7.1.2, but that is not evidence that SEU has adopted the 2025 edition. A search-index claim that the SEU library “recommends GB/T 7714—2015” was **not independently fetched** (`http://lib.seu.edu.cn/list.php?fid=59` was not obtained this round) and remains **U**. ThesisForge should record: “SEU format spec (2023-04-24, still current) does not cite a 7714 year; type-code glossary is pre-2025; do not quietly upgrade SEU students to 7714—2025 examples unless the school later says so.”

---

## 5. Zhejiang University / MOE-wide academic-degree review templates

**U / FAIL.** The previously failed ZJU CS doctoral review-form PDF was not recovered. No new public PDF of a ZJU academic-degree 评阅书 with a working URL was obtained. ZJU Graduate School “表格下载” pages (e.g. http://www.grs.zju.edu.cn/bgxz_62941/list.htm) were located by search as likely holding an anonymised doctoral review form or system-generated forms; those pages were not successfully downloaded as a filled official template this round.

**E.** No Ministry of Education **nationwide academic-degree (非专业学位)** review-form template was found. What exists, as in Round 2, are **school** forms. A current academic-degree example, distinct from the professional-doctorate forms already treated in Round 2, was obtained from Fudan University Graduate School, page dated **2025-07-01**: https://gs.fudan.edu.cn/_t221/ac/08/c2881a240648/page.htm. The page separates 学术学位博士 / 专业学位博士 / 学术学位硕士 / 专业学位硕士, and further splits academic forms into 人文社科 and 自然科学, plus open and double-blind variants.

**E.** The academic-degree, natural-sciences PhD review form was downloaded: https://gs.fudan.edu.cn/_upload/article/files/f4/a1/5a64d2564fcbbdca3126afe55b1d/582c2d82-6a6e-44ef-ae11-913dd3581df2.pdf (local: `round3-sources/fudan-phd-review-academic-ns-2025.pdf`, 7 pages). Salient rules from that form:

- The applicant’s self-evaluation page requires **论文的主要创新点（仅罗列要点）** in three numbered slots, plus 不足之处及改进设想.
- Reviewers score four indicators, each on a **百分制**: **选题** (前沿性和开创性; 理论/现实意义; 对国内外现状的归纳总结); **创新性及论文价值** (新的科学发现; 对解决自然科学或工程技术中重要问题的作用; 对科技发展和社会进步的影响和贡献); **基础知识及科研能力** (坚实宽广的理论基础与系统深入的专门知识; 方法的科学性与引证的翔实性; 独立从事科学研究的能力); **论文规范性** (引文规范性与学风严谨性; 文字准确性、流畅性与结构逻辑性).
- An “异议” is defined if **any** of: overall academic-level judgement is “差”; the defence conclusion is “须作重大修改, 重新送审通过后答辩” or “不同意”; **any indicator is below 60**. An objected thesis must be revised for **at least three months** and pass re-review before defence.
- Overall level: A 优秀 / B 良好 / C 一般 / D 差. Defence recommendation: A 同意; B 基本同意, 略作修改后答辩; C 须作重大修改, 重新送审; D 不同意.

The double-blind sibling PDF was also downloaded (same directory, file `30394939-342f-4acd-a4a9-78bd9247ec1a.pdf`) but not fully re-typed; it is the blind counterpart of the same academic-NS instrument.

**S.** ThesisForge’s reviewer-mode checklist for *academic* CS/EE theses can add this Fudan 2025 academic-NS axis set (选题 / 创新性及论文价值 / 基础知识及科研能力 / 论文规范性), the “list the innovation points, at least as three bullets” applicant instruction, and the “any criterion < 60 = 异议” rule — clearly labelled as a **Fudan 2025 school form**, not as an MOE-wide academic template. It complements, and should not be collapsed into, the Xidian 2025 20/20/50/10 review weights already encoded from Round 2, or the 学位办〔2024〕18号 professional-doctorate standard.

---

## 6. Journal of Semiconductors / 半导体学报 author guide

**FAIL.** https://www.jos.ac.cn/news/PreparingYourManuscript.htm returned **HTTP 502** to WebFetch (same family of failures as Round 2). Searches for an IOP / iopscience “Journal of Semiconductors” author-guidelines page did not return that journal’s official guide (hits were for other IOP journals). No cached official PDF was obtained.

**U.** Search-index snippets that quote title-word caps, a 200-word abstract, 3–6 keywords, or a “usually at least 15 references, of which at least 10 from the last five years” rule are **not encoded**. The 半导体学报 venue card remains a stub marked **U**, as in Round 2.

The official URL to retry later is still https://www.jos.ac.cn/news/PreparingYourManuscript.htm.

---

## 7. Ghione T-ED editorial; standing TCAS-I / TCAS-II Information for Authors

### 7.1 T-ED standing Information for Authors — this is the more important catch

**E.** The current IEEE Electron Devices Society page **Information for Authors** for IEEE Transactions on Electron Devices, https://eds.ieee.org/publications/transactions-on-electron-devices/information-for-authors, contains a standing heading **“Adequate Validation”**:

> T-ED welcomes manuscripts reporting solid, rigorous research outcomes centering round devices with adequate validation. Therefore, **submissions should generally include at least partial direct physical validation of the results.**

This is the current journal IFA, not only an editorial. It confirms, in official standing language, the Round-1/2 default that T-ED generally wants at least partial physical validation. The adverb is **“generally”**, not “always”; the IFA text obtained this round does not itself spell out exceptions for purely methodological TCAD papers.

Other IFA facts from the same page, useful for a T-ED venue card: typical regular-paper initial submission **limited to seven pages** including references, with manuscripts above seven and up to eight subject to obligatory overlength charges; review papers should not exceed **twelve** pages on initial submission; abstract **150–250 words**, one paragraph, no displayed equations or tables, self-contained; Briefs are short reports whose standard length is **4 published pages**. A PDF twin at https://eds.ieee.org/images/files/Publications/ted-info-for-authors.pdf returned **HTTP 418** this round; the HTML IFA was used instead.

### 7.2 Ghione 2019 editorial — legally posted, PDF still blocked this round

**E.** The EDS “Editorials for Authors and Reviewers” index, https://eds.ieee.org/publications/editorials-for-authors-and-reviewers, lists both Giovanni Ghione, *Looking for quality in TCAD-based papers*, and Enrico Sangiorgi, *Quality in Simulation-Only Manuscripts Submitted to J-EDS*.

**E.** Politecnico di Torino’s institutional repository records the Ghione editorial as an open author-accepted manuscript: https://iris.polito.it/handle/11583/2878716 (also `https://hdl.handle.net/11583/2878716`). The handle page was fetched. It identifies the work as Ghione G., 2019, and lists two files: a version-of-record PDF marked accesso riservato, and **`G Ghione Editorial T-ED Issue 8 2019 V2.pdf`**, 168.42 kB, marked **accesso aperto**, licence “Pubblico - Tutti i diritti riservati”, typologia “Post-print / Author’s Accepted Manuscript”. The VoR citation remains IEEE T-ED, DOI https://doi.org/10.1109/ted.2019.2924360.

**FAIL.** Direct download of the open AAM PDF (both `/retrieve/handle/11583/2878716/…` and the shorter `/retrieve/e384c433-…` paths) returned **HTTP 403** (Cloudflare challenge) to curl, and **HTTP 429** to WebFetch. The full wording of the editorial — including any stated exceptions for methodological or theory-only TCAD papers — is therefore still **U** as a quotation, even though a legal open copy is known to exist at that handle. No unauthorised copy was used. The Sangiorgi J-EDS editorial was not obtained as a PDF either.

**S.** Encode the **standing T-ED IFA “generally … at least partial direct physical validation”** sentence as the default device-paper rule. Keep Ghione (and Sangiorgi) as named editorials to be read when the PDF can be retrieved, and do not invent their exceptions. This is tighter than Round 2, which had to lean on a still-blocked editorial for the same default.

### 7.3 Standing TCAS-I and TCAS-II Information for Authors (fetched)

**E.** TCAS-I Guidelines for Authors, https://ieee-cas.org/publication/TCAS-I/TCAS-I-guidelines-authors: scope is theory, analysis, design, and practical implementation of circuits, and the application of circuit techniques to systems and signal processing. Submitted papers “are expected to contain new results, ideas, or innovations that advance significantly the state-of-the-art.” Papers at the border with communications, control, or signal processing “will focus on the impact that a particular … algorithm or control theoretical result may have on the design/implementation/performance of the corresponding circuit or system.” Power-electronics papers should “clearly exploit circuit theoretic methodologies … or present significant results in the integrated circuit implementation.” Single-blind review, minimum two reviewers. The page links an “EDICs Content upd July 2025” PDF (85.7 KB) which was not separately downloaded. **The fetched IFA does not contain a standing sentence that “TCAS-I never accepts simulation-only papers.”** A search-index remark that regular papers are “typically 7–11 pages, maximum 14” was **not** on the fetched page and is **U**.

**E.** TCAS-II Guidelines for Authors, https://ieee-cas.org/publication/TCAS-II/guidelines-author: brief papers in the same field of interest. **Standing, strict length rule:** “All TCAS-II manuscript submissions must adhere to the strict page length requirement of **4.5 pages for Content and 0.5 for References (total 5 pages)**. The last column is reserved ONLY for references. This is a strict formatting requirement. If any other information is present in the last column of the submission, it will be returned to the authors.” Single-blind review, minimum two reviewers. **The fetched standing IFA does not contain a blanket ban on simulation-only regular briefs.** The Round-2 finding that at least one special-issue CFP barred simulation-only papers remains a special-issue rule, not a TCAS-II bylaw.

**S.** Do not encode “TCAS never accepts simulation-only papers.” Encode: implementation claims should plan measurement; special issues may tighten that; TCAS-II has a hard 4.5+0.5 page format; T-ED (not TCAS) is the venue with a standing “generally partial physical validation” sentence.

---

## 8. Jeruchim 1984 and legal BER / Monte Carlo CI derivations

**Not obtained, not used.** Jeruchim, “Techniques for Estimating the Bit Error Rate in the Simulation of Digital Communication Systems,” IEEE JSAC 2(1):153–170, Jan. 1984, DOI https://doi.org/10.1109/JSAC.1984.1146031, remains paywalled. No legally posted author or university copy of that article was found. No unauthorised copy was used.

Two candidate open tutorials were located and then failed:

- George Mason University course notes, *Simulation of Wireless Communication Systems using MATLAB*, http://www.spec.gmu.edu/~pparis/classes/resources_732/simulation.pdf — **HTTP 500**.
- A Missouri S&T Scholars’ Mine faculty-work PDF, https://scholarsmine.mst.edu/cgi/viewcontent.cgi?article=2877&context=ele_comeng_facwork — **HTTP 403**.

**U.** Search-index paraphrases that “about 400 errors give 95% confidence at 10% relative error, because (1.96/0.1)^2 is about 384,” or that “10 errors give a factor of about 2, 100 errors a factor of about 1.3,” are **not encoded**. They were not read in a full legal text this round.

**S.** ThesisForge should **refuse to invent or hard-code a numeric error-event rule** until a legal primary derivation (Jeruchim 1984, or a later open tutorial that actually derives the formula) is in hand. The already-encoded legal procedure remains **Pawlikowski, Jeong, Lee 2002** (Canterbury copy, Round 2): sequential, coverage-based stopping, no folklore N. A future v3 may add a formula-level BER CI only from a fetched derivation, honestly cited.

---

## 9. ACM TOCS / TON, ACM Master Article Template, and Elsevier Computer Networks / Microelectronics Journal Guides for Authors

### 9.1 IEEE/ACM Transactions on Networking — fetched

**E.** The official submissions page https://sites.google.com/view/ieee-acm-ton/submissions was fetched in full. Standing rules that may be encoded on a TON venue card:

- Scope: papers on social networks, smart grid, or physical-layer communications are **outside the scope**.
- Format: two-column, single-spaced, 10-point; papers not meeting the format are returned before review.
- **Typical maximum length of submitted papers is 16 pages** in the two-column Transactions format. Extra material is preferably submitted as supplementary material; otherwise the length must be discussed with the EiC before submission, and the justification put in the cover letter.
- **Mandatory page charges:** 10 pages free; additional pages **$220 per page**. Academic authors unable to pay may apply for a waiver within 30 days of acceptance; non-academic authors are expected to cover charges. (These are publication charges, recorded as such, not writing rules.)
- **Abstract: 150–250 words**, one self-contained paragraph, no abbreviations, footnotes, references, displayed equations, or tables; include three or four keywords or phrases.
- Graphical abstracts are optional and are part of the technical content if supplied.
- No dual submission; no republication of a paper already published in a journal or book; conference papers may be submitted if they are not verbatim copies and include additional technical material as required by IEEE policy (the additional material need not be new results; it may be elaboration or proofs). arXiv / institutional / personal preprint posting is not treated as prior publication.
- Submission via the IEEE Author Portal, https://ieee.atyponrex.com/journal/TNET; ORCID required for all authors.
- Starting May 2024, the EiC reviews submissions weekly. The page states that the average and median times from editor assignment to a first decision are currently **five months**.

### 9.2 ACM TOCS — not fully fetched

**FAIL.** https://dl.acm.org/journal/tocs/author-guidelines timed out twice. Journal-specific TOCS page limits, abstract lengths, and Research-Highlights word caps remain **U**. A search snippet that “Research Highlights are shorter papers, typically about 5,000 words, and must include 25–30% new material” is **not encoded**. Until that page is fetched, ThesisForge may only reuse already-established ACM-wide policy (contribution-front review, authorship, artefact, simultaneous-submission rules).

### 9.3 Current ACM Primary Article Template — fetched

**E.** https://www.acm.org/publications/proceedings-template was fetched. Facts from that official page:

- The official LaTeX class is **acmart**; the page gives **Version 2.21**, “last update **November 3, 2026**.” (The footer also says “Document Last Revised: July 10, 2025 by Craig Rodkin and Bernadette Shade.” Both dates are on the same official page; report them as such.)
- “NOTE: Journal templates. **All journal use acmsmall** with the following exceptions: acmlarge — DGOV, DTRAP, HEALTH, IMWUT, JOCCH, TAP; acmtog — TOG.” **TOCS is not in the exception list**, so a TOCS submission should use `acmsmall` unless a later TOCS author-guidelines page says otherwise (**S**, cautious, pending the still-unfetched TOCS page).
- Conference proceedings use `sigconf` or SIGPLAN templates; fonts (libertine) must not be substituted; margin adjustments are not allowed.
- PACM journal authors are told to obtain the ACM Small template from the journal template webpage.
- CCS concepts and ACM-Reference-Format should be used; approved LaTeX packages only.

### 9.4 Computer Networks and Microelectronics Journal — official Guides for Authors, with numeric caps now in hand

**E.** Computer Networks (ISSN 1389-1286) Guide for Authors, fetched: https://www.sciencedirect.com/journal/computer-networks/publish/guide-for-authors.

**E.** Microelectronics Journal (ISSN 1879-2391) Guide for Authors, fetched: https://www.sciencedirect.com/journal/microelectronics-journal/publish/guide-for-authors.

Numeric and structural rules that appear **on both official pages** and may now be encoded on those venue cards (they are journal GFA text, not a generic rumour):

- **Abstract: a concise and factual abstract that does not exceed 250 words.** It should state the purpose, outline basic procedures, include main findings (and statistical significance where applicable) and principal conclusions, and emphasise what is new. The abstract must stand alone; avoid references and uncommon abbreviations (define any that are essential).
- **Keywords: 1 to 7**, in English; avoid multi-word keywords built with “and” or “of” where possible; abbreviations in keywords only if firmly established.
- **Highlights: encouraged** (not worded as mandatory). Submit as a separate editable file whose name includes the word “highlights”. **3 to 5 bullet points, each a maximum of 85 characters, including spaces.** They should capture novel results and any new methods.
- Graphical abstract: encouraged; image at least 1328 pixels wide, longest side horizontal, readable at 13 cm; TIFF / EPS / PDF / MS Office preferred.
- **Research data: Option C** — authors are required to deposit research data in a relevant repository and provide a link, or to make a statement explaining why sharing is not possible, which will appear in the published article.
- Reference style at submission may be any consistent style; the journal style is applied after acceptance. In-text references are numbered in square brackets. Dataset and software citation patterns are illustrated.
- Declaration of generative-AI use in manuscript preparation, if any, as a named section before the reference list; AI tools must not be listed as authors.

**E, Computer Networks only, from the same GFA:** the journal also publishes **Dataset Articles** and **Open-Source Software Articles** as “micro-articles” describing open datasets or open-source software used to obtain scholarly results (simulators, emulators, protocol implementations, monitoring tools, etc.). **Vitae:** “Please submit a short (**maximum 100 words**) biography of each author” plus a passport-type photograph, in an editable format.

**E, Microelectronics Journal only, from the same GFA:** article types include original papers, case studies, conference reports, book reviews, letters; review articles should be discussed with the Editor first. A “Theory and calculation” structural note: the theory section should extend the introduction; the calculation section should be a practical development from a theoretical basis. Reviewer suggestions are requested (not colleagues or recent collaborators, not editorial-board members, preferably from different countries).

**S.** Elsevier mode in ThesisForge can now carry a **filled venue card** for these two journals (250-word abstract, 1–7 keywords, optional 3–5 highlights at no more than 85 characters including spaces, Option C data, GenAI declaration), instead of the Round-2 instruction to “open the current GFA and fill the card” with the numeric caps left blank. Other Elsevier journals may share this pattern but must still be checked individually; do not generalise the 85-character highlight cap to every Elsevier title without that title’s GFA.

---

## 10. Chen Haoyuan / cjstp essays, and CY/T 173 (keywords)

### 10.1 CY/T 173—2019 — official full text obtained

**E.** GB/T 7713.1—2025 clause 5.2.9 (already established in Round 2) requires keywords to be written in conformity with **CY/T 173**. The official full text of **CY/T 173—2019《学术出版规范 关键词编写规则》** was downloaded from the National Press and Publication Administration: https://www.nppa.gov.cn/xxgk/fdzdgknr/hybz/202210/P020221004608864960855.pdf (local: `round3-sources/cyt173-2019-nppa.pdf`, 8 pages). The official announcement page is https://www.nppa.gov.cn/xxgk/fdzdgknr/hybz/202210/t20221004_445182.html. Issued 2019-05-29, in force 2019-07-01, 国家新闻出版署. A university mirror also exists at https://xuebao.xaut.edu.cn/CYT173-2019.pdf (not needed once the NPPA file was in hand).

**E. Scope (clause 1):** the standard “规定了**学术期刊论文**关键词编写的基本要求、论文审读、主题分析、选词和编排规则。” “本标准适用于学术期刊论文的编辑出版工作。**其他出版物可参照使用。**” Theses are “other publications” that 7713.1 tells authors to write keywords in conformity with this standard; they are not the primary addressee.

**E. Operative rules to encode (with that scope caveat):**

- 4.2 Keywords shall accurately and fully reveal the theme; important retrievable content shall not be omitted.
- 4.3 “根据学术论文研究的深度和广度, **宜选择 3～8 个关键词**.”
- 4.4 “学术论文**应编写英文关键词**.”
- 5.1 Prioritise title, abstract, section headings, and conclusions; browse key sections or the full text when needed. 5.2 “不应仅依据题名进行主题分析.”
- 6.x Core subject factors shall be indexed as necessary factors; limiting modifiers, concrete research content, closely related purpose/conclusion/use, new or improved methods, and limiting time/space factors shall be indexed when they qualify; a place name with no necessary link to the theme is given as a negative example (“不宜标引”).
- 7.1 Choose words that clearly express the subject concept. 7.2 Use recognised standard terms of the field; scientific nouns shall follow CY/T 119 (examples: “脚踏车” to “自行车”; “电脑” to “计算机”). 7.3 Work titles as keywords take book-title marks. 7.4 Words with a specific meaning take quotation marks (example: “一带一路”).
- **8.2.1** 关键词宜置于摘要之后. **8.2.2** 在关键词之前宜加“关键词”字样, 并在其后加冒号. **8.2.3** **关键词之间宜用分号隔开, 最后一个关键词后面不加标点符号.**
- Keywords should be ordered by importance: core-theme keywords first, non-core later (clause 8, as extracted).

**S.** This officially confirms the 3–8 keyword band that 7713.1 already states, and adds operational craft (do not index from the title alone; standard terms; semicolon separators; no terminal punctuation; English keywords). School overlays that tighten the band to 3–5 (Tsinghua, PKU) still win for those schools. CY/T 173’s “应编写英文关键词” is written for journal articles; a thesis already has a matched English keyword list under 7713.1 and most school manuals.

### 10.2 GB/T 6447—2025 clauses confirmed from the typeset copy (abstract stance)

**E.** From the CNKI-hosted typeset 6447—2025 (§1.5):

- 4.1 Length should be determined by content, type, field, information load, and need; **content is the decisive factor**.
- 4.2 “通常**报道性摘要以 400 字左右、报道-指示性摘要以 300 字左右、指示性摘要以 150 字左右**为宜, 视频摘要播放时长以 **2 min～5 min** 为宜.”
- 4.3 The foreign-language abstract of a Chinese document should correspond to the Chinese abstract and may be longer if needed, and conversely.
- 5.1–5.4 elements: 目的 / 方法 / 结果 / 结论, with a note that a reporting abstract usually treats results and conclusions in more detail and purpose briefly, and an indicative abstract the reverse.
- **6.1 (一段式摘要), author-written abstracts:** “一次文献作者编写并作为文献的一个有机组成部分的摘要, **既可采用第三人称, 也可采用第一人称, 如 ‘我们’ ‘笔者’ ‘本文’ 等**; 由一次文献作者之外的第三方人员编写的二次文献摘要, 应采用第三人称.” (Clause numbering in the extracted text is typographically cramped as “1.6.3”; the substance sits under 6.1 一段式摘要.)
- 7.1 Abstracts are a brief statement of the content **without commentary or added interpretation**, and should be objective, independent, and self-contained.
- 7.2 Exclude what is already common knowledge in the field. 7.3 Do not merely repeat the title, and do not copy-paste the body; summarise accurately.
- 7.8 Placement: after the title (page), before the body; theses and S&T reports with a contents page shall follow GB/T 7713.1 / 7713.3 and start on a new page. Academic-article abstracts follow GB/T 7713.2.

These confirm the Round-2 first-person clash: 6447 **permits** 本文 / 我们 / 笔者 in author-written abstracts; Tsinghua, PKU, and 通信学报 (already fetched) forbid or avoid first person. Venue or school wins for the document being written.

### 10.3 Chen Haoyuan / cjstp essays

**FAIL.** Targeted cjstp PDF endpoints (`https://www.cjstp.cn/EN/article/downloadArticleFile.do?attachType=PDF&id=4258` and `…/id=4373`) returned empty replies. No stable full text of a Chen Haoyuan hedging or STM-style essay was obtained. Chen Haoyuan is, from texts already in hand, a listed drafter of **GB/T 7714—2025** and of **GB/T 6447—2025**; that biographical fact does not substitute for the essays. The ZH stance band should be thickened from 6447 and CY/T 173 (this round) and from the already-fetched Chinese journal author guides, **not** from unsourced “Chen says…” folklore.

---

## 11. Have 2025–2026 Tsinghua / PKU / UCAS notices started pointing at 7713.1—2025 / 7714—2025?

**E. Tsinghua Library — yes, as a library research-help page, dated after the 7714 implementation date.**\
https://lib.tsinghua.edu.cn/info/1147/3359.htm, dated **2026-06-30**, under “中文文章写作 / 现行的国家标准”, lists:

- 《信息与文献 参考文献著录规则 **GB/T 7714-2025**》: 适用于著者和编辑著录参考文献.
- 《信息与文献 编写规则第 1 部分：学位论文 **GB/T7713.1-2025**》: 适用于印刷型、缩微型、电子版、网络版等形式的学位论文.

**E. Tsinghua writing guide — not yet, as of the already-established 2025-03 PDF.** The graduate writing guide fetched in Round 2 (https://www.tsinghua.edu.cn/__local/A/A3/A8/948F85164440B1073B73B3BAA9D_1AF5B731_137B8F.pdf, page https://www.tsinghua.edu.cn/info/1492/122142.htm) still cites GB/T 7713.1—2006 and GB/T 7714—2015. A 2026-06-30 library help page is **not** automatically a replacement of the Graduate School writing guide. No 2026 Tsinghua *graduate-school* writing-guide revision was obtained this round.

**U. PKU.** No 2025–2026 Peking University graduate-school or library notice that cites 7713.1—2025 or 7714—2025 was fetched. Hits pointed at older 7714—2015 PDFs (e.g. a philosophy-library copy of the 2015 standard). The official writing guide remains the 2018/2019 PDF already in hand, which cites even older GB editions. Do not upgrade PKU overlays on the strength of search synthesis.

**U. UCAS.** No 2025–2026 学位办 notice citing the 2025 GB editions was obtained (see §2). The live instrument is still 校发学位字〔2022〕40号 in 2024-updated clothing.

**E. Other universities have started posting the 2025 stack.** Huaqiao University Graduate School, 2026-03-01, https://grs.hqu.edu.cn/info/1078/17770.htm, lists both GB/T 7713.1—2025 and GB/T 7714—2025 as current national standards for theses (PDF attachments themselves failed to download, §1.2).

**S.** ThesisForge should implement a dated “who has switched” table, not a blanket “all elite schools now use 2025”:

| Institution | 2025 GB stack pointed to? | Evidence in hand |
| --- | --- | --- |
| National default | Yes, from the official in-force dates | 7713.1 from 2026-02-01; 7714 from 2026-07-01 |
| Tsinghua Library help page | Yes, 2026-06-30 | Fetched page |
| Tsinghua writing guide (2025-03) | No, still 2006/2015 | Round 2 PDF |
| PKU writing guide | No, still 1987/2005 | Round 2 PDF; no 2026 notice fetched |
| UCAS 40号 (2024 update) | Not shown | Full text not fetched; no contrary 2026 notice fetched |
| SEU format spec (2023-04-24, still current) | No year cited; pre-2025 type-code glossary | This round, identical to Round 2 PDF |
| Xidian 2026 notice | Template still “2015年修订版” | 2026-01-05 notice |
| Huaqiao University Graduate School | Yes, 2026-03-01 | Fetched page (files themselves failed) |

When the school overlay still cites a superseded GB, warn, and follow the school typography/abstract overlay plus the national default for anything the school does not specify.

---

## 12. Other high-value operational methods not already encoded from Rounds 1–2

The following were legally fetched this round and would materially improve v3 checklists. They are listed here rather than forced into the twelve priority headings.

1. **T-ED standing “Adequate Validation” sentence** (§7.1) — upgrade the device-experiment checklist from “editorial, PDF blocked” to a current IFA rule: generally at least partial direct physical validation.
2. **TCAS-II hard format** (§7.3): 4.5 pages of content + 0.5 page of references, last column references only.
3. **TON venue card** (§9.1): 16-page typical cap, 150–250-word abstract, out-of-scope topics, conference-to-journal increment policy, $220/page after 10 pages.
4. **Filled Elsevier venue cards** for Computer Networks and Microelectronics Journal (§9.4), including Computer Networks’ dataset and open-source-software micro-article types and 100-word vitae.
5. **CY/T 173 keyword craft** (§10.1) and confirmed 6447 length / first-person / no-commentary rules (§10.2).
6. **Fudan 2025 academic-degree (natural sciences) review form** (§5): four scored axes, three listed innovation points, <60 on any axis = 异议, three-month minimum revision. No MOE-wide academic template was found; encode this as a school template, and keep looking for ZJU.
7. **Xidian 2026 similarity thresholds** (§4.1) for the review-and-submission checklist (STEM PhD 10% / 20%; STEM master’s 15% / 30%), clearly labelled as Xidian’s 2026 notice, not a national default.
8. **7714—2025 typeset confirmations** of 7.1.1 capitalisation, 7.1.2 three-author band, 7.9 PID, 8.14/8.15 formats, Table A.1 (including the absence of a computer-program chapter), and the confirmed Zotero inconsistency (§1).
9. **ACM acmart 2.21 / November 2026** and the “all journals use acmsmall except …” list (§9.3).
10. **“Who has switched to the 2025 GB stack” table** (§11).

Nothing in this list is a substitute for Jeruchim, for a UCAS/BUPT full text, or for the 半导体学报 guide.

---

## 13. Disagreements and corrections

1. **GB/T 7714—2025 Zotero example, now confirmed in typeset type:** clause 8.11.3 example [5] uses `[CP/OL]`; appendix B.10 example [13] uses `[EB/OL]` for the same item. Additionally, **8.11 is “网站、网页”, not a computer-program clause** — this corrects the Round-2 HTML/OCR characterisation. Prefer neither example as a hidden official resolution.
2. **Tsinghua is internally split:** the Library help page of 2026-06-30 points at 7713.1—2025 and 7714—2025; the Graduate writing guide of 2025-03 still points at 2006/2015. Encode both, and do not pretend the guide has been revised.
3. **SEU format spec vs national default:** the still-current 2023-04-24 spec does not cite a 7714 year and still glosses EB as “电子公告”; 7714—2025 Table A.1 redefines EB as 网站、网页. Do not silently modernise SEU citations.
4. **First person in abstracts:** 6447—2025 (typeset, re-confirmed) allows 本文 / 我们 / 笔者 in author-written abstracts; Tsinghua, PKU, and 通信学报 do not. Venue or school wins.
5. **Official SAMR will not host 7713.1 / 7714 full text** because they adopt ISO standards. University typeset copies are the practical source; they are official-equivalent, not openstd downloads.
6. **Simulation-only papers:** T-ED IFA now supplies the standing “generally … at least partial direct physical validation” rule. TCAS-I/II standing IFAs fetched this round do **not** contain a blanket simulation-only ban. Special-issue bans remain special-issue bans. Ghione’s full wording is still unquoted because the legal AAM PDF was Cloudflare-blocked.

---

## 14. (A) Concrete additions ThesisForge v3 MUST encode

Suggested file targets are under `/workspace/ThesisForge` for a future editing pass. **This round did not edit those files.**

| ID | Addition | Suggested target |
| --- | --- | --- |
| A1 | Correct the 7714—2025 software/webpage account from the CUEB typeset copy: no computer-program chapter; 8.11 / B.10 are 网站、网页; Table A.1 keeps CP, DB, EB=网站、网页, DS, PP; confirm `[PP/OL]`, `[DS/OL]`, 7.9 PID, 7.1.1 initial-capital surnames (not ALL CAPS), 7.1.2 “no more than 3 all / more than 3 may take first 3 + 等”. Flag the typeset Zotero `[CP/OL]` vs `[EB/OL]` inconsistency as unresolved. | `references/gbt-7714-2025.md` |
| A2 | Record that official SAMR/openstd typeset full texts of 7713.1—2025 and 7714—2025 are withheld for ISO-copyright reasons; university typeset/PDFs remain the working texts. Keep the Round-2 7713.1 clauses. Optionally note the HQU 2026-03-01 posting (files themselves not downloaded). | `references/gbt-7713.1-2025.md`, `references/gbt-7714-2025.md` |
| A3 | Encode GB/T 6447—2025 typeset clauses 4.1–4.3 (400 / 300 / 150 字 bands; 2–5 min video abstract), 6.1 first-person permission for author-written abstracts, 7.1–7.3 no-commentary / no title-echo / no copy-paste. Keep the venue/school override for first person. | `references/gbt-6447-2025.md`, `references/style-and-stance.md` |
| A4 | Encode CY/T 173—2019 from the NPPA official PDF: scope = journal articles, other publications may follow; 宜 3–8 keywords; English keywords for journal articles; do not index from the title alone; standard terms (CY/T 119); semicolon separators, no terminal punctuation; core keywords first. Note 7713.1 5.2.9 points here; school 3–5 overlays still win. | `references/cyt-173-2019.md`; keyword section of `templates/` |
| A5 | School-overlay updates: UCAS current *named* instrument is 校发学位字〔2022〕40号 (2024-10 update), full numbers still **U**; BUPT current *named* instrument is the 2025-01-15 写作与制作规范, page HTTP 412, typography **U**; Xidian 2026 notice still requires the “2015年修订版” template (2025-01 Word file exists but was not read) and publishes similarity thresholds; SEU 2023-04-24 spec is unchanged and cites no 7714 year. | `references/school-overlays.md` or `references/schools/` |
| A6 | “Who has switched to the 2025 GB stack” table from §11, especially Tsinghua Library 2026-06-30 vs Tsinghua writing guide 2025-03. | `references/school-overlays.md` |
| A7 | Fudan 2025 academic-NS PhD review form: four 百分制 axes, three listed innovation points, any axis below 60 or “差” / “不同意” / “重大修改重审” = 异议, at least 3 months’ revision. Label as a school academic-degree form, not an MOE-wide template. No MOE-wide academic (non-professional) template was found. | `templates/review-checklist.md`; `references/schools/fudan-review-2025.md` |
| A8 | Device / circuit venue cards: T-ED IFA “Adequate Validation — submissions should generally include at least partial direct physical validation of the results”; T-ED length/abstract caps from the same IFA; TCAS-II 4.5+0.5 page rule; TCAS-I/II standing IFAs do not ban simulation-only papers. Keep Ghione/Sangiorgi as named editorials whose full text is still outstanding. | `references/venues-ieee-eds-cass.md`; `references/experiment-design.md` |
| A9 | ACM / Elsevier venue cards: TON rules from the official submissions page; acmart 2.21 (2026-11-03) and acmsmall-as-default for journals; Computer Networks and Microelectronics Journal GFA caps (abstract no more than 250 words, 1–7 keywords, 3–5 highlights no more than 85 characters including spaces, Option C data); Computer Networks dataset/OSS micro-articles and vitae no more than 100 words. TOCS-specific caps remain **U**. | `references/venues-acm-elsevier.md`; `references/elsevier-venue-card.md` |
| A10 | Experiment-design: do **not** encode a numeric BER / error-event rule. Keep Pawlikowski 2002. Record Jeruchim 1984 and the two open-tutorial URLs as still unfetched. | `references/experiment-design.md` |

---

## 15. (B) Residual unknowns that should stay unmarked rather than guessed

1. Official SAMR typeset PDFs of GB/T 7713.1—2025 and 7714—2025 (withheld for ISO copyright; not a fetch glitch). An official erratum, if any, that resolves the Zotero `[CP/OL]` / `[EB/OL]` clash.
2. The **full text** of UCAS 校发学位字〔2022〕40号 and the 2024-10 各学科群具体要求 (downloads 404/500). Abstract and reference-count rumour figures stay **U**.
3. The **full text** of BUPT《研究生学位论文写作与制作规范（2025年1月15日）》 (official page HTTP 412). Typography, abstract windows, and the GB edition cited stay **U**.
4. The contents of Xidian’s `…模板（2015年修订版）-2025.01修订.docx` and `研究生学位论文详细摘要的撰写要求.doc` — existence is official; typography and detailed-abstract numbers are still **U**.
5. A working ZJU (or other EE/CS) 评阅书 PDF, and any MOE-wide *academic-degree* review template (none found; only school forms).
6. 半导体学报 / Journal of Semiconductors author guide (jos.ac.cn still 502; no IOP mirror fetched).
7. The full wording of Ghione 2019 (legal AAM is at iris.polito.it but Cloudflare-blocked this round) and of Sangiorgi’s J-EDS simulation-only editorial.
8. A legal, complete Jeruchim 1984 or a later open tutorial that actually derives a BER / Monte Carlo CI formula (GMU 500; MST 403).
9. ACM TOCS author-guidelines numbers (dl.acm.org timeout).
10. Chen Haoyuan / cjstp full essays (cjstp PDF endpoints empty).
11. A PKU or UCAS 2026 notice that cites 7713.1—2025 / 7714—2025 (not found). Whether Tsinghua Graduate School has issued, or will issue, a writing-guide revision that matches the Library’s 2026-06-30 help page.
12. TCAS-I numeric page caps (a search-snippet “7–11, max 14” was not on the fetched IFA page).

---

## 16. (C) Source list (URLs and fetch status)

Status key: **OK** = full page or PDF obtained and used; **FAIL** = attempted, failure mode recorded; **LOCATED** = official record or attachment found but full text not obtained; **NOT USED** = avoided (paywall or unofficial copy).

| # | Source | URL | Status |
| --- | --- | --- | --- |
| 1 | GB/T 7713.1—2025, openstd record | https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=36C05B5738C54D42B4B262525320B52F | OK as a record (no full text; copyright withhold) |
| 2 | GB/T 7713.1—2025, SAMR detail | https://std.samr.gov.cn/gb/search/gbDetailed?id=3B46A026CC84469CE06397BE0A0AEEB8 | OK as bibliographic record (ISO 7144:1986 NEQ) |
| 3 | GB/T 7714—2025, openstd record | https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14 | OK as a record (no full text; copyright withhold) |
| 4 | GB/T 7714—2025, SAMR detail | https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F | OK as bibliographic record (ISO 690:2021 NEQ) |
| 5 | GB/T 7714—2025, CNIS / 国家标准馆 | https://ndls.cnis.ac.cn/standard/detail/5ff4aa78a1e9a5952b78c2ea5490177b | LOCATED (purchase / in-person reading, no free PDF) |
| 6 | GB/T 7714—2025, CUEB typeset PDF | https://rem.cueb.edu.cn/docs/2026-04/ab13582039564d9090a722f17cfcbf2e.pdf | OK (PDF, 48 pp, typeset, school-watermarked) |
| 7 | GB/T 6447—2025, openstd record | https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=F70F4968628FFF58FF5AE7414A815CC8 | OK as a record (preview/download offered) |
| 8 | GB/T 6447—2025, CNKI-hosted typeset PDF | https://publishmedia.cbpt.cnki.net/portal/minio/webs/wuji/media/web/2026/05/14/GBT6447-2025%E6%96%87%E7%8C%AE%E6%91%98%E8%A6%81%E7%BC%96%E5%86%99%E8%A7%84%E5%88%99-2025.pdf | OK (PDF, 11 pp) |
| 9 | GB/T 6447—2025, Shandong University journal copy | https://lxbwk.njournal.sdu.edu.cn/fileup/1671-9352/ITEM/20250813124422.pdf | LOCATED (same typeset; not re-downloaded) |
| 10 | Huaqiao University, national-standards posting, 2026-03-01 | https://grs.hqu.edu.cn/info/1078/17770.htm | OK (HTML). Attachment PDFs FAIL (HTML stub “附件下载”, 3829 B) |
| 11 | CY/T 173—2019, NPPA official PDF | https://www.nppa.gov.cn/xxgk/fdzdgknr/hybz/202210/P020221004608864960855.pdf | OK (PDF, 8 pp) |
| 12 | CY/T 173—2019, NPPA announcement | https://www.nppa.gov.cn/xxgk/fdzdgknr/hybz/202210/t20221004_445182.html | OK |
| 13 | UCAS EECE writing-guide page (2024-10 update) | https://eece.ucas.ac.cn/index.php/zh-cn/2014-06-13-06-47-02/2014-06-13-06-48-14/1535-2018-10-22-02-11-12 | OK (HTML). Attachments FAIL (404 / 500) |
| 14 | UCAS AI School, 校发学位字〔2022〕40号 page | https://ai.ucas.ac.cn/index.php/zh-cn/jxjy/fzpy1/7293-2022-40 | OK (HTML; zip not downloaded) |
| 15 | UCAS SDC English guidelines page | https://sdc.ucas.ac.cn/index.php/international-students/degree-information/1306-university-of-chinese-academy-of-sciences-degree-thesis-dissertation-guidelines | OK (HTML) |
| 16 | UCAS Hangzhou IAS, 2024-06 discipline-group requirements | http://hias.ucas.ac.cn/life/info/1515/2088.htm | OK (HTML; zip not downloaded) |
| 17 | BUPT Graduate School notice | https://grs.bupt.edu.cn/info/1035/3071.htm | FAIL (HTTP 412). Document identity LOCATED from official page title/attachments via search-retrieved text |
| 18 | Xidian 2026 degree-application notice, 2026-01-05 | https://gr.xidian.edu.cn/info/1044/17974.htm | OK (HTML) |
| 19 | Xidian academic-master’s materials / 2015 template listing | https://gr.xidian.edu.cn/info/1047/5087.htm | OK (HTML). The 2025-01 DOCX itself not downloaded |
| 20 | SEU format-spec page, 2023-04-24 | https://seugs.seu.edu.cn/2023/0424/c28878a442680/page.htm | OK (HTML) |
| 21 | SEU format-spec PDF | https://seugs.seu.edu.cn/_upload/article/files/5d/c2/abe9785f44c8b3ea4823f14bfb92/cd829a73-1b86-400d-9bce-2c4b4fdb85b7.pdf | OK (PDF, 12 pp; MD5 identical to Round 2) |
| 22 | Fudan review-form index, 2025-07-01 | https://gs.fudan.edu.cn/_t221/ac/08/c2881a240648/page.htm | OK (HTML) |
| 23 | Fudan academic-NS PhD review form | https://gs.fudan.edu.cn/_upload/article/files/f4/a1/5a64d2564fcbbdca3126afe55b1d/582c2d82-6a6e-44ef-ae11-913dd3581df2.pdf | OK (PDF, 7 pp) |
| 24 | Fudan academic-NS PhD review form, double-blind | https://gs.fudan.edu.cn/_upload/article/files/f4/a1/5a64d2564fcbbdca3126afe55b1d/30394939-342f-4acd-a4a9-78bd9247ec1a.pdf | OK (PDF downloaded; not fully re-typed) |
| 25 | ZJU CS doctoral review form (Round 2 URL) | https://cs.zju.edu.cn/_upload/article/files/c6/1b/ce73afe1471caa5aab9e581d4ae4/e496d7db-ab58-4cdc-81d7-5b77b537ec1e.pdf | Not blindly retried; no new working PDF found (U) |
| 26 | Journal of Semiconductors, Preparing Your Manuscript | https://www.jos.ac.cn/news/PreparingYourManuscript.htm | FAIL (HTTP 502) |
| 27 | EDS editorials index | https://eds.ieee.org/publications/editorials-for-authors-and-reviewers | OK (HTML; lists Ghione and Sangiorgi) |
| 28 | T-ED Information for Authors | https://eds.ieee.org/publications/transactions-on-electron-devices/information-for-authors | OK (HTML). PDF twin https://eds.ieee.org/images/files/Publications/ted-info-for-authors.pdf FAIL (HTTP 418) |
| 29 | Ghione 2019, Polito handle | https://iris.polito.it/handle/11583/2878716 | OK (HTML; AAM listed open). PDF FAIL (HTTP 403 / 429, Cloudflare) |
| 30 | Ghione 2019 VoR | https://doi.org/10.1109/ted.2019.2924360 | NOT USED (paywalled VoR; AAM preferred, but blocked) |
| 31 | TCAS-I Guidelines for Authors | https://ieee-cas.org/publication/TCAS-I/TCAS-I-guidelines-authors | OK (HTML) |
| 32 | TCAS-II Guidelines for Authors | https://ieee-cas.org/publication/TCAS-II/guidelines-author | OK (HTML) |
| 33 | Jeruchim 1984 JSAC | https://doi.org/10.1109/JSAC.1984.1146031 | NOT USED (paywalled; no legal author copy found) |
| 34 | GMU wireless-simulation notes | http://www.spec.gmu.edu/~pparis/classes/resources_732/simulation.pdf | FAIL (HTTP 500) |
| 35 | Missouri S&T “Simulation of Communication Systems” | https://scholarsmine.mst.edu/cgi/viewcontent.cgi?article=2877&context=ele_comeng_facwork | FAIL (HTTP 403) |
| 36 | IEEE/ACM TON submissions | https://sites.google.com/view/ieee-acm-ton/submissions | OK (HTML, full) |
| 37 | ACM TOCS author guidelines | https://dl.acm.org/journal/tocs/author-guidelines | FAIL (timeout, twice) |
| 38 | ACM Primary Article Template | https://www.acm.org/publications/proceedings-template | OK (HTML) |
| 39 | Computer Networks Guide for Authors | https://www.sciencedirect.com/journal/computer-networks/publish/guide-for-authors | OK (HTML, full, with numeric caps) |
| 40 | Microelectronics Journal Guide for Authors | https://www.sciencedirect.com/journal/microelectronics-journal/publish/guide-for-authors | OK (HTML, full, with numeric caps) |
| 41 | Tsinghua Library, references and writing formats, 2026-06-30 | https://lib.tsinghua.edu.cn/info/1147/3359.htm | OK (HTML) |
| 42 | cjstp PDF endpoints (ids 4258, 4373) | https://www.cjstp.cn/EN/article/downloadArticleFile.do?attachType=PDF&id=4258 and the CN equivalent for id=4373 | FAIL (empty reply) |

Local aides (not official URLs): `/workspace/thesisforge-research/round3-sources/` holds the successfully downloaded PDFs and extracted `.txt` files named above, including `gbt7714-2025-cueb-nospaces.txt` (whitespace-collapsed extraction of the typeset 7714 copy).

---

## 17. Round 3 conclusion

Round 3 closed several documentation gaps with primary or official-equivalent texts, and it corrected one important Round-2 reading. A typeset university-purchased copy of GB/T 7714—2025 confirms the worked patterns already slated for v2, shows that clause 8.11 is “网站、网页” (not a computer-program chapter), and confirms that the Zotero `[CP/OL]` / `[EB/OL]` clash is in the typeset standard itself. Official SAMR/openstd still will not release 7713.1 or 7714 full text because those standards adopt ISO documents. CY/T 173—2019 is now in hand from the NPPA, and GB/T 6447—2025 length and first-person clauses are re-confirmed from a typeset PDF. Tsinghua Library, as of 2026-06-30, points at the 2025 GB stack, while the 2025-03 writing guide has not been shown to follow; UCAS and BUPT manuals are identified by instrument and date but remain unread as full text; Xidian’s 2026 notice still requires the “2015年修订版” template. Standing T-ED, TCAS-I/II, TON, ACM template, and two Elsevier Guides for Authors are now in hand, including the T-ED “generally … at least partial direct physical validation” sentence and the actual Computer Networks / Microelectronics Journal highlight and abstract caps. A current Fudan academic-degree review form supplies a non-professional reviewer axis set. Jeruchim’s formula, Ghione’s full wording, 半导体学报, TOCS-specific caps, and Chen Haoyuan essays remain honestly **U**. No folklore numbers were filled in. ThesisForge skill files were not edited in this round.
