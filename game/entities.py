"""
Module gérant les entités du jeu avec classes POO
"""
from fltk import *
import time

class Player:
    """Classe représentant un joueur"""
    
    def __init__(self, player_id, start_x, start_y, color="lime", invincible_color="red"):
        self.player_id = player_id
        self.x = start_x
        self.y = start_y
        self.start_x = start_x
        self.start_y = start_y
        self.size = 5
        self.speed = 5
        self.color = color
        self.invincible_color = invincible_color
        self.invincible = False
        self.invincible_start_time = 0
        self.is_drawing = False
        self.drawing_positions = []
        self.polygon_positions = []
        self.start_drawing_position = None
        self.tag = f"joueur{player_id}"
        self.drawing_tag = f"dessin{player_id}"
        
    def update_invincibility(self):
        """Met à jour l'état d'invincibilité"""
        if self.invincible and time.time() - self.invincible_start_time >= 3:
            self.invincible = False
    
    def make_invincible(self):
        """Rend le joueur invincible"""
        self.invincible = True
        self.invincible_start_time = time.time()
    
    def draw(self):
        """Dessine le joueur à sa position actuelle"""
        # Efface l'ancienne position
        efface(self.tag)
        
        # Dessine à la nouvelle position
        current_color = self.invincible_color if self.invincible else self.color
        cercle(self.x, self.y, self.size, couleur=current_color, tag=self.tag)
    
    def move(self, dx, dy, game_bounds, obstacles, polygons=None):
        """Déplace le joueur en vérifiant les collisions"""
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Vérification des limites du jeu
        if (game_bounds['x1'] <= new_x <= game_bounds['x2'] and
            game_bounds['y1'] <= new_y <= game_bounds['y2'] and
            self._can_move_to(new_x, new_y, obstacles)):
            
            # Si en mode dessin, mouvement libre dans l'aire de jeu
            # Si pas en mode dessin, restriction aux bords valides
            if (self.is_drawing or 
                self._is_on_valid_boundary(new_x, new_y, game_bounds, polygons)):
                
                old_x, old_y = self.x, self.y
                self.x = new_x
                self.y = new_y
                
                # Gestion du dessin de lignes
                if self.is_drawing:
                    self._draw_line(old_x, old_y, new_x, new_y)
                    self.drawing_positions.append((old_x, old_y, new_x, new_y))
                    
                    # Vérification si on atteint un bord pour fermer le polygone
                    if (self._is_on_game_boundary(new_x, new_y, game_bounds) or
                        self._is_on_polygon_boundary(new_x, new_y, polygons)):
                        return True  # Signal pour fermer le polygone
                
                return False
        return False
    
    def _can_move_to(self, x, y, obstacles):
        """Vérifie si le joueur peut se déplacer à cette position"""
        for obstacle in obstacles:
            if obstacle[0] <= x <= obstacle[2] and obstacle[1] <= y <= obstacle[3]:
                return False
        return True
    
    def _is_on_valid_boundary(self, x, y, game_bounds, polygons):
        """Vérifie si le joueur est sur un bord valide (bord du jeu ou bord de polygone)"""
        # Si pas encore de polygones, seuls les bords du jeu sont valides
        if not polygons or len(polygons) == 0:
            return self._is_on_game_boundary(x, y, game_bounds)
        
        # Vérifier si on est sur un bord du jeu
        if self._is_on_game_boundary(x, y, game_bounds):
            return True
        
        # Vérifier si on est sur le bord d'un polygone fermé
        return self._is_on_polygon_boundary(x, y, polygons)
    
    def _is_on_game_boundary(self, x, y, game_bounds):
        """Vérifie si le joueur est sur un bord de l'aire de jeu"""
        tolerance = 2  # Tolérance pour être "sur" le bord
        return (abs(x - game_bounds['x1']) <= tolerance or  # Bord gauche
                abs(x - game_bounds['x2']) <= tolerance or  # Bord droit
                abs(y - game_bounds['y1']) <= tolerance or  # Bord haut
                abs(y - game_bounds['y2']) <= tolerance)    # Bord bas
    
    def _is_on_polygon_boundary(self, x, y, polygons):
        """Vérifie si le joueur est sur le bord d'un polygone fermé"""
        if not polygons:
            return False
        
        tolerance = 3  # Tolérance pour être "sur" le bord du polygone
        
        for polygon in polygons:
            if len(polygon.positions) >= 3:
                # Vérifier chaque segment du polygone
                for i in range(len(polygon.positions)):
                    p1 = polygon.positions[i]
                    p2 = polygon.positions[(i + 1) % len(polygon.positions)]
                    
                    # Coordonnées des points du segment
                    x1, y1 = p1[2], p1[3]
                    x2, y2 = p2[2], p2[3]
                    
                    # Calculer la distance du point au segment
                    from .geometry import GeometryHelper
                    distance = GeometryHelper.distance_point_to_line(x, y, x1, y1, x2, y2)
                    
                    if distance <= tolerance:
                        return True
        
        return False
    
    def _draw_line(self, x1, y1, x2, y2):
        """Dessine une ligne entre deux points"""
        line_color = "blue" if self.player_id == 1 else "red"
        ligne(x1, y1, x2, y2, couleur=line_color, tag=self.drawing_tag, epaisseur=3)
    
    def start_drawing(self):
        """Commence à dessiner"""
        self.is_drawing = True
        self.start_drawing_position = (self.x, self.y)
        self.drawing_positions = []
    
    def stop_drawing(self):
        """Arrête de dessiner et nettoie"""
        self.is_drawing = False
        self.drawing_positions = []
        efface(self.drawing_tag)
    
    def reset_position(self):
        """Remet le joueur à sa position initiale"""
        self.x = self.start_x
        self.y = self.start_y
        self.stop_drawing()
        self.polygon_positions.clear()
        efface(self.tag)
        efface(self.drawing_tag)
    
    def increase_speed(self):
        """Augmente la vitesse du joueur"""
        if not self.is_drawing:
            self.speed += 5

