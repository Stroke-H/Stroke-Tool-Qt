from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os
import zipfile
import sys


# noinspection PyAttributeOutsideInit
class FileDropWidget(QWidget):
    def __init__(self):  # 初始化 继承父类QMainWindow
        super(FileDropWidget, self).__init__()
        self.log_array = {}
        self.init_ui()

    def init_ui(self):
        # 创建布局
        layout = QVBoxLayout(self)

        # 创建文件拖拽区域
        self.drop_label = QLabel('拖放文件到这里', self)
        self.drop_label.setAlignment(Qt.AlignCenter)
        self.drop_label.setStyleSheet('border: 2px dashed #aaa; padding: 20px;')

        # 将文件拖拽区域添加到布局
        layout.addWidget(self.drop_label)

        # 设置文件拖拽区域接受拖拽事件
        self.setAcceptDrops(True)

        # 设置主窗口的布局
        self.setLayout(layout)

        # 设置主窗口的属性
        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle('ANR日志快速筛查')
        self.show()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        file_path = event.mimeData().urls()[0].toLocalFile()
        data = self.find_and_read_bugreport_in_zip(file_path)
        if data:
            for i in range(0, data):
                file_path_2 = os.path.join(os.path.expanduser("~"), f"result{i}.txt")
                if os.path.exists(file_path_2):
                    os.remove(file_path_2)
                self.find_and_read_bugreport_in_zip(file_path)
                # os.open(r'C:\Users\dell\result.txt')
                os.startfile(file_path_2)

    def find_and_read_bugreport_in_zip(self, zip_path):
        if '.zip' in zip_path:
            count = 0
            start_arr = []
            end_arr = []
            with zipfile.ZipFile(zip_path, 'r') as myzip:
                for filename in myzip.namelist():
                    if 'bugreport' in filename.lower():
                        count += 1
                        # 打开文件并读取内容
                        with myzip.open(filename) as file:
                            content = file.readlines()
                            for index in content:
                                index_data = index.decode('utf-8').strip()
                                self.log_array.update({count: index.decode('utf-8').strip()})
                                count += 1
                                if "ANR in" in index_data:
                                    start_index = count
                                    start_arr.append(start_index)
                                if "Completed ANR of" in index_data:
                                    end_index = count
                                    end_arr.append(end_index)
                            keys = list(self.log_array.keys())
                            for anr in range(0, len(start_arr)):
                                # 打印 ANR前1000行信息
                                if start_arr[anr] > 1000:
                                    selected_keys = keys[start_arr[anr] - 1003:start_arr[anr] - 2]
                                    selected_values = [self.log_array[key] for key in selected_keys]
                                else:
                                    selected_keys = keys[0:start_arr[anr] - 2]
                                    selected_values = [self.log_array[key] for key in selected_keys]
                                with open(os.path.join(os.path.expanduser("~"), f"result{anr}.txt"), "a",
                                          encoding='utf-8') as result_file:
                                    result_file.write(
                                        '=========================================================================================\n')
                                    result_file.write(f'This is the First 1000 Rows of ANR{anr + 1} Data\n')
                                    result_file.write(
                                        '=========================================================================================\n')
                                    for index in selected_values:
                                        result_file.write(index)
                                        result_file.write('\n')
                                # 打印中间ANR数据
                                selected_keys = keys[start_arr[anr] - 2:end_arr[anr] - 1]
                                selected_values = [self.log_array[key] for key in selected_keys]
                                with open(os.path.join(os.path.expanduser("~"), f"result{anr}.txt"), "a",
                                          encoding='utf-8') as result_file:
                                    result_file.write(
                                        '=========================================================================================\n')
                                    result_file.write(f'This is ANR {anr + 1}\n')
                                    result_file.write(
                                        '=========================================================================================\n')
                                    for index in selected_values:
                                        result_file.write(index)
                                        result_file.write('\n')
                                # 打印ANR后1000行数据
                                if len(self.log_array) - end_arr[anr] > 999:
                                    selected_keys = keys[end_arr[anr] - 2:end_arr[anr] + 998]
                                    selected_values = [self.log_array[key] for key in selected_keys]
                                else:
                                    selected_keys = keys[end_arr[anr] - 2:len(self.log_array) - 1]
                                    selected_values = [self.log_array[key] for key in selected_keys]
                                with open(os.path.join(os.path.expanduser("~"), f"result{anr}.txt"), "a",
                                          encoding='utf-8') as result_file:
                                    result_file.write(
                                        '=========================================================================================\n')
                                    result_file.write(f'This is the 1000 Rows of Data After ANR{anr + 1}\n')
                                    result_file.write(
                                        '=========================================================================================\n')
                                    for index in selected_values:
                                        result_file.write(index)
                                        result_file.write('\n')
            return len(start_arr)
        else:
            return 0


if __name__ == '__main__':
    app = QApplication(sys.argv)
    fileDropWidget = FileDropWidget()
    sys.exit(app.exec_())
