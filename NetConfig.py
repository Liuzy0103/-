"""
配置网络连接，设置姓名、IP、端口、服务器或客户端模式
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, QObject
import socket
import threading

# 网络配置窗口
class NetConfigWidget(QWidget):
    # 定义退出自定义信号
    exit_signal = pyqtSignal()
    # 定义点击确认按钮的自定义配置信号:我是主机：'server'  连接主机：'client'
    config_signal = pyqtSignal(str,str,str,str)# 类型  姓名  ip 端口

    def __init__(self,parent=None):
        super().__init__(parent)
        # 绘制界面
        self.innitUI()

    def innitUI(self):
        # 设置窗口标题
        self.setWindowTitle("网络配置")

        # 构建控件：玩家姓名
        self.name_label = QLabel("姓名：",self)
        self.name_input = QLineEdit("玩家1",self)

        # 构建控件：ip
        self.ip_label = QLabel("IP：", self)
        self.ip_input = QLineEdit("127.0.0.1", self)

        # 构建控件：port
        self.port_label = QLabel("端口：", self)
        self.port_input = QLineEdit("8888", self)

        #构建控件
        self.client_button = QPushButton("连接主机",self)
        self.server_button = QPushButton("我是主机",self)

        # 表(网)格布局：QGridelayout()
        gridlayout = QGridLayout()
        gridlayout.addWidget(self.name_label,0,0)
        gridlayout.addWidget(self.name_input,0,1)
        gridlayout.addWidget(self.ip_label,1,0)
        gridlayout.addWidget(self.ip_input,1,1)
        gridlayout.addWidget(self.port_label, 2, 0)
        gridlayout.addWidget(self.port_input, 2, 1)
        gridlayout.addWidget(self.client_button, 3, 0)
        gridlayout.addWidget(self.server_button, 3, 1)
        self.setLayout(gridlayout)# 设置窗口布局

        # 点击按钮发射信号:传递不同参数
        self.client_button.clicked.connect(self.client_btn_func)
        self.server_button.clicked.connect(self.server_btn_func)

    def client_btn_func(self):
        self.config_signal.emit('client',self.name_input.text(),
                                self.ip_input.text(),self.port_input.text())

    def server_btn_func(self):
        self.config_signal.emit('server', self.name_input.text(),
                                self.ip_input.text(), self.port_input.text())

    def closeEvent(self, QCloseEvent):
        print("点击关闭了。。。。")
        self.close()
        # 发射退出信号
        # 发射关闭窗口信号，后期用于信号处理(关闭窗口显示菜单界面)
        self.exit_signal.emit()


# 启动TCP网络服务器，接受客户端连接，进行数据传输
class NetServer(QObject):
    # 自定义信号
    msg_signal = pyqtSignal(str)

    def __init__(self,name,ip,port):
        super().__init__()
        self.cli_sockert = None
        self.name = name # ?
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # 建立网络连接
    def buildConnect(self):
        self.socket.bind(('',int(self.port)))
        self.socket.listen(1)
        # 使用线程-复习
        sthread = threading.Thread(target=self.accept_connect)
        sthread.start()

    # 等待客户端连接，进行数据传输
    def accept_connect(self):
        try:
            self.cli_sockert,cli_addr = self.socket.accept()
        except Exception as e:
            print("异常：",e)

        while True:
            try:
                data = self.cli_sockert.recv(4094).decode()
                # 每次接受导数据都要发射信号，携带数据
                self.msg_signal.emit(data)
            except Exception as e:
                print(e)
                return

    # 发送数据
    def send(self,data):
        # 判断是否有客户端的连接
        if self.cli_sockert is None:
            return
        # 发送数据
        self.cli_sockert.send(data.encode())

    def close(self):
        self.socket.close()


# TCP网络客户端，连接服务器，进行数据传输
class NetClient(QObject):
    """
    信号：msg_signal(str)：接受到数据要进行数据的处理，所以要有对应的信号去绑定函数去处理对应的数据
    方法：
    | buildConnect | 无       | 无   | 建立网络连接 |
    | ------------- | -------- | ---- | ------------ |
    | send          | data:str | 无   | 发送数据     |
    | recv          | 无       | 无   | 接收网络数据 |
    | close         | 无       | 无   | 关闭网络连接 |
    """
    # 自定义信号
    msg_signal = pyqtSignal(str)

    def __init__(self,name,ip,port):
        # 显示调用父类构造函数(初始化方法)
        # 构造函数：(初始化方法)__init__()
        # 析构函数：__del__()
        # 定义和区别：
        super().__init__()
        self.name = name
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # 建立网络连接,连接服务器
    def buildConnect(self):
        self.socket.connect((self.ip,int(self.port)))
        # 启动线程去接受数据
        threading.Thread(target=self.recv).start()


    # 接受数据
    def recv(self):
        while True:
            try:
                # 接受数据
                data = self.socket.recv(4096).decode()
                # 发射信号
                self.msg_signal.emit(data)
            except Exception as e:
                print(e)
                return

    # 发送数据
    def send(self,data):
        # data是字符串
        self.socket.send(data.encode())

    def close(self):
        self.socket.close()






import sys
if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = NetConfigWidget()
    w.show()

    sys.exit(app.exec_())







