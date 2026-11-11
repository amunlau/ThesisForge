# ThesisForge 第11轮调研报告：预注册批评、消融限度、测量不确定度、综述更新、缺失数据与专业学位基本要求

本轮是「新五轮独立研究 / 实验 / 数据」中的第 2 轮（总第 11 轮）。依据本地已核对的 research-to-report-and-briefing **v3.3.0**（SKILL 版本与入口 `/workspace/research-to-report-and-briefing/SKILL.md`，重点方法见 `references/research-and-evidence.md`）。未制作 PPT。未修改 `/workspace/ThesisForge/` 下除 `dev/` 报告副本以外的运行时技能文件，未同步用户桌面，未联系审查 bot。

观察、原文摘录、推导和建议分开写。搜索摘要不能单独支撑准备写入技能的句子。打不开的来源标为 FAIL，不用记忆填空。已结算事项（学位法硕士限度、一条主线与北大「一组相关论文」同文件两句并存、创新点位置以学校为准、北大第一人称与 6447、清华行距与篇眉、TCOM/ComSoc 无 30%、PSPB 与 ACM 25%、Heiser 标准差范围、Pawlikowski 不是 BER 事件数规则、软件学报中英文创新点字段仍未重核、T-ED IFA 保留 generally、0809 文献比例不得写成默认规则、RBR/Unbot 默示但非硬依赖等）本轮不推翻、不顺手改写。0812 现已打开，不再写「未能抽出」。

获取时间如无另行标明，均为 **2026-11-11，Asia/Shanghai（CST，UTC+8）**，大约 14:52–15:02。新来源保存在 `/workspace/thesisforge-research/round11-sources/`。上轮来源可引用原路径，不重复拷贝。

---

## 1. 研究边界与问题

### 1.1 边界

- **对象：** 第 10 版工作副本 `/workspace/ThesisForge/`，侧重点仍是独立研究、实验设计、数据处理与分析，以支撑论文工作量与创新性成果。
- **默认学科：** 计算机应用技术，兼顾通信与半导体电子。诚信约束不变。
- **本轮不做：** 已结算的格式 / 版式调研；已结算的逻辑 / 创新点位置 / 一条主线调研（除非原文与现行技能直接冲突且已打开原文，本轮未出现此类冲突）。
- **上轮报告只作背景：** `/workspace/thesisforge-research/round10-research.md`（MD5 `9b6ab578aebed0e35fc7e79287f332f8`，与任务书一致）。新结论均独立检索并核对该原文或本轮新打开的原文。

### 1.2 六个研究问题

**Q1. 预注册的批评文本。** 打开 Szollosi 等 2020（*Trends in Cognitive Sciences*，*Is Preregistration Worthwhile?*）全文。核对它反对的是把预注册当成弱理论的补丁，还是反对区分探索与验证本身。只有打开原文，才能决定技能对「预注册」一词的最终分量。打不开就标 FAIL，不得用篇名或摘要编码反对意见。

**Q2. 贡献主张式消融的方法限度。** 另找并打开讨论因素不独立、删除后重新调参、消融表上的多重比较、以及「去掉模块不等于证明该模块造成增益」的方法文献。Meyes 2019 不是这一题的答案，不用它改规程。现行消融规程里「不能自动等于因果」只标为研究判断、待补证；若找到可引用原文，给出可编码的限度句。

**Q3. 器件与电路测量在 GUM 之上的专用不确定度。** 在已编码的 GUM Type A/B 原则之上，寻找可公开取得的 NIST、IEC、JEDEC 或国内计量规程，对小样本、重复性、再现性、探针与温度控制是否有更具体的报告要求。未打开就不得写行业公式，也不得规定最小 n。

**Q4. 通信性能分析在 Pawlikowski 之外的合法原文。** 若能合法取得 Jeruchim 1984 或等价全文，再讨论误码估计的报告方式；否则维持「不写事件数」，不要用记忆补公式。

**Q5. 系统综述指南更新与缺失数据方法。** Kitchenham 2007 之后是否有作者或 EBSE 更新本改变了雪球、质量评价或协议修订的写法；未打开不得宣称 2007 已被替代。缺失数据方面，打开 Rubin 分类、多重插补或完整案例分析等可核对原文，只写原则与适用条件，不要写「必须用某一种插补」。Ralph 经验标准若吸收分册中的必要属性，必须逐条打开并去掉会议审稿色彩，避免写成学位论文法令。

**Q6. 专业学位基本要求。** 电子信息等专业学位的基本要求、或目录调整后计算机类的新文本，若能打开，与 0812 学术文本分标，不可用 0812 直接代替专业学位。打不开就保持残留，不要用记忆填空。

独立检索中若发现与本轮主题直接相关、且第 10 版尚未覆盖的其他有益方法，可以列入，但必须打开原文并标等级。

---

## 2. 对第 10 版相关文件的核对或缺口

本轮通读了任务书点名的第 10 版新写或扩写文件。判断如下。**这些是对现行文本状态的观察，不是对本轮去改运行时文件的授权。**

### 2.1 `independent-research.md`

篇幅不长，出处限度大体还在：0812 / 0810 工作量口径、Easterbrook / Kerr / Nosek 的探索与验证分离，以及「预注册是可选工具，不是学位条件」。文中仍写「不要用本轮未打开的批评短评来肯定或否定预注册」——这是编码时留下的「本轮」字样，本身不是过满，但本轮若采纳 Q1，后续编码应改成对已打开批评文本的有限度引用，而不是继续写「未打开」。未见把出处限度写丢。

### 2.2 `literature-search.md`

协议与 Wohlin 雪球步骤已经可执行。已写「不要宣称该 2007 年报告已被本出处或其他未打开的更新本替代」。本轮打开了 Kitchenham 等的**报告**指南 SEGRESS，以及 QAISER 对 2015 年书的转述，但 **2015 年书本身未打开**。因此这一限度句仍然成立：不能把「2007 已被替代」写进技能。PICOC 也还不宜仅凭二手转述删掉。

### 2.3 `data-analysis.md`

第 10 版已补上 ASA、SAMPL、Simmons、GUM 原则和「不得冒充观测」的缺失数据禁令。仍薄的地方正是本轮题目：插补 / 完整案例的适用条件写明「本轮未打开」；器件专用规程写明「未打开 NIST、IEC 或 JEDEC」。未见把 p 阈值或最小 n 偷写成默认。本轮可在这些缺口上建议补原则，但仍不得发明行业公式。

### 2.4 `experiment-design.md`

