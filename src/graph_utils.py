from typing import Tuple
import igraph as ig
from itertools import product


# mapper tous les noeuds de graph possible sur des int
def char_to_num(char):
    """Map each character to a number."""
    mapping = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    return mapping[char]

def generate_all_strings(lengths, characters):
    """Generate all possible strings of given lengths and characters."""
    all_strings = []
    for length in lengths:
        for string_tuple in product(characters, repeat=length):
            all_strings.append(''.join(string_tuple))
    return all_strings

def string_to_unique_number(string):
    """Convert a string of {A, C, G, T} to a unique base 10 number, accounting for length."""
    base = 4
    number = 0
    max_length = 4
    for i, char in enumerate(reversed(string)):
        number += char_to_num(char) * (base ** i)
    # Adding a weight based on the length of the string
    number += base ** max_length * (len(string) - 1)
    return number

# Generate all possible strings
lengths = [1, 2, 3, 4]
characters = ['A', 'C', 'G', 'T']
all_possible_strings = generate_all_strings(lengths, characters)

# Map each string to a unique number
vertex_to_id = {s: string_to_unique_number(s) for s in all_possible_strings}
id_to_vertex = {string_to_unique_number(s): s for s in all_possible_strings}


# Cette fonction crée les arrêtes ( exemple (AA, AG), à partir d'un tetranucléotide (enfaite on convertit les noeuds comme AA, AAT etc en un identifiant entier)
# Si on utilise cette fonction sur tout les tetranucléotides d'un code, il faudra verifier qu'aucune arrete n'est crée plusieurs fois
def get_vertices_and_edges_tetra(tetra: str) -> tuple[set[int], set[tuple[int, int]]]:
    vertices: set[int] = set()
    edges: set[tuple[int, int]] = set()
    for slice_idx in range(1,4):

        first_slice = tetra[0:slice_idx]
        second_slice = tetra[slice_idx:]

        # Convert first slice to ID
        first_slice_id = vertex_to_id[first_slice]
        second_slice_id = vertex_to_id[second_slice]

        vertices.add(first_slice_id)

        if slice_idx == 2:
            #On évite de remettre un noeud qui est déjà dans le graphe (par ex pour "AAAA", on ne met pas 2 fois le noeud "AA" dans nods)
            if second_slice_id != first_slice_id:
                vertices.add(second_slice_id)
        else:
            vertices.add(second_slice_id)
        edges.add((first_slice_id, second_slice_id))

    return vertices, edges

def get_vertices_and_edges_from_code(code: list[str]) -> tuple[set[int], set[tuple[int, int]]]:
    vertices: set[int] = set()
    edges: set[tuple[int, int]] = set()
    for tetra in code:
        vertices_tetra, edges_tetra = get_vertices_and_edges_tetra(tetra)
        vertices = vertices | vertices_tetra
        edges = edges | edges_tetra

    return vertices, edges


# créer le graph à partir des tetra d'un code
# OPTI:  à voir si l'union des set est opti à utiliser
def get_graph_from_code(code: list[str]) -> ig.Graph:

    size = len(code)
    vertices, edges = get_vertices_and_edges_from_code(code)

    vertex_to_id = {vertex: idx for idx, vertex in enumerate(sorted(vertices))}
    # id_to_vertex = {idx: vertex for vertex, idx in vertex_to_id.items()}  # Optional, for later reference

    vertex_ids = [vertex_to_id[vertex] for vertex in vertices]
    edges_with_ids = [(vertex_to_id[edge[0]], vertex_to_id[edge[1]]) for edge in edges]

    # Create the graph with the specified vertices
    graph = ig.Graph(directed=True)

    for vertex_id in vertex_ids:
        if vertex_id not in graph.vs["name"]:
            graph.add_vertex(vertex_id)

    # Add edges to the graph
    graph.add_edges(edges_with_ids)

    return graph


def add_code_to_graph(graph: ig.Graph, code: list[str], size: int, dict_node: dict[int, int]) -> Tuple[ig.Graph, dict, int]:
    vertices, edges = get_vertices_and_edges_from_code(code)

    # Add new vertices to the graph
    for vertex in vertices:
        if vertex not in dict_node.keys():
            dict_node[vertex] = size
            graph.add_vertices(1)
            size += 1

    # Convert edges vertices to graph IDs of the vertices using dict_node
    edges_with_ids = {(dict_node[edge[0]], dict_node[edge[1]]) for edge in edges}

    # Add edges to the graph
    graph.add_edges(edges_with_ids)

    return graph, dict_node, size

def del_code_from_graph(graph: ig.Graph, code: list[str], size: int, dict_node: dict[int, int]) -> Tuple[ig.Graph, dict, int]:
    vertices, edges = get_vertices_and_edges_from_code(code)

    graph.delete_edges((dict_node[edge[0]], dict_node[edge[1]]) for edge in edges)

    vertex_to_delete = []
    for vertex in vertices:
        if graph.degree(dict_node[vertex]) == 0:
            vertex_to_delete.append(vertex)
    graph.delete_vertices(dict_node[vertex] for vertex in vertex_to_delete)

    for vertex in vertex_to_delete:
        del dict_node[vertex]
        size -= 1

    return graph, dict_node, size

def graph_is_acyclic(tetra_list: list[str]) -> bool:
    graph = get_graph_from_code(tetra_list)

    # Now we can work with the graph using igraph functions
    return graph.is_dag()
