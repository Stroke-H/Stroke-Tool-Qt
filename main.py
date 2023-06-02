# -*- coding:utf-8 -*-

"""
@Author  :   StrokeH
@env     :   Python 3.10.5
@Time    :   2022/8/22 1:34 PM
@Desc    :   安卓主界面入口
"""

from gui.mainWindow import *

if __name__ == "__main__":
    app = QApplication(sys.argv)  # 实例化窗口
    bootstrap_window = MainWindow()  # 引导窗口展示
    sys.exit(app.exec_())  # 遇到退出情况，终止程序
 