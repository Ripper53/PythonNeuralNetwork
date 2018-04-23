class TicTacToe(object):

    def __init__(self):
        self.gameFinished = False
        self.winner = None
        self.board = [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]]

    def print(self):
        for i in range(2, -1, -1):
            print(self.board[i])

    def finished(self):
        return self.gameFinished

    def getWinner(self):
        return self.winner

    def getBoard(self, turnMark):
        board = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == turnMark:
                    board.append(1.0)
                elif self.board[i][j] == 0:
                    board.append(0.0)
                else:
                    board.append(0.5)
        return board

    def addMark(self, mark, x, y):
        if self.board[y][x] == 0:
            self.board[y][x] = mark
            self.checkForWin(mark, x, y)
            return True
        else:
            return False

    def boardFilled(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return False
        self.gameFinished = True
        return True

    def checkForWin(self, mark, x, y):
        if self.horizontalCheck(mark, y) or self.verticalCheck(mark, x) or self.tiltRightCheck(mark) or self.tiltLeftCheck(mark):
            self.winner = mark
            return True
        elif self.boardFilled():
            return True
        else:
            return False

    def horizontalCheck(self, mark, y):
        for i in range(3):
            if self.board[y][i] != mark:
                return False
        self.winner = mark
        self.gameFinished = True
        return True

    def verticalCheck(self, mark, x):
        for i in range(3):
            if self.board[i][x] != mark:
                return False
        self.winner = mark
        self.gameFinished = True
        return True

    def tiltRightCheck(self, mark):
        if self.board[0][0] == mark and self.board[1][1] == mark and self.board[2][2] == mark:
            self.winner = mark
            self.gameFinished = True
            return True
        else:
            return False

    def tiltLeftCheck(self, mark):
        if self.board[0][2] == mark and self.board[1][1] == mark and self.board[2][0] == mark:
            self.winner = mark
            self.gameFinished = True
            return True
        else:
            return False