泄漏分类、调参预算、顺序过拟合、徽章可选、T-ED generally、Pawlikowski 规程都还在。消融规程第 2 步把「不能自动把性能差写成被删模块的因果效应」标为「研究判断，待下一轮打开更贴切的方法文献再补证」——这正是本轮 Q2。Jeruchim 与讲义仍标明未取得，通信规程不写事件数。文件较长，但限度句大多还在。若干「本轮打开 / 本轮未找到」的时间性措辞是编码遗留，不是本轮要推翻的实质判断。

### 2.5 `topic-and-contribution.md` 中 0812 / 0809 / 0810

0812 已打开并分标学科与 2013/2014 年文本。0809 文献比例明确不要写成默认规则。专业学位或目录调整后的计算机类新文本，第 10 版尚未收录——本轮 Q6 补这个缺口。不得用刚打开的 0854 专业学位文本去回改 0812。

### 2.6 `SKILL.md` 主流程第 3 步与资源与助手

第 3 步已写入可检验假说与独立研究步骤，表述简短，未见过满。资源与助手中的 RBR / Unbot 默示建议及「不是硬依赖、不要把版本号写死」已在第 10 版编码，本轮不重开。专业学位若写入选题或加载表，应另标 0854 / 教指委文本，不能让第 3 步默认只指向 0812。

### 2.7 `templates/experiment-plan.md`

已有「看结果之前声明」、泄漏检查、调参预算等栏，与第 10 版分析前登记一致，没有把数值阈值写进模板。若编码消融限度或缺失数据原则，可加提示栏，但不要把模板写成必填法令。

---

## 3. 已打开来源清单与等级

等级约定：E 表示已打开原文、可引用；S 表示有出处但须写明限度（预印本、转载、课程副本、活仓库、领域外指南、非正式出版商副本等）；U/FAIL 表示未取得可核对正文，不得编码为规则。搜索命中或摘要不等于已精读。

### 3.1 Q1 预注册批评

| ID | 来源 | 等级 | 身份 |
| --- | --- | --- | --- |
| S1 | Szollosi, Kellen, Navarro, Shiffrin, van Rooij, Van Zandt, Donkin，预印本题为 *Is preregistration worthwhile?*（文件名曾为 *Preregistration is redundant, at best.pdf*），PsyArXiv / OSF，DOI 10.31234/osf.io/x36pz，2019-10-31；OSF 元数据同时给出正式发表 DOI 10.1016/j.tics.2019.11.009。本轮打开的是 OSF 主文件 `https://osf.io/download/tgan8/`，6 页 PDF，MD5 `f919409815f4fae2423c563f0391a954`。 | **S** | 作者预印本。与 TICS 短评同一作者组、同一标题，Cell 摘要首段与预印本开篇一致；**未打开** TICS 正式排印本（Cell PDF HTTP 403；Radboud 机构库「Publisher’s version」`https://repository.ubn.ru.nl/bitstream/2066/215861/1/215861.pdf` HTTP 403，与上轮相同）。引用须标明预印本，不得假装已核对正式刊出页码。 |

反向检索：Nosek 等 2018（上轮已打开，路径 `/workspace/thesisforge-research/round10-sources/pdf/nosek-2018-preregistration-unimelb.pdf`）仍是把预注册定义为区分预测与事后解释的可选工具；本轮打开的 Szollosi 预印本是对该「改进科学推理 / 补理论」论证的批评，而不是对诚实报告分析计划的全面否定。二者应并存，不要用一篇去删另一篇。

### 3.2 Q2 消融限度

| ID | 来源 | 等级 | 身份 |
| --- | --- | --- | --- |
| E1 | NIST/SEMATECH e-Handbook of Statistical Methods，§5.2.1.2 *One variable at a time*，`https://www.itl.nist.gov/div898/handbook/pri/section2/pri212.htm`。HTML MD5 `d2495fb8fcca7a4c03cb7ead785ca9ac`。 | **E** | 美国 NIST 官方公开手册，讨论 OFAT 不能反映因子交互。 |
| E2 | 同手册 §5.3.3 *How do you select an experimental design?*，`.../pri/section3/pri33.htm`。HTML MD5 `a8b6b8c01e7c4830f60e8c1097a3aaf4`。 | **E** | 按目标在比较、筛选、响应面等设计中选择；需要估计交互时，不能只用主效应 / 筛选设计应付。 |
| E3 | Melis, Dyer, Blunsom，*On the State of the Art of Evaluation in Neural Language Models*，ICLR 2018；本轮打开 arXiv:1707.05589 PDF，10 页，MD5 `dd3c984c7c998060dea3b61869672c66`。 | **E**（会议正式论文的 arXiv 版，论断以本 PDF 为准） | 公平超参控制下的架构比较；说明超参失控可使比较结论翻转。 |
| S2 | Huang，*When Do Attention-Head Ablations Support Causal Claims?*，arXiv:2610.00373v1，2026-09-30，8 页，MD5 `8a942bae04d7c05428f861aa2482e000`。 | **S** | 2026 年预印本，对象是 GPT-2 / DistilGPT2 的注意力头零化，不是贡献主张式消融的通论。可支持「一次切除结果不能自我证明因果」这一限度，不得把其实验清单写成所有论文的强制步骤。 |

Meyes 2019 仍不用来改消融规程（上轮已结算）。本轮未打开一篇专门讨论「消融表上必须用某一种多重比较校正」的通论；多重比较的一般原则仍用上轮已打开的 ASA 2016 / Simmons 2011（路径见 round10-sources），不要指定 Bonferroni 为默认。

### 3.3 Q3 测量不确定度

| ID | 来源 | 等级 | 身份 |
| --- | --- | --- | --- |
| E4 | Taylor 与 Kuyatt，*Guidelines for Evaluating and Expressing the Uncertainty of NIST Measurement Results*，NIST Technical Note 1297，1994 年版。本轮打开 nvlpubs 本 MD5 `bed4492642188c5ebc5a48b270042020`（25 页），以及 nist.gov 2017 转载本 `tn1297s.pdf` MD5 `8df8b14cc99d649dff01f97d0a6d9c06`。 | **E** | NIST 落实 GUM 的机构指南，不是器件专用规程，也不规定最小 n。 |
| E5 | Orloff 等，NIST 图书章节 *On-wafer measurements of RF nanoelectronic devices*（tsapps pub_id 921946），19 页，MD5 `239bcf0fc53173df68fc34eecd40f5fb`。 | **E** | 适用范围是**片上射频 / 纳米电子器件**的散射参数测量环境，不是通用直流 I–V 口诀。 |
| E6 | Randa 等，*Detailed Study of Uncertainties in On-Wafer Transistor Noise-Parameter Measurements*，NIST TN 1939，33 页，MD5 `2f2716f4f595654841d13d75658bf14e`。 | **E** | 片上晶体管噪声参数测量的不确定度分量研究。文中的 0.5 K 等数字是该文设定或实例，**不得**写成技能默认。 |
| E7 | NIST/SEMATECH 手册 §2.4 Gauge R&R 及 §2.4.6 *Quantifying uncertainties from a gauge study*（`mpc/section4/mpc4.htm`、`mpc46.htm`）。HTML MD5 分别为 `f37e8a7a4dc3ffaa9c29e0874750b220`、`2c196d5699f18ab1a4a10e42827116ca`。 | **E** | 生产 / 测量过程表征中的重复性、再现性、稳定性；并提到硅片电阻率测量案例。不是最小样本量法令，公式多带均匀分布等假设。 |

