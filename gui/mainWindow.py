# -*- coding:utf-8 -*-

"""
@Author  :   StrokeH
@env     :   Python 3.10.5
@Time    :   2022/8/11 1:34 PM
@Desc    :   Android界面布局
"""

import time

from PyQt5.QtWidgets import QMessageBox, QToolTip, QApplication, QSplashScreen, QLabel, QMainWindow
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from utils.AndroidFunc import AndroidFunc, logger
from gui.dialog import *
from gui.InteractWindow import InteractWindow
from gui.DelAccountWindow import DelAccountWindow
from gui.BackupInformationWindow import BackupInformationWindow
from gui.AuthorizeWindow import AuthorizeWindow
from gui.IosWindow import IosWindow
from utils.AdbThread import AdbThread
import subprocess
import platform
import os
import sys
import requests


# noinspection PyAttributeOutsideInit
class MainWindow(QMainWindow):
    def __init__(self):  # 初始化 继承父类QMainWindow
        super().__init__()
        index_x, index_y = AndroidFunc.get_desktop_size()
        self.setGeometry(int(index_x / 2) - 390, int(index_y / 2) - 175, 750, 375)  # 设置窗口大小
        self.setMinimumSize(750, 375)
        self.setWindowTitle("Stroke Tool 4.2.1")
        url = 'https://img95.699pic.com/xsj/1r/9r/g0.jpg%21/fw/700/watermark/url/L3hzai93YXRlcl9kZXRhaWwyLnBuZw/align/southeast'
        response = requests.get(url)
        pixmap = QPixmap()
        pixmap.loadFromData(response.content)
        icon = QIcon(pixmap)
        self.setWindowIcon(icon)
        # self.setWindowIcon(QIcon(QPixmap(r'C:\Users\dell\PycharmProjects\pyqtProject\image\icon_new.ico')))
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.notice = Notice()
        self.default_id = ''  # 用于接收下拉栏实时更新的id
        self.default_name = ''  # 用于接收下拉栏实时更新的package name
        self.log_count = 0
        self.img_id = 1
        self.is_open = 1
        self.devices_index = ''
        self.net_status = 'disable'
        self.source_type = 'both'
        self.status = self.statusBar()
        self.menu_bar = self.menuBar()
        self.status.showMessage(f'{AndroidFunc.get_day_soup()} ———— 欢迎使用Stroke Tool,祝您使用愉快..', 10000)
        self.msg_box = QMessageBox()
        self.gui_init()
        self.open_window_list = []
        self.con_status()
        self.onclick_listen()
        logger.info('工具已启动,监控日志正常获取中……')

    def gui_init(self):
        self.my_window = QWidget()
        self.setCentralWidget(self.my_window)
        # 创建一个垂直布局
        self.vbox = QVBoxLayout(self.centralWidget())
        # 创建多个水平布局
        self.hbox_1 = QHBoxLayout()
        self.hbox_2 = QHBoxLayout()
        self.hbox_3 = QHBoxLayout()
        self.hbox_4 = QHBoxLayout()
        self.hbox_5 = QHBoxLayout()
        self.hbox_6 = QHBoxLayout()
        self.hbox_7 = QHBoxLayout()
        self.hbox_8 = QHBoxLayout()
        self.hbox_9 = QHBoxLayout()
        self.hbox_10 = QHBoxLayout()
        self.vbox.addLayout(self.hbox_1)
        self.vbox.addLayout(self.hbox_2)
        self.vbox.addLayout(self.hbox_3)
        self.vbox.addLayout(self.hbox_4)
        self.vbox.addLayout(self.hbox_5)
        self.vbox.addLayout(self.hbox_6)
        self.vbox.addLayout(self.hbox_7)
        self.vbox.addLayout(self.hbox_8)
        self.vbox.addLayout(self.hbox_9)
        self.vbox.addLayout(self.hbox_10)

        # 菜单栏
        file_menu = self.menu_bar.addMenu('Options')
        backup_action = QAction('信息备份', self)
        self.info_select_action = QAction('仅显示tool源', self)
        account_action = QAction('显示提现账号', self)
        backup_action.triggered.connect(self.backup_information_btn_clicked)
        self.info_select_action.triggered.connect(self.info_select_clicked)
        account_action.triggered.connect(self.show_account_btn_clicked)
        file_menu.addAction(backup_action)
        file_menu.addAction(self.info_select_action)
        file_menu.addAction(account_action)

        other_menu = self.menu_bar.addMenu('IOS Function')
        ios_action = QAction('IOS功能界面', self)
        ios_action.triggered.connect(self.ios_panel_btn_clicked)
        other_menu.addAction(ios_action)

        # android_com_func_menu = self.menu_bar.addMenu('Android常用功能')
        # show_date_panel = QAction('打开时间界面', self)
        # show_language_panel = QAction('打开语言界面', self)
        # show_date_panel.triggered.connect(self)

        # 第一个水平布局的按钮
        # 选择游戏文本的label
        # self.game_select_label = QLabel('选择游戏', self)
        self.devices_select_combo_box = QComboBox(self)
        self.devices_select_combo_box.addItems(AndroidFunc.get_devices_list())
        self.devices_select_combo_box.setFixedSize(100, 20)
        # 游戏目录的下拉框
        self.game_select_combo_box = QComboBox(self)
        self.game_select_combo_box.addItems(AndroidFunc.get_id_and_package_name_list())
        self.game_select_combo_box.setFixedSize(200, 20)
        self.devices_index = self.get_index_value(self.devices_select_combo_box)
        # 文本输入框
        self.package_name_entry = QLineEdit(self)
        reg = QRegExp('[0-9a-zA-Z.]+$')
        validator = QRegExpValidator(self)  # 正则匹配规则
        validator.setRegExp(reg)
        self.package_name_entry.setValidator(validator)
        self.package_name_entry.textChanged.connect(self.show_tooltip)
        # 刷新列表按钮
        self.refresh_btn = QPushButton('刷新列表', self)
        self.refresh_btn.setToolTip('点击可以刷新左侧<b>包名及设备下拉栏</b>')
        # 打开bug_list按钮
        self.bug_list_btn = QPushButton('打开bug清单', self)
        self.bug_list_btn.setToolTip('点击可以打开左侧对应包名的<b>BugList链接</b>')

        self.hbox_1.addWidget(self.devices_select_combo_box)
        self.hbox_1.addWidget(self.game_select_combo_box)
        self.hbox_1.addWidget(self.package_name_entry)
        self.hbox_1.addWidget(self.refresh_btn)
        self.hbox_1.addWidget(self.bug_list_btn)

        # 第二个水平布局
        self.left_line_label_1 = QLabel('------------------------------------------', self)
        self.android_describe_label = QLabel('Package Control Function', self)
        self.android_describe_label.setAlignment(Qt.AlignCenter)
        self.right_line_label_1 = QLabel('------------------------------------------', self)
        self.hbox_2.addWidget(self.left_line_label_1)
        self.hbox_2.addWidget(self.android_describe_label)
        self.hbox_2.addWidget(self.right_line_label_1)

        # 第三个水平布局的按钮
        self.install_btn = QPushButton('APP安装', self)
        self.install_btn.setToolTip('选取指定的<b>APK或aab</b>文件安装')
        self.uninstall_btn = QPushButton('APP卸载', self)
        self.uninstall_btn.setToolTip('卸载<b>输入栏</b>中对应包名的手机APK')
        self.clear_cache_btn = QPushButton('清除缓存', self)
        self.clear_cache_btn.setToolTip('清除<b>输入栏</b>中对应包名的APK缓存')
        self.install_referer_btn = QPushButton('AB转换', self)
        self.install_referer_btn.setToolTip('install referer的A→B转换,使用时需要先在<b>输入栏</b>填入对应的包名')
        self.get_token_id_btn = QPushButton('RichOx ID', self)
        self.get_token_id_btn.setToolTip('从日志中找到当前使用的<b>RIchoxID</b>')
        self.current_package_btn = QPushButton('当前包名', self)
        self.current_package_btn.setToolTip('选择一个<b>APK</b>查看对应的包名,如果不选择则查看当前运行的程序包名')
        self.restart_btn = QPushButton('APP重启', self)
        self.restart_btn.setToolTip('重启<b>输入栏</b>中对应包名的应用,如果没输入则重启当前运行的应用')
        self.current_pkg_and_act_btn = QPushButton('当前P和L', self)
        self.current_pkg_and_act_btn.setToolTip('显示<b>当前运行</b>应用的packageName和launcherActivity')
        self.permission_check_btn = QPushButton('查看权限', self)
        self.permission_check_btn.setToolTip('查看选中APK的<b>权限使用情况</b>')
        self.hbox_3.addWidget(self.install_btn)
        self.hbox_3.addWidget(self.uninstall_btn)
        self.hbox_3.addWidget(self.clear_cache_btn)
        self.hbox_3.addWidget(self.install_referer_btn)
        self.hbox_3.addWidget(self.get_token_id_btn)
        self.hbox_3.addWidget(self.current_package_btn)
        self.hbox_3.addWidget(self.restart_btn)
        self.hbox_3.addWidget(self.current_pkg_and_act_btn)
        self.hbox_3.addWidget(self.permission_check_btn)

        # 第四个水平布局的按钮
        self.left_line_label_2 = QLabel('------------------------------------------', self)
        self.other_describe_label = QLabel('Surround Control Function', self)
        self.other_describe_label.setAlignment(Qt.AlignCenter)
        self.right_line_label_2 = QLabel('------------------------------------------', self)
        self.hbox_4.addWidget(self.left_line_label_2)
        self.hbox_4.addWidget(self.other_describe_label)
        self.hbox_4.addWidget(self.right_line_label_2)

        # 第五个水平布局的按钮
        self.screenshot_btn = QPushButton('手机截图', self)
        self.screenshot_btn.setToolTip('截取手机当前的界面,截图保存在<b>电脑桌面</b>')
        self.clear_screenshot_btn = QPushButton('清除截图', self)
        self.clear_screenshot_btn.setToolTip('清除<b>手机截图</b>功能截取的所有截图')
        self.show_ip_btn = QPushButton('展示当前IP', self)
        self.show_ip_btn.setToolTip('在手机上展示当前的<b>ip地址</b>,仅挂载vpn有效')
        self.net_change_btn = QPushButton('网络切换', self)
        self.net_change_btn.setToolTip('修改<b>手机WIFI</b>的状态,打开or关闭')
        self.sign_check_btn = QPushButton('签名检查', self)
        self.sign_check_btn.setToolTip('获取选择的APK的<b>SHA1,SHA256,MD5</b>与最初版本的三个属性比对')
        self.adb_reboot_btn = QPushButton('ADB重启', self)
        self.adb_reboot_btn.setToolTip('重启ADB的链接')
        self.interact_btn = QPushButton('交互面板', self)
        self.interact_btn.setToolTip('打开交互面板,实现手机与电脑的<b>文本信息传输</b>')
        self.del_panel_btn = QPushButton('删号功能', self)
        self.del_panel_btn.setToolTip('打开删号面板,实现对应项目的SQL傻瓜式<b>数据修改</b>处理')
        self.open_google_link_btn = QPushButton('google链接', self)
        self.open_google_link_btn.setToolTip('打开<b>输入栏</b>中对应报名的google商店链接')
        self.hbox_5.addWidget(self.screenshot_btn)
        self.hbox_5.addWidget(self.clear_screenshot_btn)
        self.hbox_5.addWidget(self.show_ip_btn)
        self.hbox_5.addWidget(self.net_change_btn)
        self.hbox_5.addWidget(self.sign_check_btn)
        self.hbox_5.addWidget(self.adb_reboot_btn)
        self.hbox_5.addWidget(self.interact_btn)
        self.hbox_5.addWidget(self.del_panel_btn)
        self.hbox_5.addWidget(self.open_google_link_btn)

        self.open_language_btn = QPushButton('语言目录', self)
        self.open_language_btn.setToolTip('直接打开手机的<b>语言设置页面</b>,当前适配手机:<b>pixel</b>')
        self.open_date_btn = QPushButton('时间目录', self)
        self.open_date_btn.setToolTip('直接打开手机的<b>时间设置页面</b>,当前适配手机:<b>pixel</b>')
        self.show_all_pkg_name_btn = QPushButton('所有pkg', self)
        self.show_all_pkg_name_btn.setToolTip('log打印手机的<b>所有packageName</b>')
        self.show_3_pkg_name_btn = QPushButton('第三方pkg', self)
        self.show_3_pkg_name_btn.setToolTip('log打印手机的<b>所有第三方packageName</b>')
        self.monkey_test_btn = QPushButton('启动Xtest', self)
        self.monkey_test_btn.setToolTip('启动手机上的<b>xtest的架构包</b>')
        self.test_btn = QPushButton('预留BTN', self)
        self.test_btn2 = QPushButton('预留BTN', self)
        self.test_btn3 = QPushButton('预留BTN', self)
        self.test_btn4 = QPushButton('预留BTN', self)
        self.hbox_6.addWidget(self.open_language_btn)
        self.hbox_6.addWidget(self.open_date_btn)
        self.hbox_6.addWidget(self.show_all_pkg_name_btn)
        self.hbox_6.addWidget(self.show_3_pkg_name_btn)
        self.hbox_6.addWidget(self.monkey_test_btn)
        self.hbox_6.addWidget(self.test_btn)
        self.hbox_6.addWidget(self.test_btn2)
        self.hbox_6.addWidget(self.test_btn3)
        self.hbox_6.addWidget(self.test_btn4)

        # 第七个水平布局的按钮
        self.left_line_label_3 = QLabel('===========================================', self)
        self.status_label = QLabel('Current Connect Status', self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.right_line_label_3 = QLabel('===========================================', self)
        self.hbox_7.addWidget(self.left_line_label_3)
        self.hbox_7.addWidget(self.status_label)
        self.hbox_7.addWidget(self.right_line_label_3)

        # 第八个水平布局的按钮
        self.model_label = QLabel('', self)
        self.model_label.setAlignment(Qt.AlignCenter)
        self.version_label = QLabel('', self)
        self.version_label.setAlignment(Qt.AlignCenter)
        self.size_label = QLabel('', self)
        self.size_label.setAlignment(Qt.AlignCenter)
        self.hbox_8.addWidget(self.model_label)
        self.hbox_8.addWidget(self.version_label)
        self.hbox_8.addWidget(self.size_label)

        # 第九个水平布局的按钮
        self.end_line_label = QLabel(
            '==============================================================================='
            '================================================================', self)
        self.hbox_9.addWidget(self.end_line_label)

        # 第十个水平布局的按钮
        self.logTextEdit = QTextEdit()
        self.logTextEdit.setReadOnly(True)
        self.hbox_10.addWidget(self.logTextEdit)

        self.show()

    def thread_start(self, key):
        self.install_adb = AdbThread(key)
        self.install_adb.output.connect(self.on_output_received)
        self.install_adb.start()
        logger.info(f'当前开启了子进程,进程命令为:{key}')

    def onclick_listen(self):
        self.refresh_btn.clicked.connect(self.refresh_btn_clicked)
        self.bug_list_btn.clicked.connect(self.bug_list_btn_clicked)
        self.devices_select_combo_box.currentIndexChanged.connect(self.devices_index_change)
        self.game_select_combo_box.currentIndexChanged.connect(self.game_index_change)
        self.install_btn.clicked.connect(self.install_btn_clicked)
        self.uninstall_btn.clicked.connect(self.uninstall_btn_clicked)
        self.current_package_btn.clicked.connect(self.current_package_btn_clicked)
        self.restart_btn.clicked.connect(self.restart_btn_clicked)
        self.clear_cache_btn.clicked.connect(self.clear_cache_btn_clicked)
        self.install_referer_btn.clicked.connect(self.install_referer_btn_clicked)
        self.get_token_id_btn.clicked.connect(self.get_token_id_btn_clicked)
        self.screenshot_btn.clicked.connect(self.screenshot_btn_clicked)
        self.show_ip_btn.clicked.connect(self.show_ip_btn_clicked)
        self.net_change_btn.clicked.connect(self.net_change_btn_clicked)
        self.sign_check_btn.clicked.connect(self.sign_check_btn_clicked)
        self.clear_screenshot_btn.clicked.connect(self.clear_screenshot_btn_clicked)
        self.adb_reboot_btn.clicked.connect(self.restart_adb)
        self.interact_btn.clicked.connect(self.interact_btn_clicked)
        self.del_panel_btn.clicked.connect(self.del_panel_btn_clicked)
        self.open_google_link_btn.clicked.connect(self.open_google_link_btn_clicked)
        self.permission_check_btn.clicked.connect(self.permission_check_btn_clicked)
        self.open_language_btn.clicked.connect(self.open_language_btn_clicked)
        self.open_date_btn.clicked.connect(self.open_date_btn_clicked)
        self.current_pkg_and_act_btn.clicked.connect(self.pkg_and_activity_btn_clicked)
        self.show_all_pkg_name_btn.clicked.connect(self.all_pkg_btn_clicked)
        self.show_3_pkg_name_btn.clicked.connect(self.third_pkg_btn_clicked)
        self.monkey_test_btn.clicked.connect(self.start_xtest)

    def game_index_change(self):
        self.default_id = self.get_index_value(self.game_select_combo_box)
        self.package_name_entry.setText(f"{self.default_id.split('-')[1]}")
        self.status.showMessage(f'当前选择游戏为{self.default_id}……', 3000)
        self.default_name = self.default_id.split('-')[1]
        return self.default_id.split('-')[0]

    def devices_index_change(self):
        self.devices_index = self.get_index_value(self.devices_select_combo_box)
        return self.devices_index

    @staticmethod
    def get_index_value(combo_box):
        index = combo_box.currentIndex()
        value = combo_box.itemText(index)
        return value

    def restart_adb(self):
        AndroidFunc.restart_adb(self.devices_index)
        self.logTextEdit.append(f'<b>[{self.devices_index}]</b>adb已重启')
        logger.info(f'当前重启了{self.devices_index}设备')

    def con_status(self):
        if self.devices_index:
            try:
                ad_name, ad_version, screen_size = AndroidFunc.get_info(self.devices_index)
                self.model_label.setText(f'设备名称：{ad_name.strip()}')
                self.version_label.setText(f'安卓版本：{ad_version.strip()}')
                self.size_label.setText(f'分辨率：{screen_size.split(":")[1].strip()}')
                return 1
            except BaseException as error:
                logger.error(error)
                self.model_label.setText('未连接设备')
                self.version_label.setText('未连接设备')
                self.size_label.setText('未连接设备')
                return 0
        else:
            self.model_label.setText('未连接设备')
            self.version_label.setText('未连接设备')
            self.size_label.setText('未连接设备')
            return 0

    def on_output_received(self, output):
        self.logTextEdit.append(output)

    def open_language_btn_clicked(self):
        key = f'adb -s {self.devices_index} shell am start -a android.settings.LOCALE_SETTINGS'
        AndroidFunc.subprocess_single(key)
        self.logTextEdit.append(f'<b>[{self.devices_index}]</b>设备的语言界面已打开')
        logger.info("当前打开了语言界面")

    def open_date_btn_clicked(self):
        key = f'adb -s {self.devices_index} shell am start -a android.settings.DATE_SETTINGS'
        AndroidFunc.subprocess_single(key)
        self.logTextEdit.append(f'<b>[{self.devices_index}]</b>设备的时间界面已打开')
        logger.info("当前打开了语言界面")

    def start_xtest(self):
        if AndroidFunc.check_file_exist(self.devices_index, '/data/local/tmp/', 'xtest-agent'):
            cmd = f'adb -s {self.devices_index} shell chmod 755 /data/local/tmp/xtest-agent'
            AndroidFunc.subprocess_single(cmd)
            cmd = f'adb -s {self.devices_index} shell /data/local/tmp/xtest-agent server --stop'
            AndroidFunc.subprocess_single(cmd)
            cmd = f'adb -s {self.devices_index} shell /data/local/tmp/xtest-agent server -d "$@"'
            AndroidFunc.subprocess_single(cmd)
            self.logTextEdit.append(f'检测到您手机内有必要软件，已经为设备<b>[{self.devices_index}]</b>启动xtest')
        else:
            key = f'start download*-*{self.devices_index}'
            self.thread_start(key)

    def install_btn_clicked(self):
        if self.con_status():
            path = AndroidFunc.get_file_path()
            if path[0]:
                if 'apk' in path[0]:
                    try:
                        game_code = path[0].split('/')[-1].split('_')[0]
                        my_db = AndroidFunc.sql_con(sql_name='data_sql')
                        cursor = my_db.cursor()
                        sql = f"""select package_name from android_game_info where app_id = '{game_code}'
                                                                            """
                        cursor.execute(sql)
                        game_id = cursor.fetchone()[0]
                        cursor.close()
                        my_db.close()
                        self.package_name_entry.setText(game_id)
                        self.status.showMessage(f'[{self.devices_index}]正在安装中,请稍等……', 3000)
                        self.logTextEdit.append(f'<b>[{self.devices_index}]</b>将执行安装操作！')
                    except BaseException as err:
                        self.notice.warn('您当前安装的应用非本公司项目或命名不规范，正在为您安装，请稍等')
                        self.logTextEdit.append(f'<b>[{self.devices_index}]</b>将执行安装操作！')
                    time.sleep(1)
                    key = f'adb -s {self.devices_index} install "{path[0]}"'
                    self.thread_start(key)
                elif 'aab' in path[0]:
                    game_code = path[0].split('/')[-1].split('_')[0]
                    try:
                        my_db = AndroidFunc.sql_con(sql_name='data_sql')
                        cursor = my_db.cursor()
                        sql = f"""select package_name from android_game_info where app_id = '{game_code}'
                                                                                                    """
                        cursor.execute(sql)
                        game_id = cursor.fetchone()[0]
                        cursor.close()
                        my_db.close()
                        self.package_name_entry.setText(game_id)
                    except BaseException as error:
                        self.logTextEdit.append(str(error))
                        self.notice.info('当前安装的应用名不符合标准规范~')
                    finally:
                        work_path = os.getcwd()
                        my_path = str(AndroidFunc.get_desktop())
                        system_path = my_path.replace('Desktop', '')
                        os.chdir(system_path)
                        self.status.showMessage(f'<b>[{self.devices_index}]</b>正在转化aab->apk,请稍等……', 3000)
                        model = platform.node()
                        if model != 'DESKTOP-FHQH1MA':
                            key = fr'java -jar {my_path}\bundletool.jar build-apks --connected-device --bundle="{path[0]}" --output=b.apks*-*{self.devices_index}'
                        else:
                            key = fr'java -jar {my_path}\bundletool.jar build-apks --bundle="{path[0]}" --output=b.apks --ks=C:\Users\dell\my-release-key.keystore --ks-pass=pass:102712 --ks-key-alias=hmh --key-pass=pass:102712*-*{self.devices_index}'
                        self.thread_start(key)
                        os.chdir(work_path)
                else:
                    self.notice.warn("您选择的文件不是aab或apk哦~")
            else:
                self.notice.warn("您还没选择文件呀~~")
        else:
            self.notice.error('adb未链接，请检查设备T_T~')

    def uninstall_btn_clicked(self):
        if self.con_status():
            game_id = self.package_name_entry.text()
            if game_id:
                key = f"adb -s {self.devices_index} uninstall {game_id}"
                self.logTextEdit.append(f'<b>[{self.devices_index}]</b>设备将执行卸载操作！')
                self.thread_start(key)
            else:
                self.notice.warn('您还没有选择包名呀~')
        else:
            self.notice.error('adb未链接，请检查设备T_T~')

    def current_package_btn_clicked(self):
        if self.con_status():
            path = AndroidFunc.get_file_path()[0]
            if path:
                key = fr'aapt dump badging "{path}"'
                self.thread_start(key)
            else:
                package_name = AndroidFunc.get_current_package_name(self.devices_index)
                self.logTextEdit.append(f'<b>[{self.devices_index}]</b>设备当前apk的包名为：{package_name}')
                logger.info(f'当前正在获取当前包名,获取的包名为：{package_name}')
        else:
            self.notice.error('adb未链接，请检查设备T_T~')

    def restart_btn_clicked(self):
        if self.con_status():
            package_name = self.package_name_entry.text()
            if package_name:
                logger.info(f'当前正在重启包名为{package_name}的应用')
                launcher_id = ''
                try:
                    my_db = AndroidFunc.sql_con(sql_name='data_sql')
                    cursor = my_db.cursor()
                    sql = f"""select launcher_activity from android_game_info where package_name = '{package_name}'
                                    """
                    cursor.execute(sql)
                    launcher_id = cursor.fetchone()
                    cursor.close()
                    my_db.close()
                except BaseException as error:
                    logger.error(error)
                if launcher_id[0]:
                    self.status.showMessage(f'正在为您重启LauncherActivity为{launcher_id[0]}的app……', 3000)
                    key = f"adb -s {self.devices_index} shell am force-stop {package_name}"
                    AndroidFunc.subprocess_out(key)
                    time.sleep(1)
                    key1 = f"adb -s {self.devices_index} shell am start -n {package_name}/{launcher_id[0]}"
                    res = AndroidFunc.subprocess_err(key1).readlines()
                    if "not exist" in str(res):
                        self.notice.warn('当前的app未安装在本设备内呀，核对再尝试一次吧')
                elif launcher_id[0] == '':
                    try:
                        key = f"adb -s {self.devices_index} shell am force-stop {package_name}"
                        AndroidFunc.subprocess_out(key)
                        time.sleep(1)
                        key1 = f"adb -s {self.devices_index} shell am start -n {package_name}/.UnityMain"
                        res = AndroidFunc.subprocess_err(key1).readlines()
                        if "not exist" in str(res):
                            self.notice.warn('当前的app未备份LauncherActivity，核对再尝试一次吧')
                    except Exception as e:
                        print(e)
            else:
                try:
                    self.status.showMessage('您未设置id，正在你重启当前应用', 3000)
                    AndroidFunc.restart_current_app(self.devices_index)
                except Exception as e:
                    print(e)
        else:
            self.notice.error('adb未链接，请检查设备T_T~')

    def clear_cache_btn_clicked(self):
        if self.con_status():
            package_name = self.package_name_entry.text()
            rec_data = AndroidFunc.clear_cache(package_name, self.devices_index)
            self.logTextEdit.append(f'<b>[{self.devices_index}]</b>设备将执行清除缓存操作！')
            logger.info(f'当前正在清除包名为：{package_name}的应用')
            match rec_data:
                case 'success':
                    self.notice.success('已经清除了指定的应用缓存啦^0^~~')
                    self.logTextEdit.append(f'<b>[{self.devices_index}]</b>设备缓存清除成功')
                case 'failed':
                    self.notice.warn('指定的应用没有安装在本设备中，清确认后重试-,-~~')
                case 'no running app':
                    self.notice.error('您未指定应用哦0.0~~')
                case 'current success':
                    self.notice.success('由于您未指定应用，已为您清楚了当前运行的应用缓存=,=')
        else:
            self.notice.error('adb未链接，请检查设备T_T~')

    def show_tooltip(self):
        text = self.package_name_entry.text()
        if text and len(text) == 4:
            code, dic = AndroidFunc.get_code_and_des()
            # 根据 QLineEdit 的值设置不同的提示文本
            if int(text) in code:
                tooltip_text = dic[int(text)]
                self.package_name_entry.setToolTip(tooltip_text)
                QToolTip.showText(self.package_name_entry.mapToGlobal(self.package_name_entry.rect().topLeft()),
                                  tooltip_text)
            else:
                pass

    def install_referer_btn_clicked(self):
        if self.con_status():
            temp = self.package_name_entry.text()
            path = AndroidFunc.get_file_path()
            if temp and path:
                if 'apk' in path[0]:
                    try:
                        game_code = path[0].split('/')[-1].split('_')[0]
                        my_db = AndroidFunc.sql_con(sql_name='data_sql')
                        cursor = my_db.cursor()
                        sql = f"""select package_name from android_game_info where app_id = '{game_code}'
                                                                                        """
                        cursor.execute(sql)
                        game_id = cursor.fetchone()[0]
                        cursor.close()
                        my_db.close()
                        self.package_name_entry.setText(game_id)
                        self.status.showMessage(f'[{self.devices_index}]正在安装中,请稍等……', 3000)
                        self.logTextEdit.append(f'<b>[{self.devices_index}]</b>将执行安装操作！')
                    except BaseException as err:
                        self.notice.warn('您当前安装的应用非本公司项目或命名不规范，正在为您安装，请稍等')
                        self.logTextEdit.append(f'<b>[{self.devices_index}]</b>将执行安装操作！')
                    time.sleep(1)
                    key = f'adb -s {self.devices_index} install "{path[0]}"'
                    self.thread_start(key)
                elif '.aab' in path[0]:
                    self.logTextEdit.append('正在进行aab安装并切换organic>>>>>>>')
                    link_key = f'adb -s {self.devices_index} shell am start -a android.intent.action.VIEW -d "https://play.google.com/store/apps/' \
                               f'details?id={temp}&referrer=utm_source%3Dgoogle%26utm_medium%3Dcpc%26utm_term%3Drunning' \
                               f'%252Bshoes%26utm_content%3Dlogolink%26utm_campaign%3Dspring_sale"'
                    AndroidFunc.subprocess_single(link_key)
                    game_code = path[0].split('/')[-1].split('_')[0]
                    try:
                        my_db = AndroidFunc.sql_con(sql_name='data_sql')
                        cursor = my_db.cursor()
                        sql = f"""select package_name from android_game_info where app_id = '{game_code}'
                                                                                                                        """
                        cursor.execute(sql)
                        game_id = cursor.fetchone()[0]
                        cursor.close()
                        my_db.close()
                        self.package_name_entry.setText(game_id)
                    except BaseException as error:
                        self.logTextEdit.append(str(error))
                        self.notice.info('当前安装的应用名不符合标准规范~')
                    finally:
                        work_path = os.getcwd()
                        my_path = str(AndroidFunc.get_desktop())
                        system_path = my_path.replace('Desktop', '')
                        os.chdir(system_path)
                        self.status.showMessage(f'<b>[{self.devices_index}]</b>正在转化aab->apk,请稍等……', 3000)
                        model = platform.node()
                        if model != 'DESKTOP-FHQH1MA':
                            key = fr'java -jar {my_path}\bundletool.jar build-apks --connected-device --bundle="{path[0]}" --output=b.apks*-*{self.devices_index}'
                        else:
                            key = fr'java -jar {my_path}\bundletool.jar build-apks --bundle="{path[0]}" --output=b.apks --ks=C:\Users\dell\my-release-key.keystore --ks-pass=pass:102712 --ks-key-alias=hmh --key-pass=pass:102712*-*{self.devices_index}'
                        self.thread_start(key)
                        os.chdir(work_path)
                else:
                    self.notice.warn("您选择的文件不是aab或apk哦~")
            else:
                self.notice.warn("您还没选择文件呀~~")
        else:
            self.notice.error('adb未链接，请检查设备T_T~')

    def get_token_id_btn_clicked(self):
        if self.con_status():
            temp = self.package_name_entry.text()
            if temp:
                self.status.showMessage(f'<b>[{self.devices_index}]</b>正在从日志中获取Uid,请稍等>>>>', 3000)
                self.restart_btn_clicked()
                clear_key = f'adb -s {self.devices_index} logcat -c'
                AndroidFunc.subprocess_out(clear_key)
                command = f"adb -s {self.devices_index} logcat -v threadtime"
                self.thread_start(command)
            else:
                self.notice.warn('您未选择对应应用，请选择后重试=,=')
        else:
            self.notice.error('adb未链接，请检查设备T_T~')

    def refresh_btn_clicked(self):
        self.game_select_combo_box.disconnect()
        self.game_select_combo_box.clear()
        self.game_select_combo_box.addItems(AndroidFunc.get_id_and_package_name_list())
        self.game_select_combo_box.currentIndexChanged.connect(self.game_index_change)
        self.devices_select_combo_box.disconnect()
        self.devices_select_combo_box.clear()
        self.devices_select_combo_box.addItems(AndroidFunc.get_devices_list())
        self.devices_select_combo_box.currentIndexChanged.connect(self.devices_index_change)
        self.devices_index = self.get_index_value(self.devices_select_combo_box)
        logger.info('当前刷新了下拉栏的信息')

    def bug_list_btn_clicked(self):
        if self.con_status():
            my_data = self.package_name_entry.text()
            if my_data:
                try:
                    my_db = AndroidFunc.sql_con(sql_name='data_sql')
                    cursor = my_db.cursor()
                    sql = f"""select bugList_link from android_game_info where package_name = '{my_data}'
                                    """
                    cursor.execute(sql)
                    res = cursor.fetchone()
                    cursor.close()
                    my_db.close()
                    if res:
                        self.thread_start(res[0])
                        logger.info(f'打开buglist，网址为：{res[0]}')
                        self.notice.success('已打开当前项目的buglist，请去网页查看内容')
                    else:
                        self.notice.warn('当前包名关联游戏没有bugList或未在数据库备份')
                except BaseException as error:
                    logger.error(error)
            else:
                self.notice.warn('您未选定需要打开bugList的应用名')
        else:
            self.notice.error('adb未链接，请检查设备T_T~')

    def screenshot_btn_clicked(self):
        if self.con_status():
            cmd_pull = f'adb -s {self.devices_index} pull /sdcard/screenshot.png {AndroidFunc.get_desktop()}/ScImg{self.img_id}.png*-*{self.devices_index}'
            self.thread_start(cmd_pull)
            self.img_id += 1
            self.logTextEdit.append(f'<b>[{self.devices_index}]</b>设备将执行屏幕截图操作！')
            logger.info('当前执行了截图操作')
        else:
            self.notice.error('adb未链接，请检查设备T_T~')

    def show_ip_btn_clicked(self):
        if self.con_status():
            key = f'adb -s {self.devices_index} shell am start -a android.intent.action.VIEW -d "https://www.ipaddress.my/?lang=zh_CN"'
            AndroidFunc.subprocess_out(key)
            self.logTextEdit.append(f'<b>[{self.devices_index}]</b>设备将打开ip页面')
            logger.info('当前设备将打开ip页面')
            self.notice.success(
                "IP已在手机上打开对应网页，请确认结果PS:本功能依赖Google功能，适用使用梯子的场景，需要翻墙若国内网未正常显示为正常现象,链接vpn即可")
        else:
            self.notice.error('adb未链接，请检查设备T_T~')

    def net_change_btn_clicked(self):
        if self.con_status():
            key = f'adb -s {self.devices_index} shell svc wifi {self.net_status}'
            AndroidFunc.subprocess_out(key)
            self.logTextEdit.append(f'<b>[{self.devices_index}]</b>设备将更改WiFi的链接状态')
            match self.net_status:
                case 'disable':
                    self.logTextEdit.append(f'<b>[{self.devices_index}]</b>设备的WiFi已经关闭')
                    self.notice.success('当前已关闭网络')
                    self.status.showMessage("当前网络状态：关闭", 5000)
                    self.net_status = 'enable'
                    logger.info('当前已关闭手机wifi网络')
                case 'enable':
                    self.logTextEdit.append(f'<b>[{self.devices_index}]</b>设备的WiFi已经打开')
                    self.notice.success('网络已经重新打开')
                    self.status.showMessage("当前网络状态：打开", 5000)
                    logger.info('当前已打开手机wifi网络')
                    self.net_status = 'disable'
                case _:
                    self.notice.warn("操作异常")
        else:
            self.notice.error('adb未链接，请检查设备T_T~')

    def sign_check_btn_clicked(self):
        self.con_status()
        apk_path = AndroidFunc.get_file_path()
        apk_num = apk_path[0].split('_')[0].split('/')[-1]
        print(apk_num)
        try:
            my_db = AndroidFunc.sql_con(sql_name='data_sql')
            cursor = my_db.cursor()
            sha1_sql = f"""select sha1 from android_game_info where app_id = '{apk_num}'
                                       """
            cursor.execute(sha1_sql)
            sha1 = cursor.fetchone()
            sha256_sql = f"""select sha256 from android_game_info where app_id = '{apk_num}'
                                       """
            cursor.execute(sha256_sql)
            sha256 = cursor.fetchone()
            md5_sql = f"""select md5 from android_game_info where app_id = '{apk_num}'
                                       """
            cursor.execute(md5_sql)
            md5 = cursor.fetchone()
            cursor.close()
            my_db.close()
            if len(sha1[0]) > 2:
                if apk_path[0]:
                    if 'apk' or 'aab' in apk_path[0]:
                        logger.info('当前正进行签名比对操作')
                        apk_sign = ''
                        apk_sha256 = ''
                        apk_md5 = ''
                        key = f'keytool -printcert -jarfile "{apk_path[0]}"'
                        res = AndroidFunc.subprocess_out(key).readlines()
                        for data in res:
                            my_data = str(data)
                            if 'SHA1:' in my_data:
                                apk_sign = my_data.split(' ')[2].replace(r"\n'", '')
                                print('sha1:', sha1[0])
                                print('sha1:', apk_sign)
                            if 'MD5:' in my_data:
                                apk_md5 = my_data.split('  ')[1].replace(r"\n'", '')
                                print('md5:', md5[0])
                                print('md5:', apk_md5)
                            if 'SHA256:' in my_data:
                                apk_sha256 = my_data.split(' ')[2].replace(r"\n'", '')
                                print('sha256:', sha256[0])
                                print('sha256:', apk_sha256)

                        if sha1[0] == apk_sign and apk_sha256 == sha256[0] and md5[0] == apk_md5:
                            self.notice.success('对比显示指纹属性一致^0^~')
                        elif sha1[0] != apk_sign:
                            self.notice.warn('对比显示SHA1不一致=,=')
                        elif apk_md5 != md5:
                            self.notice.warn('对比显示MD5不一致=,=')
                        else:
                            self.notice.warn('对比显示SHA256不一致=,=')
                    else:
                        self.notice.warn("你选择的文件格式有误=,=")
                else:
                    self.notice.warn("您没有选择文件哦0,0~")
            else:
                self.notice.warn('您未备份此app的签名信息哦T_T~~')
        except BaseException as error:
            logger.error(error)

    def clear_screenshot_btn_clicked(self):
        AndroidFunc.get_desktop()
        logger.info('当前正在删除截图')
        if self.img_id == 1:
            while True:
                try:
                    os.remove(f'{AndroidFunc.get_desktop()}//ScImg{self.img_id}.png')
                    self.img_id = self.img_id + 1
                except BaseException as error:
                    logger.error(error)
                    self.notice.success('所有的截图都被清除啦^0^~~')
                    return False
        else:
            while True:
                try:
                    os.remove(f'{AndroidFunc.get_desktop()}//ScImg{(self.img_id - 1)}.png')
                    self.img_id = self.img_id - 1
                except BaseException as error:
                    logger.error(error)
                    self.notice.success('所有的截图都被清除啦^0^~~')
                    return False

    def open_google_link_btn_clicked(self):
        AndroidFunc.adb_status()
        my_data = self.package_name_entry.text()
        devices = self.get_index_value(self.devices_select_combo_box)
        if my_data:
            key = f'adb -s {devices} shell am start -a android.intent.action.VIEW -d "https://play.google.com/store/apps/details?id={my_data}"'
            AndroidFunc.subprocess_single(key)
            self.notice.success('已在手机上打开当前包名关联的google链接')
            self.logTextEdit.append(f'<b>[{devices}]</b>设备已经开打了指定的商店链接')
            logger.info(f'[{devices}]设备已经开打了指定的商店链接')
        else:
            self.notice.error('当前包名关联游戏未在数据库备份')

    def permission_check_btn_clicked(self):
        permission_arr = []
        self.con_status()
        apk_path = AndroidFunc.get_file_path()[0]
        if apk_path and 'apk' in apk_path:
            com = fr'aapt dump badging {apk_path}'
            res = AndroidFunc.subprocess_multiple(com)
            for i in res:
                if 'uses-permission' in str(i):
                    permission_arr.append(
                        i.decode('utf-8').strip().split("=")[1])
            self.msg_box.setIcon(QMessageBox.Information)
            self.msg_box.setWindowTitle("查询结果")
            self.msg_box.setText(f"{str(permission_arr)}")
            self.msg_box.exec_()
            logger.info('当前正在执行权限获取操作')
        else:
            self.notice.error('您未选择文件或文件格式有误')

    def interact_btn_clicked(self):
        if 'interact_window' in self.open_window_list:
            self.status.showMessage('您已经打开了交互面板啦~请不要重复打开....', 5000)
            return
        else:
            self.interact_window = InteractWindow(self)
            self.interact_window.exec_()
            self.open_window_list.remove('interact_window')
            logger.info('打开了interact_window')

    def del_panel_btn_clicked(self):
        if 'DelAccountWindow' in self.open_window_list:
            self.status.showMessage('您已经打开了删除功能界面啦~请不要重复打开....', 5000)
            return
        else:
            self.del_account_window = DelAccountWindow(self)
            self.del_account_window.exec_()
            self.open_window_list.remove('DelAccountWindow')
            logger.info('打开了DelAccountWindow')

    def backup_information_btn_clicked(self):
        if 'BackupInformationWindow' in self.open_window_list:
            self.status.showMessage('您已经打开了备份功能界面啦~请不要重复打开....', 5000)
            return
        else:
            self.backup_info_window = BackupInformationWindow(self)
            self.backup_info_window.exec_()
            self.open_window_list.remove('BackupInformationWindow')
            logger.info('打开了BackupInformationWindow')

    def authorize_window_btn_clicked(self):
        self.authorize_window = AuthorizeWindow(self)
        self.authorize_window.exec_()
        # self.open_window_list.remove('AuthorizeWindow')
        logger.info('打开了BackupInformationWindow')

    def show_account_btn_clicked(self):
        key = 'account'
        self.thread_start(key)
        self.notice.info("已经显示了各提现帐号啦~")

    def ios_panel_btn_clicked(self):
        if self.is_open:
            AndroidFunc.get_file_path()
            self.is_open = 0
        if 'IosWindow' in self.open_window_list:
            self.status.showMessage('您已经打开了IOS功能界面啦~请不要重复打开....', 5000)
            print(self.open_window_list)
            return
        else:
            self.ios_window = IosWindow(self)
            self.ios_window.exec_()
            self.open_window_list.remove('IosWindow')
            logger.info('打开了IosWindow')

    def info_select_clicked(self):
        if self.source_type == 'both' or self.source_type == 'game':
            self.game_select_combo_box.disconnect()
            self.game_select_combo_box.clear()
            self.game_select_combo_box.addItems(AndroidFunc.get_tool_list())
            self.game_select_combo_box.currentIndexChanged.connect(self.game_index_change)
            self.info_select_action.setText('仅显示game源')
            self.source_type = 'tool'
        elif self.source_type == 'tool':
            self.game_select_combo_box.disconnect()
            self.game_select_combo_box.clear()
            self.game_select_combo_box.addItems(AndroidFunc.get_game_list())
            self.game_select_combo_box.currentIndexChanged.connect(self.game_index_change)
            self.info_select_action.setText('仅显示tool源')
            self.source_type = 'game'
        logger.info('切换了信息源')

    def pkg_and_activity_btn_clicked(self):
        key = f'adb -s {self.devices_index} shell dumpsys window | findstr mCurrentFocus'
        self.thread_start(key)
        self.notice.info("已经显示packageName和对应的activity啦~")

    def third_pkg_btn_clicked(self):
        key = f'adb -s {self.devices_index} shell pm list packages -3'
        self.thread_start(key)
        self.notice.info("已经显示所有第三方包名啦~")

    def all_pkg_btn_clicked(self):
        key = f'adb -s {self.devices_index} shell pm list packages'
        self.thread_start(key)
        self.notice.info("已经显示所有包名啦~")
