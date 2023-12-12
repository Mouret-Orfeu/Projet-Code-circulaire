# https://chat.openai.com/c/62971ffd-259d-4ad5-8f34-895914d77863
# Slow

import os
import time
from pprint import pprint
import igraph as ig

from tqdm import tqdm

from combinatorics import (
    count_valid_combinations, generate_combinations,
    get_S108_and_S12_grouped_by_complements_and_circular_permutations)
from dna_utils import (get_circular_permutations, get_complement,
                       is_circular_permutation)
from general_utils import delete_empty_and_not_in_use_output_files
from graph_utils2 import graph_is_acyclic
from graph_utils2 import add_code_to_graph
from graph_utils2 import del_code_from_graph
from logging_utils import get_formatted_datetime, log_message, log_summary

acyclic_check_count = [0]

def generate_grouped_subsets(S108: list[list[tuple[str, str]]], S12: list[list[str]], n: int, graph: list[str], igraph: ig.Graph, dict_node: dict, size: int, current_subset: list[tuple[str, str] | str]=[], start108=0, start12=0, selected_from_S12=False, acyclic_check_count=[0]):
    # Calculate the total number of tetranucleotides in the current_subset
    total_tetranucleotides = sum(2 if isinstance(item, tuple) else 1 for item in current_subset)

    # Check if the current combination has the desired total length
    if total_tetranucleotides == n:
        yield current_subset
        return
    elif total_tetranucleotides > n:
        print("ERROR: total_tetranucleotides > n")
        exit(1)

    # If we haven't selected from S12 yet, try adding a pair from S108
    if not selected_from_S12 and total_tetranucleotides <= n-2:
        for i in range(start108, len(S108)):
            for pair in S108[i]:
                new_tetras=[pair[0], pair[1]] # pair = new_tetra enfaite je crois, pas besoin de le redefinir, à voir
                igraph, dict_node, size = add_code_to_graph(igraph, new_tetras, size, dict_node)
                current_subset.append(pair)

                acyclic_check_count[0] += 1
                if igraph.is_dag():
                    yield from generate_grouped_subsets(S108, S12, n, graph, igraph, dict_node, size, current_subset, i + 1, start12, selected_from_S12, acyclic_check_count)

                current_subset.pop()
                igraph, dict_node, size = del_code_from_graph(igraph, new_tetras, size, dict_node)

    # Try adding a single string from S12
    for j in range(start12, len(S12)):
        for single in S12[j]:
            new_tetra=[single] # cette ligne est peut être inutile, on peut peut être utiliser single à la place de new_tetra
            igraph, dict_node, size = add_code_to_graph(igraph, new_tetra, size, dict_node)
            current_subset.append(single)

            acyclic_check_count[0] += 1
            if igraph.is_dag():
                yield from generate_grouped_subsets(S108, S12, n, graph, igraph, dict_node, size, current_subset, start108, j + 1, True, acyclic_check_count)

            current_subset.pop()
            igraph, dict_node, size = del_code_from_graph(igraph, new_tetra, size, dict_node)


# Cette fonction résoud le projet et écrit tout les codes circulaires autocomplémentaires dans output.txt
def nb_circular_autocomplementary_code(full_logging: bool=False, max_length: int=60) -> None:
    counts: list[int] = [0] * max_length

    S108_grouped, S12_grouped = get_S108_and_S12_grouped_by_complements_and_circular_permutations()

    # on va écrire dans output.txt tout les code de toutes les tailles trouvé
    file_name = os.path.basename(__file__)
    formatted_datetime = get_formatted_datetime()
    log_file_name = f"output-{file_name}-{formatted_datetime}.txt"
    print(f"Logging to {log_file_name}")
    log_message(log_file_name, f"Script: {os.path.basename(__file__)}\n\n", flush=True)

    # NEW
    igraph = ig.Graph(directed=True)
    dict_node = {}
    size = 0

    for n in range(1, max_length + 1):
        if full_logging:
            log_message(log_file_name, f"taille: {n}\n", flush=True)

        start_time = time.time()

        graph = []  # Initialize the graph as an empty list
        for subset in generate_grouped_subsets(S108_grouped, S12_grouped, n, graph, igraph, dict_node, size, acyclic_check_count=acyclic_check_count):
            counts[n-1] += 1
            if full_logging:
                log_message(log_file_name, str(subset) + '\n')
        end_time = time.time()
        log_message(log_file_name, f"Nombre total de codes de taille {n}: {count_valid_combinations(S108_grouped, S12_grouped, n)}\n")
        print(f"Nombre total de codes de taille {n}: {count_valid_combinations(S108_grouped, S12_grouped, n)}")
        log_message(log_file_name, f"Nombre total de codes de taile <={n}: {sum(count_valid_combinations(S108_grouped, S12_grouped, i) for i in range(1, n+1))}\n")
        print(f"Nombre total de codes de taile <={n}: {sum(count_valid_combinations(S108_grouped, S12_grouped, i) for i in range(1, n+1))}")
        log_message(log_file_name, f"Nombre d'appels à graph_is_acyclic (taille = {n}): {acyclic_check_count[0]}\n")
        print(f"Nombre d'appels à graph_is_acyclic (taille = {n}): {acyclic_check_count[0]}")
        log_summary(log_file_name, n, counts[n-1], start_time, end_time, full_logging)
        # Display the count of acyclic checks


def main():
    delete_empty_and_not_in_use_output_files()
    nb_circular_autocomplementary_code()


if __name__ == "__main__":
    main()