GUM（JCGM 100:2008）仍以上轮已打开的 BIPM PDF 为准（`/workspace/thesisforge-research/round10-sources/pdf/jcgm-100-2008-gum.pdf`）。

**FAIL / 未打开：** IEC 器件测量标准、JEDEC 程序、JJF 1059.1-2012 全文。JJF 1059.1 在「国家计量技术规范全文公开系统」（jjg.spc.org.cn）有条目，但需 FileOpen 等插件，本轮未能打开可核对正文。不得用记忆写这些文件中的公式或最小 n。NIST TN 1390 已下载（MD5 `e2643d71a9a69f5119159c0de5f79d20`），系较早期片上噪声温度测量资料，本轮未作为主要依据展开，避免把过时或过窄的设定写进技能。

### 3.4 Q4 通信误码估计

| ID | 来源 | 等级 | 身份 |
| --- | --- | --- | --- |
| FAIL-J | Jeruchim，*Techniques for Estimating the Bit Error Rate in the Simulation of Digital Communication Systems*，*IEEE JSAC* 2(1):153–170，1984。IEEE stamp 本轮未取得正文；上轮已记录的 GMU 讲义仍 HTTP 500，Missouri S&T 仍 HTTP 403。 | **FAIL** | 不得用记忆补事件数或置信区间公式。 |
| S3 | Summerfield，*Minding Your BER’s and Q’s*，1999-11-04 讲座幻灯，UCSB 课程转载，24 页，MD5 `a1396bcc9db5b760d4c3494d9ce67946`。 | **S**，且**不是** Jeruchim 的等价全文 | 光学系统 BER / Q 因子测量讲座，不是 1984 年仿真方法综述的合法替代。可证明「要谈置信区间」这一常识方向，不能用来给技能写默认错误事件数。 |
| U1 | Hamkins，*Confidence Intervals for Error Rates Observed in Coded Communications Systems*，*IPN Progress Report* 42-201，2015-05-15。官方页 `https://ipnpr.jpl.nasa.gov/progress_report/42-201/201C.html` 已打开，但只读到摘要；PDF（约 487 KB）因 TLS 中断未能保存。 | **摘要级，不得编码方法细节** | 摘要指出：编码或高阶调制下比特错误不独立，套用独立假设会得到过窄的区间。这一提示必须等全文打开后再编码。 |

合法可用的通信仿真可信度规程仍是上轮已打开的 Pawlikowski、Jeong、Lee 2002。

### 3.5 Q5 综述指南、缺失数据、Ralph 分册

| ID | 来源 | 等级 | 身份 |
| --- | --- | --- | --- |
| E8 | Kitchenham, Madeyski, Budgen，*SEGRESS: Software Engineering Guidelines for REporting Secondary Studies*，*IEEE TSE* 49(3):1273–1298，2023（在线 2022-05-10），DOI 10.1109/TSE.2022.3174092，CC BY 4.0。作者站点 PDF `https://madeyski.e-informatyka.pl/download/KitchenhamMadeyskiBudgen22TSE-SEGRESS.pdf` 本轮 TLS 失败，未能保存本地 PDF；同 URL 经抓取工具读到正文（至约第 6 节）。 | **E**（已读到正文要点；本地缺 PDF 页码，引用用章节 / 条目号） | **报告**指南，建立在 PRISMA 2020 上，并扩展到映射研究与定性综述。**不是**宣布 2007 年「如何实施」指南作废的文件。补充材料本轮未保存。 |
| E9 | Usman, Ali, Wohlin，*A Quality Assessment Instrument for Systematic Literature Reviews in Software Engineering*（QAISER），*e-Informatica Software Engineering Journal* 2023；作者副本 `https://www.wohlin.eu/einformatica23.pdf`，40 页，MD5 `2d13da1879c9b702b8ce59ce99d769f5`。 | **E** | 对**已完成 SLR** 的评价工具（15 项），不是学位论文撰写法令。它把 Kitchenham、Budgen、Brereton 2015 年书称为 revised guidelines，并转述该书对 PICO 的处理；**该书本身本轮未打开**，转述不得直接改写技能里的 PICOC。 |
| E10 | van Buuren，*Flexible Imputation of Missing Data*，Second Edition，作者站点 `https://stefvanbuuren.name/fimd/`。本轮打开 §1.2 MCAR/MAR/MNAR、§1.3.1 列表删除、§2.2.4 更精确定义、第 12 章报告与限度等章节。 | **E**（在线书，不是纸书页码本） | 明确引用 Rubin (1976) 的三类机制，并给出完整案例与多重插补的适用条件和风险。 |
| S4 | Schafer 与 Graham，*Missing Data: Our View of the State of the Art*，*Psychological Methods* 7(2):147–177，2002。本轮打开的是根特大学研讨班转载 PDF，31 页，MD5 `ce183650c2f298c268c43991747877b9`，版面为该刊论文。 | **S** | 课程 / 研讨班转载的正式期刊论文。领域是心理学方法，原则可迁移，不得把其模拟数字当成计算机学科的发生率。 |
| S5 | ACM SIGSOFT Empirical Standards 分册（GitHub `acmsigsoft/EmpiricalStandards` master，2026-11-11 取得）：`GeneralStandard.md`、`Experiments.md`、`DataScience.md`、`EngineeringResearch.md`、`QuantitativeSimulation.md`、`Benchmarking.md`、`SystematicReviews.md` 等。各文件 MD5 见第 3.7 节。 | **S** | 活仓库，不是冻结出版页码。总册定位与「不要 gotcha」上轮已打开（`round10-sources/pdf/ralph-empirical-standards-2021.pdf`）。分册带有会议审稿清单色彩，吸收时必须去掉。 |

