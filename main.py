from lexer_parser.lexer import ParhlLexer
from lexer_parser.parser import ParhlParser
from lexer_parser.structs.parse_context import ParseContext
from sys import argv

def lex_pars(filename):
    lexer = ParhlLexer()
    parser = ParhlParser()
    with open(filename, 'r') as my_code:
        data = my_code.read()
    tokens = lexer.tokenize(data)
    ast = parser.parse(tokens)
    ctx = ParseContext()
    ast.gen(ctx)
    qs = ctx.get_quadruples()
    print(qs)
    return tokens, ast

if __name__ == '__main__': 
    filename = argv[1]
    lex_pars(filename)
    pass
