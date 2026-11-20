# 回复台账与覆盖核查接口

仅在完整审稿/专家修改轮次需要机器核查时使用。单条回复可以沿用现有 Markdown 表，不强制建 JSON。方法和交付见[回复工作流](reviewer-response-workflow.md)；空模板见[reviewer-response-ledger.json](../templates/reviewer-response-ledger.json)。

本文件定义审稿循环的一份权威记录；覆盖报告和修改说明是它的视图，不另外维护第二套完成状态。项目已有证据台账可用稳定 ID 回指该记录；文件更新后必须重核涉及的锚点与结论，不凭更新时间认定版本优先。

## 从实际文件建立锚点

先用 [compare_manuscripts.py](../scripts/compare_manuscripts.py) 的 snapshot 子命令读取指定版本，获得 source.sha256 与 units。DOCX 和文本仅用标准库；PDF 需要当前解释器已有 PyMuPDF。源文件不会被修改。

    python <技能目录>/scripts/compare_manuscripts.py snapshot 修改稿.docx --view final --output 修改稿-snapshot.json

unit_id 是本次提取的 U000001 等 ID；文件、视图、提取方式变更后会变，不是永久段落编号。selector 同时绑定登记文件哈希、单元 ID 与实际短引。选取能唯一定位的真实片段，不把意译当逐字引文。长回复的一个短引只绑定该片段，不能据此声称全信已与台账一致。

## JSON 字段

顶层为对象：

- schema：整数 1。
- documents：文件 ID 到文件描述的映射。
- comments：原始意见列表。
- responses：回复/处置列表。

documents 中每项为：

| 字段 | 含义 |
| --- | --- |
| path | 相对项目根目录的实际路径，也可为根目录内的绝对路径；不跟随越界链接。 |
| sha256 | 实际选定版本的 SHA-256；缺失/不合法标 unfrozen，不能当已绑定；与现文件不符标 stale。 |
| role | before、after、reviews、response、final_pdf 或 marked。 |
| view | final 或 original，默认 final。仅影响支持该投影的格式；DOCX 不会因此真的接受/拒绝修订。 |
| encoding | 文本默认 utf-8-sig，旧中文可显式 gb18030；不静默猜编码。 |

标记稿需要对照原始/修改视图时，可以用两个文件 ID 指向同一 DOCX，各自标 role=marked 与不同 view。before 证据使用 marked 时必须为 original，after 证据无论 role=marked 还是 after 都必须为 final，不能通过换角色名称把原始投影当修改稿。复杂表格、段落标记和属性修订未被完整重建，仍需目标编辑器核验；文件里可见的红色/绿色不自动等于真实修订层。提取器发现段落标记、行或单元格修订时，在受影响单元的 locator 中记录 projection_ambiguities；文字保留供检查，但这类正文锚点为 projection_needs_review，不能用它独自证明当前稿含有所述改动。普通未修订段落和常规合并单元格不受该标记影响。

comments 的每项为：

| 字段 | 含义 |
| --- | --- |
| id | 唯一稳定意见 ID；保留专家原编号，另造整理编号时说明其身份。 |
| source | 原意见 selector。可来自 reviews 文件的正文或 DOCX/PDF comment 通道。 |
| aspect_ids | 可独立回答的子要求 ID 列表，全台账唯一。 |

selector 为 document_id、unit_id、quote 三个非空字符串。quote 必须实际存在于该文件对应单元且唯一匹配，重叠出现也计为多处；无法唯一定位时扩大真实短引或选择明确单元，不凭第一处命中确认位置。comments 原话保留整条或能明确定位原条目的片段；细分语义要求、补充出处和范围解释可在项目记录中保留。aspect_ids 只是已登记 ID，**不能自动证明复合意见拆分穷尽，也不能发现未登记的专家意见**。必须先回到意见原件清点，再把每个 aspect 的含义与原话对应；空清单不会获得“全部覆盖”结论。

responses 的每项为：

| 字段 | 含义 |
| --- | --- |
| id | 唯一回复 ID。 |
| comment_ids | 所回应的意见 ID；共享回复可以关联多条原意见。 |
| aspect_ids | 所回应的子要求 ID；其父意见必须也在 comment_ids。 |
| stance | accept、partial、clarify、decline、future、pending。 |
| action_status | completed、planned、not_changed、unknown。 |
| text | 台账中的实际回复文字，非空；不由核查器生成科研内容。 |
| reply_source | 可选，回复信实际文件中的 selector；未提供时只检查台账文字，不认证最终回复信。 |
| rationale | 不采纳的理由；decline 必需。partial 至少给 rationale 或 remaining。 |
| remaining | 部分处理后的残余要求或待办。 |
| evidence | 证据条目数组，可为空，但 completed 无证据会列待核。 |
| locations | 可选，实际最终 PDF 的位置记录。 |