**未打开：** Rubin 1976 *Inference and Missing Data*（*Biometrika*）原文；Kitchenham、Budgen、Brereton 2015 年 CRC 书《Evidence-based software engineering and systematic reviews》全文；SEGRESS 补充材料 PDF；Sterne 等 2009 BMJ 多重插补全文（HTML/PDF 均 403）。Rubin 分类本轮以 van Buuren / Schafer 中已核对的转述与定义为准，不假装打开了 1976 年原文页码。

Kitchenham 与 Charters 2007、Wohlin 2014 仍用上轮 / 更早轮次已打开的文本（`/workspace/thesisforge-research/round2-sources/kitchenham-slr-2007.pdf`，`round10-sources/pdf/wohlin-2014-snowballing.pdf`）。

### 3.6 Q6 专业学位

| ID | 来源 | 等级 | 身份 |
| --- | --- | --- | --- |
| E11 | 全国工程专业学位研究生教育指导委员会网站「类别简介及其学位基本要求」之 **0854 电子信息** 现行页：`https://meng.tsinghua.edu.cn/wjfg/zyxwlbjjjjbyq/6328.htm`（索引 `.../index.htm`）。HTML MD5 `186ac66d559793c3283f8f582503d65d`。页内写「四、编写成员：全国工程专业学位研究生教育指导委员会」，正文有「截至 2022 年底」的数据。 | **E**，但须写限度 | 这是教指委网站上的类别简介及硕、博士专业学位基本要求，**不是**与 2014 年《一级学科博士、硕士学位基本要求》上册同版式的高等教育出版社纸书；页面本身未见单独的发布文号或发布日期。2023-01-09 该网曾就「征求意见稿」发函（E12）。编码时必须分标为专业学位、教指委网站现行文本，不得写成「国务院学位委员会 2025 年新国标」。 |
| E12 | 《关于〈电子信息等8个专业学位类别简介及其博士、硕士学位基本要求（征求意见稿）〉征求意见的函》，工程教指委秘〔2023〕2 号，2023-01-09，`https://meng.tsinghua.edu.cn/xxfb/tzgg/6246.htm`。HTML MD5 `b6130812f368afcc526fe93abc83bf72`。依据学位办〔2022〕23 号委托编写。 | **E** | 证明 2023 年初仍是征求意见阶段；该页未提供附件 PDF。不能把征求意见稿与现行页混称为同一具名版本，除非另找到颁布件。 |
| E13 | 全国工程专业学位研究生教育指导委员会，《工程类专业学位类别硕士学位论文基本要求（试行）》，2023 年 12 月；门户 PDF `https://meng.tsinghua.edu.cn/docs/20240508133731877935.pdf`（文件名日期 20240508），21 页，MD5 `c7789fab37e905e1c94456f2e164912e`。 | **E** | 适用于电子信息等 8 个类别硕士学位论文工作的**指导性文件**，依据「学科专业简介及其学位基本要求」以及教研〔2023〕2 号、学位〔2020〕20 号。培养单位还要制定实施细则。这不是 0812，也不是博士专业学位全文。 |

学校自定「授予标准」（如检索中出现的昆明理工等院系页）本轮不当作全国基本要求打开。

### 3.7 主要文件指纹（便于复核）

除上表外，PsyArXiv 早期 `/download` 链接只返回了 OSF 单页应用外壳（MD5 `72882ec06c08c08879452477cdc00ac4`），**不是**论文 PDF。正式用 S1 的 primary 文件。Ralph 分册 MD5：GeneralStandard `a5c1b23dbb1ce5723196f457409cf675`，experiments `d56ab16ab146b3cefc0caa0c69d902c1`，datascience `54852ded7fa52474494e3fa6796face1`，EngineeringResearch `95656cb4c04c2748bcfa1033e7fd4105`，QuantitativeSimulation `22161ba58609fcc8f5f71d7459401697`，Benchmarking `412132587ea760cbc9a70995e141866e`，SystematicReviews `b5c112c8aba8a115718423f3ffc7ec6d`。

---

## 4. 按问题组织的发现

### 4.1 Q1 预注册批评：反对的是「用预注册补弱理论」，不是反对诚实区分探索与验证

**观察。** 预印本开篇把支持者的论点分成强、弱两式，并声明批评范围：

> Proponents of preregistration argue that, among other benefits, it improves the diagnosticity of statistical tests [1]. In the strong version of this argument, preregistration does this by solving statistical problems, such as family-wise error rates. In the weak version, it nudges people to think more deeply about their theories, methods, and analyses. We argue against both…\
> To be clear about the scope of our argument, we do not discuss the role that preregistration plays in increasing the transparency of studies and methods in depth. Our critique is focused on the use of preregistration as an attempt to improve scientific reasoning and theory development.（S1，正文第 1–2 段）

他们明确写：用预注册去补糟糕的统计实践，并不能补偿弱理论；弱理论即使预先注册，其预测也不比随机更好。另一方面，当理论足够强时，事后的**科学**推断并没有先天问题，只要事后解释也受到同样严格的检验；不能只因为想法出现在实验之后、或没有预注册，就不认真对待。

> Solving problems of poor statistical practice with preregistration does not compensate for weak theory [6]. … Researchers can preregister bad theories…\
> …unlike post-hoc comparisons in statistical inference, there is nothing inherently problematic about post-hoc scientific inference when theories are strong. … There is no reason not to take such post-hoc theories seriously just because they were thought of after or were not preregistered before an experiment was conducted.（S1，*Fixing science with statistics* 一节）

结论不是「禁止使用预注册」，而是：预注册既不能诊断、也不必然产生好科学；它应当是选项，但把预注册当作要求、奖励或推广（例如徽章、资助）并不值得。

> Preregistration is not diagnostic of, nor does it necessitate, good science. … because bad theories, methods, and analyses can also be preregistered…\
> We conclude that, although preregistration should be an option for anyone who thinks it improves their research, requiring, rewarding, or promoting it (e.g., with badges, research funding, etc.) is not worthwhile.（S1，*Preregistration is non-diagnostic, and potentially harmful* 一节）

文中引用了同一作者的另一篇预印本 *Arrested theory development: The misguided distinction between exploratory and confirmatory research*（S1 参考文献 7）。**该另一篇本轮没有作为独立全文打开**，不能把它的标题读成 TICS 短评本身的论点。就已打开的这篇短评而言，它批评的是把预注册当成改进推理或补理论的装置，并反对强制或奖励预注册；它没有要求取消「事先写清主指标、事后探索必须标明」这种诚实报告。

**含义。** 技能对「预注册」的分量可以收紧一句限度，但不应推翻第 10 版已编码的 Kerr / Nosek 区分：主分析仍应在看结果之前写下，探索可以报告但必须标明。预注册仍然只是可选工具，不是学位条件，更不能替代对照设计、诚实报告或理论工作。

