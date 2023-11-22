import itertools
# Note: we work only with bases and tetranucleotides

def complement_base(base):
    """Returns the complement of a base."""
    match base:
        case 'A':
            return 'T'
        case 'T':
            return 'A'
        case 'G':
            return 'C'
        case 'C':
            return 'G'
        case _:
            raise RuntimeError(f"Invalid base '{base}'.")

def get_complement(t):
    """Returns the complement of a tetranucleotide."""
    return ''.join(complement_base(base) for base in reversed(t))

def is_circular_permutation(t1, t2):
    """Returns True if t1 is a circular permutation of t2."""
    return t1 in (t2[i:] + t2[:i] for i in range(1, 4))

L1 = []
L2 = []
autocomplements = []
for t in itertools.product('ATGC', repeat=4):
    t = ''.join(t)
    if is_circular_permutation(t, t):
        print(f"Warning: {t} is a circular permutation of itself.")
        continue
    c = get_complement(t)
    if c == t:
        autocomplements.append(t)
    elif c not in L1 and not is_circular_permutation(t, c):
        L1.append(t)
        L2.append(c)

print(L1)
print(len(L1))
print(L2)
print(len(L2))
print(autocomplements)
print(len(autocomplements))

print(set(L1).intersection(set(L2)))

# https://chat.openai.com/c/90ea1110-2bb0-4e52-9046-ec517a0939de
def find_circular_permutations(groups, tetranucleotide):
    """Finds or creates a group for a tetranucleotide based on circular permutations."""
    for group in groups:
        if is_circular_permutation(group[0], tetranucleotide):
            group.append(tetranucleotide)
            return
    # If no group found, create a new group
    groups.append([tetranucleotide])

def group_circular_permutations(L):
    """Groups tetranucleotides into lists of circular permutations."""
    groups = []
    for tetranucleotide in L:
        find_circular_permutations(groups, tetranucleotide)
    return groups

list_of_lists_A = group_circular_permutations(L1)
print(list_of_lists_A)
print(len(list_of_lists_A))

list_of_lists_B = group_circular_permutations(L2)
print(list_of_lists_B)
print(len(list_of_lists_B))

print(all(all(get_complement(tetra)==comp for tetra, comp in zip(sublist_A, sublist_B)) for sublist_A, sublist_B in zip(list_of_lists_A, list_of_lists_B)))

list_of_lists_of_tuples = [[(tetra, comp) for tetra, comp in zip(sublist_A, sublist_B)] for sublist_A, sublist_B in zip(list_of_lists_A, list_of_lists_B)]
print(all(get_complement(tetra)==comp for list_of_tuples in list_of_lists_of_tuples for tetra, comp in list_of_tuples))

def generate_combinations_aux(list_of_lists, n):
    """
    Generates all combinations of size 'n' from a set of elements, E, where E
    consists of all elements present in the sublists of 'list_of_lists'. Each
    combination contains at most one unique element from each sublist.

    It recursively
    builds combinations by adding one element at a time from the different sublists
    without repeating a sublist in a single combination.

    Args:
    list_of_lists (list of list): A list where each element is a sublist, representing
                                  a distinct category or group of elements.
    n (int): The size of each combination to be generated.

    Yields:
    list: A generator yielding combinations of elements. Each combination is a list
          of elements, where each element is taken from a different sublist of
          'list_of_lists' and the total number of elements is 'n'.

    Example:
    >>> list(generate_combinations([[1, 2], [3, 4], [5, 6]], 2))
    [[1, 3], [1, 4], [1, 5], [1, 6], [2, 3], [2, 4], [2, 5], [2, 6], [3, 5], [3, 6], [4, 5], [4, 6]]
    """
    return itertools.chain.from_iterable(itertools.product(*subset) for subset in itertools.combinations(list_of_lists, n))
