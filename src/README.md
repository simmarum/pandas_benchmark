Short descriptions for developer

# Necessary file
Please create file `database/cred.py` with content:
```
p = "password"
```

# Develop on MACOS
You must have `Python3` and `venv` package.

`bash ./mac_create_v-env.sh` to create v-env.

`. ./v-env/bin/activate` to activate v-en.

`pyinstaller --clean -w -F pandas_benchmark.py` to create app file for MAC.
    (Find app in **dist** dir)

`python ./pandas_benchmark.py` to run benchmark with GUI

`python ./pandas_benchmark.py nogui` to run benchmark without GUI
