from fltk import *
from random import randint

def joueur(x: int, y: int, taille=5):
    cercle(x, y, taille, couleur="lime", tag="joueur")

def dessin(ax: int, ay: int, bx: int, by: int):
    ligne(ax, ay, bx, by, couleur="white", tag="dessin")

def tracerPolygone(listePositions: list):
    if len(listePositions) >= 3:
        polygone(listePositions, couleur="white", remplissage="green", tag="aire")

largeurFenetre = 1500
hauteurFenetre = 900

cree_fenetre(largeurFenetre, hauteurFenetre)
rectangle(0, 0, largeurFenetre, hauteurFenetre, remplissage="black")
x1 = 300
x2 = 1200
y1 = 200
y2 = 800
rectangle(x1, y1, x2, y2, couleur="white")
ligne(x1, y1-30, x2, y1-30, couleur="red", epaisseur=5)
# Logo Qix
image(500, 100, "Qix.gif", ancrage="center", tag="im")

xJoueur = (x2 + x1) // 2
yJoueur = y2
tailleJoueur = 5
enTrainDeDessiner = False

cercle(xJoueur, yJoueur, tailleJoueur, couleur="lime", tag="joueur")

lstBords = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
listePositionsLignes = []
listePositionsPolygone = []

# Initialiser les pommes
nombre_pommes = 5  # Choisissez le nombre initial de pommes
pommes = [(randint(x1, x2), randint(y1, y2)) for _ in range(nombre_pommes)]

def dessiner_pommes():
    for pomme in pommes:
        cercle(pomme[0], pomme[1], 5, couleur="red", tag="pomme")

while True:
    ev = donne_ev()
    if ev is not None:
        if type_ev(ev) == "Quitte":
            break
        if type_ev(ev) == "Touche":
            oldX, oldY = xJoueur, yJoueur

            if touche(ev) == "Up" and yJoueur > y1:
                yJoueur -= tailleJoueur
                if enTrainDeDessiner:
                    dessin(oldX, oldY, oldX, yJoueur)
                    listePositionsLignes.append((oldX, oldY, oldX, yJoueur))
                    if (xJoueur <= x1 or xJoueur >= x2 or yJoueur <= y1 or yJoueur >= y2):
                        dernierPoint = listePositionsLignes[-1][2:]
                        listePositionsLignes.append((xJoueur, yJoueur, *dernierPoint))
                        tracerPolygone(listePositionsLignes)
                        listePositionsPolygone.extend(listePositionsLignes)
                        listePositionsLignes = []
                        enTrainDeDessiner = not enTrainDeDessiner

            elif touche(ev) == "Down" and yJoueur < y2:
                yJoueur += tailleJoueur
                if enTrainDeDessiner:
                    dessin(oldX, oldY, oldX, yJoueur)
                    listePositionsLignes.append((oldX, oldY, oldX, yJoueur))
                    if (xJoueur <= x1 or xJoueur >= x2 or yJoueur <= y1 or yJoueur >= y2):
                        dernierPoint = listePositionsLignes[-1][2:]
                        listePositionsLignes.append((xJoueur, yJoueur, *dernierPoint))
                        tracerPolygone(listePositionsLignes)
                        listePositionsPolygone.extend(listePositionsLignes)
                        listePositionsLignes = []
                        enTrainDeDessiner = not enTrainDeDessiner

            elif touche(ev) == "Left" and xJoueur > x1:
                xJoueur -= tailleJoueur
                if enTrainDeDessiner:
                    dessin(oldX, oldY, xJoueur, oldY)
                    listePositionsLignes.append((oldX, oldY, xJoueur, oldY))
                    if (xJoueur <= x1 or xJoueur >= x2 or yJoueur <= y1 or yJoueur >= y2):
                        dernierPoint = listePositionsLignes[-1][2:]
                        listePositionsLignes.append((xJoueur, yJoueur, *dernierPoint))
                        tracerPolygone(listePositionsLignes)
                        listePositionsPolygone.extend(listePositionsLignes)
                        listePositionsLignes = []
                        enTrainDeDessiner = not enTrainDeDessiner

            elif touche(ev) == "Right" and xJoueur < x2:
                xJoueur += tailleJoueur
                if enTrainDeDessiner:
                    dessin(oldX, oldY, xJoueur, oldY)
                    listePositionsLignes.append((oldX, oldY, xJoueur, oldY))
                    if (xJoueur <= x1 or xJoueur >= x2 or yJoueur <= y1 or yJoueur >= y2):
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

            # Vérifier si le joueur touche une pomme
            for pomme in pommes:
                distance = ((pomme[0] - xJoueur) ** 2 + (pomme[1] - yJoueur) ** 2) ** 0.5
                if distance < tailleJoueur + 5:  # Ajustez la tolérance selon vos besoins
                    pommes.remove(pomme)
                    efface("pomme")  # Effacer toutes les pommes
                    dessiner_pommes()  # Redessiner les pommes restantes

    dessiner_pommes()
    mise_a_jour()

ferme_fenetre()