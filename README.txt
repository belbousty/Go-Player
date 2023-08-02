Binome : - EL BOUSTY Badreddine 
======   - SOUFARY Farouk


Myplayer:  "Ayume" 
========
    - Notre joueur "Ayume" est un joueur purement défensif, cette approche défensive consiste
        à minimiser au maximum le gain de l'adversaire, et profiter de certaines opportunités 
        au fur et à mesure de la partie, à maximiser son gain tout en prenant en considération
        la minimisation du gain adverse.
    
    - L'idée de la stratégie, consiste à construire une matrice de poids au début de la partie,
        où plus on s'approche du centre, plus le poids de la position augmente. Et à chaque fois
        que l'état du Board, la matrice poids change selon différents critères et aussi selon différents 
        coefficients. On liste les critères pris en compte au coup x, en considérant la matrice de poids 
        géneré au coup x-1 :
            - la connectivité.
            - les degrés de liberté.
            - les degrés de liberté de l'adversaire.
            - les pièces capturés.
            - le Nombre de voisins adversaire d'une position vide. 
            - la distance entre la position et le centre (variable) de la matrice 
                    (Ce centre à la valeur maximale des poids 
                    puis plus en s'éloigne plus le poids diminue)
    
    - D'un autre côté, le coefficient de chaque critère était choisis en fonction de la priorité 
        du critère. Principalement, les coefficients augmentent d'une façon exponentielle (2^ou 3^)
        cela permet au critère de forcement impacter le poids d'une position.

    - Après avoir terminé, on prend le poids maximal obtenu dans une position, puis on change
        La matrice, en considérant cette position comme étant le centre des poinds

    Exemple:
    ========

    Centre = Centre de la matrice

    [2, 2, 2, 2, 2]
    [2, 4, 4, 4, 2]
    [2, 4, 8, 4, 2]
    [2, 4, 4, 4, 2]
    [2, 4, 2, 2, 2]

    Centre = (1,1)
    
    [4, 4, 4, 2, 0]
    [4, 8, 4, 2, 0]
    [4, 4, 4, 2, 0]
    [2, 2, 2, 2, 0]
    [0, 0, 0, 0, 0]
