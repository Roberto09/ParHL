from lexer import ParhlLexer
from parser import ParhlParser
from sys import argv

def lex_pars(filename):
    lexer = ParhlLexer()
    parser = ParhlParser()
    with open(filename, 'r') as my_code:
        data = my_code.read()
    tokens = lexer.tokenize(data)
    parse_result = parser.parse(tokens)
    return tokens, parse_result

if __name__ == '__main__': 
    filename = argv[1]
    lex_pars(filename)
    pass
