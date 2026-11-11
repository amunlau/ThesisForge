"""Compare Icarus RTL against transaction traces from an independent queue."""

import random
import subprocess
import tempfile
from collections import Counter, deque
from pathlib import Path


HERE = Path(__file__).resolve().parent


def make_trace(depth, seed):
    queue = deque()
    pending = None
    next_id = 1
    rows = []
    events = Counter()

    def cycle(offer, drain, reset=False):
        nonlocal pending, next_id
        if pending is None and offer:
            pending = next_id
            next_id += 1
        was_full = len(queue) == depth
        valid = bool(queue) and not reset
        ready = not reset and (not was_full or drain)
        pop = valid and drain
        push = pending is not None and ready
        rows.append((reset, pending is not None, pending or 0, drain, ready, valid,
                     queue[0] if valid else 0))
        if reset:
            events["flushed"] += len(queue)
            queue.clear()
            pending = None
        else:
            events["output_stall"] += valid and not drain
            events["full_input_stall"] += was_full and pending is not None and not ready
            events["full_replace"] += was_full and push and pop
            if pop:
                queue.popleft()
                events["out"] += 1
            if push:
                queue.append(pending)
                pending = None
                events["in"] += 1

    cycle(False, False, reset=True)
    cycle(False, True)                    # read attempted on empty
    for _ in range(depth):
        cycle(True, False)                # fill with distinct words
    for _ in range(3):
        cycle(True, False)                # hold both the head and the blocked offer
    for _ in range(2 * depth + 1):
        cycle(True, True)                 # replace at capacity across two wraps
    cycle(True, True, reset=True)         # discard occupied entries
    cycle(False, True)                    # check the synchronous flush
    rng = random.Random(seed)
    for _ in range(128):
        cycle(bool(rng.getrandbits(1)), bool(rng.getrandbits(1)))
    for _ in range(depth + 2):
        cycle(False, True)                # complete a pending offer, then drain

    if (queue or pending is not None or events["in"] != events["out"] + events["flushed"]
            or events["flushed"] != depth or events["full_replace"] < 2 * depth + 1
            or events["full_input_stall"] < 3 or events["output_stall"] < 3):
        raise RuntimeError(f"Incomplete reference coverage for depth={depth} seed={seed}: {events}")
    return rows, events


def compile_rtl(source, depth, work):
    image = work / f"{source.stem}-{depth}.vvp"
    subprocess.run(["iverilog", "-g2012", "-s", "tb", f"-Ptb.DEPTH={depth}",
                    "-o", image, source, HERE / "tb.sv"], check=True, timeout=15)
    return image


def simulate(image, rows, work):
    vectors = work / "vectors.txt"
    vectors.write_text("".join(" ".join(str(int(field)) for field in row) + "\n"
                               for row in rows), encoding="ascii")
    proc = subprocess.run(["vvp", image, f"+vectors={vectors}", f"+cycles={len(rows)}"],
                          capture_output=True, text=True, timeout=15)
    return proc.returncode, proc.stdout + proc.stderr


def main():
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        source = HERE / "fifo.sv"
        for depth in (1, 3, 4):
            image = compile_rtl(source, depth, work)
            for seed in (17, 42):
                rows, events = make_trace(depth, seed)
                code, log = simulate(image, rows, work)
                passed = f"PASS depth={depth} cycles={len(rows)}"
                if code or passed not in log.splitlines():
                    raise RuntimeError(f"depth={depth} seed={seed}\n{log}")
                print(f"{passed} seed={seed} enqueued={events['in']} "
                      f"dequeued={events['out']} flushed={events['flushed']} "
                      f"full_replace={events['full_replace']} "
                      f"full_input_stall={events['full_input_stall']}")

        # Natural binary overflow is wrong for a three-entry circular buffer.
        text = source.read_text(encoding="utf-8")
        correct = "rd_ptr == DEPTH-1 ? '0 : rd_ptr + 1'b1"
        if text.count(correct) != 1:
            raise RuntimeError("Read pointer mutation site no longer matches the DUT")
        mutant = work / "bad_wrap.sv"
        mutant.write_text(text.replace(correct, "rd_ptr + 1'b1"), encoding="utf-8")
        image = compile_rtl(mutant, 3, work)
        rows, _ = make_trace(3, 17)
        code, log = simulate(image, rows, work)
        if not code or "expected(ready,v,d)=" not in log:
            raise RuntimeError(f"Expected a scoreboard mismatch for the wrap mutation.\n{log}")
        print(f"Detected read-pointer mutation (seed=17, exit={code}): {log.strip()}")


if __name__ == "__main__":
    main()
