import unittest
import linear_formula as lf
from linear_formula import LinearFormula

class TestLinearFormula(unittest.TestCase):

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

        for i in range(len(test_data)):
            formula = LinearFormula(test_data[i][0])
            self.assertEqual(formula.multipliers, test_data[i][1])
            self.assertEqual(formula.variables, test_data[i][2])

    def test_init_with_dict(self):

        test_data = [
            #init dict
            {'a': 1, 'b': 3, 'c': -4},
        ]

        for i in range(len(test_data)):
            formula = LinearFormula(test_data[i])
            self.assertEqual(formula.multipliers, list(test_data[i].values()))
            self.assertEqual(formula.variables, list(test_data[i].keys()))

    def test_init_with_int(self):

        test_data = [3, '3', 0, 23, '23']

        for i in range(len(test_data)):
            formula = LinearFormula(test_data[i])
            self.assertEqual(formula.multipliers, [int(test_data[i])])
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

        for i in range(len(test_data)):
            formula = LinearFormula(test_data[i][0], test_data[i][1])
            self.assertEqual(formula.multipliers, test_data[i][0])
            self.assertEqual(formula.variables, test_data[i][1])
        
    def test_inplace(self):
        #formula = LinearFormula('a + 3b - 4c + 3a')
        #control_formula = LinearFormula('a + 3b - 4c + 3a')

        test_data = [
            (LinearFormula.add_segment,     [3, 'f']                        ),
            (LinearFormula.insert_segment,  [3, 'f', 2]                     ),
            (LinearFormula.remove_segment,  [3]                             ),
            (LinearFormula.substitute,      ['b', LinearFormula('x + 3')]   ),
            (LinearFormula.zip,             []                              ),
            (LinearFormula.modulo,          [2]                             ),
        ]

        for i in range(len(test_data)):
            formula = LinearFormula('a + 3b - 4c + 3a')
            control_formula = LinearFormula('a + 3b - 4c + 3a')
            self.assertEqual(formula, control_formula)
            
            function = test_data[i][0]
            args = test_data[i][1]
            function(formula, *args)
            self.assertEqual(formula, control_formula)

            function(formula, *args, inplace=True)
            self.assertNotEqual(formula, control_formula)

    def test_str(self):

        test_data = [
            #init multipliers   init variables          expected string
            ([1, 3, -4],        ['a', 'b', 'c'],        'a + 3b - 4c'       ),
            ([1, 3, -4, 3],     ['a', 'b', 'c', 'a'],   'a + 3b - 4c + 3a'  ),
            ([1, 7, 0, -4],     ['a', 'b', 'c', 'd'],   'a + 7b + 0c - 4d'  ),
            ([-1, 4, 3, -4],    ['a', 'c', 'b', 'c'],   '-a + 4c + 3b - 4c' ),
            ([],                [],                     '0'                 ),
            ([1],               ['a'],                  'a'                 ),
            ([6],               [''],                   '6'                 ),
            ([1, 3, -34],       ['ab', 'cd', 'ef'],     'ab + 3cd - 34ef'   ),
        ]
        
        for i in range(len(test_data)):
            formula = LinearFormula(test_data[i][0], test_data[i][1])
            self.assertEqual(str(formula), test_data[i][2])

    def test_add_segment(self):

        test_data = [
            #initial         multiplier  expected result
            #formula             variable
            ('a + 3b - 4c', (3,  'g'),   'a + 3b - 4c + 3g'  ),
            ('a + 3b - 4c', (-3, 'g'),   'a + 3b - 4c - 3g'  ),
            ('',            (3,  'g'),   '3g'                ),
            ('',            (-3, 'g'),   '-3g'               ),
        ]

        for i in range(len(test_data)):
            formula = LinearFormula(test_data[i][0])
            string = str(formula)
            formula.add_segment(*test_data[i][1], inplace=True)
            self.assertEqual(str(formula), test_data[i][2])

    def test_insert_segment(self):

        test_data = [
            #initial             multiplier      expected result
            #formula                 variable
            #                             index
            ('a + 3b - 4c',     (5,  'g', 1),   'a + 5g + 3b - 4c'  ),
            ('a + 3b - 4c',     (-5, 'g', 1),   'a - 5g + 3b - 4c'  ),
            ('a + 3b - 4c',     (5,  'g', 0),   '5g + a + 3b - 4c'  ),
            ('a + 3b - 4c',     (-5, 'g', 0),   '-5g + a + 3b - 4c' ),
            ('-a + 3b - 4c',    (5,  'g', 0),   '5g - a + 3b - 4c'  ),
            ('a + 3b - 4c',     (-5, 'g', 3),   'a + 3b - 4c - 5g'  ),
            ('',                (3,  'g', 0),   '3g'                ),
            #('',                (3,  'g', 1),   'err'               ),
        ]   

        for i in range(len(test_data)):
            formula = LinearFormula(test_data[i][0])
            string = str(formula)
            formula.insert_segment(*test_data[i][1], inplace=True)
            self.assertEqual(str(formula), test_data[i][2])

    def test_remove_segment(self):

        test_data = [
            #initial formula            formula after removal
            #                   index
            ('a + 3b - 4c',     1,      'a - 4c'),
            ('a + 3b - 4c',     2,      'a + 3b'),
        ]

        for i in range(len(test_data)):
            formula = LinearFormula(test_data[i][0])
            formula.remove_segment(test_data[i][1], inplace=True)
            self.assertEqual(str(formula), test_data[i][2])

    def test_get_segment(self):

        test_data = [
            #initial formula            expected segment
            #                   index
            ('a + 3b - 4c',     1,      (3, 'b')    ),
            ('a + 3b - 4c',     2,      (-4, 'c')   ),
        ]

        for i in range(len(test_data)):
            formula = LinearFormula(test_data[i][0])
            segment = formula.get_segment(test_data[i][1])
            self.assertEqual(segment, test_data[i][2])

    def test_length(self):

        test_data = [
            #formula               length
            ('a + 3b - 4c',             3),
            ('a + b - c',               3),
            ('1 + 2 - 3',               3),
            ('a + 3b - 4c + 3a',        4),
            ('a + 7b - 0c - 4d + 1',    5),
            ('-a + 4c',                 2),
            ('',                        0),
            ('a',                       1),
            ('6',                       1),
            ('ab + 3cd - 34ef',         3),
        ]

        for i in range(len(test_data)):
            formula = LinearFormula(test_data[i][0])
            self.assertEqual(formula.length(), test_data[i][1])

    def test_substitute(self):

        test_data = [
            #initial formula             substitute formula
            #               variable to           expected result
            #                substitute
            ('a + 3b - 4c',         'a', 'x + 2', 'x + 2 + 3b - 4c'         ),
            ('a + b - c',           'a', '2',     '2 + b - c'               ),
            ('1 + 2 - 3',           'a', 'x + 2', '1 + 2 - 3'               ),
            ('a + 3b - 4c + 3a',    'a', 'x + 2', 'x + 2 + 3b - 4c + 3x + 6'),
            ('a + 7b - 4d',         'b', 'x + 2', 'a + 7x + 14 - 4d'        ),
            ('-a + 4c',             'c', 'x + 2', '-a + 4x + 8'             ),
            ('',                    'a', 'x + 2', '0'                       ),
            ('a',                   'a', 'x + 2', 'x + 2'                   ),
            ('6a + 3b',             'c', 'x + 2', '6a + 3b'                 ),
            ('a + 3b - 4c',         'a', 'aaa',   'aaa + 3b - 4c'           ),
        ]

        for i in range(len(test_data)):
            formula = LinearFormula(test_data[i][0])
            substitute = LinearFormula(test_data[i][2])
            formula.substitute(test_data[i][1], substitute, inplace=True)
            self.assertEqual(str(formula), test_data[i][3])

    def test_zip(self):

        test_data = [
            #initial formula        zipped formula
            ('a + 3b - 4c',         'a + 3b - 4c'       ),
            ('a + 3b - 4c + 3a',    '4a + 3b - 4c'      ),
            ('a + 7b - 0c - 4d',    'a + 7b - 4d'       ),
            ('-a + 4c + 3b - 4c',   '-a + 3b'           ),
            ('',                    '0'                 ),
            ('a',                   'a'                 ),
            ('6',                   '6'                 ),
            ('ab + 3cd - 34ef',     'ab + 3cd - 34ef'   ),
        ]

        for i in range(len(test_data)):
            formula = LinearFormula(test_data[i][0])
            formula.zip(inplace=True)
            self.assertEqual(str(formula), test_data[i][1])

    def test_copy(self):
        formula = LinearFormula('a + b + 4c')
        copy_of_formula = formula.copy()
        copy_of_formula.add_segment(3, 'd', inplace=True)
        self.assertNotEqual(formula, copy_of_formula)

    def test_evaluate(self):
        test_data = [
            #formula            values                      expected result
            ('1',               {'a': 5},                   1   ),
            ('a',               {'a': 5},                   5   ),
            ('a + b + c',       {'a': 1, 'b': 1, 'c': 1},   3   ),
            ('a + 3b - 4c',     {'a': 1, 'b': 1, 'c': 1},   0   ),
            ('a + 3b - 4c',     {'a': 2, 'b': 2, 'c': 3},   -4  ),
        ]

        for i in range(len(test_data)):
            formula = LinearFormula(test_data[i][0])
            value = formula.evaluate(test_data[i][1])
            self.assertEqual(value, test_data[i][2])

    def test_modulo(self):

        test_data = [
            #initial formula        n   expected result
            ('a + 3b - 4c',         2,  'a + b'         ),
            ('a + 3b - 4c + 3a',    3,  'a + 2c'        ),
            ('a + 7b - 0c - 4d',    3,  'a + b + 2d'    ),
            ('-a + 4c + 3b - 4c',   5,  '4a + 3b'       ),
            ('a',                   4,  'a'             ),
            ('6',                   4,  '2'             ),
            ('ab + 3cd - 34ef',     10, 'ab + 3cd + 6ef'),
        ]

        for i in range(len(test_data)):
            formula = LinearFormula(test_data[i][0])
            formula.modulo(test_data[i][1], inplace=True)
            self.assertEqual(str(formula), test_data[i][2])



if __name__ == '__main__':
    unittest.main()