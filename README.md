# Projet-Code

## Exécution simple avec exécutable

Cette méthode exécute le programme avec la version de Python intégrée à ce dossier (dans `python-3.12.1-embed-amd64`).


## Exécution avec la version installée de Python

- S'assurer d'avoir Python 3.11 ou supérieur installé
    ```bash
    python --version
    ```
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

Comme ils sont plutôt utiles pour le développement, nous n'avons pas paramétré le lancement avec la version Python intégrée. Si vous voulez lancer les tests, il faut vous assurer d'avoir Python 3.11 ou supérieur installé. Mais vous verrez juste qu'ils passent sans erreur, donc vous pouvez plutôt jeter un oeil à `test_dna_utils.py`, `test_graph_utils.py` et `test_combinatorics.py`.

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

## Remarques sur le programme

- Le programme utilise les informations suivantes :
  - Il y a 256 tétranucléotides
  - 16 d'entre eux ont un cycle de longueur 2 et ne peuvent donc pas être utilisés pour former un code circulaire (`AAAA,ACAC,AGAG,ATAT,CACA,CCCC,CGCG,CTCT,GAGA,GCGC,GGGG,GTGT,TATA,TCTC,TGTG,TTTT`)
  - 12 des 240 tétranucléotides restants sont autocomplémentaires (`AATT,ACGT,AGCT,CATG,CCGG,CTAG,GATC,GGCC,GTAC,TCGA,TGCA,TTAA`). On note S12 l'ensemble de ces tétranucléotides, et S228 les 228 autres tétranucléotides.
  - S'il y a un tétranucléotide dans un code autocomplémentaire, alors il doit aussi contenir son complémentaire
  - S'il y a un tétranucléotide dans un code circulaire, alors il ne peut pas contenir son complémentaire
  - 6 paires de tétranucléotides de S228 sont à la fois complémentaires et permutées (`(ATTA,TAAT), (ATGC,GCAT), (ATCG,CGAT), (TAGC,GCTA), (TACG,CGTA), (GCCG,CGGC)`), on peut donc les supprimer, ce qui nous donne S216.
  - S12 est stocké sous forme d'une liste de 2-listes de tétranucléotides permutés, ce qui permet de ne jamais empiler à la fois un tétranucléotide et son permuté.

    S12:
    ```
    [['AATT', 'TTAA'],
     ['AGCT', 'CTAG'],
     ['ACGT', 'GTAC'],
     ['TGCA', 'CATG'],
     ['TCGA', 'GATC'],
     ['GGCC', 'CCGG']]
    ```
    De la même manière, S216 est stocké sous forme d'une liste de 4-listes de paires de tétranucléotides complémentaires, de manière à ce que les premiers éléments des paires d'une 4-liste soient permutés l'un de l'autre, idem pour les deuxièmes éléments.

    S216:
    ```
    [[('AAAT', 'ATTT'), ('AATA', 'TATT'), ('ATAA', 'TTAT'), ('TAAA', 'TTTA')],
     [('AAAG', 'CTTT'), ('AAGA', 'TCTT'), ('AGAA', 'TTCT'), ('GAAA', 'TTTC')],
     [('AAAC', 'GTTT'), ('AACA', 'TGTT'), ('ACAA', 'TTGT'), ('CAAA', 'TTTG')],
     [('AATG', 'CATT'), ('GAAT', 'ATTC'), ('ATGA', 'TCAT'), ('TGAA', 'TTCA')],
     [('AATC', 'GATT'), ('CAAT', 'ATTG'), ('ATCA', 'TGAT'), ('TCAA', 'TTGA')],
     [('AAGT', 'ACTT'), ('AGTA', 'TACT'), ('TAAG', 'CTTA'), ('GTAA', 'TTAC')],
     [('AAGG', 'CCTT'), ('AGGA', 'TCCT'), ('GGAA', 'TTCC'), ('GAAG', 'CTTC')],
     [('AAGC', 'GCTT'), ('AGCA', 'TGCT'), ('GCAA', 'TTGC'), ('CAAG', 'CTTG')],
     [('AACT', 'AGTT'), ('ACTA', 'TAGT'), ('TAAC', 'GTTA'), ('CTAA', 'TTAG')],
     [('AACG', 'CGTT'), ('ACGA', 'TCGT'), ('CGAA', 'TTCG'), ('GAAC', 'GTTC')],
     [('AACC', 'GGTT'), ('ACCA', 'TGGT'), ('CCAA', 'TTGG'), ('CAAC', 'GTTG')],
     [('ATAG', 'CTAT'), ('AGAT', 'ATCT'), ('GATA', 'TATC'), ('TAGA', 'TCTA')],
     [('ATAC', 'GTAT'), ('ACAT', 'ATGT'), ('CATA', 'TATG'), ('TACA', 'TGTA')],
     [('ATGG', 'CCAT'), ('GGAT', 'ATCC'), ('TGGA', 'TCCA'), ('GATG', 'CATC')],
     [('AGAC', 'GTCT'), ('ACAG', 'CTGT'), ('GACA', 'TGTC'), ('CAGA', 'TCTG')],
     [('AGTG', 'CACT'), ('GAGT', 'ACTC'), ('TGAG', 'CTCA'), ('GTGA', 'TCAC')],
     [('AGTC', 'GACT'), ('CAGT', 'ACTG'), ('GTCA', 'TGAC'), ('TCAG', 'CTGA')],
     [('AGGT', 'ACCT'), ('TAGG', 'CCTA'), ('GGTA', 'TACC'), ('GTAG', 'CTAC')],
     [('AGGG', 'CCCT'), ('GGGA', 'TCCC'), ('GAGG', 'CCTC'), ('GGAG', 'CTCC')],
     [('AGGC', 'GCCT'), ('GGCA', 'TGCC'), ('GCAG', 'CTGC'), ('CAGG', 'CCTG')],
     [('AGCG', 'CGCT'), ('GCGA', 'TCGC'), ('GAGC', 'GCTC'), ('CGAG', 'CTCG')],
     [('AGCC', 'GGCT'), ('GCCA', 'TGGC'), ('CAGC', 'GCTG'), ('CCAG', 'CTGG')],
     [('ACGG', 'CCGT'), ('CGGA', 'TCCG'), ('GACG', 'CGTC'), ('GGAC', 'GTCC')],
     [('ACGC', 'GCGT'), ('CGCA', 'TGCG'), ('GCAC', 'GTGC'), ('CACG', 'CGTG')],
     [('ACCG', 'CGGT'), ('CCGA', 'TCGG'), ('GACC', 'GGTC'), ('CGAC', 'GTCG')],
     [('ACCC', 'GGGT'), ('CCCA', 'TGGG'), ('CCAC', 'GTGG'), ('CACC', 'GGTG')],
     [('GGGC', 'GCCC'), ('GGCG', 'CGCC'), ('GCGG', 'CCGC'), ('CGGG', 'CCCG')]]
    ```
- Le programme effectue un parcours d'arbre en profondeur en empilant/dépilant à chaque étape soit un tétranuclaotide autocomplémentaire, soit une paire de tétranucléotides complémentaires. Ce parcours est implémenté grâce à la fonction récursive `get_nb_circular_autocomplementary_codes`. À chaque étape, on teste l'absence de cycle avec `graph.is_dag()` qui est équivalente à la circularité (sachant que l'autocomplémentarité est déjà garantie par la manière dont nous générons les codes à tester). On ne peut pas obtenir de code circulaire en rajoutant un tétranucléotide à un code non circulaire, ce qui nous permet de faire du pruning dans le parcours d'arbre.
- Nous utilisons le typage, récemment ajouté à Python, pour améliorer les performances et la lisibilité du code.
- Nous avons effectués des tests unitaires, bien que non extensifs, pour vérifier le bon fonctionnement de notre programme.
- Nous avons implémenté le parallélisme avec un nombre fixe de 120 threads. Cela demande de copier le graphe à chaque passage, mais cela se traduit tout de même par un gain de performance. Cependant, nous sommes limités par le GIL (Global Interpreter Lock) du langage Python qui limite l'efficacité du multithreading de Python.
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
