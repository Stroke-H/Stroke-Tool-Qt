import sys

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from utils.AndroidFunc import AndroidFunc


# noinspection PyAttributeOutsideInit
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Translate Window')
        self.setGeometry(100, 100, 1400, 300)
        self.setWindowOpacity(0.9)
        self.country = ['en', 'zh-CN', 'zh-TW', 'ko', 'de', 'jp', 'ru', 'es', 'it', 'fr', 'vi', 'pt', 'fa']
        self.translate_info = []
        self.gui_init()
        self.on_clicked_listen()

    def gui_init(self):
        self.my_window = QWidget()
        self.setCentralWidget(self.my_window)
        # 创建一个垂直布局
        self.vbox = QVBoxLayout(self.centralWidget())
        # 创建多个水平布局
        self.hbox_1 = QHBoxLayout()
        self.hbox_2 = QHBoxLayout()
        # self.hbox_3 = QHBoxLayout()
        # self.hbox_4 = QHBoxLayout()
        self.vbox.addLayout(self.hbox_1)
        self.vbox.addLayout(self.hbox_2)
        # self.vbox.addLayout(self.hbox_3)
        # self.vbox.addLayout(self.hbox_4)

        self.need_translate_entry = QLineEdit(self)
        self.need_translate_entry.setFixedSize(1200, 20)
        self.translate_btn = QPushButton('翻译', self)
        self.choose_btn = QPushButton('选择待翻译文件', self)
        self.hbox_1.addWidget(self.need_translate_entry)
        self.hbox_1.addWidget(self.choose_btn)
        self.hbox_1.addWidget(self.translate_btn)
        #
        self.table_log = QTableWidget()
        self.table_log.setColumnCount(len(self.country))
        self.table_log.setHorizontalHeaderLabels(
            self.country)
        # self.table_log.setColumnWidth(0, 150)
        # self.table_log.setColumnWidth(1, 70)
        # self.table_log.setColumnWidth(2, 70)
        # self.table_log.setColumnWidth(3, 70)
        self.table_log.setColumnWidth(4, 150)
        self.hbox_2.addWidget(self.table_log)

        self.setLayout(self.vbox)

        self.show()

    def on_clicked_listen(self):
        self.translate_btn.clicked.connect(self.do_translate)
        self.choose_btn.clicked.connect(self.get_config_file_path)

    def get_key_data(self, path):
        with open(path, 'r', encoding='utf-8') as fp:
            data = [line.strip() for line in fp]
        return data

    def get_config_file_path(self):
        path = AndroidFunc.get_file_path()
        if path[0]:
            self.need_translate_entry.setText(f'address={path[0]}')
        else:
            pass

    def get_translate_result(self, translate_country, key_word):
        """
        :param translate_country: 翻译后的语言
        :param key_word: 翻译的内容
        :return: 结果
      """

        url = f'https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto' \
              f'&tl={translate_country}&dt=t&q={key_word}'
        json_result = requests.get(
            url=url)
        data = json_result.json()
        result = []
        print(data[2], '-------------->', translate_country)
        result.append(data[0][0][0])
        return result

    def do_translate(self):
        country_list = self.country
        need_key = self.need_translate_entry.text()
        if 'address=' in need_key:
            key_list = self.get_key_data(need_key.split('dress=')[1])
            for i in range(0, len(key_list)):
                for k in range(0, len(country_list)):
                    result = self.get_translate_result(country_list[k], key_list[i])
                    self.translate_info.append(result[0])
                row = self.table_log.rowCount()
                self.table_log.insertRow(row)
                for col in range(len(self.translate_info)):
                    item = QTableWidgetItem(self.translate_info[col])
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table_log.setItem(row, col, item)
                self.table_log.setCurrentCell(row, 0)
                self.table_log.scrollToBottom()
                self.translate_info = []
        elif need_key:
            for i in range(0, len(country_list)):
                result = self.get_translate_result(country_list[i], need_key)
                self.translate_info.append(result[0])
            row = self.table_log.rowCount()
            self.table_log.insertRow(row)
            for col in range(len(self.translate_info)):
                item = QTableWidgetItem(self.translate_info[col])
                item.setTextAlignment(Qt.AlignCenter)
                self.table_log.setItem(row, col, item)
            self.table_log.setCurrentCell(row, 0)
            self.table_log.scrollToBottom()
            self.translate_info = []

        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())
