"""Clocked single-unit packet mesh with deterministic XY routing."""
from collections import defaultdict, deque
from dataclasses import dataclass
from hashlib import sha256
import math
import random

if not __debug__:
    raise RuntimeError("Run without -O or PYTHONOPTIMIZE so the experiment's integrity checks execute.")


SIDE = 4
NODES = SIDE * SIDE
BURSTS = 12
BURST_SIZE = 4
PERIOD = 5


def route(source, destination):
    if source == destination or not (0 <= source < NODES and 0 <= destination < NODES):
        raise ValueError("XY route needs distinct mesh nodes")
    x, y = source % SIDE, source // SIDE
    tx, ty = destination % SIDE, destination // SIDE
    edges = []
    while x != tx:
        step = 1 if x < tx else -1
        edges.append((x + y * SIDE, x + step + y * SIDE))
        x += step
    while y != ty:
        step = 1 if y < ty else -1
        edges.append((x + y * SIDE, x + (y + step) * SIDE))
        y += step
    return tuple(edges)


@dataclass(frozen=True)
class Packet:
    release: int
    path: tuple

    @property
    def source(self):
        return self.path[0][0]


def traffic(pattern, seed):
    rng = random.Random(seed)
    offered = []
    for burst in range(BURSTS):
        for source in range(NODES):
            for _ in range(BURST_SIZE):
                if pattern == "hotspot" and source != 5 and rng.random() < 0.5:
                    dest = 5
                elif pattern in ("uniform", "hotspot"):
                    dest = rng.randrange(NODES - 1)
                    dest += dest >= source
                else:
                    raise ValueError(pattern)
                offered.append(Packet(burst * PERIOD, route(source, dest)))
    return tuple(offered)


def trace_hash(offered):
    digest = sha256()
    for packet_id, packet in enumerate(offered):
        fields = (packet_id, packet.release, packet.source, packet.path[-1][1])
        digest.update(("%d,%d,%d,%d\n" % fields).encode("ascii"))
    return digest.hexdigest()


def simulate(offered, weights=None):
    """Return delivery cycle indexed by packet ID. None selects source FIFO."""
    if not offered:
        return ()
    releases = defaultdict(list)
    for packet_id, packet in enumerate(offered):
        releases[packet.release].append(packet_id)
    pending = [[] for _ in range(NODES)]
    queues = {edge: deque() for p in offered for edge in p.path}
    arrivals = [-1] * len(offered)
    delivered = 0
    last_cycle = max(releases) + sum(len(p.path) for p in offered)
    for cycle in range(last_cycle + 1):
        for packet_id in releases.get(cycle, ()):
            pending[offered[packet_id].source].append(packet_id)
        for candidates in pending:
            if not candidates:
                continue
            if weights is None:
                packet_id = candidates.pop(0)
            else:
                age, distance, depth = weights
                def score(pid):
                    p = offered[pid]
                    return (age * (cycle - p.release) + distance * len(p.path)
                            + depth * len(queues[p.path[0]]), -pid)

                packet_id = max(candidates, key=score)
                candidates.remove(packet_id)
            queues[offered[packet_id].path[0]].append((packet_id, 0))

        # All transfers read current queues before any next-hop arrivals are added.
        transfers = [q.popleft() for q in queues.values() if q]
        for packet_id, hop in sorted(transfers):
            next_hop = hop + 1
            path = offered[packet_id].path
            if next_hop < len(path):
                queues[path[next_hop]].append((packet_id, next_hop))
            else:
                assert arrivals[packet_id] == -1
                arrivals[packet_id] = cycle + 1
                delivered += 1
        if delivered == len(offered):
            assert all(not q for q in queues.values()) and all(not q for q in pending)
            assert all(t >= p.release + len(p.path) for t, p in zip(arrivals, offered))
            return tuple(arrivals)
    raise RuntimeError("Mesh failed to drain within the conservative hop bound")


def metrics(offered, arrivals):
    assert len(offered) == len(arrivals) and all(t > 0 for t in arrivals)
    delays = sorted(t - p.release for t, p in zip(arrivals, offered))
    return {
        "delivered": len(delays),
        "latency_sum": sum(delays),
        "p95": delays[math.ceil(len(delays) * 0.95) - 1],
        "last_arrival": max(arrivals),
    }
