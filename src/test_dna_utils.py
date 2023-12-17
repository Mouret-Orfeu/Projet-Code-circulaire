import unittest

import dna_utils


class TestDNAUtils(unittest.TestCase):
    def test_complement_base(self):
        self.assertEqual(dna_utils.complement_base('A'), 'T')
        self.assertEqual(dna_utils.complement_base('T'), 'A')
        self.assertEqual(dna_utils.complement_base('G'), 'C')
        self.assertEqual(dna_utils.complement_base('C'), 'G')
        with self.assertRaises(RuntimeError):
            dna_utils.complement_base('X')

    def test_get_complement(self):
        self.assertEqual(dna_utils.get_complement('ATGC'), 'GCAT')
        self.assertEqual(dna_utils.get_complement('TACG'), 'CGTA')
        self.assertEqual(dna_utils.get_complement('CTAG'), 'CTAG')
        self.assertEqual(dna_utils.get_complement('GTAC'), 'GTAC')

    def test_is_circular_permutation(self):
        self.assertTrue(dna_utils.is_circular_permutation('ATGC', 'ATGC'))
        self.assertTrue(dna_utils.is_circular_permutation('TACG', 'ACGT'))
        self.assertTrue(dna_utils.is_circular_permutation('CTAG', 'AGCT'))
        self.assertTrue(dna_utils.is_circular_permutation('GTAC', 'CGTA'))
        self.assertFalse(dna_utils.is_circular_permutation('ATGC', 'ATGC', strict=True))
        self.assertTrue(dna_utils.is_circular_permutation('TACG', 'ACGT', strict=True))
        self.assertTrue(dna_utils.is_circular_permutation('CTAG', 'AGCT', strict=True))
        self.assertTrue(dna_utils.is_circular_permutation('GTAC', 'CGTA', strict=True))

    def test_get_circular_permutations(self):
        self.assertEqual(set(dna_utils.get_circular_permutations('ATGC')), {'ATGC', 'TGCA', 'GCAT', 'CATG'})
        self.assertEqual(set(dna_utils.get_circular_permutations('TACG')), {'TACG', 'ACGT', 'CGTA', 'GTAC'})
        self.assertEqual(set(dna_utils.get_circular_permutations('ATGC', strict=True)), {'TGCA', 'GCAT', 'CATG'})
        self.assertEqual(set(dna_utils.get_circular_permutations('TACG', strict=True)), {'ACGT', 'CGTA', 'GTAC'})
        self.assertEqual(len(dna_utils.get_circular_permutations('ATGC')), 4)
        self.assertEqual(len(dna_utils.get_circular_permutations('TACG')), 4)
        self.assertEqual(len(dna_utils.get_circular_permutations('ATGC', strict=True)), 3)
        self.assertEqual(len(dna_utils.get_circular_permutations('TACG', strict=True)), 3)
