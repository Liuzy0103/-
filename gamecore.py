from PyQt5.QtCore import QObject
'''
游戏核心类
'''

class GameCore(QObject):
    def __init__(self):
        super(GameCore, self).__init__()
        '''
        记录棋盘信息;None无棋子，black黑棋子，white白棋子
        使用列表生成式创建二维列表
        '''
        self.chessboard = [[None for i in range(19)] for j in range(19)]
    # 初始化棋盘信息
    def init_game(self):
        for i in range(19):
            for j in range(19):
                self.chessboard[i][j] = None
    # 是否可以悔棋（消除棋子记录chessman x,y
    def regret(self, x, y):
        # 判断当前位置是否有棋子
        if self.chessboard[x][y] == None:
            return False
        else:
            self.chessboard[x][y] = None
            return True

    # 判断输赢，判断8个的棋子是否为五子连珠
    def judge_win(self, x, y, color):
        """
        :param x: 水平坐标i
        :param y: 垂直坐标j
        :param color:
        :return:
        """
        count = 1
        # 水平方向判断，y值不变，x值发生变化
        # 左边
        i = x-1
        while i >= 0:
            if self.chessboard[y][i]==None or self.chessboard[y][i] != color:
                break
            count += 1
            i -= 1
        # 右边
        i = x+1
        while i <= 18:
            if self.chessboard[y][i]==None or self.chessboard[y][i] != color:
                break
            count += 1
            i += 1
        if count >= 5:
            return color

        # 垂直方向 x不变，y变化
        count = 1
        # 上边
        j = y-1
        while j >= 0:
            if self.chessboard[j][x]==None or self.chessboard[j][x] != color:
                break
            count += 1
            j -= 1
        # 下边
        j = y+1
        while j <= 18:
            if self.chessboard[j][x]==None or self.chessboard[j][x] != color:
                break
            count += 1
            j += 1
        if count >= 5:
            return color

        # 正斜线 右上 x增加y减小     左下x减y加
        count = 1
        # 右上：x加y减
        i = x+1
        j = y-1
        while j >= 0 and i <= 18:
            if self.chessboard[j][i]==None or self.chessboard[j][i] != color:
                break
            count += 1
            i += 1
            j -= 1
        # 左下 x减y增
        i = x-1
        j = y+1
        while i >= 0 and j <= 18:
            if self.chessboard[j][i]==None or self.chessboard[j][i] != color:
                break
            count += 1
            i -= 1
            j += 1
        if count >= 5:
            return color
        # 反斜线： 左上 x减y减   右下x加y加
        count = 1
        i = x-1
        j = y-1
        while i >= 0 and j >= 0:
            if self.chessboard[j][i]==None or self.chessboard[j][i] != color:
                break
            count += 1
            i -= 1
            j -= 1
        # 右下
        i = x+1
        j = y+1
        while i <= 18 and j <= 18:
            if self.chessboard[j][i]==None or self.chessboard[j][i] != color:
                break
            count += 1
            i += 1
            j += 1
        if count >= 5:
            return color


        return 'Down'

    # 落子逻辑
    def down_chessman(self, x, y, color):  # x:水平y:垂直
        if self.chessboard[y][x] is not None:
            return None
        self.chessboard[y][x] = color
        return self.judge_win(x, y, color)

#
if __name__=='__main__':
    gc = GameCore()
    print(gc.down_chessman(1, 1, 'black'))
    print(gc.down_chessman(1, 2, 'black'))
    print(gc.down_chessman(1, 3, 'black'))
    print(gc.down_chessman(1, 4, 'black'))
    print(gc.down_chessman(1, 5, 'black'))

