import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from gui.dialog import *
from utils.AndroidFunc import *
from gui.mainWindow import *


# noinspection PyAttributeOutsideInit
class DelAccountWindow(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        main_window_x = parent.pos().x()
        main_window_y = parent.pos().y()
        self.setGeometry(int(main_window_x) + 755, int(main_window_y) + 135, 400, 70)  # 设置窗口大小
        self.setWindowTitle("Monkey 测试面板")
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.parent.open_window_list.append('MonkeyWindow')
        self.notice = Notice()
        self.init_ui()
        self.onclick_listen()