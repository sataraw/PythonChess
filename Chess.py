import re

whitePlaying = True
gameOver = False
chessBoardProjection = [['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr'],
                        ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
                        [' ',  ' ',   ' ', ' ',  ' ',  ' ' , ' ' ,  ' '],
                        [' ',  ' ',   ' ', ' ',  ' ',  ' ' , ' ' ,  ' '],
                        [' ',  ' ',   ' ', ' ',  ' ',  ' ' , ' ' ,  ' '],
                        [' ',  ' ',   ' ', ' ',  ' ',  ' ' , ' ' ,  ' '],
                        ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
                        ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br']]
chessBoard =           [['♖', '♘', '♗', '♕', '♔', '♗', '♘', '♖'],
                        ['♙', '♙', '♙', '♙', '♙', '♙', '♙', '♙'],
                        [' ',  ' ',  ' ',  ' ', ' ', ' ',  ' ',  ' '],
                        [' ',  ' ',  ' ',  ' ', ' ', ' ',  ' ',  ' '],
                        [' ',  ' ',  ' ',  ' ', ' ', ' ',  ' ',  ' '],
                        [' ',  ' ',  ' ',  ' ', ' ', ' ',  ' ',  ' '],
                        ['♟', '♟', '♟', '♟', '♟', '♟', '♟', '♟'],
                        ['♜', '♞', '♝', '♛', '♚', '♝', '♞', '♜']]


def validateInput(str):
    str = str.lower()
    pattern = re.compile("^([a-h][1-8]){1}$")
    if (not bool(pattern.match(str))):
        return False
    else:
        x = ord(str[0]) - 97
        y = ord(str[1]) - 48 - 1
        print(x)
        print(y)
        print(chessBoardProjection[y][x])
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
    if not checkPath(x1, x2, y1, y2):
        return False
    # TODO: IMPLEMENT PAWN FIRST MOVE CORRECTLY, IMPLEMENT PAWN ATTACKING,
    # TODO: IMPLEMENT PAWN TO QUEEN, IMPLEMENT KNIGHT AND KING MOVES 
    if chessBoardProjection[y1][x1][1] == 'p':
        if dx != 0:
            return False
        if whitePlaying and y1 != 1 or not whitePlaying and y1 != 6:
            if(abs(dyReal) > 1):
                return False
        elif abs(dyReal) > 2:
            return False
        if dyReal > 0 if whitePlaying else dyReal < 0:
            makeMove(x1, x2, y1, y2)
            return True
    elif chessBoardProjection[y1][x1][1] == 'r':
        if(dx == 0 and dy != 0):
            makeMove(x1,x2,y1,y2)
            return True
        elif(dx != 0 and dy == 0):
            makeMove(x1,x2,y1,y2)
            return True
        else:
            return False
    elif chessBoardProjection[y1][x1][1] == 'b':
        if(dx == 0 or dy == 0):
            return False
        if(abs(dyReal) != abs(dxReal)):
            return False
        else:
            makeMove(x1,x2,y1,y2)
            return True
    elif chessBoardProjection[y1][x1][1] == 'q':
        if(dx == 0 and dy != 0):
            makeMove(x1,x2,y1,y2)
            return True
        elif(dx != 0 and dy == 0):
            makeMove(x1,x2,y1,y2)
            return True
        elif(abs(dyReal) == abs(dxReal)):
            makeMove(x1,x2,y1,y2)
            return True

    print(checkPath(x1, x2, y1, y2))
    return True


def printBoard(chessBoard):
    for i in range(len(chessBoard[0])):
        print(8 - i, end=" ")
        for j in range(len(chessBoard[i])):
            print('|', end=f" {chessBoard[i][j]} ")
        print('|')
        print(u'\u2500' * 35)
    print("  | a | b | c | d | e | f | g | h |")


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
            printBoard(chessBoard)
            print("Illegal Move!")
    whitePlaying = not whitePlaying
    print(validateMove(fromField, toField))
    printBoard(chessBoard)
printBoard(chessBoard)