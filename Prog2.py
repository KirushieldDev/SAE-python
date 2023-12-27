from fltk import *
from random import randint
import time

invincible = False


def joueur(x: int, y: int, taille=5):
    if not invincible:
        cercle(x, y, taille, couleur="lime", tag="joueur")
    else:
        cercle(x, y, taille, couleur="red", tag="joueur")


def dessin(ax: int, ay: int, bx: int, by: int):
    ligne(ax, ay, bx, by, couleur="white", tag="dessin")


def tracerPolygone(listePositions: list, start_position: tuple, end_position: tuple,x_fantome: int,y_fantome: int):
    fantome_est_dedans = intersection_test(x_fantome,y_fantome,listePositions)
    if (
        start_position[0] > x1
        and start_position[0] < x2
        and start_position[1] == y2
        and end_position[0] == x1
        and end_position[1] > y1
        and end_position[1] < y2
    ) :
        if fantome_est_dedans is False :
            listePositions.append((x1, y2))
        else :
            listePositions.append((x1,y1))
            listePositions.append((x2,y1))
            listePositions.append((x2,y2))
        
    if (
        start_position[0] == x1
        and start_position[1] > y1
        and start_position[1] < y2
        and end_position[0] > x1
        and end_position[0] < x2
        and end_position[1] == y2
    ): 
        if fantome_est_dedans is False :
            listePositions.append((x1, y2))
        else :
            listePositions.append((x2,y2))
            listePositions.append((x2,y1))
            listePositions.append((x1,y1))
        

    if (
        start_position[0] == x1
        and start_position[1] > y1
        and start_position[1] < y2
        and end_position[0] > x1
        and end_position[0] < x2
        and end_position[1] == y1
    ) : 
        if fantome_est_dedans is False :
            listePositions.append((x1,y1))
        else :
            listePositions.append((x2,y1))
            listePositions.append((x2,y2))
            listePositions.append((x1, y2))
    if (
        start_position[0] > x1
        and start_position[0] < x2
        and start_position[1] == y1
        and end_position[0] == x1
        and end_position[1] > y1
        and end_position[1] < y2
    ):
        if fantome_est_dedans is False :
            listePositions.append((x1,y1))
        else :
            listePositions.append((x1, y2))
            listePositions.append((x2,y2))
            listePositions.append((x2,y1))
    if (
        start_position[0] > x1
        and start_position[0] < x2
        and start_position[1] == y1
        and end_position[0] == x2
        and end_position[1] > y1
        and end_position[1] < y2
    ) :
        if fantome_est_dedans is False :
            listePositions.append((x2,y1))
        else :
            listePositions.append((x2,y2))
            listePositions.append((x1, y2))
            listePositions.append((x1,y1))
    if (
        start_position[0] == x2
        and start_position[1] > y1
        and start_position[1] < y2
        and end_position[0] > x1
        and end_position[0] < x2
        and end_position[1] == y1
    ):
        if fantome_est_dedans is False :
            listePositions.append((x2,y1))
        else :
            listePositions.append((x1,y1))
            listePositions.append((x1, y2))
            listePositions.append((x2,y2))

    if (
        start_position[0] == x2
        and start_position[1] > y1
        and start_position[1] < y2
        and end_position[0] > x1
        and end_position[0] < x2
        and end_position[1] == y2
    ) :
        if fantome_est_dedans is False :
            listePositions.append((x2,y2))
        else :
            listePositions.append((x1, y2))
            listePositions.append((x1,y1))
            listePositions.append((x2,y1))
    
    if (
        start_position[0] > x1
        and start_position[0] < x2
        and start_position[1] == y2
        and end_position[0] == x2
        and end_position[1] > y1
        and end_position[1] < y2
    ):
        if fantome_est_dedans is False :
            listePositions.append((x2,y2))
        else :
            listePositions.append((x2,y1))
            listePositions.append((x1,y1))
            listePositions.append((x1, y2))

    if (
        start_position[0] == x2
        and start_position[1] > y1
        and start_position[1] < y2
        and end_position[1] > y1
        and end_position[1] < y2
        and end_position[0] == x1
    ) :
        if fantome_est_dedans is False :
            listePositions.append((x1,y1))
            listePositions.append((x2,y1))
        else :
            listePositions.append((x1, y2))
            listePositions.append((x2,y2))
    
    if (
        start_position[1] > y1
        and start_position[1] < y2
        and start_position[0] == x1
        and end_position[0] == x2
        and end_position[1] > y1
        and end_position[1] < y2
    ):
        if fantome_est_dedans is False :
            listePositions.append((x2,y1))
            listePositions.append((x1,y1))
        else :
            listePositions.append((x2,y2))
            listePositions.append((x1, y2))

    polygone(listePositions, couleur="white", remplissage="green", tag="aire")
    
    
