import itertools
from itertools import permutations
from icecream import ic

# Create S_256 (list of all possible tetranucleotides)
nucleotides = ['A', 'C', 'G', 'T']
S_256 = {''.join(p) for p in itertools.product(nucleotides, repeat=4)}
ic(len(S_256))
with open("tetranucleotides_sets/S_256.txt", "w") as file:
    for tetra in S_256:
        file.write(tetra + '\n')

print("Tetranucleotides saved to S_256.txt")

# create S_16 (extract from S_256 the words that are repetitions of the same 2 letters)
S_16 = {nucl for nucl in S_256 if nucl[0:2] == nucl[2:4]}
ic(len(S_16))

#create S_240 (remove the words from S_16 to S_256)
S_240 = set(S_256) - set(S_16)
ic(len(S_240))

# get the complementary letter
def get_complementary_letter(l):
    return {'A':'T', 'T':'A', 'C':'G', 'G':'C'}[l]


#get complementary tetranucleotide
def get_complementary_tetra(s):
    return get_complementary_letter(s[3]) + get_complementary_letter(s[2]) + get_complementary_letter(s[1]) + get_complementary_letter(s[0])

"test if 2 word is auto complementary"
def is_auto_complementary(s):
    if s == get_complementary_tetra(s):
        return True
    else:
        return False


#create S_12 (extract from S_240 the words that are auto complementary)
S_12 = {nucl for nucl in S_240 if is_auto_complementary(nucl)}
ic(len(S_12))

#create S_228 (remove the words from S_12 to S_240)
S_228 = set(S_240) - set(S_12)
ic(len(S_228))

#create S_114 (the nucleotides from S_228 where for nucleotides its complementary is removed)
S_114 = set()

for nucl in S_228:
    if get_complementary_tetra(nucl) not in S_114:
        S_114.add(nucl)
ic(len(S_114))

#create S_126 (union of S_12 and S_114)
S_126 = S_12 | S_114
ic(len(S_126))