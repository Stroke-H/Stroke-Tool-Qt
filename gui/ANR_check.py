from gui.mainWindow import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os
import zipfile
import sys

global_count = 0
file_path = ''


# noinspection PyAttributeOutsideInit
class FileDropWidget(QWidget):
    def __init__(self, parent=None):  # 初始化 继承父类QMainWindow
        super(FileDropWidget, self).__init__()
        self.parent = parent
        main_window_x = self.parent.parent_window.pos().x()
        main_window_y = self.parent.parent_window.pos().y()
        self.setGeometry(int(main_window_x) + 450, int(main_window_y) + 465, 300, 200)  # 设置窗口大小
        self.setWindowOpacity(0.9)  # 设置窗口透明度
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
        self.setWindowTitle('ANR日志快速筛查')
        self.show()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        global file_path
        file_path = event.mimeData().urls()[0].toLocalFile()
        self.find_and_read_bugreport_in_zip(file_path)
        if global_count:
            self.anr_detail_btn_clicked()
        # os.open(r'C:\Users\dell\result.txt')
        # os.startfile(file_path_2)

    def anr_detail_btn_clicked(self):
        self.anr_detail_panel = ScrollableLabel()
        logger.info('打开了ANR面板')

    def find_and_read_bugreport_in_zip(self, zip_path):
        global global_count
        if '.zip' in zip_path:
            count = 0
            data = 0
            start_arr = []
            end_arr = []
            with zipfile.ZipFile(zip_path, 'r') as myzip:
                for filename in myzip.namelist():
                    if 'bugreport' in filename.lower():
                        global_count = 1
                        data += 1
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
                                file_path_2 = os.path.join(os.path.expanduser("~"), f"result{anr}.txt")
                                info_path = os.path.join(os.path.expanduser("~"), f"anr_info{anr}.txt")
                                if os.path.exists(file_path_2):
                                    os.remove(file_path_2)
                                if os.path.exists(info_path):
                                    os.remove(info_path)
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
                                # 单独打印4分仅ANR内容的文件
                                with open(os.path.join(os.path.expanduser("~"), f"anr_info{anr}.txt"), "a",
                                          encoding='utf-8') as info_file:
                                    info_file.write(
                                        '=========================================================================================\n')
                                    info_file.write(f'This is ANR {anr + 1}\n')
                                    info_file.write(
                                        '=========================================================================================\n')
                                    for index in selected_values:
                                        info_file.write(index)
                                        info_file.write('\n')

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
            global_count = len(start_arr)
        else:
            return 0


