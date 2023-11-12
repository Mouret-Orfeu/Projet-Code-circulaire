import itertools
from itertools import permutations
from icecream import ic
import igraph as ig

len_tetra = 4

####################################################################################################
# création de S_126

# Create S_256 (list of all possible tetranucleotides)
nucleotides = ['A', 'C', 'G', 'T']
S_256 = {''.join(p) for p in itertools.product(nucleotides, repeat=4)}

ic(len(S_256))

# create S_16 (extract from S_256 the words that are repetitions of the same 2 letters)
S_16 = {nucl for nucl in S_256 if nucl[0:2] == nucl[2:4]}

ic(len(S_16))

#create S_240 (remove the words from S_16 to S_256)
S_240 = set(S_256) - set(S_16)

ic(len(S_240))

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

ic(len(S_12))

#create S_228 (remove the words from S_12 to S_240)
S_228 = set(S_240) - set(S_12)

ic(len(S_228))

#create S_114 (the nucleotides from S_228 where for nucleotides its complementary is removed)
S_114 = set()
for nucl in S_228:
    if get_complementary_tetra(nucl) not in S_114:
        S_114.add(nucl)

ic(len(S_114))

#create S_126 (union of S_12 and S_114) (enfaite S_126 c'est juste (en gros) un sous ensemble de S_256 où on a enlevé les tétra avec des cycles, et où on a enlevé les tétra qui sont les complémentaire d'autres)
S_126 = S_12 | S_114
ic(len(S_126))



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
ic(len(S_6_A))
ic(len(S_6_B))
valid_subsets_of_S12 = []
# do the cartesian product 6 times of {0,1,2}
# for each element, if 0 then nothing, if 1 then take it in S_6_A, if 2 then take it in S_6_B
for p in itertools.product([0,1,2], repeat=6):
    valid_subsets_of_S12.append([S_6_A[i] if p[i] == 1 else S_6_B[i] if p[i] == 2 else None for i in range(6)])
ic(len(valid_subsets_of_S12))




####################################################################################################
# création de graphe à partir de sous esembles de S_126

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
    

####################################################################################################

#tests
 



####################################################################################################
# Test de présence de cycle

# S_126_list = list(S_126)
# S_126_list = sorted(S_126_list)

# nods, edges = get_graph_from_code(S_126_list[0:5])

# # Example for a directed graph
# # Create or load your graph
# dg = ig.Graph(edges, directed=True)

# # Check if the graph is a DAG (Directed Acyclic Graph)
# if dg.is_dag():
#     print("The directed graph is acyclic (no cycles).")
# else:
#     print("The directed graph has at least one cycle.")


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
                # ... 