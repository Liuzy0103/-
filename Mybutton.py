from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore

class MyButton(QLabel):
    click_signal = pyqtSignal()  # 定义一个信号
    def __init__(self, *args, parent=None):
        # parent是父类窗口
        super(MyButton, self).__init__(parent)
        # 悬浮
        self.hoverpixmap = QPixmap(args[0])  # QPixmap 加载图片
        # 正常
        self.normalpixmap = QPixmap(args[1])
        # 按压
        self.presspixmap = QPixmap(args[2])
        # 鼠标状态 True：按钮上方 False：按钮外面
        self.enterstate = False
        # 默认按钮是正常状态
        self.setPixmap(self.normalpixmap)
        self.setFixedSize(self.normalpixmap.size())

    # 鼠标释放方法
    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent):
        print('鼠标释放')
        if self.enterstate:  # true
            self.setPixmap(self.hoverpixmap)
        else:
            self.setPixmap(self.normalpixmap)
        self.click_signal.emit()  # 发射信号
    # 鼠标按压事件
    def mousePressEvent(self, event):
        print('鼠标按压')
        self.setPixmap(self.presspixmap)
        pass
    # 鼠标进入事件
    def enterEvent(self, a0: QtCore.QEvent):
        print('鼠标进入')
        self.setPixmap(self.hoverpixmap)
        self.enterstate = True
        pass
    # 鼠标离开事件
    def leaveEvent(self, a0: QtCore.QEvent):
        print('鼠标离开')
        self.setPixmap(self.normalpixmap)
        self.enterstate = False
        pass
import sys
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QWidget()
    mybtn = MyButton('source/人机对战_hover.png',
                     'source/人机对战_normal.png',
                     'source/人机对战_press.png',
                     parent=w)
    mybtn.click_signal.connect(w.close)
    w.show()
    sys.exit(app.exec_())