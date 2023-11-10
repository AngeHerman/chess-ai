# kouehemazro-nzaba-plong-2023

## Problèmes

Implémenter une version du jeu Morpion, ainsi qu'un algorithme de recherche 
de solution en utilisant un language de programmation fonctionnel OCaml.
Le but du jeu est le suivant : aligner cinq de ses 
symboles horizontalement, verticalement ou en diagonale.
Notre version du jeu est dans un quadrillage 11x11.
Le joueur sera informé à chaque coup si il est toujours apte à 
gagner la partie ou non.
On implémentera pour cela un algorithme de recherche deterministe,
qui indiquera au joueur les places optimales ou placer son symbole
afin d'avoir une chance de gagner la partie.


## Objectifs

- Principaux :  Implémenter l'algorithme de recherche.
Mettre en place le jeu du morpion en version textuel 
Ce qui impliuque :
Pouvoir placer les symboles dans les cases. 
Les cases doivent donc être nommées.
Vérifier lorsque nous sommes dans un état de défaite ou victoire.
Mettre en place un système de tour
Etudier les différentes bibliothèques graphique d'OCaml, en sélectionner.
une afin d'implémenter un système de fenêtre graphique.

- Intermédiaire : 
Implémenter un bot pouvant jouer contre le joueur.

- Supplémentaires :  
Mettre en surbrillance les cases qui peuvent nous emmener a la victoire.
Afficher les pourcentages de réusite pour chaque case en surbrillance.
Barrer les cases concernées quand un des joueurs gagne.
Intégrer la possibilité d'avoir un bot contre un autre bot.



## Testabilité
- Vérifier la fin du jeu.
- Tester le fonctionnement de l'algorithme de recherche.
- Tester la liaison entre le bakcend et le plateau en frontend.
- Tester l'intelligence des bots.


## Originalité
On utilise un language basé sur un paradigme de programmation
qui n'est pas généralement utiliser pour le developpement de jeu vidéo.

## Collage API
On utilise aucune API, uniquement Ocaml from scratch

## Calendrier/ Jalons

- Implémentation des différents entités du système : Novembre - Décembre
- Mise en place de la version textuel du jeu : Novembre - Fevrier
- Etude des bibliothèques graphique d'OCaml : Décembre
- Implémenter l'algorithme de recherche : Janvier
- Mise en place de la partie graphique : Janvier - Fevrier
- Lier la partie graphique avec le backend : Fevrier - Mars
- Finir les tâches non terminées : Mars - Avril
- Effectuer les tests et rédiger la documentation : Avril

