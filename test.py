# In this file we will try to implement moveLog on 8x8 chess board.


# Settings: ------------------------------------------------------------------------------------------------
import PySimpleGUI as pg
import os
import sys

IMAGE_PATH = "/home/muhammet/PycharmProjects/ChessPython/images"
IMAGE_PATH = "D:\codes\Python Projects\ChessPython\images"
print(IMAGE_PATH)  # -> "Python Projects\Chessss like how a python sounds like\images"
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

# first character is piece lower, the second character is color upper.
pieces = {"pB": pawnB, "rB": rookB, "bB": bishopB, "nB": knightB, "qB": queenB, "aB": amazonB, "kB": kingB,
          "pW": pawnW, "rW": rookW, "bW": bishopW, "nW": knightW, "qW": queenW, "aW": amazonW, "kW": kingW,
          "": blank}

chess_notation = {"p": "", "q": "Q", "r": "R", "n": "N", "b": "B", "a": "A", "k": "K"}

colors = ["white", "gray"]
columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
rows_reverse = [7, 6, 5, 4, 3, 2, 1, 0]
menu_def = [['File', ['New Game', 'New analysis','Open a pgn file', 'Save the game', 'Exit']], ['Controls', ['Undo', 'Redo', 'Go to the beginning'], ],  ['Analysis', ['Run Engine', 'Opening Book'], ], ['Help', 'Hint'], ]

pg.theme("DarkBlue")

# ----------------------------------------------------------------------------------------------------------------------

"""We will implement this function later entirely. for now it will only check if given two pieces have the same
color """
def validMove(piece1, piece2, board):
    return piece2 == "" or piece1[1] != piece2[1]

# function that updates one square at a time
def putPiece(pos, piece):
    # pos   = (Int, Int)
    # piece = String
    window[pos].update(image_filename = pieces[piece])
    window[pos].metadata = piece
    board[pos[0]][pos[1]] = piece

# Function that updates normally two squares at the same time.
def makeMove(move, reverse = False):
    piece = move[0]
    target = ""
    cf = move[2]
    gt = move[3]

    if reverse:
        gt, cf = cf, gt
        target = move[1]

    putPiece(cf, target)
    putPiece(gt, piece)

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
def turnIntoNotation(move):
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
        refColumn = columns[comesFrom[1]]

    return refColumn + chess_notation[piece[0]] + eaten + "{}{}".format(columns[goesTo[1]], rows_reverse[goesTo[0] - 1])

def changeButton(key, background, color, metadata, image):
    window[key].update(background_color= background)


#-----------------------------------------------------------------------------------------------------------------------
"""IT IS OUR DEFAULT BOARD 8X8."""

