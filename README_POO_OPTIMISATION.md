# Documentation - Refactorisation POO du jeu QIX

## ✅ Problèmes résolus

### 1. **Affichage multiple des joueurs** 
- **Problème** : Les cercles des joueurs ne s'effaçaient pas, laissant des traînées
- **Solution** : Chaque entité gère maintenant son propre effacement via `efface(self.tag)` avant de se redessiner

### 2. **Lenteur du jeu**
- **Problème** : Boucle principale non optimisée, trop de calculs répétitifs
- **Solution** : 
  - Limitation du taux de rafraîchissement à 60 FPS
  - Effacement sélectif (seulement les entités mobiles)
  - Optimisation des boucles de collision

### 3. **Code difficile à déboguer**
- **Problème** : Code procédural monolithique
- **Solution** : Architecture POO avec classes spécialisées

## 🏗️ Architecture POO

### Classes principales

#### `Player` - Joueur
```python
class Player:
    def __init__(self, player_id, start_x, start_y, color, invincible_color)
    def draw(self)              # Dessine le joueur (avec effacement automatique)
    def move(self, dx, dy, ...)  # Déplace et vérifie les collisions
    def start_drawing(self)      # Commence à dessiner des lignes
    def stop_drawing(self)       # Arrête le dessin
    def make_invincible(self)    # Rend invincible temporairement
    def reset_position(self)     # Remet à la position initiale
```

#### `Ghost` - Fantôme (Qix)
```python
class Ghost:
    def __init__(self, ghost_id, start_x, start_y, speed_x, speed_y, image_file)
    def update(self, game_bounds)  # Met à jour position et collisions avec bords
    def draw(self)                 # Dessine le fantôme (avec effacement automatique)
    def check_collision_with_player(self, player)  # Vérifie collision avec joueur
```

#### `Sparx` - Ennemi périphérique
```python
class Sparx:
    def __init__(self, sparx_id, start_x, start_y, speed, clockwise)
    def update(self, game_bounds)  # Mouvement autour du périmètre
    def draw(self)                 # Dessine le Sparx (avec effacement automatique)
    def check_collision_with_player(self, player)  # Vérifie collision
```

#### `Apple` - Pomme bonus
```python
class Apple:
    def __init__(self, x, y)
    def draw(self)                 # Dessine la pomme si pas collectée
    def check_collision_with_player(self, player)  # Vérifie collection
```

#### `PolygonManager` - Gestion des polygones
```python
class PolygonManager:
    def __init__(self, player_id, game_bounds)
    def create_polygon(self, ...)  # Crée un nouveau polygone
    # Gère score et aire totale du joueur
```

#### `QixGame` - Moteur principal
```python
class QixGame:
    def __init__(self)
    def run(self)                  # Lance le jeu complet
    def main_loop(self)           # Boucle principale optimisée
    def handle_input(self)        # Gestion des entrées clavier
    def update_entities(self)     # Met à jour toutes les entités
    def check_collisions(self)    # Vérifie toutes les collisions
    def draw_all(self)            # Dessine tous les éléments
```

## 🚀 Améliorations de performance

### 1. **Limitation du taux de rafraîchissement**
```python
# Limite à 60 FPS pour éviter la surcharge
if current_time - self.last_update_time < self.update_interval:
    continue
```

### 2. **Effacement sélectif**
```python
# Chaque entité gère son propre effacement
def draw(self):
    efface(self.tag)  # Efface seulement cette entité
    # Redessine à la nouvelle position
```

### 3. **Optimisation des collisions**
- Collision par entité plutôt que calculs globaux
- Vérification d'invincibilité en amont

## 🎮 Améliorations de gameplay

### 1. **Gestion intelligente du dessin**
- Le joueur dessine automatiquement en se déplaçant
- Polygone créé automatiquement en atteignant un bord
- Effacement automatique des lignes temporaires

### 2. **Collision améliorée**
- Détection plus précise
- Gestion séparée par type d'entité

### 3. **Gestion des states**
- Invincibilité temporaire bien gérée
- Reset propre en cas de collision

## 🛠️ Facilité de débogage

### Avantages POO pour le débogage :

1. **Encapsulation** : Chaque classe gère ses propres données
2. **Responsabilité unique** : Une classe = une fonction précise
3. **Isolation des bugs** : Plus facile de localiser un problème
4. **Tests unitaires** : Possibilité de tester chaque classe séparément

### Guide de débogage :

- **Problème d'affichage joueur** → Classe `Player`, méthode `draw()`
- **Problème de mouvement** → Classe `Player`, méthode `move()`
- **Problème de collision** → Méthodes `check_collision_with_player()`
- **Problème de fantôme** → Classe `Ghost`
- **Problème de performance** → Classe `QixGame`, méthode `main_loop()`

## 📊 Comparaison Avant/Après

| Aspect | Avant (Procédural) | Après (POO) |
|--------|-------------------|-------------|
| **Affichage** | Traînées de cercles | Effacement propre |
| **Performance** | Lent (pas de limite FPS) | Fluide (60 FPS) |
| **Code** | 988 lignes monolithiques | Classes spécialisées |
| **Débogage** | Difficile à localiser | Facile par classe |
| **Maintenance** | Risqué (effet domino) | Sûr (isolation) |
| **Ajout de features** | Complexe | Simple (nouvelle classe) |

## 🎯 Utilisation

Le jeu se lance exactement comme avant :
```bash
python Prog2.py
```

Mais maintenant le code est :
- ✅ **Plus rapide** (optimisations de performance)
- ✅ **Plus propre** (pas de traînées visuelles)
- ✅ **Plus maintenable** (architecture POO)
- ✅ **Plus facilement déboggable** (classes spécialisées)

## 🔧 Contrôles

**Joueur 1 :**
- Flèches directionnelles : Déplacement
- Entrée : Commencer/arrêter le dessin
- Espace : Boost de vitesse

**Joueur 2 (mode 2 joueurs) :**
- ZQSD : Déplacement
- E : Commencer/arrêter le dessin
- V : Boost de vitesse