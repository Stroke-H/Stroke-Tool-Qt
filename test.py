from utils.AndroidFunc import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QToolTip
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tooltip Example")

        # 创建一个主窗口布局
        layout = QVBoxLayout()

        # 创建一个 QLineEdit 控件
        self.line_edit = QLineEdit()
        self.line_edit.textChanged.connect(self.show_tooltip)  # 绑定 textChanged 信号

        # 将 QLineEdit 添加到布局中
        layout.addWidget(self.line_edit)

        # 创建一个空白的 QWidget 作为主窗口的中心部件
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def show_tooltip(self):
        text = self.line_edit.text()
        if text:
            code, dic = AndroidFunc.get_code_and_des()
            # 根据 QLineEdit 的值设置不同的提示文本
            if int(text) in code:
                tooltip_text = dic[int(text)]
                self.line_edit.setToolTip(tooltip_text)
                QToolTip.showText(self.line_edit.mapToGlobal(self.line_edit.rect().bottomLeft()), tooltip_text)
            else:
                pass


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()