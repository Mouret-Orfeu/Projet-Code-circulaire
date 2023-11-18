import itertools
from itertools import permutations
from icecream import ic
import igraph as ig
import math
from itertools import combinations
from tqdm import tqdm
import time
from datetime import datetime, timedelta
# import multiprocessing
#from functools import lru_cache
# from concurrent.futures import ProcessPoolExecutor




len_tetra = 4

####################################################################################################
# création de S_126

# Create S_256 (list of all possible tetranucleotides)
nucleotides = ['A', 'C', 'G', 'T']
S_256 = {''.join(p) for p in itertools.product(nucleotides, repeat=4)}

# ic(len(S_256))

# create S_16 (extract from S_256 the words that are repetitions of the same 2 letters)
S_16 = {nucl for nucl in S_256 if nucl[0:2] == nucl[2:4]}

# ic(len(S_16))

#create S_240 (remove the words from S_16 to S_256)
S_240 = set(S_256) - set(S_16)

# ic(len(S_240))

# get the complementary letter
def get_complementary_letter(l):
    return {'A':'T', 'T':'A', 'C':'G', 'G':'C'}[l]


#get complementary tetranucleotide
def get_complementary_tetra(s):
    return get_complementary_letter(s[3]) + get_complementary_letter(s[2]) + get_complementary_letter(s[1]) + get_complementary_letter(s[0])

"test if 2 word is auto complementary"
def is_auto_complementary(s):
    return s == get_complementary_tetra(s)

def is_permutation(tetra1, tetra2):
    return tetra2 in [
        tetra1[1:4] + tetra1[0],
        tetra1[2:4] + tetra1[0:2],
        tetra1[3] + tetra1[0:3]
    ]

#create S_12 (extract from S_240 the words that are auto complementary)
S_12 = {nucl for nucl in S_240 if is_auto_complementary(nucl)}

# Convert the set to a list
S_12_list = list(S_12)

# ic(len(S_12))

#create S_228 (remove the words from S_12 to S_240)
S_228 = set(S_240) - set(S_12)

# ic(len(S_228))

#create S_114 (the nucleotides from S_228 where for nucleotides its complementary is removed)
S_114 = set()

# on trie le set pour que le résultat soit toujours le même quand on run le code
S_228_sorted = sorted(S_228)
for nucl in S_228_sorted:
    if get_complementary_tetra(nucl) not in S_114:
        S_114.add(nucl)


# Convert the set to a list
S_114_list = list(S_114)

# for nucl in S_228:
#     if get_complementary_tetra(nucl) not in S_114:
#         S_114.add(nucl)

# ic(len(S_114))

#create S_126 (union of S_12 and S_114) (enfaite S_126 c'est juste (en gros) un sous ensemble de S_256 où on a enlevé les tétra avec des cycles, et où on a enlevé les tétra qui sont les complémentaire d'autres)
S_126 = S_12 | S_114
# ic(len(S_126))

S_126_list = list(S_126)


#create and print all possible variations of S_6, i.e. all subsets of S_12 where we select at most 1 element from every pair of elements that are permutations of each other
S_12_list = list(S_12)
S_6_A = []
S_6_B = []
for i in range(12):
    for j in range(i+1, 12):
        if is_permutation(S_12_list[i], S_12_list[j]):
            S_6_A.append(S_12_list[i])
            S_6_B.append(S_12_list[j])
            break
# ic(len(S_6_A))
# ic(len(S_6_B))
valid_subsets_of_S12 = []
# do the cartesian product 6 times of {0,1,2}
# for each element, if 0 then nothing, if 1 then take it in S_6_A, if 2 then take it in S_6_B
for p in itertools.product([0,1,2], repeat=6):
    valid_subsets_of_S12.append([S_6_A[i] if p[i] == 1 else S_6_B[i] if p[i] == 2 else None for i in range(6)])
# ic(len(valid_subsets_of_S12))

####################################################################################################
# permutation groups creation

