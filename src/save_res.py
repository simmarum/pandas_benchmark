import time
import os
import benchmark


def create_res_file_path():
    tmp_name = int(time.time())
    res_path = os.path.join(
        os.path.dirname(__file__),
        'res',
        '{}.tsv'.format(tmp_name)
    )
    os.makedirs(os.path.dirname(res_path), exist_ok=True)
    with open(res_path, "w") as myfile:
        tmp_row = [
            "tid",
            "time",
            "cpu",
            "memory",
            "avg_pt"
        ]
        myfile.write('\t'.join(tmp_row))
        myfile.write('\n')
    return res_path, tmp_name


def append_to_res_file(res_path, tid, ptimer):
    n_time, n_cpu, n_mem, avg_pt = benchmark.calculate_results(ptimer)

    with open(res_path, "a") as myfile:
        tmp_row = [
            "{0:d}".format(tid),
            "{0:d}".format(n_time),
            "{0:d}".format(n_cpu),
            "{0:d}".format(n_mem),
            "{0:d}".format(avg_pt),
        ]
        myfile.write('\t'.join(tmp_row))
        myfile.write('\n')
