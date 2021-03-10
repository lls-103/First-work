# ---------- encoding：UTF-8 ------------
# author:liu     time:2021/3/9

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from test_arp_attack import ARP_Attack
from test_arp_scan import ARP_Scan


# 实验
# class child(QDialog):
#     def __init__(self):
#         super(child,self).__init__()
#         self.ui = uic.loadUi('arp_scan.ui',self)

# 创建主界面
class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        self.ui = uic.loadUi('arp_mainwindow.ui')
        self.ui.setWindowIcon(QIcon("../picture/精灵球.png"))
        self.ui.setWindowTitle("网络小工具1.0")
        self.ui.show()

        self.ui.stats = self.ui.statusBar()

        self.ui.stats.showMessage("欢迎使用网络小工具",5000)
        self.connector()

    def connector(self):
        self.ui.buttonScan.clicked.connect(self.on_buttonScan_clicked)
        self.ui.buttonAttack.clicked.connect(self.on_buttonAttack_clicked)

    def on_buttonScan_clicked(self):
        self.ui.hide()
        self.arp_scan = ARP_Scan()
        self.arp_scan.exec_()
        self.ui.show()

    def on_buttonAttack_clicked(self):
        self.ui.hide()
        self.arp_attack = ARP_Attack()
        self.arp_attack.exec_()
        self.ui.show()


if __name__ == '__main__':
    app = QApplication([])

    first_window = MainWindow()

    app.exec_()
