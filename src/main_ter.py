# Note: we work only with bases and tetranucleotides

import itertools
from pprint import pprint
import math


def complement_base(base):
    """Returns the complement of a base."""
    match base:
        case 'A':
            return 'T'
        case 'T':
            return 'A'
        case 'G':
            return 'C'
        case 'C':
            return 'G'
        case _:
            raise RuntimeError(f"Invalid base '{base}'.")

def get_complement(t):
    """Returns the complement of a tetranucleotide."""
    return ''.join(complement_base(base) for base in reversed(t))

def is_circular_permutation(t1, t2, strict=False):
    """Returns True if t1 is a circular permutation of t2."""
    if strict:
        return t1 in (t2[i:] + t2[:i] for i in range(1, 4))
    else:
        return t1 in (t2[i:] + t2[:i] for i in range(4))

def get_circular_permutations(t, strict=False):
    """Returns a list of all circular permutations of a tetranucleotide."""
    if strict:
        return [t[i:] + t[:i] for i in range(1, 4)]
    else:
        return [t[i:] + t[:i] for i in range(4)]

def get_S108_and_S12_grouped_by_complements_and_circular_permutations():
    L1 = []
    L2 = []
    autocomplements = []
    for t in itertools.product('ATGC', repeat=4):
        t = ''.join(t)
        if is_circular_permutation(t, t, strict=True):
            # print(f"Warning: {t} is a circular permutation of itself.")
            continue
        c = get_complement(t)
        if c == t:
            for t2 in get_circular_permutations(t, strict=True):
                c2 = get_complement(t2)
                if c2 == t2:
                    if c2 not in (a for l in autocomplements for a in l):
                        autocomplements.append([t, t2])
                    break
            # autocomplements.append(t)
        elif not is_circular_permutation(t, c):
            circular_permutation_group_exists = False
            for i, (l1, l2) in enumerate(zip(L1, L2)):
                if is_circular_permutation(t, l1[0]):
                    circular_permutation_group_exists = True
                    if t not in (_t for l in L1 for _t in l) and t not in (_t for l in L2 for _t in l):
                        L1[i].append(t)
                        L2[i].append(c)
                    break
                if is_circular_permutation(t, l2[0]):
                    circular_permutation_group_exists = True
                    if t not in (_t for l in L1 for _t in l) and t not in (_t for l in L2 for _t in l):
                        L1[i].append(c)
                        L2[i].append(t)
                    break
            if not circular_permutation_group_exists:
                L1.append([t])
                L2.append([c])
    # print(L1)
    # print(len(L1))
    # print(L2)
    # print(len(L2))
    L = [[(L1[i][j], L2[i][j]) for j in range(len(L1[i]))] for i in range(len(L1))]

    return L, autocomplements

L, autocomplements = get_S108_and_S12_grouped_by_complements_and_circular_permutations()

pprint(L)
print(len(L))
pprint(autocomplements)
print(len(autocomplements))


