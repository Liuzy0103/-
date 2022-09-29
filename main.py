import sys

from MenuWeight import MenuWeidht
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from DoublePlayer import DoublePlayer
from SinglePlayer import SinglePlayer

'''
主控程序
'''
class Main(QObject):
    def __init__(self):
        super(Main, self).__init__()
        # 初始化菜单界面
        self.menu_widget = MenuWeidht()
        # 双人对战
        self.double_player = DoublePlayer()
        self.menu_widget.double_clicked.connect(self.start_double_player)
        # 游戏退出时，展示菜单界面
        self.double_player.exit_clicked.connect(self.menu_widget.show)
        # 人机对战
        self.single_player = SinglePlayer()
        self.menu_widget.single_clicked.connect(self.start_single_player)
        self.single_player.exit_clicked.connect(self.menu_widget.show)

    # 游戏启动方法
    def start_programe(self):
        self.menu_widget.show()
    # 启动双人对战
    def start_double_player(self):
        # 启动游戏界面
        self.double_player.start_game()
        # 隐藏菜单界面
        self.menu_widget.hide()
    # 启动人机对战
    def start_single_player(self):
        self.single_player.start_game()
        self.menu_widget.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.start_programe()
    sys.exit(app.exec_())