**不要写成什么。** 不要写成「Szollosi 反对区分探索与验证，因此技能应删掉这一区分」。不要写成「禁止预注册」。不要用预印本页码冒充 TICS 第 24 卷第 94–95 页。不要把徽章政策已结算的「可选」再改成对预注册徽章的新全国禁令以外的内容——学位论文强制预注册本来就不能写。

### 4.2 Q2 消融限度：交互、公平调参、以及「切除结果不能自我证明因果」

**观察 1：因子不独立 / OFAT。** NIST 手册用「一次只变一个输入、把该输入固定在所谓最佳值再变下一个」定义 OFAT，并指出：若真实模型存在交互（文中示例 \(Y=X_1+X_2+X_1 X_2\)），某一因子对输出的作用取决于另一因子的水平，OFAT「leaves us in the dark about factor interactions」（E1，§5.2.1.2）。手册在选设计时也把「要估计交互甚至二次效应」与只要筛主效应的设计区分开（E2，§5.3.3）。

**含义。** 贡献主张式消融若只做「去掉一个模块、其余保持原样」，在模块之间可能交互时，不能把各列差值读成彼此独立的主效应，更不能把「去掉后变差」自动说成「该模块造成了增益」。这与现行消融规程「按声称的因素有计划地去掉或替换」不冲突，但给「不能自动等于因果」补上了可引用的实验设计依据。

**不要写成什么。** 不要规定学位论文必须做满因子设计或必须估计全部二阶交互。不要把手册里的化工 / 过程改进例子改写成计算机实验的法定设计。不要用 Meyes 2019 来承担这一句。

**观察 2：删除后重新调参。** Melis 等写：模型表现不仅取决于架构（和数据），而且强烈依赖于影响学习、正则和容量的超参；超参依赖是实验中常常控制不足的变异来源，可能造成不成立的经验主张。他们在大规模自动调参之后发现，先前据称更好的架构在公平控制后并不优于适当正则的 LSTM（E3，摘要与第 1 节）。他们还建议：引入许多新超参、或只在很窄的超参范围内才好的模型，应当在发表实践中被标明（E3，第 1 节末）。

**含义。** 「去掉模块后不重新调参，直接与为完整模型调好的超参比较」会把模块效应与「超参是为完整模型而设」混淆起来。技能可要求：披露各变体是否在相当预算下重新调参；若没有重调，解释并限制因果措辞。这与第 10 版已有的「公平超参预算」「看到测试结果后再只给完整模型重新调参，不可」是同一方向的补强，而不是改成必须使用某种调参器或必须做满几千次试验（Melis 自己也写，即使超参集合很小，仍可能需要大量评估才收敛）。

**不要写成什么。** 不要写「必须用 Google Vizier / 必须做数千次试验」。不要把语言模型实验的结论写成所有消融的唯一合法协议。

**观察 3：去掉不等于证明该模块造成增益。** Huang 2026 预印本的对象是语言模型注意力头的零化。其方法论主张写得很窄、也很清楚：一次单头消融的结果「is not self-certifying」；要作可辩护的因果解读，至少要核实干预在投影意义上到底切掉了什么、所用指标是否离开了地板 / 天花板、以及效应是否在预留数据上超过匹配对照（S2，摘要与结论）。作者在限度一节明确：他们并不主张那五个头「在机制上计算 induction」（S2，§5）。

**含义。** 这可以作为「去掉模块后的性能差不能自动写成该模块的因果效应」的直接方法文献，从而把现行规程中「待补证的研究判断」升级为有出处的限度句。但其实验检查项（钩子位置、对数概率、1000 次随机头对照等）只属于该文设定，不能做成通用学位论文清单。

**消融表上的多重比较。** 本轮没有打开专门针对消融表的校正论文。上轮已打开的 ASA 2016 第 4 条与 Simmons 等关于未披露分析灵活性的讨论，已经支持：对多模块、多指标、多种子的表格做多次比较时必须披露，并说明如何处理；仍不指定某一种校正为默认。不必为了填这一空而发明规则。

### 4.3 Q3 在 GUM 之上：可以补充报告要求，但不能写行业公式或最小 n

**观察。** NIST TN 1297 与 GUM 一致地区分 Type A / Type B，并写：

> Type A evaluations of uncertainty based on limited data are not necessarily more reliable than soundly based Type B evaluations.（E4，§4.3 附近）

这加固了现行技能「n 较小时不要套用大样本区间，可补充 Type B 并写依据」「不规定最小 n」。TN 1297 是 NIST 测量结果的机构指南，适用范围仍是可表征为基本上单一值的测量，没有给出半导体器件的必测只数。

片上射频测量章节要求稳定的测量环境，「free from both significant mechanical noise as well as fluctuations in temperature and humidity」；电缆应尽量减小温度、湿度和弯折引起的相位变化；微波测量对探针接触质量和重复性特别敏感，探针触点在接触时通常会横向滑移约十到五十微米（E5，平台与探针各段）。这是**报告与控制要求**，不是最小 n。

NIST TN 1939 在晶体管噪声参数测量中，把探针损耗、环境温度、输入端噪声温度等列为不确定度分量，并用 Type A / Type B 仿真来组合（E6，目录与第 4 节）。文中出现的环境温度不确定度 0.5 K 等，是该研究的设定或实例。

手册 Gauge R&R 一节把重复性、再现性、稳定性列为测量过程表征的对象，并说明可用量规研究为不确定度评定提供依据；同时警告：若测量过程随后发生变化，量规研究得到的标准差就不再适用；还提到硅片电阻率测量的 Type A 案例（E7，§2.4 与 §2.4.6）。其中分辨率、回滞、漂移等换算公式假定了均匀分布等条件，不是普遍必用的行业法定式。

**含义。** 技能可以在 GUM 原则之上补两句有范围的报告要求：（1）做片上射频 / 探针测量时，应报告并控制温度、湿度、探针接触与定位等对重复性有影响的条件；（2）若声称重复性或再现性，应说明评定所依据的重复结构（同一操作者 / 同一仪器的重复，还是换人、换日、换仪器），不要只用一次扫描代替。仍然不规定最小器件数，不把某篇 NIST 笔记里的数字写成默认。

**不要写成什么。** 不要写「必须测 N 只器件」「环境必须控制在 ±0.5 K」「探针滑移必须是 10–50 µm」。不要把射频噪声参数或纳米电子片上测量的条款，套到所有直流 I–V 或电路仿真。不要引用未打开的 IEC、JEDEC、JJF 公式。不要把通信仿真或机器学习测试分数改称按这些规程计算的测量不确定度。

### 4.4 Q4 Jeruchim 仍 FAIL，维持「不写事件数」