def remove_duplicate_sublists(list_of_sublists):
    """
    Removes duplicate sublists from a given list of sublists, where two sublists are
    considered duplicates if they have the same elements, regardless of order.

    The function maintains the original order of the first occurrence of each unique
    sublist in the input list. Each sublist in the input list is first sorted to
    determine uniqueness. If a sorted version of a sublist is not already present
    in the list of unique sublists, the original (unsorted) sublist is included in
    the result.

    Args:
    list_of_sublists (list of list): A list containing sublists. Each sublist can
                                     contain elements of any type that are comparable
                                     and sortable.

    Returns:
    list of list: A new list containing the unique sublists from the input list,
                  preserving the order of their first occurrence.

    Example:
    >>> remove_duplicate_sublists([[3, 2, 1], [1, 2, 3], [4, 5, 6]])
    [[3, 2, 1], [4, 5, 6]]
    """
    unique_sublists = []
    result = []

    for sublist in list_of_sublists:
        # Sort the sublist to ensure consistency in representation
        sorted_sublist = sorted(sublist)

        # Check if the sorted sublist is not already in the unique_sublists
        if sorted_sublist not in unique_sublists:
            unique_sublists.append(sorted_sublist)
            result.append(sublist)

    return result

# test
# A = [[1, 2, 3], [3, 2, 1], [4, 5], [5, 4], [6, 7]]
# print(remove_duplicate_sublists(A))


def permutation_group_list_creation(list_tetra):
    """
    Creates a list of permutation groups from a given list of tetranucleotides (tetra).
    Each permutation group is a list containing a tetranucleotide and all its permutations
    present in the input list. The function ensures that each unique permutation group
    appears only once in the result.

    The function first sorts the input list to ensure consistent processing. It then
    iterates over each tetranucleotide, creating a group of its permutations. Duplicate
    groups are removed, and the final list of permutation groups is sorted in descending
    order by their length.

    Args:
    list_tetra (list): A list of tetranucleotides, where each tetranucleotide is
                       represented as a string or a sequence-like object.

    Returns:
    list of list: A list of permutation groups. Each group is a list of tetranucleotides
                  that are permutations of each other. The groups are sorted by length
                  in descending order.

    Example:
    >>> permutation_group_list_creation(['ATGC', 'GCAT', 'TACG', 'AAAA'])
    [['ATGC', 'GCAT', 'TACG'], ['AAAA']]
    """

    # Sort list_tetra for consistent processing
    list_tetra = sorted(list_tetra)

    permutation_group_list = []

    # pour tout les tetra "permutation_group_tetra" dans list_tetra
    for permutation_group_tetra in list_tetra:

        # on crée une list
        permutation_group = []
        permutation_group.append(permutation_group_tetra)

        # et on regarde tout les tetra dans list_tetra en ajoutant à la list les permutation du tetra "permutation_group_tetra"
        for tetra in list_tetra:
            if is_permutation(permutation_group_tetra, tetra):
                permutation_group.append(tetra)
        permutation_group_list.append(permutation_group)

    # on enlève les doublons
    permutation_group_list = remove_duplicate_sublists(permutation_group_list)

    # sort the lists in permutation_group_list in length order
    permutation_group_list.sort(key=len, reverse=True)

    return permutation_group_list



permutation_group_list_S_114 = permutation_group_list_creation(S_114)

# print(permutation_group_list_S_114)


# Pour tester
def nb_of_elements_in_list_of_list(list_of_list):
    nb_of_elements = 0
    for list in list_of_list:
        nb_of_elements += len(list)
    return nb_of_elements

# ic(len(S_114))
# print("nb elements in permutation_group_list_S_114: ", nb_of_elements_in_list_of_list(permutation_group_list_S_114))

def check_if_all_elements_are_in_list_of_list(list_of_list, set_tetra):
    for tetra in set_tetra:
        is_in_list = False
        for list in list_of_list:
            if tetra in list:
                is_in_list = True
        if not is_in_list:
            return False
    return True

# if check_if_all_elements_are_in_list_of_list(permutation_group_list_S_114, S_114):
#     print("all elements are in permutation_group_list_S_114")


####################################################################################################
# Fonction sur les graphes

# Cette fonction crée les arrêtes ( exemple (AA, AG), à partir d'un tetranucléotide
# Si on utilise cette fonction sur tout les tetranucléotides d'un code, il faudra verifier qu'aucune arrete n'est crée plusieurs fois
def get_nod_and_edge_tetra(tetra):
    nods = set()
    edges = set()
    for slice_idx in range(1,len_tetra):

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




####################################################################################################

# test
# tetra_test = 'AAGT'
# nods, edges = get_nod_and_edge_tetra(tetra_test)
# print(nods, edges)

