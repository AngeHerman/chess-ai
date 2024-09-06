# chess-ai

## Description

Ce projet consiste à implémenter un jeu d'échecs ainsi que plusieurs intelligences artificielles (IA) basées sur différents algorithmes. L'objectif initial est d'implémenter le jeu d'échecs, puis de créer une IA qui utilise l'algorithme de Monte Carlo pour jouer. 

L'algorithme de Monte Carlo repose sur des simulations aléatoires et un calcul de récompense. La fonction de calcul de récompense sera améliorée au fil du temps pour rendre l'IA plus performante. Ensuite, nous avons implémenté deux autres IA basées sur les algorithmes suivants :
- **Alpha-Beta Pruning** : Un algorithme de recherche d'arbre de décision optimisé pour minimiser les coups possibles de l'adversaire.
- **Algorithme Génétique** : Un algorithme évolutif qui utilise la sélection, le croisement et la mutation pour améliorer les stratégies de jeu.

## Fonctionnalités

- Jouer conre une IA utilisant l'algorithme de Monte Carlo
- Jouer conre une IA basée sur l'algorithme Alpha-Beta
- Jouer conre une IA basée sur un Algorithme Génétique
- Lancer une des AI ci dessus contre celle de lichess 

## Prérequis

Pour exécuter ce projet, vous aurez besoin des éléments suivants :

- Python 3.x
- Bibliothèques Python :
  ```bash
  pip install requirements.txt
  ```
- Avoir un token de l'api de lichess.org
- Créer un ficher .env à la racine avec le token à l'intérier:
```bash
TOKEN=Votre_Token_Recu_De_Lichess
```

## Lancement
  ```bash
  make
  ```

## Licence

Ce projet est sous la [GNU General Public License v3.0 (GPL v3)](LICENSE). Pour plus de détails, veuillez consulter le fichier `LICENSE` dans ce répertoire.

## Auteurs
- **Ange Herman KOUE-HEMAZRO**
- **Eric NZABA**

