# ---------- encoding：UTF-8 ------------
# author:liu     time:2021/3/6

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem,
from scapy.all import *
from scapy.layers.l2 import ARP, Ether
import threading
import time


class Tools:
    def __init__(self):
        self.ui = uic.loadUi("ui/tools_mini.ui")
        self.connector()
        self.ui.show()
        self.count = self.ui.tableWidget.rowCount()
        self.lock = threading.RLock()
        # print(self.count)
        # self.ui.tableWidget.setRowCount(0)
        # self.ip = ARP().psrc
        # print(self.ip[:(len(self.ip) - self.ip[::-1].find('.'))])

    def connector(self):
        self.ui.button.clicked.connect(self.arp_scan_all)
        self.ui.buttonCE.clicked.connect(self.clear_all)

    def arp_scan(self, ip):
        # text = self.ui.lineEdit.text()
        # ip = self.ui.lineEdit.text()
        eth = Ether(dst="FF:FF:FF:FF:FF:FF")
        pkt = eth / ARP(pdst=ip)
        # self.lock.acquire()
        # result = ans.getlayer(ARP).fields.get('hwsrc')

        try:
            ans = srp1(pkt, timeout=10, verbose=0)
            if ans.psrc == ip:
                # 先确认有数据需要添加，在插入新行
                self.ui.tableWidget.insertRow(int(self.count))
                # self.ui.textEdit.setPlainText("%s ----> %s" % (ip, result))
                # print(ip, ans.hwsrc)
                self.ui.tableWidget.setItem(self.count, 0, QTableWidgetItem(ip))
                self.ui.tableWidget.setItem(self.count, 1, QTableWidgetItem(ans.hwsrc))
                self.count += 1
                print(self.count)

        except:
            pass
        # finally:
            # self.lock.release()
        self.ui.lineEdit.clear()

    def arp_scan_all(self):
        tip = self.ui.lineEdit.text()
        for i in range(1, 256):
            ip = tip + str(i)
            Go = threading.Thread(target=self.arp_scan, args=(ip,))
            Go.start()

    def clear_all(self):
        self.ui.lineEdit.clear()
        # self.ui.textEdit.clear()


if __name__ == '__main__':
    app = QApplication([])

    tool = Tools()

    app.exec_()
