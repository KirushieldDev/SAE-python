"""
Module gérant les calculs géométriques et les collisions (version POO)
"""
from fltk import *

class Polygon:
    """Classe représentant un polygone"""
    
    def __init__(self, positions, color, fill_color, game_bounds):
        self.positions = positions
        self.color = color
        self.fill_color = fill_color
        self.game_bounds = game_bounds
        self.area = 0.0
    
    def calculate_area(self):
        """Calcule l'aire du polygone en pourcentage"""
        if len(self.positions) < 3:
            return 0.0
        
        area = 0.0
        n = len(self.positions)
        
        for i in range(n):
            x1, y1 = self.positions[i][2], self.positions[i][3]
            x2, y2 = self.positions[(i + 1) % n][2], self.positions[(i + 1) % n][3]
            area += (x1 * y2 - x2 * y1)
        
        area_absolute = abs(area) / 2.0
        total_area = (self.game_bounds['x2'] - self.game_bounds['x1']) * (self.game_bounds['y2'] - self.game_bounds['y1'])
        area_percentage = (area_absolute / total_area) * 100
        self.area = area_percentage
        return area_percentage
    
    def draw(self):
        """Dessine le polygone"""
        if len(self.positions) >= 3:
            polygone(self.positions, couleur=self.color, remplissage=self.fill_color, tag="aire")

