from fltk import *
from random import randint
import time

invincible = False
invincible2 = False

"""Création des joueurs"""
def joueur(x: int, y: int, taille=5):
    if invincible:
        cercle(x, y, taille, couleur="lime", tag="joueur")
    else:
        cercle(x, y, taille, couleur="red", tag="joueur")

def joueur2(x: int, y: int, taille=5):
    if invincible2:
        cercle(x, y, taille, couleur="purple", tag="joueur2")
    else:
        cercle(x, y, taille, couleur="yellow", tag="joueur2")

"""Création des lignes des joueurs"""
def dessin(ax: int, ay: int, bx: int, by: int):
    ligne(ax, ay, bx, by, couleur="blue", tag="dessin",epaisseur=3)

def dessin2(ax: int, ay: int, bx: int, by: int):
    ligne(ax, ay, bx, by, couleur="red", tag="dessin2",epaisseur=3)

# ****************************************************************************************************************************

"""Calcul de l'aire pris"""
def calculerAire(polygone: list, superficie_totale: float) -> float:
    # Calcul de l'aire du polygone en pourcentage de la superficie totale
    n = len(polygone)
    aire = 0.0

    for i in range(n):
        x1, y1 = polygone[i][2], polygone[i][3]
        x2, y2 = polygone[(i + 1) % n][2], polygone[(i + 1) % n][3]
        aire += (x1 * y2 - x2 * y1)
    

    aire_absolue = abs(aire) / 2.0
    aire_en_pourcentage = (aire_absolue / superficie_totale) * 100
    return aire_en_pourcentage

"""Rajouter les coins pour les polygones"""
def trouver_coins(start_position: tuple, end_position: tuple):
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

def sort_corners(end_position: tuple, corners: list):
    if not corners:
        return []
    for corner in corners:
        if end_position[0] == corner[2] or end_position[1] == corner[3]:
            return [corner] + sort_corners((corner[2],corner[3]), list(set(corners) - {corner}))

def inverse_coins(corners: list):
    return list({(None,None,x1, y1), (None,None,x2, y1), (None,None,x2, y2), (None,None,x1, y2)} - set(corners))

somme_aire_polygones = 0.0
score = 0.0
def tracerPolygone(listePositions: list, start_position: tuple, end_position: tuple, x_fantome: int, y_fantome: int, couleur: str):
    global somme_aire_polygones
    global score
    coins = trouver_coins(start_position, end_position)
    fantome_est_dedans = intersection_test(x_fantome, y_fantome, listePositions + coins)    
    if fantome_est_dedans:
        coins = inverse_coins(coins)
    coins = sort_corners(end_position, coins)
    listePositions.extend(coins)
    if deuxjoueur is True:
        couleur2 = "blue"
    else:
        couleur2 = "purple"
    polygone(listePositions, couleur=f"{couleur}", remplissage=f"{couleur2}", tag="aire")
    superficie_totale = (x2 - x1) * (y2 - y1)  # Calcul de la superficie totale du terrain

    if len(listePositions) >= 2:  # Au moins trois points pour former un polygone        
        aire_polygone = calculerAire(listePositions, superficie_totale)
        efface("airepoly")
        score += aire_polygone * 25
        somme_aire_polygones += aire_polygone  # Addition de l'aire du nouveau polygone à la somme totale
        print("Somme de l'aire des polygones:", somme_aire_polygones)

somme_aire_polygones2 = 0.0
score2 = 0.0
def tracerPolygone2(listePositions: list, start_position: tuple, end_position: tuple, x_fantome: int, y_fantome: int, couleur: str):
    global somme_aire_polygones2
    global score2
    coins = trouver_coins(start_position, end_position)
    fantome_est_dedans = intersection_test(x_fantome, y_fantome, listePositions + coins)    
    if fantome_est_dedans:
        coins = inverse_coins(coins)
    coins = sort_corners(end_position, coins)
    listePositions.extend(coins)
    polygone(listePositions, couleur=f"{couleur}", remplissage=f"{couleur}", tag="aire")
    superficie_totale = (x2 - x1) * (y2 - y1)  # Calcul de la superficie totale du terrain

    if len(listePositions) >= 2:  # Au moins trois points pour former un polygone        
        aire_polygone = calculerAire(listePositions, superficie_totale)
        efface("airepoly")
        score2 += aire_polygone * 25
        somme_aire_polygones2 += aire_polygone  # Addition de l'aire du nouveau polygone à la somme totale
        print("Somme de l'aire des polygones:", somme_aire_polygones2)

