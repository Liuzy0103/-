#联机对战类
from PyQt5.QtCore import * # pyqtSignal
from gamecore import GameCore
from gamewidgetplus import GameWidgetPlus
from NetConfig import NetConfigWidget, NetClient, NetServer
import json
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QMessageBox


class NetPlayer(QObject):

    exit_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.game_widget = GameWidgetPlus()
        self.game_core = GameCore()
        self.net_config = NetConfigWidget()
        self.net_object = None

        self.m_color = 'Black'
        self.is_active = False
        self.history = []

        self.game_widget.start_clicked.connect(self.restart_game)
        self.game_widget.goback_clicked.connect(self.stop_game)
        self.game_widget.position_clicked.connect(self.down_chess)
        self.game_widget.lose_clicked.connect(self.lose_game)
        self.game_widget.regret_clicked.connect(self.regret_game)
        self.game_widget.urge_clicked.connect(self.urge)

        self.net_config.config_signal.connect(self.receive_config)
        self.net_config.exit_signal.connect(self.exit_clicked)

    def urge(self):
        QSound.play('source/cuicu.wav')
        msg = {}
        msg['msg_type'] = 'urge'
        self.net_object.send(json.dumps(msg))

    @staticmethod
    def get_reverse_color(color):
        if color == 'Black':
            return 'White'
        else:
            return 'Black'

    def switch_color(self):
        self.current_color = self.get_reverse_color(self.current_color)

    def stop_game(self):
        self.exit_clicked.emit()
        self.game_widget.close()

        # print('stop game')
        # 删除网络对象
        # print(type(self.net_object))
        self.net_object.close() # 需要先关删除
        del self.net_object
        self.net_object = None

    def start_game(self):
        self.net_config.show()
    # 接受配置信息进行网络对象创建
    def receive_config(self, nettype, name, ip, port):
        if nettype == 'client':
            self.net_object = NetClient(name, ip, port)
        elif nettype == 'server':
            self.net_object = NetServer(name, ip, port)
        else:
            return

        self.game_widget.show()
        self.net_object.buildConnect()
        self.net_object.msg_signal.connect(self.parse_data)
        self.net_config.hide()

    def _start_game(self):
        self.init_game()
        self.is_active = True

    def restart_game(self):
        msg = {}
        msg['msg_type'] = 'restart'
        self.net_object.send(json.dumps(msg))

    def init_game(self):
        self.current_color = 'Black'
        self.history.clear()
        self.game_core.init_game()
        self.game_widget.reset()

    def down_chess(self, position):

        if not self.is_active:
            return

        if self.m_color != self.current_color:
            return

        result = self.game_core.down_chessman(position[0], position[1], self.current_color)
        if result is None:
            return

        self.game_widget.down_chess(position, self.current_color)
        self.history.append(position)
        self.switch_color()
        # print('result:', result)
        if result != 'Down':
            self.game_win(result)

        # 发送落子消息
        msg = {}
        msg['msg_type'] = 'position'
        msg['x'] = position[0]
        msg['y'] = position[1]
        msg['color'] = self.current_color
        self.net_object.send(json.dumps(msg))

    def _down_chess(self, position):
        # print(position)
        if not self.is_active:
            return

        result = self.game_core.down_chessman(position[0], position[1], self.current_color)
        if result is None:
            return

        self.game_widget.down_chess(position, self.current_color)
        self.history.append(position)
        self.switch_color()
        # print('result:', result)
        if result != 'Down':
            self.game_win(result)
            return

    def game_win(self, color):
        self.game_widget.show_win(color)
        self.is_active = False

    def lose_game(self):
        self.game_win(self.get_reverse_color(self.m_color))
        msg = {}
        msg['msg_type'] = 'lose'
        self.net_object.send(json.dumps(msg))

    def regret_game(self):
        if not self.is_active:
            return
        if len(self.history) <= 1:
            return

        # 仅当前回合才能悔棋
        if self.m_color != self.current_color:
            QMessageBox.warning(self.game_widget, '五子棋-消息提示','不是你的回合，不能悔棋')
            return

        msg = {}
        msg['msg_type'] = 'regret'
        self.net_object.send(json.dumps(msg))

    def _regret_game(self):
        if not self.is_active:
            return
        if len(self.history) <= 1:
            return
        # 单人悔棋两个子
        if not self.game_core.regret(*self.history.pop()):
            return
        self.game_widget.goback()

        if not self.game_core.regret(*self.history.pop()):
            return
        self.game_widget.goback()

    def parse_data(self, data):
        print('parseData:',data)
        try:
            msg = json.loads(data)
        except Exception as e:
            print(e)
            return
        # print('msg:',msg)
        # print('type(msg)',type(msg))
        if msg['msg_type'] == "position":
            self._down_chess((int(msg['x']), int(msg['y'])))
        elif msg['msg_type'] == "restart":
            result = QMessageBox.information(self.game_widget, '五子棋-消息提示',
                                    '对方请求开始游戏',
                                    QMessageBox.Yes | QMessageBox.No)
            if result == QMessageBox.Yes:
                # 我开始游戏
                self._start_game()
                self.m_color = 'White'
                msg = {}
                msg['msg_type'] = 'response'
                msg['action_type'] = 'restart'
                msg['action_result'] = 'yes'
                self.net_object.send(json.dumps(msg))
            else:
                msg = {}
                msg['msg_type'] = 'response'
                msg['action_type'] = 'restart'
                msg['action_result'] = 'no'
                self.net_object.send(json.dumps(msg))
        elif msg['msg_type'] == 'response':
            if msg['action_type'] == 'restart':
                if msg['action_result'] == 'yes':
                    self._start_game()
                    self.m_color = 'Black'
                else:
                    QMessageBox.information(self.game_widget, '五子棋-消息提示'
                                            ,'对方拒绝开始游戏')
            elif msg['action_type'] == 'regret':
                if msg['action_result'] == 'yes':
                    self._regret_game()
                else:
                    QMessageBox.information(self.game_widget, '五子棋-消息提示',
                                            '对方拒绝悔棋')

        elif msg['msg_type'] == 'regret':
            result = QMessageBox.information(self.game_widget, '五子棋-消息提示',
                                    '对方请求悔棋',
                                    QMessageBox.Yes | QMessageBox.No)
            if result == QMessageBox.Yes:
                msg = {}
                msg['msg_type'] = 'response'
                msg['action_type'] = 'regret'
                msg['action_result'] = 'yes'
                self.net_object.send(json.dumps(msg))
                self._regret_game()
            else:
                msg = {}
                msg['msg_type'] = 'response'
                msg['action_type'] = 'regret'
                msg['action_result'] = 'no'
                self.net_object.send(json.dumps(msg))

        elif msg['msg_type'] == 'lose':
            self.game_win(self.m_color)
        elif msg['msg_type'] == 'urge':
            QSound.play('source/cuicu.wav')








