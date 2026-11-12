INTRODUCTION Projet Casse Brique Développement Logiciel en Python Natan HAIDER et Yanis BOUNIGUE :

l'URL de notre repository GitHub :
https://github.com/natbinks/natanhaider_yanisbounigue_cassebrique.git

Pour notre projet casse brique nous avons utilisé comme demandé la programmation en POO ainsi que l'implémentation des piles files listes.
Pour la POO nous avons créé une classe pour définir chaque objet tels que les briques la balle et la raquette.
Règles du jeu: casser toutes les briques avec la balle en évitant qu'elle tombe à l'aide de la raquette.
Si la balle tombe une vie est retirée et le jeu reprend jusqu'à la victoire ou la perte des trois vies.
Il y a trois niveaux différents lent moyen et rapide qui modifie à la fois la vitesse de la balle et le nombre de briques à casser
Nous avons essayé de styliser la fenêtre de sorte à avoir une fenêtre qui ressemble aux anciens écrans d'ordinateur tout gris/blanc 

---------------------------------------------------------------------------------------------------
Mode d'emploi de notre jeu:

-Choisir difficulté (lent, normal, rapide) ou lancer directement la parti (régler en mode normal de base)
-La raquette se contrôle avec les flèches directionnelles, droite et gauche
-Faire rebondir la balle sur la raquette et cassé toutes les briques sans perdre les 3 vies. 
-Le score augmente de 5 lorsqu'on touche une brique et de 10 lorsqu'on la casse

---------------------------------------------------------------------------------------------------
Problèmes rencontrés: 

-Nous avons fait des commit tardivement dans l'avancé du programme puisque l'un de nous avais un soucis avec github, que nous avons ensuite résolu.
-On avait oublie de faire en POO au début et nous avions du tout recommmencer
-Interface graphique difficle à prendre en main avec tkinter tout comme la physique de la balle et de la raquette (exemple: la balle touche deux briques sur le même lancer ce qu'on a partiellement réussi à régler).
-garder la progression de la partie après la perte d'une vie 
