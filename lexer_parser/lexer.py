from sly import Lexer

class ParhlLexer(Lexer):
    # Set of token names. This is always required
    tokens = {}

    literals = { }

    # String containing ignored characters
    ignore = ' \t'
    ignore_comment = r'\#.*'

    # Regular expression rules for tokens
    # PROGRAM = r'[Pp][Rr][Oo][Gg][Rr][Aa][Mm]'
    
    # def FLOAT_VAL(self, t):
    #     t.value = float(t.value)
    #     return t

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1
