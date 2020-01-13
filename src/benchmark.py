import time
import sys
import os
import random
import pandas as pd
import create_files as cf


def load_data(l_path):
    _, l_format = os.path.splitext(l_path)
    print(l_format)
    if l_format in ['.csv', '.gz']:
        return pd.read_csv(l_path, header=0)
    elif l_format in ['.parquet']:
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
        print(f)
        df = load_data(f)
        distinct_column(df, "str")
        self_join(df)


def distinct_column(df, col_pattern):
    cols = [col for col in df.columns if col_pattern in col]
    print("!", cols)
    x = pd.unique(df[cols].values.ravel())


def self_join(df):
    join_cols = random.choices(df.columns, k=2)
    cols_left = random.choices(df.columns, k=5)
    cols_left = list(set(cols_left+join_cols))
    cols_right = random.choices(df.columns, k=5)
    cols_right = list(set(cols_right+join_cols))
    print(cols_left)
    print(cols_right)
    print(join_cols)

    x = df.merge(df, how='inner', on=join_cols)


def main():
    check_files()
    do_benchmark()


if __name__ == '__main__':
    main()
