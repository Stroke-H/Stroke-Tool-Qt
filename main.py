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
import os
import sys
# import subprocess
from PyQt5.QtWidgets import QApplication, QSplashScreen, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer


def show_splash_screen():
    app = QApplication([])

    # Replace 'newsplash.gif' with the path to your video or GIF file
    splash_file_path = os.path.join(os.path.dirname(__file__), 'newsplash.gif')
    movie = QMovie(splash_file_path)

    # Optionally, you can add some label or progress text
    # progress_label = QLabel(f"{AndroidFunc.get_day_soup()}", alignment=Qt.AlignTop | Qt.AlignRight)
    # font = progress_label.font()
    # font.setPointSize(16)
    # font.setBold(True)
    # progress_label.setFont(font)
    # progress_label.setStyleSheet("color: white;")

    splash_label = QLabel(alignment=Qt.AlignCenter)
    splash_label.setMovie(movie)
    movie.start()

    layout = QVBoxLayout()
    # layout.addWidget(progress_label)
    layout.addWidget(splash_label)

    splash_widget = QWidget()
    splash_widget.setLayout(layout)

    # Create a transparent window without window frame
    splash_widget.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    splash_widget.setAttribute(Qt.WA_TranslucentBackground)
    # Simulate the application loading time
    timer = QTimer()
    timer.timeout.connect(app.quit)
    timer.start(5000)  # 5 seconds to close the splash screen

    splash_widget.show()
    app.exec_()


if __name__ == '__main__':
    show_splash_screen()
    app = QApplication(sys.argv)  # Instantiate the application
    bootstrap_window = MainWindow()  # Show the main window
    sys.exit(app.exec_())  # Handle application exit
