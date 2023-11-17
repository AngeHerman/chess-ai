# kouehemazro-nzaba-plong-2023

## Problèmes

Implémenter le jeu d'Echec ainsi qu'un IA se basant sur l'IA d'echecs mondialement connu Stockfish.
Premièrement on implémentera, une version du jeu d'echec, ensuite
on implémentera une IA qui se base sur l'algorithme de d'élagage alpha beta avec une fonction d'évaluation qu'on complétera au fil du temps.
On évite d'utiliser un algorithme brute force pour l'implémentation
du joueur IA, afin d'éviter de parcourir des sommets inutiles ce qui augmente
la complexité de l'algorithme.
Avec l'algorithme d'élagage, on évite d'explorer des sommets inutiles, de ce
fait la complexité de celui-ci est meilleur.

## Objectifs

- Principaux : 
Mettre en place une version textuel du jeu d'Echec.
Analyser les facteurs rentrant en jeu pour la fonction d'évaluation
de sommets de l'arbre de recherche de meilleur coup afin d'ensuite
Implémenter l'algorithme d'élagage Alpha-Beta de notre IA.

- Intermédiaire : 
Implémenter des niveaux de difficultés pour l'IA, qui sera basé sur 
l'amélioration de la fonction d'évaluation
Ajouter une version graphique du jeu d'Echec

- Supplémentaires :  
Ameliorer l'IA en rajoutant d'autres facteurs dans la fonction d'évaluation
Implémenter l'annulation du dernier coup


## Testabilité
- Vérifier la fin du jeu.
- Tester l'amelioration des fonctions d'évaluation en faisant jouer les IA les unes contre les autres.
- Tester la liaison entre le backend et le plateau en frontend.


## Originalité
Implémenter le jeu d'Echec ainsi qu'un IA se basant sur l'IA d'echecs mondialement connu Stockfish

## Collage API
On utilise aucune API

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
C'est l'alogrythme bếte dont on avais parlé la dernière fois. IBM a créer un ordi special avec un super chip de 32 microprocesseur pour que l'IA puisse
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