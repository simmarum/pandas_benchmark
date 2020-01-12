import time
import sys
import random
import pandas as pd
from create_files import create_output_path


def load_data(l_path, l_format):
    if l_format in ['csv', 'csv.gz']:
        return pd.read_csv(l_path, header=0)
    elif l_format in ['snappy.parquet']:
        return pd.read_parquet(l_path)


def do_benchmark():
    for l_format in ['csv', 'csv.gz', 'snappy.parquet']:
        load_path = create_output_path()
        load_path = '{}{}'.format(load_path, l_format)

        df = load_data(load_path, l_format)
        print(load_path)


def main():
    do_benchmark()


if __name__ == '__main__':
    main()
