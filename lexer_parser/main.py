from lexer import ParhlLexer
from parser import ParhlParser

def lex_pars(filename):
    lexer = ParhlLexer()
    parser = ParhlParser()
    with open(FILE, 'r') as my_code:
        data = my_code.read()
    tokens = lexer.tokenize(data)
    parse_result = parser.parse(tokens)
    return tokens, parse_result

if __name__ == '__main__': 
    # lex_pars(filename)
    pass
