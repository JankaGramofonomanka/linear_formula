import unittest
import linear_formula as lf
from linear_formula import LinearFormula

class TestLinearFormula(unittest.TestCase):

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


    #-TEST-MAGIC-FUNCTION-OVERLOADS-------------------------------------------
    
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
        
        for info in test_data:
            formula = LinearFormula(info[0], info[1])
            self.assertEqual(str(formula), info[2])
    
    def test_eq(self):

        test_data = [
            #init multipliers   init variables
            ([1, 3, -4],        ['a', 'b', 'c']),
            ([],                []             ),
        ]

        for info in test_data:
            formula_1 = LinearFormula(info[0], info[1])
            formula_2 = LinearFormula(info[0], info[1])
            self.assertEqual(formula_1 == formula_2, True)
        
        test_data = [
            # init multipliers  init variables
            (([1, 3, -4],       ['a', 'b', 'c'] ),      # formula 1
             ([2, 5, -7],       ['e', 'f', 'g'] )   ),  # formula 2

            (([1, 1],           ['a', 'b']      ),      # formula 1
             ([1, 1],           ['b', 'a']      )   ),  # formula 2
            
            (([1, 4, 2],        ['a', 'b', 'a'] ),      # formula 1
             ([3, 4],           ['b', 'a']      )   ),  # formula 2
            
            (([1, 2],           ['', '']        ),      # formula 1
             ([2, 1],           ['', '']        )   ),  # formula 2
        ]

        for info in test_data:
            formula_1 = LinearFormula(*info[0])
            formula_2 = LinearFormula(*info[1])
            self.assertFalse(formula_1 == formula_2)
    
    def test_neg(self):

        test_data = [
            #formula                -formula
            ('a + 3b - 4c',         '-a - 3b + 4c'      ),
            ('a + 3b - 4c + 3a',    '-a - 3b + 4c - 3a' ),
            ('a + 7b - 0c',         '-a - 7b - 0c'      ),
            ('a + 7b - 0c',         '-a - 7b + 0c'      ),
            ('-a + 4c + 3b - 4c',   'a - 4c - 3b + 4c'  ),
            ('0',                   '0'                 ),
            ('a',                   '-a'                ),
            ('6',                   '-6'                ),
            ('ab + 3cd - 34ef',     '-ab - 3cd + 34ef'  ),
        ]
    
        for info in test_data:
            formula_1 = LinearFormula(info[0])
            formula_2 = LinearFormula(info[1])
            self.assertEqual(-formula_1, formula_2)
        
        test_data = [
            #formula                not equal to -formula
            ('a + 3b - 4c',         'a + 3b - 4c'       ),
            ('a + 3b - 4c + 3a',    '-4a - 3b + 4c'     ),
            ('-a + 4c + 3b - 4c',   'a - 3b'            ),
            ('ab + 3cd - 34ef',     '7g - 3d + 14f'  ),
        ]
    
        for info in test_data:
            formula_1 = LinearFormula(info[0])
            formula_2 = LinearFormula(info[1])
            self.assertNotEqual(-formula_1, formula_2)
    
    def test_add_sub(self):

        # correct results
        test_data = [
            #formula_1              formula_1 + formula_2
            #           formula_2                   formula_1 - formula 2
            ('a + 3b',  '-4c',      'a + 3b - 4c',  'a + 3b + 4c'   ),
            ('a + b',   'c',        'a + b + c',    'a + b - c'     ),
            ('a + 7b',  '0',        'a + 7b + 0',   'a + 7b + 0'    ),
            ('a + 7b',  '0c',       'a + 7b + 0c',  'a + 7b + 0c'   ),
            ('a',       'b - 4c',   'a + b -4c',    'a - b + 4c'    ),
            ('0',       '3c',       '0 + 3c',       '0 - 3c'        ),
            ('a',       'a',        'a + a',        'a - a'         ),
            ('6',       '3',        '6 + 3',        '6 - 3'         ),
            ('6',       3,          '6 + 3',        '6 - 3'         ),
        ]

        for info in test_data:
            
            formula_2 = LinearFormula(info[1])
            sum = LinearFormula(info[2])
            difference = LinearFormula(info[3])
            
            # +, -
            formula_1 = LinearFormula(info[0])
            # LinearFormula +- LinearFormula
            self.assertEqual(formula_1 + formula_2, sum)
            self.assertEqual(formula_1 - formula_2, difference)
            # LinearFormula +- str (int)
            self.assertEqual(formula_1 + info[1], sum)
            self.assertEqual(formula_1 - info[1], difference)

            # += LinearFormula
            formula_1 = LinearFormula(info[0])
            formula_1 += formula_2
            self.assertEqual(formula_1, sum)

            # -= LinearFormula
            formula_1 = LinearFormula(info[0])
            formula_1 -= formula_2
            self.assertEqual(formula_1, difference)

            # += str (int)
            formula_1 = LinearFormula(info[0])
            formula_1 += info[1]
            self.assertEqual(formula_1, sum)

            # -= str (int)
            formula_1 = LinearFormula(info[0])
            formula_1 -= info[1]
            self.assertEqual(formula_1, difference)

        # wrong results
        test_data = [
            #formula_1              not formula_1 + formula_2
            #           formula_2                   not formula_1 - formula 2
            ('a + 7b',  '0',        'a + 7b',       'a + 7b'    ),
            ('a + 7b',  '0c',       'a + 7b + 0',   'a + 7b + 0'),
            ('a + 7b',  '0c',       'a + 7b',       'a + 7b'    ),
            ('a',       'b - 4c',   'a + b + 4c',   'a - b - 4c'),
            ('0',       '3c',       '3c',           '-3c'       ),
            ('a',       'a',        '2a',           '0a'        ),
            ('a',       'a',        'aa',           '0'         ),
            ('6',       '3',        '9',            '3'         ),
        ]

        for info in test_data:
            
            formula_2 = LinearFormula(info[1])
            sum = LinearFormula(info[2])
            difference = LinearFormula(info[3])
            
            # +, -
            formula_1 = LinearFormula(info[0])
            # LinearFormula +- LinearFormula
            self.assertNotEqual(formula_1 + formula_2, sum)
            self.assertNotEqual(formula_1 - formula_2, difference)
            # LinearFormula +- str
            self.assertNotEqual(formula_1 + info[1], sum)
            self.assertNotEqual(formula_1 - info[1], difference)

            # += LinearFormula
            formula_1 = LinearFormula(info[0])
            formula_1 += formula_2
            self.assertNotEqual(formula_1, sum)

            # -= LinearFormula
            formula_1 = LinearFormula(info[0])
            formula_1 -= formula_2
            self.assertNotEqual(formula_1, difference)

            # += str
            formula_1 = LinearFormula(info[0])
            formula_1 += info[1]
            self.assertNotEqual(formula_1, sum)

            # -= str
            formula_1 = LinearFormula(info[0])
            formula_1 -= info[1]
            self.assertNotEqual(formula_1, difference)
        
        # errors
        test_data = [
            #formula_1  formula_2
            ('a + 7b',  [1, 2]),
            #('a + 7b',  {'c': 3, 'd': 2}),
            ('a + 7b',  (1, 'c')),
        ]

        for info in test_data:            
            # +, -
            formula_1 = LinearFormula(info[0])
            self.assertRaises(TypeError, formula_1.__add__, info[1])
            self.assertRaises(TypeError, formula_1.__sub__, info[1])

            # +=
            formula_1 = LinearFormula(info[0])
            self.assertRaises(TypeError, formula_1.__iadd__, info[1])

            # -=
            formula_1 = LinearFormula(info[0])
            self.assertRaises(TypeError, formula_1.__isub__, info[1])
    
    def test_mul(self):

        # correct results
        test_data = [
            #formula_1          expected result
            #           multipliter
            ('a + 3b',  2,      '2a + 6b'   ),
            ('a + 3b',  '2',    '2a + 6b'   ),
            ('a + 3b',  1,      'a + 3b'    ),
            ('a + 3b',  0,      '0a + 0b'   ),
            ('a + 3b',  -2,     '-2a - 6b'  ),
            ('a',       3,      '3a'        ),
            ('0',       3,      '0'         ),
        ]

        for info in test_data:
            formula = LinearFormula(info[0])
            expected = LinearFormula(info[2])
            # *
            self.assertEqual(formula * info[1], expected)
            #self.assertEqual(info[1] * formula, expected)
            # *=
            formula *= info[1]
            self.assertEqual(formula, expected)
        
        # errors
        test_data = [
            #formula_1                              error
            #           multipliter
            ('a + 3b',  'c + 2d',                   ValueError  ),
            ('a + 3b',  LinearFormula('c + 2d'),    TypeError   ),
            ('a + 3b',  'c',                        ValueError  ),
            ('a + 3b',  '2c',                       ValueError  ),
            ('a + 3b',  LinearFormula('2'),         TypeError   ),
            ('a + 3b',  LinearFormula('2c'),        TypeError   ),
            ('a + 3b',  '-',                        ValueError  ),
        ]

        for info in test_data:
            formula = LinearFormula(info[0])
            error = info[2]
            # *
            self.assertRaises(error, formula.__mul__, info[1])
            #self.assertRaises(error, info[1] * formula)
            # *=
            self.assertRaises(error, formula.__imul__, info[1])
    
    def test_truediv(self):

        test_data = [
            #formula_1              expected result
            #               divider
            ('4a + 2b',     2,      '2a + b'    ),
            ('4a + 2b',     '2',    '2a + b'    ),
            ('4a + 2b',     1,      '4a + 2b'   ),
            ('6a + 9b',     3,      '2a + 3b'   ),
            ('6a + 9b',     -3,     '-2a - 3b'  ),
            ('0a + 0b',     3,      '0a - 0b'   ),
            ('0',           3,      '0'         ),
            ('6',           3,      '2'         ),
        ]

        for info in test_data:
            formula = LinearFormula(info[0])
            expected = LinearFormula(info[2])
            # /
            self.assertEqual(formula / info[1], expected)
            # /=
            formula /= info[1]
            self.assertEqual(formula, expected)

        # errors
        test_data = [
            #formula_1                              error
            #           multipliter
            ('a + 3b',  'c + 2d',                   ValueError  ),
            ('a + 3b',  LinearFormula('c + 2d'),    TypeError   ),
            ('a + 3b',  'c',                        ValueError  ),
            ('a + 3b',  '2c',                       ValueError  ),
            ('a + 3b',  LinearFormula('2'),         TypeError   ),
            ('a + 3b',  LinearFormula('2c'),        TypeError   ),
            ('a + 3b',  '-',                        ValueError  ),
        ]

        for info in test_data:
            formula = LinearFormula(info[0])
            error = info[2]
            # /
            self.assertRaises(error, formula.__truediv__, info[1])
            # /=
            self.assertRaises(error, formula.__itruediv__, info[1])
    
    def test_floordiv(self):
        
        test_data = [
            #formula_1              expected result
            #               divider
            ('5a + 3b',     2,      '2a + b'    ),
            ('5a + 3b',     '2',    '2a + b'    ),
            ('4a + 2b',     '2',    '2a + b'    ),
            ('4a + 2b',     1,      '4a + 2b'   ),
            ('6a + 9b',     3,      '2a + 3b'   ),
            ('6a + 9b',     2,      '3a + 4b'  ),
            ('0a + 0b',     3,      '0a - 0b'   ),
            ('0',           3,      '0'         ),
            ('7',           3,      '2'         ),
        ]

        for info in test_data:
            formula = LinearFormula(info[0])
            expected = LinearFormula(info[2])
            # //
            self.assertEqual(formula // info[1], expected)
            # //=
            formula //= info[1]
            self.assertEqual(formula, expected)

        # errors
        test_data = [
            #formula_1                              error
            #           multipliter
            ('a + 3b',  'c + 2d',                   ValueError  ),
            ('a + 3b',  LinearFormula('c + 2d'),    TypeError   ),
            ('a + 3b',  'c',                        ValueError  ),
            ('a + 3b',  '2c',                       ValueError  ),
            ('a + 3b',  LinearFormula('2'),         TypeError   ),
            ('a + 3b',  LinearFormula('2c'),        TypeError   ),
            ('a + 3b',  '-',                        ValueError  ),
        ]

        for info in test_data:
            formula = LinearFormula(info[0])
            error = info[2]
            # //
            self.assertRaises(error, formula.__truediv__, info[1])
            # //=
            self.assertRaises(error, formula.__itruediv__, info[1])
    
    def test_mod(self):

        test_data = [
            #initial formula        n       expected result
            ('a + 3b - 4c',         2,      'a + b'         ),
            ('a + 3b - 4c',         '2',    'a + b'         ),
            ('a + 3b - 4c + 3a',    3,      'a + 2c'        ),
            ('a + 7b - 0c - 4d',    3,      'a + b + 2d'    ),
            ('-a + 4c + 3b - 4c',   5,      '4a + 3b'       ),
            ('a',                   4,      'a'             ),
            ('6',                   4,      '2'             ),
            ('ab + 3cd - 34ef',     10,     'ab + 3cd + 6ef'),
        ]

        for info in test_data:
            formula = LinearFormula(info[0])
            expected = LinearFormula(info[2])
            # %
            self.assertEqual(formula % info[1], expected)
            # %=
            formula %= info[1]
            self.assertEqual(formula, expected)

        # errors
        test_data = [
            #formula_1                              error
            #           multipliter
            ('a + 3b',  'c + 2d',                   ValueError  ),
            ('a + 3b',  LinearFormula('c + 2d'),    TypeError   ),
            ('a + 3b',  'c',                        ValueError  ),
            ('a + 3b',  '2c',                       ValueError  ),
            ('a + 3b',  LinearFormula('2'),         TypeError   ),
            ('a + 3b',  LinearFormula('2c'),        TypeError   ),
            ('a + 3b',  '-',                        ValueError  ),
        ]

        for info in test_data:
            formula = LinearFormula(info[0])
            error = info[2]
            # %
            self.assertRaises(error, formula.__truediv__, info[1])
            # %=
            self.assertRaises(error, formula.__itruediv__, info[1])
        
    #-------------------------------------------------------------------------


    #-TEST-MODIFIERS----------------------------------------------------------
        
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

        for function, args in test_data:
            formula = LinearFormula('a + 3b - 4c + 3a')
            control_formula = LinearFormula('a + 3b - 4c + 3a')
            self.assertEqual(formula, control_formula)
            
            function(formula, *args)
            self.assertEqual(formula, control_formula)

            function(formula, *args, inplace=True)
            self.assertNotEqual(formula, control_formula)

    def test_add_segment(self):

        test_data = [
            #initial         multiplier  expected result
            #formula             variable
            ('a + 3b - 4c', (3,  'g'),   'a + 3b - 4c + 3g'  ),
            ('a + 3b - 4c', (-3, 'g'),   'a + 3b - 4c - 3g'  ),
            ('',            (3,  'g'),   '3g'                ),
            ('',            (-3, 'g'),   '-3g'               ),
        ]

        for info in test_data:
            formula = LinearFormula(info[0])
            formula.add_segment(*info[1], inplace=True)
            self.assertEqual(str(formula), info[2])

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

        for info in test_data:
            formula = LinearFormula(info[0])
            string = str(formula)
            formula.insert_segment(*info[1], inplace=True)
            self.assertEqual(str(formula), info[2])

    def test_remove_segment(self):

        test_data = [
            #initial formula            formula after removal
            #                   index
            ('a + 3b - 4c',     1,      'a - 4c'),
            ('a + 3b - 4c',     2,      'a + 3b'),
        ]

        for info in test_data:
            formula = LinearFormula(info[0])
            formula.remove_segment(info[1], inplace=True)
            self.assertEqual(str(formula), info[2])

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

        for info in test_data:
            formula = LinearFormula(info[0])
            
            formula_2 = formula.substitute(info[1], info[2])
            self.assertEqual(str(formula_2), info[3])

            substitute = LinearFormula(info[2])
            formula_2 = formula.substitute(info[1], substitute)
            self.assertEqual(str(formula_2), info[3])

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

        for info in test_data:
            formula = LinearFormula(info[0])
            formula.zip(inplace=True)
            self.assertEqual(str(formula), info[1])
    
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

        for info in test_data:
            formula = LinearFormula(info[0])
            formula.modulo(info[1], inplace=True)
            self.assertEqual(str(formula), info[2])

    #-------------------------------------------------------------------------


    #-TEST-OTHER--------------------------------------------------------------
    
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

        for info in test_data:
            formula = LinearFormula(info[0])
            self.assertEqual(formula.length(), info[1])
    
    def test_copy(self):
        formula = LinearFormula('a + b + 4c')
        copy_of_formula = formula.copy()
        copy_of_formula.add_segment(3, 'd', inplace=True)
        self.assertNotEqual(formula, copy_of_formula)

    def test_get_segment(self):

        test_data = [
            #initial formula            expected segment
            #                   index
            ('a + 3b - 4c',     1,      (3, 'b')    ),
            ('a + 3b - 4c',     2,      (-4, 'c')   ),
        ]

        for info in test_data:
            formula = LinearFormula(info[0])
            segment = formula.get_segment(info[1])
            self.assertEqual(segment, info[2])

    def test_evaluate(self):
        test_data = [
            #formula            values                      expected result
            ('1',               {'a': 5},                   1   ),
            ('a',               {'a': 5},                   5   ),
            ('a + b + c',       {'a': 1, 'b': 1, 'c': 1},   3   ),
            ('a + 3b - 4c',     {'a': 1, 'b': 1, 'c': 1},   0   ),
            ('a + 3b - 4c',     {'a': 2, 'b': 2, 'c': 3},   -4  ),
        ]

        for info in test_data:
            formula = LinearFormula(info[0])
            value = formula.evaluate(**info[1])
            self.assertEqual(value, info[2])

    #-------------------------------------------------------------------------


if __name__ == '__main__':
    unittest.main()