"""Repérer si le Qix est dans le polygone"""
def intersection_test(x, y, polygone):
    intersections = 0
    for i in range(len(polygone)):
        x1, y1 = polygone[i][2],polygone[i][3]
        x2, y2 = polygone[(i + 1) % len(polygone)][2],polygone[(i + 1) % len(polygone)][3]
        
        if y > min(y1, y2) and y <= max(y1, y2) and x <= max(x1, x2) and y1 != y2:
            intersection_x = (y - y1) * (x2 - x1) / (y2 - y1) + x1
            if x1 == x2 or x <= intersection_x:
                intersections += 1

    return intersections % 2 == 1

# ****************************************************************************************************************************

"""Initialisation des obsatacles"""
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

# ****************************************************************************************************************************

"""Création des Qix"""
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

def fantome2(x, y):
    largeurFantome = 70
    hauteurFantome = 80
    image(
        x,
        y,
        "Fantome.gif",
        largeurFantome,
        hauteurFantome,
        ancrage="center",
        tag="fant2",
    )
    return x, y

"""Création des sparx"""
def sparx1(x, y):
    largeurSparx = 20
    hauteurSparx = 20
    image(x, y, "Sparx.gif", largeurSparx, hauteurSparx, ancrage="center", tag="spar1")
    return x, y

def sparx2(x, y):
    largeurSparx = 20
    hauteurSparx = 20
    image(x, y, "Sparx.gif", largeurSparx, hauteurSparx, ancrage="center", tag="spar2")
    return x, y

# ****************************************************************************************************************************

"""Vérification de collision entre les sparx et les joueur"""
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

"""Vérification de collision entre le Qix et les joueur"""
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

def qix_touche_ligne(x_fantome, y_fantome, liste_positions_lignes):
    for i in range(len(liste_positions_lignes) - 1):
        x1, y1, x2, y2 = liste_positions_lignes[i][0], liste_positions_lignes[i][1], liste_positions_lignes[i+1][0], liste_positions_lignes[i+1][1]
        if (x1 <= x_fantome + 35 <= x2 or x2 <= x_fantome - 35 <= x1) and (y1 <= y_fantome + 40 <= y2 or y2 <= y_fantome - 40 <= y1):
            return True
    return False

# ****************************************************************************************************************************

"""Initialisations des pommes"""
def dessiner_pommes():
    for pomme in pommes:
        cercle(pomme[0], pomme[1], 5, couleur="red", remplissage="red", tag="pomme")

# ****************************************************************************************************************************

"""Déplacement des joueurs"""
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

def deplacer_joueur2(dx, dy):
    new_x2, new_y2 = xJoueur2 + dx, yJoueur2 + dy
    if (
        x1 <= new_x2 <= x2
        and y1 <= new_y2 <= y2
        and peut_deplacer_nouvelle_position(new_x2, new_y2)
    ):
        return new_x2, new_y2
    return xJoueur2, yJoueur2

# ****************************************************************************************************************************

