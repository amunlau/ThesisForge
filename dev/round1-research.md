# ThesisForge Round 1 Research Report

**Skill under design:** ThesisForge\
**Round:** 1 of at least 3 independent research-and-iteration cycles\
**Focus:** Foundations — Chinese dissertation standards, contribution claims, journal workflows, evaluation methodology, argument quality, failure modes, and writing guides\
**Research date:** 2026-11-11 (Asia/Shanghai)\
**Work location:** box only (`/workspace/thesisforge-research/`)\
**This document does not contain the ThesisForge skill itself.**

---

## 0. Research boundary, method, and evidence grades

### 0.1 Boundary

This round covers reusable *foundations* for a skill that will later support:

- Master's and PhD theses, and journal papers
- Default discipline: 计算机应用技术, also covering computer science, communications, and semiconductor/electronics
- Both writing and review: format, innovation claims, logic, polish
- Journal-side work: topic discovery, full-text design, experiment design, data analysis, and complete manuscripts written to venue rules
- Innovation and logical rigor calibrated to a competent human expert reviewer — tight enough, not pedantic, not excessively defensive
- A hard design constraint, reinforced by sources below: never fabricate experimental data or citations; design real experiments; analyze only real, honestly run simulation, or measurement data

This round does **not** draft skill instructions, workflows, or templates for ThesisForge. It inventories methods and checklists the skill must later encode, and it lists gaps for Round 2.

### 0.2 Method

- Prefer primary sources: official standards platforms, the Degree Law, university graduate-school or CS-school guides, publisher author instructions, and widely used methodology documents.
- Use secondary expert commentary (faculty blogs, writing guides, reviewer essays) only when labeled as such.
- Do not invent standard numbers, quotations, or page numbers. Short quotations are taken only from pages successfully fetched or from clearly attributed public excerpts. If a page failed to fetch, the URL is retained and the failure is stated.
- Record **evidence**, **inference/synthesis**, and **unknown** separately.
- Record disagreements (school-to-school structure, first-person style, related-work placement, abstract length, simulation vs. measurement, etc.).

### 0.3 Evidence grades used below

| Grade | Meaning |
| --- | --- |
| **E** (evidence) | Fact taken from a successfully fetched primary page, or from official metadata confirmed by multiple official listings |
| **S** (synthesis) | The author's inference or recommended encoding for ThesisForge, tied to evidence but not itself a source claim |
| **U** (unknown / unverified) | Not independently confirmed in this round; a fetch failed; or only a search snippet was available |
| **C** (commentary) | Expert but unofficial advice (blogs, style guides, reviewer essays) |

### 0.4 Important date context

As of 2026-11-11 (Asia/Shanghai):

- *中华人民共和国学位法* has been in force since 2025-01-01 (**E**, official text).
- GB/T 7713.1—2025 has been in force since 2026-02-01, fully replacing GB/T 7713.1—2006 (**E**, official platform metadata and Wuhan University news).
- GB/T 7714—2025 has been in force since 2026-07-01, fully replacing GB/T 7714—2015 (**E**, official platform metadata).
- Many university writing guides still cite the 2006 / 2015 editions. ThesisForge must treat national standards and school templates as two layers, not one.

---

## 1. Chinese graduate thesis standards and typical CS thesis structure

### 1.1 The GB/T 7713 family (official lineage)

**E.** The current official family, as listed on the national standards platform (`openstd.samr.gov.cn` standard list for GBT7713), is:

| Standard | Title | Status (as listed) | Published | Implemented | Notes |
| --- | --- | --- | --- | --- | --- |
| GB/T 7713—1987 | 科学技术报告、学位论文和学术论文的编写格式 | 废止 | 1987-05-05 | 1988-01-01 | Original combined standard |
| GB/T 7713.1—2006 | 学位论文编写规则 | 废止 (废止于 2026-02-01) | 2006-12-05 | 2007-05-01 | Partial successor to 1987 for theses |
| GB/T 7713.1—2025 | 信息与文献 编写规则 第1部分：学位论文 | 现行 | 2025-08-01 | 2026-02-01 | Full replacement of 2006; neq ISO 7144:1986 |
| GB/T 7713.2—2022 | 学术论文编写规则 | 现行 | 2022-12-30 | 2023-07-01 | Journal / academic papers; partial successor to 1987 |
| GB/T 7713.3—2014 | 科技报告编写规则 | 现行 | 2014-05-06 | 2014-11-01 | Technical reports |
| GB/T 7713.4—2025 | 信息与文献 编写规则 第4部分：数据论文 | 现行 | 2025-08-29 (CN listing); an EN listing also shows 2025-12-09 | 2026-03-01 | Data papers |

Official detail pages:

- GB/T 7713.1—2025: https://std.samr.gov.cn/gb/search/gbDetailed?id=3B46A026CC84469CE06397BE0A0AEEB8 — **WebFetch timed out**. Metadata also appears at https://std.samr.gov.cn/gb/search/gbDetailed?id=MrfiyWoM%2B4Q%3D&mode=p (search result; not independently re-fetched).
- GB/T 7713.1—2006 (abolished): https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=EE8640689677E62CF7995716ACAC6A05 and https://std.samr.gov.cn/gb/search/gbDetailedCNF?id=71F772D7C5F6D3A7E05397BE0A0AB82A
- Family list: https://openstd.samr.gov.cn/bzgk/std/std_list?p.p1=0&p.p2=GBT7713&p.p90=circulation_date&p.p91=desc
- GB/T 7713.2—2022 official record (fetched): https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=0B963916637B8F34B295FCF4A51A1BE5 — status 现行; published 2022-12-30; implemented 2023-07-01; English title *Presentation of academic papers*.

**E.** Wuhan University news (fetched, dated 2026-02-01, Asia/Shanghai as published on the university site) confirms that GB/T 7713.1—2025 was led by Wuhan University (draft lead: 陈传夫), released jointly by SAMR and SAC on 2025-08-01, and implemented on 2026-02-01, described as a measure to implement the Degree Law's quality requirements. The news states that the revision adds academic-ethics and academic-integrity clauses and emphasizes originality, while remaining applicable to all types and levels of theses.\
Source: https://news.whu.edu.cn/info/1015/491287.htm

**E / partial U.** A publicly posted university copy of GB/T 7713.1—2025 (Hunan Agricultural University graduate school) was located but **not fully fetched as a PDF in this round**. Search excerpts from that file, consistent with the official change list, include the following — treat wording as *reported from a public university copy, not re-verified line-by-line against the SAMR official reader*:

- URL: https://yjsy.hunau.edu.cn/xwgz/xgxz_1462/202603/P020260325595645822472.pdf (**not fully fetched**)
- The 2025 standard *describes* components, basic writing requirements, and layout. It is a recommended (推荐性) standard.
- Compared with 2006, major technical changes include: revised scope and several definitions; added definition of 学位论文索引; added rules for scientific terms, numbers, and units; added electronic-thesis format/content requirements; added originality statement and use-authorization statement; revised abstract-page requirements and added English-abstract provisions; added a requirement that the main text follow academic norms; revised index and layout rules; replaced the old “structure diagram” appendix with a table of constitutive elements; deleted the old “学位论文数据集” appendix.
- Clause 5.1 of the reported text says a thesis *宜* include six parts: (a) 前置部分, (b) 正文部分, (c) 参考文献, (d) 附录, (e) 索引, (f) 结尾部分, with elements as in Appendix A, Table A.1.
- The preface of the reported text explicitly says disciplines and degree types differ, so application should combine seriousness with flexibility; units should write field-specific rules on top of the basic provisions; practice-based degree outcomes have separate writing rules.

**E (2006 standard, still useful historically and because many school templates still follow it).** A publicly posted copy of GB/T 7713.1—2006 is at http://yjsy.jcu.edu.cn/xueweilunwenbianxieguizeGB_T7713.1-2006.pdf (**not fully re-fetched as a file; substantial public excerpts appeared in search**). Excerpts consistent across multiple university postings:

- Abstract should be independent and self-contained; typically state purpose, methods, results, and conclusions, with emphasis on results and conclusions; no figures, tables, or uncommon symbols if avoidable.
- The 2006 text said Chinese abstracts generally should not exceed 200–300 characters and foreign-language abstracts generally should not exceed 250 words, “except where special need requires slightly more.” **This number is widely overridden by university thesis manuals** (see disagreements below). The 2025 wording on length is **U** in this round (a change is confirmed; the exact new limit was not independently read).
- Introduction / 绪论: purpose, scope, prior work and knowledge gaps, theoretical basis, research ideas, methods and experimental design, expected results and significance; should not repeat the abstract. For a dissertation, a substantial historical/literature review and theoretical analysis *may form a separate chapter* with enough length to show command of the field.
- Main text cannot be uniformly prescribed because topics and methods differ, but must be factual, accurate, complete, logical, clearly layered, and concise.
- Figures and tables should be self-explanatory (自明性).
- Conclusion is the *final, overall* conclusion, not a simple concatenation of chapter summaries; if a conclusion cannot be drawn, a necessary discussion is allowed; suggestions and open problems may appear in the conclusion or discussion.
- References follow GB/T 7714.
- Appendix is optional; may hold derivations, raw data, programs, etc.

**S.** ThesisForge should encode GB/T 7713.1—2025 as the *national default layout and integrity layer*, and the degree-granting unit's current template as the *binding local layer*. Where they conflict, the school template usually governs format; the national standard is the shared baseline and the language of graduate-school audits.

### 1.2 GB/T 7713.2—2022 (academic / journal papers in Chinese)

**E.** Official record fetched: https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=0B963916637B8F34B295FCF4A51A1BE5

**E.** A university journal office summary (fetched) of the standard: https://xbbjb.bttc.edu.cn/info/1021/1643.htm

That summary states:

- The standard defines an academic paper as a written record of the process, methods, and results of research on an academic problem, used for scholarly exchange, discussion, publication, or other uses.
- A paper generally has a front matter, a body, and an appendix part.
- Front matter: title, author information, abstract, keywords, and optional other items.
- Body: introduction, main text, conclusion, acknowledgments, references. Conclusion and appendix are situational.
- Abstract usually includes purpose, methods, results, and conclusions; a informative (报道性) abstract is preferred; 3–8 keywords; an English abstract and keywords are recommended for international exchange.
- Numbering, quantities and units, figures, tables, numerals, mathematical expressions, notes, and scientific terms must follow the cited normative standards.
- Electronic papers should use a common file format and may include audio, video, and datasets.
- Application should combine seriousness with flexibility across natural, social, and humanities fields.

Public PDF copies also exist (not fully fetched in this round), including:

- https://journal.ecjtu.edu.cn/uploadfile/hdjtdx/20240906/GB_T_7713.2-2022_%E5%AD%A6%E6%9C%AF%E8%AE%BA%E6%96%87%E7%BC%96%E5%86%99%E8%A7%84%E5%88%99.pdf
- https://nygcxb.ijournals.cn/uploadfile/nygcxb/20230209/03.%20%E5%AD%A6%E6%9C%AF%E8%AE%BA%E6%96%87%E7%BC%96%E5%86%99%E8%A7%84%E5%88%99-%E5%9B%BD%E6%A0%87.pdf

