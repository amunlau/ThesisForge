# IEEE 体例要点（Editorial Style Manual，2024-07-29）

用于把已经成立的科学主张切换到 IEEE 期刊/会议的参考文献与英文排版层，不改变主张本身。依据 IEEE Author Center 提供的 *IEEE Editorial Style Manual*（生效日期 **2024-07-29**；第2轮已下载，第4轮重读核对）以及 *IEEE Reference Guide* 中已核对的条目。具体刊物若另有摘要词数、页数或栏目，以该刊作者指南为准。

本手册是体例与排版参考，**不是**修辞手册。不要从中发明一套「IEEE 限定语等级」或统一的摘要词数上限。

## 参考文献（Reference Guide）

- 文中引用为方括号顺序编码，按出现顺序编号。
- 著录形式按指南：作者名用缩写名、期刊名用标准缩写、卷号、期号、起止页、月与年；能提供 DOI 时给出。
- 从 GB/T 7714 切换过来时，只改体例层（标识符、刊名缩写、作者格式），不要改科学内容，也不要用 7714 去「纠正」IEEE 稿。

## 摘要与题名

- 摘要是独立完整的对目的、方法、结果和结论的概括，**不含引文**，通常也不含展示公式或口语。
- 摘要中变量应为 **lightface italic**；数字和单位按手册。
- 摘要词数上限是**各刊自己的规定**，不要把某一个数字写成 IEEE 全局上限。个别学会或刊物的数字，必须来自单独获取的该刊指南。
- 题名具体、简洁。IEEE 类刊物题名避免使用 new/novel（此点与既有写作约定一致）。

## 图、表与首次引用顺序

以下条目已与 2024-07-29 手册核对。这与 GB/T 7713.1 的「图/表 + 阿拉伯数字、图下表上」不是同一套记号，从中文学位论文切换到 IEEE 稿时不要混用。

- 文中首次引用图、表必须按编号顺序。
- 图在文中一律写作缩写 **“Fig.”**，即使位于句首。
- 图题通式：abbreviation “Fig.” + 编号 + period + em space + 题注正文；题注首词始终大写。分图 (a)(b) 的标引应出现在相应题注部分之前。跨页图在后续页用 “(Continued.)” 并重复描述性题注。
- 表题：表号用 **“TABLE”** 加罗马数字，居中置于表上方；描述性文字居中直接放在表号之下。

## 单位、数量与其他已核体例

- 拼写、连字符、国际单位制（SI）、常见技术术语缩写，以及题名大小写，遵循手册中的规定，不要自造内部体例。
- 单位与数量符号、范围与单位的写法见手册「Ranges With Units」及单位符号表。这与 7713.1 4.5 指向的 GB 3100 家族是两套并列体例：中文学位论文用国标/校规，IEEE 稿用本手册，不要在同一篇里混改。见 [format-and-citations.md](format-and-citations.md)。
- 基金与致谢位置以风格手册及该刊要求为准（IEEE 基金常放首页脚注，仍以现行手册为准）。
- 作者简介与照片为已发表文章的常规部分，byline 与 biography 的姓名应一致。

## IEEEtran 1.8b HOWTO（末页栏与算法体例）

来源：CTAN 记录现行版本 **1.8b**；官方用户指南 `IEEEtran_HOWTO.pdf`（28 页）已从 https://tug.ctan.org/macros/latex2e/contrib/IEEEtran/IEEEtran_HOWTO.pdf 取得（第 5 轮）。下列命令是 LaTeX 操作说明，**不是**某刊的页数上限。

- **末页栏平衡：** IEEE 只做粗略等长。推荐手动在适当位置插入 `\newpage`，或在末页第一栏顶部使用 `\enlargethispage{-X.Yin}`。若断点必须落在参考文献某条之前，使用 `\IEEEtriggeratref{n}`（默认执行 `\newpage`），也可用 `\IEEEtriggercmd{\enlargethispage{-5.35in}}` 改变触发动作。
- **不推荐** `balance.sty` 或 `flushend.sty`：指南指出它们已知不够可靠，且可能造成末页间距问题。
- **算法 / 伪代码：** IEEE 出版物用 **figure** 环境容纳不进入正文流的算法。指南建议 `algorithmic.sty` 或 `algorithmicx.sty`。**不要**使用 `algorithm.sty` 或 `algorithm2e.sty` 的浮动 `algorithm` 环境——IEEE 只用 figure 和 table 两种浮动体，且 IEEEtran 无法控制这两种宏包产生的非 IEEE 题注样式。

这与 acmart 的算法体例不同，见 [venues-acm-elsevier.md](venues-acm-elsevier.md)。学位论文中的算法仍按该校图/表或模板处理，见 [format-and-citations.md](format-and-citations.md)。

## 与个别刊物篇幅有关的限度

- TCAS-II 硬性版式（4.5 页正文 + 0.5 页参考文献等）已在第3轮写入 [venues-ieee-eds-cass.md](venues-ieee-eds-cass.md)，本轮不重复。
- 第4、5、6 轮均打开 TCAS-I 官方 *Guidelines for Authors* 页（https://ieee-cas.org/publication/TCAS-I/TCAS-I-guidelines-authors）。全文检索没有 “7–11”、没有 “max 14”、没有独立的 Regular Papers 页数或 overlength 上限；页面大量嵌入 IEEE Author Center 通用说明。因此「7–11、最多 14 页」**仍然不能**写成规则。
- ACM TOCS 的历史稿约、待核的现行栏目要求与 ACM 评审稿、出版稿的格式区别见[ACM 专刊卡](venues-acm-elsevier.md)。

需要中文学报、ACM 或 Elsevier 体例时，分别见 [journals-cn.md](journals-cn.md)、[venues-acm-elsevier.md](venues-acm-elsevier.md)、[elsevier-venue-card.md](elsevier-venue-card.md)。TON 的篇幅与摘要规则已按官方投稿页写入刊卡。
