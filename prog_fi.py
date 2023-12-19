from fltk import *


def joueur(x: int, y: int, taille=5):
    cercle(x, y, taille, couleur="lime", tag="joueur")

#Fonctions pour les dessins
def dessin(ax: int, ay: int, bx: int, by: int):
    ligne(ax, ay, bx, by, couleur="white", tag="dessin")

#Fonctions pour remplir les dessins
def tracerPolygone(listePositions: list):
    if len(listePositions) >= 3:
        polygone(listePositions, couleur="white", remplissage="green", tag="aire")
            
#Fonction Pour les QIx
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

largeurFenetre = 1500
hauteurFenetre = 900

if __name__ == "__main__":
     
    #Creation de la fenêtre
    cree_fenetre(largeurFenetre, hauteurFenetre)
    rectangle(0, 0, largeurFenetre, hauteurFenetre, remplissage="black")
    x1 = 300
    x2 = 1200
    y1 = 200
    y2 = 800
    rectangle(x1, y1, x2, y2, couleur="white")

    """Position du Qix"""
    x_fantome = 750
    y_fantome = 550
    speedXFantome = 3
    speedYFantome = 1
    positionFantome=(x_fantome,y_fantome)

    xJoueur = (x2 + x1) // 2
    yJoueur = y2
    tailleJoueur = 5
    enTrainDeDessiner = False  # Nouvelle variable

    #Creation du joueur
    cercle(xJoueur, yJoueur, tailleJoueur, couleur="lime", tag="joueur")

    lstBords = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
    listePositionsLignes = []
    listePositionsPolygone = []

    while True:
        ev = donne_ev()
        if ev is not None:
            if type_ev(ev) == "Quitte":
                break
            if type_ev(ev) == "Touche":
                efface("fant")
                #Deplacement du Qix
                fantome(x_fantome, y_fantome)
                x_fantome += speedXFantome
                y_fantome -= speedYFantome

                if x_fantome >= x2 - 35 or x_fantome <= x1 + 35:
                    speedXFantome = -speedXFantome

                if y_fantome >= y2 - 40 or y_fantome <= y1 + 40:
                    speedYFantome = -speedYFantome
                oldX, oldY = xJoueur, yJoueur

                #Deplacement du joueur vers le haut
                if touche(ev) == "Up" and yJoueur > y1:
                    yJoueur -= tailleJoueur
                    if enTrainDeDessiner:
                        dessin(oldX, oldY, oldX, yJoueur)
                        listePositionsLignes.append((oldX, oldY, oldX, yJoueur))
                        if (xJoueur <= x1 or xJoueur >= x2 or yJoueur <= y1 or yJoueur >= y2):
                            dernierPoint = listePositionsLignes[-1][2:]
                            listePositionsLignes.append((xJoueur, yJoueur, *dernierPoint))
                            #Remplissage du coin en haut à gauche
                            if (listePositionsLignes[0][0] == x1 and listePositionsLignes[0][1] > y1 
                                or listePositionsLignes[0][1] < y2 and listePositionsLignes[-1][1] == y1 and listePositionsLignes[-1][0] > x1 
                                or listePositionsLignes[-1][0] < x2)  :
                                    listePositionsLignes.append((x1, y1))
                            #Remplissage du coin en haut à droite
                            if (listePositionsLignes[0][0] == x2 and listePositionsLignes[0][1] > y1 
                                or listePositionsLignes[0][1] < y2 and listePositionsLignes[-1][1] == y1 and listePositionsLignes[-1][0] > x1 
                                or listePositionsLignes[-1][0] < x2)  :
                                    listePositionsLignes.append((x2,y1))
                
                            tracerPolygone(listePositionsLignes)
                            listePositionsPolygone.extend(listePositionsLignes)
                
                            enTrainDeDessiner = not enTrainDeDessiner

                #Deplacement du joueur vers le bas
                if touche(ev) == "Down" and yJoueur < y2:
                    yJoueur += tailleJoueur
                    if enTrainDeDessiner:
                        dessin(oldX, oldY, oldX, yJoueur)
                        listePositionsLignes.append((oldX, oldY, oldX, yJoueur))
                        if (xJoueur <= x1 or xJoueur >= x2 or yJoueur <= y1 or yJoueur >= y2):
                            dernierPoint = listePositionsLignes[-1][2:]
                            listePositionsLignes.append((xJoueur, yJoueur, *dernierPoint))
                            #Remplissage du coin en bas à gauche
                            if (listePositionsLignes[0][0] == x1 and listePositionsLignes[0][1] > y1 
                                or listePositionsLignes[0][1] < y2 and listePositionsLignes[-1][1] == y2 and listePositionsLignes[-1][0] > x1 
                                or listePositionsLignes[-1][0] < x2)  :
                                    listePositionsLignes.append((x1,y2))
                            #Remplissage du coin en bas à droite
                            if (listePositionsLignes[0][0] == x2 and listePositionsLignes[0][1] > y1 
                                or listePositionsLignes[0][1] < y2 and listePositionsLignes[-1][1] == y2 and listePositionsLignes[-1][0] > x1 
                                or listePositionsLignes[-1][0] < x2)  :
                                    listePositionsLignes.append((x2,y2))
        
                            tracerPolygone(listePositionsLignes)
                            listePositionsPolygone.extend(listePositionsLignes)
                    
                            enTrainDeDessiner = not enTrainDeDessiner

                #Deplacement du joueur vers la gauche
                if touche(ev) == "Left" and xJoueur > x1:
                    xJoueur -= tailleJoueur
                    if enTrainDeDessiner:
                        dessin(oldX, oldY, xJoueur, oldY)
                        listePositionsLignes.append((oldX, oldY, xJoueur, oldY))
                        if (xJoueur <= x1 or xJoueur >= x2 or yJoueur <= y1 or yJoueur >= y2):
                            dernierPoint = listePositionsLignes[-1][2:]
                            listePositionsLignes.append((xJoueur, yJoueur, *dernierPoint))
                            #Remplissage du coin en haut à gauche
                            if (listePositionsLignes[0][1] == y1 and listePositionsLignes[0][0] >= x1 
                                or listePositionsLignes[0][0] <= x2 and listePositionsLignes[-1][0] == x1 and listePositionsLignes[-1][1] >= y1 
                                or listePositionsLignes[-1][1] <= y2)  :
                                    listePositionsLignes.append((x1, y1))
                            #Remplissage du coin en bas à gauche
                            if (listePositionsLignes[0][1] == y2 and listePositionsLignes[0][0] > x1 
                                or listePositionsLignes[0][0] < x2 and listePositionsLignes[-1][0] == x1 and listePositionsLignes[-1][1] > y1 
                                or listePositionsLignes[-1][1] < y2)  :
                                    listePositionsLignes.append((x1,y2))
                        
                            tracerPolygone(listePositionsLignes)
                            listePositionsPolygone.extend(listePositionsLignes)
                        
                            enTrainDeDessiner = not enTrainDeDessiner

                #Deplacement du joueur vers la droite
                if touche(ev) == "Right" and xJoueur < x2:
                    xJoueur += tailleJoueur
                    if enTrainDeDessiner:
                        dessin(oldX, oldY, xJoueur, oldY)
                        listePositionsLignes.append((oldX, oldY, xJoueur, oldY))
                        if (xJoueur <= x1 or xJoueur >= x2 or yJoueur <= y1 or yJoueur >= y2):
                            dernierPoint = listePositionsLignes[-1][2:]
                            listePositionsLignes.append((xJoueur, yJoueur, *dernierPoint))
                            #Remplissage du coin en haut à droite
                            if (listePositionsLignes[0][1] == y1 and listePositionsLignes[0][0] > x1 
                                or listePositionsLignes[0][0] < x2 and listePositionsLignes[-1][0] == x2 and listePositionsLignes[-1][1] > y1 
                                or listePositionsLignes[-1][1] < y2)  :
                                    listePositionsLignes.append((x2,y1))
                            #Remplissage du coin en bas à droite
                            if (listePositionsLignes[0][1] == y2 and listePositionsLignes[0][0] > x1 
                                or listePositionsLignes[0][0] < x2 and listePositionsLignes[-1][0] == x2 and listePositionsLignes[-1][1] > y1 
                                or listePositionsLignes[-1][1] < y2)  :
                                    listePositionsLignes.append((x2,y2))
                            
                            tracerPolygone(listePositionsLignes)
                            listePositionsPolygone.extend(listePositionsLignes)
                            
                            enTrainDeDessiner = not enTrainDeDessiner

                efface("joueur")
                joueur(xJoueur, yJoueur)

                #Appuyer une fois sur Entrée pour dessiner
                if touche(ev) == "Return":
                    enTrainDeDessiner = not enTrainDeDessiner
                    
        print(listePositionsLignes)            
        mise_a_jour()

    ferme_fenetre()