
class GobangAlgorithm(object):

    def __init__(self, chessboard):
        self.chessboard = chessboard
    # 计算每一个坐标点对应的棋子颜色的分数
    def get_point_score(self, x, y, color):
        '''
        返回每个点的得分
        y:行坐标 垂直
        x:列坐标 水平
        color：棋子颜色
        :return:
        '''
        # 分别计算点周围5子以内，空白、和同色的分数
        blank_score = 0
        color_score = 0

        # 记录该点的每条线的棋子分数
        blank_score_plus = [0, 0, 0, 0]  # 横向 纵向 正斜线 反斜线
        color_score_plus = [0, 0, 0, 0]

        # 横线
        # 右侧
        i = x  # 横坐标
        j = y  # 纵坐标
        while i < 19:
            if self.chessboard[j][i] is None:
                blank_score += 1
                blank_score_plus[0] += 1
                break
            elif self.chessboard[j][i] == color:
                color_score += 1
                color_score_plus[0] += 1
            else:
                break
            if i >= x + 4:
                break
            i += 1
        # print('123123')
        # 左侧
        i = x  # 横坐标
        j = y  # 纵坐标
        while i >= 0:
            if self.chessboard[j][i] is None:
                blank_score += 1
                blank_score_plus[0] += 1
                break
            elif self.chessboard[j][i] == color:
                color_score += 1
                color_score_plus[0] += 1
            else:
                break
            if i <= x - 4:
                break
            i -= 1

        # 竖线
        # 上方
        i = x  # 横坐标
        j = y  # 纵坐标
        while j >= 0:
            if self.chessboard[j][i] is None:
                blank_score += 1
                blank_score_plus[1] += 1
                break
            elif self.chessboard[j][i] == color:
                color_score += 1
                color_score_plus[1] += 1
            else:
                break
            if j <= y - 4:
                break
            j -= 1
        # 竖线
        # 下方
        i = x  # 横坐标
        j = y  # 纵坐标
        while j < 19:
            if self.chessboard[j][i] is None:
                blank_score += 1
                blank_score_plus[1] += 1
                break
            elif self.chessboard[j][i] == color:
                color_score += 1
                color_score_plus[1] += 1
            else:
                break

            if j >= y + 4:  # 最近五个点
                break
            j += 1
        # 正斜线
        # 右上
        i = x
        j = y
        while i < 19 and j >= 0:
            if self.chessboard[j][i] is None:
                blank_score += 1
                blank_score_plus[2] += 1
                break
            elif self.chessboard[j][i] == color:
                color_score += 1
                color_score_plus[2] += 1
            else:
                break

            if i >= x + 4:  # 最近五个点
                break
            i += 1
            j -= 1
        # 左下
        i = x
        j = y
        while j < 19 and i >= 0:
            if self.chessboard[j][i] is None:
                blank_score += 1
                blank_score_plus[2] += 1
                break
            elif self.chessboard[j][i] == color:
                color_score += 1
                color_score_plus[2] += 1
            else:
                break

            if j >= y + 4:  # 最近五个点
                break
            i -= 1
            j += 1
        # 反斜线
        # 左上
        i = x
        j = y
        while i >= 0 and j >= 0:
            if self.chessboard[j][i] is None:
                blank_score += 1
                blank_score_plus[3] += 1
                break
            elif self.chessboard[j][i] == color:
                color_score += 1
                color_score_plus[3] += 1
            else:
                break
            if i <= x - 4:
                break
            i -= 1
            j -= 1
        # 右上
        i = x
        j = y
        while i < 19 and j < 19:
            if self.chessboard[j][i] is None:
                blank_score += 1
                blank_score_plus[3] += 1
                break
            elif self.chessboard[j][i] == color:
                color_score += 1
                color_score_plus[3] += 1
            else:
                break
            if i >= x + 4:
                break
            i += 1
            j += 1

        for k in range(4):
            # 判断每个方向的同色分数如果>=5,同色五子连珠
            if color_score_plus[k] >= 5:
                return 100

        # color_score *= 5
        # 获取指定位置的每条线上的总分(同色分数+空白分数)，返回最大分
        return max([x + y for x, y in zip(color_score_plus, blank_score_plus)])

    # 获取最合适的坐标点返回
    def get_point(self):
        """
        返回落子位置
        :return:
        """
        # 白色棋子每个坐标点的分数
        white_score = [ [ 0 for i in range(19) ] for j in range(19)]
        # 黑色棋子每个坐标点的分数
        black_score = [ [ 0 for i in range(19) ] for j in range(19)]

        """
        [
            [0,3,5,7,....,0],
            [],
            ...
            []
        ]
        [0,3,5,7,....,0,0,3,5,7,....,0....]
        """

        for i in range(19):
            for j in range(19):
                # 判断当前位置上是否有棋子：无棋子：None  黑色棋子：black 白色棋子：white
                if self.chessboard[i][j] != None:
                    continue# 结束本次循环进入下一次循环
                # 模拟落子，获取当前位置的得分
                self.chessboard[i][j] = "white"
                white_score[i][j] = self.get_point_score(j, i, 'white')
                self.chessboard[i][j] = None

                self.chessboard[i][j] = 'black'
                black_score[i][j] = self.get_point_score(j, i, 'black')
                self.chessboard[i][j] = None


        # print('----------------')
        # 将二维坐标转换成一维进行计算
        r_white_score =  []
        r_black_score = []
        for i in white_score:
            r_white_score.extend(i)
            # 列表的扩展:eg:old=[1,2,3]  new=[4,5,6] odl.extend(new)=>[1,2,3,4,5,6]
        for i in black_score:
            r_black_score.extend(i)

        print(r_black_score)  # [0,2,3,4,1,0.........]
        print(r_white_score)  # [1,0,3,8,0,1.........]
        # zip(r_black_score,r_white_score)=>[(0,1),(2,0),(3,3),.....]
        #                   [1,2,3,...,12,...]# 返回分数最大值 元素个数19*19
        # 找到分数最大值                       #   最大值的下标：33  问：这下标对应的是二维列表的第几行第几列
        """
        [
            [0,3,5,7,....,0],# 19
            [],
            ...
            []
        ]
        [0,3,5,7,....,0|,
         0,3,5,7,....,0|
         ....
        ]
                           20 
        33//19 =>行
        下标索引值为20===》20//19=1   20%19=1

        """
        # 棋盘中每个点位置的分数最大值的一维列表 19*19
        score = [max(x, y) for x, y in zip(r_white_score, r_black_score)]

        # 找到分数最大的下标：max(score)：列表中的最大值
        chess_index = score.index(max(score))

        # print(score,'\n',max(score))

        y = chess_index //19
        x = chess_index % 19

        return x, y
