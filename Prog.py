from fltk import *
from random import *
from time import sleep


def fantome(x, y):
    """Création du Qix"""
    largeurFantome = 100
    hauteurFantome = 110
    image(
        x,
        y,
        "Fantome.gif",
        largeurFantome,
        hauteurFantome,
        ancrage="center",
        tag="fant",
    )
    return x, y


# ****************************************************************************************************************************


def sparx1(x, y):
    """Création du sparx1"""
    largeurSparx = 40
    hauteurSparx = 40
    image(x, y, "Sparx.gif", largeurSparx, hauteurSparx, ancrage="center", tag="spar1")
    return x, y


def sparx2(x, y):
    """Création du sparx2"""
    largeurSparx = 40
    hauteurSparx = 40
    image(x, y, "Sparx.gif", largeurSparx, hauteurSparx, ancrage="center", tag="spar2")
    return x, y


# ****************************************************************************************************************************

"""Dessin du joueur"""


def joueur(x: int, y: int, taille=8):
    cercle(x, y, taille, couleur="lime", tag="joueur")


"""La fonction qui permet de dessiner la ligne qui suit le joueur"""


def dessin(ax: int, ay: int, bx: int, by: int):
    ligne(ax, ay, bx, by, couleur="white", tag="dessin")


"""La fonction qui permet de tracer le polygone à partir des points des lignes"""


def tracerPolygone(listePositions: list):
    polygone(listePositions, couleur="blue", remplissage="blue", tag="aire")



"""La fonction qui permet de vérifier si le joueur touche l'un des deux sparx"""