# tetra_test = 'TTGA'
# nods, edges = get_nod_and_edge_tetra(tetra_test)
# print(nods, edges)


# nods, edges = get_graph_from_code(["AAGT", "TTGA"])

# print(nods, edges)



####################################################################################################
# Test de présence de cycle

S_126_list = list(S_126)
S_126_list = sorted(S_126_list)


nods, edges = get_graph_from_code(["ATGA", "TGAA"])
#nods, edges = get_graph_from_code(S_126_list[0:5])

# Step 1: Assign unique IDs to each node (on crée des dictionnaire qui lient )
node_to_id = {node: idx for idx, node in enumerate(sorted(nods))}
id_to_node = {idx: node for node, idx in node_to_id.items()}  # Optional, for later reference

# Step 2: Convert edges to integer pairs
edges_with_ids = [(node_to_id[edge[0]], node_to_id[edge[1]]) for edge in edges]

# Step 3: Create the graph in igraph
graph = ig.Graph(edges=edges_with_ids, directed=True)

# Add node names as a vertex attribute (optional, but useful for interpretation)
graph.vs["name"] = [id_to_node[idx] for idx in range(len(nods))]

# Now you can work with the graph using igraph functions
if graph.is_dag():
    print("No cycle")








####################################################################################################

# permutation_group_list_S_114 est une liste de sous list, chaque sous liste est composé d'un tetra nucléotides présent dans S_114 et des permutations de ce tetra nucléotides prentes dans S_114
permutation_group_list_S_126 = permutation_group_list_creation(S_126_list)


# Soi E l'ensemble des éléments dand list_of_lists. C'est à dire l'ensemble des elements presents dans les sous lists de list_of_lists
# Cette fonction génère toutes les combinaisons de taille n de E, tel qu'il y ai au plus un unique élément de chaque sous list dans une combinaison
def generate_combinations(list_of_lists, n):
    """
    Generates all combinations of size 'n' from a set of elements, E, where E
    consists of all elements present in the sublists of 'list_of_lists'. Each
    combination contains at most one unique element from each sublist.

    It recursively
    builds combinations by adding one element at a time from the different sublists
    without repeating a sublist in a single combination.

    Args:
    list_of_lists (list of list): A list where each element is a sublist, representing
                                  a distinct category or group of elements.
    n (int): The size of each combination to be generated.

    Yields:
    list: A generator yielding combinations of elements. Each combination is a list
          of elements, where each element is taken from a different sublist of
          'list_of_lists' and the total number of elements is 'n'.

    Example:
    >>> list(generate_combinations([[1, 2], [3, 4], [5, 6]], 2))
    [[1, 3], [1, 4], [1, 5], [1, 6], [2, 3], [2, 4], [2, 5], [2, 6], [3, 5], [3, 6], [4, 5], [4, 6]]
    """
    return itertools.chain.from_iterable(itertools.product(*subset) for subset in combinations(list_of_lists, n))

def count_valid_combinations(list_of_lists, n):
    """
    Counts the number of valid combinations of size 'n' that can be formed from
    a given list of lists, where each combination includes at most one element
    from each sublist. This function uses the 'generate_combinations' function
    to create the combinations and then counts them.

    The function iterates over all possible combinations generated by
    'generate_combinations', incrementing a counter for each valid combination
    found. A combination is considered valid if it contains 'n' elements with
    no more than one element from each sublist.

    Args:
    list_of_lists (list of list): A list where each element is a sublist, representing
                                  a distinct category or group of elements.
    n (int): The size of each combination to be generated and counted.

    Returns:
    int: The total number of valid combinations of size 'n' that can be formed
         from the elements of 'list_of_lists', respecting the constraint of
         using at most one element from each sublist.

    Example:
    >>> count_valid_combinations([[1, 2], [3, 4], [5, 6]], 2)
    12
    """
    list_of_lens = [len(l) for l in list_of_lists]
    return sum(math.prod(subset) for subset in combinations(list_of_lens, n))


# start_time = time.time()
# result = count_valid_combinations(permutation_group_list_S_126, 5)
# end_time = time.time()
# execution_time = end_time - start_time

# print("Execution time:", execution_time, "seconds")
# print("Result:", result)







