import misc


class LinearFormula():


    #-INIT--------------------------------------------------------------------

    def __init__(self, *args):
        
        self.multipliers = []
        self.variables = []
        # for example if the formula is 'a + 4b - 3c' then we should get
        #         <self.multipliers> == [1,   4,   -3 ]
        #           <self.variables> == ['a', 'b', 'c']

        if len(args) == 1:
            arg = args[0]
            if type(arg) == type(self):
                self.multipliers = arg.multipliers.copy()
                self.variables = arg.variables.copy()
            
            elif type(arg) == str:
                self.read_from_string(arg)

            elif type(arg) == dict:
                for variable, multiplier in arg.items():
                    self.variables.append(variable)
                    self.multipliers.append(int(multiplier))
            else:
                try:
                    self.multipliers.append(int(arg))
                    self.variables.append('')
                except ValueError:
                    raise ValueError(f'invalid argument: {arg}')
                except TypeError:
                    raise TypeError(f'invalid argument: {arg}')
                


        elif len(args) == 2 and type(args[0]) == type(args[1]) == list:
            if len(args[0]) != len(args[1]):
                raise ValueError("""lists of multipliers and variables must 
                    have the same length""")
            else:
                self.multipliers = args[0].copy()
                self.variables = args[1].copy()
        
        elif len(args) == 2:
            raise TypeError('arguments have to be lists')

        else:
            raise TypeError('the constructor takes at most 2 arguments')

    #-------------------------------------------------------------------------


    #-STRING-TO-FORMULA-CONVERSION--------------------------------------------

    def read_from_string(self, string):
        """Converts a string into a formula"""
        # I assume that <string> is made of substrings like this:
        # operator, multiplier, variable, operator, multiplier, variable, ...
        # where some of the substrings can be empty
        
        # the algorithm in essence works like this:
        # 1. read operator
        # 2. read multilpier
        # 3. read variable
        # 4. add segment
        # 5. go back to point 1. if the string hasn't ended

        #set up temporary data
        self._setup_read_from_string()

        for char in string:
            self._process(char)

        # this will add the last segment
        self._process(' ')

        self._tear_down_read_from_string()

    def _setup_read_from_string(self):
        """Sets up memory for the <read_from_string> function"""
        self._current_operation = None
        self._current_multiplier = None
        self._current_variable = None
        self._phase = 'operation'

    def _tear_down_read_from_string(self):
        """Deletes memory used by the <read_from_string> function"""
        del self._current_operation
        del self._current_multiplier
        del self._current_variable
        del self._phase

    def _process(self, char):
        if self._phase == 'operation':
            self._process_operation(char)
        elif self._phase == 'multiplier':
            self._process_multiplier(char)
        elif self._phase == 'variable':
            self._process_variable(char)


    # the 3 methods below:
    # <_process_operation>, <_process_multiplier>, <_process_variable> 
    # work like this:
    # if <char> is "supported":
    #     do stuff
    # else:
    #     clean up
    #     go to the next phase 
    #     pass <char> to the next _process_whatever method

    def _process_operation(self, char):
            
        if char == ' ':
            # in the middle of a string a space does not tell us anything
            # also this prevents from going in circles when a space occurs 
            # after a variable name
            pass

        elif misc.type_of_char(char) == 'operator':
            if char == '+':
                self._current_operation = '+'
            elif char == '-':
                self._current_operation = '-'
            else:
                raise ValueError(f'invalid operation - {char}')

        else:
            # clean up
            if self._current_operation is None:
                self._current_operation = '+'
            
            # next phase
            self._phase = 'multiplier'
            self._process_multiplier(char)

    def _process_multiplier(self, char):

        if misc.type_of_char(char) == 'number':
            if self._current_multiplier is None:
                self._current_multiplier = int(char)
            else:
                self._current_multiplier *= 10
                self._current_multiplier += int(char)

        else:
            # clean up
            if self._current_multiplier is None:
                self._current_multiplier = 1

            if self._current_operation == '-':
                self._current_multiplier *= -1

            # next phase
            self._phase = 'variable'
            self._process_variable(char)

    def _process_variable(self, char):
    
        if misc.type_of_char(char) == 'char':
            if self._current_variable is None:
                self._current_variable = char
            else:
                self._current_variable += char

        else:
            # clean up
            if self._current_variable is None:
                self._current_variable = ''

            # add segment (part of clean up)
            self.multipliers.append(self._current_multiplier)
            self.variables.append(self._current_variable)

            # reset temporary data and go to the next phase
            self._setup_read_from_string()
            self._process_operation(char)

    #-------------------------------------------------------------------------


    #-MAGIC-METHOD-OVERLOADS--------------------------------------------------

    def __str__(self):

        text = ''
        for i in range(self.length()):
            
            if self.multipliers[i] >= 0:
                if i != 0:
                    # the '+' should be omitted at the beginning
                    text += ' + '

                if self.multipliers[i] != 1 or self.variables[i] == '':
                    # if the multiplier is 1 and there is a variable, there is
                    # no sense in writing the multiplier
                    text += str(self.multipliers[i])
            else:
                if i != 0:
                    text += ' - '

                else:
                    # at the beginning the '-' shouldn't have spaces around it
                    text += '-'
                if self.multipliers[i] != -1 or self.variables[i] == '':
                    # if the multiplier is -1 and there is a variable, there 
                    # is no sense in writing the multiplier

                    # the '-' was alredy written
                    text += str(-self.multipliers[i])

            # dont't forget the variable
            text += self.variables[i]

        # the string shouldn't be empty
        if text == '':
            text = '0'

        return text

    def __eq__(self, other):
        return (
            self.multipliers == other.multipliers 
            and self.variables == other.variables
        )

    def __neg__(self):
        result = self.copy()

        for i in range(result.length()):
            result.multipliers[i] *= -1
        
        return result
    
    @misc.convert_to_type('owners type', operator=True)
    def __iadd__(self, other):
        for i in range(other.length()):
            multiplier = other.multipliers[i]
            variable = other.variables[i]
            self.add_segment(multiplier, variable, inplace=True)
        
        return self
    
    @misc.convert_to_type('owners type', operator=True)
    def __isub__(self, other):
        self += -other
        return self
    
    @misc.convert_to_type(int, operator=True)
    def __imul__(self, other):
        for i in range(self.length()):
            self.multipliers[i] *= other
        
        return self

    @misc.convert_to_type(int, operator=True)    
    def __itruediv__(self, other):
        for i in range(self.length()):
            self.multipliers[i] /= other
        
        return self
    
    @misc.convert_to_type(int, operator=True)
    def __ifloordiv__(self, other):        
        self.zip()
        for i in range(self.length()):
            self.multipliers[i] //= other
        
        return self

    @misc.convert_to_type(int, operator=True)        
    def __imod__(self, other):
        self.modulo(other, inplace=True)
        return self
    
    @misc.assignment_to_binary('+=')
    def __add__(self, other):
        pass
    
    @misc.assignment_to_binary('-=')
    def __sub__(self, other):
        pass
    
    @misc.assignment_to_binary('*=')
    def __mul__(self, other):
        pass
    
    @misc.assignment_to_binary('/=')
    def __truediv__(self, other):
        pass
    
    @misc.assignment_to_binary('//=')
    def __floordiv__(self, other):
        pass
    
    @misc.assignment_to_binary('%=')
    def __mod__(self, other):
        pass

    def __rmul__(self, other):
        return self * other
    
    def __len__(self):
        return len(self.multipliers)
    
    def __getitem__(self, key):
        
        if type(key) == str:
            copy_of_self = self.copy()
            copy_of_self.zip(inplace=True)
            for i in range(len(copy_of_self)):
                if copy_of_self.variables[i] == key:
                    return copy_of_self.multipliers[i]
        
            raise KeyError(f'{key}')
        
        else:
            try:
                int(key)
            except ValueError:
                raise KeyError(f'{key}')
            except TypeError:
                raise KeyError(f'invalid key type: {type(key)}')
            
            if int(key) == key:
                return self.get_segment(key)
            else:
                raise KeyError(f'{key}')

    #-------------------------------------------------------------------------


    #-MODIFICATION------------------------------------------------------------

    @misc.inplace(default=False)
    def add_segment(self, multiplier, variable):
        self.multipliers.append(multiplier)
        self.variables.append(variable)

    @misc.inplace(default=False)
    def insert_segment(self, multiplier, variable, index):
        self.multipliers.insert(index, multiplier)
        self.variables.insert(index, variable)

    @misc.inplace(default=False)
    def remove_segment(self, index):
        del self.multipliers[index]
        del self.variables[index]

    @misc.inplace(default=False)
    def substitute(self, variable, formula):
        """substitutes <variable> for <formula>"""
        # for example if <self> "==" 'a + b', 
        #             <variable> == 'a', 
        #             <formula> "==" 'x + 2' 
        # then the result should be 'x + 2 + b'

        if type(formula) == str:
            formula = LinearFormula(formula)

        while True:
            try:
                # find the first segment with <variable> and put it aside
                i = self.variables.index(variable)
                multiplier = self.get_segment(i)[0]
                self.remove_segment(i, inplace=True)

                # insert each segment from <formula> multiplied by 
                # <multiplier> into <self>
                for j in range(formula.length()):
                    self.insert_segment(
                        multiplier*formula.multipliers[j],
                        formula.variables[j],
                        i + j,
                        inplace=True
                    )

            except ValueError:
                # break if no more segments with <variable> exist
                break

    @misc.inplace(default=False)
    def zip(self):
        """Reduces the formula to the simplest form"""

        for variable in set(self.variables):

            # find the first segment with <variable> and put it aside
            i = self.variables.index(variable)
            multiplier = self.get_segment(i)[0]
            self.remove_segment(i, inplace=True)

            while True:
                try:
                    # if more segments with <variable> exist, merge them 
                    # with the segment put aside
                    j = self.variables.index(variable)
                    multiplier += self.get_segment(j)[0]
                    self.remove_segment(j, inplace=True)

                except ValueError:
                    # if no more segments with <variable> exist, add the 
                    # merged segments to the formula
                    if multiplier != 0:
                        self.insert_segment(
                            multiplier, variable, i, 
                            inplace=True
                            )
                    break

    @misc.inplace(default=False)
    def modulo(self, n):
        
        self.zip(inplace=True)
        for i in range(self.length()):
            self.multipliers[i] %= n
        self.zip(inplace=True)
    
    #-------------------------------------------------------------------------


    #-OTHER-------------------------------------------------------------------

    def length(self):
        return len(self)

    def print(self):
        print(self.__str__())

    def copy(self):
        copy_of_self = LinearFormula(self.multipliers, self.variables)
        return copy_of_self

    def get_segment(self, index):
        multiplier = self.multipliers[index]
        variable = self.variables[index]

        return (multiplier, variable)

    def evaluate(self, **kwargs):
        result = 0

        # no variable is represented by a '' string
        kwargs[''] = 1
        try:
            for i in range(self.length()):
                result += self.multipliers[i]*kwargs[self.variables[i]]
        except KeyError:
            raise TypeError("Not all values are provided")

        return result

    #-------------------------------------------------------------------------






if __name__ == '__main__':



    formula = LinearFormula('a + 3b')

    print(formula.__truediv__('c + 2d'))




