"""
Module gérant le rendu et l'affichage du jeu
"""
from fltk import *
from random import randint

def dessiner_obstacles(obstacles):
    """Dessine tous les obstacles sur l'écran"""
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

def dessiner_pommes(pommes):
    """Dessine toutes les pommes sur l'écran"""
    for pomme in pommes:
        cercle(pomme[0], pomme[1], 5, couleur="red", remplissage="red", tag="pomme")

def afficher_menu_mode(largeur_fenetre, hauteur_fenetre):
    """Affiche le menu de sélection du mode de jeu"""
    rectangle(0, 0, largeur_fenetre, hauteur_fenetre, remplissage="black")
    image(largeur_fenetre//2, 160, "Qix.gif", 450, 200, ancrage="center", tag="im")
    rectangle(375, 300, largeur_fenetre-375, 410, couleur="gold", epaisseur=5)
    texte(450, 306, "Mode 1 joueur", couleur="gold", taille=60, police='Arabic Transparent')
    rectangle(375, 440, largeur_fenetre-375, 550, couleur="gold", epaisseur=5)
    texte(450, 447, "Mode 2 joueur", couleur="gold", taille=60, police='Arabic Transparent')

def afficher_menu_difficulte(largeur_fenetre, hauteur_fenetre):
    """Affiche le menu de sélection de la difficulté"""
    rectangle(0, 0, largeur_fenetre, hauteur_fenetre, remplissage="black")
    image(largeur_fenetre//2, 160, "Qix.gif", 450, 200, ancrage="center", tag="im")
    rectangle(375, 300, largeur_fenetre-375, 410, couleur="gold", epaisseur=5)
    texte(450, 306, "Facile", couleur="gold", taille=60, police='Arabic Transparent')
    rectangle(375, 440, largeur_fenetre-375, 550, couleur="gold", epaisseur=5)
    texte(450, 447, "Normale", couleur="gold", taille=60, police='Arabic Transparent')
    rectangle(375, 580, largeur_fenetre-375, 690, couleur="gold", epaisseur=5)
    texte(450, 588, "Difficile", couleur="gold", taille=60, police='Arabic Transparent')

def afficher_aire_jeu(largeur_fenetre, hauteur_fenetre):
    """Affiche l'aire de jeu principale"""
    rectangle(0, 0, largeur_fenetre, hauteur_fenetre, remplissage="black")
    x1 = largeur_fenetre//2 - 300
    x2 = largeur_fenetre//2 + 300
    y1 = 200
    y2 = 850
    rectangle(x1, y1, x2, y2, couleur="blue", epaisseur=3)
    ligne(x1 + 10, y1 - 10, x2 - 10, y1 - 10, couleur="red", epaisseur=5)
    image(largeur_fenetre//2 - 180, 115, "Qix.gif", 250, 100, ancrage="center", tag="im")
    return x1, x2, y1, y2

def afficher_vies(largeur_fenetre, hauteur_fenetre, vie, viej2=None, deuxjoueur=False):
    """Affiche les cœurs représentant les vies"""
    efface("vie")
    efface("viej21")
    decale = 0
    decale2 = 40
    decale3 = 80
    
    if deuxjoueur:
        decale = 150
        decale2 = 190
        decale3 = 230
    
    # Affichage des vies du joueur 1
    if vie >= 3:
        image(largeur_fenetre//2 + decale, 70, "coeur.gif", 50, 60, tag="vie")
    if vie >= 2:
        image(largeur_fenetre//2 + decale2, 70, "coeur.gif", 50, 60, tag="vie2")
    else:
        efface("vie2")
    if vie >= 1:
        image(largeur_fenetre//2 + decale3, 70, "coeur.gif", 50, 60, tag="vie3")
    else:
        efface("vie3")
    
    # Affichage des vies du joueur 2 si mode 2 joueurs
    if deuxjoueur and viej2 is not None:
        if viej2 >= 3:
            image(largeur_fenetre//2 + 150, 120, "coeur.gif", 50, 60, tag="viej21")
        if viej2 >= 2:
            image(largeur_fenetre//2 + 190, 120, "coeur.gif", 50, 60, tag="viej22")
        else:
            efface("viej22")
        if viej2 >= 1:
            image(largeur_fenetre//2 + 230, 120, "coeur.gif", 50, 60, tag="viej23")
        else:
            efface("viej23")

def afficher_scores(largeur_fenetre, hauteur_fenetre, somme_aire_polygones, score, 
                   somme_aire_polygones2=None, score2=None, deuxjoueur=False):
    """Affiche les scores et pourcentages d'aire"""
    if not deuxjoueur:
        texte(largeur_fenetre//2 + 380, hauteur_fenetre//2, f"{round(somme_aire_polygones, 1)}%", 
              couleur="white", tag="airepoly")
        texte(largeur_fenetre//2 + 380, hauteur_fenetre//2 + 40, f"Score : {round(score)}", 
              couleur="white", tag="airepoly")
    else:
        texte(largeur_fenetre//2 + 400, hauteur_fenetre//2, f"{round(somme_aire_polygones, 1)}%", 
              couleur="blue", tag="airepoly")
        texte(largeur_fenetre//2 + 400, hauteur_fenetre//2 + 40, f"Score Joueur 1 :{round(score)}", 
              couleur="blue", tag="airepoly")
        texte(largeur_fenetre//2 + 400, hauteur_fenetre//2 + 80, f"{round(somme_aire_polygones2, 1)}%", 
              couleur="red", tag="airepoly")
        texte(largeur_fenetre//2 + 400, hauteur_fenetre//2 + 120, f"Score Joueur 2 :{round(score2)}", 
              couleur="red", tag="airepoly")
        
        texte(largeur_fenetre//2 - 50, 50, "Joueur 1 :", couleur="white", taille=28, tag="player1")
        texte(largeur_fenetre//2 - 50, 100, "Joueur 2 :", couleur="white", taille=28, tag="player2")

def afficher_invincibilite(largeur_fenetre, joueur_num, deuxjoueur=False):
    """Affiche l'indicateur d'invincibilité"""
    if joueur_num == 1:
        if deuxjoueur:
            image(largeur_fenetre//2 + 380, 70, "invincible.gif", 200, 45, tag="txtinvin")
        else:
            image(largeur_fenetre//2 + 50, 120, "invincible.gif", 200, 50, tag="txtinvin")
    elif joueur_num == 2:
        image(largeur_fenetre//2 + 380, 120, "invincible.gif", 200, 45, tag="txtinvin2")

def afficher_victoire(largeur_fenetre, hauteur_fenetre):
    """Affiche l'écran de victoire"""
    rectangle(0, 0, largeur_fenetre, hauteur_fenetre, remplissage="black")
    image(largeur_fenetre//2, hauteur_fenetre//2, "youwin.gif", largeur_fenetre, hauteur_fenetre, tag="win")

def afficher_game_over(largeur_fenetre, hauteur_fenetre):
    """Affiche l'écran de game over"""
    rectangle(0, 0, largeur_fenetre, hauteur_fenetre, remplissage="black")
    image(largeur_fenetre//2, hauteur_fenetre//2, "Gameover2.gif", largeur_fenetre, hauteur_fenetre, tag="game_over")

def generer_pommes_et_obstacles(x1, x2, y1, y2):
    """Génère les pommes et obstacles aléatoirement"""
    # Création des pommes
    nombre_pommes = randint(5, 8)
    pommes = [(randint(x1, x2), randint(y1, y2)) for _ in range(nombre_pommes)]

    # Création des obstacles
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
    
    return pommes, obstacles