def intersection_test(x, y, polygone):
    intersections = 0
    for i in range(len(polygone)):
        x1, y1 = polygone[i][2],polygone[i][3]
        x2, y2 = polygone[(i + 1) % len(polygone)][2],polygone[(i + 1) % len(polygone)][3]
        
        # Vérifie si le point se trouve à gauche du segment de bord
        if y > min(y1, y2) and y <= max(y1, y2) and x <= max(x1, x2) and y1 != y2:
            intersection_x = (y - y1) * (x2 - x1) / (y2 - y1) + x1
            if x1 == x2 or x <= intersection_x:
                intersections += 1

    return intersections % 2 == 1  # Si le nombre d'intersections est impair, le point est à l'intérieur

def dessiner_obstacles(obstacles):
    for obstacle in obstacles:
        rectangle(
            obstacle[0],
            obstacle[1],
            obstacle[2],
            obstacle[3],
            couleur="gray",
            remplissage="gray",
            tag="obstacle",
        )


"""Création du Qix"""


def fantome(x, y):
    largeurFantome = 70
    hauteurFantome = 80
    image(
        x,
        y,
        "Qix2.gif",
        largeurFantome,
        hauteurFantome,
        ancrage="center",
        tag="fant",
    )
    return x, y


# ****************************************************************************************************************************
"""Création des sparx"""


def sparx1(x, y):
    largeurSparx = 40
    hauteurSparx = 40
    image(x, y, "Sparx.gif", largeurSparx, hauteurSparx, ancrage="center", tag="spar1")
    return x, y


def sparx2(x, y):
    largeurSparx = 40
    hauteurSparx = 40
    image(x, y, "Sparx.gif", largeurSparx, hauteurSparx, ancrage="center", tag="spar2")
    return x, y


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


# ****************************************************************************************************************************

"""La fonction qui permet de vérifier si le joueur touche le qix"""