####################################################################################################
# Résolution du projet

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
def nb_circular_autocomplementary_code(N, full_logging=False):
    counts = [0] * N

    # on va écrire dans output.txt tout les code de toutes les tailles trouvé
    formatted_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    print(f"Logging to output-{formatted_datetime}.txt")
    with open(f"output-{formatted_datetime}.txt", "w", encoding="utf-8") as file:

        for n in tqdm(range(1, N+1), desc="Progress"):
            if full_logging:
                file.write(f"taille: {n}\n")
            file.flush()

            start_time = time.time()
            for valid_combination_S_126 in generate_combinations(permutation_group_list_S_126, n):
                # print("ON ENTRE DANS LE FOR")
                # print(valid_combination_S_126)
                if graph_is_acyclic(valid_combination_S_126):
                    counts[n-1] += 1
                    if full_logging:
                        file.write(str(valid_combination_S_126))
                        file.write("\n")
            end_time = time.time()
            execution_time = end_time - start_time
            formatted_time = format_execution_time(execution_time)
            file.write(f"Nombre de codes de taille {n}: {counts[n-1]}\n")
            file.write(f"Temps d'exécution: {formatted_time}\n")
            file.write("\n")

    return counts

print(nb_circular_autocomplementary_code(N))

# Code pour faire du multiprocessing
# https://chat.openai.com/c/68dbb4cd-bec6-46e6-9d17-ae136704b0ea

# def worker(input_queue, output_queue):
#     while True:
#         combination = input_queue.get()
#         if combination is None:  # Termination signal
#             break

#         if graph_is_acyclic(combination):
#             output_queue.put(combination)

# def nb_circular_autocomplementary_code_parallel(N, full_logging=False):
#     # permutation_group_list_S_126 = ...  # Define your permutation group list
#     input_queue = multiprocessing.Queue()
#     output_queue = multiprocessing.Queue()
#     workers = []

#     # Start worker processes
#     for _ in range(multiprocessing.cpu_count()):
#         p = multiprocessing.Process(target=worker, args=(input_queue, output_queue))
#         p.start()
#         workers.append(p)

#     counts = [0] * N

#     with open(f"output-{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt", "w", encoding="utf-8") as file:
#         for n in range(1, N+1):
#             if full_logging:
#                 file.write(f"taille: {n}\n")

#             start_time = time.time()

#             # Enqueue combinations for processing
#             for combination in generate_combinations(permutation_group_list_S_126, n):
#                 input_queue.put(combination)

#             # Retrieve and count acyclic combinations
#             while not input_queue.empty():
#                 acyclic_combination = output_queue.get()
#                 counts[n-1] += 1
#                 if full_logging:
#                     file.write(str(acyclic_combination))
#                     file.write("\n")

#             # Write additional data
#             end_time = time.time()
#             execution_time = end_time - start_time
#             formatted_time = format_execution_time(execution_time)
#             file.write(f"Nombre de codes de taille {n}: {counts[n-1]}\n")
#             file.write(f"Temps d'exécution: {formatted_time}\n")
#             print(f"Nombre de codes de taille {n}: {counts[n-1]}")
#             print(f"Temps d'exécution: {formatted_time}\n")

#             # Signal workers for the next batch
#             for _ in workers:
#                 input_queue.put(None)

#     # Clean up worker processes
#     for p in workers:
#         p.join()

#     return counts

# def main():
#     print(nb_circular_autocomplementary_code_parallel(N))

# if __name__ == '__main__':
#     # This is where you initialize multiprocessing
#     multiprocessing.freeze_support()
#     main()

####################################################################################################
# test construction des combinaison avec des for imbriqués


# permutation_group_list_S_126 est une liste de sous list, chaque sous liste est composé d'un tetra nucléotides présent dans S_114 et des permutations de ce tetra nucléotides prentes dans S_126
permutation_group_list_S_126 = permutation_group_list_creation(S_126_list)

####################################################################################################

# for longueur_de_code in range(1, 121):
#     for valid_subset_of_S12 in valid_subsets_of_S12:
#         for subset_of_S_114 in parties(S_114, taille=longueur_de_code):
#             code = valid_subset_of_S12 | subset_of_S_114
#             # ...



# for longueur_de_code in range(1, 121):
#     for longueur_S12_i in range (0,7):
#         for valid_subset_of_S12 in parties(S_12_i, taille=longueur_S12_i):
#             for subset_of_S_114 in parties(S_114, taille=longueur_de_code):
#                 code = valid_subset_of_S12 | subset_of_S_114
#                 ...
