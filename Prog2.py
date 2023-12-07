from fltk import *

def joueur(x: int, y: int, taille=5):
    """Dessine le joueur"""
    cercle(x, y, taille, couleur="lime", tag="joueur")

def dessin(ax: int, ay: int, bx: int, by: int):
    ligne(ax, ay, bx, by, couleur="lime", tag="dessin")

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

joueur(xJoueur, yJoueur)

lstBords = [(x1,y1), (x2,y1), (x2,y2), (x1,y2)]

# Boucle principale pour traiter les événements
while True:
    if type_ev(donne_ev()) == "Quitte":
        break
    efface("joueur")
    ev = donne_ev()
    if ev is not None:
        if type_ev(ev) == "Touche":
            pass

        joueur

    mise_a_jour()

ferme_fenetre()