# 计算实验执行与分析验收

本轮从已支持的单次运行扩展到重复拟合、参数化电路和跨尝试的数据分析。以下命令在技能根目录运行。正式课题的实验目录放在用户研究项目内。

## 五次独立拟合与测试

用两个确定性逻辑回归模型比较保留第三个特征后的测试对数损失。生成器的标签依赖三个特征。每个种子独立生成 256 条训练、96 条验证和 128 条测试样本，两种方法共享该组数据，在相同的三个候选轮次中按验证损失选模。每次在独立进程中重载检查点，先核对验证集输出，再导出逐样本测试预测。这个实验改变的是抽样和划分，初始化都固定为零。[实验清单](compute-smoke/ai/repeat-plan.json) · [训练和推理实现](compute-smoke/ai/repeat_fit.py)

在 Windows 的 Python 3.14.7、NumPy 2.5.4、CPU 上，两种方法各拟合五次。三特征和双特征模型的五组平均损失分别为 0.279319 和 0.420469。每个种子的三特征损失都更低，配对差均值为 −0.141150，样本标准差为 0.027266。独立从 1,280 行预测重算十个组内损失和准确数，与原始记录吻合。五对是这里的重复单位；这一结果限于该合成数据生成器和训练协议。[各重复实测值](compute-smoke/ai/repeat-metrics.csv)

```text
python -B scripts/run_matrix.py dev/compute-smoke/ai/repeat-plan.json --run-dir runs/repeat-fit
python -B scripts/compare_pairs.py --plan dev/compute-smoke/ai/repeat-units.csv --matrix dev/compute-smoke/ai/runs/repeat-fit/index.json --artifact metrics.csv --unit seed --candidate full --baseline two_features --value mean_log_loss --match test_sha256
python -B scripts/compare_pairs.py --plan dev/compute-smoke/ai/repeat-units.csv --data dev/compute-smoke/ai/repeat-metrics.csv --unit seed --candidate full --baseline two_features --value mean_log_loss --match test_sha256
```

实际在临时矩阵内改动一个已完成单元的指标文件，读取索引分析时工具报告文件内容已改变。再次执行清单，五个单元中仅该单元重跑。新结果与归档配对表一致。另用既有 NoC 逐轨迹数据重算相对随机搜索的两类负载时延差及标准差，均与归档吻合。回归还检查了整对缺失、重复、非有限值、无效分母和轨迹标识错配。[矩阵回归](test_run_matrix.py) · [配对分析回归](test_compare_pairs.py)

## 数值仿真与 RTL

- 独立执行者从技能入口处理一阶 RC 阶跃。初始电压为 0 V，输入为 1 V，时间常数与比较时刻同为 1 ms，解析端点为 0.632120559 V。显式 Euler 以 200、100、50、25 µs 步长运行到同一端点，分别高估 40.199、19.201、9.394、4.647 mV。用 `v_next = v + (1 - v) * dt / tau` 从初值迭代即可复核。79 条含初值的轨迹记录支持这组计算，步长减半后的观测阶逐渐接近 1。独立执行后已在自主实验入口补上连续数值仿真的直达链接。[数值校验规程](../references/experiment-design.md#连续数值仿真)
- 在本机 WSL Ubuntu 26.04 用 Icarus Verilog 12.0 编译单时钟 FIFO。深度取 1、3、4，每种深度运行两个种子。独立队列模型核对 892 个周期，391 次入队对应 375 次出队和 16 项复位清除。刻意取消读指针显式回绕后，深度 3 在周期编号 11 报出预期 0x0004、实际含未知位。该结果覆盖所测 RTL 功能。复跑命令为 `wsl -d Ubuntu-26.04 -- python3 dev/compute-smoke/fifo/check.py`。[设计](compute-smoke/fifo/fifo.sv) · [测试台](compute-smoke/fifo/tb.sv) · [独立参考队列与故障验证](compute-smoke/fifo/check.py)

## 环境与适用范围

Windows 用户级 NumPy 2.5.4、附带解释器的 NumPy 2.3.5 均通过实际矩阵运算。一次独立验收在新建临时 venv 内从已有 wheel 离线安装 NumPy 2.5.4，并用 `pip check` 及真实运算复验。该 venv 验收后已清理。WSL 上的 Icarus 通过寄存器编译与两拍采样检查。受测 Windows Python 缺少 PyTorch，其 CPU 和 CUDA 检查如实返回失败。本轮验证了本地 Windows 和 WSL，远程集群作业、GPU 训练和综合后时序还要在对应环境运行。[环境后端及依赖修复](../references/compute-environment.md) · [环境探针测试](test_probe_environment.py)

Windows 上运行 `python -B -m unittest discover -s dev -p "test*.py"`，55 项回归通过。另行运行 `python -B dev/noc-smoke/test_mesh.py -v`，六项 NoC 回归通过。矩阵工具的七项用例也在 Ubuntu 26.04 通过。最后一个恢复用例让普通文件占用计划中的实验目录，确认索引记下失败及尚未启动的单元；移开冲突文件后，重跑完成全部单元。
