import os
import shutil
import subprocess
import time

import benchmark
import create_files as cf
from database import db
from process_timer import ProcessTimer
from save_res import append_to_res_file, create_res_file_path


def get_benchmark_file_path():
    file_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            'benchmark.py',
        ))
    return file_path


def do_ben():
    print("###### BENCHMARK ######")
    res_file_path, tid = create_res_file_path()
    b_file_path = get_benchmark_file_path()
    ptimer = ProcessTimer(['python3', b_file_path])
    tmp_data = []
    try:
        ptimer.execute()
        # poll as often as possible; otherwise the subprocess might
        # "sneak" in some extra memory usage while you aren't looking
        while ptimer.poll():
            time.sleep(0.2)
    finally:
        # make sure that we don't leave the process dangling?
        ptimer.close()
        append_to_res_file(res_file_path, tid, ptimer)
    return ptimer


def rm_data():
    load_path = cf.create_output_path()
    shutil.rmtree(os.path.dirname(load_path), ignore_errors=True)
    print("Remove tmp data")


def main():
    rm_data()
    ptimer = do_ben()

    n_time, n_cpu, n_mem, avg_pt = benchmark.calculate_results(ptimer)
    db.save_res_to_db(n_time, n_cpu, n_mem, avg_pt)
    res_stat = db.get_statistic(n_time, n_cpu, n_mem, avg_pt)
    print(res_stat)
    return res_stat


if __name__ == '__main__':
    main()
