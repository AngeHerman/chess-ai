# kouehemazro-nzaba-plong-2023

## Problèmes

Implémenter le jeu d'Echec ainsi qu'un IA sur l'algorithme de Monte Carlo.
Premièrement on implémentera, une version du jeu d'echec, ensuite
on implémentera une IA qui se base sur l'algorithme de Monte Carlo avec une fonction de calcul de récompense 
qu'on complétera au fil du temps.
L'algorithme étant basé sur le hasard, il est nécessaire pour nous de trouver des moyens pour rendre
notre IA intelligente.

## Objectifs

- Principaux : 
Mettre en place une implémentation du jeu d'Echec.
Analyser les facteurs rentrant en jeu pour la partie simulation de l'algorithme
de Monte Carlo
Implémenter l'algorithme de Monte Carlo.
Mettre en place la communication entre l'API Lichess et notre implémentation

- Intermédiaire : 
Identifier des stratégies permettant d'améliorer l'efficacité de l'IA

- Supplémentaires :  
Mettre en place la possibilité qu'un utilisateur d'affronter l'IA


## Testabilité
- Vérifier la fin du jeu.
- Tester l'algorithme en faisant jouer les IA les unes contre les autres.


## Originalité
Implémenter le jeu d'Echec ainsi qu'un IA se basant sur l'algorithme de Monte Carlo, basé sur le hasard

## Collage API
On utilise uniquement l'API de Lichess.org, comme convenu avec les professeurs, cela nous permet de ne pas
avoir à implémenter la partie graphique de notre implémentation du jeu d'échec.

## Calendrier/ Jalons

- Implémentation des différents entités du système : Novembre - Décembre
- Mise en place de la version textuel du jeu : Novembre - Fevrier
- Etudier les différents paramètres rentrant en compte dans les facteurs d'évalutation : Décembre - Janvier
- Implémenter l'algorithme d'élagage Alpha-Beta : Janvier - Avril
- Mise en place de la partie graphique : Janvier - Fevrier
- Lier la partie graphique avec le backend : Fevrier - Mars
- Finir les tâches non terminées : Mars - Avril
- Effectuer les tests et rédiger la documentation : Avril



## Les IA d'échecs trouvé
- Deep blue : première victoire d'un ordinateur contre un humain en mai 1997. Il a battu le champion du monde Garry Kasparov lors d’un match en six parties.
C'est l'algorithme bếte dont on avais parlé la dernière fois. IBM a créer un ordi special avec un super chip de 32 microprocesseur pour que l'IA puisse
parcourir a fond tout l'arbre de recherche et prendre les meilleures coups, ça a une complexité énorme et n'est pas du tout intélligent.
- Stockfish: Il fait une recherche des meilleurs coups dans le graphe mais avec de l'élagage alpha beta pour supprimer des noeuds fils inutiles à explorer.il a aussi une fonction
d'évaluation de sommets. Une mauvaise fonction d'évalutaion peut être la différence entre une IA qui cherche à perdre ou à gagner. La fonction d'evalution
repose sur la sécurité du roi, du controle du centre, de l'importance des pièces restantes et plein d'autres paramêtres, plus on a des paramêtres plus on a un meilleur algorythme.
- AlphaGo: utilise le deep learning, il apprend a chaque partie et a des millions de données. Il nécessite un moteur comme aws.
- Leela Chess Zero: Un meilleur stockfish qui prends quelques mois pour atteindre le niveau d'un grand maître. Il enregistre des tactiques souvent utilisé,
ainsi que des séquences de coups et les utilise dans ces parties. Il est aussi utlilisé aux dames et surtout au go.

Analysis and Comparison of Chess Algorithms :
Cette recherche analyse différents algorithmes au niveau de leur efficacité face à Stockfish.
Premièrement, les auteurs expliquent le fonctionnement des différents algorithmes analysés, Minmax Algorithm, Monte Carlo Algorithm ainsi que le Genetic Algorithm.
Les auteurs se basent sur le elo rating afin de pouvoir conclure quel algorithme est le plus adapté dans le jeu d'échec.
Suite à leur analyse, ils observent que après 7 game, l'algorithme MinMax devance, les deux autres algorithmes.
Ils concluent, en affirmant que l'algorithme Minmax est le plus adapté mais que ses variantes utilisant des optimisations tel que l'élagage peuvent fournir de meilleures résultats.
## Source
https://astrakhan.consulting/fr/blog/analyse-de-lintelligence-artificielle-aux-echecs/
https://les-echiquiers-du-roi.fr/blogs/blog-echecs/lintelligence-artificielle-et-les-echecs-une-revolution-pour-les-amateurs-et-les-professionnels
https://repository.ukim.mk/bitstream/20.500.12188/27381/1/CIIT2023_paper_5.pdf



## Pour 1 Décembre

L'algorithme de recherche arborescente Monte Carlo, est un algorithme de recherche d'arbre caractérisé par 4 étapes distinctes.

La sélection, l'expansion, la simulation
et la backpropagation.

