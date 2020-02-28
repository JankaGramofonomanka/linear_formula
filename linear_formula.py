def type_of(char):
    try:
        int(char)
        return 'number'
    except ValueError:
        if char == ' ':
            return 'space'
        elif char in {'+', '-'}:
            return 'operator'
        else:
            return 'char'

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
            if type(arg) == str:
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
                    raise ValueError('invalid argument')


        elif len(args) == 2 and type(args[0]) == type(args[1]) == list:
            if len(args[0]) != len(args[1]):
                raise ValueError("""lists of multipliers and variables must 
                    have the same length""")
            else:
                self.multipliers = args[0].copy()
                self.variables = args[1].copy()

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

        elif type_of(char) == 'operator':
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

        if type_of(char) == 'number':
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
    
        if type_of(char) == 'char':
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


    #-OPERATOR-OVERLOADS------------------------------------------------------

    def __str__(self):

        text = ''
        for i in range(self.length()):
            
            if self.multipliers[i] >= 0:
                if i != 0:
                    text += ' + '
                if self.multipliers[i] != 1 or self.variables[i] == '':
                    text += str(self.multipliers[i])
            else:
                if i != 0:
                    text += ' - '
                else:
                    text += '-'
                if self.multipliers[i] != -1 or self.variables[i] == '':
                    text += str(-self.multipliers[i])

            text += self.variables[i]

        if text == '':
            text = '0'
        return text

    def __eq__(self, other):
        return (
            self.multipliers == other.multipliers 
            and self.variables == other.variables
        )

    #-------------------------------------------------------------------------


    #-MODIFICATION------------------------------------------------------------

    def add_segment(self, multiplier, variable, inplace=False):
        if inplace:
            self.multipliers.append(multiplier)
            self.variables.append(variable)
        else:
            copy_of_self = self.copy()
            copy_of_self.add_segment(multiplier, variable, inplace=True)
            return copy_of_self

    def insert_segment(self, multiplier, variable, index, inplace=False):
        if inplace:
            self.multipliers.insert(index, multiplier)
            self.variables.insert(index, variable)
        else:
            copy_of_self = self.copy()
            copy_of_self.insert_segment(
                multiplier, variable, index, inplace=True)
            return copy_of_self

    def remove_segment(self, index, inplace=False):
        if inplace:
            del self.multipliers[index]
            del self.variables[index]

        else:
            copy_of_self = self.copy()
            copy_of_self.remove_segment(index, inplace=True)
            return copy_of_self

    def substitute(self, variable, formula, inplace=False):
        """substitutes <variable> for <formula>"""
        # for example if <self> "==" 'a + b', 
        #             <variable> == 'a', 
        #             <formula> "==" 'x + 2' 
        # then the result should be 'x + 2 + b'

        if inplace:
            while True:
                try:
                    i = self.variables.index(variable)
                    multiplier = self.get_segment(i)[0]
                    self.remove_segment(i, inplace=True)

                    for j in range(formula.length()):
                        self.insert_segment(
                            multiplier*formula.multipliers[j],
                            formula.variables[j],
                            i + j,
                            inplace=True
                        )

                except ValueError:
                    break
        else:
            copy_of_self = self.copy()
            copy_of_self.substitute(variable, formula, inplace=True)
            return copy_of_self

    def zip(self, inplace=False):
        """Reduces the formula to the simplest form"""

        if inplace:
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
                        # if no more segmrnts with <variable> exist, add the 
                        # merged segments to the formula
                        if multiplier != 0:
                            self.insert_segment(
                                multiplier, variable, i, 
                                inplace=True
                                )
                        break
        else:
            copy_of_self = self.copy()
            copy_of_self.zip(inplace=True)
            return copy_of_self

    def modulo(self, n, inplace=False):
        
        if inplace:
            self.zip(inplace=True)
            for i in range(self.length()):
                self.multipliers[i] %= n
            self.zip(inplace=True)
        else:
            copy_of_self = self.copy()
            copy_of_self.modulo(n, inplace=True)
            return copy_of_self

    #-------------------------------------------------------------------------


    #-RETURN-STUFF------------------------------------------------------------

    def length(self):
        return len(self.multipliers)

    def print(self):
        print(self.__str__())

    def copy(self):
        copy_of_self = LinearFormula(self.__str__())
        return copy_of_self

    def get_segment(self, index):
        multiplier = self.multipliers[index]
        variable = self.variables[index]

        return (multiplier, variable)

    def evaluate(self, values_dict):
        result = 0
        values_dict[''] = 1
        try:
            for i in range(self.length()):
                result += self.multipliers[i]*values_dict[self.variables[i]]
        except KeyError:
            raise ValueError("Not all variables are provided")
        return result

    #-------------------------------------------------------------------------






if __name__ == '__main__':

    x = LinearFormula('a - 4')

    print(x.multipliers)




