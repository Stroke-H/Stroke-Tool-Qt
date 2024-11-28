from gui.mainWindow import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os
import sys
import re
import langid
from collections import Counter

file_path = ''
err_file = ''


# noinspection PyAttributeOutsideInit
class DramaWidget(QWidget):
    def __init__(self):  # 初始化 继承父类QMainWindow
        super().__init__()
        index_x, index_y = AndroidFunc.get_desktop_size()
        self.setGeometry(int(index_x / 2) - 390, int(index_y / 2) - 175, 450, 400)  # 设置窗口大小
        # self.setMinimumSize(750, 400)
        # self.setGeometry(0, 0, 300, 200)  # 设置窗口大小
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        try:
            url = 'https://img95.699pic.com/xsj/1r/9r/g0.jpg%21/fw/700/watermark/url/L3hzai93YXRlcl9kZXRhaWwyLnBuZw/align/southeast'
            response = requests.get(url)
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            icon = QIcon(pixmap)
            self.setWindowIcon(icon)
        except BaseException as error:
            print(error)
        self.log_array = {}
        # self.time_pattern = r"^00:0\d(:\d{2})?(\,\d{3})?$"
        # self.time_pattern = r"^00:0\d(:\d{2})?([.,]\d{3})?$"
        self.time_pattern = r'^00:0[0-6](:\d{2})?([.,]\d{3})?$'
        self.pinyin_name_pattern = r"^([bpmfdtnlgkhjqxrzcsyw]?[aeiouüv]{1,2}(ng?|n)?)+$"
        self.country_code_arr = []
        self.subtitle_arr = []
        self.most_code_arr = []
        self.init_ui()

    def init_ui(self):
        # 创建布局

        layout = QVBoxLayout(self)

        # 创建文件拖拽区域
        self.drop_label = QLabel('请将包含剧集或字幕文件的文件夹拖放到这里', self)
        self.drop_label.setAlignment(Qt.AlignCenter)
        self.drop_label.setStyleSheet('border: 2px dashed #aaa; padding: 20px;')

        # 将文件拖拽区域添加到布局
        layout.addWidget(self.drop_label)

        # 设置文件拖拽区域接受拖拽事件
        self.setAcceptDrops(True)

        # 设置主窗口的布局
        self.setLayout(layout)

        # 设置主窗口的属性
        self.setWindowTitle('剧集命名/字幕时间检查')
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
        if non_mp4_files == 'vtt' or non_mp4_files == 'srt':
            global err_file
            err_file = missing_files
            self.anr_detail_panel = ScrollableLabel()
            logger.info('打开了ANR面板')
            # self.subtitle_message(missing_files)
        else:
            self.drama_message(non_mp4_files, missing_files)

    def drama_message(self, non_mp4_files, missing_files):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)  # 设置消息图标类型
        need_show_data = f"""当前命名可能出错的文件有：{non_mp4_files}
当前文件可能出现的排序不正确或缺失的文件有：{missing_files}"""
        msg.setText(need_show_data)  # 弹窗的主要内容
        msg.setWindowTitle("信息")  # 弹窗标题
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)  # 设置按钮
        # 显示弹窗并捕获用户的按钮操作
        ok_button = msg.button(QMessageBox.Ok)
        ok_button.clicked.connect(lambda: self.copy_text(need_show_data))

        retval = msg.exec_()
        print("用户点击的按钮编号:", retval)

    def subtitle_message(self, missing_files):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)  # 设置消息图标类型
        msg.setText(missing_files)  # 弹窗的主要内容
        msg.setWindowTitle("信息")  # 弹窗标题
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)  # 设置按钮
        # 获取确定按钮并连接到复制函数
        ok_button = msg.button(QMessageBox.Ok)
        ok_button.clicked.connect(lambda: self.copy_text(missing_files))

        retval = msg.exec_()

    @staticmethod
    def copy_text(text):
        """将文本复制到剪贴板"""
        clipboard = QApplication.clipboard()
        clipboard.setText(text)

    def get_drama_info_check_result(self, folder_path):
        # 正则表达式，匹配"x.mp4"格式，其中x是阿拉伯数字
        try:
            data = os.listdir(folder_path)
            print(data[0], data[-1])
            mp4_pattern = re.compile(r'^(\d+)\.mp4$')
            vtt_pattern = re.compile(r'^.*\.vtt$')
            srt_pattern = re.compile(r'^.*\.srt$')
            if mp4_pattern.match(data[0]) or mp4_pattern.match(data[-1]):
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
            elif vtt_pattern.match(data[0]) or vtt_pattern.match(data[-1]):
                time_arr = []
                err_format = []
                for filename in os.listdir(folder_path):
                    if vtt_pattern.match(filename):
                        pass
                    else:
                        err_format.append(filename)
                    with open(fr"{folder_path}\{filename}", 'r', encoding='utf-8') as file:
                        lines = file.readlines()
                    # 跳过文件开头的WEBVTT声明行
                    for line in lines[1:]:
                        line = line.strip()
                        if '-->' in line:
                            # 这是时间戳行
                            start_time, end_time = line.split(' --> ')
                            if re.match(self.time_pattern, start_time):
                                pass
                            else:
                                time_arr.append(f'{filename}---->{start_time}')
                            if re.match(self.time_pattern, end_time):
                                pass
                            else:
                                time_arr.append(f'{filename}---->{end_time}')
                if err_format:
                    format_data = f'''可能出错的文件格式为：
{err_format}
    '''
                else:
                    format_data = ''
                need_show_info = f'''{format_data}
可能出错的时间戳：
{time_arr}
    '''
                # 当前语言统计最多的语种为:{most_code}
                # 以下是可能翻译错误的语种记录:
                # {error_country_code_arr}
                return "vtt", time_arr
            elif srt_pattern.match(data[0]) or srt_pattern.match(data[-1]):
                time_arr = []
                err_format = []
                for filename in os.listdir(folder_path):
                    if srt_pattern.match(filename):
                        pass
                    else:
                        err_format.append(filename)
                    with open(fr"{folder_path}\{filename}", 'r', encoding='utf-8') as file:
                        lines = file.readlines()
                    # 跳过文件开头的WEBVTT声明行
                    for line in lines[1:]:
                        line = line.strip()
                        if '-->' in line:
                            # 这是时间戳行
                            start_time, end_time = line.split(' --> ')
                            if re.match(self.time_pattern, start_time):
                                pass
                            else:
                                time_arr.append(f'{filename}---->{start_time}')
                            if re.match(self.time_pattern, end_time):
                                pass
                            else:
                                time_arr.append(f'{filename}---->{end_time}')
                if err_format:
                    format_data = f'''可能出错的文件格式为：
{err_format}
                '''
                else:
                    format_data = ''
                need_show_info = f'''{format_data}
可能出错的时间戳：
{time_arr}
                    '''
                # 当前语言统计最多的语种为:{most_code}
                # 以下是可能翻译错误的语种记录:
                # {error_country_code_arr}
                return "srt", time_arr
            else:
                return "vtt", '文件夹内文件非MP4或vtt文件,请检查文件后重新尝试'
        except BaseException as error:
            if '目录' in str(error):
                return "vtt", '您放入的不是文件夹，请重新尝试！'
            elif 'list' in str(error):
                return "vtt", '文件夹中文件仅有1个，请确认文件是否正确！'

    def closeEvent(self, event):
        # 重写关闭事件
        self.clear_file()
        event.accept()

    def clear_file(self):
        pass


