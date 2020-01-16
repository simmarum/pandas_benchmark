import random
import os
import pandas as pd
from create_files import CreateFiles
import create_files as cf


class Benchmark():
    def __init__(self):
        self.cf = CreateFiles()

    def _load_data(self, l_path):
        _, l_format = os.path.splitext(l_path)
        if l_format in ['.csv', '.gz']:
            return pd.read_csv(l_path, header=0)
        elif l_format in ['.parquet']:
            return pd.read_parquet(l_path)

    def _check_files(self):
        found = True
        for f in self.cf.get_file_paths():
            found &= os.path.exists(f)
        if not found:
            self.cf.create_file()

    def run(self):
        self._check_files()
        for idx, f in enumerate(self.cf.get_file_paths()):
            print("Package of tests: {}".format(idx+1))
            df = self._load_data(f)
            # self._distinct_column(1, df, "str")
            # self._self_join(2, df)
            # self._distinct_column(3, df, "int")
            # self._self_join_2(4, df)
            # self._distinct_column(6, df, "date")
            self._stats(7, df)

    def _distinct_column(self, idx, df, col_pattern):
        cols = [col for col in df.columns if col_pattern in col]
        x = pd.unique(df[cols].values.ravel())
        print("Test {} done".format(idx))

    def _self_join(self, idx, df):
        join_cols = random.choices(df.columns, k=2)
        cols_left = random.choices(df.columns, k=5)
        cols_left = list(set(cols_left+join_cols))
        cols_right = random.choices(df.columns, k=5)
        cols_right = list(set(cols_right+join_cols))

        x = df.merge(df, how='inner', on=join_cols)
        print("Test {} done".format(idx))

    def _self_join_2(self, idx, df):
        join_cols = random.choices(df.columns, k=3)
        cols_left = random.choices(df.columns, k=5)
        cols_left = list(set(cols_left+join_cols))
        cols_right = random.choices(df.columns, k=5)
        cols_right = list(set(cols_right+join_cols))

        x = df.merge(df, how='outer', on=join_cols)
        print("Test {} done".format(idx))

    def _stats(self, idx, df):
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

    def calculate_results(self, rtime, rcpu, rmem):
        avg_pt = int((
            0.6*(100 * 80000 / rtime) +
            0.2*(100 * 25 / rcpu) +
            0.2*(100 * 560000000 / rmem)
        )*100)

        return avg_pt
