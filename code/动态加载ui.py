# ---------- encoding：UTF-8 ------------
# author:liu     time:2021/3/4

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox


class Stats():

    def __init__(self):
        # 从文件中加载ui定义
        self.ui = uic.loadUi("ui/stats.ui")
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui.button.clicked.connect(self.handleCalc)

    def handleCalc(self):
        info = self.ui.textEdit.toPlainText()  # 接收文本框内写入的数据

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

        QMessageBox.about(self.ui, '统计结果', f"""薪资20000以上的有：\n{salary_above_20k}
        \n薪资20000以下的有：\n{salary_below_20k}""")


if __name__ == '__main__':
    app = QApplication([])

    stats = Stats()
    stats.ui.show()
    app.exec_()