class ScrollableLabel(QWidget):
    def __init__(self):
        super().__init__()
        index_x, index_y = AndroidFunc.get_desktop_size()
        self.setGeometry(int(index_x / 2) - 390, int(index_y / 2) - 175, 750, 400)  # 设置窗口大小
        self.anr_arr = []
        self.trace_arr = []
        self.setWindowTitle("结果查看面板")
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
        self.anr_select_combo_box.addItems(self.show_err_file())
        self.anr_select_combo_box.setFixedSize(300, 20)
        self.hbox_1.addWidget(self.anr_select_combo_box, alignment=Qt.AlignLeft)

        self.show_detail_btn = QPushButton('打开错误文件', self)
        self.hbox_1.addWidget(self.show_detail_btn, alignment=Qt.AlignLeft)
        self.test_btn = QPushButton('预留btn', self)
        self.log_export_btn = QPushButton('预留btn', self)
        self.hbox_1.addWidget(self.test_btn, alignment=Qt.AlignRight)
        self.hbox_1.addWidget(self.log_export_btn, alignment=Qt.AlignRight)
        anr_title = QLabel('错误总览', self)
        anr_title.setWordWrap(True)
        anr_title.setTextInteractionFlags(Qt.TextSelectableByMouse)
        title_font = QFont()
        title_font.setPointSize(20)  # 设置字体大小为20
        anr_title.setText(str(err_file))
        scroll_area = QScrollArea()
        scroll_area.setWidget(anr_title)
        scroll_area.setWidgetResizable(True)  # 允许 QScrollArea 调整 QLabel 的大小
        self.hbox_2.addWidget(scroll_area)

        self.onclick_listen()
        self.show()

    def onclick_listen(self):
        self.anr_select_combo_box.currentIndexChanged.connect(self.get_index_change)
        self.show_detail_btn.clicked.connect(self.open_need_file)

    @staticmethod
    def show_err_file():
        unique_items = {}
        for item in err_file:
            prefix = item.split("--->")[0]  # 提取前缀
            if prefix not in unique_items:
                unique_items[prefix] = item  # 只保存第一个出现的

        # 获取去重后的结果
        result = list(unique_items.values())
        return result

    @staticmethod
    def get_index_value(combo_box):
        index = combo_box.currentIndex()
        value = combo_box.itemText(index)
        return value

    def open_need_file(self):
        file_name = self.get_index_change()
        need_path = os.path.join(file_path, file_name)
        if '//172.16.31.17/' in need_path:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)  # 设置消息图标类型
            msg.setText('暂不支持打开网络磁盘内的文件')  # 弹窗的主要内容
            msg.setWindowTitle("信息")  # 弹窗标题
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)  # 设置按钮
            retval = msg.exec_()
        else:
            os.startfile(need_path)

        # os.open()

    def get_index_change(self):
        need_data = self.get_index_value(self.anr_select_combo_box)
        res = str(need_data).split('---->')[0]
        return res


if __name__ == '__main__':
    app = QApplication(sys.argv)  # Instantiate the application object
    bootstrap_window = DramaWidget()  # Show the main window
    bootstrap_window.show()
    sys.exit(app.exec_())  # Handle application exit
