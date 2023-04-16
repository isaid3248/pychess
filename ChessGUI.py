# In this file we will try to implement moveLog on 8x8 chess board.


# Settings: ------------------------------------------------------------------------------------------------
import PySimpleGUI as pg
import os
import sys

IMAGE_PATH = "./images"
IMAGE_PATH = "D:\codes\Python Projects\ChessPython\images"
print(IMAGE_PATH)
pawnB = os.path.join(IMAGE_PATH, "bp.png")
pawnW = os.path.join(IMAGE_PATH, "wp.png")
knightB = os.path.join(IMAGE_PATH, "bN.png")
knightW = os.path.join(IMAGE_PATH, "wN.png")
bishopB = os.path.join(IMAGE_PATH, "bB.png")
bishopW = os.path.join(IMAGE_PATH, "wB.png")
rookW = os.path.join(IMAGE_PATH, "wR.png")
rookB = os.path.join(IMAGE_PATH, "bR.png")
queenW = os.path.join(IMAGE_PATH, "wQ.png")
queenB = os.path.join(IMAGE_PATH, "bQ.png")
kingB = os.path.join(IMAGE_PATH, "bK.png")
kingW = os.path.join(IMAGE_PATH, "wK.png")
amazonB = os.path.join(IMAGE_PATH, "bA.png")
amazonW = os.path.join(IMAGE_PATH, "wA.png")
blank = os.path.join(IMAGE_PATH, "blank.png")

