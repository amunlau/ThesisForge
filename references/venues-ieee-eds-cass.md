# IEEE EDS / CASS 器件与电路评价政策

供半导体、电子器件、电路稿对照目标刊物的证据期望。具体实验步骤见 [实验设计](experiment-design.md) 中的器件 I–V/验证规程。不要把本页写成对所有电路论文「禁止纯仿真」的总禁令。

## EDS touchstones

来源：IEEE Electron Device Society 官方 *TouCHSTONES* PDF（用于 *IEEE Transactions on Electron Devices* 及相关 EDS 刊物的作者/审稿要点）。文件本身不是打分表，按下列质检要点使用，不要发明隐藏的分值清单。

- 论文应有**清楚的技术贡献**（新器件、机制、模型、工艺，或实质性的、非琐碎增量的进展）。
- 主张须有与之相称的证据：测量、仿真或二者兼有，方法披露到可重复的程度。
- 使用仿真时，应说明模型、校准与限度；仿真不能当成数据并不支持的物理主张的替代品。
- 相关工作与先有技术应公平对待；不鼓励过满的「首次」宣称。
- 表述清楚：图可读、单位一致、英文达到可送审水平。

## T-ED 现行 Information for Authors

来源：https://eds.ieee.org/publications/transactions-on-electron-devices/information-for-authors（第3轮取得 HTML；同内容 PDF 副本当时 HTTP 418，改用 HTML）。第 8 轮（2026-11-11）再次打开该现行页（HTTP 200），页内版权年 2025；Adequate Validation 措辞与既有转写一致，不改写。该页有常设标题 **Adequate Validation**，并写明：

> T-ED welcomes manuscripts reporting solid, rigorous research outcomes centering round devices with adequate validation. Therefore, **submissions should generally include at least partial direct physical validation of the results.**

这是现行期刊作者须知中的句子，不只是社论。副词是 **generally（一般）**，不是 always（必须一律）。本轮取得的 IFA **没有**写明纯方法类 TCAD 论文的例外。不要把「一般应有至少部分直接物理验证」改写成「任何稿件都必须有实物」；也不要把纯仿真投稿 T-ED 说成常规路径，或编造 IFA 未写出的例外。若主张本身是方法或模型，须把主张收窄到方法/模型范围，并写清校准与限度。

同一 IFA 中可写入刊卡的篇幅与摘要规则：

- 常规论文初次投稿**通常限制在含参考文献共 7 页**；超过 7 页、至多 8 页须交纳超长页费。
- 综述初次投稿不超过 **12 页**。
- 摘要 **150–250 词**，一段、自洽，不含显示公式或表格。
- Briefs 的标准长度是正式出版后的 **4 页**。

Giovanni Ghione, *Looking for quality in TCAD-based papers*（T-ED, 2019, DOI 10.1109/ted.2019.2924360）以及 Enrico Sangiorgi, *Quality in Simulation-Only Manuscripts Submitted to J-EDS*，仍列在 EDS「Editorials for Authors and Reviewers」索引中。Ghione 的合法作者接受稿（AAM）已知位于 Politecnico di Torino 机构库（https://iris.polito.it/handle/11583/2878716），但本轮 PDF 因 Cloudflare 被拦（HTTP 403 / 429），全文仍未核对；Sangiorgi 社论也未取得 PDF。**把这两篇当作尚待阅读的具名社论，不要引用未见的例外表述。**

## TCAS-I / TCAS-II

来源：第3轮已取得的常设作者指南——TCAS-I https://ieee-cas.org/publication/TCAS-I/TCAS-I-guidelines-authors ；TCAS-II https://ieee-cas.org/publication/TCAS-II/guidelines-author 。

- **TCAS-II 硬性版式：** 「All TCAS-II manuscript submissions must adhere to the strict page length requirement of **4.5 pages for Content and 0.5 for References (total 5 pages)**. The last column is reserved ONLY for references.」最后一栏若出现参考文献以外的内容，将退回作者。这是严格格式要求。
- **常设 IFA 并不禁止纯仿真稿。** 已取得的 TCAS-I、TCAS-II 常设作者指南中，都没有「本刊绝不接受纯仿真论文」这样的句子。实现类主张仍应规划测量；特刊征稿可以收紧（第2轮已见至少一次特刊 CFP 不接受纯仿真），那是**特刊规则**，不要写成 TCAS-I/II 的常设禁令，也不要说「TCAS 从不接受纯仿真论文」。
- TCAS-I 范围覆盖电路的理论、分析、设计与实际实现，以及把电路方法用于系统与信号处理。稿件「are expected to contain new results, ideas, or innovations that advance significantly the state-of-the-art。」单盲评审，至少两名审稿人。检索摘要中出现的「通常 7–11 页、最多 14 页」**未出现在已取得的 IFA 页面上**，不得写成规则。

## 三条证据轨道（与主张类型对齐）

1. **T-ED 类电子器件：** 按现行 IFA，一般应包含至少部分直接物理验证（副词是 generally）。
2. **TCAS 类电路实现：** 实现主张默认规划对已实现电路的测量；常设 IFA 并未全面禁止仿真稿。
3. **仅方法的 TCAD / 建模论文：** 仿真可以就是贡献，但主张必须落在方法或模型上，而不是未经测量的已流片器件性能。T-ED IFA 本身未列出这类例外，收窄主张时须诚实标明。
