from fltk import *
from random import randint
import time

invincible = False


def joueur(x: int, y: int, taille=5):
    if invincible:
        cercle(x, y, taille, couleur="lime", tag="joueur")
    else:
        cercle(x, y, taille, couleur="red", tag="joueur")


def dessin(ax: int, ay: int, bx: int, by: int):
    ligne(ax, ay, bx, by, couleur="blue", tag="dessin", epaisseur=2)


def calculerAire(polygone: list, superficie_totale: float) -> float:
    """
    Calcul de l'aire du polygone en pourcentage de la superficie totale
    """
    n = len(polygone)
    aire = 0.0

    for i in range(n):
        x1, y1 = polygone[i][2], polygone[i][3]
        x2, y2 = polygone[(i + 1) % n][2], polygone[(i + 1) % n][3]
        aire += x1 * y2 - x2 * y1

    aire_absolue = abs(aire) / 2.0
    aire_en_pourcentage = (aire_absolue / superficie_totale) * 100
    return aire_en_pourcentage


def trouver_coins(start_position: tuple, end_position: tuple):
    if (
        min(start_position[1], end_position[1]) == y1
        and max(start_position[1], end_position[1]) == y2
        or min(start_position[0], end_position[0]) == x1
        and max(start_position[0], end_position[0]) == x2
    ):
        # si le joueur va de haut en bas (ou de bas en haut) alors je prends les coins de droites.
        y_corner1 = min(start_position[1], end_position[1])
        if y_corner1 == y1:
            x_corner1 = x_corner2 = x2
            y_corner2 = y2
        else:  # Sinon je prends les coins du haut
            x_corner1 = x1
            y_corner1 = y_corner2 = y1
            x_corner2 = x2
        return [(None, None, x_corner1, y_corner1), (None, None, x_corner2, y_corner2)]

    # si le joueur va dans un des axes adjacents alors je prends les coins de droites.
    x_corner = x1 if start_position[0] == x1 or end_position[0] == x1 else x2
    y_corner = y1 if start_position[1] == y1 or end_position[1] == y1 else y2
    return [(None, None, x_corner, y_corner)]


def sort_corners(end_position: tuple, corners: list):
    if not corners:
        return []
    for corner in corners:
        if end_position[0] == corner[2] or end_position[1] == corner[3]:
            return [corner] + sort_corners(
                (corner[2], corner[3]), list(set(corners) - {corner})
            )


def inverse_coins(corners: list):
    return list(
        {
            (None, None, x1, y1),
            (None, None, x2, y1),
            (None, None, x2, y2),
            (None, None, x1, y2),
        }
        - set(corners)
    )


somme_aire_polygones = 0.0


def tracerPolygone(
    listePositions: list,
    start_position: tuple,
    end_position: tuple,
    x_fantome: int,
    y_fantome: int,
):
    global somme_aire_polygones

    coins = trouver_coins(start_position, end_position)
    fantome_est_dedans = intersection_test(x_fantome, y_fantome, listePositions + coins)
    if fantome_est_dedans:
        coins = inverse_coins(coins)
    coins = sort_corners(end_position, coins)
    listePositions.extend(coins)
    polygone(listePositions, couleur="blue", remplissage="purple", tag="aire")
    superficie_totale = (x2 - x1) * (
        y2 - y1
    )  # Calcul de la superficie totale du terrain

    if len(listePositions) >= 2:  # Au moins trois points pour former un polygone
        aire_polygone = calculerAire(listePositions, superficie_totale)
        efface("airepoly")
        somme_aire_polygones += (
            aire_polygone  # Addition de l'aire du nouveau polygone à la somme totale
        )
        print("Somme de l'aire des polygones:", somme_aire_polygones)


