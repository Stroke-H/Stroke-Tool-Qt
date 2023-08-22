# -*- coding:utf-8 -*-

"""
@Author  :   StrokeH
@env     :   Python 3.11.3
@Time    :   2023/3/20 1:34 PM
@Desc    :   Qt子进程页面，主要为IOS的功能携程
"""

from gui.mainWindow import *
import os
import time
import webbrowser


class IosThread(QThread):
    output = pyqtSignal(str)

    def __init__(self, adb_cmd):
        super().__init__()
        self.cmd = adb_cmd
        self.log_count = 0

    def run(self):
        cmd = self.cmd
        if 'IPA安装' in cmd:
            ios_udid = AndroidFunc.get_ios_udid()
            res = str(AndroidFunc.install(ios_udid))
            if '未链接设备' in res:
                self.output.emit(res)
            elif 'Local path  not exist' in res:
                self.output.emit('您未选择IPA安装包,请选择安装包后重试')
            elif '不是ipa格式' in res:
                self.output.emit(res)
            else:
                self.output.emit('安装成功')
