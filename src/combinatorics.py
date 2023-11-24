import itertools
import math

from dna_utils import (get_circular_permutations, get_complement,
                       is_circular_permutation)
from graph_utils import graph_is_acyclic


def get_S108_and_S12_grouped_by_complements_and_circular_permutations():
    L = []
    autocomplements = []
    for t in itertools.product("ATGC", repeat=4):
        t = "".join(t)
        if is_circular_permutation(t, t, strict=True):
            # print(f"Warning: {t} is a circular permutation of itself.")
            continue
        c = get_complement(t)
        if c == t:
            for t2 in get_circular_permutations(t, strict=True):
                c2 = get_complement(t2)
                if c2 == t2:
                    if c2 not in (a for l in autocomplements for a in l):
                        autocomplements.append([t, t2])
                    break
        elif not is_circular_permutation(t, c):
            circular_permutation_group_exists = False
            for i, l in enumerate(L):
                if is_circular_permutation(t, l[0][0]):
                    circular_permutation_group_exists = True
                    if t not in (_t for l in L for c in l for _t in c):
                        L[i].append((t,c))
                    break
                if is_circular_permutation(t, l[0][1]):
                    circular_permutation_group_exists = True
                    if t not in (_t for l in L for c in l for _t in c):
                        L[i].append((c,t))
                    break
            if not circular_permutation_group_exists:
                L.append([(t,c)])

    return L, autocomplements


def generate_combinations(L, autocomplements, n):
    # n-2*i <= len_autocomplements
    # n-len_autocomplements <= 2*i
    # i >= (n-len_autocomplements)/2
    # i >= (n-len_autocomplements+1)//2
    len_L = len(L)
    len_autocomplements = len(autocomplements)
    # m = 0
    # M = n//2+1
    m = max(0, (n - len_autocomplements + 1) // 2)
    M = min(n // 2 + 1, len_L)
    return itertools.chain.from_iterable(
        itertools.product(
            itertools.product(*L_subset), itertools.product(*autocomplements_subset)
        )
        for i in range(m, M)
        for L_subset in itertools.combinations(L, i)
        for autocomplements_subset in itertools.combinations(autocomplements, n - 2 * i)
    )

def count_valid_combinations(L, autocomplements, n):
    len_L = len(L)
    len_autocomplements = len(autocomplements)
    m = max(0, (n - len_autocomplements + 1) // 2)
    M = min(n // 2 + 1, len_L)
    return sum(
        math.comb(len_L, i)
        * math.comb(len_autocomplements, n - 2 * i)
        * 4**i
        * 2 ** (n - 2 * i)
        for i in range(m, M)
    )
