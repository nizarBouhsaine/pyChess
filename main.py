"""Le programe principale responsable de l'affichage"""

"""Import des packages/biblios"""
import pygame as p
import ChessEngine
from collections import OrderedDict

# initialisation des modules de pygame
p.init()
"""Les fonctions"""


# fonction qui associe les images aux pieces correspendantes
def load_images(img):
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bP", "wR", "wN", "wB", "wQ", "wK", "wP"]
    for piece in pieces:
        img[piece] = p.transform.smoothscale(p.image.load(f"./images/{piece}.png"), (SQ_SIZE, SQ_SIZE))

def load_reverse_images(img):
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bP", "wR", "wN", "wB", "wQ", "wK", "wP"]
    for piece in pieces:
        if piece[0] == "w":
            img["b"+piece[1]] = p.transform.smoothscale(p.image.load(f"./images/{piece}.png"), (SQ_SIZE, SQ_SIZE))
        else:
            img["w" + piece[1]] = p.transform.smoothscale(p.image.load(f"./images/{piece}.png"), (SQ_SIZE, SQ_SIZE))


        # transform.smoothscale adapte l'image à la taille des cases de l'échiquier


# fontion de dessin de l echiquier
def drawBoard(window):
    # couleur on rgb
    global color
    white = (255, 255, 255)
    gray = (130, 130, 130)
    # list des couleurs de l'echequier
    colors = [white, gray]

    # Insérer du texte
    FONT = p.font.Font(None, 23)

    # liste des lettres de marquages de colonnes
    alpha_list = ["a", "b", "c", "d", "e", "f", "g", "h"]

    # dessin des cases de l'échequier
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            # couleur les pair de blanc et l'impair de gris
            color = colors[((r + c) % 2)]

            # dessin des carrés sous forme de rectangle
            # Rect(left, top, width, height)
            p.draw.rect(window, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

            # précise la couleur et la chaine à afficher
            alpha = FONT.render(alpha_list[c], True, colors[c % 2])

            # positionne l'alphabet dans la dernière ligne de l'échiquier
            window.blit(alpha, (SQ_SIZE * (c + 1) - (DIMENSION + 2), WIDTH - 15))
            # blit(source,(colonne,ligne))

        # positionne les nbres dans la premiere case de chaque colonne
        nbr = FONT.render(str(DIMENSION - r), True, color)
        window.blit(nbr, (0, r * SQ_SIZE + 5))

    # necessaire pour la mis a jour de l affichage chaque fois qqchose change
    # p.display.update()


def drawPieces(window, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":  # piece != d une case vide
                window.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

# def drawPiecesReverse(window, board):
#     for r in range(DIMENSION):
#         for c in range(DIMENSION):
#             piece = board[r][c]
#             if piece != "--":  # piece != d une case vide
#                 window.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))



def drawState(window, gs):
    drawBoard(window)
    drawPieces(window, gs.board)


def draw_available_moves(window, moveList):
    for move in moveList:
        if len(move) > 0:
            r = move[0]
            c = move[1]
            # p.draw.rect(window, BLUE, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            p.draw.circle(window, BLUE, (c * SQ_SIZE + SQ_SIZE // 2, r * SQ_SIZE + SQ_SIZE // 2), SQ_SIZE // DIMENSION)
            p.display.update()


def high_light_piece(window, r, c, board):
    p.draw.rect(window, BLUE, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    window.blit(IMAGES[board[r][c]], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    p.display.update()


"""Les variables globales"""
# Dimension de la fenetre
WIDTH = 720

# la Dimension de l'échiquier
DIMENSION = 8

# la taille d'un carré
SQ_SIZE = WIDTH // DIMENSION

# Le nombre de frame par seconde, nombre du "re-dessin" du contenu de la fenetre
FPS = 15

# Dictionnaire de stockage des images des pieces, préferabe de les stocker comme variable, afin d'éviter les lags
IMAGES = {}
load_images(IMAGES)


BLUE = (0, 100, 120)

"""La programe principale"""


def main():
    global draw_moves
    draw_moves = []
    # La fenetre elle-meme
    WIN = p.display.set_mode((WIDTH, WIDTH))

    # variable utiliser pour la FPS
    clock = p.time.Clock()

    # objet de class gameState
    gs = ChessEngine.gameState()
    valid_moves = gs.getValidMoves()
    valid_possible = gs.getValidMoves()
    inCheck, Checks, pins = gs.checkForPinsAndChecks()
    moveMade = False  # flag pour génerer des nouveaux mvts juste au cas le joueur a effectué un movt valide

    # chargement des images des pieces
    load_images(IMAGES)

    # constante de la boucle principale
    run = True

    # historique des cliques
    sqSelected = ()  # va prendre la ligne et la colonne de la case choisie
    playerClicks = []  # va contenir la position initial et terminal de la piece

    # boucle principale
    while run:
        # responsable de l ouverture et fermeture de la fenetre
        for event in p.event.get():
            if event.type == p.QUIT:
                run = False
            # gestion des cliques souris
            elif event.type == p.MOUSEBUTTONDOWN:
                # la position de la souris (colonne,ligne) sur l'échiquier
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE  # colonne de l'échiquier
                row = location[1] // SQ_SIZE  # ligne de l'échiquier
                if gs.board[row][col] != "--":
                    high_light_piece(WIN, row, col, gs.board)
                for moves in valid_moves:
                    if moves.startSq == (row, col):
                        draw_moves.append(moves.endSq)
                draw_moves = list(OrderedDict.fromkeys(draw_moves))
                move_list = []
                for move in valid_possible:
                    move_list.append(move.endSq)
                move_list = list(OrderedDict.fromkeys(move_list))

                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClicks = []
                    draw_moves = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                    # cas de sélection d'une case vide comme case de depart
                    if gs.board[playerClicks[0][0]][playerClicks[0][1]] == "--":
                        sqSelected = ()
                        playerClicks = []
                if len(playerClicks) == 2:  # responsable du déplacement des pieces
                    # réception des cases choisies par le joueur
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    # affichage du mvt sous forme de notation d'echec
                    if move in valid_moves:
                        gs.makeMove(move)
                        moveMade = True
                        print(move.getChessNotation())


                    # réalisation du mouvement

                    # vider les clicks du joueur après un mouvement
                    sqSelected = ()
                    playerClicks = []
                    draw_moves = []
            elif event.type == p.KEYDOWN:
                if event.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
        if moveMade:
            valid_moves = gs.getValidMoves()
            inCheck, Checks, pins = gs.checkForPinsAndChecks()
            valid_possible = gs.getValidMoves()
            if gs.checkMate:
                if gs.whiteToMove:
                    print("Black wins")
                else:
                    print("White Wins")
            elif gs.staleMate:
                print("StaleMate")
            moveMade = False


        if draw_moves:
            draw_available_moves(WIN, draw_moves)

        else:
            drawState(WIN, gs)
            p.display.flip()
            # if gs.Checkmate():
            #     print("game over")
    # qd run = False on quite la boucle et le programme se ferme
    p.quit()


if __name__ == "__main__":
    main()