**观察。** Jeruchim 1984 全文仍未合法取得。Summerfield 1999 讲座讨论了在独立错误、二项式计数下可以计算置信区间，并提出「需要数多少个错误」的问题（S3，约第 16 页起）。这是讲座，对象是光学系统实测 BER / Q 因子，不是该 1984 年 JSAC 论文的替代，也不能用来给技能写默认事件数。Hamkins 2015 的官方摘要（U1）指出：编码或高阶调制下比特错误不独立，盲目套用独立假设会得到不适当的过窄区间；并声称提出了用每个码字误比特数的一、二阶样本矩来计算区间的方法。摘要级内容不足以支撑把该方法或任何数值规则写入技能。

**含义与不要写成什么。** 继续维持现行写法：定性说明不确定度随观测到的错误事件增多而缩小；报告观测窗口、观测到的错误个数和不确定性陈述；**不写入任何具体错误事件数或数值置信区间公式**。通信仿真可信度仍走 Pawlikowski 规程。不要用讲座或摘要里的「大约 100 个错误」一类记忆或检索摘要来填空。

### 4.5 Q5 综述指南并未在已打开文本中「替代 2007」；缺失数据可写原则，不能写「必须某种插补」

#### 4.5.1 Kitchenham 之后的文本

**观察。** SEGRESS 开篇把自己的目标写成：为软件工程**二次研究的报告**提供指南，以回应报告质量的批评。它评估 PRISMA 2020，并说明原有 SE 系统综述实施指南（文中引为 [5]、[6]，对应 Kitchenham 2004 与 Kitchenham 与 Charters 2007 一路）来自医疗领域指南，因而 PRISMA 2020 可能对 SE **报告**有用（E8，第 1 节）。它把 PRISMA 的 risk of bias 与原先常说的质量评价、limitations 与效度威胁对应起来，并在条目 24c 要求：说明并解释对注册信息或协议所作的修改。对映射研究，若干与效应量、综合、跨研究偏倚有关的条目可省略或改为可选。它没有在已读部分宣布 2007 年实施指南作废，也没有改写 Wohlin 的后向 / 前向雪球步骤。

QAISER 是评估**已经写成的 SLR** 的 15 项工具。它把 2007 年报告与 2015 年书并列为指南来源，并写：2007 年曾建议用 PICO 组织研究问题，而「revised guidelines [31]」（书目为 Kitchenham、Budgen、Brereton，CRC，2015）「excluded the suggestion for using this structured approach」（E9，约第 443–445 行附近）。它还把 Wohlin 2014 当作雪球指南，并在评价指导中出现「可接受的前向 / 后向轮次数」、AMSTAR 2「最近一次检索宜在 24 个月内」等审稿式尺度。

**含义。** 可以建议：若作者写过检索或综述协议，改动必须记录并解释（这与现行「看到结果后再改纳入标准，必须记录」同向，可用 SEGRESS 24c 加固）。系统综述的**报告**若要与国际报告清单对齐，可把 SEGRESS / PRISMA 2020 列为可选参考，尤其当作者真正声称做了系统综述时。质量评价应说明目的，并按初级研究类型选择评价工具，而不是只用刊物级别——QAISER 与 SEGRESS 都支持这一点，且与现行技能已有方向一致。

**不要写成什么。** 不要宣称「Kitchenham 2007 已被 SEGRESS 或 2015 年书替代」——2015 年书未打开，SEGRESS 是报告指南。不要仅凭 QAISER 的转述删掉技能中的 PICOC。不要把 QAISER 的 15 项、24 个月时效或「可接受的雪球轮次」写成学位论文或选题轻量检索的强制规则。不要把 2020 版 PRISMA 从本出处写成所有计算机应用技术论文的强制流程。选题阶段的轻量变体仍然有效。

#### 4.5.2 缺失数据

**观察。** van Buuren 写：Rubin (1976) 把缺失问题分成三类；若每一例缺失概率相同，则为 MCAR；若只在由已观测数据定义的组内相同，则为 MAR；若还依赖未观测信息（包括缺失值本身），则为 MNAR。MCAR「often unrealistic」（E10，§1.2）。更精确的定义见 §2.2.4 的条件概率式。

关于完整案例（列表删除）：它是许多软件的默认；**若数据为 MCAR**，对均值、方差和回归系数的估计无偏，标准误对缩小后的子样本是正确的，但相对全部可用数据往往更大；**若不是 MCAR**，则可能严重偏倚；即使在 MCAR 下也可能因为丢掉大量样本而浪费效率（E10，§1.3.1）。

Schafer 与 Graham 给出更细的例外：案例删除「generally valid only under MCAR」；在少数情形下，对某些参数（例如他们举的、在特定单变量缺失格局下 Y 对 X 子集的回归）在 MAR 下也可以有效且有效率，但这一结果不自动推广到相关系数或 Y 的边际分布；非 MCAR 时，完整案例可能无法代表总体；即使 MCAR 成立，若 Y 与已观测 X 高度相关，丢掉不完全记录也会浪费预测信息。他们的主要优点是简单：若只丢掉很小一部分样本，方法可以相当有效，但仍应检查被丢掉的案例是否过分有影响（S4，第 155–156 页，「Properties of case deletion」）。他们总体推荐在 MAR 下使用极大似然或贝叶斯多重插补，并讨论非 MAR 的困难；同时开篇就写「no single procedure that is technically correct in every situation」。

van Buuren 还写：多重插补「is not a simple technical fix」；需要判断缺失机制、设定插补模型并检查；MICE 算法并非在一切条件下都有事先保证的收敛；编辑或审稿人「increasingly expecting」多重插补，哪怕作者有充分理由不用（例如缺失例很少），但作者引用这一现象是为了讨论报告策略，不是设立 5% 阈值（E10，第 12 章报告与限度）。

**含义。** 技能可补：先交代缺失机制的合理假设（MCAR / MAR / MNAR），再选择方法并报告。完整案例不是普遍禁止，也不是普遍安全：在非 MCAR 时可能偏倚，在 MCAR 下也可能低效。多重插补或似然方法是 MAR 下常用的原则性做法，但不是唯一合法选择，不能写成「必须用多重插补」。继续禁止把插补值排成与实测无法区分的「观测」，禁止用生成式补全冒充观测。

**不要写成什么。** 不要写「必须用 MICE / 必须用某种插补」。不要写「缺失不到 5% 就可以列表删除」。不要把 Schafer 血压模拟表中的数字当成计算机实验的判据。不要假装打开了 Rubin 1976 原文页码。

#### 4.5.3 Ralph 分册

