import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from gui.dialog import *
from utils.AndroidFunc import *
from gui.mainWindow import *


# noinspection PyAttributeOutsideInit
class DelAccountWindow(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        main_window_x = parent.pos().x()
        main_window_y = parent.pos().y()
        self.setGeometry(int(main_window_x) + 755, int(main_window_y) + 135, 400, 70)  # 设置窗口大小
        self.setWindowTitle("删号功能面板")
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.parent.open_window_list.append('DelAccountWindow')
        self.game_list = ['A902-com.yalla.bingocash', 'A871-com.yalla.bubbleshooter', 'A918-com.yalla.cashdomino']
        self.notice = Notice()
        self.init_ui()
        self.onclick_listen()

    def init_ui(self):
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox3 = QHBoxLayout()
        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox1)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addLayout(self.hbox3)

        # 第一个水平布局
        self.game_choose_label = QLabel('请选择项目', self)
        self.game_choose_combo_box = QComboBox(self)
        self.game_choose_combo_box.addItems(self.game_list)
        self.game_choose_combo_box.setFixedSize(300, 20)
        self.hbox1.addWidget(self.game_choose_label)
        self.hbox1.addWidget(self.game_choose_combo_box)

        # 第二个水平布局
        self.id_label = QLabel('账号ID', self)
        self.id_entry = QLineEdit(self)
        reg = QRegExp('^[0-9]+$')
        validator = QRegExpValidator(self)  # 正则匹配规则
        validator.setRegExp(reg)
        self.id_entry.setValidator(validator)
        self.del_account_btn = QPushButton('删除账号', self)
        self.hbox2.addWidget(self.id_label)
        self.hbox2.addWidget(self.id_entry)
        self.hbox2.addWidget(self.del_account_btn)

        # 第三个水平布局
        self.organic_label = QLabel('账号ID', self)
        self.organic_entry = QLineEdit(self)
        reg = QRegExp('[0-1]')
        validator = QRegExpValidator(self)  # 正则匹配规则
        validator.setRegExp(reg)
        self.organic_entry.setValidator(validator)
        self.change_organic_btn = QPushButton('修改归属', self)
        self.hbox3.addWidget(self.organic_label)
        self.hbox3.addWidget(self.organic_entry)
        self.hbox3.addWidget(self.change_organic_btn)

        self.setLayout(self.vbox)

        self.show()

    def onclick_listen(self):
        self.game_choose_combo_box.currentIndexChanged.connect(self.on_game_choose_combo_box_changed)
        self.del_account_btn.clicked.connect(self.del_account_btn_clicked)
        self.change_organic_btn.clicked.connect(self.change_organic)

    def on_game_choose_combo_box_changed(self):
        # current_id = self.game_choose_combo_box.currentIndex()
        # current_index = self.game_choose_combo_box.itemText(current_id)
        current_index = self.game_choose_combo_box.currentText()
        return current_index

    def del_account_btn_clicked(self):
        game_id = self.id_entry.text()
        current_choose = self.on_game_choose_combo_box_changed()
        if game_id and len(game_id) == 6:
            match current_choose:
                case 'A902-com.yalla.bingocash':
                    my_db = AndroidFunc.sql_con(sql_name='bingo_sql')
                    cursor = my_db.cursor()
                    sql = f"""DELETE FROM account_t WHERE userid={game_id};
                                                   """
                    cursor.execute(sql)
                    my_db.commit()
                    cursor.close()
                    my_db.close()
                    self.notice.success('删除成功~0v0')
                    logger.info(f'成功删除bingo库内id为：{game_id}的账号')
                case 'A871-com.yalla.bubbleshooter':
                    my_db = AndroidFunc.sql_con(sql_name='bubble_sql')
                    cursor = my_db.cursor()
                    sql = f"""DELETE FROM account_t WHERE userid={game_id};
                                                                           """
                    cursor.execute(sql)
                    my_db.commit()
                    cursor.close()
                    my_db.close()
                    self.notice.success('删除成功~~0v0')
                    logger.info(f'成功删除bubble库内id为：{game_id}的账号')
                case 'A918-com.yalla.cashdomino':
                    my_db = AndroidFunc.sql_con(sql_name='domino_sql')
                    cursor = my_db.cursor()
                    sql = f"""DELETE FROM account_t WHERE userid={game_id};
                                                                                           """
                    cursor.execute(sql)
                    my_db.commit()
                    cursor.close()
                    my_db.close()
                    self.notice.success('删除成功~~0v0')
                    logger.info(f'成功删除domino库内id为：{game_id}的账号')
                case _:
                    logger.error('选择的项目错误，请重试')
        else:
            self.notice.error('您输入的账号不正确T^T')

    def change_organic(self):
        current_choose = self.on_game_choose_combo_box_changed()
        game_id = self.id_entry.text()
        organic = self.organic_entry.text()
        if game_id and organic:
            match current_choose:
                case 'A902-com.yalla.bingocash':
                    my_db = AndroidFunc.sql_con(sql_name='bingo_sql')
                    cursor = my_db.cursor()
                    sql = f"""UPDATE abtest_t SET origin='{organic}' WHERE userid={game_id};
                                                           """
                    cursor.execute(sql)
                    my_db.commit()
                    cursor.close()
                    my_db.close()
                    self.notice.success('修改成功0v0')
                    logger.info(f'成功修改bingo库内id为{game_id}的账号的归属为：{organic}')
                case 'A871-com.yalla.bubbleshooter':
                    my_db = AndroidFunc.sql_con(sql_name='bubble_sql')
                    cursor = my_db.cursor()
                    sql = f"""UPDATE abtest_t SET origin='{organic}' WHERE userid={game_id};
                                                                                   """
                    cursor.execute(sql)
                    my_db.commit()
                    cursor.close()
                    my_db.close()
                    self.notice.success('修改成功~0v0')
                    logger.info(f'成功修改Bubble库内id为{game_id}的账号的归属为：{organic}')
                case 'A918-com.yalla.cashdomino':
                    my_db = AndroidFunc.sql_con(sql_name='domino_sql')
                    cursor = my_db.cursor()
                    sql = f"""UPDATE abtest_t SET origin='{organic}' WHERE userid={game_id};
                                                                           """
                    cursor.execute(sql)
                    my_db.commit()
                    cursor.close()
                    my_db.close()
                    self.notice.success('修改成功0v0')
                    logger.info(f'成功修改domino库内id为{game_id}的账号的归属为：{organic}')
                case _:
                    logger.error('选择的项目错误，请重试')
        else:
            self.notice.error('未填入id或organic ID~T^T')


if __name__ == "__main__":
    pass
