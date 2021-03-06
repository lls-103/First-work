# ---------- encoding：UTF-8 ------------
# author:liu     time:2021/3/5

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

class Cal:

    def __init__(self):
        self.ui = uic.loadUi('ui/cal.ui')
        self.connecter()

    def num_1(self):
        self.ui.lineEdit.insert('1')

    def num_2(self):
        self.ui.lineEdit.insert('2')

    def num_3(self):
        self.ui.lineEdit.insert('3')

    def num_4(self):
        self.ui.lineEdit.insert('4')

    def num_5(self):
        self.ui.lineEdit.insert('5')

    def num_6(self):
        self.ui.lineEdit.insert('6')

    def num_7(self):
        self.ui.lineEdit.insert('7')

    def num_8(self):
        self.ui.lineEdit.insert('8')

    def num_9(self):
        self.ui.lineEdit.insert('9')

    def num_0(self):
        self.ui.lineEdit.insert('0')

    def num_dian(self):
        self.ui.lineEdit.insert('.')

    def num_plus(self):
        self.ui.lineEdit.insert('+')

    def num_sub(self):
        self.ui.lineEdit.insert('-')

    def num_mul(self):
        self.ui.lineEdit.insert('*')

    def num_divide(self):
        self.ui.lineEdit.insert('/')

    def num_CE(self):
        self.ui.lineEdit.clear()

    def connecter(self):

        self.ui.button1.clicked.connect(self.num_1)
        self.ui.button2.clicked.connect(self.num_2)
        self.ui.button3.clicked.connect(self.num_3)
        self.ui.button4.clicked.connect(self.num_4)
        self.ui.button5.clicked.connect(self.num_5)
        self.ui.button6.clicked.connect(self.num_6)
        self.ui.button7.clicked.connect(self.num_7)
        self.ui.button8.clicked.connect(self.num_8)
        self.ui.button9.clicked.connect(self.num_9)
        self.ui.button0.clicked.connect(self.num_0)
        self.ui.buttondian.clicked.connect(self.num_dian)
        self.ui.buttonadd.clicked.connect(self.num_plus)
        self.ui.buttonsub.clicked.connect(self.num_sub)
        self.ui.buttonmul.clicked.connect(self.num_mul)
        self.ui.buttondivide.clicked.connect(self.num_divide)
        self.ui.buttonCE.clicked.connect(self.num_CE)
        self.ui.buttonCal.clicked.connect(self.calcu)

    def calcu(self):

        text = self.ui.lineEdit.text()

        try:
            result = eval(text)
            self.ui.lineEdit.setText(str(eval(text)))
        except:
            self.ui.lineEdit.setText('invalid syntax, check your input!')


if __name__ == '__main__':

    app = QApplication([])

    ca = Cal()
    ca.ui.show()

    app.exec_()







