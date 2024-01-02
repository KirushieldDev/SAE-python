from fltk import *
from random import randint
import time

invincible = False


def joueur(x: int, y: int, taille=5) -> None:
    """
    Fonction qui permet de dessiner le joueur
    """
    if invincible:
        cercle(x, y, taille, couleur="lime", tag="joueur")
    else:
        cercle(x, y, taille, couleur="red", tag="joueur")


def dessin(ax: int, ay: int, bx: int, by: int) -> None:
    """
    Fonction qui permet de dessiner la ligne qui va suivre
    le joueur
    """
    ligne(ax, ay, bx, by, couleur="blue", tag="dessin",epaisseur=3)


def trouver_coins(start_position: tuple, end_position: tuple) -> list:
    if min(start_position[1], end_position[1]) == y1 and max(start_position[1], end_position[1]) == y2 or min(start_position[0], end_position[0]) == x1 and max(start_position[0], end_position[0]) == x2:
        # si le joueur va de haut en bas (ou de bas en haut) alors je prends les coins de droites.
        y_corner1 = min(start_position[1], end_position[1])
        if y_corner1 == y1:
            x_corner1 = x_corner2 = x2
            y_corner2 = y2
        else:  # Sinon je prends les coins du haut
            x_corner1 = x1
            y_corner1 = y_corner2 = y1
            x_corner2 = x2
        return [(None,None,x_corner1, y_corner1), (None,None,x_corner2, y_corner2)]
    
    # si le joueur va dans un des axes adjacents alors je prends les coins de droites.
    x_corner = x1 if start_position[0] == x1 or end_position[0] == x1 else x2
    y_corner = y1 if start_position[1] == y1 or end_position[1] == y1 else y2
    return [(None,None,x_corner, y_corner)]

def sort_corners(end_position: tuple, corners: list) -> list:
    if not corners:
        return []
    for corner in corners:
        if end_position[0] == corner[2] or end_position[1] == corner[3]:
            return [corner] + sort_corners((corner[2],corner[3]), list(set(corners) - {corner}))

def inverse_coins(corners: list) -> list:
    return list({(None,None,x1, y1), (None,None,x2, y1), (None,None,x2, y2), (None,None,x1, y2)} - set(corners))


def tracerPolygone(listePositions: list, start_position: tuple, end_position: tuple, x_fantome: int, y_fantome: int) -> None:
    coins = trouver_coins(start_position, end_position)
    fantome_est_dedans = intersection_test(x_fantome, y_fantome, listePositions + coins)    
    if fantome_est_dedans:
        coins = inverse_coins(coins)
    coins = sort_corners(end_position, coins)
    listePositions.extend(coins)
    polygone(listePositions, couleur="blue", remplissage="purple", tag="aire")
 
    
    
def intersection_test(x, y, polygone) -> bool:
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

def dessiner_obstacles(obstacles: list) -> None:
    """
    Fonction qui permet de dessiner les obstacles
    """
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


def fantome(x: int, y: int) -> tuple:
    """
    Fonction qui permet de dessiner le qix
    """
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


def sparx1(x: int, y: int) -> None:
    """
    Fonction qui permet de dessiner le premier sparx
    """
    largeurSparx = 20
    hauteurSparx = 20
    image(x, y, "Sparx.gif", largeurSparx, hauteurSparx, ancrage="center", tag="spar1")


def sparx2(x: int, y: int) -> None:
    """
    Fonction qui dessine le deuxième sparx
    """
    largeurSparx = 20
    hauteurSparx = 20
    image(x, y, "Sparx.gif", largeurSparx, hauteurSparx, ancrage="center", tag="spar2")


def checkSparxPlayer(
    xJoueur: float,
    yJoueur: float,
    x_sparx1: float,
    y_sparx1: float,
    x_sparx2: float,
    y_sparx2: float,
    tailleJoueur: int,
) -> bool:
    """
    Fonctio qui vérifie si il y a eu contact entre le joueur et un sparx
    Renvoie True si il y a eu contact et False sinon
    """
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


def checkQixPlayer(
    xJoueur: float, yJoueur: float, xQix: float, yQix: float, tailleJoueur: int
) -> bool:
    """
    Fonction qui vérifie si il y a eu contact entre le joueur et le qix
    Renvoie True si il y a eu contact et False sinon
    """
    if (
        (xJoueur + (tailleJoueur // 2) >= xQix - 80 // 2)
        and ((xJoueur + tailleJoueur) <= (xQix + 80 // 2))
        and (yJoueur + (tailleJoueur // 2) >= yQix - 90 // 2)
        and ((yJoueur + tailleJoueur) <= (yQix + 90 // 2))
    ):
        return True
    else:
        return False


def dessiner_pommes() -> None:
    """
    Fonction qui permet de dessiner les pommes
    """
    for pomme in pommes:
        cercle(pomme[0], pomme[1], 5, couleur="red", remplissage="red", tag="pomme")


def peut_deplacer_nouvelle_position(x: int, y: int) -> bool:
    """
    Fonction qui vérifie si le joueur est bloqué par un obstacle
    Renvoi True si il peut se déplacer et False sinon
    """
    for obstacle in obstacles:
        if obstacle[0] <= x <= obstacle[2] and obstacle[1] <= y <= obstacle[3]:
            return False
    return True


def deplacer_joueur(dx: int, dy: int) -> tuple:
    """
    Fonction qui permet de faire déplacer le joueur
    """
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
    # if touche_pressee == "ClicGauche" and ordonnee("ClicGauche") == 115 and abscisse("ClicGauche") == largeurFenetre//2:
    global x1, x2, y1, y2
    x1 = largeurFenetre//2 - 300
    x2 = largeurFenetre//2 + 300
    y1 = 200
    y2 = 850
    rectangle(x1, y1, x2, y2, couleur="blue",epaisseur=3)
    ligne(x1 + 10, y1 - 10, x2 - 10, y1 - 10, couleur="red", epaisseur=5)
    # Logo Qix
    image(largeurFenetre//2 - 200, 115, "Qix.gif", ancrage="center", tag="im")

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
    positionFantome = (None,None,x_fantome, y_fantome)
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
            x_sparx1 = largeurFenetre//2 + 300
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
            x_sparx2 = largeurFenetre//2 - 300
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

                if touche(ev) == "space" and not enTrainDeDessiner:
                    vitesseJoueur += 5

        """On affiche le nombre de vies"""
        efface("vie")
        vie1 = 3
        if vie1 == vie:
            image(
                largeurFenetre//2 ,
                70,
                "coeur.gif",
                35,
                40,
                tag="vie",
            )
        vie2 = 2
        if vie2 <= vie:
            image(
                largeurFenetre//2 + 40,
                70,
                "coeur.gif",
                35,
                40,
                tag="vie2",
            )
        vie3 = 1
        if vie3 <= vie:
            image(
                largeurFenetre//2 + 80,
                70,
                "coeur.gif",
                35,
                40,
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
                efface("dessin")
                listePositionsLignes = []
                
                

        if invincible and time.time() - temps_initial_invincible < 3:
            image(largeurFenetre//2 + 50, 120, "invincible.gif",200 , 50 ,tag="txtinvin")
        else:
            invincible = False
            efface("txtinvin")
        
        if positionFantome in listePositionsLignes and enTrainDeDessiner :
            vie -= 1
            xJoueur = (x1 + x2) / 2
            yJoueur = y2
            efface("dessin")
            listePositionsLignes = []
        
    
        dessiner_pommes()
        dessiner_obstacles(obstacles)
        mise_a_jour()
    time.sleep(0.1)
    ferme_fenetre()