def checkSparxPlayer(
    xJoueur: float,
    yJoueur: float,
    x_sparx1: float,
    y_sparx1: float,
    x_sparx2: float,
    y_sparx2: float,
    tailleJoueur: int,
) -> bool:
    if (
        (xJoueur + (tailleJoueur // 2) >= x_sparx1)
        and ((xJoueur + tailleJoueur) <= (x_sparx1 + 40))
        and (yJoueur + (tailleJoueur // 2) >= y_sparx1)
        and ((yJoueur + tailleJoueur) <= (y_sparx1 + 40))
    ):
        return True
    if (
        (xJoueur + (tailleJoueur // 2) >= x_sparx2)
        and ((xJoueur + tailleJoueur) <= (x_sparx2 + 40))
        and (yJoueur + (tailleJoueur // 2) >= y_sparx2)
        and ((yJoueur + tailleJoueur) <= (y_sparx2 + 40))
    ):
        return True
    else:
        return False


"""La fonction qui permet de vérifier si le joueur touche le qix"""


def checkQixPlayer(
    xJoueur: float,
    yJoueur: float,
    xQix: float,
    yQix: float,
    tailleJoueur: int,
) -> bool:
    if (
        (xJoueur + (tailleJoueur // 2) >= xQix)
        and ((xJoueur + tailleJoueur) <= (xQix + 100))
        and (yJoueur + (tailleJoueur // 2) >= yQix)
        and ((yJoueur + tailleJoueur) <= (yQix + 110))
    ):
        return True
    else:
        return False


if __name__ == "__main__":
    """Création de la fenêtre"""
    largeurFenetre = 1500
    hauteurFenetre = 1000
    cree_fenetre(largeurFenetre, hauteurFenetre)

    # Position de l'air de jeu
    x_gauche_contour = 375
    x_droite_contour = 1125
    y_bas_contour = 800
    y_haut_contour = 200

    # Fond noir
    rectangle(5, 1000, 1500, 5, epaisseur=10, remplissage="black")
    # ****************************************************************************************************************************
    """Air de jeu"""
    rectangle(
        x_gauche_contour,
        y_bas_contour,
        x_droite_contour,
        y_haut_contour,
        couleur="white",
        tag="air",
    )
    ligne(382, 185, 1120, 185, couleur="red", epaisseur=3)
    # Logo Qix
    image(500, 100, "Qix.gif", ancrage="center", tag="im")
    # ****************************************************************************************************************************
    """Position du Qix"""
    x_fantome = 750
    y_fantome = 550
    speedXFantome = 5
    speedYFantome = 2
    # ****************************************************************************************************************************
    """Position des sparx"""
    x_sparx1 = 755
    y_sparx1 = 200
    x_sparx2 = 745
    y_sparx2 = 200
    speedSparx = 3.5
    fantome(750, 550)
    # ****************************************************************************************************************************
    """Joueur"""
    xJoueur = (x_droite_contour + x_gauche_contour) // 2
    yJoueur = y_bas_contour
    tailleJoueur = 5
    enTrainDeDessiner = False
    vie = 3

    lstBords = [(x_gauche_contour, y_haut_contour), (x_droite_contour, y_haut_contour), (x_droite_contour, y_bas_contour), (x_gauche_contour, y_bas_contour)]
    listePositionsLignes = []
    listePositionsPolygone = []
    # ****************************************************************************************************************************
    """Boucle du jeu"""
    while True and vie > 0:
        ev = donne_ev()
        if type_ev(ev) == "Quitte":
            break
        listePositionsLignes = []
        """Déplacement du Qix"""
        efface("txtAire")
        efface("fant")
        efface("player")
        fantome(x_fantome, y_fantome)
        joueur(xJoueur, yJoueur, tailleJoueur)
        x_fantome += speedXFantome
        y_fantome -= speedYFantome
        # Collisions du Qix
        if x_fantome >= x_droite_contour - 60 or x_fantome <= x_gauche_contour + 60:
            speedXFantome = -speedXFantome

        if y_fantome >= y_bas_contour - 60 or y_fantome <= y_haut_contour + 60:
            speedYFantome = -speedYFantome
        # ****************************************************************************************************************************
        """Déplacement des sparx"""
        efface("spar1")
        sparx1(x_sparx1, y_sparx1)

        if y_sparx1 <= y_haut_contour:
            x_sparx1 += speedSparx

        if x_sparx1 >= x_droite_contour:
            x_sparx1 = 1125
            y_sparx1 += speedSparx

        if y_sparx1 >= y_bas_contour:
            y_sparx1 = y_bas_contour
            x_sparx1 -= speedSparx

        if x_sparx1 <= x_gauche_contour:
            x_sparx1 = x_gauche_contour
            y_sparx1 -= speedSparx

        efface("spar2")
        sparx2(x_sparx2, y_sparx2)

        if y_sparx2 <= y_haut_contour:
            x_sparx2 -= speedSparx

        if x_sparx2 <= x_gauche_contour:
            x_sparx2 = 375
            y_sparx2 += speedSparx

        if y_sparx2 >= y_bas_contour:
            y_sparx2 = y_bas_contour
            x_sparx2 += speedSparx

        if x_sparx2 >= x_droite_contour:
            x_sparx2 = x_droite_contour
            y_sparx2 -= speedSparx
        # ****************************************************************************************************************************
        """On vérifie si l'utilisateur a appuyé sur une touche"""
        # ****************************************************************************************************************************
        """Si la touche flèche droite est appuyée et que les autres touches ne sont pas appuyées"""
        if type_ev(ev) == "Touche":
            oldX, oldY = xJoueur, yJoueur
            if touche(ev) == "Up" and yJoueur > y_haut_contour:
                yJoueur -= tailleJoueur
                if enTrainDeDessiner:
                    dessin(oldX, oldY, oldX, yJoueur)
                    listePositionsLignes.append((oldX, oldY, oldX, yJoueur))
                    if (xJoueur <= x_gauche_contour or xJoueur >= x_droite_contour or yJoueur <= y_haut_contour or yJoueur >= y_bas_contour):
                        dernierPoint = listePositionsLignes[-1][2:]
                        listePositionsLignes.append((xJoueur, yJoueur, *dernierPoint))
                        tracerPolygone(listePositionsLignes)
                        listePositionsPolygone.extend(listePositionsLignes)
                        listePositionsLignes = []
                        enTrainDeDessiner = not enTrainDeDessiner

            elif touche(ev) == "Down" and yJoueur < y_bas_contour:
                yJoueur += tailleJoueur
                if enTrainDeDessiner:
                    dessin(oldX, oldY, oldX, yJoueur)
                    listePositionsLignes.append((oldX, oldY, oldX, yJoueur))
                    if (xJoueur <= x_gauche_contour or xJoueur >= x_droite_contour or yJoueur <= y_haut_contour or yJoueur >= y_bas_contour):
                        dernierPoint = listePositionsLignes[-1][2:]
                        listePositionsLignes.append((xJoueur, yJoueur, *dernierPoint))
                        tracerPolygone(listePositionsLignes)
                        listePositionsPolygone.extend(listePositionsLignes)
                        listePositionsLignes = []
                        enTrainDeDessiner = not enTrainDeDessiner

            elif touche(ev) == "Left" and xJoueur > x_gauche_contour:
                xJoueur -= tailleJoueur
                if enTrainDeDessiner:
                    dessin(oldX, oldY, xJoueur, oldY)
                    listePositionsLignes.append((oldX, oldY, xJoueur, oldY))
                    if (xJoueur <= x_gauche_contour or xJoueur >= x_droite_contour or yJoueur <= y_haut_contour or yJoueur >= y_bas_contour):
                        dernierPoint = listePositionsLignes[-1][2:]
                        listePositionsLignes.append((xJoueur, yJoueur, *dernierPoint))
                        tracerPolygone(listePositionsLignes)
                        listePositionsPolygone.extend(listePositionsLignes)
                        listePositionsLignes = []
                        enTrainDeDessiner = not enTrainDeDessiner

            elif touche(ev) == "Right" and xJoueur < x_droite_contour:
                xJoueur += tailleJoueur
                if enTrainDeDessiner:
                    dessin(oldX, oldY, xJoueur, oldY)
                    listePositionsLignes.append((oldX, oldY, xJoueur, oldY))
                    if (xJoueur <= x_gauche_contour or xJoueur >= x_droite_contour or yJoueur <= y_haut_contour or yJoueur >= y_bas_contour):
                        dernierPoint = listePositionsLignes[-1][2:]
                        listePositionsLignes.append((xJoueur, yJoueur, *dernierPoint))
                        tracerPolygone(listePositionsLignes)
                        listePositionsPolygone.extend(listePositionsLignes)
                        listePositionsLignes = []
                        enTrainDeDessiner = not enTrainDeDessiner

            efface("joueur")
            joueur(xJoueur, yJoueur)

            if touche(ev) == "Return":
                enTrainDeDessiner = not enTrainDeDessiner
        # ****************************************************************************************************************************
        """Si il y a contact entre joueur et sparx alors on enlève une vie et on place le joueur au milieu en bas"""
        if (
            checkSparxPlayer(
                xJoueur, yJoueur, x_sparx1, y_sparx1, x_sparx2, y_sparx2, tailleJoueur
            )
            == True
        ):
            vie -= 1
            xJoueur = largeurFenetre // 2
            yJoueur = y_bas_contour - (tailleJoueur // 2)
            continue
        # ****************************************************************************************************************************
        """Si il y a contact entre joueur et sparx alors on enlève une vie et on place le joueur au milieu en bas"""
        if checkQixPlayer(xJoueur, yJoueur, x_fantome, y_fantome, tailleJoueur) == True:
            vie -= 1
            xJoueur = largeurFenetre // 2
            yJoueur = y_bas_contour - (tailleJoueur // 2)
            continue

        mise_a_jour()

# ****************************************************************************************************************************
if vie < 1:
    texte(400, 400, chaine="PERDU", couleur="red")
sleep(3)  # Attente de 3 secondes
ferme_fenetre()  # Fermer la fenêtre