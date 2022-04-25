from sly import Parser
from lexer import ParhlLexer

class ParhlParser(Parser):
    # Get the token list from the lexer (required)
    tokens = CalcLexer.tokens
    
    # Grammar rules and actions
    # """PROGRAM"""
    # @_('PROGRAM ID ";" program2 bloque1')
    # def program1(self, p):
    #     return "program parsed"

    # @_('')
    # def empty(self, p):
    #     pass