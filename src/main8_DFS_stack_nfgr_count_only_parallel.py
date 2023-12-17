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

import concurrent.futures
import copy


def get_nb_circular_autocomplementary_codes_parallel(
        S108: list[list[tuple[str, str]]],
        S12: list[list[str]],
        n: int,
        igraph: ig.Graph,
        dict_node: dict,
        size: int,
        current_subset: list[tuple[str, str] | str]=[],
        start108: int=0,
        start12: int=0,
        selected_from_S12: bool=False
    ) -> int:
    total_tetranucleotides = sum(2 if isinstance(item, tuple) else 1 for item in current_subset)

    if total_tetranucleotides == n:
        return 1
    elif total_tetranucleotides > n:
        print("ERROR: total_tetranucleotides > n")
        exit(1)

    count = 0
    tasks = []

    # Parallel execution for the first level of recursion
    if not selected_from_S12 and total_tetranucleotides <= n-2:
        for i in range(start108, len(S108)):
            for pair in S108[i]:
                new_igraph, new_dict_node = copy.deepcopy(igraph), copy.deepcopy(dict_node)
                new_igraph, new_dict_node, new_size = add_code_to_graph(new_igraph, [pair[0], pair[1]], size, new_dict_node)
                new_subset = current_subset + [pair]

                if new_igraph.is_dag():
                    tasks.append((S108, S12, n, new_igraph, new_dict_node, new_size, new_subset, i + 1, start12, selected_from_S12))

    for j in range(start12, len(S12)):
        for single in S12[j]:
            new_igraph, new_dict_node = copy.deepcopy(igraph), copy.deepcopy(dict_node)
            new_igraph, new_dict_node, new_size = add_code_to_graph(new_igraph, [single], size, new_dict_node)
            new_subset = current_subset + [single]

            if new_igraph.is_dag():
                tasks.append((S108, S12, n, new_igraph, new_dict_node, new_size, new_subset, start108, j + 1, True))

    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Prepare a list of futures
        futures = {executor.submit(get_nb_circular_autocomplementary_codes, *task) for task in tasks}

        # Use tqdm to track the progress of futures as they complete
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
            count += future.result()

    return count

def get_nb_circular_autocomplementary_codes(
        S108: list[list[tuple[str, str]]],
        S12: list[list[str]],
        n: int,
        igraph: ig.Graph,
        dict_node: dict,
        size: int,
        current_subset: list[tuple[str, str] | str]=[],
        start108: int=0,
        start12: int=0,
        selected_from_S12: bool=False
    ) -> int:
    total_tetranucleotides = sum(2 if isinstance(item, tuple) else 1 for item in current_subset)

    if total_tetranucleotides == n:
        return 1
    elif total_tetranucleotides > n:
        print("ERROR: total_tetranucleotides > n")
        exit(1)

    count = 0

    # If we haven't selected from S12 yet, try adding a pair from S108
    if not selected_from_S12 and total_tetranucleotides <= n-2:
        for i in range(start108, len(S108)):
            for pair in S108[i]:
                new_igraph, new_dict_node = copy.deepcopy(igraph), copy.deepcopy(dict_node)
                new_igraph, new_dict_node, new_size = add_code_to_graph(new_igraph, [pair[0], pair[1]], size, new_dict_node)
                current_subset.append(pair)

                if new_igraph.is_dag():
                    count += get_nb_circular_autocomplementary_codes(S108, S12, n, new_igraph, new_dict_node, new_size, current_subset, i + 1, start12, selected_from_S12)

                current_subset.pop()

    # Try adding a single string from S12
    for j in range(start12, len(S12)):
        for single in S12[j]:
            new_igraph, new_dict_node = copy.deepcopy(igraph), copy.deepcopy(dict_node)
            new_igraph, new_dict_node, new_size = add_code_to_graph(new_igraph, [single], size, new_dict_node)
            current_subset.append(single)

            if new_igraph.is_dag():
                count += get_nb_circular_autocomplementary_codes(S108, S12, n, new_igraph, new_dict_node, new_size, current_subset, start108, j + 1, True)

            current_subset.pop()

    return count

# Cette fonction résoud le projet et écrit tout les codes circulaires autocomplémentaires dans output.txt
def nb_circular_autocomplementary_code(full_logging: bool=False, max_length: int=60) -> None:
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
        start_time = time.time()

        count =  get_nb_circular_autocomplementary_codes_parallel(S108_grouped, S12_grouped, n, igraph, dict_node, size)
        end_time = time.time()

        log_summary(log_file_name, n, count, start_time, end_time, full_logging)


def main():
    delete_empty_and_not_in_use_output_files()
    nb_circular_autocomplementary_code()


if __name__ == "__main__":
    main()
