"""Run the arbiter and verify that its testbench detects a stuck priority."""
import subprocess
import tempfile
from pathlib import Path

here = Path(__file__).resolve().parent
source = (here / "dut.sv").read_text()
with tempfile.TemporaryDirectory() as tmp:
    work = Path(tmp)
    for label, rtl in (("original", source), ("stuck", source.replace(
            "prefer_one <= 1'b1", "prefer_one <= 1'b0"))):
        dut = work / (label + ".sv")
        image = work / (label + ".vvp")
        dut.write_text(rtl)
        subprocess.run(["iverilog", "-g2012", "-s", "tb", "-o", image,
                        dut, here / "tb.sv"], check=True)
        sim = subprocess.run(["vvp", image], capture_output=True, text=True, timeout=10)
        print(label, sim.returncode, sim.stdout.strip(), sim.stderr.strip())
        if label == "original":
            if sim.returncode or "PASS cycles=56 transfers=30" not in sim.stdout:
                raise SystemExit("Unexpected baseline simulation result")
        elif sim.returncode == 0 or "expected=" not in sim.stdout:
            raise SystemExit("The testbench did not detect the injected priority fault")
