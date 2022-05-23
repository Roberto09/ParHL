import pytest
from ..lexer import ParhlLexer
from ..parser import ParhlParser
from ..structs.parse_context import ParseContext

"""FIXTURES AND HELPERS"""
def write_tokens_to_file_testing(toks_file, out_file):
    with open(toks_file, 'r') as my_code:
        data = my_code.read()
    lexer = ParhlLexer()
    iter = list(lexer.tokenize(data))
    with open(out_file, 'w') as my_file:
        for i in iter:
            my_file.write(f"{i}\n")

def data_out(code_f, out_f):
    # write_tokens_to_file_testing(code_f, out_f)
    with open(code_f, 'r') as my_code:
        data = my_code.read()
    with open(out_f, 'r') as my_out:
        out = my_out.read()
    return data, out

@pytest.fixture(params=[("./lexer_parser/tests/data/lex_1.parhl", "./lexer_parser/tests/data/lex_1.out"),
                        ("./lexer_parser/tests/data/lex_2.parhl", "./lexer_parser/tests/data/lex_2.out")])
def data_out_lexer(request):
    code_f, toks_f = request.param
    # write_tokens_to_file_testing(code, toks)
    return data_out(code_f, toks_f)

@pytest.fixture(params=[("./lexer_parser/tests/data/parser_func_dir_1.parhl",
                        "./lexer_parser/tests/data/parser_func_dir_1.out")])
def data_out_parser_func_dir(request):
    code_f, func_dir_f = request.param
    return data_out(code_f, func_dir_f)


"""TESTS"""
def test_lexer(data_out_lexer, capfd):
    data_lexer, out_lexer = data_out_lexer
    lexer = ParhlLexer()
    tokens = list(lexer.tokenize(data_lexer))
    for token in tokens: print(token)
    out, _ = capfd.readouterr()
    assert out == out_lexer

def test_parser_func_dir(data_out_parser_func_dir, capfd):
    data_parser, out_parser = data_out_parser_func_dir
    lexer = ParhlLexer()
    tokens = lexer.tokenize(data_parser)
    parser = ParhlParser()
    ast = parser.parse(tokens)
    ctx = ParseContext()
    ast.gen(ctx)
    print(ctx.func_dir)
    out, _ = capfd.readouterr()
    assert out == out_parser
