from fltk import *
from random import randint

def joueur(x: int, y: int, taille=5):
    cercle(x, y, taille, couleur="lime", tag="joueur")

def dessin(ax: int, ay: int, bx: int, by: int):
    ligne(ax, ay, bx, by, couleur="white", tag="dessin")

def tracerPolygone(listePositions: list):
    if len(listePositions) >= 3:
        polygone(listePositions, couleur="white", remplissage="green", tag="aire")

def dessiner_obstacles(obstacles):
    for obstacle in obstacles:
        rectangle(obstacle[0], obstacle[1], obstacle[2], obstacle[3], couleur="gray", remplissage="gray", tag="obstacle")

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

nombre_pommes = 5
pommes = [(randint(x1, x2), randint(y1, y2)) for _ in range(nombre_pommes)]

nombre_obstacles = randint(1, 5)
obstacles = []
for _ in range(nombre_obstacles):
    taille_obstacle = randint(20, 50)
    x_obstacle = randint(x1, x2 - taille_obstacle)
    y_obstacle = randint(y1, y2 - taille_obstacle)
    obstacles.append((x_obstacle, y_obstacle, x_obstacle + taille_obstacle, y_obstacle + taille_obstacle))

def dessiner_pommes():
    for pomme in pommes:
        cercle(pomme[0], pomme[1], 5, couleur="red", tag="pomme", remplissage="red")

def peut_deplacer_nouvelle_position(x, y):
    for obstacle in obstacles:
        if obstacle[0] <= x <= obstacle[2] and obstacle[1] <= y <= obstacle[3]:
            return False
    return True

def deplacer_joueur_nouvelle_position(dx, dy):
    new_x, new_y = xJoueur + dx, yJoueur + dy
    if x1 <= new_x <= x2 and y1 <= new_y <= y2 and peut_deplacer_nouvelle_position(new_x, new_y):
        return new_x, new_y
    return xJoueur, yJoueur

while True:
    ev = donne_ev()
    if ev is not None:
        if type_ev(ev) == "Quitte":
            break
        if type_ev(ev) == "Touche":
            oldX, oldY = xJoueur, yJoueur

            if touche(ev) == "Up":
                xJoueur, yJoueur = deplacer_joueur_nouvelle_position(0, -tailleJoueur)
            elif touche(ev) == "Down":
                xJoueur, yJoueur = deplacer_joueur_nouvelle_position(0, tailleJoueur)
            elif touche(ev) == "Left":
                xJoueur, yJoueur = deplacer_joueur_nouvelle_position(-tailleJoueur, 0)
            elif touche(ev) == "Right":
                xJoueur, yJoueur = deplacer_joueur_nouvelle_position(tailleJoueur, 0)

            if enTrainDeDessiner and peut_deplacer_nouvelle_position(xJoueur, yJoueur):
                dessin(oldX, oldY, xJoueur, yJoueur)
                listePositionsLignes.append((oldX, oldY, xJoueur, yJoueur))
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

            for pomme in pommes:
                distance = ((pomme[0] - xJoueur) ** 2 + (pomme[1] - yJoueur) ** 2) ** 0.5
                if distance < tailleJoueur + 5:
                    pommes.remove(pomme)
                    efface("pomme")
                    dessiner_pommes()

    dessiner_pommes()
    dessiner_obstacles(obstacles)
    mise_a_jour()

ferme_fenetre()