# ---------- encoding：UTF-8 ------------
# author:liu     time:2021/3/5

from PyQt5.QtWidgets import QHBoxLayout, QApplication, QMainWindow, QPushButton, QWidget
from PyQt5.QtGui import QIcon


class FirstMainWin(QMainWindow):
    def __init__(self):
        super(FirstMainWin, self).__init__()

        # 设置主窗口的标题
        self.setWindowTitle("第一个主窗口应用")

        # 设置窗口的尺寸
        self.resize(400, 300)

        # 状态栏
        self.status = self.statusBar()
        self.status.showMessage('只存在5秒的消息', 5000)
        self.button1 = QPushButton('退出应用程序')
        self.button1.clicked.connect(self.onClick_Button)

        # 创建水平布局
        layout = QHBoxLayout()
        layout.addWidget(self.button1)

        mainFrame = QWidget()
        mainFrame.setLayout(layout)

        self.setCentralWidget(mainFrame)

    def onClick_Button(self):
        sender = self.sender()
        print(sender.text() + '按钮被按下')
        app = QApplication.instance()
        app.quit()


if __name__ == '__main__':
    app = QApplication([])

    app.setWindowIcon(QIcon('picture/精灵球.ico'))
    w = FirstMainWin()

    w.show()
    app.exec_()
