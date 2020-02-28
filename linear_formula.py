def type_of(char):
    try:
        int(char)
        return 'number'
    except ValueError:
        if char == ' ':
            return 'space'
        elif char in {'+', '-'}:
            return 'sign'
        else:
            return 'char'

class LinearFormula():

    def __init__(self, string):
        
        self.multipliers = []
        self.variables = []
        # for example if <string> == 'a + 4b - 3c' then we should get
        #      <self.multipliers> == [1,   4,   -3 ]
        #        <self.variables> == ['a', 'b', 'c']

        # temporary data
        self.current_multiplier = None;
        self.current_variable = ''
        self.sign = 1
        
        #### True if the algorithm has finished processing the current 
        #### multiplier / variable
        self.processed_mult = False
        self.processed_var = False

        #### the type of last substring type ('number' or 'char' or 'other')
        self.last_substr_type = 'other'

        #process
        for char in string.strip():
            self._check(char)
            if self._ready():
                # add the current multiplier and variable if the algorith has 
                # finished processing them
                self.add_segment(
                    self.current_multiplier, self.current_variable, 
                    inplace=True
                    )
                # reset the temporary data except <self.last_substr_type>
                self._reset()
            

            if type_of(char) == 'number':
                self._process_number(char)

            elif type_of(char) == 'char':
                self._process_character(char)

            elif type_of(char) == 'sign':
                self._process_sign(char)

            elif type_of(char) == 'space':
                self.last_substr_type = 'other'

        #add what remained
        self._check('end')
        self.add_segment(
            self.current_multiplier, self.current_variable, 
            inplace=True
            )
        self._reset()

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
            and self.variables == other.variables)

    def _process_number(self, char):
        if self.current_multiplier is None:
            self.current_multiplier = 0

        self.current_multiplier *= 10
        self.current_multiplier += int(char)
        self.last_substr_type = 'number'

    def _process_character(self, char):
        if self.current_multiplier is None:
            self.current_multiplier = 1

        self.current_variable += char
        self.last_substr_type = 'char'

    def _process_sign(self, char):
        if char == '-':
            self.sign = -1;
        elif char == '+':
            self.sign = 1
        self.last_substr_type = 'other'

    def _ready(self):
        return self.processed_mult and self.processed_var

    def _check(self, char):
        """Checks if temporary data should be modified"""
    
        if self.last_substr_type == 'number' and type_of(char) == 'char':
            self.processed_mult = True

        if char == 'end' or (self.last_substr_type != 'other' 
            and type_of(char) in {'space', 'sign'}):

            self.current_multiplier *= self.sign
            self.processed_var = True
            self.processed_mult = True

    def _reset(self):
        """resets all temporay data except <self.last_substr_type>"""

        self.sign = 1
        self.processed_mult = False
        self.processed_var = False
        self.current_multiplier = None
        self.current_variable = ''


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

    def get_and_remove_segment(self, index):
        multiplier = self.multipliers[index]
        variable = self.variables[index]

        del self.multipliers[index]
        del self.variables[index]

        return (multiplier, variable)


    def length(self):
        return len(self.multipliers)

    def print(self):
        print(self.__str__())


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
                    multiplier = self.get_and_remove_segment(i)[0]
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
                multiplier = self.get_and_remove_segment(i)[0]

                while True:
                    try:
                        # if more segments with <variable> exist, merge them 
                        # with the segment put aside
                        j = self.variables.index(variable)
                        multiplier += self.get_and_remove_segment(j)[0]

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

    def copy(self):
        copy_of_self = LinearFormula(self.__str__())
        return copy_of_self

    def evaluate(self, values_dict):
        #"""
        result = 0
        values_dict[''] = 1
        try:
            for i in range(self.length()):
                result += self.multipliers[i]*values_dict[self.variables[i]]
        except:
            raise ValueError("Not all variables are provided")
        return result
        """
        temp_formula = self.copy()

        for variable in values_dict.keys():
            value_as_formula = LinearFormula(str(values_dict[variable]))
            temp_formula.substitute(variable, value_as_formula, inplace=True)

        temp_formula.zip(inplace=True)
        if temp_formula.variables == ['']:
            return temp_formula.multipliers[0]
        elif temp_formula.variables == []:
            return 0
        else:
            raise ValueError("Not all variables are provided")
        #"""

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



if __name__ == '__main__':

    x = LinearFormula('a - 4')

    print(x.multipliers)




