# kouehemazro-nzaba-plong-2023

## Problèmes

Implémenter une version du jeu Star Defenders, en utilisant un 
language de programmation fonctionnel OCaml.
Le but du jeu est le suivant : contrôler un vaiseau pouvant se déplacer de gauche à droite et tirer des projectile en ligne droite.
Afin de passer au niveau suivant, l'utilisateur doit vaincre des vagues d'ennemies ainsi qu'un boss final.
Chaque niveau deviendra plus complexe, avec des vaiseaux adverses
différents (plus rapide, plus fort)

## Objectifs

- Principaux :  
Implémenter les différentes entités nécessaires au bon déroulement du jeu.  
Etudier les différentes bibliothèque graphique d'OCaml, en sélectionner 
une afin d'implémenter un système de fenêtre graphique.
Implémenter un système de déplacement afin de pouvoir controler son vaiseau. Le vaiseau de l'utilisateur pourra être de capable de tirer sur ses ennemies et prendre des dégats, cela implique que l'utilisateur aura accès à son nombre de points de vie.
Implémenter un système de niveau, dans lequel se trouvera un certain nombre d'entités (vaiseaux ennemis, boss)
L'utilisateur pourra savoir à quel niveau, il se trouve actuellement, ainsi que le nombre d'adversaires restants.

- Intermédiaire : 
Pouvoir accéder au nombre de vie restantes du boss du niveau.
Ajouter la possibilité de recupérer des bonus permettant d'altérer
le vaiseau de l'utilisateur.

- Supplémentaires : 
Un utilisateur pourrait être capable de configurer son propre niveau.
Rendre les adversaires assez complexe.
Les boss seront dotés de plusieurs armes.


## Testabilité
- Tester la configuration des niveaux
- Tester le bon déroulement du niveau, si les différentes vagues d'ennemis s'enchainent bien et le niveau se termine si le boss est battu.
- Tester les mouvements de notre vaisseau
- Tester l'enregistrement de balles sur les vaisseaux adverse et le notre (diminution de la vie)

## Originalité
On utilise un language basé sur un paradigme de programmation
qui n'est pas généralement utiliser pour le developpement de jeu vidéo.

## Collage API
On utilise aucune API, uniquement Ocaml

## Calendrier/ Jalons

- Implémentation des différents entités et du système de niveau : Novembre - Décembre
- Etude des bibliothèque graphique d'OCaml : Décembre
- Mise en place de la partie graphique : Janvier - Fevrier
- Lier la partie graphique avec le backend : Fevrier - Mars
- Ajouter des niveaux jouables : Fevrier - Mars
- Implémenter le système de configuration de niveau : Mars - Avril
- Effectuer les tests et rédiger la documentation : Avril

