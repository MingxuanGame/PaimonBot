import json
import os
import platform

import requests
import yaml


def get_version():
    release = json.loads(requests.get("https://api.github.com/repos/Mrs4s/go-cqhttp/releases").text)[0]
    assets = json.loads(requests.get(release["assets_url"]).text)
    download_url = []
    for asset in assets:
        download_url.append(asset["browser_download_url"])
    return download_url


def get_os():
    def get_os_id():
        os_info = platform.version()
        if "Ubuntu" in os_info:
            return "Ubuntu"
        elif "Centos" in os_info:
            return "Centos"
        elif "Debian" in os_info:
            return "Debian"
        elif "Deepin" in os_info:
            return "Deepin"
        elif "Red Hat" in os_info:
            return "RedHat"
        elif "10.0" in os_info or "6.2" in os_info or "6.3" in os_info or "6.1" in os_info:
            return "Windows"
        else:
            return "Others"

    def get_machine_id():
        if platform.machine().lower() == "x86_64" or platform.machine().lower() == "amd64" or platform.machine().lower() == "x64":
            return "amd64"
        elif platform.machine().lower() == "x86" or platform.machine().lower() == "i686" or platform.machine().lower() == "i386":
            return "386"
        elif platform.machine().lower() == "arm":
            return "arm"
        elif platform.machine().lower() == "arm64":
            return "arm64"
        elif platform.machine().lower() == "armv7":
            return "armv7"
        else:
            return None

    return {
        "machine": get_machine_id(),
        "os": get_os_id()
    }


def get_suffix(os_id):
    if os_id == "Ubuntu" or os_id == "Debian" or os_id == "Deepin":
        return ".deb"
    elif os_id == "RedHat" or os_id == "Centos":
        return ".rpm"
    elif os_id == "Windows":
        return ".exe"
    else:
        return ".tar.gz"


def get_download_url(download_url_list):
    system = get_os()
    for download_url in download_url_list:
        if system["machine"] in download_url and get_suffix(system["os"]) in download_url:
            return download_url.replace("github.com", "download.fastgit.org")


def set_config(qq, password, port=9898):
    go_cqhttp_config = {
        'account': {
            'uin': qq,
            'password': password,
            'encrypt': False,
            'status': 0,
            'relogin': {
                'delay': 3,
                'interval': 3,
                'max-times': 0
            },
            'use-sso-address': True
        },
        'heartbeat': {
            'interval': 5
        },
        'message': {
            'post-format': 'string',
            'ignore-invalid-cqcode': False,
            'force-fragment': False,
            'fix-url': False,
            'proxy-rewrite': '',
            'report-self-message': False,
            'remove-reply-at': False,
            'extra-reply-data': False
        },
        'output': {
            'log-level': 'warn',
            'debug': False
        },
        'default-middlewares': {
            'access-token': '',
            'filter': '',
            'rate-limit': {
                'enabled': False,
                'frequency': 1,
                'bucket': 1
            }
        },
        'database': {
            'leveldb': {
                'enable': True
            }
        },
        'servers': [
            {
                'ws-reverse': {
                    'universal': f'ws://127.0.0.1:{port}/cqhttp/ws',
                    'reconnect-interval': 3000,
                    'middlewares': {
                        'access-token': '',
                        'filter': '',
                        'rate-limit': {
                            'enabled': False,
                            'frequency': 1,
                            'bucket': 1
                        }
                    }
                }
            }
        ]
    }

    nonebot_config_dev = f"""
HOST="127.0.0.1"
PORT={port}
DEBUG=true

SUPERUSERS=[""]  # 配置 NoneBot 超级用户
# NICKNAME=["awesome", "bot"]  # 配置机器人的昵称
COMMAND_START=["/", ""]  # 配置命令起始字符
# COMMAND_SEP=["."]  # 配置命令分割字符
    """

    nonebot_config_prod = f"""
HOST="127.0.0.1"
PORT={port}
SECRET=
ACCESS_TOKEN=
    """

    with open("go-cqhttp/config.yml", "w", encoding="utf-8") as f:
        f.write(yaml.dump(go_cqhttp_config))
    with open("bot/.env.dev", "w", encoding="utf-8") as f:
        f.write(nonebot_config_dev)
    with open("bot/.env.prod", "w", encoding="utf-8") as f:
        f.write(nonebot_config_prod)


def main():
    if not os.path.exists("go-cqhttp"):
        os.mkdir("go-cqhttp")
    url = get_download_url(get_version())
    print(f"下载go-cqhttp{get_suffix(get_os()['os'])}中")
    with open(f"go-cqhttp/go-cqhttp{get_suffix(get_os()['os'])}", "wb") as f:
        f.write(requests.get(url).content)

    print("开始安装go-cqhttp")
    os.system(f'sudo dpkg -i \"go-cqhttp/go-cqhttp{get_suffix(get_os()["os"])}\"')

    while True:
        try:
            qq = int(input("请输入你的QQ >>> "))
            break
        except ValueError:
            print("输入无效，请重试")
    password = input("请输入你的QQ密码 >>> ")
    try:
        port = int(input("请输入开启的端口号（不填默认9898） >>> "))
    except ValueError:
        pass

    try:
        set_config(qq, password, port)
    except NameError:
        set_config(qq, password)


if __name__ == '__main__':
    main()
