import pytest
from ..lexer import ParhlLexer


def write_tokens_to_file_testing(toks_file, out_file):
    with open(toks_file, 'r') as my_code:
        data = my_code.read()
    lexer = ParhlLexer()
    iter = list(lexer.tokenize(data))
    with open(out_file, 'w') as my_file:
        for i in iter:
            my_file.write(f"{i}\n")


@pytest.fixture(params=[("./lexer_parser/tests/data/lex_1.parhl", "./lexer_parser/tests/data/lex_1.out"),
                        ("./lexer_parser/tests/data/lex_2.parhl", "./lexer_parser/tests/data/lex_2.out")])
def data_out_lexer(request):
    code, toks = request.param
    with open(code, 'r') as my_code:
        data = my_code.read()
    with open(toks, 'r') as my_toks:
        out = my_toks.read()
    return data, out


def test_lexer(data_out_lexer, capfd):
    data_lexer, out_lexer = data_out_lexer
    lexer = ParhlLexer()
    tokens = list(lexer.tokenize(data_lexer))
    for token in tokens: print(token)
    out, _ = capfd.readouterr()
    assert out ==  out_lexer
 