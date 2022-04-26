import pytest
from ..lexer import ParhlLexer

def write_to_file_testing(iter, file):
    with open(file, 'w') as my_file:
        for i in iter:
            my_file.write(f"{i}\n")


@pytest.fixture(params=[("./tests/data/lex_1.parhl", "./tests/data/lex_1.out"),
                        ("./tests/data/lex_2.parhl", "./tests/data/lex_2.out")])
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