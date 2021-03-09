# ---------- encoding：UTF-8 ------------
# author:liu     time:2021/3/8

"""
arp扫描
使用QTread多线程
可以保存数据
"""
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, pyqtSignal
from scapy.all import *
from scapy.layers.l2 import ARP, Ether
import time
import random

num = ARP().psrc
num = num[:(len(num) - num[::-1].find('.'))]

print(num)


class myThread(QThread):
    s = pyqtSignal(tuple)

    def __init__(self):
        super(myThread, self).__init__()
        self.flag = 1

    def run(self):

        for i in range(1, 255):
            ip = num + str(i)
            a = arp_scan(ip)
            if a is None:
                continue
            else:
                self.s.emit(a)  # 发射信号


# arp扫描程序
def arp_scan(ip):
    eth = Ether(dst="FF:FF:FF:FF:FF:FF")
    pkt = eth / ARP(pdst=ip)
    try:
        ans = srp1(pkt, timeout=1, verbose=0)
        if ans:
            message = (ip, ans.hwsrc)
            return message
        else:
            return
    except Exception as e:
        print(e)


class Tools(QMainWindow):
    def __init__(self):
        super(Tools, self).__init__()

        self.ui = uic.loadUi("../ui/tools_3.ui")
        self.ui.setWindowTitle("arp扫描小工具")
        self.ui.setWindowIcon(QIcon('../picture/精灵球.png'))
        self.connector()
        self.ui.show()
        self.count = self.ui.tableWidget.rowCount()
        # self.lock = threading.RLock()

        # 初始化状态栏
        self.ui.status = self.ui.statusBar()

    def connector(self):
        self.ui.button.clicked.connect(self.arp_thread)
        self.ui.buttonCE.clicked.connect(self.clear_all)
        self.ui.buttonSave.clicked.connect(self.date_save)

    def arp_thread(self):
        self.myThread = myThread()  # 创建线程
        self.myThread.s.connect(self.arp_start)
        self.myThread.start()  # 执行run函数
        self.ui.status.showMessage('[*]正在进行ARP扫描[*]')

    def arp_start(self, message):
        # print('444444')
        ip, mac = message
        # tip = self.ui.lineEdit.text()
        self.ui.tableWidget.insertRow(int(self.count))
        self.ui.tableWidget.setItem(self.count, 0, QTableWidgetItem(str(ip)))
        self.ui.tableWidget.setItem(self.count, 1, QTableWidgetItem(str(mac)))
        self.count += 1
        # QApplication.processEvents()

        if self.myThread.isRunning() == 0:
            self.ui.status.showMessage('[*]扫描完成[*]')

    def clear_all(self):
        self.ui.lineEdit.clear()
        # self.ui.tableWidget.clear()

        # 清空表格
        self.ui.tableWidget.clearContents()
        self.ui.tableWidget.setRowCount(0)
        self.count = 0

    def date_save(self):
        # self.ui.lineEdit.setText(self.count)
        text = ''
        # text += self.ui.tableWidget.item(0, 0).text()

        for i in range(self.count):
            text += self.ui.tableWidget.item(i, 0).text() + ' + '
            text += self.ui.tableWidget.item(i, 1).text() + '\n'

        file_name = generate_file_name()
        try:
            with open(file_name, 'w') as f:
                f.write(text)
        except:
            pass
        self.ui.status.showMessage("[*]保存完毕[*]", 5000)


# 随机生成文件名。txt
def generate_file_name():
    file_name = ''
    txt = '1234567890abcdefghijklmnopqrstABCDEFGHIJKLMNOPQRST'
    s = random.sample(txt, 3)
    for each in s:
        file_name += each
    return file_name + '.txt'


if __name__ == '__main__':
    app = QApplication([])

    tool = Tools()

    app.exec_()
