from fltk import *

def joueur(x: int, y: int, taille=5):
    """Dessine le joueur"""
    cercle(x, y, taille, couleur="lime", tag="joueur")

def dessin(ax: int, ay: int, bx: int, by: int):
    ligne(ax, ay, bx, by, couleur="white", tag="dessin")

def mise_a_jour_direction(direction):
    nouvelle_dir = direction
    ev = donne_ev()
    t_ev = type_ev(ev)
    if t_ev == "Touche":
        t = touche(ev)
        if t == "Right":
            nouvelle_dir = "droite"
        elif t == "Left":
            nouvelle_dir = "gauche"
        if t == "Up":
            nouvelle_dir = "haut"
        elif t == "Down":
            nouvelle_dir = "bas"
    return nouvelle_dir

def tracerPolygone(listePositions: list):
    polygone(listePositions, couleur="lime", remplissage="red", tag="aire")

largeurFenetre = 1500
hauteurFenetre = 900

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

lstBords = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
lstPositions = []

# Boucle principale pour traiter les événements
while True:
    ev = donne_ev()
    if ev is not None:
        if type_ev(ev) == "Touche":
            # Sauvegarde les anciennes coordonnées
            oldX, oldY = xJoueur, yJoueur

            # Déplace le joueur uniquement le long des bords
            if touche(ev) == "Up" and yJoueur > y1:
                yJoueur -= tailleJoueur
                if touche_pressee("Return"):
                    dessin(xJoueur, yJoueur, xJoueur, yJoueur + tailleJoueur)
            elif touche(ev) == "Down" and yJoueur < y2:
                yJoueur += tailleJoueur
                if touche_pressee("Return"):
                    dessin(xJoueur, yJoueur, xJoueur, yJoueur - tailleJoueur)
            elif touche(ev) == "Left" and xJoueur > x1:
                xJoueur -= tailleJoueur
                if touche_pressee("Return"):
                    dessin(xJoueur, yJoueur, xJoueur + tailleJoueur, yJoueur)
            elif touche(ev) == "Right" and xJoueur < x2:
                xJoueur += tailleJoueur
                if touche_pressee("Return"):
                    dessin(xJoueur, yJoueur, xJoueur - tailleJoueur, yJoueur)

            efface("joueur")
            joueur(xJoueur, yJoueur)
    mise_a_jour()