import os
import time
from pprint import pprint

from tqdm import tqdm

from combinatorics import (
    count_valid_combinations, generate_combinations,
    get_S108_and_S12_grouped_by_complements_and_circular_permutations)
from dna_utils import (get_circular_permutations, get_complement,
                       is_circular_permutation)
from general_utils import delete_empty_and_not_in_use_output_files
from graph_utils import graph_is_acyclic
from logging_utils import get_formatted_datetime, log_message, log_summary


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

    for n in range(1, max_length + 1):
        if full_logging:
            log_message(log_file_name, f"taille: {n}\n", flush=True)

        start_time = time.time()
        total_combinations = count_valid_combinations(S108_grouped, S12_grouped, n)
        for S108_grouped_i, S12_grouped_i in tqdm(generate_combinations(S108_grouped, S12_grouped, n), total=total_combinations, desc=f"taille={n}"):
            if graph_is_acyclic([el for tup in S108_grouped_i for el in tup]+[el for el in S12_grouped_i]):
                counts[n-1] += 1
                if full_logging:
                    log_message(log_file_name, str([el for tup in S108_grouped_i for el in tup]+[el for el in S12_grouped_i])+'\n')
        end_time = time.time()
        log_message(log_file_name, f"Nombre total de codes de taille {n}: {count_valid_combinations(S108_grouped, S12_grouped, n)}\n")
        print(f"Nombre total de codes de taille {n}: {count_valid_combinations(S108_grouped, S12_grouped, n)}")
        log_message(log_file_name, f"Nombre total de codes de taile <={n}: {sum(count_valid_combinations(S108_grouped, S12_grouped, i) for i in range(1, n+1))}\n")
        print(f"Nombre total de codes de taile <={n}: {sum(count_valid_combinations(S108_grouped, S12_grouped, i) for i in range(1, n+1))}")
        log_summary(log_file_name, n, counts[n-1], start_time, end_time, full_logging)


def main():
    delete_empty_and_not_in_use_output_files()
    nb_circular_autocomplementary_code()


if __name__ == "__main__":
    main()
