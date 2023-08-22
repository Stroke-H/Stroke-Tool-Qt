from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import sys
from gui.mainWindow import *

from gui.mainWindow import MainWindow
main_window_x = MainWindow.window()
print(main_window_x)

# class ContentWidget(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.layout = QVBoxLayout(self)
#         self.label = QLabel('this is 1', self)
#         self.layout.addWidget(self.label)
#
#
# class TestWidget(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.hbox1 = QHBoxLayout()
#         self.hbox2 = QHBoxLayout()
#         self.hbox3 = QHBoxLayout()
#         self.hbox4 = QHBoxLayout()
#         self.vbox = QVBoxLayout()
#         self.vbox.addLayout(self.hbox1)
#         self.vbox.addLayout(self.hbox2)
#         self.vbox.addLayout(self.hbox3)
#         self.vbox.addLayout(self.hbox4)
#
#         # 第一个水平布局
#         self.data_label = QLabel('Data Label')
#         self.data_entry = QLineEdit(self)
#         self.test_btn = QPushButton('test', self)
#         self.test_btn.clicked.connect(self.test_btn_clicked)
#         self.hbox1.addWidget(self.data_label)
#         self.hbox1.addWidget(self.data_entry)
#         self.hbox1.addWidget(self.test_btn)
#
#         # 第二个水平布局
#         self.logTextEdit = QTextEdit()
#         self.logTextEdit.setReadOnly(True)
#         self.hbox2.addWidget(self.logTextEdit)
#         # self.vbox.setAlignment(self.label, Qt.AlignCenter)
#         self.setLayout(self.vbox)
#
#     def test_btn_clicked(self):
#         self.logTextEdit.append(self.data_entry.text())
#
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Content Switcher")
#         self.central_widget = QWidget()
#         self.setCentralWidget(self.central_widget)
#         self.setGeometry(0, 0, 750, 375)  # 设置窗口大小
#         self.stacked_widget = QStackedWidget(self)
#         self.menu_bar = self.menuBar()
#         self.status = self.statusBar()
#         other_menu = self.menu_bar.addMenu('IOS Function')
#         ios_action = QAction('IOS功能界面', self)
#         ios_action.triggered.connect(self.show_content_2)
#         other_menu.addAction(ios_action)
#
#         self.layout = QVBoxLayout(self.central_widget)
#         self.layout.addWidget(self.stacked_widget)
#
#         self.content_1 = ContentWidget()
#         self.content_2 = TestWidget()
#
#         self.stacked_widget.addWidget(self.content_1)
#         self.stacked_widget.addWidget(self.content_2)
#
#         self.setLayout(self.layout)
#
#     def show_content_1(self):
#         self.stacked_widget.setCurrentWidget(self.content_1)
#
#     def show_content_2(self):
#         self.stacked_widget.setCurrentWidget(self.content_2)
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     main_window = MainWindow()
#     main_window.show()
#     sys.exit(app.exec_())
