import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Mybutton import MyButton
from chessman import ChessMan
from PyQt5 import QtGui, QtCore
from PyQt5.QtMultimedia import QSound
'''
游戏界面类
'''
class GameWiget(QWidget):
    # 定义信号
    goback_clicked = pyqtSignal()
    start_clicked = pyqtSignal()
    regret_clicked = pyqtSignal()
    lose_clicked = pyqtSignal()
    # 鼠标点击触发棋子落子的信号，带参数的信号 ，坐标值，行和列
    position_clicked = pyqtSignal(tuple)
    def __init__(self, parent=None):
        super(GameWiget, self).__init__(parent)
        self.initui()
        # 用于存储棋子对象，目的实现悔棋，重新开始，棋子对象的记录
        self.chessman_list = []
        # 定义一个显示输赢状态的label
        self.winlable = QLabel(self)
        self.winlable.hide()
        # 定义一个棋子标识的lable
        self.focus = QLabel(self)
        self.focus.setPixmap(QPixmap('source/标识.png'))
        self.focus.setFixedSize(30, 30)
        self.focus.hide()
    # 界面绘制方法
    def initui(self):
        # 设置窗口标题
        self.setWindowTitle('五子棋游戏')
        # 设置窗口图标
        self.setWindowIcon(QIcon('source/五子棋界面.png'))
        # 设置窗口的大小，为图片的大小
        self.setFixedSize(QImage('source/游戏界面.png').size())
        # 设置背景
        # 获取当前界面调色板
        p = QPalette(self.palette())
        brush = QBrush(QImage('source/游戏界面.png'))
        # 设置调色板
        p.setBrush(QPalette.Background, brush)
        # 给窗口添加调色板
        self.setPalette(p)
        # 构造控件
        # ------------------------------------------------------------
        # 返回按钮
        self.goback_button = MyButton('source/返回按钮_hover.png',
                                      'source/返回按钮_normal.png',
                                      'source/返回按钮_press.png',
                                      parent=self)
        self.goback_button.move(660, 100)
        self.goback_button.show()
        # 连接信号与槽
        self.goback_button.click_signal.connect(self.goback_clicked)
        # ------------------------------------------------------------
        # 开始按钮
        self.start_button = MyButton('source/开始按钮_hover.png',
                                     'source/开始按钮_normal.png',
                                     'source/开始按钮_press.png',
                                     parent=self)
        self.start_button.move(650, 200)
        self.start_button.show()
        # 连接信号与槽
        self.start_button.click_signal.connect(self.start_clicked)
        # ------------------------------------------------------------
        # 悔棋按钮
        self.regret_button = MyButton('source/悔棋按钮_hover.png',
                                      'source/悔棋按钮_normal.png',
                                      'source/悔棋按钮_press.png',
                                      parent=self)
        self.regret_button.move(650, 300)
        self.regret_button.show()
        # 连接信号与槽
        self.regret_button.click_signal.connect(self.regret_clicked)
        # ------------------------------------------------------------
        # 认输按钮
        self.lose_button = MyButton('source/认输按钮_hover.png',
                                    'source/认输按钮_normal.png',
                                    'source/认输按钮_press.png',
                                    parent=self)
        self.lose_button.move(650, 400)
        self.lose_button.show()
        # 连接信号与槽
        self.lose_button.click_signal.connect(self.lose_clicked)

    # 重新开始功能，回复棋盘状态
    def reset(self):
        # 清空棋子标识
        self.focus.hide()
        # 清空输赢显示
        self.winlable.hide()
        # 将界面中每个棋子都关闭
        for chessman in self.chessman_list:
            chessman.close()
            del chessman
        # 恢复棋盘状态
        self.chessman_list.clear()
    # 悔棋
    def goback(self):
        if len(self.chessman_list) > 0:
            # 删除列表中最后一个元素
            chessman = self.chessman_list.pop()
            chessman.close()  # 关闭棋子在界面显示
        # 清空棋子标识
        self.focus.hide()

    # 显示游戏赢得状态
    def show_win(self, color):
        if color == 'black':
            # 黑棋胜利图片显示
            self.winlable.setPixmap(QPixmap('source/黑棋胜利.png'))
            self.winlable.show()
            self.winlable.move(100, 100)
            # 图片在窗口最上层显示
            self.winlable.raise_()
        else:
            # 白棋胜利图片显示
            self.winlable.setPixmap(QPixmap('source/白棋胜利.png'))
            self.winlable.show()
            self.winlable.move(100, 100)
            # 图片在窗口最上层显示
            self.winlable.raise_()

    # 获取鼠标点击坐标，鼠标释放事件
    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        # 鼠标点击窗口的位置坐标
        print('鼠标点击的坐标值', a0.x(), a0.y())
        # 调用reverse_to_position方法返回棋盘落子位置
        position = self.reverse_to_position(coordinate=a0)
        print('棋盘交点位置为', position)
        # 发射落子信号
        if position is None:
            return
        else:
            self.position_clicked.emit(position)



    # 将鼠标点击坐标转化为棋盘交点坐标
    def reverse_to_position(self, coordinate):
        coor_x = coordinate.x()
        coor_y = coordinate.y()
        # 首先判断鼠标位置是否有效，如果无效返回None
        """
        根据棋盘尺寸对落子位置分析
        棋盘上边界y：50-15=35
        棋盘下边界y：50+18*30+15=605
        棋盘左边界x: 50-15=35 
        棋盘右边界x: 50+18*30+15=605
        """
        if coor_x <= 35 or coor_x >= 605 or coor_y <= 35 or coor_y >= 605:
            return None
        # 点击坐标转化为位置坐标
        pos_x = (coor_x-35)//30
        pos_y = (coor_y-35)//30
        return (pos_x, pos_y)

    # 将棋盘交点坐标转化为落子坐标
    def reverse_to_coordinate(self, position):
        # (0,0)=>(50,50)
        # 落子坐标=坐标原点+30*交点坐标
        x = 50+30*position[0]
        y = 50+30*position[1]
        return (x, y)


    # 落子position参数为交点位置
    def down_chess(self, position, color):
        print('执行触发落子')
        # 构建棋子对象
        chessman = ChessMan(color, self)
        # 确定棋子落子的位置，鼠标点击窗口的位置坐标
        coorx, coory = self.reverse_to_coordinate(position)
        # 设置棋子位置,将棋子中心落在棋盘交点
        chessman.move(coorx-15, coory-15)
        # 记录棋子对象的交点坐标位置，增加新的xy实例化属性
        chessman.x = position[0]
        chessman.y = position[1]
        # 将新的棋子对象加入到棋子列表里面
        self.chessman_list.append(chessman)
        # 展示棋子
        chessman.show()
        # 添加落子声音
        QSound.play('source/luozisheng.wav')
        # 显示最新的落子标识
        self.focus.move(coorx-15, coory-15)
        self.focus.show()
        self.focus.raise_()

# 以下函数均为测试
def functest():
    print('start......')
# 只有逻辑，没有页面
class Test(QObject):
    def __init__(self, w):
        super(Test, self).__init__()
        self.w = w
    def testdown(self, data):
        print(data)
        # 实现落子
        w.down_chess(data, 'Black')
if __name__=='__main__':
    app = QApplication(sys.argv)

    w = GameWiget()
    # 测试开始按钮
    w.show()
    w.start_clicked.connect(functest)
    # #测试输赢显示
    # w.show_win('black')
    # 测试落子
    # w.down_chess((3,3),'Black')
    # w.down_chess((0,0),'white')
    # w.goback()
    # w.reset()
    # 测试落子 ，通过鼠标点击坐标。返回落子位置，发送文章点击信号
    w.start_clicked.connect(w.reset)
    test_obj = Test(w)
    w.position_clicked.connect(test_obj.testdown)

    sys.exit(app.exec_())