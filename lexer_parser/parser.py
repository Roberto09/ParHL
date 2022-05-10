from ast_classes.Const import Const
from ast_classes.Globals import Globals
from ast_classes.Id import Id
from ast_classes.BinExpr import BinExpr
from ast_classes.UnExpr import UnExpr
from ast_classes.Var import Var
from sly import Parser
from lexer import ParhlLexer

class ParhlParser(Parser):
    debugfile = 'parser.out'
    # Get the token list from the lexer (required)
    tokens = ParhlLexer.tokens
    
    @_('ignored_newlines globals_aux')
    def globals(self, p):
        return p.globals_aux

    @_('statement globals_aux')
    def globals_aux(self, p):
        return Globals(p[0], p[1])

    @_('statements')
    def globals_aux(self, p):
        return Globals(p[0], None)

    @_('empty')
    def globals_aux(self, p):
        return Globals(None, None)

    @_('INT_V')
    def const(self, p):
        return Const(p[0], 'Int')

    @_('FLOAT_V')
    def const(self, p):
        return Const(p[0], 'Float')
   
    @_('BOOL_V')
    def const(self, p):
        return Const(p[0], 'Bool')
    
    @_('STRING_V')
    def const(self, p):
        return Const(p[0], 'String')

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

    @_('ignored_newlines L_BRACE ignored_newlines block_1 R_BRACE ignored_newlines')
    def block(self, p):
        pass

    @_('statement block_1', 'empty')
    def block_1(self, p):
        pass

    @_('INT_T', 'FLOAT_T', 'STRING_T', 'BOOL_T', 'GPU_INT_T', 'GPU_FLOAT_T','GPU_BOOL_T')
    def const_type(self, p):
        pass
    
    @_('t_expr', 't_expr OR expr')
    def expr(self, p):
        if(len(p) == 1):
            return p[0]
        else:
            return BinExpr(p[0], p[1], p[2])

    @_('g_expr', 'g_expr AND t_expr')
    def t_expr(self, p):
        if(len(p) == 1):
            return p[0]
        else:
            return BinExpr(p[0], p[1], p[2])

    @_('m_expr', 'm_expr comparison m_expr')
    def g_expr(self, p):
        if(len(p) == 1):
            return p[0]
        else:
            return BinExpr(p[0], p[1], p[2])

    @_('EQ', 'NOT_EQ', 'GT', 'LT', 'GEQT', 'LEQT')
    def comparison(self, p):
        return p[0]

    @_('term', 'term PLUS m_expr', 'term MINUS m_expr')
    def m_expr(self, p):
        if(len(p) == 1):
            return p[0]
        else:
            return BinExpr(p[0], p[1], p[2])

    @_('exp_factor', 'exp_factor MULT term', 'exp_factor DIV term', 'exp_factor MOD term')
    def term(self, p):
        if(len(p) == 1):
            return p[0]
        else:
            return BinExpr(p[0], p[1], p[2])

    @_('factor', 'factor EXP exp_factor')
    def exp_factor(self, p):
        if(len(p) == 1):
            return p[0]
        else:
            return BinExpr(p[0], p[1], p[2])

    @_('factor_1', 'NOT factor_1', 'PLUS factor_1', 'MINUS factor_1')
    def factor(self, p):
        if len(p) == 1:
            return p[0]
        else:
            return UnExpr(p[0], p[1])

    @_('L_PAREN expr R_PAREN', 'const', 'func_call', 'tens', 'tens_id')
    def factor_1(self, p):
        if len(p) == 3:
            return p[1]
        else:
            return p[0]

    @_('ID')
    def factor_1(self, p):
        return Id(p[0])

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
        return p[1]

    @_('var_2', 'var_2 COMMA var_1')
    def var_1(self, p):
        return p[0]

    @_('var_3', 'var_3 ASSIG expr')
    def var_2(self, p):
        if len(p) == 1:
            return Var(p[0][0], p[0][1], None)
        else:
            return Var(p[0][0], p[0][1], p[2])

    @_('var_id COLON const_type')
    def var_3(self, p):
        return [p[0], p[2]]

    @_('ID','ID var_id_1')
    def var_id(self, p):
        if len(p) == 1:
            return Id(p[0])
        return

    @_('L_BRACKET INT_V R_BRACKET', 'L_BRACKET INT_V R_BRACKET var_id_1')
    def var_id_1(self, p):
        pass

    @_('WHILE L_PAREN expr R_PAREN block')
    def while_loop(self, p):
        pass

    @_('FOR L_PAREN var SEMICOLON expr SEMICOLON assign R_PAREN block')
    def for_loop(self, p):
        pass

    @_('cond_if', 'cond_if_else', 'cond_if_else_if')
    def cond(self, p):
        pass

    @_('IF L_PAREN expr R_PAREN block')
    def simple_if(self, p):
        pass

    @_('ELSE block')
    def simple_else(self, p):
        pass

    @_('ELSE_IF L_PAREN expr R_PAREN block complex_else_if')
    def simple_else_if(self, p):
        pass

    @_('simple_else_if', 'empty', 'simple_else')
    def complex_else_if(self, p):
        pass

    @_('simple_if')
    def cond_if(self, p):
        pass

    @_('simple_if simple_else')
    def cond_if_else(self, p):
        pass

    @_('simple_if simple_else_if')
    def cond_if_else_if(self, p):
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

    @_('RETURN expr')
    def ret(self, p):
        pass

    @_('statements eos', 'block_statements')
    def statement(self, p):
        pass

    @_('var', 'assign', 'read_line', 'print_rule', 'read_file', 
        'write_file', 'func_call', 'ret')
    def statements(self, p):
        pass
    
    @_('while_loop', 'for_loop', 'cond', 'func')
    def block_statements(self, p):
        pass

    @_('SEMICOLON ignored_newlines','NEWLINE ignored_newlines')
    def eos(self, p):
        pass

    @_('NEWLINE ignored_newlines', 'empty')
    def ignored_newlines(self, p):
        pass

    @_('')
    def empty(self, p):
        pass
    