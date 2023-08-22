# -*- coding:utf-8 -*-

"""
@Author  :   StrokeH
@env     :   Python 3.11.3
@Time    :   2023/3/20 1:34 PM
@Desc    :   ios功能界面
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from gui.dialog import *
from utils.AndroidFunc import *
from gui.mainWindow import *
from utils.IOSThread import IosThread
import tidevice
from tidevice import Usbmux


# noinspection PyAttributeOutsideInit
class IosWindow(QWidget):

    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        main_window_x = self.parent_window.pos().x()
        main_window_y = self.parent_window.pos().y()
        self.setGeometry(int(main_window_x), int(main_window_y) - 180, 750, 70)  # 设置窗口大小
        self.setWindowTitle("IOS 功能辅助面板")
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.msg_box = QMessageBox()
        self.id = 1
        self.notice = Notice()
        self.init_ui()
        self.onclick_listen()

    def init_ui(self):
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox3 = QHBoxLayout()
        self.hbox4 = QHBoxLayout()
        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox3)
        self.vbox.addLayout(self.hbox4)

        # 第一个水平布局
        self.data_label = QLabel('Data Label', self)
        self.data_entry = QLineEdit(self)
        self.hbox1.addWidget(self.data_label)
        self.hbox1.addWidget(self.data_entry)

        # 第二个水平布局
        self.logTextEdit = QTextEdit()
        self.logTextEdit.setReadOnly(True)
        self.hbox2.addWidget(self.logTextEdit)

        # 第三个水平布局
        self.install_ipa = QPushButton('IPA安装', self)
        self.uninstall_ipa = QPushButton('IPA卸载', self)
        self.restart_app = QPushButton('重启应用', self)
        self.hbox3.addWidget(self.install_ipa)
        self.hbox3.addWidget(self.uninstall_ipa)
        self.hbox3.addWidget(self.restart_app)

        # 第四个水平布局
        self.get_phone_info = QPushButton('获取手机信息', self)
        self.screen_shot = QPushButton('手机截屏', self)
        self.get_package_name = QPushButton('获取包名', self)
        self.hbox4.addWidget(self.get_phone_info)
        self.hbox4.addWidget(self.screen_shot)
        self.hbox4.addWidget(self.get_package_name)

        self.setLayout(self.vbox)
        # self.show()

    def onclick_listen(self):
        self.install_ipa.clicked.connect(self.install_ipa_clicked)
        self.uninstall_ipa.clicked.connect(self.uninstall_ipa_clicked)
        self.restart_app.clicked.connect(self.restart_app_clicked)
        self.get_phone_info.clicked.connect(self.get_phone_info_clicked)
        self.screen_shot.clicked.connect(self.screen_shot_clicked)
        self.get_package_name.clicked.connect(self.show_package_name_clicked)

    def ios_thread_start(self, key):
        self.ios_thread = IosThread(key)
        self.ios_thread.output.connect(self.on_output_received)
        self.ios_thread.start()

    def on_output_received(self, output):
        self.logTextEdit.append(output)

    def install_ipa_clicked(self):
        if 'ConnectionType.USB' in str(Usbmux().device_list()).split(',')[2]:
            key = 'IPA安装'
            self.ios_thread_start(key)
        else:
            self.logTextEdit.append('未链接手机~~')

    def uninstall_ipa_clicked(self):
        if 'ConnectionType.USB' in str(Usbmux().device_list()).split(',')[2]:
            ios_udid = AndroidFunc.get_ios_udid()
            ios_bundle_id = self.data_entry.text()
            if ios_bundle_id:
                res = AndroidFunc.uninstall(ios_udid, ios_bundle_id)
                if '未链接设备' in str(res):
                    self.logTextEdit.append(res)
                else:
                    self.logTextEdit.append('卸载成功')
            else:
                self.logTextEdit.append('您未填入IosBundleId')
        else:
            self.logTextEdit.append('未链接手机~~')

    # 重启 app
    def restart_app_clicked(self):
        if 'ConnectionType.USB' in str(Usbmux().device_list()).split(',')[2]:
            ios_udid = AndroidFunc.get_ios_udid()
            ios_bundle_id = self.data_entry.text()
            res = str(AndroidFunc.restart_ipa(ios_udid, ios_bundle_id))
            if '未链接设备' in res:
                self.logTextEdit.append(res)
            elif 'Developer Mode is not opened' in res:
                self.logTextEdit.append(res)
            else:
                self.logTextEdit.append(f'已重启bundle id为:{ios_bundle_id}的应用')
        else:
            self.logTextEdit.append('未链接手机~~')

    # 获取当前链接的手机信息
    def get_phone_info_clicked(self):
        info = []
        msg = ''
        if 'ConnectionType.USB' in str(Usbmux().device_list()).split(',')[2]:
            ios_details = str(AndroidFunc.show_ios_info())
            data_list = ios_details.split(',')
            for i in data_list:
                res = i.replace("b'", '').replace("n'", '').replace('"', '') \
                    .replace('\\r\\', '').replace('[', '').replace("\x1b[0m']", '').strip()
                info.append(res)
            if 'MarketName:' in ios_details:
                self.msg_box.setIcon(QMessageBox.Information)
                self.msg_box.setWindowTitle("查询结果")

                self.msg_box.setText(f"{info}")
                self.msg_box.exec_()
            else:
                self.logTextEdit.append('Device：您当前未链接设备，请链接设备 not ready')
        else:
            self.logTextEdit.append('未链接手机~~')

    # 截图
    def screen_shot_clicked(self):
        if 'ConnectionType.USB' in str(Usbmux().device_list()).split(',')[2]:
            ios_udid = AndroidFunc.get_ios_udid()
            _path = AndroidFunc.screenshot(ios_udid, self.id)
            print(_path)
            if 'Developer Mode is not opened' in _path:
                self.logTextEdit.append(_path)
            else:
                self.id += 1
                self.logTextEdit.append(f'截图成功,图片保存在：{_path}')
        else:
            self.logTextEdit.append('未链接手机~~')

    # 展示bundle id
    def show_package_name_clicked(self):
        if 'ConnectionType.USB' in str(Usbmux().device_list()).split(',')[2]:
            try:
                ios_bundle_id = AndroidFunc.get_bundle_id()
                self.data_entry.setText(ios_bundle_id)
            except BaseException as error:
                print(error)
        else:
            self.logTextEdit.append('未链接手机~~')


if __name__ == "__main__":
    pass
