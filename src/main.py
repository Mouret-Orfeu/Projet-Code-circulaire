import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import time
from pprint import pprint
import igraph as ig

from tqdm import tqdm

from combinatorics import get_S108_and_S12_grouped_by_complements_and_circular_permutations
from general_utils import delete_empty_and_not_in_use_output_files
from graph_utils import add_code_to_graph
from logging_utils import get_formatted_datetime, log_message, log_summary

import concurrent.futures
import copy


def get_nb_circular_selfcomplementary_codes(
        S108: list[list[tuple[str, str]]],
        S12: list[list[str]],
        n: int,
        igraph: ig.Graph,
        dict_node: dict,
        size: int,
        current_subset: list[tuple[str, str] | str]=[],
        start108: int=0,
        start12: int=0,
        selected_from_S12: bool=False,
        parallel: bool=True
    ) -> int:

    total_tetranucleotides = sum(2 if isinstance(item, tuple) else 1 for item in current_subset)

    if total_tetranucleotides == n:
        return 1
    elif total_tetranucleotides > n:
        print("ERROR: total_tetranucleotides > n")
        exit(1)

    count = 0

    if parallel:
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
            futures = {executor.submit(get_nb_circular_selfcomplementary_codes, *task, parallel=False) for task in tasks}
            for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
                count += future.result()

    else:
        # Recursive logic
        if not selected_from_S12 and total_tetranucleotides <= n-2:
            for i in range(start108, len(S108)):
                for pair in S108[i]:
                    new_igraph, new_dict_node = copy.deepcopy(igraph), copy.deepcopy(dict_node)
                    new_igraph, new_dict_node, new_size = add_code_to_graph(new_igraph, [pair[0], pair[1]], size, new_dict_node)
                    current_subset.append(pair)

                    if new_igraph.is_dag():
                        count += get_nb_circular_selfcomplementary_codes(S108, S12, n, new_igraph, new_dict_node, new_size, current_subset, i+1, start12, selected_from_S12, parallel=False)

                    current_subset.pop()

        for j in range(start12, len(S12)):
            for single in S12[j]:
                new_igraph, new_dict_node = copy.deepcopy(igraph), copy.deepcopy(dict_node)
                new_igraph, new_dict_node, new_size = add_code_to_graph(new_igraph, [single], size, new_dict_node)
                current_subset.append(single)

                if new_igraph.is_dag():
                    count += get_nb_circular_selfcomplementary_codes(S108, S12, n, new_igraph, new_dict_node, new_size, current_subset, start108, j + 1, True, parallel=False)

                current_subset.pop()

    return count

# Cette fonction résout le projet et écrit tous les codes circulaires autocomplémentaires dans output.txt
def nb_circular_selfcomplementary_codes(max_length: int=60) -> None:
    S108_grouped, S12_grouped = get_S108_and_S12_grouped_by_complements_and_circular_permutations()

    print("Calculating the number of circular self-complementary codes by code length")
    print("A program from Maxime DROUHIN and Orfeú MOURET")
    print()

    # On va écrire dans output.txt tous les codes de toutes les tailles trouvé
    formatted_datetime = get_formatted_datetime()
    log_file_name = f"output-{formatted_datetime}.txt"
    print(f"Logging to {log_file_name}")

    igraph = ig.Graph(directed=True)
    dict_node = {}
    size = 0

    for n in range(1, max_length + 1):
        start_time = time.time()

        count = get_nb_circular_selfcomplementary_codes(S108_grouped, S12_grouped, n, igraph, dict_node, size)
        end_time = time.time()

        log_summary(log_file_name, n, count, start_time, end_time)


def main():
    delete_empty_and_not_in_use_output_files()
    nb_circular_selfcomplementary_codes()


if __name__ == "__main__":
    main()
