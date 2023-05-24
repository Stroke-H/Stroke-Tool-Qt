from gui.mainWindow import *


# from PyQt5.QtGui import *


# noinspection PyAttributeOutsideInit
class InteractWindow(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        main_window_x = parent.pos().x()
        main_window_y = parent.pos().y()
        self.setGeometry(int(main_window_x) + 755, int(main_window_y) + 30, 400, 70)  # 设置窗口大小
        self.setWindowTitle("交互面板")
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.parent.open_window_list.append('interact_window')
        self.notice = Notice()
        self.init_ui()
        self.onclick_listen()

    def init_ui(self):
        # 创建水平布局
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        # 创建标签
        self.data_label = QLabel('Link or Data', self)
        self.data_entry = QLineEdit(self)
        # # reg = QRegExp('[1-9a-zA-Z.]+$')
        # # validator = QRegExpValidator(self)  # 正则匹配规则
        # # validator.setRegExp(reg)
        # # self.package_name_entry.setValidator(validator)
        self.open_link_btn = QPushButton('打开网页', self)
        self.send_data_btn = QPushButton('发送内容', self)
        self.get_data_btn = QPushButton('获取内容', self)

        # 将标签添加到布局中
        self.hbox1.addWidget(self.data_label)
        self.hbox1.addWidget(self.data_entry)
        self.hbox2.addWidget(self.open_link_btn)
        self.hbox2.addWidget(self.send_data_btn)
        self.hbox2.addWidget(self.get_data_btn)

        self.setLayout(self.vbox)

        # 创建垂直布局

        self.show()

    def onclick_listen(self):
        self.open_link_btn.clicked.connect(self.open_link_btn_clicked)
        self.send_data_btn.clicked.connect(self.send_data_btn_clicked)
        self.get_data_btn.clicked.connect(self.get_data_btn_clicked)

    # 手机上打开链接
    def open_link_btn_clicked(self):
        my_link = self.data_entry.text()
        key = f'adb shell am start -a android.intent.action.VIEW -d "{my_link}"'
        AndroidFunc.subprocess_single(key)

    # 向手机剪切板发送信息
    def send_data_btn_clicked(self):
        key = f"adb shell am start -n ca.zgrs.clipper/ca.zgrs.clipper.Main"
        AndroidFunc.subprocess_single(key)
        time.sleep(1)
        send_data = str(self.data_entry.text()).replace('&', '%26')
        print(send_data)
        key1 = f'adb shell am broadcast -a clipper.set -e text "{send_data}"'
        AndroidFunc.subprocess_single(key1)
        time.sleep(1)
        key2 = 'adb shell am force-stop ca.zgrs.clipper'
        AndroidFunc.subprocess_single(key2)

    # 获取手机剪切板信息
    def get_data_btn_clicked(self):
        key = f"adb shell am start -n ca.zgrs.clipper/ca.zgrs.clipper.Main"
        AndroidFunc.subprocess_single(key)
        time.sleep(1)
        key1 = 'adb shell am broadcast -a clipper.get'
        res = AndroidFunc.subprocess_multiple(key1)
        time.sleep(1)
        data_res = res[1].decode('utf-8')
        print(data_res)
        if len(data_res) > 1:
            my_data = data_res.split('data=')[1]
            self.data_entry.setText(my_data)
        else:
            self.notice.error('您的手机剪切板没有内容')
        time.sleep(1)
        key2 = 'adb shell am force-stop ca.zgrs.clipper'
        AndroidFunc.subprocess_single(key2)


if __name__ == "__main__":
    pass