class ChessGUI:# first character is piece lower, the second character is color upper.
    
    def __init__(self):
        self.pieces = {"pB": pawnB, "rB": rookB, "bB": bishopB, "nB": knightB, "qB": queenB, "aB": amazonB, "kB": kingB,
                "pW": pawnW, "rW": rookW, "bW": bishopW, "nW": knightW, "qW": queenW, "aW": amazonW, "kW": kingW,
                "": blank}

        self.chess_notation = {"p": "", "q": "Q", "r": "R", "n": "N", "b": "B", "a": "A", "k": "K"}
        # -----------------------------------------------------------------------------------------------------------------------
        """IT IS OUR DEFAULT BOARD 8X8."""

        self.default_board = [["rB", "nB", "bB", "qB", "kB", "bB", "nB", "rB"],
                        ["pB", "pB", "pB", "pB", "pB", "pB", "pB", "pB"],
                        ["", "", "", "", "", "", "", ""],
                        ["", "", "", "", "", "", "", ""],
                        ["", "", "", "", "", "", "", ""],
                        ["", "", "", "", "", "", "", ""],
                        ["pW", "pW", "pW", "pW", "pW", "pW", "pW", "pW"],
                        ["rW", "nW", "bW", "qW", "kW", "bW", "nW", "rW"]]

        # Layout is a list element with 2 dimensions.
        # It contains the objects for the window.

        self.layout = [[], []]
        self.columnA = []
        self.columnB = []
        self.colors = ["white", "gray"]
        self.columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self.rows_reverse = [7, 6, 5, 4, 3, 2, 1, 0]
        
    
    def validMove(self, piece1, piece2, board):
        return piece2 == "" or piece1[1] != piece2[1]
    
    def drawMenuBar(self):
        self.menu_def = [['File', ['New Game', 'New analysis', 'Open a pgn file', 'Save the game', 'Exit']],
                ['Controls', ['Undo', 'Redo', 'Go to the beginning'], ], ['Analysis', ['Run Engine', 'Opening Book'], ],
                ['Help', 'Hint'], ]

        self.layout[0].append(pg.Menu(self.menu_def))

    # ----------------------------------------------------------------------------------------------------------------------

    """We will implement this function later entirely. for now it will only check if given two pieces have the same
    color """


    


    # function that updates one square at a time
    def putPiece(self, pos, piece):
        # pos   = (Int, Int)
        # piece = String
        self.window[pos].update(image_filename=self.pieces[piece])
        self.window[pos].metadata = piece
        self.board[pos[0]][pos[1]] = piece


    # Function that updates normally two squares at the same time.
    def makeMove(self, move, reverse=False):
        piece = move[0]
        target = ""
        cf = move[2]
        gt = move[3]

        if reverse:
            gt, cf = cf, gt
            target = move[1]

        self.putPiece(cf, target)
        self.putPiece(gt, piece)

        # MAKE MOVE
        # window[move[2]].update(image_filename=blank)
        # window[move[2]].metadata = ""
        # window[move[3]].metadata = selectedPiece
        # window[move[3]].update(image_filename=pieces[selectedPiece])
        # # UNDO MOVE
        # window[move[2]].update(image_filename=pieces[moveToBeReversed[0]])
        # window[move[2]].metadata = moveToBeReversed[0]
        # window[move[3]].update(image_filename=pieces[moveToBeReversed[1]])
        # window[move[3]].metadata = moveToBeReversed[1]
        # # REDO MOVE
        # window[move[2]].update(image_filename=blank)
        # window[move[2]].metadata = ""
        # window[move[3]].update(image_filename=pieces[moveToBePlayed[0]])
        # window[move[3]].metadata = moveToBePlayed[0]


    # old one :def turnIntoNotation(piece, comesFrom, goesTo):
    # move = (piece, target,  comesFrom, goesTo)
    def turnIntoNotation(self, move):
        piece = move[0]
        target = move[1]
        comesFrom = move[2]
        goesTo = move[3]
        eaten = ""
        refColumn = ""

        # window[goesTo].metadata must also be included in the list.
        if target != "":
            eaten = "x"

        if piece[0] == "p" and eaten == "x":
            refColumn = self.columns[comesFrom[1]]

        return refColumn + self.chess_notation[piece[0]] + eaten + "{}{}".format(self.columns[goesTo[1]], self.rows_reverse[goesTo[0] - 1])


    def changeButton(self, key, background, color, metadata, image):
        self.window[key].update(background_color=background)


    


    def initialize_board(self, board):
        # We store the location as tuple (column, row)
        resolution = 520
        colors = ["white", "gray"]
        for row in range(len(board)):
            current_row = []
            for column in range(len(board[row])):
                color = colors[(row + column) % 2]
                current_row.append(pg.Button(pad=(0, 0), image_filename=self.pieces[self.default_board[row][column]],
                                            button_color=color, mouseover_colors=color, key=(row, column),
                                            metadata=self.default_board[row][column]))
            self.columnA.append(current_row)
        self.layout[0].append(pg.Column(self.columnA, scrollable=False, element_justification="right", size=(resolution, resolution)))
        


    def drawMoveLog(self):
        # moves will be self.moves when we turn everything into class.
        self.columnB.append([pg.Listbox([], size=(30, 15), background_color="white", highlight_background_color="white",
                                highlight_text_color="black", text_color="black", key="Move-Log")])
        self.layout[0].append(
            pg.Column(self.columnB, scrollable=False, element_justification="left", vertical_alignment="top", pad=(0, 1)))


    def drawUndoButton(self):
        self.layout[1].append(pg.Button(button_text="Undo Move", size=(12, 2),
                                pad=(1, 1), mouseover_colors=("gray", "gray"),
                                button_color="gray"
                                , key="Undo", metadata=""))


    def drawRedoButton(self):
        self.layout[1].append(pg.Button(button_text="Redo Move", size=(12, 2), target=(0, 0),
                                pad=(1, 1), mouseover_colors=("gray", "gray"),
                                button_color="gray"
                                , key="Redo", metadata=""))


    def drawGUI(self):
        self.initialize_board(self.default_board)
        self.drawMenuBar()
        self.drawMoveLog()
        self.drawUndoButton()
        self.drawRedoButton()

    def run(self):
        self.drawGUI()
        self.window = pg.Window("Python Chess", self.layout)

    
        # Settings ---------------------------------------------------------------------------------------------------------

        started_Undoing_Moves = False
        moveLogNotation = []
        moveLog = []
        click = 0
        selectedPiece = ""
        whiteToMove = True
        countMoves = 0  # len(moveLog)
        movesPlayed = 0  # len(moveLogNotation)
        rewinded_Moves_Stack_Notation = []
        rewinded_Moves_Stack = []
        self.board = self.default_board

        # These will be used in the future.
        # kingOnCheck = False
        # pieceCaptured = False

    # -------------------------------------------------------------------------------------------------------------------

        while True:
            event, values = self.window.read()

            if event == pg.WIN_CLOSED or event == "Leave" or event == "Exit":
                break

            if event == "Go to the beginning":
                while len(moveLog) > 0:
                    if len(moveLog) == 0:
                        continue

                    if whiteToMove:
                        countMoves -= 1
                        rewinded_Moves_Stack_Notation.append(
                            moveLogNotation.pop())  # moveLogNotation + rewindedMovesQuery = current game recorded to date.
                        self.window["Move-Log"].update(moveLogNotation)  # update Move Log Listbox

                    moveToBeReversed = moveLog.pop()  # removes the last element
                    rewinded_Moves_Stack.append(moveToBeReversed)
                    movesPlayed -= 1

                    # condition when to de-select when you selected a square.
                    if click == 1:
                        self.window[previousEvent].update(button_color=self.colors[(previousEvent[0] + previousEvent[1]) % 2])
                        click = 0

                    self.makeMove(moveToBeReversed, reverse=True)

                    started_Undoing_Moves = True  # Important flag variable for redoing Moves..
                    whiteToMove = not whiteToMove  # don't forget to change the turns.

                    print(moveLog)
                countMoves = 0
                event, values = self.window.read()

            # take the clicked button element.
            piece = self.window[event]

            # check if the piece with the specific color can execute a move.
            # First click checks, if clicked button contains a piece, then a move can be executed.
            # Also check if the selected color has the moving turn.

            if event == "Undo":
                # skip this condition if moveLog is empty
                if len(moveLog) == 0:
                    continue

                if whiteToMove:
                    countMoves -= 1
                    rewinded_Moves_Stack_Notation.append(
                        moveLogNotation.pop())  # moveLogNotation + rewindedMovesQuery = current game recorded to date.
                    self.window["Move-Log"].update(moveLogNotation)  # update Move Log Listbox

                moveToBeReversed = moveLog.pop()  # removes the last element
                rewinded_Moves_Stack.append(moveToBeReversed)
                movesPlayed -= 1

                # condition when to de-select when you selected a square.
                if click == 1:
                    self.window[previousEvent].update(button_color=self.colors[(previousEvent[0] + previousEvent[1]) % 2])
                    click = 0

                self.makeMove(moveToBeReversed, reverse=True)

                started_Undoing_Moves = True  # Important flag variable for redoing Moves..
                whiteToMove = not whiteToMove  # don't forget to change the turns.

                print(moveLog)

            if event == "Redo":
                print(rewinded_Moves_Stack)
                # skip this condition if rewinded_Moves_Query is empty or we havent started Undoing Moves
                if len(rewinded_Moves_Stack) == 0:
                    continue

                moveToBePlayed = rewinded_Moves_Stack.pop()  # last item of rewinded_Moves_Query
                self.makeMove(moveToBePlayed)

                moveLog.append(moveToBePlayed)
                movesPlayed += 1
                if not whiteToMove:
                    countMoves += 1
                    moveLogNotation.append(rewinded_Moves_Stack_Notation.pop())
                    self.window["Move-Log"].update(moveLogNotation)  # update MoveLogNotation.

                whiteToMove = not whiteToMove  # don't forget to change the turns.

            if click == 0 and piece.metadata != "":

                color = str(piece.metadata[1])
                if (color == "B" and whiteToMove or color == "W" and not whiteToMove):
                    continue

                self.window[event].update(
                    button_color="red")  # change the background color to signal the user that which square he clicked to play

                selectedPiece = piece.metadata
                previousEvent = event

                click += 1

            # Second click checks if the move is possible then plays it, if not then cancels.
            elif click == 1 and previousEvent != "Undo":

                if previousEvent == event:
                    click = 0

                if self.validMove(selectedPiece, piece.metadata, self.board):  # check if a move is valid.
                    whiteToMove = not whiteToMove

                    if started_Undoing_Moves:
                        rewinded_Moves_Stack = []
                        rewinded_Moves_Stack_Notation = []
                        started_Undoing_Moves = False

                    move = (selectedPiece, self.window[event].metadata, previousEvent, event)
                    self.makeMove(move)
                    moveLog.append(move)
                    movesPlayed += 1

                    # window[event].metadata = selectedPiece  # Current square will now contain the selected piece.
                    # window[event].update(image_filename=pieces[selectedPiece])  # we change the background of the selected square accordingly.
                    # window[previousEvent].update(image_filename=blank)
                    # window[previousEvent].metadata = ""  # Current square will now be empty

                    # if black has played its move then append the moves in moveLog.
                    if whiteToMove:
                        countMoves += 1

                        notation = "{}. {} {}".format(countMoves, self.turnIntoNotation(moveLog[movesPlayed - 2]),
                                                    self.turnIntoNotation(moveLog[movesPlayed - 1]))

                        moveLogNotation.append(notation)  # add all elements in MoveLogElem to moveLog
                        self.window["Move-Log"].update(moveLogNotation)  # add move to Column so it's visible on the GUI.

                    click = 0  # reset clicks since the move has been made

                self.window[previousEvent].update(button_color=self.colors[(previousEvent[0] + previousEvent[1]) % 2])

            else:

                # you clicked on the same square again so the progress within the first click will reset
                # selectedPiece = "" this is useless because selectedPiece value will be changed again.
                if (click == 1):
                    self.window[previousEvent].update(button_color=self.colors[(previousEvent[0] + previousEvent[1]) % 2])

            for i in self.board: print(i)
        self.window.close()  # dont forget thisss