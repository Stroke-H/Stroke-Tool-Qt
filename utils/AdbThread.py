# -*- coding:utf-8 -*-

"""
@Author  :   StrokeH
@env     :   Python 3.11.3
@Time    :   2023/3/20 1:34 PM
@Desc    :   Qt子进程页面，主要为Android的功能携程
"""
import sys
import time

from PyQt5.QtCore import QThread, pyqtSignal
import subprocess
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
        if ' install' in cmd:
            path = cmd.split('install ')[1]
            try:
                key = fr'aapt dump badging "{path}"'
                res = subprocess.Popen(key, shell=True, stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                data_res = str(res.stdout.readlines())
                data_pkg = data_res.split("name='")[1].split("' versionCode")[0]
                data_activity = data_res.split("launchable-activity: name='")[1].split("'  label=")[0]
                self.output.emit(f'当前正在安装的APK PackageName为：<b>{data_pkg}</b>')
                self.output.emit(f'当前正在安装的APK LauncherActivity为：<b>{data_activity}</b>')
            except BaseException as error:
                self.output.emit(f'位置错误，信息处理异常:{error}')
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
            data = cmd.split('*-*')
            cmd = data[0]
            devices = data[1]
            proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            path = cmd.split('jar ')[1].split('\\bundletool')[0]
            self.output.emit('正在转化aab->apk>>>>>>请稍等……')
            turn_apk = str(proc.stdout.readlines())
            err_report = proc.stderr.readlines()
            if 'The APKs will be signed with the debug keystore found at' in turn_apk:
                self.output.emit('转包成功，正在安装转换完成的apk>>>>请稍等......')
                key = fr'java -jar {path}\bundletool.jar install-apks --apks=b.apks --device-id={devices}'
                apks_install = subprocess.Popen(key, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE)
                res = apks_install.stdout.readlines()
                res_data = str(res)
                print(res_data)
                key1 = 'del b.apks'
                self.output.emit('正在删除临时包:b.apks,安装即将完成,请稍等.....')
                subprocess.Popen(key1, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
                if 'Failed to commit install session' in res_data:
                    self.output.emit('安装失败！！！设备内已有相同或更高版本的apk包、或装有相同签名的apk')
                else:
                    self.output.emit('安装结果：安装成功！')
            elif '[]' in str(err_report):
                self.output.emit('转包成功，正在安装转换完成的apk>>>>请稍等......')
                # time.sleep(15)
                key = fr'java -jar {path}\bundletool.jar install-apks --apks=b.apks --device-id={devices}'
                apks_install = subprocess.Popen(key, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE)
                res = apks_install.stdout.readlines()
                res_data = str(res)
                print(res_data)
                key1 = 'del b.apks'
                self.output.emit('正在删除临时包:b.apks,安装即将完成,请稍等.....')
                subprocess.Popen(key1, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
                if 'Failed to commit install session' in res_data:
                    self.output.emit('安装失败！！！设备内已有相同或更高版本的apk包、或装有相同签名的apk')
                else:
                    self.output.emit('安装结果：安装成功！')
            elif 'Error:' in str(err_report):
                for i in err_report:
                    self.output.emit(f"<code><big>{i.decode('utf-8').strip()}</big></code>")
            else:
                self.output.emit('发生未知错误')

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
            data = cmd.split('*-*')
            cmd = data[0]
            devices = data[1]
            pic_name = cmd.split('/')[-1]
            cmd_shot = f'adb -s {devices} shell /system/bin/screencap -p /sdcard/screenshot.png'
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
                self.output.emit(f'<b>[{devices}]</b>截图成功，文件已保存桌面为>>>>>>{pic_name}')
            else:
                self.output.emit('截图失败T_T~~')
        elif 'https://webeye.feishu' in cmd:
            webbrowser.open_new_tab(cmd)  # 在新的浏览器标签页中打开网页
            self.output.emit('已打开当前项目的buglist,请去网页查看')
        elif 'aapt dump badging' in cmd:
            res = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            data = str(res.stdout.readline()).split("name='")[1].split("' versionCode")[0]
            self.output.emit(f'当前apk的包名为：<b>{data}</b>')
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
        elif 'logcat -v threadtime' in cmd:
            keyword_reg = 'uid_fission='
            res = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            devices = cmd.split(' ')[2]
            while res.poll() is None:
                line = res.stdout.readline().decode().strip()
                self.log_count += 1
                if keyword_reg in line:
                    data_res = line.split('uid_fission=')[1][0:16]
                    self.output.emit(f'{line}\n当前的uid={data_res}')
                    self.log_count = 0
                    clear_key = f'adb -s {devices} logcat -c'
                    res = subprocess.Popen(clear_key, shell=True, stdin=subprocess.PIPE,
                                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                elif self.log_count > 5000:
                    self.output.emit('暂未找到对应的Uid，请确认是否log中打印了id')
                    self.log_count = 0
                    clear_key = f'adb -s {devices} logcat -c'
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
        elif 'findstr mCurrentFocus' in cmd:
            res = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            data = res.stdout.readline().decode('utf-8')
            self.output.emit("当前正运行的APP应用PackageName和Activity如下:")
            self.output.emit(data)
            # if proc.returncode != 0:
            #     error = proc.stderr.read().decode()
            #     self.output.emit(error)
        elif 'shell pm list packages -3' in cmd:
            res = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            data = res.stdout.readlines()
            for pkg in data:
                self.output.emit(pkg.decode('utf-8').strip())
        elif 'shell pm list packages' in cmd:
            res = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            data = res.stdout.readlines()
            for pkg in data:
                self.output.emit(pkg.decode('utf-8').strip())
        elif 'start download' in cmd:
            device = cmd.split('*-*')[1]
            self.output.emit('未检测到待测试设备中安装了Xtest服务,即将开始下载Xtest-agent')
            self.output.emit('开始下载xtest-agent,请稍等~')
            time.sleep(1)
            download_url = 'http://172.16.32.30:8000/download_file/xtest-agent'
            save_path = os.path.join(AndroidFunc.get_desktop(), 'xtest-agent')

            # curl 方式，速度快，方便，但是log少
            key = rf'curl -L -o "{save_path}" {download_url}'
            res = subprocess.Popen(key, shell=True, stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            time.sleep(3)
            self.output.emit('xtest-agent: 100%|██████████| 17.5M/17.5M [00:04<00:00, 3.45MB/s]')
            # request方法，速度稍慢，但是打印多
            # response = requests.get(download_url, stream=True)
            # total_size = int(response.headers.get('content-length', 0))
            # print(total_size)
            # with open(save_path, 'wb') as file, tqdm(
            #         desc=os.path.basename(save_path),
            #         total=total_size,
            #         unit='B',
            #         unit_scale=True,
            #         unit_divisor=1024,
            # ) as bar:
            #     for data in response.iter_content(chunk_size=1024):
            #         size = file.write(data)
            #         print(size)
            #         bar.update(size)
            #         self.output.emit(str(bar)
            if os.path.exists(save_path):
                self.output.emit('xtest-agent下载完成，正在给待测试机器安装，请稍等~')
                key = f'adb -s {device} push {AndroidFunc.get_desktop()}/xtest-agent /data/local/tmp/xtest-agent'
                subprocess.Popen(key, shell=True, stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                time.sleep(1)
                if AndroidFunc.check_file_exist(device, '/data/local/tmp/', 'xtest-agent'):
                    self.output.emit('1 file pulled, 0 skipped. 32.9 MB/s (Done)')
                    self.output.emit('xtest-agent安装完成，正在为您启动服务~')
                    time.sleep(0.5)
                    cmd = f'adb -s {device} shell chmod 755 /data/local/tmp/xtest-agent'
                    subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                    time.sleep(0.5)
                    cmd = f'adb -s {device} shell /data/local/tmp/xtest-agent server --stop'
                    subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                    time.sleep(0.5)
                    cmd = f'adb -s {device} shell /data/local/tmp/xtest-agent server -d "$@"'
                    subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                    self.output.emit(f'已经为设备<b>[{device}]</b>启动Xtest')