# noinspection PyAttributeOutsideInit
class ScrollableLabel(QWidget):
    def __init__(self):
        super().__init__()
        self.anr_arr = []
        self.trace_arr = []
        self.showMaximized()
        self.setWindowTitle("ANR结果查看面板")
        self.hbox_1 = QHBoxLayout()
        self.hbox_2 = QHBoxLayout()
        self.hbox_3 = QHBoxLayout()
        self.hbox_4 = QHBoxLayout()
        self.hbox_5 = QHBoxLayout()
        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox_1)
        self.vbox.addLayout(self.hbox_2)
        self.vbox.addLayout(self.hbox_3)
        self.vbox.addLayout(self.hbox_4)
        self.vbox.addLayout(self.hbox_5)

        # 设置主窗口的布局
        self.setLayout(self.vbox)
        self.anr_select_combo_box = QComboBox(self)
        self.anr_select_combo_box.addItems(self.get_anr_count())
        self.anr_select_combo_box.setFixedSize(200, 20)

        self.trace_select_combo_box = QComboBox(self)
        self.trace_select_combo_box.addItems(self.get_trace())
        self.trace_select_combo_box.setFixedSize(200, 20)
        self.hbox_1.addWidget(self.anr_select_combo_box, alignment=Qt.AlignLeft)
        self.hbox_1.addWidget(self.trace_select_combo_box, alignment=Qt.AlignLeft)

        self.show_detail_btn = QPushButton('查看详细记录', self)
        self.hbox_2.addWidget(self.show_detail_btn, alignment=Qt.AlignLeft)

        anr_title = QLabel('ANR显示区域', self)
        title_font = QFont()
        title_font.setPointSize(20)  # 设置字体大小为20
        anr_title.setFont(title_font)
        trace_title = QLabel('Trace显示区域', self)
        trace_title.setFont(title_font)
        self.hbox_3.addWidget(anr_title, alignment=Qt.AlignCenter)
        self.hbox_3.addWidget(trace_title, alignment=Qt.AlignCenter)

        # 创建anr滚动区域和标签
        anr_scroll_area = QScrollArea(self)
        self.anr_label = QLabel('', self)
        content_font = QFont()
        content_font.setPointSize(10)  # 设置字体大小为20
        self.anr_label.setTextInteractionFlags(self.anr_label.textInteractionFlags() | Qt.TextSelectableByMouse)
        # 将标签设置为滚动区域的小部件
        anr_scroll_area.setWidget(self.anr_label)
        # 设置滚动区域的属性
        anr_scroll_area.setWidgetResizable(True)
        # 设置垂直滚动条
        anr_scroll_area.setVerticalScrollBarPolicy(1)  # Qt.ScrollBarAsNeeded
        # file_path = r'C:\Users\dell\anr_info0.txt'  # 替换成你的文件路径
        # content = self.read_file(file_path)
        # self.anr_label.setText(content)
        self.anr_label.setFont(content_font)

        # 创建trace滚动区域和标签
        trace_scroll_area = QScrollArea(self)
        self.trace_label = QLabel('', self)
        self.trace_label.setTextInteractionFlags(self.trace_label.textInteractionFlags() | Qt.TextSelectableByMouse)
        # 将标签设置为滚动区域的小部件
        trace_scroll_area.setWidget(self.trace_label)
        # 设置滚动区域的属性
        trace_scroll_area.setWidgetResizable(True)
        # 设置垂直滚动条
        trace_scroll_area.setVerticalScrollBarPolicy(1)  # Qt.ScrollBarAsNeeded
        # file_path = r'C:\Users\dell\anr_info0.txt'  # 替换成你的文件路径
        # content = self.read_file(file_path)
        # trace_label.setText(content)
        self.trace_label.setFont(content_font)

        self.test_btn = QPushButton('预留btn', self)
        self.log_export_btn = QPushButton('导出日志', self)
        self.hbox_5.addWidget(self.test_btn, alignment=Qt.AlignLeft)
        self.hbox_5.addWidget(self.log_export_btn, alignment=Qt.AlignRight)

        # 将两个滚动区域添加到布局
        self.hbox_4.addWidget(anr_scroll_area)
        self.hbox_4.addWidget(trace_scroll_area)
        self.on_listen()
        self.show()

    @staticmethod
    def read_file(file_path):
        try:
            # 使用 QFile 读取文件内容
            file = QFile(file_path)
            if file.open(QFile.ReadOnly | QFile.Text):
                stream = QTextStream(file)
                content = stream.readAll()
                file.close()
                return content
        except Exception as e:
            print(f"发生错误: {e}")
        return "无法读取文件内容"

    @staticmethod
    def read_part_file(file_path):
        try:
            # 使用 QFile 读取文件内容
            file = QFile(file_path)
            if file.open(QFile.ReadOnly | QFile.Text):
                stream = QTextStream(file)
                content = stream.read(20000)
                file.close()
                return content
        except Exception as e:
            print(f"发生错误: {e}")
        return "无法读取文件内容"

    def anr_change(self):
        self.anr_index = self.get_index_value(self.anr_select_combo_box)
        anr_path = os.path.join(os.path.expanduser("~"), f"{self.anr_index}.txt")  # 替换成你的文件路径
        content = self.read_file(anr_path)
        self.anr_label.setText(content)
        return self.anr_index

    def trace_change(self):
        self.trace_index = self.get_index_value(self.trace_select_combo_box)
        trace_path = os.path.join(os.path.expanduser("~"), f"{self.trace_index}.txt")
        content = self.read_part_file(trace_path)
        self.trace_label.setText(content)
        return self.trace_index

    @staticmethod
    def get_index_value(combo_box):
        index = combo_box.currentIndex()
        value = combo_box.itemText(index)
        return value

    def get_anr_count(self):
        for i in range(0, global_count):
            self.anr_arr.append("anr_info" + str(i))
        return self.anr_arr

    def get_trace(self):
        with zipfile.ZipFile(file_path, 'r') as myzip:
            for filename in myzip.namelist():
                if 'anr' in filename.lower():
                    trace_name = filename.split('/')[-1]
                    self.trace_arr.append(trace_name)
                    with myzip.open(filename) as file:
                        content = file.readlines()
                        with open(os.path.join(os.path.expanduser("~"), f"{trace_name}.txt"), "a",
                                  encoding='utf-8') as result_file:
                            for index in content:
                                index_data = index.decode('utf-8')
                                result_file.write(index_data)
            return self.trace_arr

    def show_detail_btn_clicked(self):
        what_to_show = self.anr_select_combo_box.currentIndex()
        file_path = os.path.join(os.path.expanduser("~"), f"result{what_to_show}.txt")
        # os.open(fr'C:\Users\dell\result{what_to_show}.txt')
        os.startfile(file_path)

    def log_export_btn_clicked(self):
        pass

    def on_listen(self):
        self.anr_select_combo_box.currentIndexChanged.connect(self.anr_change)
        self.trace_select_combo_box.currentIndexChanged.connect(self.trace_change)
        self.show_detail_btn.clicked.connect(self.show_detail_btn_clicked)

    def closeEvent(self, event):
        # 重写关闭事件
        self.clear_file()
        event.accept()

    def clear_file(self):
        # 在关闭窗口时执行的函数
        data = self.trace_arr
        anr_data = self.anr_arr
        for trace_name in data:
            trace_path = os.path.join(os.path.expanduser("~"), f"{trace_name}.txt ")
            os.remove(trace_path)
        for anr_name in anr_data:
            anr_path = os.path.join(os.path.expanduser("~"), f"{anr_name}.txt")
            anr_path2 = os.path.join(os.path.expanduser("~"), f"result{anr_data.index(anr_name)}.txt")
            os.remove(anr_path)
            os.remove(anr_path2)


if __name__ == '__main__':
    pass
