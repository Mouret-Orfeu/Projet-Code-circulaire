import time
from pprint import pprint

from tqdm import tqdm

from combinatorics import (
    count_valid_combinations, generate_combinations,
    get_S108_and_S12_grouped_by_complements_and_circular_permutations)
from dna_utils import (get_circular_permutations, get_complement,
                       is_circular_permutation)
from general_utils import (delete_empty_and_not_in_use_output_files,
                           format_execution_time, get_formatted_datetime)
from graph_utils import graph_is_acyclic


# Cette fonction résoud le projet et écrit tout les codes circulaires autocomplémentaires dans output.txt
def nb_circular_autocomplementary_code(full_logging=False, max_length=60):
    counts = [0] * max_length

    S108_grouped, S12_grouped = get_S108_and_S12_grouped_by_complements_and_circular_permutations()

    # on va écrire dans output.txt tout les code de toutes les tailles trouvé
    formatted_datetime = get_formatted_datetime()
    print(f"Logging to output-{formatted_datetime}.txt")
    with open(f"output-{formatted_datetime}.txt", "w", encoding="utf-8") as file:
        for n in range(1, max_length + 1):
            if full_logging:
                file.write(f"taille: {n}\n")
            file.flush()

            start_time = time.time()
            total_combinations = count_valid_combinations(S108_grouped, S12_grouped, n)
            for S108_grouped_i, S12_grouped_i in tqdm(generate_combinations(S108_grouped, S12_grouped, n), total=total_combinations, desc=f"taille={n}"):
                if graph_is_acyclic([el for tup in S108_grouped_i for el in tup]+[el for el in S12_grouped_i]):
                    counts[n-1] += 1
                    if full_logging:
                        file.write(str([el for tup in S108_grouped_i for el in tup]+[el for el in S12_grouped_i]))
                        file.write("\n")
            end_time = time.time()
            execution_time = end_time - start_time
            formatted_time = format_execution_time(execution_time)
            file.write(f"Nombre de codes de taille {n}: {counts[n-1]}\n")
            file.write(f"Temps d'exécution: {formatted_time}\n")
            file.write("\n")
            print(f"Nombre de codes de taille {n}: {counts[n-1]}")
            print(f"Temps d'exécution: {formatted_time}")
            print()


def main():
    delete_empty_and_not_in_use_output_files()
    nb_circular_autocomplementary_code()


if __name__ == "__main__":
    main()
