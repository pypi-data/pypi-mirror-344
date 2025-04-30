## Usage

1. 使用命令行启动 Chrome 浏览器，开启远程调试模式
```bash
# MacOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \ --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-debug

# Windows
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\tmp\chrome-debug"
```

2. 在Chrome浏览器地址栏输入 https://www.showmetheparts.com, 然后人工完成验证码

3. 安装Python(如果已经安装了Python 3.11，可以跳过此步骤)

```bash
# MacOS
brew install python@3.11
python3.11 -m pip install --upgrade pip

# Windows
winget install python --version 3.11
python3.11 -m pip install --upgrade pip
```

4. 安装 qte-parts-crawler
```bash
pip3 install qte-parts-crawler==0.1.3
```
5. 使用 qte-parts-crawler-cli
```bash

```


## Install
```bash
pip install -r requirements.txt
```

## Package & Publish
```bash
python3.11 -m build
twine upload dist/*
```
