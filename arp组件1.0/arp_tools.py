# ---------- encoding：UTF-8 ------------
# author:liu     time:2021/3/9

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from test_arp_scan import ARP_Scan
from test_arp_attack import ARP_Attack
from test_QMainWindow import MainWindow


class parentWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.main_ui = MainWindow()

class scan(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.child = ARP_Scan()

class attack(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.child = ARP_Attack()

if __name__ == '__main__':
    app = QApplication([])

    window = parentWindow()
    child_1 = scan()
    child_2 = attack()


