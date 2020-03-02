import unittest
import linear_formula as lf
from linear_formula import LinearFormula

class TestInit(unittest.TestCase):

    #-TEST-INITIALIZATION-----------------------------------------------------

    def test_init_with_string(self):

        test_data = [
            #init string            expected        expected
            #                       multipliers     variables
            ('a + 3b - 4c',         [1, 3, -4],     ['a', 'b', 'c']     ),
            ('a+3b-4c+3a',          [1, 3, -4, 3],  ['a', 'b', 'c', 'a']),
            (' a  +7b-  0c -4d ',   [1, 7, 0, -4],  ['a', 'b', 'c', 'd']),
            ('-a + 4c + 3b - 4c',   [-1, 4, 3, -4], ['a', 'c', 'b', 'c']),
            ('',                    [],             []                  ),
            ('a',                   [1],            ['a']               ),
            ('6',                   [6],            ['']                ),
            ('ab + 3cd - 34ef',     [1, 3, -34],    ['ab', 'cd', 'ef']  ),
        ]

        for info in test_data:
            formula = LinearFormula(info[0])
            self.assertEqual(formula.multipliers, info[1])
            self.assertEqual(formula.variables, info[2])

    def test_init_with_dict(self):

        test_data = [
            #init dict
            {'a': 1, 'b': 3, 'c': -4},
        ]

        for init_data in test_data:
            formula = LinearFormula(init_data)
            self.assertEqual(formula.multipliers, list(init_data.values()))
            self.assertEqual(formula.variables, list(init_data.keys()))

    def test_init_with_int(self):

        test_data = [3, '3', 0, 23, '23']

        for init_data in test_data:
            formula = LinearFormula(init_data)
            self.assertEqual(formula.multipliers, [int(init_data)])
            self.assertEqual(formula.variables, [''])

    def test_init_with_lists(self):

        test_data = [
            #init multipliers   init variables
            ([1, 3, -4],        ['a', 'b', 'c']     ),
            ([1, 3, -4, 3],     ['a', 'b', 'c', 'a']),
            ([1, 7, 0, -4],     ['a', 'b', 'c', 'd']),
            ([-1, 4, 3, -4],    ['a', 'c', 'b', 'c']),
            ([],                []                  ),
            ([1],               ['a']               ),
            ([6],               ['']                ),
            ([1, 3, -34],       ['ab', 'cd', 'ef']  ),
        ]

        for info in test_data:
            formula = LinearFormula(info[0], info[1])
            self.assertEqual(formula.multipliers, info[0])
            self.assertEqual(formula.variables, info[1])
    
    def test_init_wrong(self):

        test_data = [
            ([1, 3, -4],        ['a', 'b', 'c'],    3   ),
            ('a + 3b - 4c',     7                       ),
            ('a + 3b - 4c',     ['a', 'b', 'c']         ),
            (7,                 7                       ),
            ([-1, 4, 3, -4],    'a + b + c'             ),
        ]

        for args in test_data:
            self.assertRaises(TypeError, LinearFormula, *args)
    
    #-------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()