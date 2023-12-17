import unittest

import combinatorics
import dna_utils


class TestCombinatorics(unittest.TestCase):
    def setUp(self) -> None:
        self.L, self.autocomplements = combinatorics.get_S108_and_S12_grouped_by_complements_and_circular_permutations()

    def test_get_S108_and_S12_grouped_by_complements_and_circular_permutations(self):
        self.assertEqual(len(self.L), 27)
        for l in self.L:
            self.assertEqual(len(l), 4)
            for c in l:
                self.assertEqual(dna_utils.get_complement(c[0]), c[1])
        self.assertEqual(len(self.autocomplements), 6)
        for l in self.autocomplements:
            self.assertEqual(len(l), 2)
            for t in l:
                self.assertEqual(dna_utils.get_complement(t), t)

    def test_generate_combinations_and_count_valid_combinations(self):
        for i in range(5):
            with self.subTest(i=i):
                self.assertEqual(
                    combinatorics.count_valid_combinations(self.L, self.autocomplements, i),
                    sum(1 for _ in combinatorics.generate_combinations(self.L, self.autocomplements, i))
                )