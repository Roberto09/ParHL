from sly import Parser
from lexer import ParhlLexer

class ParhlParser(Parser):
    debugfile = 'parser.out'
    # Get the token list from the lexer (required)
    tokens = ParhlLexer.tokens
    
    @_('statement globals', 'statements', 'block_statements', 'empty')
    def globals(self, p):
        pass

    @_('INT_V','FLOAT_V', 'BOOL_V', 'STRING_V')
    def const(self, p):
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

    @_('ignored_newlines L_BRACE block_1 R_BRACE')
    def block(self, p):
        pass

    @_('statement block_1', 'ret block_1', 'empty')
    def block_1(self, p):
        pass

    @_('INT_T', 'FLOAT_T', 'STRING_T', 'BOOL_T', 'GPU_INT_T', 'GPU_FLOAT_T','GPU_BOOL_T')
    def const_type(self, p):
        pass
    
    @_('t_expr', 't_expr OR expr')
    def expr(self, p):
        pass

    @_('g_expr', 'g_expr AND t_expr')
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

    @_('L_PAREN expr R_PAREN', 'const', 'ID', 'func_call', 'tens', 'tens_id')
    def factor_1(self, p):
        pass

    @_('READ_LINE L_PAREN R_PAREN')
    def read_line(self, p):
        pass
    
    @_('PRINT L_PAREN func_call_1')
    def print_rule(self, p):
        pass

    @_('READ_FILE L_PAREN R_PAREN')
    def read_file(self, p):
        pass

    @_('WRITE_FILE L_PAREN func_call_1')
    def write_file(self, p):
        pass

    @_('ID L_PAREN func_call_1')
    def func_call(self, p):
        pass

    @_('R_PAREN', 'expr R_PAREN', 'expr COMMA func_call_1')
    def func_call_1(self, p):
        pass

    @_('ID ASSIG expr')
    def assign(self, p):
        pass
    
    @_('LET var_1')
    def var(self, p):
        pass

    @_('var_2', 'var_2 COMMA var_1')
    def var_1(self, p):
        pass

    @_('var_3', 'var_3 ASSIG expr')
    def var_2(self, p):
        pass

    @_('var_id COLON const_type')
    def var_3(self, p):
        pass

    @_('ID','ID var_id_1')
    def var_id(self, p):
        pass

    @_('L_BRACKET INT_V R_BRACKET', 'L_BRACKET INT_V R_BRACKET var_id_1')
    def var_id_1(self, p):
        pass

    @_('WHILE L_PAREN expr R_PAREN block')
    def while_loop(self, p):
        pass

    @_('FOR L_PAREN var SEMICOLON expr SEMICOLON assign R_PAREN block')
    def for_loop(self, p):
        pass
    
    @_('IF L_PAREN expr R_PAREN block cond_prima')
    def cond(self, p):
        pass

    @_('empty', 'cond_else', 'cond_else_if')
    def cond_prima(self, p):
        pass
    
    @_('ELSE block')
    def cond_else(self, p):
        pass

    @_('else_if', 'else_if cond_else_if')
    def cond_else_if(self, p):
        pass
    
    @_('ELSE_IF L_PAREN expr R_PAREN block')
    def else_if(self, p):
        pass

    @_('LET ID L_PAREN func_params R_PAREN COLON func_type block')
    def func(self, p):
        pass

    @_('empty', 'func_params_1')
    def func_params(self, p):
        pass

    @_('ID COLON const_type ', 'ID COLON const_type COMMA func_params_1')
    def func_params_1(self, p):
        pass

    @_('const_type', 'VOID')
    def func_type(self, p):
        pass

    @_('RETURN expr eos')
    def ret(self, p):
        pass

    @_('statements eos', 'block_statements NEWLINE', 'NEWLINE')
    def statement(self, p):
        pass

    @_('var', 'assign', 'read_line', 'print_rule', 'read_file', 
        'write_file', 'func_call')
    def statements(self, p):
        pass
    
    @_('while_loop', 'for_loop', 'cond', 'cond_else', 'cond_else_if', 'func')
    def block_statements(self, p):
        pass;

    @_('SEMICOLON','NEWLINE')
    def eos(self, p):
        pass
    
    @_('')
    def empty(self, p):
        pass
    
    @_('NEWLINE ignored_newlines', 'empty')
    def ignored_newlines(self, p):
        pass
