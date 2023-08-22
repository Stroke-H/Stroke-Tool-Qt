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


# noinspection PyAttributeOutsideInit
class InitWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.index_window = self
        index_x, index_y = AndroidFunc.get_desktop_size()
        self.setGeometry(int(index_x / 2) - 390, int(index_y / 2) - 175, 750, 400)  # 设置窗口大小
        self.setMinimumSize(750, 400)
        self.setWindowTitle("Stroke Tool 4.2.1")
        url = 'https://img95.699pic.com/xsj/1r/9r/g0.jpg%21/fw/700/watermark/url/L3hzai93YXRlcl9kZXRhaWwyLnBuZw/align/southeast'
        response = requests.get(url)
        pixmap = QPixmap()
        pixmap.loadFromData(response.content)
        icon = QIcon(pixmap)
        self.setWindowIcon(icon)
        # self.setWindowIcon(QIcon(QPixmap(r'C:\Users\dell\PycharmProjects\pyqtProject\image\icon_new.ico')))
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.menu_bar = self.menuBar()
        # self.status = self.statusBar()
        # self.source_type = 'both'
        self.ui_init()
        self.is_show = True

    def ui_init(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        window_menu = self.menu_bar.addMenu('Window Select')
        android_action = QAction('安卓功能界面', self)
        android_action.triggered.connect(self.android_panel_btn_clicked)
        window_menu.addAction(android_action)

        ios_action = QAction('IOS功能界面', self)
        ios_action.triggered.connect(self.ios_panel_btn_clicked)
        window_menu.addAction(ios_action)

        # self.file_menu = self.menu_bar.addMenu('Options')
        # backup_action = QAction('信息备份', self)
        # info_select_action = QAction('仅显示tool源', self)
        # account_action = QAction('显示提现账号', self)
        #
        # self.file_menu.addAction(backup_action)
        # self.file_menu.addAction(info_select_action)
        # self.file_menu.addAction(account_action)

        self.android_window = MainWindow(self.index_window)
        self.ios_window = IosWindow(self.index_window)

        self.stacked_widget = QStackedWidget(self)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.stacked_widget)

        self.stacked_widget.addWidget(self.android_window)
        self.stacked_widget.addWidget(self.ios_window)

        self.setLayout(self.layout)

    def android_panel_btn_clicked(self):
        self.stacked_widget.setCurrentWidget(self.android_window)
        # self.file_menu.setEnabled(True)

    def ios_panel_btn_clicked(self):
        self.stacked_widget.setCurrentWidget(self.ios_window)
        if self.is_show:
            AndroidFunc.get_file_path()
            self.is_show = False


if __name__ == '__main__':
    # show_splash_screen()
    app = QApplication(sys.argv)  # Instantiate the application
    bootstrap_window = InitWindow()  # Show the main window
    bootstrap_window.show()
    sys.exit(app.exec_())  # Handle application exit
