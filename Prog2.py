from fltk import *

def joueur(x: int, y: int, taille=5):
    """Dessine le joueur"""
    cercle(x, y, taille, couleur="lime", tag="joueur")

def dessin(ax: int, ay: int, bx: int, by: int):
    ligne(ax, ay, bx, by, couleur="lime", tag="dessin")

def tracerPolygone(listePositions: list):
    polygone(listePositions, couleur="blue", remplissage="blue", tag="aire")

largeurFenetre = 1500
hauteurFenetre = 1000

cree_fenetre(largeurFenetre, hauteurFenetre)
rectangle(0, 0, largeurFenetre, hauteurFenetre, remplissage="black")
x1 = 375
x2 = 1100
y1 = 200
y2 = 800
rectangle(x1, y1, x2, y2, couleur="white")

xJoueur = x2-x1
yJoueur = y2
tailleJoueur = 5

cercle(xJoueur, yJoueur, tailleJoueur, couleur="lime", tag="joueur")

lstBords = [(x1,y1), (x2,y1), (x2,y2), (x1,y2)]

# Boucle principale pour traiter les événements
while True:
    ev = donne_ev()
    if ev is not None:
        if type_ev(ev) == "Touche":
            # Sauvegarde les anciennes coordonnées
            oldX, oldY = xJoueur, yJoueur

            # Déplace le joueur selon les touches flèche
            if touche(ev) == "Up":
                yJoueur -= tailleJoueur
                if touche_pressee("Return"):
                    dessin(xJoueur,yJoueur,xJoueur,yJoueur+tailleJoueur)
            elif touche(ev) == "Down":
                yJoueur += tailleJoueur
                if touche_pressee("Return"):
                    dessin(xJoueur,yJoueur,xJoueur,yJoueur-tailleJoueur)
            elif touche(ev) == "Left":
                xJoueur -= tailleJoueur
                if touche_pressee("Return"):
                    dessin(xJoueur,yJoueur,xJoueur+tailleJoueur,yJoueur)
            elif touche(ev) == "Right":
                xJoueur += tailleJoueur
                if touche_pressee("Return"):
                    dessin(xJoueur,yJoueur,xJoueur-tailleJoueur,yJoueur)

            # Vérifie les limites du rectangle
            if xJoueur < x1 or xJoueur > x2 or yJoueur < y1 or yJoueur > y2:
                # Si les nouvelles coordonnées sont en dehors, restaure les anciennes
                xJoueur, yJoueur = oldX, oldY

            # Efface la fenêtre et redessine le joueur
            efface("joueur")
            joueur(xJoueur, yJoueur)

    mise_a_jour()