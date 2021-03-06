# ---------- encoding：UTF-8 ------------
# author:liu     time:2021/3/6
from scapy.all import *
from scapy.layers.l2 import ARP, Ether
import threading

tip = ARP().psrc
tip = tip[:(len(tip) - tip[::-1].find('.'))]


def ScanIp(ip):
    pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)
    ARP.display()
    try:
        res = srp1(pkt, timeout=10, verbose=0)
        if res.psrc == ip:
            print('[+]' + res.psrc + ' ' + res.hwsrc)
    except:
        pass


if __name__ == '__main__':
    print(tip)
    print('IP     MAC')
    for i in range(1, 256):
        ip = tip + str(i)
        Go = threading.Thread(target=ScanIp, args=(ip,))
        Go.start()
