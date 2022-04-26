from sly import Parser
from lexer import ParhlLexer

class ParhlParser(Parser):
    # Get the token list from the lexer (required)
    tokens = ParhlLexer.tokens
    
    # Grammar rules and actions
    # """PROGRAM"""
    # @_('PROGRAM ID ";" program2 bloque1')
    # def program1(self, p):
    #     return "program parsed"

    # @_('')
    # def empty(self, p):
    #     pass
    @_('estatuto globales', 'estatuto')
    def globales(self, p)
    
    @_('SEMICOLON','NEWLINE')
    def eos(self, p):
        pass
    
    @_('INT_v','FLOAT_V', 'BOOL_V', 'STRING_v')
    def cte(self, p):
        pass

    @_('L_BRACKET expr tens_1')
    def tens(self, p):
        pass

    @_('R_BRACKET', 'COMMA expr tens_1')
    def tens_1(self, p):
        pass

    @_('ID tens_id_1')
    def tens_id(self,p):
        pass
    
    @_('L_BRACKET expr R_BRACKET', 'L_BRACKET expr R_BRACKET tens_id_1')
    def tens_id_1(self, p):
        pass

    @_('L_BRACE bloque_1 R_BRACE')
    def bloque(self, p):
        pass

    @_('bloque_1 bloque_1', 'estatuto', 'retorno')
    def bloque_1(self, p):
        pass

    @_('INT_T', 'FLOAT_T', 'STRING_T', 'BOOL_T', 'GPU_INT_T', 'GPU_FLOAT_T','GPU_BOOL_T')
    def type(self, p):
        pass
    
    @_('t_expr', 't_expr OR expr')
    def expr(self, p):
        pass

    @_('g_expr', 'g_exp AND t_expr')
    def t_expr(self, p):
        pass

    @_('m_expr', 'm_expr comparison m_expr')
    def g_expr(self, p):
        pass

    @_('EQ', 'NOT_EQ', 'GT', 'LT', 'GEQT', 'LEQT')
    def comparison(self, p):
        pass

    @_('term', 'term PLUS m_expr', 'term MINUS m_expr')
    def m_expr(self, p):
        pass

    @_('exp_factor', 'exp_factor MULT term', 'exp_factor DIV term', 'exp_factor MOD term')
    def term(self, p):
        pass

    @_('factor', 'factor EXP exp_factor')
    def exp_factor(self, p):
        pass

    @_('factor_1', 'NOT factor_1', 'PLUS factor_1', 'MINUS factor_1')
    def factor(self, p):
        pass

    @_('L_PAREN expr R_PAREN', 'cte', 'ID', 'func_call', 'tens', 'tens_id')
    def factor_1(self, p):
        pass

    @_('ID L_PAREN func_call_1')
    def func_call(self, p):
        pass

    @_('R_PAREN', 'expr R_PAREN', 'expr COMMA func_call_1')
    def func_call_1(self, p):
        pass
    
    @_('ID ASSIG expr')
    def asignacion(self, p):
        pass
    
    @_('LET var_1')
    def var(self, p):
        pass
    
    @_('var_2', 'var_2 var_3')
    def var_1(self, p):
        pass

    @_('LET var_id COLON type')
    def var_2(self, p):
        pass

    @_('ASSIG expr', 'ASSIG expr COMMA var_1', 'COMMMA var_1')
    def var_3(self, p):
        pass

    @_('ID','ID var_id_1')
    def var_id(self, p):
        pass

    @_('L_PAREN CTE_I R_PAREN', 'L_PAREN CTE_I R_PAREN var_id_1')
    def var_id_1(self, p):
        pass

    @_('WHILE L_PAREN expr R_PAREN bloque')
    def while_loop(self, p):
        pass

    @_('FOR L_PAREN var SEMICOLON expr SEMICOLON ASSIG R_PAREN bloque')
    def for_loop(self, p):
        pass 

    @_('IF L_PAREN expr R_PAREN cond_1')
    def cond(self, p):
        pass

    @_('bloque', 'bloque ELSE bloque', 'bloque cond_2')
    def cond_1(self, p):
        pass

    @_('ELSE_IF BLOQUE', 'ELSE_IF BLOQUE cond_2')
    def cond_2(self, p):
        pass

    @_('LET ID L_PAREN func_params func_type bloque')
    def func(self, p):
        pass

    @_('R_PAREN', 'func_params_1')
    def func_params(self, p):
        pass

    @_('ID COLON type R_PAREN', 'ID COLON TYPE COMMA func_params_1')
    def func_params_1(self, p):
        pass

    @_('type', 'VOID')
    def func_type(self, p):
        pass

    @_('RETURN expr eos')
    def retorno(self, p):
        pass
    
    @_('var eos', 'asignacion eos', 'while_loop eos', 'for_loop eos', 'cond eos', 'func_call eos', 'func eos', 'eos')
    def estatuto(self, p):
        pass