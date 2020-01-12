import time
import sys
import os
import random
import pandas as pd
import create_files as cf


def load_data(l_path):
    _, l_format = os.path.splitext(l_path)
    if l_format in ['csv', 'csv.gz']:
        return pd.read_csv(l_path, header=0)
    elif l_format in ['snappy.parquet']:
        return pd.read_parquet(l_path)


def list_files():
    load_path = cf.create_output_path()
    return ['{}{}'.format(load_path, l_format)
            for l_format in ['csv', 'csv.gz', 'snappy.parquet']
            ]


def check_files():
    found = True
    for f in list_files():
        found &= os.path.exists(f)
    if not found:
        cf.main()


def do_benchmark():
    for f in list_files():
        df = load_data(f)
        print(f)


def main():
    check_files()
    do_benchmark()


if __name__ == '__main__':
    main()
