from gui.mainWindow import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os
import sys
import re

file_path = ''


# noinspection PyAttributeOutsideInit
class FileDropWidget(QWidget):
    def __init__(self):  # 初始化 继承父类QMainWindow
        super(FileDropWidget, self).__init__()
        index_x, index_y = AndroidFunc.get_desktop_size()
        self.setGeometry(int(index_x / 2) - 390, int(index_y / 2) - 175, 450, 400)  # 设置窗口大小
        # self.setMinimumSize(750, 400)
        # self.setGeometry(0, 0, 300, 200)  # 设置窗口大小
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.log_array = {}
        self.init_ui()

    def init_ui(self):
        # 创建布局

        layout = QVBoxLayout(self)

        # 创建文件拖拽区域
        self.drop_label = QLabel('请将包含剧集的文件夹拖放到这里', self)
        self.drop_label.setAlignment(Qt.AlignCenter)
        self.drop_label.setStyleSheet('border: 2px dashed #aaa; padding: 20px;')

        # 将文件拖拽区域添加到布局
        layout.addWidget(self.drop_label)

        # 设置文件拖拽区域接受拖拽事件
        self.setAcceptDrops(True)

        # 设置主窗口的布局
        self.setLayout(layout)

        # 设置主窗口的属性
        self.setWindowTitle('剧集命名检查')
        self.show()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        global file_path
        file_path = event.mimeData().urls()[0].toLocalFile()
        self.drama_chapter_info_received()
        # os.open(r'C:\Users\dell\result.txt')
        # os.startfile(file_path_2)

    def drama_chapter_info_received(self):
        non_mp4_files, missing_files = self.get_drama_info_check_result(file_path)
        self.show_message(non_mp4_files, missing_files)

    def show_message(self, non_mp4_files, missing_files):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)  # 设置消息图标类型
        need_show_data = f"""当前命名可能出错的文件有：{non_mp4_files}
当前文件可能出现的排序不正确或缺失的文件有：{missing_files}"""
        msg.setText(need_show_data)  # 弹窗的主要内容
        msg.setWindowTitle("信息")  # 弹窗标题
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)  # 设置按钮

        # 显示弹窗并捕获用户的按钮操作
        retval = msg.exec_()
        print("用户点击的按钮编号:", retval)

    @staticmethod
    def get_drama_info_check_result(folder_path):
        # 正则表达式，匹配"x.mp4"格式，其中x是阿拉伯数字
        mp4_pattern = re.compile(r'^(\d+)\.mp4$')
        mp4_files = []
        non_mp4_files = []

        # 遍历文件夹中的所有文件
        for filename in os.listdir(folder_path):
            match = mp4_pattern.match(filename)
            if match:
                # 提取x部分（数字），并转换为整数
                mp4_files.append(int(match.group(1)))
            else:
                # 标记不符合"x.mp4"格式的文件
                non_mp4_files.append(filename)

        # 对提取到的数字部分进行排序
        mp4_files.sort()

        # 检查是否有缺失的数字
        missing_files = []
        for i in range(mp4_files[0], mp4_files[-1] + 1):
            if i not in mp4_files:
                missing_files.append(f"{i}.mp4")

        return non_mp4_files, missing_files

    def closeEvent(self, event):
        # 重写关闭事件
        self.clear_file()
        event.accept()

    def clear_file(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)  # Instantiate the application object
    bootstrap_window = FileDropWidget()  # Show the main window
    bootstrap_window.show()
    sys.exit(app.exec_())  # Handle application exit
