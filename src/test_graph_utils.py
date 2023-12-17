import unittest
import itertools

import graph_utils

class TestStringToUniqueNumber(unittest.TestCase):
    def test_tetranucleotide_uniqueness(self):
        """Test that all tetranucleotides are assigned distinct numbers."""
        nucleotides = ['A', 'C', 'G', 'T']
        all_combinations = [''.join(combo) for combo in itertools.product(nucleotides, repeat=4)]
        assigned_numbers = set()
        for combo in all_combinations:
            number = graph_utils.string_to_unique_number(combo)
            self.assertNotIn(number, assigned_numbers)
            assigned_numbers.add(number)
