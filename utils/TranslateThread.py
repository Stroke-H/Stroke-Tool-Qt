# -*- coding:utf-8 -*-

"""
@Author  :   StrokeH
@env     :   Python 3.11.3
@Time    :   2024/1/26 9:34 PM
@Desc    :   Qt子进程页面，主要为Translate的功能携程
"""
from PyQt5.QtCore import QThread, pyqtSignal
import requests


class TranslateThread(QThread):
    output = pyqtSignal(str, list)
    status_output = pyqtSignal(str, int)

    def __init__(self, thread_cmd):
        super().__init__()
        self.cmd = thread_cmd
        self.log_count = 0
        self.translate_info = []

    def run(self):
        cmd = self.cmd
        if 'address=' in cmd[1]:
            key_list = self.get_key_data(cmd[1].split('dress=')[1])
            for i in range(0, len(key_list)):
                for k in range(0, len(cmd[0])):
                    result = self.get_translate_result(cmd[0][k], key_list[i])
                    self.translate_info.append(result[0])
                    self.status_output.emit(key_list[i], k)
                self.output.emit(key_list[i], self.translate_info)
                self.translate_info = []
        else:
            for i in range(0, len(cmd[0])):
                result = self.get_translate_result(cmd[0][i], cmd[1])
                self.translate_info.append(result[0])
                self.status_output.emit(cmd[1], i)
            self.output.emit(cmd[1], self.translate_info)
            self.translate_info = []

    @staticmethod
    def get_translate_result(translate_country, key_word):
        """
        :param translate_country: 翻译后的语言
        :param key_word: 翻译的内容
        :return: 结果
      """
        result = []
        url = f'https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto' \
              f'&tl={translate_country}&dt=t&q={key_word}'
        json_result = requests.get(
            url=url)
        data = json_result.json()
        result.append(data[0][0][0])
        return result

    @staticmethod
    def get_key_data(path):
        with open(path, 'r', encoding='utf-8') as fp:
            data = [line.strip() for line in fp]
        return data
