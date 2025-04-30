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


```
# MacOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \ --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-debug

# Windows
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\tmp\chrome-debug"
```

地址栏输入 showmetheparts.com, 然后人工完成验证码

安装 qte-parts-crawler-cli
```aiignore
pip install qte-parts-crawler==0.1.2
qte-parts-crawler-cli 
```
