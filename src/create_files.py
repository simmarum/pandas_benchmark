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


def produce_amount_keys(amount_of_keys):
    def gen_keys(_urandom=os.urandom, _encode=base64.b32encode, _randint=np.random.randint):
        while True:
            _randint(20)
            yield _encode(_urandom(20))[:20].decode('ascii')
    return list(islice(unique_everseen(gen_keys()), amount_of_keys))


def create_output_path():
    save_path = os.path.join(
        os.path.dirname(__file__),
        'data',
        'tmp.'
    )
    return save_path


def create_file():
    string_chars = string.ascii_lowercase + string.ascii_uppercase
    date_format = "%Y-%m-%d %H:%M:%S"
    stime = time.mktime(time.strptime("2018-01-01 00:00:00", date_format))
    etime = time.mktime(time.strptime("2020-01-01 00:00:00", date_format))

    val_v = 1_000
    val_s = 250_000
    val_w = 10
    etime = stime + val_v
    gen_p = produce_amount_keys(val_v)
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
    save_path = create_output_path()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    df.to_csv(save_path+"csv", index=False)
    print("Save file 1")
    df.to_csv(save_path+"csv.gz", index=False)
    print("Save file 2")
    df.to_parquet(save_path+"snappy.parquet", index=False)
    print("Save file 3")

    return save_path


def main():
    create_file()


if __name__ == '__main__':
    main()
