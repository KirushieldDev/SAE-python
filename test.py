from fltk import *

def joueur(x: int, y: int, taille=5):
    """Dessine le joueur"""
    cercle(x, y, taille, couleur="lime", tag="joueur")

def dessin(ax: int, ay: int, bx: int, by: int):
    ligne(ax, ay, bx, by, couleur="white", tag="dessin")

def tracerPolygone(listePositions: list):
    polygone(listePositions, couleur="white", epaisseur=3, remplissage="red", tag="aire")

largeurFenetre = 1500
hauteurFenetre = 1000

cree_fenetre(largeurFenetre, hauteurFenetre)
rectangle(0, 0, largeurFenetre, hauteurFenetre, remplissage="black")
x1 = 375
x2 = 1100
y1 = 200
y2 = 800
rectangle(x1, y1, x2, y2, couleur="white")

xJoueur = x2 - x1
yJoueur = y2
tailleJoueur = 5

cercle(xJoueur, yJoueur, tailleJoueur, couleur="lime", tag="joueur")
arc_point = []
lstBords = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]

# Boucle principale pour traiter les événements
while True:
    ev = donne_ev()
    if ev is not None:
        if type_ev(ev) == "Touche":
            # Sauvegarde les anciennes coordonnées
            oldX, oldY = xJoueur, yJoueur
            positionJoueur = (xJoueur,yJoueur)
            # Déplace le joueur uniquement le long des bords
            if touche(ev) == "Up" and yJoueur > y1:
                yJoueur -= tailleJoueur
                if touche_pressee("Return"):
                    dessin(xJoueur, yJoueur, xJoueur, yJoueur + tailleJoueur)
                    arc_point.append(positionJoueur)
            elif touche(ev) == "Down" and yJoueur < y2:
                yJoueur += tailleJoueur
                if touche_pressee("Return"):
                    dessin(xJoueur, yJoueur, xJoueur, yJoueur - tailleJoueur)
                    arc_point.append(positionJoueur)
            elif touche(ev) == "Left" and xJoueur > x1:
                xJoueur -= tailleJoueur
                if touche_pressee("Return"):
                    dessin(xJoueur, yJoueur, xJoueur + tailleJoueur, yJoueur)
                    arc_point.append(positionJoueur)
            elif touche(ev) == "Right" and xJoueur < x2:
                xJoueur += tailleJoueur
                if touche_pressee("Return"):
                    dessin(xJoueur, yJoueur, xJoueur - tailleJoueur, yJoueur)
                    arc_point.append(positionJoueur)
            if xJoueur == x1 and y1 <= yJoueur and yJoueur >= y2 or xJoueur == x2 and y1 <= yJoueur and yJoueur >= y2 or yJoueur == y1 and x1 <= xJoueur and xJoueur >= x2 or yJoueur == y2 and x1 <= xJoueur and xJoueur >= x2 :
                if positionJoueur in arc_point:
                    tracerPolygone(arc_point)

            # Efface la fenêtre et redessine le joueur
            efface("joueur")
            joueur(xJoueur, yJoueur)

    mise_a_jour()