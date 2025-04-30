## Install
```bash
pip install -r requirements.txt
```

## Usage

Open a Debug Browser:
```bash
python main.py --task browser
```

Run Preparation Task:
```bash
python main.py --task prepare --year 2025
```

Run Detail Task:
```bash
python main.py --task detail --count 3
```


## Package
```bash
python3.11 -m build
twine upload dist/*
```

