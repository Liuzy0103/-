from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

# 创建第一个窗口
class mainwindow(QMainWindow):
    def __init__(self):
        super(mainwindow, self).__init__()
        # 设置窗口标题
        self.setWindowTitle('这是一个窗口')
        # 设置标签
        labal = QLabel('欢迎使用qt窗口')
        # 将标签显示在窗口中央
        labal.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(labal)
        # 设置大小
        self.resize(600, 500)

        # 创建布局
        layout = QVBoxLayout()
        # 创建按钮
        for i in range(5):
            button = QPushButton(str(i))
            # 绑定槽函数
            button.pressed.connect(lambda x=i:self.mybutton(x))
            # 将按钮添加到布局里面
            layout.addWidget(button)
        # 创建一个部件
        weight = QWidget()
        # 将布局添加到部件里面
        weight.setLayout(layout)
        # 将部件添加到窗口
        self.setCentralWidget(weight)
    # 槽函数
    def mybutton(self,n):
        print(f'这是第{n}个按钮')

# 创建应用实例，通过sys。argv传入命令行参数
app=QApplication(sys.argv)
# 创建窗口
window = mainwindow()
# 显示窗口
window.show()
# 执行应用，进入事件循环
app.exec_()
