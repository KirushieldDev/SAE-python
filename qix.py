#--------------------------import---------------------------#
#-----------------------------------------------------------#

from fltk import *
import random

#-----------------------------------------------------------#
#___________________________________________________________#



#----------------les declarations de variables----------------#
#-------------------------------------------------------------#
return1 = 0
lives = 3
lancement_dessin = False
ligne_tracee = False
largeur_ecran = 800
hauteur_ecran = 800
dep = 5
yr1, xr1, yr2, xr2 = 400, 150, 400, 150
cx, cy, rayon = 100, 150, 10
qix_x, qix_y = largeur_ecran // 2, hauteur_ecran // 2
qix_radius = 10
qix_speed = 2
liste_coordonnees = []
#-----------------------------------------------------------#
#___________________________________________________________#



#------------------Crée une fenêtre de jeu------------------#
#-----------------------------------------------------------#
cree_fenetre(largeur_ecran, hauteur_ecran)
remplissage="black"
efface_tout()
rectangle(0, 0, 800, 800, remplissage="black")
texte(largeur_ecran//2-30, 25, "QIX", couleur='white',)
rectangle(100, 150, 700, 750, epaisseur=2, couleur="white")
#-----------------------------------------------------------#
#___________________________________________________________#



#--------------------------------------------------------fonction--------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------#
def carre(x, y, rayon):
   cercle(x, y, rayon, "green", "green", tag='carre')

# dessin initial du carré
#cx, cy, taille = 700, 750, 10
carre(cx, cy, rayon)


# Qix position et movement


#dessiner le qix
def dessiner_qix(qix_x, qix_y):
    qix_x = max(100 + qix_radius, min(qix_x, 700 - qix_radius))
    qix_y = max(150 + qix_radius, min(qix_y, 750 - qix_radius))
    cercle(qix_x, qix_y, qix_radius, "blue", "blue", tag='qix')
    return qix_x, qix_y


#création du premier point rouge sur les lignes blanches
def cercle1(yr1, xr1):
   cercle(yr1, xr1, 5, couleur="red", remplissage="red", tag='cercle1')
#création du deuxième
def cercle2(yr2, xr2):
   cercle(yr2, xr2, 5, couleur="red", remplissage="red", tag='cercle2')

def limitation(x, y):
    if lancement_dessin:
        return False
    # Vérifier si le joueur est sur une ligne existante
    lines = [(xr1, yr1), (xr2, yr2)]
    for line_x, line_y in lines:
        if x == line_x and y == line_y:
            return True
    if x == 100 or x == 700 or y == 150 or y == 750:
        return True
    if x < 100 or x > 700 or y < 150 or y > 750:
        return False
    return False


def vie ():
    efface("12")
    texte(10, 10, f"Vies: {lives}", couleur="white", tag="12")
    

def perdreVie():
    global lives
    lives -= 1
    efface('life_text')
    texte(largeur_ecran // 2, hauteur_ecran // 2, "You Lost a Life", couleur="red", tag='life_text')
    mise_a_jour()
    efface('life_text')

def game_over():
    efface_tout()
    efface('dessiner_qix')
    efface('carre')
    efface('cercle1')
    efface('cercle2')
    texte(largeur_ecran // 2, hauteur_ecran // 2, "Game Over", couleur="white")
    mise_a_jour()
    reset_game()
    ferme_fenetre()

def reset_game():
    global lives
    lives = 3  # Reset lives to initial value
    efface('life_text')  # Clear any remaining "You Lost a Life" message
    # Reset other game variables and positions as needed
    # Implement code to redraw the initial state of the game

def creer_polygone(liste_coordonnees):
    if len(liste_coordonnees) > 2:
        # Close the polygon by adding the starting point to the end
        liste_coordonnees.append(liste_coordonnees[0])
        polygone(liste_coordonnees, couleur="white", remplissage="blue", epaisseur=1, tag='polygone1')
        efface('carre')  # Remove the player's square from the screen
        cx, cy = liste_coordonnees[0]  # Set player's position to the polygon's starting point
        carre(cx, cy, rayon)  # Redraw the player's square

def detecter_collision_ligne(cx, cy, xr1, yr1, xr2, yr2, distance_tolerance):
    # Calculez la distance entre le joueur (cx, cy) et la ligne définie par les points (xr1, yr1) et (xr2, yr2).
    # Utilisez la formule de distance entre un point et une ligne.

    # Calculez la distance entre le joueur et les deux points de la ligne
    distance1 = ((cx - xr1) ** 2 + (cy - yr1) ** 2) ** 0.5
    distance2 = ((cx - xr2) ** 2 + (cy - yr2) ** 2) ** 0.5

    # Calculez la longueur de la ligne
    line_length = ((xr2 - xr1) ** 2 + (yr2 - yr1) ** 2) ** 0.5

    # Calculez la distance entre le joueur et la ligne (en utilisant la formule de projection)
    if line_length > 0:
        distance_line = abs((yr2 - yr1) * cx - (xr2 - xr1) * cy + xr2 * yr1 - yr2 * xr1) / line_length
    else:
        # Si les deux points sont identiques (longueur de la ligne nulle), utilisez la distance au premier point
        distance_line = distance1

    # Vérifiez si la distance à la ligne est inférieure ou égale à la tolérance de distance
    return distance_line <= distance_tolerance

#------------------------------------------------------------------------------------------------------------------------#
#________________________________________________________________________________________________________________________#


#------------------------------------------------------boucle while------------------------------------------------------#
#------------------------------------------------------------------------------------------------------------------------#
while lives != 0 or lives < 0:
    ev = donne_ev()
    tev = type_ev(ev)
    lx = cx
    ly = cy
    # Déplacement du carré
    dx = 0
    dy = 0
    if tev == 'Quitte':
        break
    if tev == 'Touche':
        nom_touche = touche(ev)
        
        if nom_touche == 'Left':
            if return1 == 0:
                if limitation(cx - dep, cy):
                    dx = -dep
            else:
                dx = max(-dep, -cx)
                
        elif nom_touche == 'Right':
            if return1 == 0:
                if limitation(cx + dep, cy):
                    dx = dep
            else:
                dx = min(dep, 749 - cx - rayon)
        elif nom_touche == 'Down':
            if return1 == 0:
                if limitation(cx, cy + dep):
                    dy = dep
            else:
                dy = min(dep, 760 - cy - rayon)
        elif nom_touche == 'Up':
            if return1 == 0:
                if limitation(cx, cy - dep):
                    dy = -dep
            else:
                dy = max(-dep, -cy)
                
        if dx != 0 or dy != 0:
            efface('carre')
            cx = max(100, min(cx + dx, 700))
            cy = max(150, min(cy + dy, 750))
            carre(cx, cy, rayon)

        
            
            liste_coordonnees.append((cx, cy))
        if nom_touche == 'Return':
            return1 = return1 + 1 
            if not lancement_dessin:
                lancement_dessin = True
                # Create the polygon immediately when "Return" is pressed
                if len(liste_coordonnees) > 0:
                    if liste_coordonnees[-1][0] <= 100 or liste_coordonnees[-1][0] >= 700 or liste_coordonnees[-1][1] <= 150 or liste_coordonnees[-1][1] >= 750:
                        creer_polygone(liste_coordonnees)
                    liste_coordonnees = []
            else:
                return1 = 0
                lancement_dessin = False
                if len(liste_coordonnees) > 0:
                    if (
                        (liste_coordonnees[-1][0] <= 100 or liste_coordonnees[-1][0] >= 700 or
                        liste_coordonnees[-1][1] <= 150 or liste_coordonnees[-1][1] >= 750) or
                        (liste_coordonnees[-1][0] <= 100 or liste_coordonnees[-1][0] >= 700 or
                        liste_coordonnees[-1][1] <= 150 or liste_coordonnees[-1][1] >= 750) or
                        (liste_coordonnees[-1][0] <= 100 or liste_coordonnees[-1][0] >= 700 or
                        liste_coordonnees[-1][1] <= 150 or liste_coordonnees[-1][1] >= 750) or
                        (liste_coordonnees[-1][0] <= 100 or liste_coordonnees[-1][0] >= 700 or
                        liste_coordonnees[-1][1] <= 150 or liste_coordonnees[-1][1] >= 750)
                        ):
                        
                        creer_polygone(liste_coordonnees)
                        liste_coordonnees = []
        
        elif lancement_dessin and nom_touche == 'Return':
            lancement_dessin = False
            ligne_tracee = False
            
        if lancement_dessin:
                if not ligne_tracee:
                    lx, ly = cx, cy
                    ligne_tracee = True
                else:
                    ligne(lx, ly, cx, cy, couleur="white", epaisseur=2)
                    lx, ly = cx, cy

   #point rouge sur les lignes blanches .
    if xr1==150 and yr1<699:
        yr1=yr1+1
        efface('cercle1')
        cercle1(yr1, xr1)
    elif yr1==699 and xr1>=150 and xr1<749:
        xr1=xr1+1
        efface('cercle1')
        cercle1(yr1, xr1)
    elif xr1==749 and yr1>100:
        yr1=yr1-1
        efface('cercle1')
        cercle1(yr1, xr1)
    else :
        xr1=xr1-1
    efface('cercle1')
    cercle1(yr1, xr1)
  


   #deuxième point rouge sur les lignes blanches .
    if xr2==150 and yr2>100:
        yr2=yr2-1
        efface('cercle2')
        cercle2(yr2, xr2)
    elif yr2==100 and xr2>=150 and xr2<749:
        xr2=xr2+1
        efface('cercle2')
        cercle2(yr2, xr2)
    elif xr2==749 and yr2<699:
        yr2=yr2+1
        efface('cercle2')
        cercle2(yr2, xr2)
    else :
        xr2=xr2-1
    efface('cercle2')
    cercle2(yr2, xr2)
    
    
   # Qix movement (random)
    qix_x += random.uniform(-qix_speed* 2.5 , qix_speed * 2.5)
    qix_y += random.uniform(-qix_speed* 2.5 , qix_speed * 2.5)
    efface('qix')

    dessiner_qix(qix_x, qix_y)

        # Detect collision with Qix
    qix_collision_distance = rayon + qix_radius
    if (abs(cx - qix_x) < qix_collision_distance) and (abs(cy - qix_y) < qix_collision_distance):
        perdreVie()
        if lives <= 0:
            game_over()
        else:
            # Reset the player's position
            efface('carre')
            cx, cy = 100, 150
            carre(cx, cy, rayon)

    # Detect collision with red circles
    cercle1_collision_distance = rayon + 5  # Radius of red circles
    cercle2_collision_distance = rayon + 5
    if (abs(cx - xr1) < cercle1_collision_distance) and (abs(cy - yr1) < cercle1_collision_distance):
        perdreVie()
        if lives <= 0:
            game_over()
        else:
            cx, cy = 100, 150
            carre(cx, cy, rayon)

    if (abs(cx - xr2) < cercle2_collision_distance) and (abs(cy - yr2) < cercle2_collision_distance):
        perdreVie()
        if lives <= 0:
            game_over()
        else:
            cx, cy = 100, 150
            carre(cx, cy, rayon)

    vie()

    mise_a_jour()
    
#------------------------------------------------------------------------------------------------------------------------#
#________________________________________________________________________________________________________________________#


#-------------------------fermeture-------------------------#
#-----------------------------------------------------------#

ferme_fenetre()

#-----------------------------------------------------------#
#___________________________________________________________#