#!/usr/bin/python3


import shutil
import subprocess
import time
import os

from measure_thread import MeasureThread
from benchmark import Benchmark
from create_files import CreateFiles
from db import DB


class RunBenchmark():
    ver = 1

    def __init__(self):
        self.mt = MeasureThread()
        self.benchmark = Benchmark()
        self.cf = CreateFiles()
        self.db = DB()

    def run(self):
        print("###### BENCHMARK ######")
        self.mt.start()
        try:
            self.benchmark.run()
        finally:
            self.mt.stop()

    def rm_data(self):
        one_path = self.cf.get_file_paths()[0]
        shutil.rmtree(os.path.dirname(one_path), ignore_errors=True)
        print("Remove tmp data")


def main():
    run_benchmark = RunBenchmark()
    run_benchmark.rm_data()
    run_benchmark.run()
    avg_pt = run_benchmark.benchmark.calculate_results(
        run_benchmark.mt.time_elapsed,
        run_benchmark.mt.cpu_avg,
        run_benchmark.mt.mem_max,
    )
    run_benchmark.db.save_res_to_db(
        run_benchmark.ver,
        run_benchmark.mt.time_elapsed,
        run_benchmark.mt.cpu_avg,
        run_benchmark.mt.mem_max,
        avg_pt
    )
    res_stats = run_benchmark.db.get_statistic(
        run_benchmark.ver,
        run_benchmark.mt.time_elapsed,
        run_benchmark.mt.cpu_avg,
        run_benchmark.mt.mem_max,
        avg_pt
    )
    return res_stats


if __name__ == '__main__':
    main()
