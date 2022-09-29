import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Mybutton import MyButton
# 创建游戏窗口
class MenuWeidht(QWidget):
    # 创建信号
    single_clicked = pyqtSignal()
    double_clicked = pyqtSignal()
    network_clicked = pyqtSignal()
    def __init__(self, parent=None):
        super(MenuWeidht, self).__init__(parent)
        self.initUi()
    def initUi(self):
        # 设置窗口的大小
        self.setFixedSize(760, 650)
        # 设置标题
        self.setWindowTitle('五子棋游戏')
        # 设置窗口图标
        self.setWindowIcon(QIcon('source/五子棋界面.png'))
        # 设置窗口背景
        # 获取当前界面调色板
        p = QPalette(self.palette())
        brush = QBrush(QImage('source/五子棋界面.png'))
        # 设置调色板
        p.setBrush(QPalette.Background, brush)
        # 给窗口添加调色板
        self.setPalette(p)

        # ----------------------------------
        # 创建按钮控件
        # ------------------------------------------------------------
        # 人机对战按钮
        self.single_button = MyButton('source/人机对战_hover.png',
                                      'source/人机对战_normal.png',
                                      'source/人机对战_press.png',
                                      parent=self)
        self.single_button.move(250, 300)
        self.single_button.show()
        # 连接信号与槽
        self.single_button.click_signal.connect(self.single_clicked)
        # 网络对战按钮
        # -----------------------------------------------------------
        self.network_button = MyButton('source/联机对战_hover.png',
                                       'source/联机对战_normal.png',
                                       'source/联机对战_press.png',
                                       parent=self)
        self.network_button.move(250, 400)
        self.network_button.show()
        # 连接信号与槽
        self.network_button.click_signal.connect(self.network_clicked)
        # 双人对战按钮
        # -----------------------------------------------------------------
        self.double_button = MyButton('source/双人对战_hover.png',
                                      'source/双人对战_normal.png',
                                      'source/双人对战_press.png',
                                      parent=self)
        self.double_button.move(250, 500)
        self.double_button.show()
        # 连接信号与槽
        self.double_button.click_signal.connect(self.double_clicked)


# 程序入口
if __name__ == '__main__':

    # 创建应用实例
    app = QApplication(sys.argv)
    w = MenuWeidht()
    w.show()
    l = QLabel('已经被点击')
    # 测试连接槽函数，打开窗口
    w.single_clicked.connect(l.show)
    sys.exit(app.exec_())