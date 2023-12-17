import unittest

import combinatorics
import dna_utils


class TestCombinatorics(unittest.TestCase):
    def test_get_S108_and_S12_grouped_by_complements_and_circular_permutations(self):
        L, autocomplements = combinatorics.get_S108_and_S12_grouped_by_complements_and_circular_permutations()
        self.assertEqual(len(L), 27)
        for l in L:
            self.assertEqual(len(l), 4)
            for c in l:
                self.assertEqual(dna_utils.get_complement(c[0]), c[1])
        self.assertEqual(len(autocomplements), 6)
        for l in autocomplements:
            self.assertEqual(len(l), 2)
            for t in l:
                self.assertEqual(dna_utils.get_complement(t), t)