**S.** For a Chinese journal manuscript, ThesisForge should default to GB/T 7713.2—2022 for structure and to the *target journal's* author instructions for length, heading style, and reference style. IEEE/ACM/Elsevier English venues override this with their own structure manuals (Section 3).

### 1.3 GB/T 7714 citation standard (2015 to 2025)

**E.** Official metadata:

- GB/T 7714—2025: https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14 and https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F
- Title: 信息与文献 参考文献著录规则 / *Information and documentation—Rules for bibliographic references and citations to information resources*
- Status: 现行; published 2025-12-02; implemented 2026-07-01; full replacement of GB/T 7714—2015; neq ISO 690:2021
- List view: https://openstd.samr.gov.cn/bzgk/std/std_list?p.p1=0&p.p2=7714&p.p90=circulation_date&p.p91=desc
- National Digital Standards Library note: https://www.ndls.org.cn/resources/info/2001648569829879809

**E / OCR caveat.** A public OCR PDF of GB/T 7714—2025 is posted at:

https://publishmedia.cbpt.cnki.net/portal/minio/webs/jjkj/media/web/2026/07/27/GBT%207714%E4%B8%802025%E4%BF%A1%E6%81%AF%E4%B8%8E%E6%96%87%E7%8C%AE%20%20%E5%8F%82%E8%80%83%E6%96%87%E7%8C%AE%E8%91%97%E5%BD%95%E8%A7%84%E5%88%99_OCR.pdf

This file was located by search and its table of contents was visible in snippets. It was **not line-checked as a clean official typeset text** in this round (OCR errors are visible in the snippet, e.g. garbled appendix letters). Reliable points from those snippets, to be re-verified in Round 2 against a clean official copy:

- Scope: rules for reference information sources, script, punctuation, general rules, itemized formats by document type, and reference-system compilation. For authors and compilers of references; *not* for librarians or indexers.
- Two systems remain: 顺序编码制 and 著者-出版年制.
- Document types now include, among others, books, book chapters, serials, articles in serials, conference proceedings, theses, reports, standards, patents, websites/pages, archives, maps, **datasets**, and **preprints**.
- “数字对象唯一标识符” is revised to “永久标识符”.
- Preprints receive a type code **PP** (reported in the change list).
- Electronic-resource rules are folded into each document type rather than treated as a single leftover “electronic resource” class.

**E.** The still-familiar 2015 rules remain the ones actually printed in many 2023–2025 school guides (e.g., Wuhan University School of Computer Science, 2023-09). ThesisForge must:

1. Prefer the degree-granting unit's current EndNote/BibTeX style or Word template.
2. If the unit has not yet migrated, say so explicitly, and know both 2015 and 2025 formats.
3. Never invent DOIs, page ranges, or author lists.

### 1.4 Degree Law quality and defense procedures

**E.** Official text fetched from the Chinese government site:

https://www.gov.cn/yaowen/liebiao/202404/content_6947841.htm

Also listed at http://www.npc.gov.cn/c2/c30834/202404/t20240426_436840.html (not re-fetched; same law).

Adopted 2024-04-26; in force 2025-01-01; the Degree Ordinance is repealed.

Provisions most relevant to ThesisForge:

