"""
增加催促游戏界面

"""
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtMultimedia import QSound

from Mybutton import MyButton
from gameweight import GameWiget
from PyQt5.QtWidgets import QApplication
import sys

class GameWidgetPlus(GameWiget):
    #  自定义催促信号
    urge_clicked = pyqtSignal()
    def __init__(self, parent = None):
        super(GameWidgetPlus, self).__init__(parent)
        #  催促按钮
        self.uyge_btn = MyButton('source/催促按钮_hover.png',
                                 'source/催促按钮_normal.png',
                                 'source/催促按钮_press.png',
                                 parent=self)
        self.uyge_btn.move(650, 500)
        self.uyge_btn.click_signal.connect(self.urge_clicked)
    #  仅为测试
    def urge(self):
        QSound.a = QSound.play('source/cuicu.wav')
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = GameWidgetPlus()
    w.urge_clicked.connect(w.urge)
    w.show()
    sys.exit(app.exec_())