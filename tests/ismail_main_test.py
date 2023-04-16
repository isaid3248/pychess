# In this file we will try to implement moveLog on 8x8 chess board.


# Settings: ------------------------------------------------------------------------------------------------
import PySimpleGUI as pg
import os
import sys

IMAGE_PATH = "/home/muhammet/PycharmProjects/ChessPython/images"
# IMAGE_PATH = "Python Projects\Chessss like how a python sounds like\images"
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

pg.theme("DarkBlue")

# ----------------------------------------------------------------------------------------------------------------------

"""We will implement this function later entirely. for now it will only check if given two pieces have the same
color """


def validMove(piece1, piece2):
    return piece2 == "" or piece1[1] != piece2[1]


def turnIntoNotation(piece, destination, comesFrom, goesTo):
    eaten = ""
    refColumn = ""

    if window[goesTo].metadata != "":
        eaten = "x"

    if piece[0] == "p" and eaten == "x":
        refColumn = columns[comesFrom[1]]

    return refColumn + chess_notation[piece[0]] + eaten + "{}{}".format(columns[goesTo[1]], rows_reverse[goesTo[0] - 1])


def undoButton():
    layout[1].append(pg.Button(button_text="Undo", size=(12, 2), pad=(1, 1), mouseover_colors=("purple", "purple"),
                               button_color="blue",
                               key="undoMove", metadata=""))


def redoButton():
    layout[1].append(pg.Button(button_text="Redo", size=(12, 2), pad=(1, 1), mouseover_colors=("purple", "purple"),
                               button_color="blue",
                               key="redoMove", metadata=""))


# We store the location as tuple (column, row)

# Input = (int, int) -> String = Output
# location is part of (int, int)


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

layout = [[], []]
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


def drawGUI():
    initialize_board(default_board)
    drawMoveLog()
    redoButton()
    undoButton()


drawGUI()

window = pg.Window("Python Chess", layout)

# Settings ---------------------------------------------------------------------------------------------------------

selectedPieceLog = []
moveLogNotation = []
moveLog = []
click = 0
selectedPiece = ""
whiteToMove = True
countMoves = 0
moveLogElem = []  # contains white and black's move.
rewinded_moves = []
rewinded_moves_notation = []

# These will be used in the future.
# kingOnCheck = False
# pieceCaptured = False

# -------------------------------------------------------------------------------------------------------------------

while True:
    event, values = window.read()

    if event == pg.WIN_CLOSED or event == "Leave":
        break

    # take the clicked button element.
    piece = window[event]

    if event == "undoMove":
        if moveLog == []:
            continue

        if whiteToMove:
            countMoves -= 1
            rewinded_moves_notation.append(moveLogNotation.pop())
            window["Move-Log"].update(moveLogNotation)

        moveToBeReversed = moveLog.pop()
        rewinded_moves.append(moveToBeReversed)

        if click == 1:
            window[previousEvent].update(button_color=colors[(previousEvent[0] + previousEvent[1]) % 2])
            click = 0

        window[moveToBeReversed[3]].update(image_filename=pieces[moveToBeReversed[1]])
        window[moveToBeReversed[3]].metadata = moveToBeReversed[1]
        window[moveToBeReversed[2]].update(image_filename=pieces[moveToBeReversed[0]])
        window[moveToBeReversed[2]].metadata = moveToBeReversed[0]

        whiteToMove = not whiteToMove
        print(moveLog)

    if event == "redoMove":
        print(rewinded_moves)
        if rewinded_moves == []:
            continue

        moveToBePlayed = rewinded_moves.pop()
        window[moveToBePlayed[2]].update(image_filename=blank)
        window[moveToBePlayed[2]].metadata = ""
        window[moveToBePlayed[3]].update(image_filename=pieces[moveToBePlayed[0]])
        window[moveToBePlayed[3]].metadata = moveToBePlayed[0]

        moveLog.append(moveToBePlayed)
        if not whiteToMove:
            countMoves += 1
            moveLogNotation.append(rewinded_moves_notation.pop())
            window["Move-Log"].update(moveLogNotation)

        whiteToMove = not whiteToMove

    # check if the piece with the specific color can execute a move.
    # First click checks, if clicked button contains a piece, then a move can be executed.
    # Also check if the selected color has the moving turn.
    if click == 0 and piece.metadata != "":

        color = str(piece.metadata[1])
        if (color == "B" and whiteToMove or color == "W" and not whiteToMove):
            continue

        # change the background color to signal the user that which square he clicked to play
        window[event].update(button_color="red")
        # store the selectedPiece and previousEvent
        selectedPiece = piece.metadata
        previousEvent = event

        # In the end increment the amount of clicks by 1.
        click += 1

        # and shift the white's turn
        whiteToMove = not whiteToMove

    # Second click checks if the move is possible then plays it, if not then cancels.
    # delete the second condition in order to give pieces the ability to capture.
    elif click == 1:

        # condition for deselecting the piece to be moved
        if previousEvent == event:
            window[event].update(button_color=colors[(event[0] + event[1]) % 2])
            whiteToMove = not whiteToMove
            click = 0

        # First control if move made is valid.
        if validMove(selectedPiece, piece.metadata):

            # white's and black's move will be added
            moveLogElem.append(turnIntoNotation(selectedPiece, window[event].metadata, previousEvent, event))
            moveLog.append([selectedPiece, window[event].metadata, previousEvent, event])
            # Current square will now contain the selected piece.
            window[event].metadata = selectedPiece

            # we change the background of the selected square accordingly.
            window[event].update(image_filename=pieces[selectedPiece])

            # Old square reverts back to its original color and becomes empty.
            window[previousEvent].update(image_filename=blank,
                                         button_color=colors[(previousEvent[0] + previousEvent[1]) % 2])

            # Current square will now be empty
            window[previousEvent].metadata = ""

            # if black has played its move then append the moves in moveLog.
            if whiteToMove:
                # increment countMoves by 1 to count amount of moves made.
                countMoves += 1

                blacksMove = turnIntoNotation(moveLog[len(moveLog) - 1])
                whitesMove = turnIntoNotation(moveLog[len(moveLog) - 2])

                notation = "{}. {} {}".format(countMoves, whitesMove, blacksMove)
                print(notation)

                selectedPieceLog.append(moveLogElem[1][0])
                # add move to moveLog
                moveLogNotation.append(notation)
                # add move to Column so it's visible on the GUI.
                window["Move-Log"].update(moveLogNotation)

                # empty the current move so the other round can be stored.
                moveLogElem = []

            else:
                selectedPieceLog.append(moveLogElem[0][0])

            # reset clicks since the move has been made
            click = 0
            print(selectedPieceLog)


    else:

        # you clicked on the same square again so the progress within the first click will reset
        # selectedPiece = "" this is useless because selectedPiece value will be changed again.
        if (click == 1):
            window[previousEvent].update(button_color=colors[(previousEvent[0] + previousEvent[1]) % 2])

window.close()  # dont forget thisss