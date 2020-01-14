import time
import sys
import os
import random
import pandas as pd
import create_files as cf


def load_data(l_path):
    _, l_format = os.path.splitext(l_path)
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
    for idx, f in enumerate(list_files()):
        print("Package of tests: {}".format(idx))
        df = load_data(f)
        distinct_column(1, df, "str")
        self_join(2, df)
        distinct_column(3, df, "int")
        self_join_2(4, df)
        distinct_column(6, df, "date")
        stats(7, df)


def distinct_column(idx, df, col_pattern):
    cols = [col for col in df.columns if col_pattern in col]
    x = pd.unique(df[cols].values.ravel())
    print("Test {} done".format(idx))


def self_join(idx, df):
    join_cols = random.choices(df.columns, k=2)
    cols_left = random.choices(df.columns, k=5)
    cols_left = list(set(cols_left+join_cols))
    cols_right = random.choices(df.columns, k=5)
    cols_right = list(set(cols_right+join_cols))

    x = df.merge(df, how='inner', on=join_cols)
    print("Test {} done".format(idx))


def self_join_2(idx, df):
    join_cols = random.choices(df.columns, k=3)
    cols_left = random.choices(df.columns, k=5)
    cols_left = list(set(cols_left+join_cols))
    cols_right = random.choices(df.columns, k=5)
    cols_right = list(set(cols_right+join_cols))

    x = df.merge(df, how='outer', on=join_cols)
    print("Test {} done".format(idx))


def stats(idx, df):
    cols = [c for c in df.columns if "int" in c]
    df2 = df[cols[0:4]]
    x = 0
    for index, row in df2.iterrows():
        for e in row:
            x += e
            if x > 1_000_000:
                x -= 2 * 1_000_000
        if index > 50_000:
            break
    print("Test {} done".format(idx))


def main():
    check_files()
    do_benchmark()


if __name__ == '__main__':
    main()
