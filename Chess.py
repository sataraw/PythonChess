import re

whitePlaying = True
gameOver = False
whiteKingMoved = False
blackKingMoved = False
whiteRooksMoved = [False, False]  # [queenside, kingside]
blackRooksMoved = [False, False]  # [queenside, kingside]
gameOver = False
chessBoardProjection = [['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr'],
                        ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
                        [' ',  ' ',   ' ', ' ',  ' ',  ' ', ' ',  ' '],
                        [' ',  ' ',   ' ', ' ',  ' ',  ' ', ' ',  ' '],
                        [' ',  ' ',   ' ', ' ',  ' ',  ' ', ' ',  ' '],
                        [' ',  ' ',   ' ', ' ',  ' ',  ' ', ' ',  ' '],
                        ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
                        ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br']]
chessBoard = [['♖', '♘', '♗', '♕', '♔', '♗', '♘', '♖'],
              ['♙', '♙', '♙', '♙', '♙', '♙', '♙', '♙'],
              [' ',  ' ',  ' ',  ' ', ' ', ' ',  ' ',  ' '],
              [' ',  ' ',  ' ',  ' ', ' ', ' ',  ' ',  ' '],
              [' ',  ' ',  ' ',  ' ', ' ', ' ',  ' ',  ' '],
              [' ',  ' ',  ' ',  ' ', ' ', ' ',  ' ',  ' '],
              ['♟', '♟', '♟', '♟', '♟', '♟', '♟', '♟'],
              ['♜', '♞', '♝', '♛', '♚', '♝', '♞', '♜']]


def validateInput(str):
    # Checks if a move is legal
    str = str.lower()
    pattern = re.compile("^([a-h][1-8]){1}$")
    if (not bool(pattern.match(str))):
        return False
    else:
        x = ord(str[0]) - 97
        y = ord(str[1]) - 48 - 1
        return True


def makeMove(x1, x2, y1, y2):
    chessBoardProjection[y2][x2] = chessBoardProjection[y1][x1]
    chessBoardProjection[y1][x1] = ' '
    chessBoard[7 - y2][x2] = chessBoard[7 - y1][x1]
    chessBoard[7 - y1][x1] = ' '


def checkPath(x1, x2, y1, y2):
    dy = y2 - y1
    dx = x2 - x1
    if (dx != 0):
        dx = dx / abs(dx)
    if (dy != 0):
        dy = dy / abs(dy)
    tempX = x1 + dx
    tempY = y1 + dy
    while (tempY != y2 or tempX != x2):
        if (chessBoardProjection[int(tempY)][int(tempX)] != ' '):
            return False
        tempX += dx
        tempY += dy
    return True


def validateMove(fromField, toField):
    if(not validateInput(fromField) or not validateInput(toField)):
        return False
    x1 = ord(fromField[0]) - 97
    y1 = ord(fromField[1]) - 48 - 1
    x2 = ord(toField[0]) - 97
    y2 = ord(toField[1]) - 48 - 1
    if (chessBoardProjection[y1][x1][0] == ' '):
        return False
    if (chessBoardProjection[y1][x1][0] == 'w' and not whitePlaying)\
            or (chessBoardProjection[y1][x1][0] == 'b' and whitePlaying):
        return False
    if (chessBoardProjection[y2][x2][0] == 'w' and whitePlaying)\
            or (chessBoardProjection[y2][x2][0] == 'b' and not whitePlaying):
        return False
    dyReal = y2 - y1
    dxReal = x2 - x1
    if (dxReal != 0):
        dx = dxReal / abs(dxReal)
    else:
        dx = dxReal
    if (dyReal != 0):
        dy = dyReal / abs(dyReal)
    else:
        dy = dyReal
    
    # Castling
    if chessBoardProjection[y1][x1][1] == 'k' and abs(dxReal) == 2 and dyReal == 0:
        if whitePlaying and not whiteKingMoved:
            if x2 == 2 and not whiteRooksMoved[0]:  # Queenside
                if checkPath(x1, 0, y1, y1) and not isKingInCheck(whitePlaying) and not isSquareAttacked(x1-1, y1, whitePlaying) and not isSquareAttacked(x1-2, y1, whitePlaying):
                    castle(x1, y1, x2, y2)
                    return True
            elif x2 == 6 and not whiteRooksMoved[1]:  # Kingside
                if checkPath(x1, 7, y1, y1) and not isKingInCheck(whitePlaying) and not isSquareAttacked(x1+1, y1, whitePlaying) and not isSquareAttacked(x1+2, y1, whitePlaying):
                    castle(x1, y1, x2, y2)
                    return True
        elif not whitePlaying and not blackKingMoved:
            if x2 == 2 and not blackRooksMoved[0]:  # Queenside
                if checkPath(x1, 0, y1, y1) and not isKingInCheck(whitePlaying) and not isSquareAttacked(x1-1, y1, whitePlaying) and not isSquareAttacked(x1-2, y1, whitePlaying):
                    castle(x1, y1, x2, y2)
                    return True
            elif x2 == 6 and not blackRooksMoved[1]:  # Kingside
                if checkPath(x1, 7, y1, y1) and not isKingInCheck(whitePlaying) and not isSquareAttacked(x1+1, y1, whitePlaying) and not isSquareAttacked(x1+2, y1, whitePlaying):
                    castle(x1, y1, x2, y2)
                    return True
    
    if chessBoardProjection[y1][x1][1] == 'n':  # Knight move
        if (abs(dxReal) == 2 and abs(dyReal) == 1) or (abs(dxReal) == 1 and abs(dyReal) == 2):
            makeMove(x1, x2, y1, y2)
            return True
        else:
            return False
    
    if not checkPath(x1, x2, y1, y2):
        return False
    if chessBoardProjection[y1][x1][1] == 'p':
        if chessBoardProjection[y2][x2] != ' ':
            if whitePlaying and dy == abs(dx) and dyReal == 1 and (abs(dxReal) == 1)\
                    or not whitePlaying and -dy == abs(dx) and dyReal == -1 and abs(dxReal) == 1:
                if (whitePlaying and y2 == 7) or (not whitePlaying and y2 == 0):
                    handlePromotion(x1, y1, x2, y2)
                else:
                    makeMove(x1, x2, y1, y2)
                return True
            else:
                return False
        elif dx != 0:
            return False
        if whitePlaying and y1 != 1 or not whitePlaying and y1 != 6:
            if(abs(dyReal) > 1):
                return False
        elif abs(dyReal) > 2:
            return False
        if dyReal > 0 if whitePlaying else dyReal < 0:
            if (whitePlaying and y2 == 7) or (not whitePlaying and y2 == 0):
                handlePromotion(x1, y1, x2, y2)
            else:
                makeMove(x1, x2, y1, y2)
            return True
    elif chessBoardProjection[y1][x1][1] == 'r':
        if(dx == 0 and dy != 0) or (dx != 0 and dy == 0):
            makeMove(x1, x2, y1, y2)
            updateRookMoved(x1, y1)
            return True
        else:
            return False
    elif chessBoardProjection[y1][x1][1] == 'b':
        if(dx == 0 or dy == 0):
            return False
        if(abs(dyReal) != abs(dxReal)):
            return False
        else:
            makeMove(x1, x2, y1, y2)
            return True
    elif chessBoardProjection[y1][x1][1] == 'q':
        if(dx == 0 and dy != 0) or (dx != 0 and dy == 0) or (abs(dyReal) == abs(dxReal)):
            makeMove(x1, x2, y1, y2)
            return True
    elif chessBoardProjection[y1][x1][1] == 'k':
        if(abs(dxReal) <= 1 and abs(dyReal) <= 1):
            makeMove(x1, x2, y1, y2)
            updateKingMoved()
            return True
    return False


def printBoard(chessBoard):
    for i in range(len(chessBoard[0])):
        print(8 - i, end=" ")
        for j in range(len(chessBoard[i])):
            print('|', end=f" {chessBoard[i][j]} ")
        print('|')
        print(u'\u2500' * 35)
    print("  | a | b | c | d | e | f | g | h |")

def handlePromotion(x1, y1, x2, y2):
    while True:
        piece = input("Choose promotion piece (q: Queen, r: Rook, b: Bishop, n: Knight): ").lower()
        if piece in ['q', 'r', 'b', 'n']:
            color = 'w' if whitePlaying else 'b'
            chessBoardProjection[y2][x2] = color + piece
            chessBoard[7 - y2][x2] = {'q': '♕', 'r': '♖', 'b': '♗', 'n': '♘'}[piece] if not whitePlaying else \
                                     {'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞'}[piece]
            chessBoardProjection[y1][x1] = ' '
            chessBoard[7 - y1][x1] = ' '
            break
        else:
            print("Invalid choice. Please choose q, r, b, or n.")
def castle(x1, y1, x2, y2):
    # Move king
    makeMove(x1, x2, y1, y2)
    # Move rook
    if x2 == 2:  # Queenside
        makeMove(0, 3, y1, y1)
    else:  # Kingside
        makeMove(7, 5, y1, y1)
    updateKingMoved()
    updateRookMoved(x1, y1)

def updateKingMoved():
    global whiteKingMoved, blackKingMoved
    if whitePlaying:
        whiteKingMoved = True
    else:
        blackKingMoved = True

def updateRookMoved(x, y):
    global whiteRooksMoved, blackRooksMoved
    if whitePlaying:
        if x == 0:
            whiteRooksMoved[0] = True
        elif x == 7:
            whiteRooksMoved[1] = True
    else:
        if x == 0:
            blackRooksMoved[0] = True
        elif x == 7:
            blackRooksMoved[1] = True

def isKingInCheck(isWhite):
    # Implement check detection logic here
    return False

def isSquareAttacked(x, y, isWhite):
    # Implement square attack detection logic here
    return False



printBoard(chessBoard)

fromField = ' '
toField = ' '
while(not gameOver):
    while True:
        fromField = ' '
        toField = ' '
        while (not validateInput(fromField)):
            fromField = input("Enter a valid input for the starting field: ")
        while (not validateInput(toField)):
            toField = input("Enter a valid input for the ending field: ")
        if(validateMove(fromField, toField)):
            break
        else:
            print("Illegal Move!")
    whitePlaying = not whitePlaying
    print("\033c", end="")
    printBoard(chessBoard)
printBoard(chessBoard)
