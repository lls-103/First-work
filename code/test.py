# ---------- encoding：UTF-8 ------------
# author:liu     time:2021/3/4


from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from scapy.all import *
from scapy.layers.l2 import ARP, Ether
import threading

tip = ARP().psrc
tip = tip[:(len(tip) - tip[::-1].find('.'))]


class tools:
    def __init__(self):
        self.ui = uic.loadUi("ui/tools_mini.ui")
        self.ui.show()
        self.count = self.ui.tableWidget.rowCount()
        print(self.count)
        self.connector()

    def connector(self):
        self.ui.button.clicked.connect(self.arp_threading)

    def arp_scan(self, ip):

        pkt = ARP(pdst=ip)

        try:
            res = sr1(pkt, timeout=10, verbose=0)
            if res.psrc == ip:
                print('[+]' + res.psrc + ' ' + res.hwrsc)
        except:
            pass

    def arp_threading(self):
        print('IP          MAC')
        for i in range(1, 256):
            ip = tip + str(i)
            thread = threading.Thread(target=self.arp_scan, args=(ip,))
            thread.start()


if __name__ == '__main__':
    app = QApplication([])

    tool = tools()

    app.exec_()
