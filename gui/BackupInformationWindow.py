# -*- coding:utf-8 -*-

"""
@Author  :   StrokeH
@env     :   Python 3.11.3
@Time    :   2023/3/20 1:34 PM
@Desc    :   备份功能界面
"""

from gui.mainWindow import *
from PyQt5.QtWidgets import QMessageBox


# noinspection PyAttributeOutsideInit
class BackupInformationWindow(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        main_window_x = parent.pos().x()
        main_window_y = parent.pos().y()
        self.setGeometry(int(main_window_x) + 755, int(main_window_y) + 270, 400, 50)  # 设置窗口大小
        self.setWindowTitle("备份功能面板")
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.parent.open_window_list.append('BackupInformationWindow')
        self.msg_box = QMessageBox()
        self.notice = Notice()
        self.init_ui()
        self.onclick_listen()

    def init_ui(self):
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox3 = QHBoxLayout()
        self.hbox4 = QHBoxLayout()
        self.hbox5 = QHBoxLayout()
        self.hbox6 = QHBoxLayout()
        self.hbox7 = QHBoxLayout()
        self.hbox8 = QHBoxLayout()
        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox3)
        self.vbox.addLayout(self.hbox4)
        self.vbox.addLayout(self.hbox5)
        self.vbox.addLayout(self.hbox6)
        self.vbox.addLayout(self.hbox7)
        self.vbox.addLayout(self.hbox8)

        # 第一个水平布局
        self.info_label = QLabel('项目代号：', self)
        self.id_entry = QLineEdit(self)
        reg = QRegExp('^[A-Z0-9]{4}$')
        validator = QRegExpValidator(self)  # 正则匹配规则
        validator.setRegExp(reg)
        self.id_entry.setValidator(validator)
        self.hbox1.addWidget(self.info_label)
        self.hbox1.addWidget(self.id_entry)

        # 第二个水平布局
        self.package_label = QLabel('游戏包名：', self)
        self.package_entry = QLineEdit(self)
        reg = QRegExp('[0-9A-z.]+$')
        validator = QRegExpValidator(self)  # 正则匹配规则
        validator.setRegExp(reg)
        self.package_entry.setValidator(validator)
        self.hbox2.addWidget(self.package_label)
        self.hbox2.addWidget(self.package_entry)
        # 第三个水平布局
        self.activity_label = QLabel('Activity：', self)
        self.activity_entry = QLineEdit(self)
        reg = QRegExp('[0-9A-z.]+$')
        validator = QRegExpValidator(self)  # 正则匹配规则
        validator.setRegExp(reg)
        self.activity_entry.setValidator(validator)
        self.hbox3.addWidget(self.activity_label)
        self.hbox3.addWidget(self.activity_entry)
        # 第四个水平布局
        self.bug_label = QLabel('Bug 链接：', self)
        self.link_entry = QLineEdit(self)
        self.hbox4.addWidget(self.bug_label)
        self.hbox4.addWidget(self.link_entry)
        # 第五个水平布局
        self.sha1_label = QLabel('项目SHA1：', self)
        self.sha1_entry = QLineEdit(self)
        self.hbox5.addWidget(self.sha1_label)
        self.hbox5.addWidget(self.sha1_entry)
        # 第六个水平布局
        self.sha256_label = QLabel('项目SHA256：', self)
        self.sha256_entry = QLineEdit(self)
        self.hbox6.addWidget(self.sha256_label)
        self.hbox6.addWidget(self.sha256_entry)
        # 第七个水平布局
        self.MD5_label = QLabel('项目 MD5：', self)
        self.MD5_entry = QLineEdit(self)
        self.hbox7.addWidget(self.MD5_label)
        self.hbox7.addWidget(self.MD5_entry)
        # 第八个水平布局
        self.select_btn = QPushButton('查询', self)
        self.create_btn = QPushButton('新增', self)
        self.update_btn = QPushButton('修改', self)
        self.hbox8.addWidget(self.select_btn)
        self.hbox8.addWidget(self.create_btn)
        self.hbox8.addWidget(self.update_btn)

        self.setLayout(self.vbox)

        self.show()

    def onclick_listen(self):
        self.select_btn.clicked.connect(self.select_btn_clicked)
        self.create_btn.clicked.connect(self.create_btn_clicked)
        self.update_btn.clicked.connect(self.update_btn_clicked)

    def select_btn_clicked(self):
        app_id = self.id_entry.text()
        if app_id:
            print(app_id)
            my_db = AndroidFunc.sql_con(sql_name='data_sql')
            cursor = my_db.cursor()
            sql = f"""SELECT * from android_game_info WHERE app_id = '{app_id}'"""
            cursor.execute(sql)
            data = cursor.fetchall()
            if data:
                self.msg_box.setIcon(QMessageBox.Information)
                self.msg_box.setWindowTitle("查询结果")
                self.msg_box.setText(f"{str(data)}")
                self.msg_box.exec_()
            else:
                self.notice.info('无当前ID信息')
            cursor.close()
            my_db.close()

    def create_btn_clicked(self):
        app_id = self.id_entry.text()
        package_name = self.package_entry.text()
        launcher_activity = self.activity_entry.text()
        bug_list = self.link_entry.text()
        sha1 = self.sha1_entry.text()
        sha256 = self.sha256_entry.text()
        md5 = self.MD5_entry.text()
        if app_id and package_name and sha1 and sha256 and md5:
            try:
                my_db = AndroidFunc.sql_con(sql_name='data_sql')
                cursor = my_db.cursor()
                sql = f"""INSERT INTO android_game_info(app_id,package_name,launcher_activity,bugList_link,sha1,md5,sha256) 
                                VALUE ('{app_id}','{package_name}',{launcher_activity},'{bug_list}','{sha1}','{md5}','{sha256}')"""
                cursor.execute(sql)
                my_db.commit()
                cursor.close()
                my_db.close()
                self.notice.success('数据新建成功啦~~')
            except BaseException as error:
                if '1062' in str(error):
                    self.notice.error('您已经备份过此id的数据了T_T~')
                else:
                    self.msg_box.setIcon(QMessageBox.Information)
                    self.msg_box.setWindowTitle("错误反馈")
                    self.msg_box.setText(f"{str(error)}")
                    self.msg_box.exec_()
        else:
            self.notice.warn('您数据没有填写完整T_T~')

    def update_btn_clicked(self):
        app_id = self.id_entry.text()
        package_name = self.package_entry.text()
        launcher_activity = self.activity_entry.text()
        bug_list = self.link_entry.text()
        sha1 = self.sha1_entry.text()
        sha256 = self.sha256_entry.text()
        md5 = self.MD5_entry.text()
        if app_id:
            my_db = AndroidFunc.sql_con(sql_name='data_sql')
            cursor = my_db.cursor()
            sql = f"""SELECT * from android_game_info WHERE app_id = '{app_id}'"""
            cursor.execute(sql)
            data = cursor.fetchone()
            print(data)
            if data:
                if package_name:
                    sql = f"""UPDATE android_game_info SET package_name='{package_name}' WHERE app_id='{app_id}'"""
                    cursor.execute(sql)
                    my_db.commit()
                if launcher_activity:
                    sql = f"""UPDATE android_game_info SET launcher_activity='{launcher_activity}' WHERE app_id='{app_id}'"""
                    cursor.execute(sql)
                    my_db.commit()
                if bug_list:
                    sql = f"""UPDATE android_game_info SET bugList_link='{bug_list}' WHERE app_id='{app_id}'"""
                    cursor.execute(sql)
                    my_db.commit()
                if sha1:
                    sql = f"""UPDATE android_game_info SET sha1='{sha1}' WHERE app_id='{app_id}'"""
                    cursor.execute(sql)
                    my_db.commit()
                if sha256:
                    sql = f"""UPDATE android_game_info SET sha256='{sha256}' WHERE app_id='{app_id}'"""
                    cursor.execute(sql)
                    my_db.commit()
                if md5:
                    sql = f"""UPDATE android_game_info SET md5='{md5}' WHERE app_id='{app_id}'"""
                    cursor.execute(sql)
                    my_db.commit()
                self.msg_box.setIcon(QMessageBox.Information)
                self.msg_box.setWindowTitle("修改结果")
                self.msg_box.setText(f'''
                        packageName→{package_name}
                        bugList_link→{bug_list}
                        SHA1→{sha1}
                        SHA256→{sha256}
                        MD5→{md5}
                        ''')
                self.msg_box.exec_()
            else:
                self.notice.warn('该项目代号还没有备份信息，无法修改O.o！！')
        else:
            self.notice.warn('您未填入项目代号信息O.o！！')


if __name__ == "__main__":
    pass
