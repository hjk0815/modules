# coding=utf-8

import socket
import fcntl
import struct
import os
from IPy import IP

# 本地代理端口，你的和我不一定一样，按照自己的设置改动一下
PORT = 7897


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack(('256s').encode("utf-8"), (ifname[:15]).encode("utf-8"))
    )[20:24])


def get_windows_ip(wsl_ip):
    ip = IP(wsl_ip).make_net("20").strNormal()
    ip = ip.split('/')[0][:-1] + '1'
    return ip


def config_git_proxy(ip):
    config_str = (
        "git config --global https.proxy 'http://%s:%d'" % (ip, PORT))
    # print(config_str)
    ret = os.system(config_str)
    if ret:
        print("set git porxy fail")
        return
    else:
        config_str = (
            "git config --global http.proxy 'http://%s:%d'" % (ip, PORT))
        # print(config_str)
        ret = os.system(config_str)
    if ret:
        print("set git porxy fail")
        return
    else:
        print("set git porxy success")
        return


if __name__ == "__main__":
    wsl_ip = get_ip_address('eth0')
    print(wsl_ip)
    windows_ip = get_windows_ip(wsl_ip)
    print(windows_ip)
    # config_git_proxy(windows_ip)

