"""
Tests for Symbol class.
"""
import unittest
from src.symbol import Symbol


class SymbolTest(unittest.TestCase):
    """
    Tests for Symbol class.
    """
    data = [
        [
            (1, 0, 'V_1', 'red'),
            (1, 90, 'V_2', 'blue'),
            (1, 180, 'V_3', 'green')
        ],
        [
            (1, 0, 'I_1', 'red'),
            (1, 90, 'I_2', 'blue'),
            (1, 180, 'I_3', 'green')
        ]
    ]

    def test_from_list(self):
        """
        Tests if Symbol.from_list() returns a list of symbols.
        :return: None
        """
        symbols = Symbol.from_list(self.data)
        self.assertEqual(len(symbols), 2)
        self.assertEqual(symbols[0], Symbol(self.data[0]))
        self.assertEqual(symbols[1], Symbol(self.data[1]))


if __name__ == '__main__':
    unittest.main()
