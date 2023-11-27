# https://chat.openai.com/c/62971ffd-259d-4ad5-8f34-895914d77863
# Doesn't work!!!

import os
import time
from collections import deque

from tqdm import tqdm

from combinatorics import \
    get_S108_and_S12_grouped_by_complements_and_circular_permutations
from general_utils import delete_empty_and_not_in_use_output_files
from graph_utils import graph_is_acyclic
from logging_utils import get_formatted_datetime, log_message, log_summary


def bfs_generate_grouped_subsets_incremental(S108, S12, target_n, graph_is_acyclic, acyclic_check_count, queues):
    queue_n_1, queue_n_2 = queues.get(target_n-1, (deque([(graph := [], current_subset := [])]), deque()))

    for current_n in range(len(queues) + 1, target_n + 1):
        current_level_queue = deque()

        # Extend graphs from queue_n_1 with singles from S12
        for graph, current_subset in queue_n_1:
            for sublist in S12:
                for string in sublist:
                    if string not in graph:  # Check against the graph, not current_subset
                        new_graph = graph + [string]
                        new_subset = current_subset + [string]
                        acyclic_check_count[0] += 1
                        if graph_is_acyclic(new_graph):
                            current_level_queue.append((new_graph, new_subset))

        # Extend graphs from queue_n_2 with pairs from S108
        if current_n >= 2:
            for graph, current_subset in queue_n_2:
                for sublist in S108:
                    for pair in sublist:
                        if all(elem not in graph for elem in pair):  # Check each element of the pair against the graph
                            new_graph = graph + list(pair)
                            new_subset = current_subset + [pair]
                            acyclic_check_count[0] += 1
                            if graph_is_acyclic(new_graph):
                                current_level_queue.append((new_graph, new_subset))

        # Update queues for the next level
        queue_n_2, queue_n_1 = queue_n_1, current_level_queue
        queues[current_n] = (queue_n_2, queue_n_1)

    return [subset for _, subset in queue_n_1]

def nb_circular_autocomplementary_code(full_logging: bool=False, max_length: int=60) -> None:
    counts: list[int] = [0] * max_length
    acyclic_check_count = [0]
    queues = {}

    S108_grouped, S12_grouped = get_S108_and_S12_grouped_by_complements_and_circular_permutations()

    formatted_datetime = get_formatted_datetime()
    log_file_name = f"output-{formatted_datetime}.txt"
    print(f"Logging to {log_file_name}")
    log_message(log_file_name, f"Script: {os.path.basename(__file__)}\n\n", flush=True)

    for n in tqdm(range(1, max_length + 1), desc="Processing"):
        if full_logging:
            log_message(log_file_name, f"taille: {n}\n", flush=True)

        start_time = time.time()
        subsets = bfs_generate_grouped_subsets_incremental(S108_grouped, S12_grouped, n, graph_is_acyclic, acyclic_check_count, queues)
        counts[n-1] = len(subsets)

        for subset in subsets:
            if full_logging:
                log_message(log_file_name, str(subset) + '\n')

        end_time = time.time()
        log_summary(log_file_name, n, counts[n-1], start_time, end_time, full_logging)
        print(f"Nombre d'appels à graph_is_acyclic (taille = {n}): {acyclic_check_count[0]}")

def main():
    delete_empty_and_not_in_use_output_files()
    nb_circular_autocomplementary_code()

if __name__ == "__main__":
    main()
