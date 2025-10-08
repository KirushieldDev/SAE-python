"""
Launcher principal du jeu QIX
Ce fichier a été refactorisé pour utiliser la nouvelle architecture modulaire.
Tout le code de jeu a été déplacé dans le package 'game' pour faciliter le débogage.
"""
from game import QixGame

if __name__ == "__main__":
    # Créer et lancer le jeu
    jeu = QixGame()
    jeu.run()