class Ghost:
    """Classe représentant un fantôme (Qix)"""
    
    def __init__(self, ghost_id, start_x, start_y, speed_x=5, speed_y=3, image_file="Qix2.gif"):
        self.ghost_id = ghost_id
        self.x = start_x
        self.y = start_y
        self.start_x = start_x
        self.start_y = start_y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.image_file = image_file
        self.width = 70
        self.height = 80
        self.tag = f"fant{ghost_id}"
    
    def update(self, game_bounds, polygons=None):
        """Met à jour la position du fantôme"""
        # Sauvegarder l'ancienne position
        old_x, old_y = self.x, self.y
        
        # Calculer la nouvelle position
        new_x = self.x + self.speed_x
        new_y = self.y - self.speed_y
        
        # Vérifier collision avec les polygones fermés (rebond)
        collision_detected = False
        bounce_x = False
        bounce_y = False
        
        if polygons:
            from .geometry import GeometryHelper
            
            # Définir les points de test du QIX (centre + bords)
            half_width = self.width // 2
            half_height = self.height // 2
            
            # Points de test pour une détection précise
            test_points = [
                (self.x, self.y),  # Centre
                (self.x - half_width, self.y),  # Gauche
                (self.x + half_width, self.y),  # Droite
                (self.x, self.y - half_height),  # Haut
                (self.x, self.y + half_height),  # Bas
                (self.x - half_width, self.y - half_height),  # Coin haut-gauche
                (self.x + half_width, self.y - half_height),  # Coin haut-droite
                (self.x - half_width, self.y + half_height),  # Coin bas-gauche
                (self.x + half_width, self.y + half_height),   # Coin bas-droite
            ]
            
            # Tester collision avec les nouvelles positions
            for polygon in polygons:
                if len(polygon.positions) >= 3:
                    # Test collision horizontale (mouvement en X)
                    test_points_x = [
                        (new_x, self.y),
                        (new_x - half_width, self.y),
                        (new_x + half_width, self.y),
                        (new_x, self.y - half_height),
                        (new_x, self.y + half_height),
                    ]
                    
                    for test_x, test_y in test_points_x:
                        if GeometryHelper.point_in_polygon(test_x, test_y, polygon.positions):
                            bounce_x = True
                            collision_detected = True
                            break
                    
                    # Test collision verticale (mouvement en Y)
                    test_points_y = [
                        (self.x, new_y),
                        (self.x - half_width, new_y),
                        (self.x + half_width, new_y),
                        (self.x, new_y - half_height),
                        (self.x, new_y + half_height),
                    ]
                    
                    for test_x, test_y in test_points_y:
                        if GeometryHelper.point_in_polygon(test_x, test_y, polygon.positions):
                            bounce_y = True
                            collision_detected = True
                            break
                    
                    # Si collision détectée, pas besoin de tester les autres polygones
                    if collision_detected:
                        break
        
        # Appliquer le rebond
        if bounce_x:
            self.speed_x = -self.speed_x
        if bounce_y:
            self.speed_y = -self.speed_y
        
        # Si pas de collision avec polygones, déplacer normalement
        if not collision_detected:
            self.x = new_x
            self.y = new_y
        
        # Collision avec les bords du jeu (correction avec vraie hitbox)
        half_width = self.width // 2
        half_height = self.height // 2
        
        # Vérification des bords horizontaux (gauche/droite)
        if self.x - half_width <= game_bounds['x1'] or self.x + half_width >= game_bounds['x2']:
            self.speed_x = -self.speed_x
            # Repositionner pour éviter de sortir
            if self.x - half_width <= game_bounds['x1']:
                self.x = game_bounds['x1'] + half_width
            if self.x + half_width >= game_bounds['x2']:
                self.x = game_bounds['x2'] - half_width
        
        # Vérification des bords verticaux (haut/bas)
        if self.y - half_height <= game_bounds['y1'] or self.y + half_height >= game_bounds['y2']:
            self.speed_y = -self.speed_y
            # Repositionner pour éviter de sortir
            if self.y - half_height <= game_bounds['y1']:
                self.y = game_bounds['y1'] + half_height
            if self.y + half_height >= game_bounds['y2']:
                self.y = game_bounds['y2'] - half_height
    
    def draw(self):
        """Dessine le fantôme"""
        # Efface l'ancienne position
        efface(self.tag)
        
        # Dessine à la nouvelle position
        image(self.x, self.y, self.image_file, self.width, self.height, 
              ancrage="center", tag=self.tag)
    
    def check_collision_with_player(self, player):
        """Vérifie la collision avec un joueur"""
        return (player.x + (player.size // 2) >= self.x - self.width // 2 and
                player.x + player.size <= self.x + self.width // 2 and
                player.y + (player.size // 2) >= self.y - self.height // 2 and
                player.y + player.size <= self.y + self.height // 2)
    
    def check_collision_with_drawing_lines(self, drawing_positions):
        """Vérifie la collision avec les lignes de dessin en cours"""
        if not drawing_positions:
            return False
        
        from .geometry import GeometryHelper
        return GeometryHelper.check_ghost_line_collision(
            self.x, self.y, self.width, self.height, drawing_positions
        )

class Sparx:
    """Classe représentant un Sparx"""
    
    def __init__(self, sparx_id, start_x, start_y, speed=3, clockwise=True):
        self.sparx_id = sparx_id
        self.x = start_x
        self.y = start_y
        self.speed = speed
        self.clockwise = clockwise
        self.width = 20
        self.height = 20
        self.tag = f"spar{sparx_id}"
        self.image_file = "Sparx.gif"
    
    def update(self, game_bounds):
        """Met à jour la position du Sparx autour du périmètre"""
        if self.clockwise:
            # Mouvement dans le sens horaire
            # Coin supérieur gauche
            if self.x <= game_bounds['x1'] and self.y <= game_bounds['y1']:
                self.x += self.speed
            # Coin supérieur droit
            elif self.x >= game_bounds['x2'] and self.y <= game_bounds['y1']:
                self.y += self.speed
            # Coin inférieur droit
            elif self.x >= game_bounds['x2'] and self.y >= game_bounds['y2']:
                self.x -= self.speed
            # Coin inférieur gauche
            elif self.x <= game_bounds['x1'] and self.y >= game_bounds['y2']:
                self.y -= self.speed
            # Bord supérieur (en mouvement vers la droite)
            elif self.y <= game_bounds['y1']:
                self.x += self.speed
            # Bord droit (en mouvement vers le bas)
            elif self.x >= game_bounds['x2']:
                self.y += self.speed
            # Bord inférieur (en mouvement vers la gauche)
            elif self.y >= game_bounds['y2']:
                self.x -= self.speed
            # Bord gauche (en mouvement vers le haut)
            elif self.x <= game_bounds['x1']:
                self.y -= self.speed
        else:
            # Mouvement dans le sens anti-horaire
            # Coin supérieur gauche
            if self.x <= game_bounds['x1'] and self.y <= game_bounds['y1']:
                self.y += self.speed
            # Coin supérieur droit
            elif self.x >= game_bounds['x2'] and self.y <= game_bounds['y1']:
                self.x -= self.speed
            # Coin inférieur droit
            elif self.x >= game_bounds['x2'] and self.y >= game_bounds['y2']:
                self.y -= self.speed
            # Coin inférieur gauche
            elif self.x <= game_bounds['x1'] and self.y >= game_bounds['y2']:
                self.x += self.speed
            # Bord supérieur (en mouvement vers la gauche)
            elif self.y <= game_bounds['y1']:
                self.x -= self.speed
            # Bord gauche (en mouvement vers le bas)
            elif self.x <= game_bounds['x1']:
                self.y += self.speed
            # Bord inférieur (en mouvement vers la droite)
            elif self.y >= game_bounds['y2']:
                self.x += self.speed
            # Bord droit (en mouvement vers le haut)
            elif self.x >= game_bounds['x2']:
                self.y -= self.speed
        
        # Correction des positions pour rester sur le périmètre
        if self.x < game_bounds['x1']:
            self.x = game_bounds['x1']
        elif self.x > game_bounds['x2']:
            self.x = game_bounds['x2']
        if self.y < game_bounds['y1']:
            self.y = game_bounds['y1']
        elif self.y > game_bounds['y2']:
            self.y = game_bounds['y2']
    
    def draw(self):
        """Dessine le Sparx"""
        # Efface l'ancienne position
        efface(self.tag)
        
        # Dessine à la nouvelle position
        image(self.x, self.y, self.image_file, self.width, self.height, 
              ancrage="center", tag=self.tag)
    
    def check_collision_with_player(self, player):
        """Vérifie la collision avec un joueur"""
        return (player.x + (player.size // 2) >= self.x and
                player.x + player.size <= self.x + self.width and
                player.y + (player.size // 2) >= self.y and
                player.y + player.size <= self.y + self.height)

class Apple:
    """Classe représentant une pomme"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 5
        self.color = "red"
        self.collected = False
        self._drawn = False  # Optimisation pour éviter le redessinage constant
    
    def draw(self):
        """Dessine la pomme"""
        if not self.collected and not self._drawn:
            cercle(self.x, self.y, self.size, couleur=self.color, remplissage=self.color, tag="pomme")
            self._drawn = True
        elif self.collected and self._drawn:
            # Efface la pomme quand elle est collectée
            efface("pomme")
            self._drawn = False
    
    def check_collision_with_player(self, player):
        """Vérifie la collision avec un joueur"""
        if self.collected:
            return False
        
        distance = ((self.x - player.x) ** 2 + (self.y - player.y) ** 2) ** 0.5
        return distance < player.size + self.size