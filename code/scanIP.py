# ---------- encoding：UTF-8 ------------
# author:liu     time:2021/3/5
"""
本程序目的：实现局域网下扫描存活主机和端口
"""
from scapy.all import *
from scapy.layers.l2 import ARP


def arp_scan(ip):
    p = ARP(pdst=ip)
    ans = sr1(p, timeout=1)
    if ans != None:
        ans.display()
        print(ip, "host is up.")
        box.append(ip)
    else:
        print(ip, "host id down....")


if __name__ == '__main__':

    begin = "10.12.11."
    box = []
    for i in range(1, 255):
        ip = begin
        ip += str(i)
        print("当前扫描的ip地址：", ip)
        arp_scan(ip)

    print("存活的主机有：\n", box)