if __name__ == "__main__":
    
    """Création de la fenêtre de jeu"""
    largeurFenetre = 1500
    hauteurFenetre = 900
    cree_fenetre(largeurFenetre, hauteurFenetre)
    unjoueur = False
    deuxjoueur = False
    
    """Création du menu de mode de jeu"""
    rectangle(0, 0, largeurFenetre, hauteurFenetre, remplissage="black")
    image(largeurFenetre//2, 160, "Qix.gif",450,200, ancrage="center", tag="im")
    rectangle(375, 300, largeurFenetre-375, 410,couleur="gold",epaisseur=5)
    texte(450, 306, "Mode 1 joueur", couleur="gold", taille=60, police='Arabic Transparent')
    rectangle(375, 440, largeurFenetre-375, 550,couleur="gold",epaisseur=5)
    texte(450, 447, "Mode 2 joueur", couleur="gold", taille=60, police='Arabic Transparent')
    test = True
    test2 = True

    """Vérifie quel mode de jeu est choisie"""
    while test:
        sourisx, sourisy = attend_clic_gauche()
        if sourisx <= 1125 and sourisx >= 375 and sourisy >= 300 and sourisy <= 410:
            unjoueur = True
            deuxjoueur = False
            test = False

        elif sourisx <= 1125 and sourisx >= 375 and sourisy >= 440 and sourisy <= 550:
            deuxjoueur = True
            unjoueur = False
            test = False

    """Création du menu de choix de difficulté"""
    rectangle(0, 0, largeurFenetre, hauteurFenetre, remplissage="black")
    image(largeurFenetre//2, 160, "Qix.gif",450,200, ancrage="center", tag="im")
    rectangle(375, 300, largeurFenetre-375, 410,couleur="gold",epaisseur=5)
    texte(450, 306, "Facile", couleur="gold", taille=60, police='Arabic Transparent')
    rectangle(375, 440, largeurFenetre-375, 550,couleur="gold",epaisseur=5)
    texte(450, 447, "Normale", couleur="gold", taille=60, police='Arabic Transparent')
    rectangle(375, 580, largeurFenetre-375, 690,couleur="gold",epaisseur=5)
    texte(450, 588, "Difficile", couleur="gold", taille=60, police='Arabic Transparent')

    facile = False
    normale = False
    difficile = False

    """Vérifie quel difficulté est choisie"""
    while test2:  
        sourisx, sourisy = attend_clic_gauche() 
        if sourisx <= 1125 and sourisx >= 375 and sourisy >= 300 and sourisy <= 410:
            facile = True
            test2 = False

        elif sourisx <= 1125 and sourisx >= 375 and sourisy >= 440 and sourisy <= 550:
            normale = True
            test2 = False

        elif sourisx <= 1125 and sourisx >= 375 and sourisy >= 580 and sourisy <= 690:
            difficile = True
            test2 = False
            
    """Création de l'aire de jeu"""
    rectangle(0, 0, largeurFenetre, hauteurFenetre, remplissage="black")
    global x1, x2, y1, y2
    x1 = largeurFenetre//2 - 300
    x2 = largeurFenetre//2 + 300
    y1 = 200
    y2 = 850
    rectangle(x1, y1, x2, y2, couleur="blue",epaisseur=4)
    ligne(x1 + 10, y1 - 10, x2 - 10, y1 - 10, couleur="red", epaisseur=5)
    image(largeurFenetre//2 - 180, 115, "Qix.gif",250,100, ancrage="center", tag="im")

    # ****************************************************************************************************************************

    """Initialisation des paramètres de jeu"""

    xJoueur = (x2 + x1) // 2
    yJoueur = y2
    if deuxjoueur is True:
        xJoueur = x2
        yJoueur = y2
    if deuxjoueur is True:
        xJoueur2 = x1
        yJoueur2 = y2
    tailleJoueur = 5
    tailleJoueur2 = 5
    vitesseJoueur = 5
    vitesseJoueur2 = 5
    enTrainDeDessiner = False
    enTrainDeDessiner2 = False
    couleur = "blue"
    couleur2 = "red"

    x_fantome = (x1 + x2) // 2
    y_fantome = (y1 + y2) // 2
    x_fantome2 = (x1 + x2) // 2
    y_fantome2 = (y1 + y2) // 2
    if facile is True:
        speedXFantome = 5
        speedYFantome = 3
        speedXFantome2 = 5
        speedYFantome2 = 3
    if normale is True:
        speedXFantome = 6
        speedYFantome = 4
        speedXFantome2 = 6
        speedYFantome2 = 4
    if difficile is True:
        speedXFantome = 8
        speedYFantome = 5
        speedXFantome2 = 8
        speedYFantome2 = 5
    positionFantome = (None,None,x_fantome, y_fantome)

    x_sparx1 = 750
    y_sparx1 = y1
    x_sparx2 = 750
    y_sparx2 = y1
    if facile is True:
        speedSparx = 3
    if normale is True:
        speedSparx = 6
    if difficile is True:
        speedSparx = 9

    cercle(xJoueur, yJoueur, tailleJoueur, couleur="lime", tag="joueur")

    lstBords = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
    listePositionsLignes = []
    listePositionsLignes2 = []
    listePositionsPolygone2 = []
    listePositionsPolygone = []

    """Création des pommes et des obstacles"""
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
    viej2 = 3
    temps_initial = 0
    joueur_dessine = False

# ****************************************************************************************************************************
    
    """Boucle principale du jeu"""
    boucle = True
    while boucle:        
        efface("txtAire")
        efface("fant")
        efface("fant2")

        fantome(x_fantome, y_fantome)
        if difficile is True:
            fantome2(x_fantome2, y_fantome2)
        joueur(xJoueur, yJoueur, tailleJoueur)
        positionJoueur = (xJoueur, yJoueur)
        if deuxjoueur is True :
            joueur2(xJoueur2, yJoueur2, tailleJoueur)
            positionJoueur2 = (xJoueur2, yJoueur2)
        
        """Déplacement du Qix"""
        x_fantome += speedXFantome
        y_fantome -= speedYFantome
        x_fantome2 -= speedXFantome2
        y_fantome2 += speedYFantome2

        """Collisions du Qix"""   
        if x_fantome >= x2 - 35 or x_fantome <= x1 + 35:
            speedXFantome = -speedXFantome

        if y_fantome >= y2 - 40 or y_fantome <= y1 + 40:
            speedYFantome = -speedYFantome

        if deuxjoueur is True:
            if x_fantome2 >= x2 - 35 or x_fantome2 <= x1 + 35:
                speedXFantome2 = -speedXFantome2

            if y_fantome2 >= y2 - 40 or y_fantome2 <= y1 + 40:
                speedYFantome2 = -speedYFantome2

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
            y_sparx1 = 850
            x_sparx1 -= speedSparx

        if x_sparx1 <= x1:
            x_sparx1 = largeurFenetre//2 - 300
            y_sparx1 -= speedSparx

        for position in listePositionsLignes:
            if (position[2], position[3]) == (x_sparx1 + 10, y_sparx1):
                x_sparx1 += speedSparx
            if (position[2], position[3]) == (x_sparx1 - 10, y_sparx1):
                x_sparx1 -= speedSparx
            if (position[2], position[3]) == (x_sparx1, y_sparx1 + 10):
                y_sparx1 += speedSparx
            if (position[2], position[3]) == (x_sparx1, y_sparx1 - 10):
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

        for position in listePositionsLignes:
            if (position[2], position[3]) == (x_sparx2 + 10, y_sparx2):
                x_sparx2 += speedSparx
            if (position[2], position[3]) == (x_sparx2 - 10, y_sparx2):
                x_sparx2 -= speedSparx
            if (position[2], position[3]) == (x_sparx2, y_sparx2 + 10):
                y_sparx2 += speedSparx
            if (position[2], position[3]) == (x_sparx2, y_sparx2 - 10):
                y_sparx2 -= speedSparx

        # ****************************************************************************************************************************

        """Déplacement des joueurs"""
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
        
            
            if ev is not None:
                if type_ev(ev) == "Quitte":
                    break
                if type_ev(ev) == "Touche":
                    if deuxjoueur is True:
                        oldX2, oldY2 = xJoueur2, yJoueur2

                        if touche(ev) == "z":
                            xJoueur2, yJoueur2 = deplacer_joueur2(
                                0, -vitesseJoueur2
                            )
                        elif touche(ev) == "s":
                            xJoueur2, yJoueur2 = deplacer_joueur2(
                                0, vitesseJoueur2
                            )
                        elif touche(ev) == "q":
                            xJoueur2, yJoueur2 = deplacer_joueur2(
                                -vitesseJoueur2, 0
                            )
                        elif touche(ev) == "d":
                            xJoueur2, yJoueur2 = deplacer_joueur2(
                                vitesseJoueur2, 0
                            )
                print(listePositionsLignes)

                """Création des polygones"""
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
                            listePositionsLignes, start_position, end_position,x_fantome,y_fantome,couleur
                        )
                        
                        
                        listePositionsPolygone.extend(listePositionsLignes)
                        for element in listePositionsPolygone:
                            if (None, None, xJoueur, yJoueur) in element:
                                end_position == (None, None, xJoueur, yJoueur)
                        listePositionsLignes = []
                        enTrainDeDessiner = not enTrainDeDessiner
                        joueur_dessine = True

                if deuxjoueur is True:
                    if enTrainDeDessiner2 and peut_deplacer_nouvelle_position(
                        xJoueur2, yJoueur2
                    ):
                        dessin2(oldX2, oldY2, xJoueur2, yJoueur2)
                        listePositionsLignes2.append((oldX2, oldY2, xJoueur2, yJoueur2))
                        if xJoueur2 <= x1 or xJoueur2 >= x2 or yJoueur2 <= y1 or yJoueur2 >= y2:
                            end_position2 = (xJoueur2, yJoueur2)
                            dernierPoint2 = listePositionsLignes2[-1][2:]
                            listePositionsLignes2.append((xJoueur2, yJoueur2, *dernierPoint2))
                            tracerPolygone2(
                                listePositionsLignes2, start_position2, end_position2,x_fantome,y_fantome,couleur2
                            )
                
                            
                            listePositionsPolygone2.extend(listePositionsLignes2)
                            for element in listePositionsPolygone2:
                                if (None, None, xJoueur2, yJoueur2) in element:
                                    end_position2 == (None, None, xJoueur2, yJoueur2)
                            listePositionsLignes2 = []
                            enTrainDeDessiner2 = not enTrainDeDessiner2
                            joueur_dessine2 = True


                efface("joueur")
                joueur(xJoueur, yJoueur)
                if deuxjoueur is True:
                    efface("joueur2")
                    joueur2(xJoueur2, yJoueur2)

                if touche(ev) == "Return":
                    start_position = (xJoueur, yJoueur)
                    enTrainDeDessiner = not enTrainDeDessiner
                
                if deuxjoueur is True :
                    if touche(ev) == "e":
                        start_position2 = (xJoueur2, yJoueur2)
                        enTrainDeDessiner2 = not enTrainDeDessiner2

                # ****************************************************************************************************************************

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

                if deuxjoueur is True :
                    for pomme in pommes:
                        distance2 = (
                            (pomme[0] - xJoueur2) ** 2 + (pomme[1] - yJoueur2) ** 2
                        ) ** 0.5
                        if distance2 < tailleJoueur2 + 5:
                            pommes.remove(pomme)
                            efface("pomme")
                            dessiner_pommes()
                            if invincible2 == False:
                                invincible2 = True
                                temps_initial_invincible2 = time.time()

                if touche(ev) == "v" and not enTrainDeDessiner2:
                    vitesseJoueur2 += 5
        
        # ****************************************************************************************************************************************

        """On affiche le nombre de vies"""
        efface("vie")
        efface("viej21")
        decale = 0
        decale2 = 40
        decale3 = 80
        if deuxjoueur is True:
            decale = 150
            decale2 = 190
            decale3 = 230
        vie1 = 3
        if vie1 == vie:
            image(
                largeurFenetre//2 + decale ,
                70,
                "coeur.gif",
                50,
                60,
                tag="vie",
            )
        vie2 = 2
        if vie2 <= vie:
            image(
                largeurFenetre//2 + decale2,
                70,
                "coeur.gif",
                50,
                60,
                tag="vie2",
            )
        else:
            efface("vie2")
        vie3 = 1
        if vie3 <= vie:
            image(
                largeurFenetre//2 + decale3,
                70,
                "coeur.gif",
                50,
                60,
                tag="vie3",
            )
        else:
            efface("vie3")
        if deuxjoueur is True:
            viej21 = 3
            if viej21 == viej2:
                image(
                    largeurFenetre//2 + 150 ,
                    120,
                    "coeur.gif",
                    50,
                    60,
                    tag="viej21",
                )
            viej22 = 2
            if viej22 <= viej2:
                image(
                    largeurFenetre//2 + 190,
                    120,
                    "coeur.gif",
                    50,
                    60,
                    tag="viej22",
                )
            else:
                efface("viej22")
            viej23 = 1
            if viej23 <= viej2:
                image(
                    largeurFenetre//2 + 230,
                    120,
                    "coeur.gif",
                    50,
                    60,
                    tag="viej23",
                )
            else:
                efface("viej23")

        # ******************************************************************************************************************************************************

        """Collision des joueurs contre les Qix et les sparx"""
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
                if deuxjoueur is True :
                    xJoueur = x2
                    yJoueur = y2
                listePositionsPolygone.clear()
                x_sparx1 = 755
                y_sparx1 = 200
                x_sparx2 = 745
                y_sparx2 = 200
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
                if deuxjoueur is True :
                    xJoueur = x2
                    yJoueur = y2
                listePositionsPolygone.clear()
                x_fantome = largeurFenetre // 2 
                y_fantome = hauteurFenetre // 2
                x_sparx1 = 755
                y_sparx1 = 200
                x_sparx2 = 745
                y_sparx2 = 200
                efface("joueur")
                efface("dessin")
                listePositionsLignes = []

            if (
                checkQixPlayer(xJoueur, yJoueur, x_fantome2, y_fantome2, tailleJoueur)
                == True
            ):
                vie -= 1
                xJoueur = (x1 + x2) / 2
                yJoueur = y2
                if deuxjoueur is True :
                    xJoueur = x2
                    yJoueur = y2
                listePositionsPolygone.clear()
                x_fantome2 = largeurFenetre // 2 
                y_fantome2 = hauteurFenetre // 2
                x_sparx1 = 755
                y_sparx1 = 200
                x_sparx2 = 745
                y_sparx2 = 200
                efface("joueur")
                efface("dessin")
                listePositionsLignes = []

            if qix_touche_ligne(x_fantome,y_fantome,listePositionsLignes) is True:
                    print("touché")
                    vie -= 1
                    xJoueur = (x1 + x2) / 2
                    yJoueur = y2
                    if deuxjoueur is True :
                        xJoueur = x2
                        yJoueur = y2
                    listePositionsPolygone.clear()
                    efface("joueur")
                    efface("dessin")
                    listePositionsLignes = []

            if qix_touche_ligne(x_fantome2,y_fantome2,listePositionsLignes) is True:
                    print("touché")
                    vie -= 1
                    xJoueur = (x1 + x2) / 2
                    yJoueur = y2
                    if deuxjoueur is True :
                        xJoueur = x2
                        yJoueur = y2
                    listePositionsPolygone.clear()
                    efface("joueur")
                    efface("dessin")
                    listePositionsLignes = []

        
        if deuxjoueur is True:
            if invincible2 == False:
                if (
                    checkSparxPlayer(
                        xJoueur2,
                        yJoueur2,
                        x_sparx1,
                        y_sparx1,
                        x_sparx2,
                        y_sparx2,
                        tailleJoueur2,
                    )
                    == True
                ):
                    viej2 -= 1
                    xJoueur2 = x1
                    yJoueur2 = y2
                    listePositionsPolygone2.clear()
                    x_sparx1 = 755
                    y_sparx1 = 200
                    x_sparx2 = 745
                    y_sparx2 = 200
                    efface("joueur2")
                    efface("dessin2")
                    listePositionsLignes2 = []
                    

                if (
                    checkQixPlayer(xJoueur2, yJoueur2, x_fantome, y_fantome, tailleJoueur2)
                    == True
                ):
                    viej2 -= 1
                    xJoueur2 = x1 
                    yJoueur2 = y2
                    listePositionsPolygone2.clear()
                    x_sparx1 = 755
                    y_sparx1 = 200
                    x_sparx2 = 745
                    y_sparx2 = 200
                    efface("joueur2")
                    efface("dessin2")
                    listePositionsLignes2 = []

                if (
                checkQixPlayer(xJoueur2, yJoueur2, x_fantome2, y_fantome2, tailleJoueur2)
                == True
                ):
                    viej2 -= 1
                    xJoueur2 = x1
                    yJoueur2 = y2
                    listePositionsPolygone.clear()
                    x_sparx1 = 755
                    y_sparx1 = 200
                    x_sparx2 = 745
                    y_sparx2 = 200
                    efface("joueur")
                    efface("dessin")
                    listePositionsLignes = []


                if qix_touche_ligne(x_fantome,y_fantome,listePositionsLignes2) is True:
                    print("touché")
                    viej2 -= 1
                    xJoueur2 = x1
                    yJoueur2 = y2
                    listePositionsPolygone2.clear()
                    efface("joueur2")
                    efface("dessin2")
                    listePositionsLignes2 = []
                
                if qix_touche_ligne(x_fantome2,y_fantome2,listePositionsLignes2) is True:
                    print("touché")
                    viej2 -= 1
                    xJoueur2 = x1
                    yJoueur2 = y2
                    listePositionsPolygone2.clear()
                    efface("joueur2")
                    efface("dessin2")
                    listePositionsLignes2 = []

        # *******************************************************************************************************************************************************************
        
        """Affichage du pourcentage d'aire pris"""
        if deuxjoueur is False:
            texte(largeurFenetre//2 + 380, hauteurFenetre//2, f"{round(somme_aire_polygones, 1)}%",couleur="white",tag="airepoly")
            texte(largeurFenetre//2 + 380, hauteurFenetre//2 + 40, f"Score : {round(score)}",couleur="white",tag="airepoly")
        if deuxjoueur is True:
            texte(largeurFenetre//2 + 380, hauteurFenetre//2, f"{round(somme_aire_polygones, 1)}%",couleur="blue",tag="airepoly")
            texte(largeurFenetre//2 + 380, hauteurFenetre//2 + 40, f"Score Joueur 1 : {round(score)}",couleur="blue",tag="airepoly")
            texte(largeurFenetre//2 + 380, hauteurFenetre//2 + 80, f"{round(somme_aire_polygones2, 1)}%",couleur="red",tag="airepoly")
            texte(largeurFenetre//2 + 380, hauteurFenetre//2 + 120, f"Score Joueur 2 : {round(score2)}",couleur="red",tag="airepoly")

        if deuxjoueur is True :
            texte(largeurFenetre//2 - 50, 50,"Joueur 1 :",couleur="white",taille = 28, tag="player1")
            texte(largeurFenetre//2 - 50, 100,"Joueur 2 :",couleur="white",taille = 28, tag="player2")

        # **************************************************************************************************************************************************************************

        """Invincibilité du joueur s'il touche une pomme"""
        if invincible and time.time() - temps_initial_invincible < 3:
            if deuxjoueur is True:
                image(largeurFenetre//2 + 380, 70, "invincible.gif",200 , 45 ,tag="txtinvin")
            else:
                image(largeurFenetre//2 + 50, 120, "invincible.gif",200 , 50 ,tag="txtinvin")
        else:
            invincible = False
            efface("txtinvin")

        if deuxjoueur is True :
            if invincible2 and time.time() - temps_initial_invincible2 < 3:
                image(largeurFenetre//2 + 380, 120, "invincible.gif",200 , 45 ,tag="txtinvin2")
            else:
                invincible2 = False
                efface("txtinvin2")
    
        dessiner_pommes()
        dessiner_obstacles(obstacles)
        if unjoueur is True:
            if vie == 0 or somme_aire_polygones >= 75:
                boucle = False
        if deuxjoueur is True:
            if vie == 0 and viej2 == 0 or somme_aire_polygones >= 75 or somme_aire_polygones2 >= 75:
                boucle = False
        mise_a_jour()
    time.sleep(0.1)
    
    efface_tout()

    # **********************************************************************************************************************************************************************************

    """Affichage de la victoire"""
    while somme_aire_polygones >= 75 :
        rectangle(0, 0, largeurFenetre, hauteurFenetre, remplissage="black")
        image(
                largeurFenetre//2 ,
                hauteurFenetre//2,
                "youwin.gif",
                largeurFenetre,
                hauteurFenetre,
                tag="win",
            )
        mise_a_jour( )
        time.sleep(4)
        break

    if deuxjoueur is True:
        while somme_aire_polygones >= 75 or somme_aire_polygones2 >= 75:
            rectangle(0, 0, largeurFenetre, hauteurFenetre, remplissage="black")
            image(
                    largeurFenetre//2 ,
                    hauteurFenetre//2,
                    "youwin.gif",
                    largeurFenetre,
                    hauteurFenetre,
                    tag="win",
                )
            mise_a_jour( )
            time.sleep(4)
            break

    """Affichage du game over"""
    if unjoueur is True:
        while vie == 0:
            rectangle(0, 0, largeurFenetre, hauteurFenetre, remplissage="black")
            image(
                    largeurFenetre//2 ,
                    hauteurFenetre//2,
                    "Gameover2.gif",
                    largeurFenetre,
                    hauteurFenetre,
                    tag="vie",
                )
            mise_a_jour( )
            time.sleep(4)
            break
    
    if deuxjoueur is True:
        while vie == 0 and viej2 == 0:
            print("yes")
            rectangle(0, 0, largeurFenetre, hauteurFenetre, remplissage="black")
            image(
                    largeurFenetre//2 ,
                    hauteurFenetre//2,
                    "Gameover2.gif",
                    largeurFenetre,
                    hauteurFenetre,
                    tag="vie",
                )
            mise_a_jour()
            time.sleep(4)
            break
    
    
        
    ferme_fenetre()
