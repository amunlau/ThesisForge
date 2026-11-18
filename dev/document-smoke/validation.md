# 文档后端验证

2026-11-18，Windows Python 3.14.7 与 WSL Ubuntu 24.04。

`python -B -X utf8 -m unittest discover -s dev -p test_documents.py -v`：Windows 20 项通过；WSL `python3 -B -m unittest discover -s dev -p test_documents.py -v`：20 项通过。严格模式仅阻断已确定的结构错误；合法缩进和修订覆盖提示保持可继续，另有回归验证。非有限超时参数在启动外部进程前拒绝。

覆盖自定义标题样式继承、表内段落、直接属性覆盖、合法分片 REF、嵌套/未闭合域、跟踪修订、样式缺失/循环、Strict OOXML、缺页眉关系、文本框不重复计数、编号定义/缺失引用、UTF-16 DTD 拒绝、坏 ZIP、输出不能覆盖原稿；LaTeX 覆盖新工作目录、保留图形但排除旧主 PDF、BibTeX 失败不能接受第一轮 PDF、缺工具、已有输出拒绝、未解引用以及真实子进程超时终止。LaTeX 引擎成功/文献失败分支采用模拟接口验证控制流程；模拟 PDF 不是实际编译结果。

实际环境：Windows 及 WSL 24.04 未找到 pdflatex/xelatex/lualatex/BibTeX/Biber。`build_latex.py --probe` 如实返回未安装、渲染 NOT_RUN；本轮没有安装大型 TeX 环境，不能声称已完成真实 LaTeX 排版验收。

Windows Word COM 实测：用标准库生成临时合成 DOCX，包含自定义标题、正文、表格和缓存为旧值的书签引用；通过 `export_word_pdf.ps1` 生成独立更新 DOCX 与 PDF，状态 EXPORTED，字段错误为空，源文件 SHA-256 保持不变。再运行只读审计，REF 显示从旧值更新为 `Table 1`，表内段落被纳入。用现有 PyMuPDF 读取 PDF，1 页，提取内容含标题、说明、表格字段及更新引用；渲染该页并实际查看，未见文字裁切或内容遗漏。此为工具冒烟，不是学校模板合规测试或复杂论文分页验证。

源 DOCX SHA-256：`ba5505905a62abbff08c6bfe76cf5112719f7d9f818455e478ee8b9195b7f2df`

更新 DOCX SHA-256：`2330cdeae0c666a55a82e4f64ed1ad22f0a6144f5a40109eb203597aa89fef31`

PDF SHA-256：`864e74f3820bf8601914a29d569fb564a5f58557ce4736b214538ca1b4563b5b`

试件和导出位于本次系统临时目录，未进入技能安装包。检查器没有使用 Word 来改写任何用户论文。后续仍需用获准的真实模板验证字体、复杂跨节页码、脚注文本框、长表、批注修订和特定文献 recipe。

另对同一源试件进行了 PDF-only 实际导出，状态 EXPORTED；重新计算源文件 SHA-256，与上述输入完全一致。只导出 PDF 不会保存源 DOCX。
