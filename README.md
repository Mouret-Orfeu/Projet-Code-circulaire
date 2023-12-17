# Projet-Code

## Exécution

- Se placer à la racine du projet
- Installer les dépendances
    ```bash
    pip install -r requirements.txt
    ```
- Lancer le programme
    ```bash
    python src/main.py
    ```

## Tests

- Se placer à la racine du projet
- Installer les dépendances
    ```bash
    pip install -r requirements.txt
    ```
- Lancer les tests
    ```bash
    python -m unittest discover -s tests
    ```
    (Certains IDEs comme PyCharm et VS Code permettent de lancer les tests directement depuis l'IDE)
    ![Tests dans PyCharm](assets/Tests%20dans%20PyCharm.png)
    ![Tests dans VS Code](assets/Tests%20dans%20VS%20Code.png)

## Remarques sur le code

- Typage
- Tests unitaires (non extensifs)
- Parallélisme
- Nombre de lignes : ???? ainsi que ???? lignes de test.

## Résultats : Nombre de codes circulaires autocomplémentaires en fonction de la longueur

| Longueur | Nombre    | Durée d'exécution   |
|----------|-----------|---------------------|
|        1 |        12 |         0:00:00.001 |
|        2 |       168 |         0:00:00.013 |
|        3 |      1408 |         0:00:00.134 |
|        4 |     11728 |         0:00:01.191 |
|        5 |     76312 |         0:00:04.952 |
|        6 |    475168 |         0:00:35.267 |
|        7 |   2530868 |         0:03:03.709 |
|        8 |  12764634 |         0:16:10.927 |
|        9 |  57374400 |         2:33:00.306 |
|       10 | 243658816 |         5:55:55.479 |
|       11 | 942624972 | 1 day, 19:03:30.691 |

## Pistes d'amélioration

- **Adapter le code pour le faire tourner sur GPU**, ce qui est possible avec Python avec des librairies comme Numba.

  Cela reviendrait à paralléliser sur un très grand nombre de threads, ce qui peut améliorer grandement les performances, mais il est possible que nous soyons obligés d'abandonner les optimisations permises par le pruning dans le parcours d'arbre, car les GPUs ne sont pas bien adaptés à la récursivité ou au parcours d'arbre.

  Nous n'avons pas directement accès à un GPU donc cela nécessiterait de passer par un service cloud ou de voir avec la scolarité pour avoir accès à un GPU.
- **Traduire notre algorithme dans un langage comme Java ou C++** pour éviter le blocage du GIL (Global Interpreter Lock) de Python, qui limite l'efficacité du multithreading de Python.
