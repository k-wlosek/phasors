import unittest


class MyTestCase(unittest.TestCase):
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
        from src.symbol import Symbol
        symbols = Symbol.from_list(self.data)
        self.assertEqual(len(symbols), 2)
        self.assertEqual(symbols[0], Symbol(self.data[0]))
        self.assertEqual(symbols[1], Symbol(self.data[1]))


if __name__ == '__main__':
    unittest.main()
