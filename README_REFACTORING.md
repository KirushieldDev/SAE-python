# Documentation - Refactorisation du jeu QIX

## Structure du projet

Le projet a été refactorisé pour une meilleure organisation et faciliter le débogage. Voici la nouvelle structure :

```
SAE-python/
├── Prog2.py                 # Launcher principal (point d'entrée)
├── fltk.py                 # Bibliothèque graphique
├── game/                   # Package principal du jeu
│   ├── __init__.py         # Initialisation du package
│   ├── engine.py          # Moteur principal du jeu (classe QixGame)
│   ├── entities.py        # Gestion des entités (joueurs, fantômes, sparx)
│   ├── geometry.py        # Calculs géométriques et collisions
│   └── renderer.py        # Fonctions de rendu et d'affichage
└── assets/                # Images du jeu (*.gif)
```

## Modules

### 1. `Prog2.py` - Launcher principal
- **Rôle** : Point d'entrée simple qui lance le jeu
- **Contenu** : Instancie `QixGame` et appelle `run()`
- **Avantage** : Code minimal, facile à comprendre

### 2. `game/engine.py` - Moteur principal
- **Classe** : `QixGame`
- **Rôle** : Gère la logique principale du jeu, la boucle de jeu, et coordonne tous les modules
- **Méthodes principales** :
  - `run()` : Lance le jeu complet
  - `boucle_principale()` : Boucle de jeu principale
  - `gerer_entrees_clavier()` : Gestion des inputs
  - `gerer_collisions()` : Détection des collisions
  - `gerer_deplacement_fantomes()` : Mouvement des ennemis

### 3. `game/entities.py` - Entités du jeu
- **Rôle** : Gère les joueurs, fantômes et sparx
- **Fonctions principales** :
  - `joueur()`, `joueur2()` : Affichage des joueurs
  - `fantome()`, `fantome2()` : Affichage des Qix
  - `sparx1()`, `sparx2()` : Affichage des sparx
  - `deplacer_joueur()`, `deplacer_joueur2()` : Déplacement avec validation

### 4. `game/geometry.py` - Calculs géométriques
- **Rôle** : Gère tous les calculs mathématiques et géométriques
- **Fonctions principales** :
  - `calculer_aire()` : Calcul de l'aire des polygones
  - `intersection_test()` : Test point-dans-polygone
  - `tracer_polygone()` : Création des polygones
  - `check_sparx_player()`, `check_qix_player()` : Détection de collisions
  - `trouver_coins()` : Calcul des coins pour fermer les polygones

### 5. `game/renderer.py` - Rendu et affichage
- **Rôle** : Gère tout l'affichage graphique (menus, HUD, etc.)
- **Fonctions principales** :
  - `afficher_menu_mode()`, `afficher_menu_difficulte()` : Menus
  - `afficher_vies()`, `afficher_scores()` : HUD
  - `afficher_victoire()`, `afficher_game_over()` : Écrans de fin
  - `dessiner_pommes()`, `dessiner_obstacles()` : Éléments de jeu

## Avantages de cette structure

### 1. **Séparation des responsabilités**
- Chaque module a un rôle spécifique et bien défini
- Plus facile de localiser un bug ou une fonctionnalité

### 2. **Facilité de débogage**
- Les fonctions sont regroupées logiquement
- Plus facile de tester chaque composant individuellement
- Messages d'erreur plus précis pointant vers le bon module

### 3. **Maintenabilité**
- Code plus lisible et organisé
- Modifications plus faciles à implémenter
- Moins de risque de casser autre chose en modifiant un module

### 4. **Réutilisabilité**
- Les modules peuvent être réutilisés dans d'autres projets
- Fonctions génériques (géométrie, rendu) facilement adaptables

### 5. **Extensibilité**
- Facile d'ajouter de nouvelles fonctionnalités
- Structure modulaire permet l'ajout de nouveaux modules

## Guide de débogage

### Problème avec les menus ou l'affichage
→ Vérifier `game/renderer.py`

### Problème avec les déplacements ou collisions
→ Vérifier `game/entities.py` et `game/geometry.py`

### Problème avec la logique de jeu
→ Vérifier `game/engine.py`

### Problème au lancement
→ Vérifier `Prog2.py` et `game/__init__.py`

## Utilisation

Pour lancer le jeu :
```bash
python Prog2.py
```

Pour importer des modules dans d'autres scripts :
```python
from game import QixGame
from game.entities import joueur, fantome
from game.geometry import calculer_aire
from game.renderer import afficher_menu_mode
```

## Performance Windows

La refactorisation n'affecte pas directement les performances Windows liées à `fltk.py`. 
Pour améliorer les performances sur Windows, il faudrait modifier la fonction `update()` 
dans `fltk.py` pour utiliser `root.after()` au lieu de `sleep()`.