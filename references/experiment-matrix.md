# 按清单执行与接续实验

同一研究要在若干方法、条件和种子上运行时，先列出预期单元。项目已有实验管理器时沿用它。独立的前台命令可用本技能的[矩阵工具](../scripts/run_matrix.py)串行执行，适合个人计算机或已分配的服务器计算节点。

按项目规格定义通过条件。若 DUT 违反握手规格，保留失败波形并修复实现。若程序正确执行而候选算法慢于基线、没有在预算内达到目标值或验证集选中了简单模型，将这些观测按原协议记入结果。只为改善数值而换种子会使论文高估方法的表现。

下面以两个搜索种子为例。把清单保存在研究项目的 `matrix.json`。每个 JSON 对象中的字段名须唯一。将代码、配置、锁文件和所读数据列入 `inputs`，共用输入写在顶层，单元专用输入写在对应的 `cases` 项。各单元的命令从清单所在目录运行。`outputs` 列出每个单元应交付的相对文件名，支持以 `/` 分隔的子目录，由实验命令创建。

```json
{
  "inputs": ["simulate.py", "config.json"],
  "outputs": ["metrics.csv"],
  "cases": [
    {"id": "evolution-17", "argv": ["{python}", "simulate.py", "--config", "config.json", "--method", "evolution", "--seed", "17", "--out", "{run_dir}/metrics.csv"]},
    {"id": "evolution-23", "argv": ["{python}", "simulate.py", "--config", "config.json", "--method", "evolution", "--seed", "23", "--out", "{run_dir}/metrics.csv"]}
  ]
}
```

按正式方案补齐基线、工作负载和种子，参数必须真正传入被测程序。用已验证的项目解释器执行矩阵。首项 `{python}` 展开为同一解释器，`{run_dir}` 展开为本次尝试的绝对目录。每个参数独占一个字符串；含空格的文件名保持一个元素，无须在 JSON 字符串中另外嵌入 shell 引号。子进程也可读取环境变量 `THESISFORGE_RUN_DIR`。

**可移植清单。** 项目内的文件名尽量使用相对路径和 `/`，保持大小写一致，避开 Windows 保留文件名及仅大小写不同的两个输出。运行器会按研究目录解释程序的显式相对路径及 PATH 中的相对目录。用同一原生命令名时，Windows 可按 PATHEXT 找到 `.exe`，Linux 需要相应文件具有执行权限。平台专属工具或 shell 语法使用实际后端的单独命令配置。如需写跨平台的处理逻辑，可在 `argv` 里调用项目自有的 Python 脚本。Windows 和 POSIX 对子进程的默认可执行文件搜索不同，运行器在启动前定位实际程序并记入 `run.json`。[Python 子进程路径说明](https://docs.python.org/3/library/subprocess.html#subprocess.Popen)

声明的输入文件在一次尝试中应保持原内容。需要从旧检查点继续训练时，把旧检查点作为只读输入，把新检查点写到本次输出目录。运行器保存启动前输入摘要，在命令成功、产物齐备后再次核对。输入已被改写时保留本次产物和失败记录，查清改写原因后再续跑。收到中断时，索引区分中断的单元与尚未启动的单元。

终态索引中成功单元的 `inputs_verified_after_run` 为 `true`，表示该次命令退出后的输入内容与启动前一致。旧记录缺少这个字段时，仍按当前文件、参数和产物复核决定能否复用，索引写 `null`，保留旧记录原样。如果输入曾被修改后又恢复，当前摘要无法追认它在旧命令退出时的状态。即使两次摘要相同，也无法排除两次检查之间曾发生改写再恢复。研究确有此类风险时，用只读快照在新目录重跑受影响的单元。

Windows PowerShell 与 Linux Bash 分别可如下启动。将示意的技能路径换为实际安装目录，命令从研究项目运行。

```powershell
$skillDir = 'C:\path with spaces\thesisforge'
& '.\.venv\Scripts\python.exe' -B "$skillDir\scripts\run_matrix.py" matrix.json --run-dir runs/windows-search
```

```bash
skill_dir='/path with spaces/thesisforge'
.venv/bin/python -B "$skill_dir/scripts/run_matrix.py" matrix.json --run-dir runs/linux-search
```

下文以 `runs/search` 表示选定的运行目录。单次前台实验也可通过 [run_experiment.py](../scripts/run_experiment.py) 的 `--` 传入 `'{python}'` 及脚本参数，使用启动工具的解释器。将清单、代码和数据迁到另一系统后，用该系统自己的环境和运行目录重跑；已有记录中的工具路径、文件摘要和运行目录用于原地点核验。Windows 与 Linux 上的两个进程不要同时写同一个共享盘实验目录。

- **读结果。** `runs/search/index.json` 记录本次清单的 SHA-256。运行期间按 ID 显示等待、运行及完成状态，并列出本次选用的 `run.json` 路径。各次尝试另存标准输出、错误日志和声明的产物。个别单元失败时仍执行其余单元。矩阵结束前再次复核已成功单元的输入与产物，全部成功时返回 0。分析从本次索引选择记录，检查预期行数、有效事务、样本键和指标，再按研究方案处理配对、失败、超时或删失。直接遍历历史尝试会重复计数。
- **恢复。** 修复失败原因后执行相同命令。工具检查每个单元最近一次尝试，核对退出状态、工作目录、完整命令、声明输入、启动程序及声明产物的内容摘要。失败、被中断、参数或数据变更、输出损坏的单元重新运行到新目录。目录冲突等执行器错误会写入索引，出错单元标为 `failed`，尚未启动的单元标为 `not_started`。若索引自身无法写入，应查看执行器退出码及标准错误。旧日志与产物保留。若操作系统强制结束了父进程，先确认旧子进程已停止并释放算力。
- **环境与版本。** 直接或间接读取的模块、检查点和数据分片都应纳入输入；大型数据集可用项目的不可变快照与校验清单，并先验证快照内容。硬件、驱动、线程配置或第三方包会影响比较时，把相应的实际环境记录作为输入。改变研究协议后可以开新矩阵，保存之前的清单和结果，注明哪些比较仍有效。
- **服务器。** 在实际分配的节点运行上述前台命令，并给实验所需的时间和资源。目录锁避免两次启动同时修改同一索引。多节点共享盘需支持可靠的进程锁；站点作业数组或并行任务可沿用集群管理器分配不同的运行目录，再汇总作业终态。Python 提供的文件锁随句柄关闭释放。[Windows 文件锁](https://docs.python.org/3/library/msvcrt.html#msvcrt.locking) · [Unix 文件锁](https://docs.python.org/3/library/fcntl.html#fcntl.flock)
