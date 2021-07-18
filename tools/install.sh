#!/bin/bash
LANG=zh_CN.UTF-8

echo -E "
______     _                      ______       _   
| ___ \   (_)                     | ___ \     | |  
| |_/ /_ _ _ _ __ ___   ___  _ __ | |_/ / ___ | |_ 
|  __/ _\` | | '_ \` _ \ / _ \| '_ \| ___ \/ _ \| __|
| | | (_| | | | | | | | (_) | | | | |_/ / (_) | |_ 
\_|  \__,_|_|_| |_| |_|\___/|_| |_\____/ \___/ \__|
"

set -e

test_python() {
  {
    python3 -V
  } || {
    echo 1
    return 1
  }
}

test_pip() {
  {
    pip -V
  } || {
    echo 1
    return 1
  }
}

test_git() {
  {
    git --version
  } || {
    echo 1
    return 1
  }
}

if [[ $(test_python) == 1 ]]; then
  echo "未检测到Python，将安装Python"
  sudo apt install python3
  sudo apt install python3-pip
  echo "Python安装成功"
else
  python_version=$(test_python | cut -b 8-)
  echo "找到Python，Python版本：$python_version"
fi
if [[ $(test_pip) == 1 ]]; then
  echo "未检测到pip，将安装pip"
  sudo apt install python3-pip
  echo "pip安装成功"
else
  pip_version=$(test_pip | cut -b 5-11)
  echo "找到pip，pip版本：$pip_version"
fi

if [[ $(test_git) == 1 ]]; then
  echo "未检测到git，将安装git"
  sudo apt install git
  echo "git安装成功"
else
  git_version=$(test_git | cut -b 13-)
  echo "找到git，git版本：$git_version"
fi

#echo "从Github克隆PaimonBot"
#git clone https://hub.fastgit.org/MingxuanGame/PaimonBot_Continuation.git bot

echo "补全Python包"
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r bot/requirements.txt

echo "开始运行安装脚本（Python）"
python3 bot/tools/install.py
