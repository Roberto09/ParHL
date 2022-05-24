from lexer_parser.lexer import ParhlLexer
from lexer_parser.parser import ParhlParser
from lexer_parser.structs.parse_context import ParseContext
from lexer_parser.structs.parhl_exceptions import ParhlException
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
    for (i, q) in enumerate(qs):
        print(i, " - ", q)
    return tokens, ast

if __name__ == '__main__': 
    filename = argv[1]
    try:
        lex_pars(filename)
    except ParhlException as pe:
        print(pe)
    except Exception as e:
        # TODO, same as in Node : we must change this handling in prod
        raise e