default_board = [["rB", "nB", "bB", "qB", "kB", "bB", "nB", "rB"],
                 ["pB", "pB", "pB", "pB", "pB", "pB", "pB", "pB"],
                 ["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""],
                 ["", "", "", "", "", "", "", ""],
                 ["pW", "pW", "pW", "pW", "pW", "pW", "pW", "pW"],
                 ["rW", "nW", "bW", "qW", "kW", "bW", "nW", "rW"]]

# Layout is a list element with 2 dimensions.
# It contains the objects for the window.

layout = [[pg.Menu(menu_def)],
   [pg.Multiline("", key='-IN-',
   expand_x=True, expand_y=True)],
   [pg.Multiline("", key='-OUT-',
   expand_x=True, expand_y=True)],
   [pg.Text("", key='-TXT-',
   expand_x=True, font=("Arial Bold", 14))], [], []]
columnA = []
columnB = []


def initialize_board(board):
    # We store the location as tuple (column, row)

    resolution = 520
    colors = ["white", "gray"]
    for row in range(len(board)):
        current_row = []
        for column in range(len(board[row])):
            color = colors[(row + column) % 2]
            current_row.append(pg.Button(pad=(0, 0), image_filename=pieces[default_board[row][column]],
                                         button_color=color, mouseover_colors=color, key=(row, column),
                                         metadata=default_board[row][column]))
        columnA.append(current_row)
    layout[0].append(pg.Column(columnA, scrollable=False, element_justification="right", size=(resolution, resolution)))


def drawMoveLog():
    # moves will be self.moves when we turn everything into class.
    columnB.append([pg.Listbox([], size=(30, 15), background_color="white", highlight_background_color="white",
                               highlight_text_color="black", text_color="black", key="Move-Log")])
    layout[0].append(
        pg.Column(columnB, scrollable=False, element_justification="left", vertical_alignment="top", pad=(0, 1)))


def drawUndoButton():
    layout[1].append(pg.Button(button_text="Undo Move", size=(12, 2),
                               pad=(1, 1), mouseover_colors=("gray", "gray"),
                               button_color="gray"
                               , key="Undo", metadata=""))


def drawRedoButton():
    layout[1].append(pg.Button(button_text="Redo Move", size=(12, 2), target=(0, 0),
                               pad=(1, 1), mouseover_colors=("gray", "gray"),
                               button_color="gray"
                               , key="Redo", metadata=""))


def drawGUI():
    initialize_board(default_board)
    drawMoveLog()
    drawUndoButton()
    drawRedoButton()


drawGUI()

window = pg.Window("Python Chess", layout)

# Settings ---------------------------------------------------------------------------------------------------------

started_Undoing_Moves = False
moveLogNotation = []
moveLog = []
click = 0
selectedPiece = ""
whiteToMove = True
countMoves = 0 # len(moveLog)
movesPlayed = 0 # len(moveLogNotation)
rewinded_Moves_Stack_Notation = []
rewinded_Moves_Stack = []
board = default_board

# These will be used in the future.
# kingOnCheck = False
# pieceCaptured = False

# -------------------------------------------------------------------------------------------------------------------

while True:
    event, values = window.read()

    if event == pg.WIN_CLOSED or event == "Leave" or event == "Exit":
        break

    if event == "Go to the beginning":
        while countMoves>=1:
            if len(moveLog) == 0:
                continue

            if whiteToMove:
                countMoves -= 1
                rewinded_Moves_Stack_Notation.append(
                    moveLogNotation.pop())  # moveLogNotation + rewindedMovesQuery = current game recorded to date.
                window["Move-Log"].update(moveLogNotation)  # update Move Log Listbox

            moveToBeReversed = moveLog.pop()  # removes the last element
            rewinded_Moves_Stack.append(moveToBeReversed)
            movesPlayed -= 1

            # condition when to de-select when you selected a square.
            if click == 1:
                window[previousEvent].update(button_color=colors[(previousEvent[0] + previousEvent[1]) % 2])
                click = 0

            makeMove(moveToBeReversed, reverse = True)

            started_Undoing_Moves = True  # Important flag variable for redoing Moves..
            whiteToMove = not whiteToMove  # don't forget to change the turns.

            print(moveLog)
        countMoves = 0
    
    # take the clicked button element.
    piece = window[event]

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
            window["Move-Log"].update(moveLogNotation)  # update Move Log Listbox

        moveToBeReversed = moveLog.pop()  # removes the last element
        rewinded_Moves_Stack.append(moveToBeReversed)
        movesPlayed -= 1

        # condition when to de-select when you selected a square.
        if click == 1:
            window[previousEvent].update(button_color=colors[(previousEvent[0] + previousEvent[1]) % 2])
            click = 0

        makeMove(moveToBeReversed, reverse = True)

        started_Undoing_Moves = True  # Important flag variable for redoing Moves..
        whiteToMove = not whiteToMove  # don't forget to change the turns.

        print(moveLog)

    if event == "Redo":
        print(rewinded_Moves_Stack)
        # skip this condition if rewinded_Moves_Query is empty or we havent started Undoing Moves
        if len(rewinded_Moves_Stack) == 0:
            continue

        moveToBePlayed = rewinded_Moves_Stack.pop()  # last item of rewinded_Moves_Query
        makeMove(moveToBePlayed)

        moveLog.append(moveToBePlayed)
        movesPlayed += 1
        if not whiteToMove:
            countMoves += 1
            moveLogNotation.append(rewinded_Moves_Stack_Notation.pop())
            window["Move-Log"].update(moveLogNotation)  # update MoveLogNotation.

        whiteToMove = not whiteToMove  # don't forget to change the turns.

    
    if click == 0 and piece.metadata != "":

        color = str(piece.metadata[1])
        if (color == "B" and whiteToMove or color == "W" and not whiteToMove):
            continue

        window[event].update(button_color="red")  # change the background color to signal the user that which square he clicked to play

        selectedPiece = piece.metadata
        previousEvent = event

        click += 1

    # Second click checks if the move is possible then plays it, if not then cancels.
    elif click == 1 and previousEvent != "Undo":

        if previousEvent == event :
            click = 0

        if validMove(selectedPiece, piece.metadata, board): # check if a move is valid.
            whiteToMove = not whiteToMove

            if started_Undoing_Moves:
                rewinded_Moves_Stack = []
                rewinded_Moves_Stack_Notation = []
                started_Undoing_Moves = False

            move = (selectedPiece, window[event].metadata, previousEvent, event)
            makeMove(move)
            moveLog.append(move)
            movesPlayed += 1


            # window[event].metadata = selectedPiece  # Current square will now contain the selected piece.
            # window[event].update(image_filename=pieces[selectedPiece])  # we change the background of the selected square accordingly.
            # window[previousEvent].update(image_filename=blank)
            # window[previousEvent].metadata = ""  # Current square will now be empty

            # if black has played its move then append the moves in moveLog.
            if whiteToMove:
                countMoves += 1

                notation = "{}. {} {}".format(countMoves, turnIntoNotation(moveLog[movesPlayed - 2]),
                                              turnIntoNotation(moveLog[movesPlayed - 1]))

                moveLogNotation.append(notation)  # add all elements in MoveLogElem to moveLog
                window["Move-Log"].update(moveLogNotation)  # add move to Column so it's visible on the GUI.

            click = 0  # reset clicks since the move has been made

        window[previousEvent].update(button_color=colors[(previousEvent[0] + previousEvent[1]) % 2])

    else:

        # you clicked on the same square again so the progress within the first click will reset
        # selectedPiece = "" this is useless because selectedPiece value will be changed again.
        if (click == 1):
            window[previousEvent].update(button_color=colors[(previousEvent[0] + previousEvent[1]) % 2])

    for i in board: print(i)
window.close()  # dont forget thisss