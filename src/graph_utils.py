import igraph as ig


# Cette fonction crée les arrêtes ( exemple (AA, AG), à partir d'un tetranucléotide
# Si on utilise cette fonction sur tout les tetranucléotides d'un code, il faudra verifier qu'aucune arrete n'est crée plusieurs fois
def get_vertices_and_edges_tetra(tetra):
    vertices = set()
    edges = set()
    for slice_idx in range(1,4):

        first_slice = tetra[0:slice_idx]
        second_slice = tetra[slice_idx:]

        vertices.add(first_slice)
        if slice_idx == 2:
            #On évite de remettre un noeud qui est déjà dans le graphe (par ex pour "AAAA", on ne met pas 2 fois le noeud "AA" dans nods)
            if second_slice != first_slice:
                vertices.add(second_slice)
        else:
            vertices.add(second_slice)
        edges.add((first_slice, second_slice))
    return vertices, edges

# créer le graph à partir des tetra d'un code
# OPTI:  à voir si l'union des set est opti à utiliser
def get_graph_from_code(code):
    vertices = set()
    edges = set()
    for tetra in code:
        vertices_tetra, edges_tetra = get_vertices_and_edges_tetra(tetra)
        vertices = vertices | vertices_tetra
        edges = edges | edges_tetra
    return vertices, edges

def graph_is_acyclic(tetra_list):
    vertices, edges = get_graph_from_code(tetra_list)

    # Step 1: Assign unique IDs to each node (on crée des dictionnaire qui lient )
    vertex_to_id = {vertex: idx for idx, vertex in enumerate(sorted(vertices))}
    id_to_vertex = {idx: vertex for vertex, idx in vertex_to_id.items()}  # Optional, for later reference

    # Step 2: Convert edges to integer pairs
    edges_with_ids = [(vertex_to_id[edge[0]], vertex_to_id[edge[1]]) for edge in edges]

    # Step 3: Create the graph in igraph
    graph = ig.Graph(edges=edges_with_ids, directed=True)

    # Now we can work with the graph using igraph functions
    return graph.is_dag()
