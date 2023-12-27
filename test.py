def raycasting(x, y, polygone):
    intersections = 0
    for i in range(len(polygone)):
        x1, y1 = polygone[i]
        x2, y2 = polygone[(i + 1) % len(polygone)]
        
        # Vérifie si le point se trouve à gauche du segment de bord
        if y > min(y1, y2) and y <= max(y1, y2) and x <= max(x1, x2) and y1 != y2:
            intersection_x = (y - y1) * (x2 - x1) / (y2 - y1) + x1
            if x1 == x2 or x <= intersection_x:
                intersections += 1
                print("l'intersection est : ",intersection_x)
    return intersections % 2 == 1  # Si le nombre d'intersections est impair, le point est à l'intérieur


polygone = [(1, 1), (5, 1), (5, 5), (1, 5)]
point_a_tester = (3, 3)

resultat = raycasting(point_a_tester[0], point_a_tester[1], polygone)
print("Le point est-il à l'intérieur du polygone ?", resultat)