stance 是采纳立场，action_status 是动作状态，二者不等于关切已解决。future+completed 是明确结构冲突；计划状态中出现“已修改”等完成措辞仅提示回读上下文，不直接判造假。合理澄清或有据不改也可覆盖原意见，不强制制造正文差异。

evidence 每项包含：

- kind：text、figure、format、analysis。
- description：说明该证据与要求的关系。
- before：可选，原稿 selector。
- after：可选，修改稿 selector。

正文变更证据不能来自专家批注或回复信正文。对 text，先对实际两个版本做字面单元对齐；只有两个选中单元位于同一真实变更范围，且修改稿短引不已经出现在前稿其他位置，才报告 observed_text_difference。该状态仍不证明两段语义相应或学术修改正确。仅挑两句不同的话不能充当版本变化：两份提取文本相同为 identical_extracted_text，旧稿别处已有为 prior_text_present_elsewhere，选中单元不对应变更范围为 different_selected_fragments_not_a_verified_revision，均待复核。选中短引本身相同为 same_selected_text，不能自动判未改（可能是澄清、图表、格式或不同位置）。只有修改稿片段时报告 current_presence_only：当前存在，不代表本轮新增。修改稿不可读或未提供时为 not_independently_verified，不是“没修改”。figure/format/analysis 为 nontext_review_required，需实际图面、版式或运行/分析证据；字面搜索不能替代。

locations 每项包含：

| 字段 | 含义 |
| --- | --- |
| document_id | 登记的实际 PDF 文件 ID。 |
| pdf_page | 从 1 开始的 PDF 页面序号；可自动核页数范围。 |
| printed_page、printed_lines | 可选，页面可见页码/行号；不能根据 PDF label、源码行号或固定偏移推算。 |
| verification | visual 或 unverified；这是记录者报告的状态。 |
| verified_sha256 | 声明 visual 时记录实际看过的 PDF 哈希；缺失待核，变更失效。 |
| note | 可选，核验位置、未核范围或说明。 |

脚本不会实际看页面，visual 声明也始终附 visual_independently_verified=false。它只核指定 PDF 的身份和页序范围；不能认证印刷页行号，更不能把字体或分页问题关闭。

## 核查命令与结果

    python <技能目录>/scripts/audit_reviewer_response.py case.json --root . --output response-audit.json --markdown response-coverage.md --strict

路径以 --root 为界。JSON 和 Markdown 输出必须是不同的新文件，不能覆盖任何现有文件，也不能以暂缺的输入文件路径充当输出。所有材料只读。source 文件缺失、可选 PDF 依赖缺失、未渲染、片段重复等标为待核，不自动判已改或未改。审计结束前重新检查已读材料的指纹；审计中换稿或删除材料会报输入冲突并要求重跑，不发布沿用旧锚点的 current 报告。这是冲突检查，不锁住编辑器；报告只绑定输出中记录的文件身份，之后继续改稿仍须重核。

- 默认退出 0：完成扫描，包括有待核或结构错误；不是稿件验收通过。
- --strict：确定的结构冲突、未知/重复 ID、评论或子要求漏关联、已绑定文件变更、真实引文锚点不符、明确页数越界等退出 1。
- 输入协议/路径/输出冲突等错误退出 2。
- 缺材料、启发式措辞问题、图表/格式需目检、没有前稿、空意见列表等仅列 review，不以这些提示独自阻断 strict。

报告 counts 分别列 registered_comments、registered_aspects、mapped_comments、mapped_aspects、registered_responses。分母仅为登记范围；映射完成不能称语义解决率，也不能证明原评论全集或正文事实全部检查过。source 文字命中、文件差异、动作声明、科学充分性和视觉核验分别保留状态。

对登记为 response 的文件，reply_document_coverage 另列提取的正文单元数、含当前 reply_source 短引的单元数及未绑定单元 ID/位置/短片段。未绑定可能是致谢，也可能是未登记的完成声明，统一提示 review 而非严格阻断。即使所有单元都有短引，也只说明绑定覆盖，不能称整封信的每句话已经通过核验；未读的单元、短引以外文字和其他通道仍需实际回读。

JSON 中 documents 的 coverage 继承提取器真实范围；DOCX 复杂修订、图片、嵌入对象，PDF 扫描页、公式和阅读顺序，以及 TeX include/宏展开不在这个文字接口的完整覆盖内。只要本次要求依赖这些对象，就按文档工作流继续实际核查。

## 最小填写方式

空模板默认不含假评论、假结果或假位置。先 snapshot 实际文件，再填写 documents 哈希和真实 selector；从原评论拆出子要求，然后写实际回复和证据。不要为了让检查通过而从最新版文件批量刷新旧台账哈希：版本变更需重新对照原意见、真实改动和回复声明。脚本发现无确定结构错误时，仍需完成真实的语义覆盖、改稿保真和最终文档检查。
