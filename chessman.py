import sys

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
# 棋子类
class ChessMan(QLabel):
    # color:black\white
    def __init__(self, color='Black', parent=None):
        super(ChessMan, self).__init__(parent)
        self.color = color
        self.pic = None
        # 判断参数，执行相应的棋子图片
        if self.color == 'black':
            self.pic = QPixmap('source/黑子.png')
        else:
            self.pic = QPixmap('source/白子.png')
        # 初始化游戏，默认棋子图片
        self.setPixmap(self.pic)
        # 设置棋子大小
        self.setFixedSize(self.pic.size())
        # 坐标初始化
        self.x = 0
        self.y = 0

    # #通过坐标移动棋子
    # def move(self,a0:QtCore.QPoint):
    #     super().move(a0.x()-15,a0.y()-15)

    # 设置点位
    def setIndex(self, x, y):
        self.x = x
        self.y = y

if __name__ == '__main__':
    import cgitb  # 显示错误信息
    cgitb.enable('text')
    app = QApplication(sys.argv)
    chessman = ChessMan()
    chessman.show()
    chessman.move(QPoint(100, 200))
    sys.exit(app.exec_())