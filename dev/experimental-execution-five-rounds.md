# 五轮计算实验能力迭代与验收

2026-11-11。每轮围绕一个独立缺口做公开网络检索，阅读与该缺口直接相关的一手材料，修改技能后检查结果。下列数值来自本机运行，文献用于确定方法和判断边界。按需加载的运行入口见 [SKILL.md](../SKILL.md)。

## 第一轮　把主题转成有辨别力的实验

**原有缺口。** 接入规则把只有题目的任务导向可行性和方案。对于“自行做实验并写成文章”，缺少执行模式及完成条件。

**检索。** 分别查找 NoC application task mapping / scheduling、genetic algorithm / contention、NIST selecting experimental design。Yan 等的原文涉及映射、静态调度、链路竞争与带局部搜索的进化方法。其结果不能直接当作源端流量注入的同问题基线。NIST 区分比较、筛选、优化等目标，由此选择实验结构。[Yan 等，ICAPS 2020](https://cdn.aaai.org/ojs/6675/6675-40-9904-1-10-20200521.pdf) · [NIST 方法页](https://www.itl.nist.gov/div898/handbook/pri/section3/pri33.htm)

**修改与检查。** 增加 `execute`，改变题目主导任务的路由。将映射、注入调度和路由器仲裁分别对应到决策变量与测量指标。以“进化选出的权重是否带来额外收益”为验收问题，安排 FIFO、固定启发式及等搜索预算的随机基线。把 SCI B 类具体名单的核验留到取得适用目录时，允许研究先开始。[接入规则](../references/intake-and-modes.md) · [自主实验研究](../references/computational-research.md)

## 第二轮　从环境发现到实际执行

**原有缺口。** “记录工具版本”不能发现两个解释器拥有不同的包，也不能区分“服务器已接受作业”和“作业产生可用结果”。

**检索。** 查找 PyPA virtual environments、pip repeatable installs 和 Slurm sbatch / job exit codes。官方文档分别给出项目级环境与版本复现、批作业提交与作业结束状态的语义。Slurm 仍要检查具体作业步骤和输出。[PyPA](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) · [pip](https://pip.pypa.io/en/stable/topics/repeatable-installs/) · [Slurm 作业提交](https://slurm.schedmd.com/sbatch.html) · [退出码](https://slurm.schedmd.com/job_exit_code.html)

**修改与检查。** 加入项目内依赖安装、复杂环境协作、队列作业跟踪与失败重跑规则。新工具分别负责只读环境探测和运行记录。Windows 当前 Python 3.14.7 可运行纯标准库工作负载，另一个 Python 3.12.14 已有 NumPy 2.3.5。Windows 外部 PATH 未发现 Icarus，在已有的 Ubuntu 26.04 中找到并验证。此次没有新增安装。运行记录工具的六项 CLI 测试覆盖成功、失败、部分/缺失输出、旧文件与重跑。真实 NoC 实验又通过它在新目录运行仿真和分析，两次均返回 0，三个结果文件与存档 SHA-256 逐一相同。[探测工具](../scripts/probe_environment.py) · [前台运行记录器](../scripts/run_experiment.py) · [回归用例](test_run_experiment.py)

## 第三轮　验证仿真器和数字逻辑是否按规格工作

**原有缺口。** 通信仿真设计已有统计建议，有限突发 NoC 模型的排空、守恒检查以及 HDL 的实现和功能验证尚无对应操作。

**检索。** 查找 gem5 Garnet synthetic traffic injection、Icarus language flags / vvp 和 cocotb timing model。依据后端官方说明区分注入过程、编译与仿真实行，以接口语义确定时钟沿前后的检查点。[gem5](https://www.gem5.org/documentation/general_docs/debugging_and_testing/directed_testers/garnet_synthetic_traffic/) · [Icarus 编译选项](https://steveicarus.github.io/iverilog/usage/command_line_flags.html) · [VVP](https://steveicarus.github.io/iverilog/targets/tgt-vvp.html) · [cocotb](https://docs.cocotb.org/en/stable/timing_model.html)

**修改与检查。** 增加模型层次、流量守恒、可手算情形、DUT、测试台、参考模型与错误注入规程。NoC 用例覆盖单包、相向链路、源端速率限制、链路争用及优先次序，另有完整复跑对照。RTL 用 Icarus 编译并运行一个独立的两请求者仲裁器，56 个检查周期内完成 30 次传输。让优先级卡在端口 0 后，同一测试台在编号 23 的周期报出预期 10、实际 01，进程返回 1。RTL 用例检验工具链，本次 NoC 结果来自包级软件仿真。[模型与 HDL 规程](../references/simulation-and-hdl.md) · [可执行 RTL 验收](compute-smoke/hdl/check.py) · [NoC 手算与复跑用例](noc-smoke/test_mesh.py)

## 第四轮　从原始数据分析效应，验证训练与推理

**原有缺口。** 已有统计和泄漏原则还需落实到实际分析脚本、运行配对、检查点重载与测试集评价。

**检索。** 查找 NIST paired observations、scikit-learn data leakage、PyTorch save/load model 与 benchmark timing。分别核对自然配对、只在训练集拟合变换、评估模式和异步设备计时。[NIST 配对分析](https://www.itl.nist.gov/div898/handbook/prc/section3/prc311.htm) · [scikit-learn](https://scikit-learn.org/stable/common_pitfalls.html) · [PyTorch 重载](https://docs.pytorch.org/tutorials/beginner/basics/saveloadrun_tutorial.html) · [PyTorch 计时](https://docs.pytorch.org/tutorials/recipes/recipes/benchmark.html)

**修改与检查。** 加入预期运行矩阵、行键与缺对检查、统计单位、效应方向、聚合权重和模型选择/重载规则。NoC 按轨迹配对，每种负载 12 个独立种子，四种方法共 96 次留出运行，每次交付 768 个包。NumPy 实例在 CPU 上从 256 条合成训练样本拟合模型，用 96 条验证样本选择轮次，然后在 128 条留出样本上推理。常数基线答对 68 条，逻辑回归答对 115 条，重载前后所有测试 logits 逐项相同。[分析规程](../references/data-analysis.md) · [NoC 配对汇总](noc-smoke/results/summary.csv) · [CPU 训练源码](compute-smoke/ai/train_and_reload.py) · [训练与推理结果](compute-smoke/ai/result.json)

## 第五轮　从主要比较写到结论并复算

**原有缺口。** 现有规则要求结论与材料一致，执行模式还需要实际成稿、中心数字的复算入口以及对创新主张作出取舍。

**检索。** 查找 reproducible computational research raw data behind plots 和 NeurIPS claims / limitations / reproducibility。Sandve 等讨论如何从正文陈述追到结果，NeurIPS 清单要求贡献和适用范围与理论或实验证据相称。这里采用相应的编辑判断，具体投稿要求按目标刊物执行。[Sandve 等原文](https://doi.org/10.1371/journal.pcbi.1003285) · [NeurIPS Paper Checklist](https://neurips.cc/public/guides/PaperChecklist)

**修改与检查。** 加入“结论—表/图—分析代码—原始行—配置”的工作记录，统一摘要、结果及讨论中的比较对象、单位和范围。在新目录从零运行 NoC 搜索与评价并重新生成汇总。进化策略在均匀与热点负载上相对 FIFO 的平均差分别为 −0.244900、−0.310547 周期/包，相对等预算随机搜索分别为 +0.076714、+0.004015。两类结果共同限定论文可写的主张，优化器各自只有一个搜索种子。对应材料见 [原始记录](noc-smoke/results/paired.csv)、[计算代码](noc-smoke/analyze.py) 与 [示例研究文章](noc-smoke/article.md)。

## 复核入口

独立复查发现旧审查清单对所有网络实验一律要求按稳态精度停止并删除暂态。对本次从空网到排空的负载，删除初段会改变被测量的时延。已按 Law 的终止型/稳态区分同步修改设计、选域与审查规则。NoC 案例的完整性检查依赖 Python 断言，现对禁用断言的优化模式显式中止，并在独立新目录生成正式输出。两种搜索均已由另一执行者重跑，384 次训练仿真与 96 次留出仿真得到归档数值，据此写成上述短文。[Law，WSC 2004，第 3–4 节](https://www.informs-sim.org/wsc04papers/009.pdf)

在技能根目录执行下列指令。HDL 项需能调用 Icarus Verilog 和 vvp 的环境，AI 项需含 NumPy 的解释器。

```text
python -B dev/noc-smoke/test_mesh.py -v
python -B dev/noc-smoke/analyze.py dev/noc-smoke/results
python -B dev/test_run_experiment.py -v
python -I -B dev/compute-smoke/ai/train_and_reload.py
wsl -d Ubuntu-26.04 -- python3 dev/compute-smoke/hdl/check.py
```

本次实测覆盖本地包级仿真、WSL 下的 SystemVerilog 功能验证与 CPU 训练推理。GPU、远程 Slurm、综合后的时序/面积和芯片实测需要相应资源再验证。研究文章是小规模验收样例，投稿前仍需按实际课题、当前相近工作及适用期刊目录评估。
