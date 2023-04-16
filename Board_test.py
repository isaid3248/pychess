class Board:
    def __init__(self, board, height = 8, width = 8):
        # type board = List[List[String]]
        # type height, width = Int
        self.board = board
        self.height = height
        self.width = width

    def update_square(self, elem, x, y):
        self.board[x][y] = elem

    def change_squares(self, poses):
        # poses = List[pos]
        # pos = (elem, x, y)
        for elem, x, y in poses:
            self.update_square(elem, x, y)


    def update_board(self, board):

        for i in len(board):
            for j in len(board):
                elem = board[i][j]
                if(elem!= self.board[i][j]):
                   self._update_square(i, j, elem)

    def __str__(self):
        return self.board


