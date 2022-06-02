from sly import Lexer
from .structs.parhl_exceptions import ParhlException

class ParhlLexer(Lexer):
    # Set of token names. This is always required
    tokens = {
        # Variables / Funcs
        LET, RETURN, VOID,
        # Loops
        FOR, WHILE,
        # Conditionals
        ELSE_IF, IF, ELSE,
        # Types
        INT_T, FLOAT_T, BOOL_T, STRING_T, GPU_INT_T, GPU_FLOAT_T, GPU_BOOL_T,
        # Bool Operators
        OR, AND, NOT,
        # Values
        FLOAT_V, INT_V, STRING_V, BOOL_V,
        # IO
        PRINT, READ_LINE, READ_FILE, WRITE_FILE,
        # Arrays
        L_BRACKET, R_BRACKET,
        # Scopes
        L_BRACE, R_BRACE,
        # Operators
        PLUS, MINUS, DIV, MULT, EXP, MOD, EQ, ASSIG, NOT_EQ, GEQT, LEQT, GT, LT, L_PAREN, R_PAREN,  
        # Misc
        COLON, SEMICOLON, COMMA, NEWLINE, ID,        
    }

    # String containing ignored characters
    ignore = ' \t'
    ignore_comment = r'\#.*'

    # Regular expression rules for tokens

    # Variables
    LET = r"let"
    RETURN = r"return"
    VOID = r"void"
    # Loops
    FOR = r"for"
    WHILE = r"while"
    # Conditionals
    ELSE_IF = r"else if"
    IF = r"if"
    ELSE = r"else"
    # Types
    INT_T = r"int"
    FLOAT_T = r"float"
    BOOL_T = r"bool"
    STRING_T = r"string"
    GPU_INT_T = r"gpu_int"
    GPU_FLOAT_T = r"gpu_float"
    GPU_BOOL_T = r"gpu_bool"
    # Bool Operators
    OR = r"or"
    AND = r"and"
    NOT = r"not"
    # Values
    FLOAT_V = r'[0-9]+\.[0-9]+'
    INT_V = r'[0-9]+'
    STRING_V = r'\".*\"'
    BOOL_V = r"True|False"
    # IO
    PRINT = r"print"
    READ_LINE = r"read_line"
    READ_FILE = r"read_file"
    WRITE_FILE = r"write_file"
    # Arrays
    L_BRACKET = r"\["
    R_BRACKET = r"\]"
    # Scopes
    L_BRACE = r"\{"
    R_BRACE = r"\}"
    # Operators
    PLUS = r"\+"
    MINUS = r"\-"
    DIV = r"\/"
    MULT = r"\*"
    EXP = r"\^"
    MOD = r"\%"
    EQ = r"\="
    ASSIG = r"\:\="
    NOT_EQ = r"\<\>"
    GEQT = r"\>\="
    LEQT = r"\<\="
    GT = r"\>"
    LT = r"\<"
    L_PAREN = r"\("
    R_PAREN = r"\)"    
    # Misc
    COLON = r"\:"
    COMMA = r"\,"
    SEMICOLON = r"\;"
    NEWLINE = r"\n"
    ID = r"[a-zA-Z_][a-zA-Z0-9_]*"
    
    def FLOAT_V(self, t):
        t.value = (float(t.value), 'FLOAT_V')
        return t

    def INT_V(self, t):
        t.value = (int(t.value), 'INT_V')
        return t

    def STRING_V(self, t):
        t.value = (t.value[1:-1], 'STRING_V')
        return t

    def BOOL_V(self, t):
        t.value = (t.value == "True", 'BOOL_V')
        return t
    
    def NEWLINE(self, t): 
        self.lineno = self.lineno + 1
        return t

    def error(self, t):
        raise ParhlException(f'Bad character {t.value[0]}', self.lineno)

type_to_token = {
    'int': 'INT_T',
    'float': 'FLOAT_T',
    'string': 'STRING_T', 
    'bool': 'BOOL_T',
    'gpu_int': 'GPU_INT_T',
    'gpu_float': 'GPU_FLOAT_T',
    'gpu_bool': 'GPU_BOOL_T',
    'void': 'VOID',
}

type_token_to_mem_id = {
    'INT_T' : 0,
    'FLOAT_T' : 0,
    'STRING_T' : 0,
    'BOOL_T' : 0,
    'GPU_INT_T' : 1,
    'GPU_FLOAT_T' : 2,
    'GPU_BOOL_T' : 3,
}

symbol_to_token = {
    "*": 'MULT',
    "+": 'PLUS',
    "-": 'MINUS',
    "/": 'DIV',
    "^": 'EXP',
    "%": 'MOD',
    "=": 'EQ',
    "<>": 'NOT_EQ',
    ">=": 'GEQT',
    "<=": 'LEQT',
    ">": 'GT',
    "<": 'LT',
    "and": 'AND',
    "or": 'OR',
    "not": 'NOT',
}
