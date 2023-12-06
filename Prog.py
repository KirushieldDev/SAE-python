from fltk import *
from random import *
from time import sleep

"""Création du Qix"""


def fantome(x, y):
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


def player(x: int, y: int, cote: int):
    rectangle(x, y, x + cote, y + cote, epaisseur="3", couleur="red", tag="player")


"""La fonction qui permet de dessiner la ligne qui suit le joueur"""


def dessin(ax: int, ay: int, bx: int, by: int):
    ligne(ax, ay, bx, by, couleur="lime", tag="dessin")


"""La fonction qui permet de tracer le polygone à partir des points des lignes"""


def tracerPolygone(listePositions: list):
    polygone(listePositions, couleur="blue", remplissage="blue", tag="aire")


"""La fonction qui permet de calculer l'aire des polygones"""


def calculAire(sommets):
    n = len(sommets)
    aire = 0
    for i in range(n):
        x1, y1 = sommets[i]
        x2, y2 = sommets[(i + 1) % n]
        aire += x1 * y2 - x2 * y1
    aire = abs(aire) / 2.0
    return aire


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
        epaisseur=5,
        couleur="blue",
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
    tailleJoueur = 20
    xJoueur = largeurFenetre // 2
    yJoueur = y_bas_contour - (tailleJoueur // 2)
    vitesseJoueur = 5
    player(xJoueur, yJoueur, tailleJoueur)
    vie = 3
    listePositionsLignes = []
    # ****************************************************************************************************************************
    """Boucle du jeu"""
    while True and vie > 0:
        if type_ev(donne_ev()) == "Quitte":
            break
        """Déplacement du Qix"""
        efface("txtAire")
        efface("fant")
        efface("player")
        fantome(x_fantome, y_fantome)
        player(xJoueur, yJoueur, tailleJoueur)
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
        if touche_pressee("Right") and (
            (xJoueur + (tailleJoueur // 2)) < x_droite_contour
            and touche_pressee("Up") == 0
            and touche_pressee("Down") == 0
        ):
            xJoueur += vitesseJoueur  # On fait déplacer le joueur à droite
            if (
                touche_pressee("Return")
                and (yJoueur + (tailleJoueur // 2)) != y_bas_contour
                and (yJoueur + (tailleJoueur // 2)) != y_haut_contour
                and (xJoueur + (tailleJoueur // 2)) != x_gauche_contour
                and (xJoueur + (tailleJoueur // 2)) != x_droite_contour
            ):  # Si la touche entrée est appuyée et que le joueur est bien positionné
                dessin(
                    xJoueur + (tailleJoueur // 2),
                    yJoueur + (tailleJoueur // 2),
                    xJoueur + (tailleJoueur // 2) + vitesseJoueur,
                    yJoueur + (tailleJoueur // 2),
                )  # On dessine la ligne qui va suivre le joueur
                listePositionsLignes.append(
                    (xJoueur + (tailleJoueur // 2), yJoueur + (tailleJoueur // 2))
                )  # On ajoute les positions des sommets des lignes afin de tracer le polygone
                if (
                    xJoueur < x_gauche_contour
                    or xJoueur + tailleJoueur > x_droite_contour
                    or yJoueur < y_haut_contour
                    or yJoueur + tailleJoueur > y_bas_contour
                ):
                    if len(listePositionsLignes) > 2:
                        if xJoueur < x_gauche_contour:
                            listePositionsLignes.append(listePositionsLignes[0])
                        tracerPolygone(listePositionsLignes)
                    listePositionsLignes = []

        """Si la touche flèche gauche est appuyée"""
        if touche_pressee("Left") and (
            (xJoueur + (tailleJoueur // 2)) > x_gauche_contour
            and touche_pressee("Up") == 0
            and touche_pressee("Down") == 0
        ):
            xJoueur -= vitesseJoueur
            if (
                touche_pressee("Return")
                and (yJoueur + (tailleJoueur // 2)) != y_bas_contour
                and (yJoueur + (tailleJoueur // 2)) != y_haut_contour
                and (xJoueur + (tailleJoueur // 2)) != x_gauche_contour
                and (xJoueur + (tailleJoueur // 2)) != x_droite_contour
            ):  # Si la touche entrée est appuyée et que le joueur est bien positionné
                dessin(
                    xJoueur + (tailleJoueur // 2),
                    yJoueur + (tailleJoueur // 2),
                    xJoueur + (tailleJoueur // 2) + vitesseJoueur,
                    yJoueur + (tailleJoueur // 2),
                )  # On dessine la ligne qui va suivre le joueur
                listePositionsLignes.append(
                    (xJoueur + (tailleJoueur // 2), yJoueur + (tailleJoueur // 2))
                )  # On ajoute les positions des sommets des lignes afin de tracer le polygone
                if (
                    xJoueur < x_gauche_contour
                    or xJoueur + tailleJoueur > x_droite_contour
                    or yJoueur < y_haut_contour
                    or yJoueur + tailleJoueur > y_bas_contour
                ):
                    if len(listePositionsLignes) > 2:
                        if xJoueur < x_gauche_contour:
                            listePositionsLignes.append(listePositionsLignes[0])
                        tracerPolygone(listePositionsLignes)
                    listePositionsLignes = []

        """Si la touche flèche haut est appuyée et que les autres touches ne sont pas appuyées"""
        if touche_pressee("Up") and ((yJoueur + (tailleJoueur // 2)) > y_haut_contour):
            yJoueur -= vitesseJoueur
            if (
                touche_pressee("Return")
                and (yJoueur + (tailleJoueur // 2)) != y_bas_contour
                and (yJoueur + (tailleJoueur // 2)) != y_haut_contour
                and (xJoueur + (tailleJoueur // 2)) != x_gauche_contour
                and (xJoueur + (tailleJoueur // 2)) != x_droite_contour
            ):  # Si la touche entrée est appuyée et que le joueur est bien positionné
                dessin(
                    xJoueur + (tailleJoueur // 2),
                    yJoueur + (tailleJoueur // 2),
                    xJoueur + (tailleJoueur // 2),
                    yJoueur + (tailleJoueur // 2) + vitesseJoueur,
                )  # On dessine la ligne qui va suivre le joueur
                listePositionsLignes.append(
                    (xJoueur + (tailleJoueur // 2), yJoueur + (tailleJoueur // 2))
                )  # On ajoute les positions des sommets des lignes afin de tracer le polygone
                if (
                    xJoueur < x_gauche_contour
                    or xJoueur + tailleJoueur > x_droite_contour
                    or yJoueur < y_haut_contour
                    or yJoueur + tailleJoueur > y_bas_contour
                ):
                    if len(listePositionsLignes) > 2:
                        if xJoueur < x_gauche_contour:
                            listePositionsLignes.append(listePositionsLignes[0])
                        tracerPolygone(listePositionsLignes)
                    listePositionsLignes = []

        """Si la touche flèche bas est appuyée et que les autres touches ne sont pas appuyées"""
        if touche_pressee("Down") and ((yJoueur + (tailleJoueur // 2)) < y_bas_contour):
            yJoueur += vitesseJoueur
            if (
                touche_pressee("Return")
                and (yJoueur + (tailleJoueur // 2)) != y_bas_contour
                and (yJoueur + (tailleJoueur // 2)) != y_haut_contour
                and (xJoueur + (tailleJoueur // 2)) != x_gauche_contour
                and (xJoueur + (tailleJoueur // 2)) != x_droite_contour
            ):  # Si la touche entrée est appuyée et que le joueur est bien positionné
                dessin(
                    xJoueur + (tailleJoueur // 2),
                    yJoueur + (tailleJoueur // 2),
                    xJoueur + (tailleJoueur // 2),
                    yJoueur + (tailleJoueur // 2) + vitesseJoueur,
                )  # On dessine la ligne qui va suivre le joueur
                listePositionsLignes.append(
                    (xJoueur + (tailleJoueur // 2), yJoueur + (tailleJoueur // 2))
                )  # On ajoute les positions des sommets des lignes afin de tracer le polygone
                if (
                    xJoueur < x_gauche_contour
                    or xJoueur + tailleJoueur > x_droite_contour
                    or yJoueur < y_haut_contour
                    or yJoueur + tailleJoueur > y_bas_contour
                ):
                    if len(listePositionsLignes) > 2:
                        if xJoueur < x_gauche_contour:
                            listePositionsLignes.append(listePositionsLignes[0])
                        tracerPolygone(listePositionsLignes)
                    listePositionsLignes = []
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

        # ****************************************************************************************************************************
        """On affiche l'aire des polygones"""
        texte(
            700,
            100,
            chaine=calculAire(listePositionsLignes),
            couleur="red",
            tag="txtAire",
        )

        mise_a_jour()

# ****************************************************************************************************************************
if vie < 1:
    texte(400, 400, chaine="PERDU", couleur="red")
sleep(3)  # Attente de 3 secondes
ferme_fenetre()  # Fermer la fenêtre