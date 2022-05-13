"""Pour l'instant, responsable du stockage de l'historique des mouvements aka l'état courant du jeu
et la vérification de la légitimité des mouvements des pieces"""
from Move import *
from piece import *


class gameState():
    """ Board : attribut representant m'état courant(ici initial) de l'échiquier
        Couleur : b =noir , w= blanc
        piece : R = tour , N=Cavalier, B=Fou, Q=Dame, K=Roi, P=pion
        "--" represente une case vide, utiliser au lieu d"un zero afin de faciliter l'échange de str par str"""

    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        # self.board = [
        #     ["--", "--", "--", "--", "bQ", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "bQ", "--"],
        #     ["--", "--", "--", "--", "--", "wQ", "--", "--"],
        #     ["--", "--", "--", "--", "wK", "--", "--", "--"]
        # ]

        self.moveFunction = {"P": self.get_Pawn_moves,
                             "Q": self.get_Queen_moves,
                             "K": self.get_King_moves,
                             "N": self.get_Knight_moves,
                             "B": self.get_Bishop_moves,
                             "R": self.get_Rook_moves}

        """True : Blanc a le trait; False: Noir a le trait, initialiser à True car le blanc commence le premier """
        self.whiteToMove = True

        """L'historique des mvts"""
        self.moveLog = []

        self.whiteKinglocation = (7, 4)
        self.blackKinglocation = (0, 4)

        self.checkMate =False
        self.staleMate = False

        self.inCheck = False  # si un roi est en echec cette variable devient vraie
        self.pins = []  # pieces bloquées afin de protéger le roi
        self.checks = []  # pièces qui mettent le roi en echec

    # fonction responsable de deplacer une piece d'une case à une autre

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.whiteToMove = not self.whiteToMove
        self.moveLog.append(move)
        if move.pieceMoved == 'wK':
            self.whiteKinglocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKinglocation = (move.endRow, move.endCol)

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == 'wK':
                self.whiteKinglocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKinglocation = (move.startRow, move.startCol)

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board)):
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunction[piece](r, c, moves)

        return moves

    def get_Pawn_moves(self, row, col, moves):
        piecePinned = False
        pinDirection =()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        moves += Pawn(self.board[row][col][0], row, col).get_available_moves(self.board, piecePinned, pinDirection)
        if piecePinned:
            for move in moves:
                print(move.endSq)
        return moves

    def get_Knight_moves(self, row, col, moves):
        piecePinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break
        moves += Knight(self.board[row][col][0], row, col).get_available_moves(self.board,piecePinned)
        return moves

    def get_Rook_moves(self, row, col, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        moves += Rook(self.board[row][col][0], row, col).get_available_moves(self.board,piecePinned,pinDirection)
        return moves

    def get_Bishop_moves(self, row, col, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        moves += Bishop(self.board[row][col][0], row, col).get_available_moves(self.board,piecePinned,pinDirection)
        return moves

    def get_Queen_moves(self, row, col, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == row and self.pins[i][1] == col:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        moves += Queen(self.board[row][col][0], row, col).get_available_moves(self.board,piecePinned,pinDirection)
        return moves

# la classe king est un special donc on la definie ici
    def get_King_moves(self, row, col, moves):
        if self.whiteToMove:
            allyColor = "w"
        else:
            allyColor = "b"

        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)

        for i in range(len(self.board)):
            endRow = row + rowMoves[i]
            endCol = col + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    if allyColor == "w":
                        self.whiteKinglocation = (endRow, endCol)
                    else:
                        self.blackKinglocation = (endRow, endCol)
                    inCheck, checks, pins = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((row, col), (endRow, endCol), self.board))

                    if allyColor =="w":
                        self.whiteKinglocation =(row,col)
                    else:
                        self.blackKinglocation =(row,col)
        return moves

    def getValidMoves(self):
        moves = []
        self.inCheck, self.checks, self.pins = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKinglocation[0]
            kingCol = self.whiteKinglocation[1]
        else:
            kingRow = self.blackKinglocation[0]
            kingCol = self.blackKinglocation[1]
        if self.inCheck:
            if len(self.checks) == 1:  # une seule piece qui met le roi en echec
                moves = self.getAllPossibleMoves()
                # pour bloquer un echec une piece doit etre mise entre le roi la piece enemie
                check = self.checks[0]  # info de la piece attaquante
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []  # les carrés auxquels les pieces peuvent se déplacer
                # si c'est un cavalier, on doit soit déplacer le roi ou bien capturer le cavalier
                if pieceChecking[1] == "N":
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i,
                                       kingCol + check[3] * i)  # check[2] et check[3] sont les directions d echec
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[
                            1] == checkCol:  # on sort quand on arrive a le piece attaquante
                            break
                # pour supprimer les mouvements qui ne bloquent pas l echec ou deplace le roi
                for i in range(len(moves) - 1, -1, -1):  # commencer du debut peut laisser des elements dupliqués
                    if moves[i].pieceMoved[1] != "K":  # movement qui ne déplace pas le roi
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            else:  # s'il s'agit d'un double echec (2 pieces attaque le roi au meme temps) le roi doit se deplacer
                self.get_King_moves(kingRow, kingCol, moves)
        else:  # s'il n'y pas d'echec
            moves = self.getAllPossibleMoves()

        if len(moves) == 0:
            if self.inCheck:
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.staleMate = False
            self.staleMate = False
        return moves

    def checkForPinsAndChecks(self):

        pins = []  # piece qui protege le roi contre un echec
        checks = []  # piece enemies qui mettent le roi en echec
        inCheck = False

        if self.whiteToMove:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.whiteKinglocation[0]
            startCol = self.whiteKinglocation[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKinglocation[0]
            startCol = self.blackKinglocation[1]

        # cherche les pins et checks a partir de la position du roi
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))  # direction des mouvements du roi

        for j in range(len(directions)):
            d = directions[j]
            possiblePins = ()  # reinitialise les pins possible
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i

                if 0 <= endRow < 8 and 0 <= endCol < 8:  # verifie si la case est a l'interieur de l'échoquier
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != "K":  # verifier si c'est un ami ou enemie, on a ajouté endPiece[1] != "K" pour éviter que le roi voit lui meme comme pin
                        if possiblePins == ():  # la premiere piece amie est bloquée
                            possiblePins = (endRow, endCol, d[0], d[1])
                        else:  # 2eme piece n'est pas bloquée
                            break

                    elif endPiece[0] == enemyColor:
                        pieceType = endPiece[1]
                        """ici on a plusieurs cas possible 
                            si la piece est otho au roi et c'est une Tour
                            si la piece attaque diagonallement et c'est un fou
                            si la piece est à un carré du roi diagonnallement et c'est un pion
                            si la piece est une reine, on considère tous les directions
                            si la piece est un roi, on considère tous les directions à un carré du roi
                            (interdire au roi de se déplacer à un carré controllé par un roi enemie)
                        """
                        if (0 <= j <= 3 and pieceType == "R") or \
                                (4 <= j <= 7 and pieceType == "B") or \
                                (i == 1 and pieceType == "P" and (
                                        (enemyColor == "w" and 6 <= j <= 7) or (enemyColor == "b" and 4 <= j <= 5))) or \
                                (pieceType == "Q") or (i == 1 and pieceType == "K"):
                            if possiblePins == ():  # ya pas de piece qui bloque , donc echec
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else:  # piece qui bloque donc c'est un pin
                                pins.append(possiblePins)
                                break
                        else:  # si la piece enemie ne met pas le roi en echec
                            break

        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == "N":  # cavalier enemie attaquant le roi
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, checks, pins