- **Art. 18.** Applicants must observe academic ethics and academic norms.
- **Art. 20 (master's).** After coursework and research or professional training, and after a thesis defense or a prescribed practical-outcome defense, the applicant should: (1) have a firm grasp of the basic theory and systematic specialized knowledge of the field; (2) academic-degree applicants should be able to conduct academic research; professional-degree applicants should be able to undertake professional practice.
- **Art. 21 (doctoral).** In addition to a firm, comprehensive theoretical foundation and systematic, in-depth specialized knowledge: academic-degree applicants should be able to conduct academic research independently *and should produce innovative results in the academic research field*; professional-degree applicants should be able to undertake professional practice independently *and should produce innovative results in the professional-practice field*.
- **Art. 22.** Degree-granting units must publish field-specific degree standards, with a scientific evaluation orientation.
- **Art. 25.** Before organizing a master's or doctoral defense, the unit must send the thesis or practical outcome to experts for review. Only those that meet the unit's rules enter the defense.
- **Art. 26.** Master's defense committee: at least 3 members. Doctoral defense committee: at least 5 members, of whom at least 2 are from outside the degree-granting unit. The work must be sent to committee members in advance; they must perform their duties independently. The committee votes; passage requires at least two-thirds. Defenses are public except when state secrets are involved.
- **Art. 27.** A failed defense may, with the committee's consent, be revised and re-attempted within a set period. A doctoral committee that finds master's-level but not doctoral-level work may, with the applicant's consent and if the applicant does not already hold that master's degree from the unit, recommend a master's degree.
- **Art. 33.** Doctoral students must prepare the thesis or practical outcome carefully and ensure that it meets academic-norm and innovation requirements.
- **Art. 37.** Degree is denied or revoked if the thesis or practical outcome is found to involve ghostwriting, plagiarism, fabrication, or other academic misconduct.

**S.** What defense and review committees actually examine, at the *legal* level, is: (i) academic ethics; (ii) whether the work meets the published *unit and field* standard; (iii) for a PhD academic degree, independent research ability *plus* innovative results; (iv) for professional degrees, independent practical ability *plus* innovative practical results. The Law does not define “创新性成果” operationally; that is left to unit standards and expert judgment.


### 1.5 Typical 计算机 / 计算机应用技术 thesis structure

There is **no single mandated chapter order** at national level. The 2006 and 2025 standards allow a dedicated literature-review chapter and refuse to prescribe a uniform body. School CS guides, however, converge on a recognizable pattern.

**E.** Wuhan University School of Computer Science, *研究生学位论文写作要求与规范（2023-09）*, fetched in full from https://cs.whu.edu.cn/info/1140/35551.htm

This is the strongest CS-specific primary source located in this round. Key requirements:

**Topic and title**

- A topic should have importance (scientific value), innovativeness (status, bottlenecks, challenges), systematicity, and necessity (significance).
- Prefer “小题大做” over “大题小做”; keep the scope small enough to treat thoroughly.
- A thesis is not a simple concatenation of published papers; it should be problem- and need-driven, not a collage of techniques.
- Title: clear, not too long (not more than 25 Chinese characters), a noun phrase, avoid uncommon acronyms. Bad examples: “计算机视觉的若干问题研究” (too big), “大规模图像数据的内容理解与分析” (too vague). Good example: “面向精细视觉解析的深度结构化模型”.

**Layout**

- A PhD thesis should have its own academic idea and tell one complete “story”; all chapters serve that theme.
- Open quickly: do not spend long pages on background every peer already knows; research-status writing should emphasize bottlenecks, open problems, and the author's approach.
- Macro structure: 起 (pose the problem) — 承 (decompose it) — 转 (solve it: theory, method, technique, experiment, results) — 合 (summarize).

**Two thesis types**

1. Theory / technology research (basic, applied-basic, applied, pre-research, experimental, or systems research). Analysis must be correct, experiments scientific, results credible, with innovative results in theory, viewpoint, method, technique, or materials. Typically required of PhD and academic master's students, usually with journal publications.
2. Engineering-design theses. Solve a real production or engineering problem; correct scheme, reasonable structure, accurate data, industry-standard compliance, complete technical documents, and implementation or evaluation by a relevant business unit. Typically for professional master's students; patents or software copyrights may substitute for papers, per school rules.

**Recommended research-thesis skeleton (WHU CS)**

1. 绪论 / 引言: background and significance; research content and methods; contributions; organization
2. 相关工作及背景知识介绍
3. Research work I — problem, analysis, approach, solution, experiment design, results and comparison
4. Research work II (must be related and logically connected)
5. Research work III …
6. 总结与展望: overall results, innovations and contributions; future work

**Recommended engineering-design skeleton:** introduction → related work → design scheme → software/hardware system design and implementation → application and analysis → summary and outlook.

**Language (WHU CS, important disagreement with English systems style — see Section 8)**

- Do not use first-person pronouns in the body, especially “我” or “我们” (the thesis is an individual work). Abstracts use third person, e.g. “论文提出了一种…方法”. “本文” may be used sparingly; passive voice is also suggested.
- Use neutral language; no emotional coloring.
- Use topic sentences: start a paragraph with the result or conclusion, then give details.
- Be cautious with evaluative language such as “首次提出了…”, “最先进的…”, “高效的方法”. Use such phrases only with very sufficient evidence.

**Format pointers in the same guide**

- Still cites GB/T 7713—1987, GB/T 7713.1—2006, and GB/T 7714—2015 (i.e., a 2023 school guide lagging the 2025 national updates).
- Also cites GB/T 6447 (abstracts), GB/T 7156 (secrecy marks), GB/T 15834 (punctuation), GB/T 15835 (numerals).
- Headings only to three levels; figures and tables numbered as 章.序号, self-explanatory, referred to by number not “上图/下图”; three-line tables recommended; references may use numeric or author–year style per GB/T 7714.

**E.** Tongji University School of Computer Science and Technology doctoral defense guide: https://cs.tongji.edu.cn/info/1075/1407.htm

- Writing and binding follow the graduate-school site.
- “关于论文篇幅，博士生学位论文至少有六个完整章节，其中四个章节重点撰写学生本人研究工作。”
- Pre-defense, five expert reviews (with a blind-review offset rule), defense committee of at least five (at least two external), and post-defense revision with a written response, are specified as process, not as writing craft.

**U.** Tsinghua, Peking University, and UCAS manuals were *located* but not fully fetched:

- Tsinghua writing guide PDF: https://www.dhs.tsinghua.edu.cn/wp-content/uploads/2023/12/2025032107444819.pdf — **not fetched**. Search syntheses claiming specific typographic rules such as a 800–1000-character abstract are **not treated as verified** here.
- UCAS 2024-10 update landing page (fetched, but only points to attachments, not the full norm): https://ic.cas.cn/jyc/xwsq/xwwj/202209/t20220905_6508792.html
- UCAS library copy: https://las.cas.cn/yjsjy2021/pyyxw/xwglgd2021/202112/t20211229_6329144.html — **WebFetch returned HTTP 500**.
- PKU intelligent-science page pointing to writing requirements: https://cis.pku.edu.cn/info/1453/2416.htm — **not fetched**.

**S.** A practical default skeleton ThesisForge can offer for 计算机应用技术 academic theses, to be overridden by the school's template:

1. 封面 / 题名页 / 原创性声明 / 授权说明 (2025 national additions; local wording)
2. 中英文摘要与关键词
3. 目录、图表清单、符号说明
4. 第1章 绪论: 问题来源与意义、科学问题、研究内容与方法、贡献/创新点、章节安排
5. 第2章 相关工作与预备知识: 谱系、比较、缺口、本文定位 (not a paper-by-paper dump)
6. 第3–N章 相互关联的研究工作 (PhD often 3–4 work chapters; master's often 1–2). Each chapter: problem → idea → method/design → experiment → results and discussion
7. 最后一章 结论与展望: 总结论、创新点复述（与摘要/绪论一致）、局限、后续工作
8. 参考文献 (GB/T 7714, school style)
9. 附录、致谢、简历与成果清单、索引（如学校要求）

Master's vs PhD, as a synthesis (not a national quota): a master's thesis usually answers one focused question in depth; a PhD thesis usually contains several related studies under one academic idea, and must not read as stapled papers (WHU CS is explicit on this). Tongji's “at least six chapters, four of them the student's own work” is a *local* length rule, not a national one.

### 1.6 What committees actually examine

**E (legal / procedural).** Review before defense; independent expert judgment; for a PhD, innovative results plus demonstrated independent research ability; public defense; two-thirds vote; academic-misconduct sanctions (Degree Law, Arts. 21, 25–26, 37).

**E (school process).** Tongji CS and similar guides emphasize: complete structure, enough chapters of original work, pre-defense, multi-expert review, and documented response to comments.

**C (expert commentary, not official).** 刘凤朝, 科学网, “博士学位论文预答辩几个问题的探讨”: https://blog.sciencenet.cn/blog-42082-1434034.html

Useful because it describes what senior Chinese examiners often *look at*, even though it is not a legal instrument:

- Pre-defense assesses quality of results along 理论构建 — 实证检验 — 结论导出, with originality of hypotheses, reliability of evidence, and depth of dialogue with benchmark literature.
- Structure is examined at coarse grain (overall logic, method–problem fit) and fine grain (title/section alignment, derivations, data use).
- Abstract, 创新点, 研究结论, and 理论贡献 have different jobs and should not be copy-pasted into one another.
- Innovation points must be traceable to argued claims and evidence, not inflated slogans.

**U.** Typical blind-review score sheets (选题、创新性、研究水平、写作规范, etc.) were seen only as search snippets from individual universities (NEU, ECNU, ZJU CS, Xidian, etc.). Exact weights vary by school and by academic vs. professional degree. Round 2 should collect 2–3 current CS/电子信息 评阅书 templates.

**S.** A competent Chinese CS defense / 盲审 reading, at expert-reviewer (not pedantic) level, typically checks:

1. Is there a real, sufficiently focused problem, and is the title honest?
2. Does the literature review locate a gap, or only list papers?
3. Are 2–4 contribution claims explicit, modest, and aligned across abstract, Chapter 1, and the conclusion?
4. Do the middle chapters form one story, not stapled papers?
5. Are methods adequate, experiments comparable, and results credible?
6. Are format, references, figures, and language clean enough not to obstruct judgment?
7. Is there any academic-integrity red flag (plagiarism, fabricated data, missing citations, authorship issues)?

---

## 2. How to state 创新点 well in Chinese CS dissertations

### 2.1 Legal and school-level expectations

**E.** Degree Law Art. 21 requires doctoral academic-degree applicants to produce 创新性成果 in the academic research field (professional degrees: in the professional-practice field). It does not prescribe wording.

**E.** WHU CS: contributions should be stated in Section 1.3; the closing chapter should summarize results, innovations, and contributions; evaluative superlatives need very strong evidence; the thesis must abstract a coherent academic idea from (possibly several) papers.

**C.** 刘凤朝 (same essay as above) gives a compact and widely circulated craft formula for an innovation-point sentence:

- Three elements: **承继** (what prior work it continues), **突破** (what it changes or newly achieves), **价值** (what that is good for).
- Logic: based on which representative prior results, by what means, what breakthrough, what is distinctive, and what theoretical or practical function it has.
- Innovation points are abstracted from posed claims and tight argument, not imagined or arbitrarily elevated.
- Innovation points must be 可溯源、可求证. Theoretical contribution is a dialogue with benchmark literature, based on *conclusions*, not a restatement of the innovation-point slogans.
- Do not arbitrarily elevate claims.

**S.** This matches the later international advice in Sections 3 and 5 (IEEE: do not inflate findings; SIGPLAN: claims must be explicit and scoped; Sewell: misleading over-selling is a legitimate reason to reject). ThesisForge should treat 创新点 as *scoped, evidence-backed contribution claims*, not as marketing.

### 2.2 Types of contribution (synthesis, mapped to sources)

No official Chinese CS standard lists a closed taxonomy of “algorithm / system / theory / measurement / architecture.” The following is **S**, aligned with WHU CS's “理论、观点、方法、技术与材料”, Degree Law's academic vs. professional split, and typical CS/comm/electronics venues:

| Type | What a tight claim looks like | Typical evidence | Typical overclaim |
| --- | --- | --- | --- |
| Theory / model | A new formalization, bound, or explanatory model for a stated class of problems | Proof, derivation, consistency with prior theorems, or clearly scoped assumptions | Calling a restated known theorem “a new theory” |
| Algorithm / method | A method that achieves a stated improvement or capability under stated conditions | Complexity, correctness argument, comparison with strong baselines | “首次提出高效算法” with only an old baseline |
| Architecture / system | A system or architectural design that realizes a capability or trade-off | Implementation, workload evaluation, conservative + progressive criteria (Heiser) | Design document with no system, or only microbenchmarks |
| Measurement / characterization | New empirical facts about systems, channels, devices, or workloads | Sound measurement, enough samples, disclosed platform | A single trace presented as a general law |
| Evaluation methodology / artifact | A benchmark, dataset, or protocol that others can reuse | Documentation, coverage, comparison to existing suites | “A new dataset” that is a trivial split of a public one |
| Application / transfer | A known method applied in a new, non-trivial setting with domain constraints | Domain-valid evaluation, honest comparison | “创新性应用” that is a routine port |
| Professional / engineering (专硕/工程博士) | A scheme that solves a real engineering problem to a stated standard | Implementation, acceptance, or third-party evaluation (WHU CS) | Lab demo claimed as production deployment |

**S.** A good 创新点 is typed, scoped, and paired with a literature gap and an evidence pointer (chapter, figure, theorem, or table). Three tight claims are usually stronger than six inflated ones. Official or quasi-official Chinese commentary often warns against too many innovation points, especially in a master's thesis; the exact “one is enough” rule was not independently verified from a fetched 陈浩元 text in this round (**U**, see Section 7).

### 2.3 Mapping a claim to a literature gap

**S**, combining Swales CARS (Section 7), WHU CS, and 刘凤朝:

1. State the research territory and why the problem matters (not a long textbook primer).
2. Synthesize prior lines of work by *approach*, not by paper title.
3. Name a specific gap, limitation, contradiction, or untested assumption — not “few people have studied X.”
4. Occupy the gap with a claim of the form: *Under conditions C, relative to line of work L, this thesis does D, which yields outcome O, evidenced in Chapter N / Figure F.*
5. Keep abstract, Chapter 1 contributions, chapter-level claims, and the closing chapter lexically consistent (WHU CS lists inconsistency among these as a typical defect).

A claim that cannot be pointed at a gap and a result is not ready to be called an 创新点.

### 2.4 Common overclaim patterns (Chinese dissertations)

**E (WHU CS typical-problems list, Section 10 of the same guide).** Directly relevant items:

- Using most of the abstract for background
- Inconsistent statements of content and innovation across abstract, Chapter 1, and the conclusion
- Evaluative language without sufficient evidence (from the language section)
- Comparing experiments only with the most classical (i.e., oldest) results, not with recent work
- Stapling papers together with no central theme; chapters that do not echo one another
- Presenting a proposition as a “theorem” without a proof, or not distinguishing others' theorems from one's own
- Algorithms with unclear inputs/outputs and no complexity analysis

**C (刘凤朝).** Abstract that narrates effort rather than results; innovation points that merely repeat “theoretical contributions”; elevating claims beyond the hypotheses actually argued.

**S (additional patterns ThesisForge should flag, labeled as synthesis):**

- “首次 / 填补空白 / 国际领先 / 最优” without a documented search boundary
- Claiming generality (“适用于所有…”) from one dataset, one process node, or one channel model
- Counting engineering integration, “using the latest data,” or routine parameter tuning as an innovation
- Attribution blur: advisor's prior platform, a teammate's module, or a reproduced baseline treated as the author's idea
- Semantic inflation: a modest empirical improvement described as a “new paradigm”

**S.** The desired tone is expert-reviewer tight: prefer “在…条件下，相对于…，本文给出…并在…上验证” over both hype and a fog of hedges.


---

## 3. Journal-paper workflow (IEEE / ACM / Elsevier-style CS, communications, electronics)

### 3.1 IEEE article structure and author advice

**E.** IEEE Author Center, “Structure Your Article” (fetched):\
https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/create-the-text-of-your-article/structure-your-article/

- Title: specific, concise, descriptive; **avoid words such as “new” or “novel”** in the title, because readers already assume published work is new.
- Abstract: brief summary of the research, conclusions, and potential implications; one paragraph, up to 250 words; self-contained (no abbreviations, footnotes, references, or equations); highlight what is novel; 3–5 keywords, with abbreviations defined. Write the abstract last and revise it often. Do not put information in the abstract that is absent from the article. IEEE recommends avoiding mathematical symbols in title and abstract because they may not display properly.
- Introduction: review literature to position the work and show novelty; state the question and why it matters.
- Methodology: a straightforward account of what was done and how; enough detail for reproducibility.
- Results: report results; use figures for trends and tables when exact values matter.
- Discussion: what the results mean and how they contribute.
- Conclusion: broader implications and further study; **“Be careful not to inflate your findings.”**
- References: cite only work that directly supports the article; inflating citations is an ethics breach.
- Acknowledgments optional; funding usually goes in the first footnote, not the acknowledgment, in IEEE style.

**E.** IEEE Editorial Style Manual for Authors (PDF located, not fully re-fetched):\
https://journals.ieeeauthorcenter.ieee.org/wp-content/uploads/sites/7/IEEE-Editorial-Style-Manual-for-Authors.pdf

Search excerpt (treat as secondary until fully read in Round 2): recommended order is title page, abstract (one paragraph, 150–250 words), index terms, optional nomenclature, introduction, body, conclusion, appendix(es), acknowledgment, references, photographs and biographies.

**E.** IEEE reviewer-section guidance, as reproduced in an IEEE PELS “IEEE Journals and Magazines Reviewer Guidelines” PDF (located; the PDF itself was not fully fetched in this round):\
https://www.ieee-pels.org/wp-content/uploads/2025/05/ieee-reviewer-guidelines.pdf (**not fully fetched**)

The same section-purpose language is consistent with the Author Center page. Search excerpts, to be confirmed: reviewers should ask whether the article contributes new knowledge; whether the literature review motivates the work; whether the study is well designed and executed; whether there is sufficient benchmarking and validation; whether conclusions are supported; whether experiments are reproducible; and, for surveys, whether there are new insights and archival value. The conclusion must not introduce new concepts or inflate findings.

**U.** https://edu.ieee.org/eg-ejust/submission-process-and-peer-review/ was **blocked (HTTP 403)** in this round. Search snippets from that page listed reviewer concerns of scope, validity, data, clarity, compliance, advancement, and novelty, and said extensions of prior work should not be merely incremental. These bullets are **not treated as verified quotations** here. The same ideas are independently supported by TCOM and ACM policies below.

### 3.2 IEEE Transactions on Communications (communications-journal primary source)

**E.** Fetched: https://www.comsoc.org/publications/journals/ieee-tcom/policies-and-guidelines

Material points:

- TCOM invites original theoretical and/or experimental work of permanent reference value. Papers are considered for **significance, novelty, and usefulness** to the readership.
- Conference vs. journal: TCOM treats them as separate venues; a conference paper cannot be republished without significant differences. The old informal “30% difference” rule is **explicitly not** IEEE or ComSoc policy. IEEE requires “substantial” differences, judged by the editor. Text and figures *may* be copied from the conference paper; the journal title should be at least slightly different; the conference version must be cited at submission and in the paper; for conference papers of 8 pages or more, a differences/similarities summary is required as a supplement.
- Length: initially at most 13 double-column pages (10-pt, 1-inch margins) including everything; revised papers up to 16 pages. Figures and tables should sit with the text. Manuscripts that significantly exceed the guidelines are returned unreviewed.
- Abstract: 75–200 words, clearly outlining scope and contributions; up to five keywords.
- “Introductory discussion should be kept at a minimum and material published elsewhere should be referenced rather than reproduced or paraphrased.” Organization should make the contributions and a logical progression of thought evident. Non-essential proofs and derivations should go to appendices.
- Two-part papers that cannot stand alone are not considered; titles should not say “Part I/II.”
- English only; clarity is essential because an obscure presentation can hide the significance of the work.
- Resubmission of a manuscript already rejected by two journals is ineligible; undisclosed connection to a prior rejection leads to rejection without review.
- AI use by authors and reviewers is governed by IEEE PSPB Operations Manual Section 8.2.1.
- Plagiarism and double-submission policies are strict (immediate rejection and a minimum 6-month ComSoc ban for pre-publication misconduct).

**S.** Communications journal papers in this family are expected to be concise, contribution-front, and either theoretically or experimentally of archival value. Evaluation expectations (baselines, analysis–simulation agreement) are widely practiced in the field; venue-level *methodological* prescriptions were thinner on the TCOM policy page itself than on TED (below). Round 2 should add a fetched classic on simulation credibility (Pawlikowski et al., 2002) and a current TCOM/TWC reviewer form if available.

### 3.3 IEEE Transactions on Electron Devices (semiconductor / device primary source)

**E.** Fetched: https://eds.ieee.org/publications/transactions-on-electron-devices/information-for-authors

Especially important sentence, quoted because it is a venue rule ThesisForge must not soften:

> “Adequate Validation: T-ED welcomes manuscripts reporting solid, rigorous research outcomes centering round devices with adequate validation. Therefore, submissions should generally include at least partial direct physical validation of the results.”

Other fetched points:

- Scope: theory, modeling, design, performance, and reliability of electron and ion devices and interconnects, including emerging materials and a wide application list; tutorials and reviews also published.
- Peer review: at least two independent reviewers; single-anonymous; plagiarism screening.
- Language problems may prevent a manuscript from being sent to review.
- Typical regular-paper length: about seven pages including references at initial submission; more than seven may incur mandatory overlength charges; more than eight generally returned without review unless pre-approved. Reviews: at most twelve pages at initial submission.
- Abstract: 150–250 words, self-contained, one paragraph, no displayed equations or tables; include three or four keywords.
- References must list all authors (no et al.), complete titles, first and last page numbers, month and year, and DOI where available.
- Supplementary material (datasets, simulation files, etc.) must be supplied at submission and cannot be added after review.

**S.** For semiconductor/electronics device papers aimed at T-ED-like venues, simulation-only work is disadvantaged unless the authors can meet “adequate validation,” which the journal itself defines as generally including at least partial direct physical validation. TCAS author pages were located but not fully fetched (https://ieee-cas.org/publication/TCAS-I/TCAS-I-guidelines-authors, https://ieee-cas.org/publication/TCAS-II/tcas-ii-manuscript-submission-guide) — Round 2.

### 3.4 ACM evaluation criteria

**E.** Fetched: https://www.acm.org/publications/policies/pre-publication-evaluation\
Updated 10 February 2022.

For *refereed* material, evaluation is directed at **originality, correctness, novelty, importance, and clarity of exposition**. Process rules include:

- At least three qualified independent reviewers, with written reports provided to the author (rare exceptions).
- At least one round of major revision must be allowed at refereed venues.
- Desk rejects (including “assisted” desk rejects with one outside review) are allowed when a paper is out of scope or far from acceptable.
- Prior publication: journal republication of a disseminated conference paper is allowed only if the editor judges there is significant amplification/clarification *or* significant additional benefit; ACM policy cited in this document mentions a general “at least 25%” extension expectation for republication of archival work. Any prior appearance should be noted on the title page.
- Conferences are typically “formally reviewed” rather than “refereed,” because of time limits and no guaranteed major-revision path, but written multi-reviewer evaluation of technical accuracy is still required.

ACM Computing Surveys author/reviewer pages were located but not fully fetched:

- https://dl.acm.org/journal/csur/author-guidelines
- https://dl.acm.org/journal/csur/reviewers

**S.** Surveys are judged as novel *synthesis*, taxonomy, or perspective, not as new algorithms. ThesisForge should branch “original research article” vs. “survey/tutorial” early.

### 3.5 Elsevier-style workflow

**U / secondary.** No Elsevier CS journal author-instruction page was fully fetched in this round. Secondary Elsevier training materials located:

- https://researcheracademy.elsevier.com/uploads/2018-04/Understanding%20the%20Publishing%20Process_Apr2018_Web.pdf
- https://legacyfileshare.elsevier.com/promis_misc/international%20publishing%20china.pdf
- https://scientific-publishing.webshop.elsevier.com/manuscript-preparation/the-essentials-of-writing-to-communicate-research-in-medicine/

These generally teach IMRaD, a clear gap and objective, reproducible methods, un-overstated discussion, and a complete, polite response to reviews. **Round 2 should fetch a concrete CS/engineering Elsevier guide** (e.g., *Computer Networks*, *Microelectronics Journal*, or *Integration*) rather than relying on medicine-oriented or generic slide decks.

**S.** A reusable journal workflow ThesisForge can later encode, consistent with IEEE/ACM/Belcher and not venue-invented:

1. Clarify the one-sentence research claim and its evidence (Belcher weeks 2–3, 6–8).
2. Choose the venue by scope, contribution type, length, and whether the evaluation (simulation, measurement, system, theory) matches reviewer expectations (TED vs. TCOM vs. ACM Transactions vs. a Chinese 学报).
3. Study 2–3 recent papers in that venue (Belcher week 4).
4. Write to the venue skeleton (IEEE IMRaD-like; ACM Transactions; GB/T 7713.2 plus 学报 template).
5. Make claims, related work, and evaluation mutually consistent.
6. Run an author checklist (length, abstract, reproducibility, baselines, ethics, prior-conference disclosure, ORCID, AI policy).
7. After reviews: respond point-by-point; distinguish agreed fixes from reasoned rebuttals; do not silently ignore a comment.

### 3.6 Topic selection, related work, and reviewer criteria (synthesis)

**S,** tied to sources:

- **Topic / question:** A real problem that matters (Sewell, Heiser, WHU CS, Nature Scitable). “Never studied before” is not, by itself, a reason to study it (Nature Scitable).
- **Related work:** Complete enough and current enough to show novelty (IEEE). In systems papers, a full related-work *section* is often delayed until after the design so the paper can reach the contribution quickly, but every background claim is still cited (Heiser). In Chinese theses, a dedicated Chapter 2 is the norm (WHU CS). In IEEE introductions, the literature review often lives *inside* the introduction. ThesisForge must not force one placement.
- **Reviewer criteria, merged at expert level (not a formal union standard):** novelty / originality; soundness / correctness; adequate evaluation or proof; importance; clarity; scope fit; ethics and policy compliance; for archival journals, lasting usefulness (TCOM's “permanent reference value,” ACM's archival correctness).


---

## 4. Experiment design and evaluation methodology

### 4.1 Computer systems / applied CS

This is the best-documented of the three subfields in this round.

**C / high-value expert sources, widely used in systems PCs:**

1. Gernot Heiser, *Systems Benchmarking Crimes* (fetched): https://gernot-heiser.org/benchmarking-crimes.html
2. Gernot Heiser, *Guide to Technical Writing*, including thesis and systems-paper sections (fetched): https://gernot-heiser.org/style-guide.html
3. ACM SIGPLAN Empirical Evaluation Checklist (2018-10-26) and accompanying guidelines (fetched):\
   https://sigplan.org/Resources/EmpiricalEvaluation/\
   PDF: https://raw.githubusercontent.com/SIGPLAN/empirical-evaluation/master/checklist/checklist.pdf
4. USENIX OSDI '25 Call for Artifacts (fetched): https://www.usenix.org/conference/osdi25/call-for-artifacts
5. Peter Sewell, “Bad Reasons to Reject Good Papers, and Vice Versa,” *Communications of the ACM* blog (fetched): https://cacm.acm.org/blogcacm/bad-reasons-to-reject-good-papers-and-vice-versa/

**Heiser — crimes and best practice (C, but highly operational).** Categories:

- **Selective benchmarking:** not checking for performance degradation outside the advertised case; unjustified subsetting of suites (and quoting a suite-wide score from a subset); selective input ranges that hide the interesting operating region. A fair improvement must meet a *progressive* criterion (significant gain on the target) and a *conservative* criterion (no significant harm elsewhere, or a candid analysis if there is a trade-off).
- **Improper handling of results:** treating microbenchmarks as end-to-end performance; calling a throughput drop of x% an “x% overhead” (often an underestimate); confusing percentage with percentage points; choosing the wrong denominator for relative change; no indication of significance / variance; arithmetic mean of normalized scores (cites Fleming & Wallace, *CACM* 29, on geometric mean).
- **Wrong benchmarks:** oversimplified simulation; uniprocessor SPEC copies used to “prove” multiprocessor scalability; CPU-bound tests used to show networking overhead; calibration and validation on the same data.
- **Improper comparison:** no native / SOTA / unperturbed baseline; only comparing with one's previous paper; evaluating a model on a simulator that embeds the same assumptions; unfair competitor setup; ignoring a newer state of the art and advertising a large gain over an obsolete baseline.
- **Missing information:** platform (hardware and software) underspecified; no per-benchmark numbers; relative numbers only.

Best-practice fragments from the same page: quiescent system; document the rig; verify data actually written/read; do not reuse identical payloads in a way that hits stale caches unnoticed; repeated and re-ordered runs; watch standard deviations (Heiser notes that in *his* OS microbenchmark practice, SDs are often expected to be very small, and >1% should raise an alarm — this is field-specific, not a universal CS law); warm-up iterations; isolate the timed operation; eliminate loop overhead.

**Heiser on systems papers (C).** “Ideas are considered cheap” in systems; a real paper needs a system and an evaluation. The classical reference he points to is the SOSP'83 chairs' “How (and How Not) to Write a Good Systems Paper.” A convincing case requires identifying a *real* problem, offering a solution, and showing that the problem is actually solved. Evaluation should anticipate adversarial readings, include worst-case scenarios, and look honest.

**SIGPLAN checklist — seven categories (E as a community document).** The checklist is explicitly meant to *support informed judgment, not supplant it*. Not every box applies to every paper; a paper with all boxes ticked is not automatically acceptable, and a paper with one box unticked is not automatically rejectable. Categories and example violations:

1. **Clearly stated claims:** claims must be explicit (what is achieved and how); appropriately scoped (no “works for all Java” from a subset; no “works on real hardware” from unrealistic simulation only; no “automatic” if humans intervened); important limitations acknowledged (a generic, evasive “threats to validity” section is *not* the goal).
2. **Suitable comparison:** appropriate baseline, including sometimes a simple/random baseline; fair configuration of competitors.
3. **Principled benchmark choice:** use an established suite when it exists and fits; justify non-standard or subsetted suites; do not substitute kernels for full applications when claims are about applications.
4. **Adequate data analysis:** enough trials for non-deterministic systems; appropriate summary statistics (notes: geometric mean when averaging values with different ranges; harmonic mean for rates; median when there are outliers); report a distribution (variance, SD, quantiles, and/or confidence intervals), not only a mean.
5. **Relevant metrics:** no unjustified proxy metric (e.g., cache misses claimed as end-to-end performance or energy); measure all important effects (e.g., compile time as well as speedup).
6. **Experimental design:** reasonable platform matching the claims; explore key parameters and expected configurations (warm-up vs. steady state); sufficient detail to repeat (all parameters, versions, hardware); open-loop load generation where appropriate; no testing only on the training set.
7. **Appropriate presentation of results:** do not summarize 4%, 6%, 7%, and 49% as “up to 49%”; do not truncate axes in a misleading way; do not plot ratios on a linear scale in a way that distorts reciprocals; use an appropriate number of significant digits.

**OSDI / NSDI artifact badges (E, OSDI '25).** Optional but incentivized evaluation after acceptance. Three badges:

- **Artifacts Available:** permanently and publicly retrievable (Zenodo preferred; institutional or third-party repos acceptable; not a personal webpage).
- **Artifacts Functional:** documentation, completeness, exercisability (scripts and data to run the paper's experiments).
- **Results Reproduced:** independent rerun yields results *within an allowed tolerance* that support the paper's main claims; exact numerical identity is not required.

High-quality artifacts are expected to be consistent with the paper, as complete as possible, well documented, and easy to reuse.

**S for applied CS / 计算机应用技术 systems-style chapters.** Encode: claims → metrics that actually test those claims → SOTA and simple baselines, fairly configured → progressive and conservative criteria → enough runs and a distribution → platform disclosure → no train/test contamination → optional artifact package. Do not require formal artifact badges for a Chinese thesis unless the school or target paper venue does.

### 4.2 Communications

**E.** TCOM (above): significance, novelty, usefulness; original theoretical and/or experimental archival work; concise writing; appendices for non-essential derivations.

**C / U.** A classic, widely cited methodology paper is:

K. Pawlikowski, H.-D. J. Jeong, and J.-S. R. Lee, “On credibility of simulation studies of telecommunication networks,” *IEEE Communications Magazine*, 2002.\
DOI: https://doi.org/10.1109/35.978060\
Open PDF located: https://akaroa.canterbury.ac.nz/pdf/PJL2002.pdf (**not fully fetched in this round**)

Search descriptions (to be verified in Round 2 from the PDF) say the paper argues that many network-simulation studies lack credibility because of inadequate pseudo-random generators and inadequate statistical analysis of output, and recommends documented PRNGs, repeatable experiments, and reporting of output-analysis methods and statistical error / confidence intervals.

**S (labeled synthesis, not a TCOM rulebook).** Communications papers commonly combine analysis and Monte Carlo simulation (e.g., BER / BLER vs. SNR), sometimes plus testbed or over-the-air measurement. A competent review typically looks for: (i) channel and system assumptions stated and matched across analysis, simulation, and baselines; (ii) baselines that are current and fairly tuned; (iii) enough trials for the claimed error rates; (iv) no silent mismatch between analysis and simulation; (v) complexity or overhead discussed when a performance gain is claimed. Hardware validation strengthens credibility but, unlike T-ED's written “generally include at least partial direct physical validation,” TCOM's fetched policy page does not impose a measurement mandate.

**U.** Specific rules of thumb (e.g., how many error events are needed for a given confidence interval on BER) appear in older IEEE literature (e.g., techniques for estimating BER in digital-communication simulation) but were not fetched as clean primary text here. Round 2 should extract operational statistical guidance from Pawlikowski 2002 and one BER-estimation reference, without inventing numbers.

### 4.3 Semiconductor / electronics (simulation vs. measurement)

**E.** T-ED author instructions (fetched, quoted in Section 3.3): submissions should generally include at least partial *direct physical validation*.

**U.** Related documents located but not fetched:

- IEEE EDS “Touchstones of a Quality Compact Model”: https://eds.ieee.org/images/files/Publications/touchstones.pdf
- A 2019 T-ED editorial discussion of simulation-only papers is pointed to in search results (Ghione editorial); not fetched.
- TCAS-I / TCAS-II author guidelines (circuit journals often stress implementation or measured circuit behavior): pages listed in Section 3.3, not fetched.

**S.** For device/circuit/process papers, ThesisForge should default to: model or simulation *plus* a validation path (measurement, or a candid scoped claim if only simulation is possible). A simulation-only manuscript must: declare the tools and all parameters; justify model accuracy and technological feasibility; avoid claiming hardware performance from unvalidated simulation; and not hide the limitation. That is a synthesis consistent with T-ED, not a universal IEEE rule.

### 4.4 Statistical reporting and reproducibility (cross-cutting)

**E / C.** Convergent advice from SIGPLAN, Heiser, IEEE methodology section, and OSDI AE:

- Report variability, not only means.
- Do not treat differences within noise as improvements.
- Use summary statistics that match the data (geometric mean, harmonic mean, median — per SIGPLAN notes).
- Give enough methodological detail (and, where the venue values it, artifacts) for a reasonably skilled reader to repeat the work.
- Reproduced is not the same as bit-identical; claims must still stand.
- Never use the development / training set as the sole test set.
- Never fabricate or silently retouch data. Degree Law Art. 37 and IEEE/ACM plagiarism and research-integrity rules all treat fabrication as disqualifying.

**S.** ThesisForge must refuse to invent numbers, fill missing experimental cells, or “polish” a figure by inventing smoother curves. If data are incomplete, the skill should help design the remaining real experiment or narrow the claim.

---

## 5. Academic argument quality at expert-reviewer level

### 5.1 Claim–evidence–warrant

**U.** A Toulmin explainer at https://open.library.okstate.edu/writingforpublication/part/section-1-for-research-argument-argument-structure-the-toulmin-model/ **failed to fetch (HTTP 504)**. The model itself is standard and can be used as a teaching frame, but this report does not quote that page.

**S,** consistent with Sewell, SIGPLAN “clearly stated claims,” 刘凤朝, IEEE “conclusions supported by the data,” and Nature Scitable's “theorem-proof” paragraph habit:

- **Claim:** what is being asserted (a contribution, a result, a limitation).
- **Evidence (grounds):** the theorem, measurement, ablation, comparison, or citation that is actually in the manuscript.
- **Warrant:** why that evidence is enough for *this* claim (metric matches the claim; baseline is the right one; assumptions hold; sample is adequate).
- **Qualifier / scope:** under which conditions the claim is meant to hold.
- **Rebuttal / limitation:** the important conditions where it may fail — the real ones, not a ritual paragraph.

A competent reviewer asks Sewell's four questions: Is the motivation real? Would the claims, if true, be substantial progress? Are the claims backed up? Is the writing clear enough for a reader with the right background? A clear “no” on any of these is enough to reject at a serious venue (Sewell). That is the right rigor target for ThesisForge — not an infinite hunt for extra experiments that are only “nice to have” (Sewell explicitly lists “I want extra evaluation, even though it does a decent job to support the claims” as a *bad* reason to reject).

### 5.2 How much hedging is enough

**E.** IEEE Author Center: do not inflate findings; do not use “new/novel” in titles.

**E.** WHU CS: no casual “首次 / 最先进 / 高效”; if used, evidence must be very sufficient; remain objective.

**E.** Nature Scitable (fetched): https://www.nature.com/scitable/topicpage/scientific-papers-13815490/\
Papers must inform, not impress; they must convince referees and readers that the work is important, valid, and relevant; include *just enough* evidence to establish the outcome. Conclusions interpret at a higher level and tie back to the need in the introduction, without focusing on the authors' labor.

**C.** Heiser: avoid buzzwords (“new,” “novel,” “innovative”) and bait-and-switch overselling in the introduction; be forthright about limitations; do not misrepresent prior work in order to look better.

**C.** Sewell: “The claims are misleading: the work is over-sold and the authors aren't clear about the limitations, or about the relationship to previous work” is a good reason to reject. Conversely, demanding a different paper, or rejecting a simple but useful idea because it is “too simple,” is a bad reason.

**S (hedging policy for ThesisForge, calibrated to the user's brief).** Encode a three-band rule:

1. **State plainly** when the warrant is strong: a measured 12% reduction on a named, fairly configured baseline, with variance reported, may be written as a 12% reduction — not “might potentially tend to somewhat reduce.”
2. **Scope, don't fog,** when the warrant is partial: “On Dataset D and Model M, …; whether this holds for … is not established.” That is a scope restriction, not a stack of modals.
3. **Do not claim** when evidence is missing. Do not write around a missing experiment with “it is believed that,” and do not invent the experiment.

Avoid both:

- Overclaim: 首次、通用、最优、paradigm shift, “works on real hardware” from simulation only;
- Over-defense: “to the best of our limited knowledge, one might perhaps tentatively suggest…”; ritual threats-to-validity that name trivial risks and hide the real ones (SIGPLAN FAQ).

The USC CARS guide (fetched, https://libguides.usc.edu/writingguide/CARS) also shows how to establish a niche *without* a hostile tone: “Although research has been devoted to A, less attention has been paid to B…” rather than “Doe fails to….” This matches Heiser's advice on related work. ThesisForge should prefer contrastive, non-derogatory gap statements.

### 5.3 Paragraph-level argument

**E.** Nature Scitable: lead with the message (topic sentence), then evidence; Materials and Methods can still explain *choices*, not only list steps; Results and Discussion are often clearer when interpretation sits next to results; the conclusion should not merely repeat the introduction. The same page recommends a four-part introduction: context, need, task, and object of the document. “Never studied before” is not, by itself, a reason to study a phenomenon.

**E.** WHU CS: topic sentence first; then details.

**C.** Heiser: maintain “user state”; define-before-use; short strategic redundancy (“say what you will say, say it, say what you said”) in main sections; one clear message for the whole paper; be concise as well as clear.

**C.** Belcher, *Writing Your Journal Article in Twelve Weeks* (author's site fetched): https://wendybelcher.com/writing-advice/how-to-write-a-journal-article/\
The weekly arc is itself a checklist: plan; create and test the argument; write the abstract early as a test of the argument; choose a journal; refine citations; craft claims for significance; analyze and present evidence; macrostructure; title/introduction/conclusion; sentence-level clarity; submission; then revision after review. ThesisForge should steal the *order* (argument and claim before ornamental prose), not pirate the book.


---

## 6. Common failure modes in CS master's/PhD theses and journal submissions

### 6.1 Chinese CS theses (primary: WHU CS Section 10)

**E.** The WHU CS 2023 guide's “历年学位论文中一些典型问题” is the most concrete CS-thesis failure list fetched in this round. Grouped:

**Title, abstract, and front matter**

- English titles beginning with “Research on / Study On” (called 中式英语 in the guide)
- Abstract mostly background; references inside the abstract
- Translating “本文” as “This paper” rather than “This thesis”
- Inconsistent content/innovation statements among abstract, Chapter 1, and the conclusion

**Structure and logic**

- A “related work” subsection in every later chapter, repeating Chapter 2
- In Section 1.1 already citing dozens or nearly half of all references, then repeating them in Chapter 2 (Section 1.1 should cite only a few)
- Stapled papers; no central theme; chapters that do not refer to one another or to the title

**Technical soundness**

- Algorithms with unclear I/O, weak theory, no complexity analysis
- “Theorems” without proofs; or long proofs of other people's theorems; or no statement of where a new theorem was published or how it was recognized
- Experiments compared only with classic/old methods, not recent ones
- Defined formulas that are never used
- Non-standard formula typography; inconsistent italic/roman for the same symbol

**Format and language**

- Nested or repeated numbering schemes; mixed Chinese and Arabic numbering
- Language errors, 的/地 confusion, typographical errors
- Punctuation at the end of headings; citations inside headings
- Chapters not starting on a new page
- Old references, or not a single Chinese reference
- Figure/table and reference-format errors (detailed in earlier sections of the same guide)

### 6.2 Journal and conference submissions

**C (Sewell, good reasons to reject).** Motivation missing or bogus; technically correct but pointless; only a minor increment for the venue; genuinely done before; over-sold claims or unclear limitations / related work; proofs or data missing without good reason; evaluation too limited or flawed to support the claims; substantially less rigor than normal in the area; technically wrong and not easily fixable; exposition so bad that an informed reader cannot tell what was done.

**C (Sewell, bad reasons — ThesisForge should *not* emulate these as a reviewer).** “I could have done this”; wanting a different paper; demanding more pages of examples or extra evaluation when the claims are already supported; “I just wasn't excited”; reviewing the paper as if it were a different kind of paper; punishing simplicity or honest incrementality; inflating a missing citation of the reviewer's own paper into a fatal flaw.

**C (Heiser).** Benchmarking crimes and chart abuse; bait-and-switch introductions; related work that is vague or unfair; sloppy writing that makes reviewers suspect sloppy technical work.

**E (IEEE / TCOM / TED / ACM).** Out of scope; incremental republication without substantial addition; inadequate validation (especially TED); irreproducible methods; inflated citations; plagiarism or undisclosed prior rejection; poor English that blocks review; conclusions not supported; literature review incomplete or stale.

**S (cross-cutting failure modes to encode).**

| Failure | Typical symptom | Why a competent reviewer cares |
| --- | --- | --- |
| Logic gap | Method does not address the stated question; conclusion wider than results | Claim–evidence broken |
| Unfocused related work | Paper-by-paper annotated bibliography; missing SOTA; hostile or inaccurate summaries | Novelty cannot be judged; may anger expert reviewers |
| Weak baselines | Old, untuned, or self-only comparison | Apparent gain is uninterpretable |
| Abstract / contribution mismatch | Abstract promises a system-wide result; body has a simulator study on one workload | Bait-and-switch |
| Format noise | Inconsistent numbering, broken GB/T 7714, unreadable figures | Obstructs, and signals carelessness |
| Irreproducibility | Missing hyperparameters, versions, seeds, device process, or channel parameters | Results cannot be trusted or built on |
| Integrity failure | Fabricated data, recycled figures, citation invention, plagiarism | Disqualifying (Degree Law; IEEE/ACM policy) |

---

## 7. Writing guides worth absorbing

The following are recommended *inputs* to ThesisForge, not texts to copy.

### 7.1 English-language guides

| Guide | Why it matters | Status this round | URL |
| --- | --- | --- | --- |
| John Swales, CARS (Create a Research Space), via *Genre Analysis* (1990) and Swales & Feak, *Academic Writing for Graduate Students* | Standard move structure for introductions: territory → niche → occupy niche | **E** on a reliable university guide that attributes the model; books themselves not copied | https://libguides.usc.edu/writingguide/CARS ; also https://uwaterloo.ca/writing-and-communication-centre/creating-research-space-cars-model |
| Wendy Belcher, *Writing Your Journal Article in Twelve Weeks* | Process: argument first, abstract as a test, venue study, claims for significance, evidence, macro- then micro-structure, revision after review | **E** on the author's outline page; book not fetched (copyright — do not paste) | https://wendybelcher.com/writing-advice/how-to-write-a-journal-article/ ; https://wendybelcher.com/writing-advice/writing-your-journal-article-in-twelve/ |
| Justin Zobel, *Writing for Computer Science* (Springer, 2014 ed. widely used) | CS-specific writing, experiment reporting, and common mistakes | **U / secondary only.** PDFs circulate; this round did **not** treat unofficial ebook mirrors as a source to quote. Round 2 should use a legitimate copy or a university lecture that fairly summarizes it. | Publisher record should be preferred over file-sharing URLs found in search |
| Gernot Heiser, style guide + benchmarking crimes | Systems evaluation and writing craft; also useful for applied-CS theses | **E** (fetched) | https://gernot-heiser.org/style-guide.html ; https://gernot-heiser.org/benchmarking-crimes.html |
| SIGPLAN Empirical Evaluation Checklist | One-page evaluation best practices; judgment aid, not a score sheet | **E** (fetched) | https://sigplan.org/Resources/EmpiricalEvaluation/ |
| Peter Sewell, reviewing essay | Calibrates “expert reviewer” vs. pedantic reviewer | **E** (fetched) | https://cacm.acm.org/blogcacm/bad-reasons-to-reject-good-papers-and-vice-versa/ |
| IEEE Author Center + Editorial Style Manual | Default English journal skeleton for IEEE fields | **E** / style manual PDF not fully read | https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/create-the-text-of-your-article/structure-your-article/ |
| Nature Scitable, “Scientific Papers” (Doumont-style advice republished by Nature Education) | Context–need–task–object introductions; inform not impress; topic sentences; short, high-level conclusions | **E** (fetched; page marked archived) | https://www.nature.com/scitable/topicpage/scientific-papers-13815490/ |
| Nature journal formatting / style checklist | Useful only for *Nature* family venues; not a default for IEEE/ACM CS | Located, not relied on as general CS advice | https://www.nature.com/nature/for-authors/formatting-guide ; http://mtscommon.nature.com/letters/author_style_checklist.pdf |
| Simon Peyton Jones, “How to write a great research paper” (slides; recommended by Heiser) | Popular CS talk on paper stories and contributions | Located via Heiser; slides not fetched | To be added in Round 2 from an official Microsoft/University source |

### 7.2 Chinese-language standards and guides

| Guide | Why it matters | Status this round | URL |
| --- | --- | --- | --- |
| GB/T 7713.1—2025 / 2006 | National thesis structure and integrity | Metadata **E**; 2025 full text **partial U** | Official: https://std.samr.gov.cn/gb/search/gbDetailed?id=3B46A026CC84469CE06397BE0A0AEEB8 ; university copy: https://yjsy.hunau.edu.cn/xwgz/xgxz_1462/202603/P020260325595645822472.pdf |
| GB/T 7713.2—2022 | National academic-paper structure | Official record **E**; journal-office summary **E** | https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=0B963916637B8F34B295FCF4A51A1BE5 ; https://xbbjb.bttc.edu.cn/info/1021/1643.htm |
| GB/T 7714—2025 / 2015 | Reference format | Metadata **E**; 2025 OCR PDF **not clean-verified** | https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14 |
| 学位法 | Quality, innovation requirement, review and defense procedure, misconduct | **E** | https://www.gov.cn/yaowen/liebiao/202404/content_6947841.htm |
| 武汉大学计算机学院研究生学位论文写作要求与规范（2023-09） | Best CS-specific thesis manual fetched | **E** | https://cs.whu.edu.cn/info/1140/35551.htm |
| 同济大学计算机科学与技术学院博士答辩指南 | Local length and process rules | **E** | https://cs.tongji.edu.cn/info/1075/1407.htm |
| 刘凤朝, 预答辩与创新点撰写 | Examiner-side craft of 创新点 | **C** | https://blog.sciencenet.cn/blog-42082-1434034.html |
| 陈浩元 and 《科技论文写作》 / 编辑学会 materials | Very widely used in Chinese STM editing | **U** this round (cjstp article did not load useful text: https://www.cjstp.cn/CN/10.11946/cjstp.201805220456 ; Tsinghua *科技与出版* article located: http://kjycb.tsinghuajournals.com/article/2017/1005-0590/113209G-2017-10-115.shtml — not fetched) | Round 2 |
| UCAS / Tsinghua / PKU official manuals | Elite-university defaults for length and typography | Located, **not fully fetched** | See Section 1.5 |
| 计算机学报 / 电子学报 / 通信学报 author guides | Chinese CS/comm/electronics journal conventions | **U**, not searched in depth this round | Round 2 |

GB/T 6447 (文摘编写规则) is cited by WHU CS and remains relevant to abstract writing; it was not independently fetched (**U**).

---

## 8. Disagreements and counter-evidence (do not hide these)

1. **National standard vs. school template.** GB/T 7713.1 is 推荐性. WHU CS (2023) still cites 1987/2006/2015. Abstract length in the 2006 standard (200–300 Chinese characters) is much shorter than what many doctoral manuals actually require. **ThesisForge must always load the school's current template and treat it as binding for format.**

2. **2025 vs. 2006/2015 migration.** As of this research date, 7713.1—2025 and 7714—2025 are already in force, but campus practice will lag. Innovation: 2025 adds originality and authorization statements, electronic-thesis rules, and academic-integrity language, and drops the old dataset appendix of 2006.

3. **Chapter order differs.** WHU CS: related work as Chapter 2, then several work chapters. Heiser: related work often *after* the contribution in a conference paper. IEEE: literature often inside the introduction. Some theses put methods first (experimental sciences). Engineering-design theses use a scheme / implementation / application structure, not “three algorithms.”

4. **Master's academic vs. professional vs. PhD.** Degree Law and WHU CS distinguish them. Tongji's six-chapter / four-work-chapter rule is local. Professional theses may emphasize implementation and acceptance criteria more than theoretical novelty.

5. **First person.** WHU CS forbids “我 / 我们” in the thesis body and prefers third person in the abstract. Heiser strongly attacks overuse of the passive and prescribes inclusive “we” in English theses and papers. Nature Scitable uses “we” in the past tense for the research task and “this paper” in the present tense for the document. **ThesisForge must switch style by language and by venue/school, not pick one universal pronoun rule.**

6. **“Incremental” work.** ACM/IEEE reviewers reject *merely* incremental extensions, but Sewell and Heiser warn against punishing honest, substantial increments or simple useful ideas. Expert-level review is not “reject unless paradigm-shifting.”

7. **Simulation vs. measurement.** T-ED generally wants partial physical validation. TCOM accepts theoretical and/or experimental work without a fetched measurement mandate. Systems venues usually want a real system, not only a simulation, but Heiser acknowledges that simulation is sometimes unavoidable if the model is defended. SIGPLAN warns against claiming “real hardware” from unrealistic simulation.

8. **Related-work tone.** CARS can be written in a contrastive but non-hostile way; Heiser warns that the author you slight may be the reviewer.

9. **Statistics culture differs by subfield.** Heiser's very small SD expectations are typical of tight OS microbenchmarks, not of ML training runs or Monte Carlo BER at very low error rates. SIGPLAN's “enough trials / report a distribution” is the safer cross-field rule; specific tests (t-test, geometric mean, error-event counts) depend on the claim.

10. **Artifact evaluation is usually post-acceptance and optional** (OSDI '25). Do not treat badges as a submission prerequisite unless a venue says so.

11. **Checklists can be misused.** SIGPLAN and Sewell both insist on judgment. ThesisForge should use checklists to *avoid missing* a real issue, not to generate a long list of pedantic demands.


---

## 9. (A) Structured inventory of methods and checklists ThesisForge MUST encode

The following is **S**, but every item is grounded in sources above.

### A1. Dual-product, dual-layer architecture

- Products: (1) dissertation (academic master's, professional master's, academic PhD, professional doctorate); (2) journal or conference paper (IEEE, ACM, Elsevier, Chinese 学报).
- Layers: national standard (GB/T 7713.x, 7714, Degree Law) → school or publisher template → discipline evaluation norms (systems / communications / devices).
- Always ask for, or stop and request, the binding template and target venue *before* formatting advice.

### A2. Integrity rails (non-negotiable)

- No fabricated data, figures, or citations; no silent reuse of others' text or results.
- Design experiments that can actually be run; analyze only real measurements, honest simulations, or user-supplied data.
- If evidence is missing, narrow the claim or plan the next real experiment.
- Disclose prior conference versions (TCOM / ACM / IEEE rules).
- Flag plagiarism, ghostwriting, and data-fabrication risks in review mode (Degree Law Art. 37).

### A3. Dissertation workflow (write + review)

1. Topic focusing (“小题大做,” problem-driven, one story).
2. Contribution design: 2–4 typed, scoped 创新点, each mapped to a gap and to evidence.
3. Skeleton by thesis type (research vs. engineering) and by school.
4. CARS-style 绪论 and a *comparative* 文献综述, not a list.
5. Per-chapter research write-up: problem, idea, method, experiment, discussion.
6. Consistency pass: title, abstract, Chapter 1 contributions, chapter claims, conclusion.
7. Format pass: school template + GB/T 7713.1—2025 + GB/T 7714 (version as required).
8. Defense/预答辩 reading: one-story arc, limitations stated without theatrical humility, likely committee questions.

### A4. 创新点 checklist

For each claim: type; 承继; 突破; 价值; scope conditions; evidence pointer; not a superlative unless warranted; wording aligned across abstract / Chapter 1 / conclusion; distinguishable from adjacent claims; author's own work clearly separated from advisor/team/prior publications.

### A5. Journal workflow

Belcher-like argument-first process; venue matching; IEEE/ACM/GB/T 7713.2 skeleton; author checklist (length, abstract, keywords, reproducibility, ethics, AI policy, ORCID, prior publication); review-response protocol.

### A6. Evaluation methodology pack (by subfield)

- **Applied CS / systems:** SIGPLAN seven categories + Heiser progressive/conservative criteria, baseline fairness, no cherry-picking, variance, platform disclosure, optional artifacts.
- **Communications:** matched assumptions; analysis vs. simulation agreement; current, fairly tuned baselines; documented simulation statistics (details to be filled from Pawlikowski et al. in Round 2); measurement when claimed.
- **Semiconductor / electronics:** T-ED-like validation expectation; tool and parameter disclosure; do not report simulated device data as measured; compact-model quality to be added from EDS Touchstones in Round 2.

### A7. Argument and tone pack

- Claim–evidence–warrant–scope–limitation.
- Topic-sentence paragraphs; message before chronology (Nature Scitable, WHU CS).
- Hedging bands (Section 5.2): plain statement / scoped statement / do not claim.
- No bait-and-switch introductions (Heiser, IEEE).
- Contrastive, non-hostile related work (CARS + Heiser).
- Reviewer mode calibrated to Sewell's good reasons, and *forbidden* from his bad reasons (no pedantic extra-experiment demands when claims are already supported).

### A8. Failure-mode review pack

Encode the WHU CS typical-problem list, Sewell's legitimate rejection reasons, Heiser's crimes, and the cross-cutting table in Section 6.2 as a review rubric with severity: blocking (integrity, unsupported main claim, fatal experimental flaw), major (weak baseline, mismatch, unfocused review), minor (format, language). Expert-level, not nitpicking.

### A9. Style switches

- Language: Chinese dissertation (often no “我们”; 本文 / 论文) vs. English paper (inclusive we / this paper, by venue).
- Related-work placement: Chapter 2 vs. end vs. inside introduction.
- Abstract length and heading depth: school/venue, not a single national number.
- Citation system: numeric vs. author–year vs. IEEE vs. ACM; 2015 vs. 2025 GB/T 7714.

### A10. Things ThesisForge should not encode as hard rules

- “Innovation must be paradigm-shifting.”
- “Always reject simulation-only work” (false for many communications and theory papers).
- “Always write related work as Chapter 2” or “always put it last.”
- “Always use first person” or “never use first person.”
- “A threats-to-validity section is mandatory and sufficient.”
- “Artifact badges are required for every thesis.”
- Any invented experimental result or bibliographic record.

---

## 10. (B) Gaps still unsolved, to feed Round 2

1. **Clean official text of GB/T 7713.1—2025** (SAMR page timed out; university PDF not fully read). Need exact rules on abstract length, electronic theses, originality statements, and Appendix A element table.
2. **Clean official text of GB/T 7714—2025** (OCR PDF is messy). Need worked examples for preprints, datasets, software, and persistent identifiers, plus a 2015 vs. 2025 delta sheet for CS theses.
3. **Elite-university manuals actually fetched:** Tsinghua, PKU, UCAS, and at least one 电子/通信 school (e.g., BUPT, Xidian, SEU) current Word/LaTeX norms, including abstract length and 创新点 placement.
4. **Current CS 盲审 / 评阅书 templates** and any Ministry or professional-degree quality standard (an MOE professional-doctorate quality standard was mentioned in search: http://www.moe.gov.cn/jyb_xwfb/s7600/202410/t20241030_1159900.html — not fetched).
5. **Zobel, *Writing for Computer Science*, from a legitimate source**, summarized fairly (common CS writing faults, experiment write-up).
6. **Chinese STM writing canon:** 陈浩元, GB/T 6447, 《科技论文写作》 or 中国科学技术期刊编辑学会 materials, and the cjstp paper on presenting 创新点 (page did not load).
7. **Chinese journal author guides:** 计算机学报, 软件学报, 电子学报, 通信学报, 半导体学报 — structure, length, 创新点/要点, and reference style.
8. **Communications statistics primary text:** Pawlikowski et al. 2002 PDF, plus one BER/Monte Carlo error-estimation source, to put real numbers and procedures into the comms evaluation pack.
9. **Semiconductor primary supplements:** EDS compact-model touchstones; T-ED editorial policy on simulation-only papers; TCAS-I/II measurement vs. simulation expectations; maybe IEEE TMTT author information (already located: https://mtt.org/publications/t-mtt/information-for-authors/).
10. **Elsevier CS/engineering journal guide** fetched as a primary page, plus one ACM Transactions (e.g., TOCS or TON) author guideline beyond the Publications Board policy.
11. **IEEE Editorial Style Manual and IEEE reviewer-guidelines PDF** fully read; the ejust page that 403'd can be replaced by these.
12. **Peyton Jones slides**, and “How (and How Not) to Write a Good Systems Paper” (SOSP'83), if still the canonical pointer.
13. **ML / AI evaluation subset**, because much 计算机应用技术 work is now model-centric: data leakage, unfair hyperparameter tuning, test-set reuse, reporting means over seeds. Only lightly touched via SIGPLAN's training-set warning in this round.
14. **Topic-discovery method** for journal papers (systematic gap analysis, not just “find a hot keyword”): still thin.
15. **Experiment-design templates** that are actually runnable (ablation plans, communication link-budget/sim plans, device I–V measurement plans) — this round collected *criteria*, not procedures.
16. **Hedging / stance:** Hyland-type research was only search-cited; a short, practical English/Chinese phrase band (enough vs. too much) should be built from fetched style guides, not from invented psychology.

Round 2 should stay evidence-based, close the official-text gaps first, then deepen the three evaluation subfields and Chinese journal conventions.

---

## 11. (C) Source list, with URLs and fetch status

Legend: **Fetched** = WebFetch returned usable text in this round. **Located** = URL confirmed by search or by a fetched page's citation, but the page/PDF was not fully read. **Failed** = fetch attempted and did not succeed.

### Official standards and law

1. GB/T 7713.1—2025 official detail — https://std.samr.gov.cn/gb/search/gbDetailed?id=3B46A026CC84469CE06397BE0A0AEEB8 — **Failed (timeout)**
2. GB/T 7713.1—2025 alternate official listing — https://std.samr.gov.cn/gb/search/gbDetailed?id=MrfiyWoM%2B4Q%3D&mode=p — **Located**
3. GB/T 7713 family list — https://openstd.samr.gov.cn/bzgk/std/std_list?p.p1=0&p.p2=GBT7713&p.p90=circulation_date&p.p91=desc — **Located (search); metadata used**
4. GB/T 7713.1—2006 official record — https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=EE8640689677E62CF7995716ACAC6A05 — **Located**
5. GB/T 7713.1—2006 official CNF record — https://std.samr.gov.cn/gb/search/gbDetailedCNF?id=71F772D7C5F6D3A7E05397BE0A0AB82A — **Located**
6. GB/T 7713.1—2006 public university copy — http://yjsy.jcu.edu.cn/xueweilunwenbianxieguizeGB_T7713.1-2006.pdf — **Located (excerpts used; file not fully re-fetched)**
7. GB/T 7713.1—2025 public university copy — https://yjsy.hunau.edu.cn/xwgz/xgxz_1462/202603/P020260325595645822472.pdf — **Located (search excerpts used; PDF not fully fetched)**
8. GB/T 7713.2—2022 official record — https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=0B963916637B8F34B295FCF4A51A1BE5 — **Fetched**
9. GB/T 7713.2—2022 journal-office summary — https://xbbjb.bttc.edu.cn/info/1021/1643.htm — **Fetched**
10. GB/T 7713.2—2022 public PDFs — https://journal.ecjtu.edu.cn/uploadfile/hdjtdx/20240906/GB_T_7713.2-2022_%E5%AD%A6%E6%9C%AF%E8%AE%BA%E6%96%87%E7%BC%96%E5%86%99%E8%A7%84%E5%88%99.pdf ; https://nygcxb.ijournals.cn/uploadfile/nygcxb/20230209/03.%20%E5%AD%A6%E6%9C%AF%E8%AE%BA%E6%96%87%E7%BC%96%E5%86%99%E8%A7%84%E5%88%99-%E5%9B%BD%E6%A0%87.pdf — **Located**
11. GB/T 7714—2025 official record — https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14 — **Located (search)**
12. GB/T 7714—2025 official detail — https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F — **Located (search)**
13. GB/T 7714—2025 OCR PDF — https://publishmedia.cbpt.cnki.net/portal/minio/webs/jjkj/media/web/2026/07/27/GBT%207714%E4%B8%802025%E4%BF%A1%E6%81%AF%E4%B8%8E%E6%96%87%E7%8C%AE%20%20%E5%8F%82%E8%80%83%E6%96%87%E7%8C%AE%E8%91%97%E5%BD%95%E8%A7%84%E5%88%99_OCR.pdf — **Located (OCR excerpts; not clean-verified)**
14. GB/T 7714 list — https://openstd.samr.gov.cn/bzgk/std/std_list?p.p1=0&p.p2=7714&p.p90=circulation_date&p.p91=desc — **Located**
15. NDLS note on GB/T 7714—2025 — https://www.ndls.org.cn/resources/info/2001648569829879809 — **Located**
16. *中华人民共和国学位法* — https://www.gov.cn/yaowen/liebiao/202404/content_6947841.htm — **Fetched**
17. Same law, NPC — http://www.npc.gov.cn/c2/c30834/202404/t20240426_436840.html — **Located**

### University and policy commentary

18. Wuhan University news on GB/T 7713.1—2025 implementation — https://news.whu.edu.cn/info/1015/491287.htm — **Fetched**
19. WHU School of Computer Science thesis writing norms (2023-09) — https://cs.whu.edu.cn/info/1140/35551.htm — **Fetched**
20. Tongji CS doctoral defense / degree guide — https://cs.tongji.edu.cn/info/1075/1407.htm — **Fetched**
21. 刘凤朝, 科学网 — https://blog.sciencenet.cn/blog-42082-1434034.html — **Located / substantial search text; treat as commentary**
22. UCAS thesis-norm landing page (2024-10 update) — https://ic.cas.cn/jyc/xwsq/xwwj/202209/t20220905_6508792.html — **Fetched (attachments only, not the full norm)**
23. UCAS library copy of the norm — https://las.cas.cn/yjsjy2021/pyyxw/xwglgd2021/202112/t20211229_6329144.html — **Failed (HTTP 500)**
24. Tsinghua writing guide PDF — https://www.dhs.tsinghua.edu.cn/wp-content/uploads/2023/12/2025032107444819.pdf — **Located, not fetched**
25. PKU intelligent-college writing-format page — https://cis.pku.edu.cn/info/1453/2416.htm — **Located, not fetched**
26. ICT/CAS lecture note page — https://ict.cas.cn/xwgg/jssxw/202304/t20230410_6728779.html — **Located, not fetched**
27. MOE note on professional-doctorate quality standard (search hit) — http://www.moe.gov.cn/jyb_xwfb/s7600/202410/t20241030_1159900.html — **Located, not fetched**

### IEEE / ACM / publishers

28. IEEE Author Center, Structure Your Article — https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/create-the-text-of-your-article/structure-your-article/ — **Fetched**
29. IEEE Editorial Style Manual for Authors — https://journals.ieeeauthorcenter.ieee.org/wp-content/uploads/sites/7/IEEE-Editorial-Style-Manual-for-Authors.pdf — **Located**
30. IEEE PELS reviewer guidelines PDF — https://www.ieee-pels.org/wp-content/uploads/2025/05/ieee-reviewer-guidelines.pdf — **Located, not fully fetched**
31. IEEE E-JUST “Submission Process and Peer Review” — https://edu.ieee.org/eg-ejust/submission-process-and-peer-review/ — **Failed (HTTP 403)**
32. IEEE TCOM policies and guidelines — https://www.comsoc.org/publications/journals/ieee-tcom/policies-and-guidelines — **Fetched**
33. IEEE Communications Magazine policies — https://www.comsoc.org/publications/magazines/ieee-communications-magazine/policies-guidelines — **Located**
34. IEEE T-ED Information for Authors — https://eds.ieee.org/publications/transactions-on-electron-devices/information-for-authors — **Fetched**
35. IEEE EDS compact-model touchstones — https://eds.ieee.org/images/files/Publications/touchstones.pdf — **Located**
36. IEEE TCAS-I author guidelines — https://ieee-cas.org/publication/TCAS-I/TCAS-I-guidelines-authors — **Located**
37. IEEE TCAS-II manuscript guide — https://ieee-cas.org/publication/TCAS-II/tcas-ii-manuscript-submission-guide — **Located**
38. IEEE MTT-S Information for Authors — https://mtt.org/publications/t-mtt/information-for-authors/ — **Located**
39. ACM pre-publication evaluation policy — https://www.acm.org/publications/policies/pre-publication-evaluation — **Fetched**
40. ACM CSUR author guidelines — https://dl.acm.org/journal/csur/author-guidelines — **Located**
41. ACM CSUR reviewer page — https://dl.acm.org/journal/csur/reviewers — **Located**
42. USENIX OSDI '25 Call for Artifacts — https://www.usenix.org/conference/osdi25/call-for-artifacts — **Fetched**
43. USENIX OSDI/NSDI later AE pages — https://www.usenix.org/conference/osdi26/call-for-artifacts ; https://www.usenix.org/conference/nsdi26/call-for-artifacts — **Located**

### Evaluation and reviewing methodology

44. SIGPLAN Empirical Evaluation Guidelines — https://sigplan.org/Resources/EmpiricalEvaluation/ — **Fetched**
45. SIGPLAN checklist PDF — https://raw.githubusercontent.com/SIGPLAN/empirical-evaluation/master/checklist/checklist.pdf — **Fetched**
46. SIGPLAN blog on the checklist — https://blog.sigplan.org/2019/08/28/a-checklist-manifesto-for-empirical-evaluation-a-preemptive-strike-against-a-replication-crisis-in-computer-science/ — **Located**
47. Heiser, Systems Benchmarking Crimes — https://gernot-heiser.org/benchmarking-crimes.html — **Fetched**
48. Heiser, Guide to Technical Writing — https://gernot-heiser.org/style-guide.html — **Fetched**
49. Sewell, CACM blog — https://cacm.acm.org/blogcacm/bad-reasons-to-reject-good-papers-and-vice-versa/ — **Fetched**
50. Pawlikowski, Jeong, Lee, 2002, IEEE Communications Magazine — https://doi.org/10.1109/35.978060 ; PDF https://akaroa.canterbury.ac.nz/pdf/PJL2002.pdf — **Located, not fully fetched**

### Writing guides

51. USC Libraries, CARS model — https://libguides.usc.edu/writingguide/CARS — **Fetched**
52. University of Waterloo, CARS — https://uwaterloo.ca/writing-and-communication-centre/creating-research-space-cars-model — **Located**
53. Belcher, how to write a journal article — https://wendybelcher.com/writing-advice/how-to-write-a-journal-article/ — **Fetched**
54. Belcher book page — https://wendybelcher.com/writing-advice/writing-your-journal-article-in-twelve/ — **Located**
55. Nature Scitable, Scientific Papers — https://www.nature.com/scitable/topicpage/scientific-papers-13815490/ — **Fetched**
56. Nature formatting guide — https://www.nature.com/nature/for-authors/formatting-guide — **Located**
57. cjstp paper on presenting 创新点 — https://www.cjstp.cn/CN/10.11946/cjstp.201805220456 — **Failed (no useful text loaded)**
58. 科技与出版, 科技论文写作常见问题 — http://kjycb.tsinghuajournals.com/article/2017/1005-0590/113209G-2017-10-115.shtml — **Located, not fetched**
59. Toulmin explainer (Oklahoma State) — https://open.library.okstate.edu/writingforpublication/part/section-1-for-research-argument-argument-structure-the-toulmin-model/ — **Failed (HTTP 504)**
60. Elsevier generic publishing process PDF — https://researcheracademy.elsevier.com/uploads/2018-04/Understanding%20the%20Publishing%20Process_Apr2018_Web.pdf — **Located, not fetched**

---

## 12. Round 1 conclusion

Round 1 established a usable foundation, not a finished methodology pack.

What is solid enough to design from:

- The **current Chinese standard stack** is Degree Law (in force 2025-01-01) + GB/T 7713.1—2025 (in force 2026-02-01) + GB/T 7713.2—2022 + GB/T 7714—2025 (in force 2026-07-01), with school templates still often lagging on the 2006/2015 editions.
- A **typical 计算机应用技术 academic thesis** is a single-story document: 绪论 — 相关工作 — several linked research chapters — 结论与展望; professional theses follow a design/implementation path; PhD work must show independent research plus innovative results, and must not be stapled papers.
- **创新点** should be few, typed, scoped, and written as 承继–突破–价值, aligned across abstract, introduction, and conclusion, and never stronger than the evidence.
- **Journal workflows** at IEEE/ACM share a contribution-front IMRaD-like skeleton and reviewer criteria of novelty, soundness, evaluation, and clarity; T-ED uniquely writes down a physical-validation expectation; TCOM writes down significance/novelty/usefulness and a precise conference-extension policy.
- **Evaluation** can already be encoded from SIGPLAN + Heiser for systems/applied CS, with communications and device-validation packs still needing primary statistical and measurement texts in Round 2.
- **Expert-level rigor** is Sewell's four questions plus honest scope, not infinite hedging and not infinite extra experiments.

The largest Round-2 priorities are official full texts (7713.1—2025, 7714—2025), elite-school and 学报 manuals, Zobel and Chinese writing canons from legitimate copies, and operational evaluation procedures for communications and semiconductors.