class GeometryHelper:
    """Classe utilitaire pour les calculs géométriques"""
    
    @staticmethod
    def point_in_polygon(x, y, polygon_positions):
        """Test point-dans-polygone (ray casting)"""
        intersections = 0
        n = len(polygon_positions)
        
        for i in range(n):
            x1, y1 = polygon_positions[i][2], polygon_positions[i][3]
            x2, y2 = polygon_positions[(i + 1) % n][2], polygon_positions[(i + 1) % n][3]
            
            if y > min(y1, y2) and y <= max(y1, y2) and x <= max(x1, x2) and y1 != y2:
                intersection_x = (y - y1) * (x2 - x1) / (y2 - y1) + x1
                if x1 == x2 or x <= intersection_x:
                    intersections += 1
        
        return intersections % 2 == 1
    
    @staticmethod
    def find_corners(start_pos, end_pos, game_bounds):
        """Trouve les coins nécessaires pour compléter le polygone"""
        x1, x2 = game_bounds['x1'], game_bounds['x2']
        y1, y2 = game_bounds['y1'], game_bounds['y2']
        
        if ((min(start_pos[1], end_pos[1]) == y1 and max(start_pos[1], end_pos[1]) == y2) or
            (min(start_pos[0], end_pos[0]) == x1 and max(start_pos[0], end_pos[0]) == x2)):
            
            y_corner1 = min(start_pos[1], end_pos[1])
            if y_corner1 == y1:
                x_corner1 = x_corner2 = x2
                y_corner2 = y2
            else:
                x_corner1 = x1
                y_corner1 = y_corner2 = y1
                x_corner2 = x2
            return [(None, None, x_corner1, y_corner1), (None, None, x_corner2, y_corner2)]
        
        x_corner = x1 if start_pos[0] == x1 or end_pos[0] == x1 else x2
        y_corner = y1 if start_pos[1] == y1 or end_pos[1] == y1 else y2
        return [(None, None, x_corner, y_corner)]
    
    @staticmethod
    def sort_corners(end_pos, corners):
        """Trie les coins pour le tracé du polygone"""
        if not corners:
            return []
        for corner in corners:
            if end_pos[0] == corner[2] or end_pos[1] == corner[3]:
                remaining_corners = list(set(corners) - {corner})
                return [corner] + GeometryHelper.sort_corners((corner[2], corner[3]), remaining_corners)
        return corners
    
    @staticmethod
    def inverse_corners(corners, game_bounds):
        """Inverse les coins sélectionnés"""
        x1, x2 = game_bounds['x1'], game_bounds['x2']
        y1, y2 = game_bounds['y1'], game_bounds['y2']
        all_corners = {(None, None, x1, y1), (None, None, x2, y1), 
                      (None, None, x2, y2), (None, None, x1, y2)}
        return list(all_corners - set(corners))
    
    @staticmethod
    def distance_point_to_line(px, py, x1, y1, x2, y2):
        """Calcule la distance entre un point et un segment de ligne"""
        # Vecteur de la ligne
        A = px - x1
        B = py - y1
        C = x2 - x1
        D = y2 - y1
        
        # Produit scalaire
        dot = A * C + B * D
        # Longueur au carré du segment
        len_sq = C * C + D * D
        
        if len_sq == 0:
            # Le segment est un point
            return ((px - x1) ** 2 + (py - y1) ** 2) ** 0.5
        
        # Paramètre de projection
        param = dot / len_sq
        
        if param < 0:
            # Le point le plus proche est x1, y1
            xx = x1
            yy = y1
        elif param > 1:
            # Le point le plus proche est x2, y2
            xx = x2
            yy = y2
        else:
            # Le point le plus proche est sur le segment
            xx = x1 + param * C
            yy = y1 + param * D
        
        # Distance
        dx = px - xx
        dy = py - yy
        return (dx * dx + dy * dy) ** 0.5
    
    @staticmethod
    def check_ghost_line_collision(ghost_x, ghost_y, ghost_width, ghost_height, drawing_positions):
        """Vérifie si un fantôme (QIX) entre en collision avec les lignes de dessin"""
        # Points de test plus précis du fantôme (centre + bords + coins)
        half_width = ghost_width // 2
        half_height = ghost_height // 2
        
        ghost_test_points = [
            (ghost_x, ghost_y),  # Centre
            (ghost_x - half_width, ghost_y),  # Gauche
            (ghost_x + half_width, ghost_y),  # Droite
            (ghost_x, ghost_y - half_height),  # Haut
            (ghost_x, ghost_y + half_height),  # Bas
            (ghost_x - half_width, ghost_y - half_height),  # Coin haut-gauche
            (ghost_x + half_width, ghost_y - half_height),  # Coin haut-droite
            (ghost_x - half_width, ghost_y + half_height),  # Coin bas-gauche
            (ghost_x + half_width, ghost_y + half_height),   # Coin bas-droite
            # Points intermédiaires pour une meilleure détection
            (ghost_x - half_width//2, ghost_y - half_height//2),
            (ghost_x + half_width//2, ghost_y - half_height//2),
            (ghost_x - half_width//2, ghost_y + half_height//2),
            (ghost_x + half_width//2, ghost_y + half_height//2),
        ]
        
        for line in drawing_positions:
            x1, y1, x2, y2 = line
            for test_x, test_y in ghost_test_points:
                distance = GeometryHelper.distance_point_to_line(test_x, test_y, x1, y1, x2, y2)
                if distance < 8:  # Augmenté le seuil pour une meilleure détection
                    return True
        return False

class PolygonManager:
    """Gestionnaire de polygones pour un joueur"""
    
    def __init__(self, player_id, game_bounds):
        self.player_id = player_id
        self.game_bounds = game_bounds
        self.polygons = []
        self.total_area = 0.0
        self.score = 0.0
    
    def create_polygon(self, drawing_positions, start_pos, end_pos, ghost_x, ghost_y):
        """Crée un nouveau polygone"""
        if len(drawing_positions) < 2:
            return 0.0
        
        # Détermine le type de fermeture nécessaire
        start_on_game_boundary = self._is_on_game_boundary(start_pos[0], start_pos[1])
        end_on_game_boundary = self._is_on_game_boundary(end_pos[0], end_pos[1])
        start_on_polygon = self._find_polygon_at_point(start_pos[0], start_pos[1])
        end_on_polygon = self._find_polygon_at_point(end_pos[0], end_pos[1])
        
        corners = []
        
        # Cas 1: Des deux bords de l'aire de jeu (logique originale)
        if start_on_game_boundary and end_on_game_boundary:
            corners = GeometryHelper.find_corners(start_pos, end_pos, self.game_bounds)
        
        # Cas 2: D'un polygone vers un bord de l'aire de jeu
        elif start_on_polygon and end_on_game_boundary:
            corners = self._trace_polygon_to_boundary(start_pos, end_pos, start_on_polygon)
        
        # Cas 3: D'un bord de l'aire de jeu vers un polygone
        elif start_on_game_boundary and end_on_polygon:
            corners = self._trace_boundary_to_polygon(start_pos, end_pos, end_on_polygon)
        
        # Cas 4: Entre deux polygones
        elif start_on_polygon and end_on_polygon:
            if start_on_polygon == end_on_polygon:
                # Même polygone - trace le contour
                corners = self._trace_same_polygon(start_pos, end_pos, start_on_polygon)
            else:
                # Polygones différents - connexion complexe
                corners = self._trace_between_polygons(start_pos, end_pos, start_on_polygon, end_on_polygon)
        
        # Si pas de coins trouvés, utiliser la logique originale
        if not corners:
            corners = GeometryHelper.find_corners(start_pos, end_pos, self.game_bounds)
        
        # Vérifie si le fantôme est dans le polygone potentiel
        test_positions = drawing_positions + corners
        ghost_inside = GeometryHelper.point_in_polygon(ghost_x, ghost_y, test_positions)
        
        if ghost_inside:
            corners = GeometryHelper.inverse_corners(corners, self.game_bounds)
        
        corners = GeometryHelper.sort_corners(end_pos, corners)
        final_positions = drawing_positions + corners
        
        # Détermine les couleurs selon le joueur
        if self.player_id == 1:
            color = "blue"
            fill_color = "purple"
        else:
            color = "red"
            fill_color = "red"
        
        # Crée et dessine le polygone
        polygon = Polygon(final_positions, color, fill_color, self.game_bounds)
        area = polygon.calculate_area()
        polygon.draw()
        
        self.polygons.append(polygon)
        self.total_area += area
        self.score += area * 25
        
        efface("airepoly")  # Efface l'ancien affichage du score
        return area
    
    def _is_on_game_boundary(self, x, y):
        """Vérifie si un point est sur le bord de l'aire de jeu"""
        tolerance = 3
        return (abs(x - self.game_bounds['x1']) <= tolerance or
                abs(x - self.game_bounds['x2']) <= tolerance or
                abs(y - self.game_bounds['y1']) <= tolerance or
                abs(y - self.game_bounds['y2']) <= tolerance)
    
    def _find_polygon_at_point(self, x, y):
        """Trouve le polygone dont le contour passe par ce point"""
        tolerance = 5
        
        for polygon in self.polygons:
            if len(polygon.positions) >= 3:
                # Vérifier chaque segment du polygone
                for i in range(len(polygon.positions)):
                    p1 = polygon.positions[i]
                    p2 = polygon.positions[(i + 1) % len(polygon.positions)]
                    
                    x1, y1 = p1[2], p1[3]
                    x2, y2 = p2[2], p2[3]
                    
                    distance = GeometryHelper.distance_point_to_line(x, y, x1, y1, x2, y2)
                    if distance <= tolerance:
                        return polygon
        return None
    
    def _trace_polygon_to_boundary(self, start_pos, end_pos, start_polygon):
        """Trace le chemin d'un polygone vers un bord de l'aire de jeu"""
        corners = []
        
        # Trouve les points du polygone à partir de la position de départ
        start_x, start_y = start_pos[0], start_pos[1]
        end_x, end_y = end_pos[0], end_pos[1]
        
        # Trouve l'index du point de départ sur le polygone
        start_index = self._find_closest_point_on_polygon(start_x, start_y, start_polygon)
        
        if start_index is not None:
            # Suit le contour du polygone depuis le point de départ
            # jusqu'à atteindre un point proche du bord de fin
            current_index = start_index
            polygon_positions = start_polygon.positions
            
            while True:
                current_pos = polygon_positions[current_index]
                corners.append(current_pos)
                
                # Vérifier si on est proche du point d'arrivée ou d'un coin approprié
                curr_x, curr_y = current_pos[2], current_pos[3]
                
                # Si on est proche du bord de destination, s'arrêter
                if (self._is_on_game_boundary(curr_x, curr_y) and 
                    self._is_close_to_end_boundary(curr_x, curr_y, end_x, end_y)):
                    break
                
                # Passer au point suivant du polygone
                current_index = (current_index + 1) % len(polygon_positions)
                
                # Éviter les boucles infinies
                if current_index == start_index:
                    break
        
        # Ajouter le coin final si nécessaire
        final_corner = self._get_appropriate_corner(end_pos)
        if final_corner and final_corner not in corners:
            corners.append(final_corner)
        
        return corners
    
    def _find_closest_point_on_polygon(self, x, y, polygon):
        """Trouve l'index du point le plus proche sur un polygone"""
        min_distance = float('inf')
        closest_index = None
        
        for i, pos in enumerate(polygon.positions):
            px, py = pos[2], pos[3]
            distance = ((px - x)**2 + (py - y)**2)**0.5
            
            if distance < min_distance:
                min_distance = distance
                closest_index = i
        
        return closest_index if min_distance <= 10 else None
    
    def _is_close_to_end_boundary(self, curr_x, curr_y, end_x, end_y):
        """Vérifie si on est sur le même bord que le point de fin"""
        tolerance = 20
        
        # Même bord vertical
        if (abs(curr_x - self.game_bounds['x1']) <= 3 and abs(end_x - self.game_bounds['x1']) <= 3) or \
           (abs(curr_x - self.game_bounds['x2']) <= 3 and abs(end_x - self.game_bounds['x2']) <= 3):
            return abs(curr_y - end_y) <= tolerance
        
        # Même bord horizontal
        if (abs(curr_y - self.game_bounds['y1']) <= 3 and abs(end_y - self.game_bounds['y1']) <= 3) or \
           (abs(curr_y - self.game_bounds['y2']) <= 3 and abs(end_y - self.game_bounds['y2']) <= 3):
            return abs(curr_x - end_x) <= tolerance
        
        return False
    
    def _get_appropriate_corner(self, end_pos):
        """Obtient le coin approprié pour fermer le polygone"""
        end_x, end_y = end_pos[0], end_pos[1]
        x1, x2 = self.game_bounds['x1'], self.game_bounds['x2']
        y1, y2 = self.game_bounds['y1'], self.game_bounds['y2']
        
        # Détermine le coin le plus proche
        if abs(end_x - x1) <= 3:  # Bord gauche
            corner_y = y1 if abs(end_y - y1) < abs(end_y - y2) else y2
            return (None, None, x1, corner_y)
        elif abs(end_x - x2) <= 3:  # Bord droit
            corner_y = y1 if abs(end_y - y1) < abs(end_y - y2) else y2
            return (None, None, x2, corner_y)
        elif abs(end_y - y1) <= 3:  # Bord haut
            corner_x = x1 if abs(end_x - x1) < abs(end_x - x2) else x2
            return (None, None, corner_x, y1)
        elif abs(end_y - y2) <= 3:  # Bord bas
            corner_x = x1 if abs(end_x - x1) < abs(end_x - x2) else x2
            return (None, None, corner_x, y2)
        
        return None
    
    def _trace_boundary_to_polygon(self, start_pos, end_pos, end_polygon):
        """Trace le chemin d'un bord vers un polygone"""
        # Logique similaire mais dans l'autre sens
        return self._trace_polygon_to_boundary(end_pos, start_pos, end_polygon)
    
    def _trace_same_polygon(self, start_pos, end_pos, polygon):
        """Trace le contour d'un même polygone"""
        corners = []
        
        # Trouve les segments du polygone entre start et end
        # Pour l'instant, utilise une approche simplifiée
        tolerance = 5
        start_found = False
        
        for i, pos in enumerate(polygon.positions):
            x, y = pos[2], pos[3]
            start_dist = ((x - start_pos[0])**2 + (y - start_pos[1])**2)**0.5
            end_dist = ((x - end_pos[0])**2 + (y - end_pos[1])**2)**0.5
            
            if start_dist <= tolerance:
                start_found = True
            elif end_dist <= tolerance and start_found:
                break
            elif start_found:
                corners.append(pos)
        
        return corners
    
    def _trace_between_polygons(self, start_pos, end_pos, start_polygon, end_polygon):
        """Trace entre deux polygones différents"""
        # Cas complexe - pour l'instant, utilise la logique de base
        return GeometryHelper.find_corners(start_pos, end_pos, self.game_bounds)

class CollisionDetector:
    """Détecteur de collisions"""
    
    @staticmethod
    def check_entity_collision(entity1, entity2):
        """Vérifie la collision entre deux entités"""
        # Simple collision rectangulaire
        return (entity1.x < entity2.x + getattr(entity2, 'width', entity2.size) and
                entity1.x + getattr(entity1, 'width', entity1.size) > entity2.x and
                entity1.y < entity2.y + getattr(entity2, 'height', entity2.size) and
                entity1.y + getattr(entity1, 'height', entity1.size) > entity2.y)