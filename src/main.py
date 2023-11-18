import itertools
from itertools import permutations
from icecream import ic
import igraph as ig
import math
from itertools import combinations
from tqdm import tqdm
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

# OPTI: à voir si la structure set est la plus opti à utiliser

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
# Parcourir l'ensemble des codes de taille inferieur à N


N = 20 

# permutation_group_list_S_114 est une liste de sous list, chaque sous liste est composé d'un tetra nucléotides présent dans S_114 et des permutations de ce tetra nucléotides prentes dans S_114
permutation_group_list_S_126 = permutation_group_list_creation(S_126_list) 


# Soi E l'ensemble des éléments dand list_of_lists. C'est à dire l'ensemble des elements presents dans les sous lists de list_of_lists
# Cette fonction génère toutes les combinaisons de taille n de E, tel qu'il y ai au plus un unique élément de chaque sous list dans une combinaison
# J'ai un peu de mal à comprendre bien cette fonction, mais elle semble fonctionner
def generate_combinations(list_of_lists, n):
    def recurse(current, depth, last_used_index):
        if depth == n:
            yield current
            return
        for i in range(last_used_index + 1, len(list_of_lists)):
            if used[i]:
                continue
            for elem in list_of_lists[i]:
                used[i] = True
                yield from recurse(current + [elem], depth + 1, i)
                used[i] = False

    used = [False] * len(list_of_lists)
    return recurse([], 0, -1)


# def count_valid_combinations(list_of_lists, N):
#     count = [0] * N
#     for n in tqdm(range(1, N+1), desc="Progress"):
#         for valid_combination in generate_combinations(list_of_lists, n):
#             count[n-1] += 1
#     return count

def count_valid_combinations(list_of_lists, n):
    count = 0
    for valid_combination in generate_combinations(list_of_lists, n):
        count += 1
    return count

print(count_valid_combinations(permutation_group_list_S_126, 6))











####################################################################################################
# Résolution du projet

# Cette fonction résoud le projet et écrit tout les codes circulaires autocomplémentaires dans output.txt
def nb_circular_autocomplementary_code_detailed(N):
    count = [0] * N
    
    # on va écrire dans output.txt tout les code de toutes les tailles trouvé
    with open("output.txt", "w") as file:
        file.truncate(0)

        for n in range(1, N+1):
            file.write("\n" + "taille: " + str(n) + "\n\n")        
                
            for valid_combination_S_126 in generate_combinations(permutation_group_list_S_126, n):
                # print("ON ENTRE DANS LE FOR")
                # print(valid_combination_S_126)
                if graph_is_acyclic(valid_combination_S_126):
                    count[n-1] += 1
                    # print("ON ENTRE DANS LE IF")
                    file.write(str(valid_combination_S_126))
                    file.write("\n") 
                
    return count

# Cette fonction résoud le projet et n'écrit pas les codes circulaires autocomplémentaires dans output.txt
def nb_circular_autocomplementary_code(N):
    count = [0] * N

    for n in tqdm(range(1, N+1), desc="Progress"):    
            
        for valid_combination_S_126 in generate_combinations(permutation_group_list_S_126, n):
        
            if graph_is_acyclic(valid_combination_S_126):
                count[n-1] += 1
                 
    return count
    

# print(nb_circular_autocomplementary_code(N))

    


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