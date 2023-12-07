from fltk import *

def joueur(x: int, y: int, taille=5):
    """Dessine le joueur"""
    cercle(x, y, taille, couleur="lime")

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
    ev = donne_ev()
    if ev is not None:
        if type_ev(ev) == "Touche":
            # Sauvegarde les anciennes coordonnées
            oldX, oldY = xJoueur, yJoueur

            # Déplace le joueur selon les touches flèche
            if touche(ev) == "Up":
                yJoueur -= tailleJoueur
            elif touche(ev) == "Down":
                yJoueur += tailleJoueur
            elif touche(ev) == "Left":
                xJoueur -= tailleJoueur
            elif touche(ev) == "Right":
                xJoueur += tailleJoueur

            # Vérifie les limites du rectangle
            if xJoueur < x1 or xJoueur > x2 or yJoueur < y1 or yJoueur > y2:
                # Si les nouvelles coordonnées sont en dehors, restaure les anciennes
                xJoueur, yJoueur = oldX, oldY

            # Efface la fenêtre et redessine le joueur
            efface_tout()
            rectangle(0, 0, largeurFenetre, hauteurFenetre, remplissage="black")
            rectangle(x1, y1, x2, y2, couleur="white")
            joueur(xJoueur, yJoueur)

    mise_a_jour()