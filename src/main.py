import subprocess
import psutil
import os
import time
from process_timer import ProcessTimer
from save_res import create_res_file_path, append_to_res_file


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


def main():
    do_ben()


if __name__ == '__main__':
    main()
