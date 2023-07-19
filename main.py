# # -*- coding:utf-8 -*-
#
# """
# @Author  :   StrokeH
# @env     :   Python 3.10.5
# @Time    :   2022/8/22 1:34 PM
# @Desc    :   安卓主界面入口
# """
#
from gui.mainWindow import *
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)  # 实例化窗口
#     bootstrap_window = MainWindow()  # 引导窗口展示
#     sys.exit(app.exec_())  # 遇到退出情况，终止程序
import os
import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QSplashScreen, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer


def show_splash_screen():
    app = QApplication([])
    splash_image_path = os.path.join(os.path.dirname(__file__), '1.png')
    splash_pixmap = QPixmap(splash_image_path).scaled(750, 375)
    splash_screen = QSplashScreen(splash_pixmap, Qt.WindowStaysOnTopHint)
    splash_screen.show()

    # 模拟应用程序加载的过程
    progress_label = QLabel(f"{AndroidFunc.get_day_soup()}", alignment=Qt.AlignBottom | Qt.AlignHCenter)
    font = progress_label.font()
    font.setPointSize(16)  # 设置字体大小
    font.setBold(True)  # 设置字体加粗
    progress_label.setFont(font)
    progress_label.setStyleSheet("color: white;")
    layout = QVBoxLayout()
    layout.addWidget(progress_label)
    splash_screen.setLayout(layout)

    # 模拟应用程序加载的时间
    timer = QTimer()
    timer.timeout.connect(app.quit)
    timer.start(3000)  # 3秒后关闭启动画面

    app.exec_()


if __name__ == '__main__':
    show_splash_screen()
    app = QApplication(sys.argv)  # 实例化窗口
    bootstrap_window = MainWindow()  # 引导窗口展示
    sys.exit(app.exec_())  # 遇到退出情况，终止程序
    # 启动应用程序的主要逻辑
