Nous avons fait des points différents du programme.
Jawed s’est occupé de :
-La création des sparx et du Qix grâce au site figma
-L’initialisation des sparx en haut au centre et l’initialisation du Qix au centre de l’air de jeu
-La création de l’interface (fond noir, air de jeu bleu, implémentation du logo QIX, ligne rouge au dessus de l’air de jeu)
-Le déplacement aléatoire du Qix
-Le déplacement des sparx sur le cadre
-Les fonctions qui permette de repéré si le qix est dans le polygone du joueur
Kirushi s’est occupé de :
- La création et le déplacement du joueur 
- La fonction qui permet de dessiner les lignes
- La fonction qui permet de tracer les polygones
- Les fonctions qui détectent le contact des ennemis
- La fonciton qui calcule les surfaces des polygones

Nous avons organisé de le programme de manière suivante : 
Création des fonctions pour les différents aspects du jeu (Qix, Joueur, Sparx, Dessin, etc…)
Création de la fenêtre et de ses éléments (air de jeu, logo Qix, etc…)
Initialisation d’une boucle infini qui utilisera les fonctions afin de faire “vivre” le jeu (Déplacement du Qix, des Sparx, traçage des ligne derrière le joueur, etc…)

Nous avons rencontré plusieurs problème durant la programmation de ce jeu : 
Jawed : 
-Le Qix ne voulait pas bouger malgré mon code .
-Lorsqu’il a commencé à bouger il ne faisait que trembler.
-Les Sparx ne faisaient pas correctement tout le tour du cadre, ils s’arrêtaient lorsqu’ils atteignaient les deux coins du bas de l’air de jeu.
-Parfois les sparx sortaient de la fenêtre.

Kirushi :
- Parfois le joueur dépassait le cadre du jeu
- Il fallait régler le problème que l'utilisateur n'appuie pas sur plusieurs touches
- Pour tracer le polygone la liste qui prennait les positions, prennait toutes les positions du Joueur même sans dessiner
- Le calcul de surface des polygones