La sélection est basé sur une stratégie pré-déterminé.
On traverse l'arbre puis on sélectionne un noeud avec la meilleur valeur, d'après la stratégie choisi.
Ce procédé est répété jusqu'à tombé sur une feuille.
Lorsqu'une feuille est sélectionné l'étape de l'expansion peut commencer.

Si la feuille selectionné ne représente pas un état final de la partie, on crée des enfants à la feuille sélectionné. Les enfants de l'état seront les états accessibles depuis celui-ci, lorsqu'on effectue un coup légal.

L'étape de simulation, depuis l'enfant, on effectue une partie au hasard jusqu'à atteindre un état final 
(Victoire, égalité, défaite), cette partie nous donne 
un score.

Dernièrement, l'étape de backpropagation qui utilise 
le résultat de la partie joué au hasard, et qui associe cette valeur à ce sommmet mais aussi aux sommets qui ont amené à cette état.

La stratégie, la plus commune est l'Upper Confidence Bound. Celle-ci se base sur l'exploration (explorer les noeuds pour lesquels peu de simuation ont été effectué) ainsi que l'exploitation (choix prometteur).
Chaque noeud a une valeur qui se base sur le nombre de visite du noeud lui-même ainsi que du noeud parent, et le score du noeud (Celui-ci est obtenu grâce à l'étape de backpropagation).

Pour les echecs l'algorithme de MTCS s'applique de la manière suivante : chaque noeud de l'arbre représente le plateau avec les pièces placé. 
On suivra donc les différentes étapes de l'algortihme, c'est à dire on selectionne un noeud, puis on l'étend, ce qui implique de choisir une action au hasard et de simuler une partie depuis ce noeud, jusqu'à ce que la fin soit atteinte (égalité ou victoire).
Suite à ses simulations chaque noeuds aura des scores attribués pour les deux joueurs et on selectionnera donc l'action la plus avantageuse. [1]

L'algorithme de Monte-Carlo est connue pour ne pas être un algorithme adapté pour les jeux tel que les echecs.[2]
Contrairement à l'algorithme Min-Max, l'article explique que l'algorithme a du mal à faire la différence entre des coups très mauvais et des coups bons.

On peut donc se demander comment les engines actuels utilisent l'algorithme MTCS, pour vaincre d'autres engines traditionnels utilisant l'alpha beta pruning.
(L'algorithme traditionellement utilisé pour les echecs est l'algorithme d'Alpha Beta Pruning, le document [3] décrit une implémentation de cette algorithme )

Les implémentations de l'algorithme de Monte-Carlo dans les échecs doivent donc utiliser des manières de contre palier les points faibles de celui-ci.

AlphaZero est un exemple concret d'utilisation de l'algorithme de Monte Carlo. Cette engine couple l'algorithme de Monte-Carlo avec du Deep Learning.
Dans le document "Mastering Chess and Shogi by Self-Play with a
General Reinforcement Learning Algorithm."
Les performances d'AlphaZero sont comparés aux engines Stockfish, et on observe qu'après un certains nombres de parties AlphaZero performe mieux. [4]

MTCS est aussi utilisé pour des variantes des echecs 
[5]





## Source

[1] https://www.diva-portal.org/smash/get/diva2:1656144/FULLTEXT01.pdf The Multiple Uses of Monte-Carlo Tree Search - Richard SENINGTON 

[2] https://ojs.aaai.org/index.php/ICAPS/article/view/13437/13286 - On Adversarial Search Spaces and Sampling-Based PlanningRaghuram RamanujanandAshish SabharwalandBart SelmanDepartment of Computer ScienceCornell University

[3] https://www.researchgate.net/publication/319390201_APPLYING_ALPHA-BETA_ALGORITHM_IN_A_CHESS_ENGINE 

[4] https://arxiv.org/pdf/1712.01815.pdf -
Mastering Chess and Shogi by Self-Play with a
General Reinforcement Learning Algorithm.

[5] https://www.researchgate.net/publication/363182984_Tree_Search_Algorithms_For_Chinese_Chess
Tree Search Algorithms For Chinese Chess
Siyu Heng
Nanjing Institute of Technology, Nanjing, China

https://www.researchgate.net/publication/23751563_Progressive_Strategies_for_Monte-Carlo_Tree_Search - Progressive Strategies for Monte-Carlo Tree Search Article  in  New Mathematics and Natural Computation ·

# Projet
## Installation des librairies
    pip install -r requirements.txt

## Vidéo explicative du projet
    [text](https://youtu.be/ML6Wx9bfmtQ)
## Lancement du projet
    make

## Explication des niveaux de notre IA
-   Niveau 0: Move hasardeux, surtout pour les tests
-   Niveau 1: Mobte Carlo  (Prends beaucoup trop de temps et coup pas optimal)
-   Niveau 2: Algorythme Genétique  (Prends beaucoup trop de temps et coup pas optimal)
-   Niveau 3: Alpha-Beta de profondeur 1  (1 seconde max)
-   Niveau 4: Alpha-Beta de profondeur 2  (5 secondes max)