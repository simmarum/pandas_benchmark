# How to start
Navigate to `./releases` directory
- `mac/pandas_benchmark.app` for MAC
- `win/pandas_benchmark.exe` for Windows

# Develop

## Necessary file
Please create file `./cred.py` with content:
```
p = "password"
```

## Running
You must have `Python3` and `venv` package.
- `python3 -m venv ./v-env` to create v-env.
- `. ./v-env/bin/activate` to activate v-enn
- `pip isntall -r requirements.txt` to install dependencies
- `pyinstaller --clean -w -F pandas_benchmark.py` to create app file
    (Find app in **dist** dir)
- `python ./pandas_benchmark.py` to run benchmark with GUI
- `python ./pandas_benchmark.py nogui` to run benchmark without GUI