def generate_combinations(L, autocomplements, n):
    # n-2*i <= len_autocomplements
    # n-len_autocomplements <= 2*i
    # i >= (n-len_autocomplements)/2
    # i >= (n-len_autocomplements+1)//2
    len_L = len(L)
    len_autocomplements = len(autocomplements)
    # m = 0
    # M = n//2+1
    m = max(0, (n-len_autocomplements+1)//2)
    M = min(n//2+1, len_L)
    return itertools.chain.from_iterable(
        itertools.product(itertools.product(*L_subset), itertools.product(*autocomplements_subset))
        for i in range(m, M) for L_subset in itertools.combinations(L, i)
        for autocomplements_subset in itertools.combinations(autocomplements, n-2*i)
    )


def count_valid_combinations(L, autocomplements, n):
    return sum(1 for _ in generate_combinations(L, autocomplements, n))

def count_valid_combinations_bis(L, autocomplements, n):
    L_list_of_lens = [len(l) for l in L]
    autocomplements_list_of_lens = [len(l) for l in autocomplements]
    len_L = len(L)
    len_autocomplements = len(autocomplements)
    m = max(0, (n-len_autocomplements+1)//2)
    M = min(n//2+1, len_L)
    return sum(
        math.prod(L_subset)*math.prod(autocomplements_subset)
        for i in range(m, M) for L_subset in itertools.combinations(L_list_of_lens, i)
        for autocomplements_subset in itertools.combinations(autocomplements_list_of_lens, n-2*i))

def count_valid_combinations_ter(L, autocomplements, n):
    L_list_of_lens = [len(l) for l in L]
    autocomplements_list_of_lens = [len(l) for l in autocomplements]
    len_L = len(L)
    len_autocomplements = len(autocomplements)
    # print(len_L, len_autocomplements)
    m = max(0, (n-len_autocomplements+1)//2)
    M = min(n//2+1, len_L)
    return sum(math.comb(len_L, i)*math.comb(len_autocomplements, n-2*i)*4**i*2**(n-2*i) for i in range(m, M))

# for i in range(62):
#     print(i, count_valid_combinations_ter(L, autocomplements, i))

# L = [[('AAAT', 'ATTT'), ('AATA', 'TATT'), ('ATAA', 'TTAT'), ('TAAA', 'TTTA')],
#  [('AAAG', 'CTTT'), ('AAGA', 'TCTT'), ('AGAA', 'TTCT'), ('GAAA', 'TTTC')]]
# autocomplements = [['AATT', 'TTAA'],
#  ['AGCT', 'CTAG']]

# for c in generate_combinations(L, autocomplements, 7):
#     print(c)

# print(count_valid_combinations_ter(L, autocomplements, 5))
# print(count_valid_combinations_bis(L, autocomplements, 5))
# print(count_valid_combinations(L, autocomplements, 5))

# print(set(L1).intersection(set(L2)))

# # https://chat.openai.com/c/90ea1110-2bb0-4e52-9046-ec517a0939de
# def find_circular_permutations(groups, tetranucleotide):
#     """Finds or creates a group for a tetranucleotide based on circular permutations."""
#     for group in groups:
#         if is_circular_permutation(group[0], tetranucleotide):
#             group.append(tetranucleotide)
#             return
#     # If no group found, create a new group
#     groups.append([tetranucleotide])

# def group_circular_permutations(L):
#     """Groups tetranucleotides into lists of circular permutations."""
#     groups = []
#     for tetranucleotide in L:
#         find_circular_permutations(groups, tetranucleotide)
#     return groups

# list_of_lists_A = group_circular_permutations(L1)
# print(list_of_lists_A)
# print(len(list_of_lists_A))

# list_of_lists_B = group_circular_permutations(L2)
# print(list_of_lists_B)
# print(len(list_of_lists_B))

# print(all(all(get_complement(tetra)==comp for tetra, comp in zip(sublist_A, sublist_B)) for sublist_A, sublist_B in zip(list_of_lists_A, list_of_lists_B)))

# list_of_lists_of_tuples = [[(tetra, comp) for tetra, comp in zip(sublist_A, sublist_B)] for sublist_A, sublist_B in zip(list_of_lists_A, list_of_lists_B)]
# print(all(get_complement(tetra)==comp for list_of_tuples in list_of_lists_of_tuples for tetra, comp in list_of_tuples))

# def generate_combinations_aux(list_of_lists, n):
#     """
#     Generates all combinations of size 'n' from a set of elements, E, where E
#     consists of all elements present in the sublists of 'list_of_lists'. Each
#     combination contains at most one unique element from each sublist.

#     It recursively
#     builds combinations by adding one element at a time from the different sublists
#     without repeating a sublist in a single combination.

#     Args:
#     list_of_lists (list of list): A list where each element is a sublist, representing
#                                   a distinct category or group of elements.
#     n (int): The size of each combination to be generated.

#     Yields:
#     list: A generator yielding combinations of elements. Each combination is a list
#           of elements, where each element is taken from a different sublist of
#           'list_of_lists' and the total number of elements is 'n'.

#     Example:
#     >>> list(generate_combinations([[1, 2], [3, 4], [5, 6]], 2))
#     [[1, 3], [1, 4], [1, 5], [1, 6], [2, 3], [2, 4], [2, 5], [2, 6], [3, 5], [3, 6], [4, 5], [4, 6]]
#     """
#     return itertools.chain.from_iterable(itertools.product(*subset) for subset in itertools.combinations(list_of_lists, n))

####################################################################################################
# Fonction sur les graphes

import igraph as ig

# Cette fonction crée les arrêtes ( exemple (AA, AG), à partir d'un tetranucléotide
# Si on utilise cette fonction sur tout les tetranucléotides d'un code, il faudra verifier qu'aucune arrete n'est crée plusieurs fois
def get_nod_and_edge_tetra(tetra):
    nods = set()
    edges = set()
    for slice_idx in range(1,4):

        first_slice = tetra[0:slice_idx]
        second_slice = tetra[slice_idx:]

        nods.add(first_slice)
        if slice_idx == 2:
            #On évite de remettre un noeud qui est déjà dans le graphe (par ex pour "AAAA", on ne met pas 2 fois le noeud "AA" dans nods)
            if second_slice != first_slice:
                nods.add(second_slice)
        else:
            nods.add(second_slice)
        edges.add((first_slice, second_slice))
    return nods, edges


# créer le graph à partir des tetra d'un code
# OPTI:  à voir si l'union des set est opti à utiliser
def get_graph_from_code(code):
    nods = set()
    edges = set()
    for tetra in code:
        nods_tetra, edges_tetra = get_nod_and_edge_tetra(tetra)
        nods = nods | nods_tetra
        edges = edges | edges_tetra
    return nods, edges


def graph_is_acyclic(tetra_list):

    nods, edges = get_graph_from_code(tetra_list)

    # Step 1: Assign unique IDs to each node (on crée des dictionnaire qui lient )
    node_to_id = {node: idx for idx, node in enumerate(sorted(nods))}
    id_to_node = {idx: node for node, idx in node_to_id.items()}  # Optional, for later reference

    # Step 2: Convert edges to integer pairs
    edges_with_ids = [(node_to_id[edge[0]], node_to_id[edge[1]]) for edge in edges]

    # Step 3: Create the graph in igraph
    graph = ig.Graph(edges=edges_with_ids, directed=True)

    # Now you can work with the graph using igraph functions
    if graph.is_dag():
        return True
    else:
        return False




from datetime import datetime, timedelta
import time
from concurrent.futures import ProcessPoolExecutor
import concurrent.futures
from tqdm import tqdm

S108_grouped, S12_grouped = get_S108_and_S12_grouped_by_complements_and_circular_permutations()

def format_execution_time(execution_time):
    # Convert execution_time to a timedelta object
    execution_duration = timedelta(seconds=execution_time)

    # Format the duration into hours, minutes, seconds, and milliseconds
    formatted_duration = str(execution_duration).split('.')[0]  # This gives hh:mm:ss
    milliseconds = f"{execution_time:.3f}".split('.')[1]  # This gives milliseconds

    # Combine formatted_duration and milliseconds
    formatted_time = f"{formatted_duration}.{milliseconds}"
    return formatted_time

# On parcourt l'ensemble des codes de taille inferieur à N
N = 20

# Cette fonction résoud le projet et écrit tout les codes circulaires autocomplémentaires dans output.txt
def nb_circular_autocomplementary_code(N, S108_grouped, S12_grouped, full_logging=False):
    counts = [0] * N

    # on va écrire dans output.txt tout les code de toutes les tailles trouvé
    formatted_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    print(f"Logging to output-{formatted_datetime}.txt")
    with open(f"output-{formatted_datetime}.txt", "w", encoding="utf-8") as file:

        for n in range(1, N+1):
            if full_logging:
                file.write(f"taille: {n}\n")
            file.flush()

            start_time = time.time()
            total_combinations = count_valid_combinations_ter(S108_grouped, S12_grouped, n)
            for S108_grouped_i, S12_grouped_i in tqdm(generate_combinations(S108_grouped, S12_grouped, n), total=total_combinations, desc=f"taille={n}"):
                # print("ON ENTRE DANS LE FOR")
                # print(valid_combination_S_126)
                if graph_is_acyclic([el for tup in S108_grouped_i for el in tup]+[el for el in S12_grouped_i]):
                    counts[n-1] += 1
                    if full_logging:
                        file.write(str([el for tup in S108_grouped_i for el in tup]+[el for el in S12_grouped_i]))
                        file.write("\n")
            end_time = time.time()
            execution_time = end_time - start_time
            formatted_time = format_execution_time(execution_time)
            file.write(f"Nombre de codes de taille {n}: {counts[n-1]}\n")
            file.write(f"Temps d'exécution: {formatted_time}\n")
            file.write("\n")
            print(f"Nombre de codes de taille {n}: {counts[n-1]}")
            print(f"Temps d'exécution: {formatted_time}")
            print()

nb_circular_autocomplementary_code(N, S108_grouped, S12_grouped)
