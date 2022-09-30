"""
联机对战模式的逻辑控制
"""
import sys

from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QApplication, QMessageBox

from gamecore import GameCore
from gamewidgetplus import GameWidgetPlus
from NetConfig import NetConfigWidget, NetClient, NetServer
import json


class NetPlayer(QObject):
    # 自定义信号：退出游戏，返回菜单界面
    exit_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        # 游戏界面
        self.game_widget = GameWidgetPlus()
        # 游戏核心逻辑
        self.game_core = GameCore()
        # 网络配置窗口
        self.net_config = NetConfigWidget()
        # 网络对象
        self.net_object = None
        # 游戏状态
        self.is_active = False
        # 记录位置
        self.history = []
        # 当前局颜色
        self.current_color = 'black'

        # 通过网络配置窗口的按钮点击实现tcp网络客户端或者tcp网络服务器的创建
        self.net_config.config_signal.connect(self.receive_config)

        # 游戏退出
        self.game_widget.goback_signal.connect(self.stop_game)
        # 催促
        self.game_widget.urge_signal.connect(self.urge_game)
        # 开始游戏
        self.game_widget.start_signal.connect(self.start_game)

    # 请求开始游戏
    def start_game(self):
        data = {"msg_type": "start"}
        self.net_object.send(json.dumps(data))

    # 开始游戏
    def realy_start_game(self):
        # 游戏初始化
        self.init_game()
        # 状态改变
        self.is_active = True

    def init_game(self):
        self.history.clear()
        self.current_color = 'black'
        # gamecore核心逻辑上的(chessboard二维列表)初始化
        self.game_core.init_game()
        # 实际游戏界面的初始化
        self.game_widget.reset()

    # 接收网络窗口按钮点击的配置信号
    def receive_config(self, nettype, name, ip, port):
        # 判断网络类型，根据网络类型创建客户端或者服务器
        if nettype == 'client':
            print(1)
            # 创建tcp网络客户端
            self.net_object = NetClient(name, ip, port)
        elif nettype == 'server':
            # 创建tcp网络服务器
            self.net_object = NetServer(name, ip, port)
        else:
            return
        # 显示游戏界面
        self.game_widget.show()
        # 建立连接
        self.net_object.buildConnect()
        # 捕获数据接收信号，绑定槽函数处理信号
        self.net_object.msg_signal.connect(self.parse_data)
        # 隐藏网络配置小窗口
        self.net_config.hide()

    # 处理接收到的数据
    def parse_data(self, data):
        # 客户端和服务器之间额数据传输今年采用json格式
        print("接收到的数据：", data, type(data), json.loads(data))
        # 将json字符串转为对应的数据类型
        msg = json.loads(data)
        # 催促的数据处理
        if msg['msg_type'] == 'urge':
            QSound.play('./source/luozisheng.wav')
        elif msg['msg_type'] == 'start':
            # 接受到请求开始的数据显示询问对话框
            res = QMessageBox.information(self.game_widget, '消息提示',
                                          '对方请求开始游戏，您是否同意',
                                          QMessageBox.Yes | QMessageBox.No)
            # 根据消息框按钮的点击回复对方不同的数据
            if res == QMessageBox.Yes:
                # 同意开始游戏
                self.realy_start_game()
                data = {"msg_type": "response", "results": "yes", "request": "start"}
                self.net_object.send(json.dumps(data))
            else:
                # 不同意
                data = {"msg_type": "response", "results": "no", "request": "start"}
                self.net_object.send(json.dumps(data))
        # 返回信息数据梳理
        elif msg['msg_type'] == 'response':
            if msg['request'] == 'start':
                if msg['results'] == 'yes':
                    self.realy_start_game()
                    # 规定：谁请求开始谁是黑子
                    self.my_color = "black"
                else:
                    QMessageBox.information(self.game_widget, '消息提示', '对方拒绝开始游戏')

    # 催促
    def urge_game(self):
        # 当前窗口播放催促音乐
        QSound.play('./source/cuicu.wav')
        # 给对方发送催促消息，对方窗口播放催促音乐
        # 数据交互格式json：特殊的字符串 "{'name':'zs','age':18}"  "[1,'str',2.3]"
        # {"msg_type":"urge"}
        data = {"msg_type": "urge"}
        # 将字典数据转为json字符串 json.dumps()
        json_data = json.dumps(data)
        print("发送的json：", json_data)
        # 发送数据-》前提是启动了客户端和服务器
        if self.net_config is None:
            return
        self.net_object.send(json_data)

    # 退出游戏
    def stop_game(self):
        # 发射退出游戏信号
        self.exit_clicked.emit()
        # 关闭游戏界面窗口
        self.game_widget.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = NetPlayer()
    # w.game_widget.show()
    w.net_config.show()

    sys.exit(app.exec_())

