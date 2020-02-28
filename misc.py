def type_of_char(char):
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

def inplace(**kwargs):
    try:
        def decorator(func):
            def real_func(self, *args, inplace=kwargs['default']):
                if inplace == True:
                    func(self, *args)
                elif inplace == False:
                    copy_of_self = self.copy()
                    func(copy_of_self, *args)
                    return copy_of_self
                else:
                    raise ValueError(f"invalid 'inplace' argument: {inplace}")

            return real_func

        return decorator
    except KeyError:
        raise ValueError('default argument not specified')