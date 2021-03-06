# ---------- encoding：UTF-8 ------------
# author:liu     time:2021/3/4

from PyQt5.QtWidgets import QApplication,QMainWindow,QPushButton,QPlainTextEdit,QMessageBox

# 信号与槽
def handleCalc():
    # print("统计按钮被点击了")

    info = textEdit.toPlainText()   # 接收文本框内写入的数据

    salary_above_20k = ''
    salary_below_20k = ''
    for line in info.splitlines():
        if not line.strip():
            continue
        parts = line.split(' ')

        # 去掉列表中的空字符串内容
        parts = [p for p in parts if p]
        name,salary,age = parts
        if int(salary) >= 20000:
            salary_above_20k +=name +'\n'
        else:
            salary_below_20k +=name+'\n'


    QMessageBox.about(w,'统计结果',f"""薪资20000以上的有：\n{salary_above_20k}
\n薪资20000以下的有：\n{salary_below_20k}""")



if __name__ == '__main__':

    app = QApplication([])

    w = QMainWindow()
    w.resize(500,400)
    w.move(300,310)
    w.setWindowTitle("薪资统计")

    textEdit = QPlainTextEdit(w)
    textEdit.setPlaceholderText("请输入薪资表")
    textEdit.move(10,25)
    textEdit.resize(300,350)

    button = QPushButton("统计",w)
    button.move(380,80)
    button.clicked.connect(handleCalc)

    w.show()

    app.exec_()