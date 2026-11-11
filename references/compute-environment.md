# 确认实验后端与修复环境

先确定本次实验必需的后端和操作。例如数据分析需要读取某种文件并完成矩阵运算，RTL 需要从编译到测试台运行，GPU 训练需要指定设备上的前向与反向。优先沿用项目指定的解释器、锁文件、容器或服务器模块。用实际作业身份在运行节点执行探测，再试跑一组真实格式的输入。

## 盘点与执行

在研究项目目录中调用[环境探针](../scripts/probe_environment.py)。选用实际执行实验的解释器，把示例中的技能路径换为宿主加载的目录。Windows 原生进程、WSL 和远程 Linux 节点各自探测；在 Windows 上打开 Claude Code 或 Codex 时，仍以命令实际运行的系统为准。

Windows PowerShell 示例。项目已有虚拟环境时使用其 `python.exe`；系统解释器已满足要求时也可直接用 `py -3` 或已验证的 `python` 命令。

```powershell
$skillDir = 'C:\path with spaces\thesisforge'
& '.\.venv\Scripts\python.exe' -B "$skillDir\scripts\probe_environment.py" --workspace . --workload data --verify numpy
```

Linux 或 WSL 的 Bash 示例。没有使用虚拟环境时将第一项换为 `python3`。做 GPU 或 HDL 项目时分别采用 `--workload ai --verify torch-cuda` 或 `--workload hdl --verify iverilog`。

```bash
skill_dir='/path with spaces/thesisforge'
.venv/bin/python -B "$skill_dir/scripts/probe_environment.py" --workspace . --workload data --verify numpy
```

- 不带 `--verify` 时，只盘点当前解释器、外部 PATH 工具版本与标准库小样例。指定后端后，在 `backend_checks` 读取每项结果。多次使用 `--verify` 会运行各项检查，任一所选后端失败即退出 1，仍输出完整 JSON。仅检查当前任务确实需要的后端。
- `numpy` 实算矩阵乘法。 `torch-cpu` 和 `torch-cuda` 在所选设备上分配张量，计算并核对目标函数和梯度，记录框架版本、模块路径及设备。CUDA 检查使用分配给本进程的默认可见设备。其他框架、精度、分布式通信和显存需求，用真实项目的小批量任务另行验证。[PyTorch CUDA 运行语义](https://docs.pytorch.org/docs/stable/notes/cuda.html)
- Python 子进程沿用此次调用的隔离和用户包策略。显式配置的相对 `PYTHONPATH` 以启动探针时的目录解释。若任务通常使用用户级安装，就用同一解释器普通运行。若实验使用独立 venv，就直接调用该环境的 Python。加 `-I` 会隐藏用户级包并忽略 Python 环境变量，此时发现包缺失仅适用于该启动方式。查看 JSON 中的 `system.python` 和实际模块路径，再决定是否要安装。[Python 解释器选项](https://docs.python.org/3/using/cmdline.html#cmdoption-I)
- `iverilog` 使用外部 PATH 的 Icarus Verilog 和 vvp，在临时目录编译 SystemVerilog 并核对两个时钟沿后的寄存器值。项目内自建后端、其他 HDL 工具或特定语言扩展，按现有构建文件运行实际 DUT。验证结论写出通过的接口场景和计数。[Icarus 编译与运行](https://steveicarus.github.io/iverilog/usage/getting_started.html)

## 服务器上如何估算预算

Linux 报告主机内存、进程可用逻辑 CPU 和 `system.linux_cgroup_v2`。当本进程的 cgroup v2 路径可见时，探针沿可见祖先读取 `cpu.max`、`memory.max` 及 `memory.current`。CPU 配额以等价核数表示，例如 1.5 可对应多个 CPU 上共享的总计算时间。内存余量取各已知上限减对应层级当前用量的最小值，兄弟作业的用量变化会影响该值。数值为 null 表示此次未读到相应的有限值，挂载不可见或 cgroup v1 时也应查调度器实际分配。[Linux cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html)

在分配到的节点核对调度器分配、CPU 亲和性、磁盘配额/剩余量、可见加速器，再测单次试跑峰值和耗时。磁盘剩余空间还需考虑用户配额。根据最紧的已知约束为 BLAS/框架线程、并发试验、显存、日志和检查点留出空间。用真实训练小批次或 RTL 用例验证。配额、CPU 数或 GPU 型号变化可能影响耗时比较，记录每组实际设备与预算。[Slurm 资源申请](https://slurm.schedmd.com/sbatch.html)

## 普通依赖与复杂缺口

单个导入、动态库或版本查询失败时，先核对解释器、隔离选项、模块路径和现有工具链。若项目确实缺普通依赖，自行在项目独立环境内安装匹配版本，优先使用已有锁文件或依赖清单。用户要求安装前告知时，先说明依赖、用途和安装位置。明确要求等待确认时按约定执行。虚拟环境依赖本机解释器及平台，换系统时用项目清单重新建立。以下命令从研究项目目录运行，沿用上节的技能路径变量。

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip check
.venv/bin/python -B "$skill_dir/scripts/probe_environment.py" --workspace . --workload data --verify numpy
```

```powershell
py -3 -m venv .venv
& '.\.venv\Scripts\python.exe' -m pip install -r requirements.txt
& '.\.venv\Scripts\python.exe' -m pip check
& '.\.venv\Scripts\python.exe' -B "$skillDir\scripts\probe_environment.py" --workspace . --workload data --verify numpy
```

若已有合适的 venv，直接复用。从主题新建课题时，依据已选实现确定实际需要的包，例如数值实现用到 NumPy 就在项目 venv 中运行 `python -m pip install numpy`（这里的 `python` 指该 venv 的解释器）。记录所用版本供复跑。离线可使用来源和散列已核对、匹配平台与解释器的 wheel，或使用已备齐依赖的本地目录跑 `-m pip install --no-index --find-links <wheel目录> -r requirements.txt`。安装后用该环境继续跑项目试验。`pip check` 核对已安装包声明的依赖，后端和项目试跑分别核对原生模块导入、真实硬件及数据路径。[PyPA 虚拟环境](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) · [pip check](https://pip.pypa.io/en/stable/cli/pip_check/)

当缺口涉及主机驱动、重启、专有工具许可证、服务器账号或算力配额时，把失败命令和错误摘要、受影响的试验、已验证的替代环境、用户需要执行的最小操作及同一条复验命令交给用户。同时完成能用现有条件执行的部分。需要 GPU 延迟数据时，CPU 可用于验证输入和模型输出，GPU 性能单元留待对应设备实测。
