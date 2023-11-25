def complement_base(base: str) -> str:
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

def get_complement(t: str) -> str:
    """Returns the complement of a tetranucleotide."""
    return ''.join(complement_base(base) for base in reversed(t))

def is_circular_permutation(t1: str, t2: str, strict: bool=False) -> bool:
    """Returns True if t1 is a circular permutation of t2."""
    if strict:
        return t1 in (t2[i:] + t2[:i] for i in range(1, 4))
    else:
        return t1 in (t2[i:] + t2[:i] for i in range(4))

def get_circular_permutations(t: str, strict=False) -> list[str]:
    """Returns a list of all circular permutations of a tetranucleotide."""
    if strict:
        return [t[i:] + t[:i] for i in range(1, 4)]
    else:
        return [t[i:] + t[:i] for i in range(4)]
