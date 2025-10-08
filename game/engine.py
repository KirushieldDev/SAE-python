"""
Module principal du jeu QIX - Version POO optimisée
"""
from fltk import *
import time
from random import randint
from .entities import Player, Ghost, Sparx, Apple
from .geometry import PolygonManager
from .renderer import *

class QixGame:
    """Classe principale du jeu QIX avec architecture POO"""
    
    def __init__(self):
        """Initialise le jeu QIX"""
        self.window_width = 1500
        self.window_height = 900
        
        # Mode de jeu
        self.single_player = False
        self.two_players = False
        
        # Difficulté
        self.easy = False
        self.normal = False
        self.hard = False
        
        # Limites de l'aire de jeu
        self.game_bounds = {}
        
        # Entités du jeu
        self.players = []
        self.ghosts = []
        self.sparx_list = []
        self.apples = []
        self.obstacles = []
        
        # Gestionnaires de polygones
        self.polygon_managers = []
        
        # État du jeu
        self.lives = [3, 3]  # Vies pour joueur 1 et 2
        self.running = True
        
        # Optimisation : limiter les mises à jour d'affichage
        self.last_update_time = 0
        self.update_interval = 1/30  # 30 FPS au lieu de 60 pour plus de fluidité
        self.last_cleanup_time = 0
        self.cleanup_interval = 5.0  # Nettoyage toutes les 5 secondes
    
    def initialize_window(self):
        """Crée la fenêtre de jeu"""
        cree_fenetre(self.window_width, self.window_height)
    
    def choose_game_mode(self):
        """Gère le menu de sélection du mode de jeu"""
        afficher_menu_mode(self.window_width, self.window_height)
        
        while True:
            mouse_x, mouse_y = attend_clic_gauche()
            if 375 <= mouse_x <= 1125:
                if 300 <= mouse_y <= 410:
                    self.single_player = True
                    break
                elif 440 <= mouse_y <= 550:
                    self.two_players = True
                    break
    
    def choose_difficulty(self):
        """Gère le menu de sélection de la difficulté"""
        afficher_menu_difficulte(self.window_width, self.window_height)
        
        while True:
            mouse_x, mouse_y = attend_clic_gauche()
            if 375 <= mouse_x <= 1125:
                if 300 <= mouse_y <= 410:
                    self.easy = True
                    break
                elif 440 <= mouse_y <= 550:
                    self.normal = True
                    break
                elif 580 <= mouse_y <= 690:
                    self.hard = True
                    break
    
    def initialize_game(self):
        """Initialise tous les éléments du jeu"""
        # Configuration de l'aire de jeu
        x1, x2, y1, y2 = afficher_aire_jeu(self.window_width, self.window_height)
        self.game_bounds = {'x1': x1, 'x2': x2, 'y1': y1, 'y2': y2}
        
        # Vitesses selon la difficulté
        if self.easy:
            ghost_speed_x, ghost_speed_y = 3, 2
            sparx_speed = 2
        elif self.normal:
            ghost_speed_x, ghost_speed_y = 5, 3
            sparx_speed = 4
        else:  # hard
            ghost_speed_x, ghost_speed_y = 7, 5
            sparx_speed = 6
        
        # Création des joueurs
        if self.two_players:
            player1 = Player(1, x2, y2, "lime", "red")
            player2 = Player(2, x1, y2, "yellow", "purple")
            self.players = [player1, player2]
        else:
            player1 = Player(1, (x1 + x2) // 2, y2, "lime", "red")
            self.players = [player1]
        
        # Création des gestionnaires de polygones
        for i, player in enumerate(self.players):
            manager = PolygonManager(player.player_id, self.game_bounds)
            self.polygon_managers.append(manager)
        
        # Création des fantômes
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        
        ghost1 = Ghost(1, center_x, center_y, ghost_speed_x, ghost_speed_y, "Qix2.gif")
        self.ghosts = [ghost1]
        
        if self.hard:
            ghost2 = Ghost(2, center_x, center_y, -ghost_speed_x, ghost_speed_y, "Fantome.gif")
            self.ghosts.append(ghost2)
        
        # Création des Sparx
        sparx1 = Sparx(1, (x1 + x2) // 2, y1, sparx_speed, True)
        sparx2 = Sparx(2, (x1 + x2) // 2, y1, sparx_speed, False)
        self.sparx_list = [sparx1, sparx2]
        
        # Génération des pommes et obstacles
        self.generate_apples_and_obstacles()
    
    def generate_apples_and_obstacles(self):
        """Génère les pommes et obstacles"""
        # Pommes
        num_apples = randint(5, 8)
        for _ in range(num_apples):
            x = randint(self.game_bounds['x1'], self.game_bounds['x2'])
            y = randint(self.game_bounds['y1'], self.game_bounds['y2'])
            self.apples.append(Apple(x, y))
        
        # Obstacles
        num_obstacles = randint(1, 5)
        for _ in range(num_obstacles):
            size = randint(20, 50)
            x = randint(self.game_bounds['x1'], self.game_bounds['x2'] - size)
            y = randint(self.game_bounds['y1'], self.game_bounds['y2'] - size)
            self.obstacles.append((x, y, x + size, y + size))
    
    def handle_input(self):
        """Gère les entrées clavier"""
        ev = donne_ev()
        if ev is None:
            return True
        
        if type_ev(ev) == "Quitte":
            return False
        
        if type_ev(ev) == "Touche":
            key = touche(ev)
            
            # Contrôles joueur 1
            if len(self.players) >= 1:
                player1 = self.players[0]
                moved = False
                
                if key == "Up":
                    moved = player1.move(0, -player1.speed, self.game_bounds, self.obstacles, self.polygon_managers[0].polygons)
                elif key == "Down":
                    moved = player1.move(0, player1.speed, self.game_bounds, self.obstacles, self.polygon_managers[0].polygons)
                elif key == "Left":
                    moved = player1.move(-player1.speed, 0, self.game_bounds, self.obstacles, self.polygon_managers[0].polygons)
                elif key == "Right":
                    moved = player1.move(player1.speed, 0, self.game_bounds, self.obstacles, self.polygon_managers[0].polygons)
                elif key == "Return":
                    if not player1.is_drawing:
                        player1.start_drawing()
                elif key == "space":
                    player1.increase_speed()
                
                # Si le joueur a atteint un bord en dessinant, créer un polygone
                if moved and player1.is_drawing:
                    area = self.polygon_managers[0].create_polygon(
                        player1.drawing_positions,
                        player1.start_drawing_position,
                        (player1.x, player1.y),
                        self.ghosts[0].x,
                        self.ghosts[0].y
                    )
                    player1.stop_drawing()
            
            # Contrôles joueur 2
            if len(self.players) >= 2:
                player2 = self.players[1]
                moved = False
                
                if key == "z":
                    moved = player2.move(0, -player2.speed, self.game_bounds, self.obstacles, self.polygon_managers[1].polygons)
                elif key == "s":
                    moved = player2.move(0, player2.speed, self.game_bounds, self.obstacles, self.polygon_managers[1].polygons)
                elif key == "q":
                    moved = player2.move(-player2.speed, 0, self.game_bounds, self.obstacles, self.polygon_managers[1].polygons)
                elif key == "d":
                    moved = player2.move(player2.speed, 0, self.game_bounds, self.obstacles, self.polygon_managers[1].polygons)
                elif key == "e":
                    if not player2.is_drawing:
                        player2.start_drawing()
                elif key == "v":
                    player2.increase_speed()
                
                # Si le joueur a atteint un bord en dessinant, créer un polygone
                if moved and player2.is_drawing:
                    area = self.polygon_managers[1].create_polygon(
                        player2.drawing_positions,
                        player2.start_drawing_position,
                        (player2.x, player2.y),
                        self.ghosts[0].x,
                        self.ghosts[0].y
                    )
                    player2.stop_drawing()
        
        return True
    
    def update_entities(self):
        """Met à jour toutes les entités"""
        # Collecte tous les polygones fermés pour les rebonds du QIX
        all_polygons = []
        for manager in self.polygon_managers:
            all_polygons.extend(manager.polygons)
        
        # Mise à jour des fantômes avec gestion des rebonds sur polygones
        for ghost in self.ghosts:
            ghost.update(self.game_bounds, all_polygons)
        
        # Mise à jour des Sparx
        for sparx in self.sparx_list:
            sparx.update(self.game_bounds)
        
        # Mise à jour de l'invincibilité des joueurs
        for player in self.players:
            player.update_invincibility()
    
    def cleanup_graphics(self):
        """Nettoie les éléments graphiques qui peuvent s'accumuler"""
        # Liste des tags à nettoyer périodiquement
        cleanup_tags = [
            "vie", "vie2", "vie3", "viej21", "viej22", "viej23",
            "airepoly", "player1", "player2", "txtinvin", "txtinvin2",
            "pomme", "txtAire"
        ]
        
        for tag in cleanup_tags:
            efface(tag)
    
    def check_collisions(self):
        """Vérifie toutes les collisions"""
        for i, player in enumerate(self.players):
            if player.invincible:
                continue
            
            # Collision avec les fantômes
            for ghost in self.ghosts:
                if ghost.check_collision_with_player(player):
                    self.lives[i] -= 1
                    player.reset_position()
                    # Ne pas supprimer les polygones fermés - ils restent des obstacles permanents
                    # self.polygon_managers[i].polygons.clear()
                    # self.polygon_managers[i].total_area = 0.0
                    break
                
                # NOUVELLE FONCTIONNALITÉ: Collision avec les lignes de dessin
                if player.is_drawing and ghost.check_collision_with_drawing_lines(player.drawing_positions):
                    self.lives[i] -= 1
                    player.reset_position()
                    # Ne pas supprimer les polygones fermés - ils restent des obstacles permanents
                    # self.polygon_managers[i].polygons.clear()
                    # self.polygon_managers[i].total_area = 0.0
                    break
            
            # Collision avec les Sparx
            for sparx in self.sparx_list:
                if sparx.check_collision_with_player(player):
                    self.lives[i] -= 1
                    player.reset_position()
                    # Ne pas supprimer les polygones fermés - ils restent des obstacles permanents
                    # self.polygon_managers[i].polygons.clear()
                    # self.polygon_managers[i].total_area = 0.0
                    break
        
        # Collision avec les pommes
        for apple in self.apples:
            for player in self.players:
                if apple.check_collision_with_player(player):
                    apple.collected = True
                    player.make_invincible()
                    break
        
        # Supprimer les pommes collectées
        self.apples = [apple for apple in self.apples if not apple.collected]
    
    def draw_all(self):
        """Dessine tous les éléments du jeu"""
        # Effacer les tags des entités mobiles ET les éléments d'interface
        efface("txtAire")
        efface("vie")
        efface("vie2") 
        efface("vie3")
        efface("viej21")
        efface("viej22")
        efface("viej23")
        efface("airepoly")
        efface("player1")
        efface("player2")
        efface("txtinvin")
        efface("txtinvin2")
        efface("pomme")
        
        # Dessiner les entités
        for player in self.players:
            player.draw()
        
        for ghost in self.ghosts:
            ghost.draw()
        
        for sparx in self.sparx_list:
            sparx.draw()
        
        # Dessiner les pommes
        for apple in self.apples:
            apple.draw()
        
        # Dessiner les obstacles (une seule fois, pas à chaque frame)
        if not hasattr(self, '_obstacles_drawn'):
            dessiner_obstacles(self.obstacles)
            self._obstacles_drawn = True
        
        # Afficher les vies et scores
        if self.two_players:
            afficher_vies(self.window_width, self.window_height, 
                         self.lives[0], self.lives[1], True)
            afficher_scores(self.window_width, self.window_height,
                           self.polygon_managers[0].total_area, self.polygon_managers[0].score,
                           self.polygon_managers[1].total_area, self.polygon_managers[1].score, True)
        else:
            afficher_vies(self.window_width, self.window_height, self.lives[0])
            afficher_scores(self.window_width, self.window_height,
                           self.polygon_managers[0].total_area, self.polygon_managers[0].score)
        
        # Afficher l'invincibilité
        for i, player in enumerate(self.players):
            if player.invincible:
                afficher_invincibilite(self.window_width, i + 1, self.two_players)
    
    def check_game_over(self):
        """Vérifie les conditions de fin de jeu"""
        # Vérifier les vies
        if self.single_player and self.lives[0] <= 0:
            return True
        elif self.two_players and all(life <= 0 for life in self.lives):
            return True
        
        # Vérifier la victoire (75% de territoire conquis)
        for manager in self.polygon_managers:
            if manager.total_area >= 75:
                return True
        
        return False
    
    def show_end_screen(self):
        """Affiche l'écran de fin"""
        time.sleep(0.1)
        efface_tout()
        
        # Déterminer si c'est une victoire ou une défaite
        victory = any(manager.total_area >= 75 for manager in self.polygon_managers)
        
        if victory:
            afficher_victoire(self.window_width, self.window_height)
        else:
            afficher_game_over(self.window_width, self.window_height)
        
        mise_a_jour()
        time.sleep(4)
    
    def main_loop(self):
        """Boucle principale du jeu optimisée"""
        frame_count = 0
        
        while self.running:
            current_time = time.time()
            
            # Limiter le taux de rafraîchissement pour améliorer les performances
            if current_time - self.last_update_time < self.update_interval:
                time.sleep(0.001)  # Petite pause pour éviter la surcharge CPU
                continue
            
            self.last_update_time = current_time
            frame_count += 1
            
            # Nettoyage périodique pour éviter l'accumulation d'éléments graphiques
            if current_time - self.last_cleanup_time > self.cleanup_interval:
                self.cleanup_graphics()
                self.last_cleanup_time = current_time
            
            # Gestion des entrées
            if not self.handle_input():
                break
            
            # Mise à jour des entités
            self.update_entities()
            
            # Vérification des collisions (optimisée - pas à chaque frame)
            if frame_count % 2 == 0:  # Collision check tous les 2 frames
                self.check_collisions()
            
            # Dessin (optimisé - pas tout à chaque frame)
            if frame_count % 1 == 0:  # Dessin à chaque frame mais optimisé
                self.draw_all()
                
                # Vérification de fin de jeu
                if self.check_game_over():
                    break
                
                # Mise à jour de l'affichage
                mise_a_jour()
        
        self.show_end_screen()
        ferme_fenetre()
    
    def run(self):
        """Lance le jeu complet"""
        self.initialize_window()
        self.choose_game_mode()
        self.choose_difficulty()
        self.initialize_game()
        self.main_loop()