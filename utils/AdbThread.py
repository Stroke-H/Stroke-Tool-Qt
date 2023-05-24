# -*- coding:utf-8 -*-

"""
@Author  :   StrokeH
@env     :   Python 3.11.3
@Time    :   2023/3/20 1:34 PM
@Desc    :   Qt子进程页面，主要为Android的功能携程
"""

import time

from PyQt5.QtCore import QThread, pyqtSignal
import subprocess
from gui.dialog import *
from gui.mainWindow import *
import os
import time
import webbrowser
from utils.AndroidFunc import *


class AdbThread(QThread):
    output = pyqtSignal(str)

    def __init__(self, adb_cmd):
        super().__init__()
        self.cmd = adb_cmd
        self.log_count = 0

    def run(self):
        cmd = self.cmd
        if 'adb install' in cmd:
            proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            self.output.emit('APK开始安装>>>>>请稍等......')
            while proc.poll() is None:
                line = proc.stdout.readline().decode().strip()
                if line:
                    self.output.emit(line)
                    if 'Success' in line:
                        self.output.emit('安装结果：安装成功!')
                    elif 'no devices/emulators' in line:
                        self.output.emit('安装结果：您当前没有链接移动设备，请检查链接后重试!')
            if proc.returncode != 0:
                error = proc.stderr.read().decode()
                self.output.emit(error)
        elif 'bundletool.jar' in cmd:
            proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            path = cmd.split('jar ')[1].split('\\bundletool')[0]
            self.output.emit('正在转化aab->apk>>>>>>请稍等……')
            turn_apk = str(proc.stdout.readlines())
            if 'The APKs will be signed with the debug keystore found at' in turn_apk:
                self.output.emit('转包成功，正在安装转换完成的apk>>>>请稍等......')
                key = fr'java -jar {path}\bundletool.jar install-apks --apks=b.apks'
                apks_install = subprocess.Popen(key, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE)
                res = apks_install.stdout.readlines()
                res_data = str(res)
                key1 = 'del b.apks'
                self.output.emit('正在删除临时包:b.apks,安装即将完成,请稍等.....')
                subprocess.Popen(key1, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
                if 'Failed to commit install session' in res_data:
                    print(1)
                    self.output.emit('安装失败！！！设备内已有相同或更高版本的apk包、或装有相同签名的apk')
                else:
                    self.output.emit('安装结果：安装成功！')
            else:
                self.output.emit(f'转包失败，失败原因：{turn_apk}')
        elif 'uninstall' in cmd:
            proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            self.output.emit('正在查找选中应用并卸载>>>>>请稍等......')
            line = proc.stdout.readline().decode().strip()
            if "Success" in line:
                self.output.emit('卸载成功~~~')
            else:
                self.output.emit('当前应用未安装在本设备中，请确认包名……')
        elif 'pull /sdcard/screenshot.png' in cmd:
            pic_name = cmd.split('/')[-1]
            cmd_shot = 'adb shell /system/bin/screencap -p /sdcard/screenshot.png'
            res = subprocess.Popen(cmd_shot, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
            print(f"out >>>>>{res.stdout.readlines()}")
            print(f'err >>>>>{res.stderr.readlines()}')
            proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            res_data = proc.stdout.readline().decode()
            print(f"out >>>>>{res_data}")
            print(f'err >>>>>{proc.stderr.readlines()}')
            if "0 skipped" in res_data:
                self.output.emit(f'截图成功，文件已保存桌面为>>>>>>{pic_name}')
            else:
                self.output.emit('截图失败T_T~~')
        elif 'https://webeye.feishu' in cmd:
            webbrowser.open_new_tab(cmd)  # 在新的浏览器标签页中打开网页
            self.output.emit('已打开当前项目的buglist,请去网页查看')
        elif 'aapt dump badging' in cmd:
            res = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            data = str(res.stdout.readline()).split("name='")[1].split("' versionCode")[0]
            self.output.emit(f'当前apk的包名为：{data}')
        elif 'withdraw' in cmd:
            clear_key = 'adb logcat -c'
            res1 = subprocess.Popen(clear_key, shell=True, stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            res = subprocess.Popen('adb logcat -v threadtime', shell=True, stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            while res.poll() is None:
                line = res.stdout.readline().decode().strip()
                if 'code: ' in line:
                    code_num = line.split('code: ')[1]
                    my_db = AndroidFunc.sql_con(sql_name='data_sql')
                    cursor = my_db.cursor()
                    sql = f"""select * from code_list where code = '{code_num}'
                                                                        """
                    cursor.execute(sql)
                    data = cursor.fetchall()
                    cursor.close()
                    my_db.close()
                    self.output.emit(str(data))
                    print(data)
                    clear_key = 'adb logcat -c'
                    res = subprocess.Popen(clear_key, shell=True, stdin=subprocess.PIPE,
                                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif 'adb logcat -v threadtime' in cmd:
            keyword_reg = 'uid_fission='
            res = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            while res.poll() is None:
                line = res.stdout.readline().decode().strip()
                self.log_count += 1
                if keyword_reg in line:
                    data_res = line.split('uid_fission=')[1][0:16]
                    self.output.emit(f'{line}\n当前的uid={data_res}')
                    self.log_count = 0
                    clear_key = 'adb logcat -c'
                    res = subprocess.Popen(clear_key, shell=True, stdin=subprocess.PIPE,
                                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                elif self.log_count > 5000:
                    self.output.emit('暂未找到对应的Uid，请确认是否log中打印了id')
                    self.log_count = 0
                    clear_key = 'adb logcat -c'
                    res = subprocess.Popen(clear_key, shell=True, stdin=subprocess.PIPE,
                                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elif 'account' in cmd:
            self.output.emit(f'---  OVO and Dana  ---')
            self.output.emit(f'087712354684')
            self.output.emit(f'---  Paypal  ---')
            self.output.emit(f'Lunaazul2754@gmail.com  or  1126425037@qq.com')
            self.output.emit(f'---  Pix  ---')
            self.output.emit(f'80255600909')
            self.output.emit(f'---  Pagbank  ---')
            self.output.emit(f'allyssonnascimento04@gmail.com')
            # if proc.returncode != 0:
            #     error = proc.stderr.read().decode()
            #     self.output.emit(error)