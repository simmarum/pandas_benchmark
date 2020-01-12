import time
import os


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
        ]
        myfile.write('\t'.join(tmp_row))
        myfile.write('\n')
    return res_path, tmp_name


def append_to_res_file(res_path, tid, ptimer):
    n_time = ptimer.t1 - ptimer.t0
    n_cpu = sum(ptimer.cpu_percent_list)/len(ptimer.cpu_percent_list)
    n_mem = max(ptimer.rss_memory_list)

    with open(res_path, "a") as myfile:
        tmp_row = [
            "{0:d}".format(tid),
            "{0:.2f}".format(n_time),
            "{0:.2f}".format(n_cpu),
            "{0:d}".format(n_mem),
        ]
        myfile.write('\t'.join(tmp_row))
        myfile.write('\n')
