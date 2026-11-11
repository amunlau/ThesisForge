import unittest
from pathlib import Path
from unittest.mock import patch

from analyze import read_rows, summarize
from experiment import csv_bytes, run
from mesh import Packet, metrics, route, simulate


def packet(release, source, dest):
    return Packet(release, route(source, dest))


class MeshTests(unittest.TestCase):
    def test_xy_order_and_zero_queue_delay(self):
        self.assertEqual(route(9, 3), ((9, 10), (10, 11), (11, 7), (7, 3)))
        self.assertEqual(simulate([packet(5, 9, 3)]), (9,))

    def test_independent_opposing_links(self):
        self.assertEqual(simulate([packet(0, 1, 0), packet(0, 0, 1)]), (1, 1))

    def test_source_port_limit_and_exhaustive_drain(self):
        trace = [packet(0, 0, 1)] * 3
        times = simulate(trace)
        self.assertEqual(times, (1, 2, 3))
        self.assertEqual(metrics(trace, times), dict(delivered=3, latency_sum=6, p95=3, last_arrival=3))

    def test_ingress_and_transit_contend_for_one_directed_link(self):
        self.assertEqual(simulate([packet(0, 0, 2), packet(1, 1, 2)]), (2, 3))

    def test_policy_reorders_source_burst(self):
        trace = [packet(0, 0, 1), packet(0, 0, 3)]
        self.assertEqual(simulate(trace), (1, 4))
        self.assertEqual(simulate(trace, (1, 1, 0)), (2, 3))

    def test_replay_both_searches_and_all_test_runs(self):
        archived = Path(__file__).parent / "results"
        for name, rows in run().items():
            self.assertEqual(csv_bytes(rows), (archived / name).read_bytes())
        self.assertEqual(summarize(archived), (archived / "summary.csv").read_text(encoding="utf-8"))

    def test_impossible_latency_records_are_rejected_before_analysis(self):
        archived = Path(__file__).parent / "results"
        for name, column, value in (("paired.csv", "latency_sum", "-1"),
                                    ("paired.csv", "latency_sum", "999999999"),
                                    ("search.csv", "train_latency_sum", "0")):
            def damaged(path):
                rows = read_rows(path)
                if path.name == name:
                    rows[0][column] = value
                return rows

            with self.subTest(name=name, column=column, value=value), \
                    patch("analyze.read_rows", side_effect=damaged), self.assertRaises(ValueError):
                summarize(archived)


if __name__ == "__main__":
    unittest.main()
