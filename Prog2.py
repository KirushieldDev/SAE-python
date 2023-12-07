from fltk import *

def joueur(x: int, y: int, taille=5):
    cercle(x, y, taille, couleur="lime", tag="joueur")

def dessin(ax: int, ay: int, bx: int, by: int):
    ligne(ax, ay, bx, by, couleur="white", tag="dessin")

def tracerPolygone(listePositions: list):
    if len(listePositions) >= 3:
        polygone(listePositions, couleur="white", epaisseur=2, remplissage="green", tag="aire")

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
listePositionsLignes = []

while True:
    ev = donne_ev()
    if ev is not None:
        if type_ev(ev) == "Quitte":
            break
        if type_ev(ev) == "Touche":
            oldX, oldY = xJoueur, yJoueur

            if touche(ev) == "Up" and yJoueur > y1:
                yJoueur -= tailleJoueur
                if touche_pressee("Return"):
                    dessin(oldX, oldY, oldX, yJoueur)
                    listePositionsLignes.append((oldX, oldY, oldX, yJoueur))
                    
            elif touche(ev) == "Down" and yJoueur < y2:
                yJoueur += tailleJoueur
                if touche_pressee("Return"):
                    dessin(oldX, oldY, oldX, yJoueur)
                    listePositionsLignes.append((oldX, oldY, oldX, yJoueur))
                        
            elif touche(ev) == "Left" and xJoueur > x1:
                xJoueur -= tailleJoueur
                if touche_pressee("Return"):
                    dessin(oldX, oldY, xJoueur, oldY)
                    listePositionsLignes.append((oldX, oldY, xJoueur, oldY))

            elif touche(ev) == "Right" and xJoueur < x2:
                xJoueur += tailleJoueur
                if touche_pressee("Return"):
                    dessin(oldX, oldY, xJoueur, oldY)
                    listePositionsLignes.append((oldX, oldY, xJoueur, oldY))

            efface("joueur")
            joueur(xJoueur, yJoueur)
            
        tracerPolygone(listePositionsLignes)
    mise_a_jour()

ferme_fenetre()