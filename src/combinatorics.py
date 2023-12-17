import itertools
import math

from dna_utils import get_circular_permutations, get_complement, is_circular_permutation


def get_S108_and_S12_grouped_by_complements_and_circular_permutations() -> tuple[list[list[tuple[str, str]]], list[list[str]]]:
    L: list[list[tuple[str, str]]] = []
    autocomplements: list[list[str]] = []
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
