import base64
import os
import random
import string
import time
from datetime import datetime
from itertools import islice

import numpy as np
import pandas as pd
from more_itertools import unique_everseen

import sys
import os


class CreateFiles():
    f_formats = [
        "csv",
        "csv.gz"
    ]
    f_name = "tmp"

    def __init__(self):
        if getattr(sys, 'frozen', False):
            application_path = sys._MEIPASS
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))
        self.save_path = os.path.join(
            application_path,
            'data'
        )

    def _produce_amount_keys(self, amount_of_keys):
        def gen_keys(_urandom=os.urandom, _encode=base64.b32encode, _randint=np.random.randint):
            while True:
                _randint(20)
                yield _encode(_urandom(20))[:20].decode('ascii')
        return list(islice(unique_everseen(gen_keys()), amount_of_keys))

    def get_file_paths(self):
        file_paths = [
            os.path.join(self.save_path, self.f_name+"."+f_format)
            for f_format in self.f_formats
        ]
        return file_paths

    def create_file(self):
        val_v = 10_000
        val_s = 300_000
        val_w = 10
        gen_p = self._produce_amount_keys(val_v)
        gen_date = random.sample(range(1515751437, 1578823437), val_v)
        tmp_header = [
            ['int_{}'.format(i),
             'str_{}'.format(i+1),
             'date_{}'.format(i+2)
             ] for i in range(0, val_w*3, 3)
        ]
        tmp_header = [item for sublist in tmp_header for item in sublist]

        tmp_data = []
        for i in range(val_s):
            tmp_row = []
            for j in range(val_w):
                tmp_row.extend(
                    [
                        random.randint(100, 99+val_v),
                        random.choice(gen_p),
                        datetime.utcfromtimestamp(
                            random.choice(gen_date))
                    ]
                )
            tmp_data.append(tmp_row)

        df = pd.DataFrame(tmp_data, columns=tmp_header)
        print("Create tmp dataset")

        file_paths = self.get_file_paths()
        os.makedirs(os.path.dirname(file_paths[0]), exist_ok=True)

        df.to_csv(file_paths[0], index=False)
        print("Save file 1")
        df.to_csv(file_paths[1], index=False)
        print("Save file 2")

        return file_paths
