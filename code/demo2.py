# ---------- encoding：UTF-8 ------------
# author:liu     time:2021/3/4

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit, QMessageBox
from PyQt5.QtGui import QIcon

# 封装到类
class Stats():
    def __init__(self):
        self.window = QMainWindow()
        self.window.resize(500, 400)
        self.window.move(300, 300)
        self.window.setWindowTitle("薪资统计")

        self.textEdit = QPlainTextEdit(self.window)
        self.textEdit.setPlaceholderText("请输入薪资")
        self.textEdit.move(10, 25)
        self.textEdit.resize(300, 350)

        self.button = QPushButton('统计', self.window)
        self.button.move(380, 80)

        self.button.clicked.connect(self.handleCalc)

    def handleCalc(self):
        info = self.textEdit.toPlainText()  # 接收文本框内写入的数据

        salary_above_20k = ''
        salary_below_20k = ''
        for line in info.splitlines():
            if not line.strip():
                continue
            parts = line.split(' ')

            # 去掉列表中的空字符串内容
            parts = [p for p in parts if p]
            name, salary, age = parts
            if int(salary) >= 20000:
                salary_above_20k += name + '\n'
            else:
                salary_below_20k += name + '\n'

        QMessageBox.about(self.window, '统计结果', f"""薪资20000以上的有：\n{salary_above_20k}
        \n薪资20000以下的有：\n{salary_below_20k}""")


if __name__ == '__main__':

    app = QApplication([])

    # 加载Icon
    app.setWindowIcon(QIcon('picture/精灵球.png'))
    stats = Stats()
    stats.window.show()
    app.exec_()