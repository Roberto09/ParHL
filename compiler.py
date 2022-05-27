from lexer_parser.lexer import ParhlLexer
from lexer_parser.parser import ParhlParser
from lexer_parser.structs.parse_context import ParseContext
from lexer_parser.structs.parhl_exceptions import ParhlException
from sys import argv

def get_output_file(input_file):
    if input_file[-6:] != '.parhl':
        raise ParhlException(f"The provided filename: {input_file} does not have the .parhl extension.")
    return input_file[:-6] + ".out"

def lex_pars(input_file):
    output_file = get_output_file(input_file)
    lexer = ParhlLexer()
    parser = ParhlParser()
    with open(input_file, 'r') as my_code:
        data = my_code.read()
    tokens = lexer.tokenize(data)
    ast = parser.parse(tokens)
    ctx = ParseContext()
    ast.gen(ctx)
    ctx.output(output_file)
   
if __name__ == '__main__': 
    filename = argv[1]
    try:
        lex_pars(filename)
    except ParhlException as pe:
        print(pe)
    except Exception as e:
        # TODO, same as in Node : we must change this handling in prod
        raise e