def intersection_test(x, y, polygone):
    intersections = 0
    for i in range(len(polygone)):
        x1, y1 = polygone[i][2], polygone[i][3]
        x2, y2 = (
            polygone[(i + 1) % len(polygone)][2],
            polygone[(i + 1) % len(polygone)][3],
        )

        if y > min(y1, y2) and y <= max(y1, y2) and x <= max(x1, x2) and y1 != y2:
            intersection_x = (y - y1) * (x2 - x1) / (y2 - y1) + x1
            if x1 == x2 or x <= intersection_x:
                intersections += 1

    return intersections % 2 == 1


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
        "assets/Qix2.gif",
        largeurFantome,
        hauteurFantome,
        ancrage="center",
        tag="fant",
    )
    return x, y


# ****************************************************************************************************************************
"""Création des sparx"""


def sparx1(x, y):
    largeurSparx = 20
    hauteurSparx = 20
    image(x, y, "assets/Sparx.gif", largeurSparx, hauteurSparx, ancrage="center", tag="spar1")
    return x, y


def sparx2(x, y):
    largeurSparx = 20
    hauteurSparx = 20
    image(x, y, "assets/Sparx.gif", largeurSparx, hauteurSparx, ancrage="center", tag="spar2")
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
        and ((xJoueur + tailleJoueur) <= (x_sparx1 + 20))
        and (yJoueur + (tailleJoueur // 2) >= y_sparx1)
        and ((yJoueur + tailleJoueur) <= (y_sparx1 + 20))
    ):
        return True
    if (
        (xJoueur + (tailleJoueur // 2) >= x_sparx2)
        and ((xJoueur + tailleJoueur) <= (x_sparx2 + 20))
        and (yJoueur + (tailleJoueur // 2) >= y_sparx2)
        and ((yJoueur + tailleJoueur) <= (y_sparx2 + 20))
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
    
def checkQixLine(listePositionsLignes: list, drawState: bool, positionFantome: tuple) -> bool:
    """
    Fonction qui permet de vérifier si le qix a touché la ligne du joueur
    """
    if drawState:
        for ligne in listePositionsLignes:
            if ligne == (positionFantome[2], positionFantome[3]):
                return True
    
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
    eve = donne_ev()
    tev = type_ev(eve)

    rectangle(0, 0, largeurFenetre, hauteurFenetre, remplissage="black")
    image(largeurFenetre // 2, 160, "assets/Qix.gif", 450, 200, ancrage="center", tag="im")
    rectangle(375, 300, largeurFenetre - 375, 410, couleur="gold", epaisseur=5)
    texte(
        450,
        306,
        "Mode 1 joueur",
        couleur="gold",
        taille=60,
        police="Arabic Transparent",
    )
    rectangle(375, 440, largeurFenetre - 375, 550, couleur="gold", epaisseur=5)
    texte(
        450,
        447,
        "Mode 2 joueur",
        couleur="gold",
        taille=60,
        police="Arabic Transparent",
    )
    # if tev == "ClicGauche":
    #     if abscisse(ev) < 1125 and abscisse(ev) > 375 and ordonnee(ev) > 300 and ordonnee(ev) < 410  :
    attend_clic_gauche()
    efface_tout()
    # if touche_pressee == "ClicGauche" and ordonnee("ClicGauche") == 115 and abscisse("ClicGauche") == largeurFenetre//2:
    rectangle(0, 0, largeurFenetre, hauteurFenetre, remplissage="black")
    global x1, x2, y1, y2
    x1 = largeurFenetre // 2 - 300
    x2 = largeurFenetre // 2 + 300
    y1 = 200
    y2 = 850
    rectangle(x1, y1, x2, y2, couleur="blue", epaisseur=3)
    ligne(x1 + 10, y1 - 10, x2 - 10, y1 - 10, couleur="red", epaisseur=5)
    # Logo Qix
    image(
        largeurFenetre // 2 - 180, 115, "assets/Qix.gif", 250, 100, ancrage="center", tag="im"
    )

    xJoueur = (x2 + x1) // 2
    yJoueur = y2
    tailleJoueur = 5
    vitesseJoueur = 5
    enTrainDeDessiner = False

    """Position du Qix"""
    x_fantome = (x1 + x2) // 2
    y_fantome = (y1 + y2) // 2
    speedXFantome = 4
    speedYFantome = 2
    positionFantome = (None, None, x_fantome, y_fantome)
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
    joueur_dessine = False

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
            x_sparx1 = largeurFenetre // 2 + 300
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
            x_sparx2 = largeurFenetre // 2 - 300
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
                    xJoueur, yJoueur = deplacer_joueur(0, -vitesseJoueur)
                elif touche(ev) == "Down":
                    xJoueur, yJoueur = deplacer_joueur(0, vitesseJoueur)
                elif touche(ev) == "Left":
                    xJoueur, yJoueur = deplacer_joueur(-vitesseJoueur, 0)
                elif touche(ev) == "Right":
                    xJoueur, yJoueur = deplacer_joueur(vitesseJoueur, 0)

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
                            listePositionsLignes,
                            start_position,
                            end_position,
                            x_fantome,
                            y_fantome,
                        )
                        listePositionsPolygone.extend(listePositionsLignes)
                        for element in listePositionsPolygone:
                            if (None, None, xJoueur, yJoueur) in element:
                                end_position == (None, None, xJoueur, yJoueur)
                        listePositionsLignes = []
                        enTrainDeDessiner = not enTrainDeDessiner
                        joueur_dessine = True

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

                if touche(ev) == "space" and enTrainDeDessiner:
                    vitesseJoueur += 5

        if checkQixLine(listePositionsLignes, enTrainDeDessiner, positionFantome):
            vie -= 1

        """On affiche le nombre de vies"""
        efface("vie")
        vie1 = 3
        if vie1 == vie:
            image(
                largeurFenetre // 2,
                70,
                "assets/coeur.gif",
                50,
                60,
                tag="vie",
            )
        vie2 = 2
        if vie2 <= vie:
            image(
                largeurFenetre // 2 + 40,
                70,
                "assets/coeur.gif",
                50,
                60,
                tag="vie2",
            )
        vie3 = 1
        if vie3 <= vie:
            image(
                largeurFenetre // 2 + 80,
                70,
                "assets/coeur.gif",
                50,
                60,
                tag="vie3",
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
                efface("joueur")
                efface("dessin")
                listePositionsLignes = []

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
                efface("joueur")
                efface("dessin")
                listePositionsLignes = []

        texte(
            largeurFenetre // 2 + 380,
            hauteurFenetre // 2,
            f"{round(somme_aire_polygones, 1)} %",
            couleur="white",
            tag="airepoly",
        )

        if invincible and time.time() - temps_initial_invincible < 3:
            image(
                largeurFenetre // 2 + 50, 120, "assets/invincible.gif", 200, 50, tag="txtinvin"
            )
        else:
            invincible = False
            efface("txtinvin")

        if positionFantome in listePositionsLignes and enTrainDeDessiner:
            vie -= 1
            xJoueur = (x1 + x2) / 2
            yJoueur = y2
            efface("dessin")
            listePositionsLignes = []

        dessiner_pommes()
        dessiner_obstacles(obstacles)
        mise_a_jour()
    time.sleep(0.1)

    if somme_aire_polygones >= 75:
        rectangle(0, 0, largeurFenetre, hauteurFenetre, remplissage="black")
        image(
            largeurFenetre // 2,
            hauteurFenetre // 2,
            "assets/Gameover2.gif",
            largeurFenetre,
            hauteurFenetre,
            tag="vie",
        )
        mise_a_jour()
        time.sleep(4)

    efface_tout()

    while vie == 0:
        rectangle(0, 0, largeurFenetre, hauteurFenetre, remplissage="black")
        image(
            largeurFenetre // 2,
            hauteurFenetre // 2,
            "assets/Gameover2.gif",
            largeurFenetre,
            hauteurFenetre,
            tag="vie",
        )
        mise_a_jour()
        time.sleep(4)
        break

    ferme_fenetre()