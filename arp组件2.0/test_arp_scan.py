# ---------- encoding：UTF-8 ------------
# author:liu     time:2021/3/9

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from scapy.all import *
from scapy.layers.l2 import ARP, Ether
import random

num = ARP().psrc
num = num[:(len(num) - num[::-1].find('.'))]
print(num)


# 第一类线程为全局扫描
class myFirst_Thread(QThread):
    s1 = pyqtSignal(tuple)

    def __init__(self, num=None):
        super(myFirst_Thread, self).__init__()
        self.flag = True
        self.num = num

    def run(self):
        # print('2')
        print(self.flag)
        if self.num == 0:
            for i in range(1, 255):  # 26
                self.num = i
                print(self.num)
                if self.flag == False:
                    self.s1.emit((self.num, self.num))
                    break
                ip = num + str(i)
                a = arp_scan(ip)
                if a is None:
                    continue
                else:
                    self.s1.emit(a)
            self.s1.emit((0, 1))
        else:
            for i in range(self.num, 255):  # 26
                self.num = i
                if self.flag == False:
                    self.s1.emit((self.num, self.num))
                    break
                ip = num + str(i)
                a = arp_scan(ip)
                if a is None:
                    continue
                else:
                    self.s1.emit(a)
            self.s1.emit((0, 1))

    def stop(self):
        self.flag = False


# 第二类线程为单一扫描
class mySecond_Thread(QThread):
    s2 = pyqtSignal(tuple)

    def __init__(self, ip):
        super(mySecond_Thread, self).__init__()
        self.ip = ip

    def run(self):
        # print('2222')
        a = arp_scan(self.ip)
        if a is not None:
            self.s2.emit(a)
        else:
            self.s2.emit((0, 0))
        # self.s2.emit((0, 1))


# arp扫描程序
def arp_scan(ip):
    # print('3')
    # print('3333')
    eth = Ether(dst="FF:FF:FF:FF:FF:FF")
    pkt = eth / ARP(pdst=ip)
    try:
        ans = srp1(pkt, timeout=1, verbose=0)
        # ans = srp1(pkt, verbose=0)
        if ans:
            message = (ip, ans.hwsrc)
            return message
        else:
            return None
    except Exception as e:
        print(e)


class ARP_Scan(QDialog):
    stop_singnal = pyqtSignal(bool)

    def __init__(self):
        super(ARP_Scan, self).__init__()
        self.ini_UI()
        self.count = self.ui_scan.tableWidget.rowCount()
        self.flag = True
        self.num = 0

    def ini_UI(self):
        self.ui_scan = uic.loadUi('arp_scan.ui', self)  # 注意最后这个self，没有它不会显示这个页面
        self.ui_scan.setWindowTitle('arp扫描')
        self.ui_scan.setWindowIcon(QIcon('../picture/放大镜.png'))
        # self.ui_scan.lineEdit.setText("arp扫描窗口")
        # self.ui_scan.lineE = self.ui_scan.lineEdit.text()
        self.connector()

    def connector(self):
        self.ui_scan.button.clicked.connect(lambda: self.arp_threadOrarp_alone(self.ui_scan.lineEdit.text()))
        self.ui_scan.buttonCE.clicked.connect(self.clear_all)
        self.ui_scan.buttonSave.clicked.connect(self.date_save)
        self.ui_scan.buttonStop.clicked.connect(self.startOrstop)

    # 创建线程去执行扫描任务
    def arp_threadOrarp_alone(self, text):
        if text == '':
            # print('11111111')
            self.myThread1 = myFirst_Thread(0)  # 创建线程
            self.myThread1.s1.connect(self.arp_all)
            self.myThread1.start()  # 执行run函数
        else:
            # print('11111')
            self.myThread2 = mySecond_Thread(text)
            self.myThread2.s2.connect(self.arp_alone)
            self.myThread2.start()

    def arp_all(self, message):
        # print('4')
        # print('44444')
        # print(message)
        ip, mac = message
        print(ip, mac)
        try:
            if ip == 0 and mac == 1:
                self.ui_scan.lineEdit_2.setText('[***]扫描完成[***]')
                # QMessageBox.about(self, "扫描完成")
            elif ip == mac:
                self.num = ip
                print('hahahaha')
                print(self.num)
            else:
                self.ui_scan.lineEdit_2.setText('[***]正在扫描[***]')
                self.insert_data(ip, mac)
        except Exception as e:
            print(e)

    def arp_alone(self, message):
        ip, mac = message
        # try:
        if ip == 0 and mac == 0:
            self.ui_scan.lineEdit_2.setText('[***]this host is not alive[***]')
            # QMessageBox.about(self, 'this host is not alive!!!')
        else:
            self.insert_data(ip, mac)
            self.ui_scan.lineEdit_2.setText('[***]扫描完成[***]')
            # QMessageBox.about(self, "扫描完成")

        # except Exception as e:
        #     print(e)

    def startOrstop(self):
        if self.flag == True:
            self.stop_singnal.connect(self.myThread1.stop)
            self.stop_singnal.emit(False)
            self.flag = False
            self.myThread1.exit()
        else:
            self.myThread1 = myFirst_Thread(self.num)
            self.myThread1.s1.connect(self.arp_all)
            self.myThread1.start()
            self.flag = True

    def clear_all(self):
        self.ui_scan.lineEdit.clear()
        self.ui_scan.lineEdit_2.clear()

        # self.ui.tableWidget.clear()

        # 清空表格
        self.ui_scan.tableWidget.clearContents()
        self.ui_scan.tableWidget.setRowCount(0)
        self.count = 0

    # 保存数据
    def date_save(self):
        text = ''
        for i in range(self.count):
            text += self.ui_scan.tableWidget.item(i, 0).text() + ' + '
            text += self.ui_scan.tableWidget.item(i, 1).text() + '\n'

        file_name = generate_file_name()
        try:
            with open(file_name, 'w') as f:
                f.write(text)
        except:
            pass
        self.ui_scan.lineEdit_2.setText("[*]保存完毕[*]")

    # 插入数据
    def insert_data(self, ip, mac):

        self.ui_scan.tableWidget.insertRow(int(self.count))
        self.ui_scan.tableWidget.setItem(self.count, 0, QTableWidgetItem(str(ip)))
        self.ui_scan.tableWidget.setItem(self.count, 1, QTableWidgetItem(str(mac)))
        self.count += 1


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

    arp_scan = ARP_Scan()

    app.exec_()