def checkQixPlayer(
    xJoueur: float, yJoueur: float, xQix: float, yQix: float, tailleJoueur: int
) -> bool:
    if (
        (xJoueur + (tailleJoueur // 2) >= xQix - 80 // 2)
        and ((xJoueur + tailleJoueur) <= (xQix + 80 // 2))
        and (yJoueur + (tailleJoueur // 2) >= yQix - 90 // 2)
        and ((yJoueur + tailleJoueur) <= (yQix + 90 // 2))
    ):
        return True
    else:
        return False


def dessiner_pommes():
    for pomme in pommes:
        cercle(pomme[0], pomme[1], 5, couleur="red", remplissage="red", tag="pomme")


def peut_deplacer_nouvelle_position(x, y):
    for obstacle in obstacles:
        if obstacle[0] <= x <= obstacle[2] and obstacle[1] <= y <= obstacle[3]:
            return False
    return True


def deplacer_joueur(dx, dy):
    new_x, new_y = xJoueur + dx, yJoueur + dy
    if (
        x1 <= new_x <= x2
        and y1 <= new_y <= y2
        and peut_deplacer_nouvelle_position(new_x, new_y)
    ):
        return new_x, new_y
    return xJoueur, yJoueur


if __name__ == "__main__":
    largeurFenetre = 1500
    hauteurFenetre = 900

    cree_fenetre(largeurFenetre, hauteurFenetre)
    rectangle(0, 0, largeurFenetre, hauteurFenetre, remplissage="black")
    global x1, x2, y1, y2
    x1 = 300
    x2 = 1200
    y1 = 200
    y2 = 800
    rectangle(x1, y1, x2, y2, couleur="white")
    ligne(x1 + 10, y1 - 10, x2 - 10, y1 - 10, couleur="red", epaisseur=5)
    # Logo Qix
    image(480, 115, "Qix.gif", ancrage="center", tag="im")

    xJoueur = (x2 + x1) // 2
    yJoueur = y2
    tailleJoueur = 5
    vitesseJoueur = 5
    enTrainDeDessiner = False

    """Position du Qix"""
    x_fantome = (x1 + x2) // 2
    y_fantome = (y1 + y2) // 2
    speedXFantome = 0
    speedYFantome = 0
    positionFantome = (x_fantome, y_fantome)
    # ****************************************************************************************************************************
    """Position des sparx"""
    x_sparx1 = 750
    y_sparx1 = y1
    x_sparx2 = 750
    y_sparx2 = y1
    speedSparx = 3
    fantome(750, 550)

    cercle(xJoueur, yJoueur, tailleJoueur, couleur="lime", tag="joueur")

    lstBords = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
    listePositionsLignes = []
    listePositionsPolygone = []

    nombre_pommes = randint(5, 8)
    pommes = [(randint(x1, x2), randint(y1, y2)) for _ in range(nombre_pommes)]

    nombre_obstacles = randint(1, 5)
    obstacles = []

    for _ in range(nombre_obstacles):
        taille_obstacle = randint(20, 50)
        x_obstacle = randint(x1, x2 - taille_obstacle)
        y_obstacle = randint(y1, y2 - taille_obstacle)
        obstacles.append(
            (
                x_obstacle,
                y_obstacle,
                x_obstacle + taille_obstacle,
                y_obstacle + taille_obstacle,
            )
        )

    vie = 3
    temps_initial = 0

    while True and vie != 0:
        """Déplacement du Qix"""
        efface("txtAire")
        efface("fant")

        fantome(x_fantome, y_fantome)
        joueur(xJoueur, yJoueur, tailleJoueur)
        positionJoueur = (xJoueur, yJoueur)

        x_fantome += speedXFantome
        y_fantome -= speedYFantome
        # Collisions du Qix
        if x_fantome >= x2 - 35 or x_fantome <= x1 + 35:
            speedXFantome = -speedXFantome

        if y_fantome >= y2 - 40 or y_fantome <= y1 + 40:
            speedYFantome = -speedYFantome

        for i in range(len(listePositionsLignes)):
            if positionFantome == listePositionsLignes[i]:
                speedXFantome = -speedXFantome
                speedYFantome = -speedYFantome

        # ****************************************************************************************************************************
        """Déplacement des sparx"""
        efface("spar1")
        sparx1(x_sparx1, y_sparx1)

        if y_sparx1 <= y1:
            x_sparx1 += speedSparx

        if x_sparx1 >= x2:
            x_sparx1 = 1200
            y_sparx1 += speedSparx

        if y_sparx1 >= y2:
            y_sparx1 = y2
            x_sparx1 -= speedSparx

        if x_sparx1 <= x1:
            x_sparx1 = x1
            y_sparx1 -= speedSparx

        efface("spar2")
        sparx2(x_sparx2, y_sparx2)

        if y_sparx2 <= y1:
            x_sparx2 -= speedSparx

        if x_sparx2 <= x1:
            x_sparx2 = 300
            y_sparx2 += speedSparx

        if y_sparx2 >= y2:
            y_sparx2 = y2
            x_sparx2 += speedSparx

        if x_sparx2 >= x2:
            x_sparx2 = x2
            y_sparx2 -= speedSparx
        ev = donne_ev()
        if ev is not None:
            if type_ev(ev) == "Quitte":
                break
            if type_ev(ev) == "Touche":
                oldX, oldY = xJoueur, yJoueur

                if touche(ev) == "Up":
                    xJoueur, yJoueur = deplacer_joueur(
                        0, -vitesseJoueur
                    )
                elif touche(ev) == "Down":
                    xJoueur, yJoueur = deplacer_joueur(
                        0, vitesseJoueur
                    )
                elif touche(ev) == "Left":
                    xJoueur, yJoueur = deplacer_joueur(
                        -vitesseJoueur, 0
                    )
                elif touche(ev) == "Right":
                    xJoueur, yJoueur = deplacer_joueur(
                        vitesseJoueur, 0
                    )

                if enTrainDeDessiner and peut_deplacer_nouvelle_position(
                    xJoueur, yJoueur
                ):
                    dessin(oldX, oldY, xJoueur, yJoueur)
                    listePositionsLignes.append((oldX, oldY, xJoueur, yJoueur))
                    if xJoueur <= x1 or xJoueur >= x2 or yJoueur <= y1 or yJoueur >= y2:
                        end_position = (xJoueur, yJoueur)
                        dernierPoint = listePositionsLignes[-1][2:]
                        listePositionsLignes.append((xJoueur, yJoueur, *dernierPoint))
                        tracerPolygone(
                            listePositionsLignes, start_position, end_position,x_fantome,y_fantome
                        )
                        listePositionsPolygone.extend(listePositionsLignes)
                        listePositionsLignes = []
                        enTrainDeDessiner = not enTrainDeDessiner

                efface("joueur")
                joueur(xJoueur, yJoueur)

                if touche(ev) == "Return":
                    start_position = (xJoueur, yJoueur)
                    enTrainDeDessiner = not enTrainDeDessiner

                for pomme in pommes:
                    distance = (
                        (pomme[0] - xJoueur) ** 2 + (pomme[1] - yJoueur) ** 2
                    ) ** 0.5
                    if distance < tailleJoueur + 5:
                        pommes.remove(pomme)
                        efface("pomme")
                        dessiner_pommes()
                        if invincible == False:
                            invincible = True
                            temps_initial_invincible = time.time()

                if touche(ev) == "space" and not enTrainDeDessiner:
                    vitesseJoueur += 5

        """On affiche le nombre de vies"""
        efface("txtvie")
        texte(
            700,
            50,
            chaine=f"Vie : {vie}",
            couleur="white",
            tag="txtvie",
        )

        if invincible == False:
            if (
                checkSparxPlayer(
                    xJoueur,
                    yJoueur,
                    x_sparx1,
                    y_sparx1,
                    x_sparx2,
                    y_sparx2,
                    tailleJoueur,
                )
                == True
            ):
                vie -= 1
                xJoueur = (x1 + x2) / 2
                yJoueur = y2
                listePositionsPolygone.clear()

            if (
                checkQixPlayer(xJoueur, yJoueur, x_fantome, y_fantome, tailleJoueur)
                == True
            ):
                vie -= 1
                xJoueur = (x1 + x2) / 2
                yJoueur = y2
                listePositionsPolygone.clear()
                x_sparx1 = 755
                y_sparx1 = 200
                x_sparx2 = 745
                y_sparx2 = 200

        if invincible and time.time() - temps_initial_invincible < 3:
            texte(700, 100, chaine="Invincible", couleur="white", tag="txtinvin")
        else:
            invincible = False
            efface("txtinvin")
        
        print(listePositionsLignes)
        dessiner_pommes()
        dessiner_obstacles(obstacles)
        mise_a_jour()
    
    ferme_fenetre()