**观察。** 各分册都区分 Essential / Desirable / Extraordinary，并带有给审稿人的初始检查、反模式和「无效批评」。总册已有的「不要机械、僵硬、勾框或 gotcha」仍然适用。关键适用范围：

- **Experiments** 明确只适用于有人类被试、操纵自变量并控制外来变量的受控或准实验；无人类被试的实验应看 Data Science 或 Engineering Research（S5，Experiments「Application」）。
- **Engineering Research** 适用于提出并评价算法、模型、系统、工具等制品，要求描述制品、说明必要性，并用行动研究、案例、有人实验、定量仿真、基准或「另有清楚有说服力理由的方法」做经验评价，以及与当代替代或基准比较（或说明为何无法比较）。
- **Data Science** 强调数据如何选取与预处理、基线、指标，以及超越单维汇总、报告变异或分布信息——与现行数据分析条款同向。
- **Quantitative Simulation** 要求说明模型、工具与版本、校准、不同抽象层次的验证、协议（含每场景运行次数、稳态或终止条件）以及假设。这与 Pawlikowski 的事先精度、序贯停止、点名暂态处理可以互补，但不能取代通信领域已编码的规程。「必须公开全部代码」只出现在 Desirable，不是 Essential。

**含义。** 可以有限度吸收「与主张类型相称的评价」「报告分布而不仅是均值」「仿真要写模型、版本、校准、验证与停止规则」等原则。必须去掉会议审稿色彩：不要把 Essential 清单当成学位论文拒稿标准，不要把人类实验的样本量 / 随机分配 / 功效分析套到机器学习训练、器件 I–V 或网络仿真，不要把「必须公开代码」升级为学位条件。

**不要写成什么。** 不要整份复制分册。不要用 Engineering Research 的评价菜单去否定纯理论证明或 T-ED 政策已覆盖的器件验证方式。不要把 Systematic Reviews 分册写成所有学位论文必须先做系统综述。

### 4.6 Q6 专业学位文本已打开，必须与 0812 分标

**观察。** 0854 页把电子信息定义为与行业任职资格相联系的专业学位；2018 年目录调整后，原工程硕士中的计算机技术、软件工程、电子与通信工程、集成电路工程等，以及工程博士中的电子与信息，统筹对应到电子信息类别；2021 年工程教指委〔2021〕1 号指导性目录列出十二个领域方向，其中包括计算机技术、软件工程、通信工程、集成电路工程、人工智能等（E11，「专业学位类别概况」）。自 2020 年起按调整后类别招生、培养和授予。这与 0812 计算机科学与技术**学术学位一级学科**不是同一文本。

硕士专业学位基本要求中的规范与实践条款，与 0812 学术文本明显不同。例如：专业实践原则上不少于半年，已有两年及以上企业工作经历的全日制工程类硕士可申请免修；学位论文选题「直接来源于生产实际或具有明确的工程背景」；形式可为专题研究类论文、调研报告、案例分析报告、产品设计（作品创作）报告或方案设计报告；「工作量饱满，应在导师组指导下独立完成」（E11，「二、硕士专业学位基本要求」之实践训练、学位论文规范要求）。博士专业实践累计不少于 1 年；创新性要求强调对工程实践与产业的贡献，并列举成果鉴定、发明专利、标准、软著、论文、奖励、应用与经济效益证明等支撑材料（E11，「三、博士专业学位基本要求」）。「工作量饱满」同样没有定量定义。

2023 年 12 月《工程类专业学位类别硕士学位论文基本要求（试行）》进一步把五种形式写为适用于八个工程类别硕士的指导性文件，并写培养单位应根据办学定位补充实施细则（E13，概述之编制依据、适用范围与第二章）。它依据「学科专业简介及其学位基本要求」，与 E11 相互指向，但不能互相替代为「已经看到纸质国标全书」。

**含义。** 用户题目若走电子信息等专业学位，技能应加载 0854 / 教指委文本及（硕士）2023 年 12 月试行论文基本要求，而不是用 0812 学术基本要求直接代替。实践时间、论文形式、选题来自工程实际、工程伦理等，都应标为专业学位条款。计算机技术作为 0854 下的领域方向，不能写成「目录调整后计算机类学术学位已经改成这份文本」。

**不要写成什么。** 不要用 0812 五类创造性成果去改写专业学位的创新与成果要求，也不要用 0854 去回改 0812。不要给「工作量饱满」发明页数或实验组数。不要把教指委网站现行页写成 2025 年学位法实施细则或高等教育出版社 2014 年上册的新版。不要把两年工作经历免修实践、或博士一年实践，写成学术型学位的要求。不要把某校自己的授予标准当成全国基本要求。

---

## 5. 建议编码的 A 项，以及明确不要编码的残留

下列 A 项只包含 E，或限度已经写明的 S。它们是给后续编码轮的建议，不是本轮对运行时文件的修改。

**A1. 用已打开的 Szollosi 预印本收紧「预注册」的分量，但不撤掉探索 / 验证的诚实区分。** 写明：预注册不能补偿弱理论，也不能诊断好科学；它仍是可选工具，不是学位条件，不应用学位、徽章或资助条件去强制。主指标、停止规则、纳入剔除和对照仍应在看结果之前写下（Kerr / Nosek，上轮已编码）。引用须标明这是 PsyArXiv 预印本，正式 TICS 排印本本轮未打开。

**A2. 把消融「不能自动等于因果」从「待补证的研究判断」改为有出处的限度句。** 依据 NIST 手册的 OFAT / 交互（E1–E2）、Melis 等的公平超参控制（E3），以及 Huang 预印本「一次切除不能自我证明因果」（S2，须写明对象与预印本限度）。编码句建议限于：若因素可能交互，不要把单因素去掉后的差值写成独立主效应；须披露各变体是否在相当预算下重新调参，未重调则限制因果措辞；去掉模块后的性能差不能自动写成该模块造成了增益。不写满因子设计强制，不写死调参次数，不把注意力头实验协议写成通例。多重比较继续用上轮 ASA / Simmons 的披露原则，不指定默认校正。

**A3. 在 GUM 原则之上补 NIST TN 1297 的同向限度，并给片上 / 探针测量补有范围的报告要求。** 保留「不规定最小 n」；重申有限次数的 Type A 不一定比有依据的 Type B 更可靠。对片上射频或探针测量，要求报告温度、湿度、探针接触与定位等控制条件；若声称重复性或再现性，须说明重复结构。TN 1939 与手册 R&R 只作方法参考，不把文中数字或带分布假设的换算式写成默认。

**A4. 通信误码估计维持「不写事件数」。** Jeruchim 1984 仍 FAIL。不使用讲座或摘要填公式。

**A5. 综述协议修订可引用 SEGRESS / PRISMA 条目 24c 加固「改动必须记录并解释」；SEGRESS 只作为真正做系统综述时的可选报告参考。** 明确：这不是宣布 2007 年实施指南已被替代。不把 PRISMA 2020、QAISER 15 项或 2015 年书的二手转述写成强制。PICOC 暂不删。雪球仍以已打开的 Wohlin 2014 为准。

**A6. 在 `data-analysis.md` 补缺失数据的原则与适用条件。** 采用 van Buuren / Schafer 中的 MCAR、MAR、MNAR 分类（注明 Rubin 1976 原文未打开，定义来自已打开转述）。完整案例在 MCAR 下对某些估计可无偏但仍可能低效，在非 MCAR 下可能偏倚，只在丢掉很小一部分且检查过影响时才比较简单可用。多重插补或似然方法是 MAR 下常用的原则性做法，不是唯一合法选择。继续禁止把插补或生成式补全写成与实测无法区分的观测。不写 5% 阈值，不指定某种算法。

**A7. 有限度吸收 Ralph 分册中与主张相称的评价原则，并写清适用范围。** 工程研究类题目：说清制品与评价方法，比较当代替代或说明为何无法比较。数据驱动题目：预处理、基线、分布或变异。定量仿真：模型、版本、校准、验证、运行次数与终止 / 稳态条件——与通信已有的 Pawlikowski 规程互补，不替代。Experiments 分册只用于有人类被试的受控实验。全部去掉拒稿清单色彩，不把公开代码从「可取」改成学位条件。上轮总册「不要 gotcha、未列出的属性不要临时当新标准」保持。

**A8. 专业学位与 0812 分标收录。** 电子信息（0854）加载教指委网站现行「类别简介及其学位基本要求」，并（对工程类硕士论文工作）并列 2023 年 12 月试行《工程类专业学位类别硕士学位论文基本要求》。必须标明文本性质、网站来源、「截至 2022 年底」等时间信息，以及未见与 2014 年学术基本要求同书的正式纸书。写清实践时间、多种论文形式、选题来自工程实际；「工作量饱满」仍不得发明数值。计算机技术是 0854 下的领域方向，不是用这份文本替换 0812。学校细则优先于指导性文件的空白处，但不能用某校标准冒充全国文本。

**明确不要编码的残留：**

- 用 Szollosi 否定探索 / 验证的诚实区分，或禁止可选的预注册。
- 用 Meyes 2019 改消融规程；把 Huang 2026 的注意力头协议写成通例；规定必须满因子或必须某种调参器。
- 任何最小器件数、k 的默认值、0.5 K、探针滑移毫米数；未打开的 IEC / JEDEC / JJF 公式。
- 任何 BER 事件数或数值置信区间公式；把 Summerfield 讲座或 Hamkins 摘要当成 Jeruchim 等价全文。
- 「2007 年实施指南已被替代」；删除 PICOC；把 QAISER、PRISMA 2020 或 SEGRESS 写成所有学位论文强制流程；24 个月检索时效或「可接受雪球轮次」。
- 「必须用多重插补」；「缺失少于 5% 即可列表删除」；假装打开了 Rubin 1976 原文。
- 把 Ralph Essential 清单写成学位论文法令；把人类实验条款套到无人类被试的题目；必须公开全部代码。
- 用 0812 代替 0854，或用 0854 回改 0812；给专业学位「工作量饱满」发明页数或组数；把教指委网站现行页写成学位法实施细则或 2025 年新国标。
- 上轮已列出、本轮仍成立的其他残留（0809 文献比例、p&lt;0.05、徽章强制、T-ED 删 generally 等）。

---

## 6. 给第 3–5 轮的独立调研线索

本轮没有写透、值得另开一轮、且不能假装已经结论的问题：

1. **Kitchenham、Budgen、Brereton 2015 年书。** QAISER 称其为修订后的实施指南并转述了对 PICO 的处理。必须打开该书（或可合法取得的相应章节）后，才能决定技能是否改写 PICOC、质量评价或协议修订，而不能只根据二手转述改。打开后再判断它与 2007 年报告的关系，仍然不要轻易写成「已替代」。
2. **Jeruchim 1984 或真正等价的全文。** 本轮讲座与 JPL 摘要不够。若取得 Hamkins 2015 全文（官方 PDF 约 487 KB，本轮 TLS 失败），可讨论编码系统下误码区间的报告方式，但仍须避免把某一种公式写成默认事件数规则。
3. **TICS 正式排印本。** 若后续得到 Radboud 或出版社 PDF，应用正式页码核对预印本是否有实质性删改，再决定引用形式。
4. **JJF 1059.1、IEC、JEDEC 或国内半导体测量规程全文。** 官方公开系统存在条目，但本轮未能打开正文。未打开就继续不写行业公式和最小 n。若打开，只吸收与小样本、重复性 / 再现性、探针与温度报告有关的要求，并写清适用范围。
5. **Rubin 1976 原文。** 若要对分类作页码级引用，需打开 *Biometrika* 原文或合法作者副本；本轮已可用 van Buuren / Schafer 写原则。
6. **更一般的贡献消融方法文献。** 本轮已有 OFAT、公平调参和一篇注意力头预印本。若出现讨论「删除后重调、因素不独立、消融表多重比较」的更直接通论（正式发表、范围不限于某一架构），可再收紧限度句。
7. **专业学位文本的正式颁布件。** 教指委网站现行页与 2023 年 12 月试行论文要求已可分标使用；若出现国务院学位委员会正式汇编、明确文号的颁布本或计算机类学术学位的新基本要求，应再核对是否与现行页一致，仍不得用记忆填空。

---

## 7. 收束

本轮在未改运行时技能、未同步桌面的前提下，打开了上轮未能取得的 Szollosi 预印本、电子信息（0854）专业学位基本要求的教指委现行页，以及一批与消融限度、GUM 之上的测量报告、系统综述**报告**指南、缺失数据原则有关的原文。第 10 版已经写好的独立研究步骤、主张—证据式工作量、GUM 原则和「不写事件数」不需要推翻；需要补的是预注册的理论限度、消融不能自动等于因果的可引用表述、有范围的探针 / 温度报告要求、协议修订的报告义务、缺失数据方法的适用条件，以及专业学位与 0812 的分标。Jeruchim 1984、2015 年 Kitchenham 书、JJF / IEC / JEDEC 全文仍未打开，相应规则必须保持残留，不能用摘要、转述或记忆填成事实。第 3–5 轮应优先补这些仍 FAIL 或仅有二手转述的原文，而不是重开已结算的格式与法律判断。
