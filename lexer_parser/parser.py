from lexer_parser.structs.parhl_exceptions import ParhlException
from .structs.ast.Expressions import Assign, BinExpr, Const, Id, UnExpr, Access
from .structs.ast.Statements import DimConst, TensorDecl, TensorDim, FuncDecl, VarDecl, Seq, If, While, For, Ret, FuncCall, IOFunc, Empty
from sly import Parser
from .lexer import ParhlLexer

class ParhlParser(Parser):
    # debugfile = 'parser.out'
    # Get the token list from the lexer (required)
    
    tokens = ParhlLexer.tokens
    precedence = (
        ('left', OR),
        ('left', AND),
        ('left', EQ, NOT_EQ, GT, LT, GEQT, LEQT),
        ('left', PLUS, MINUS),
        ('left', MULT, DIV, MOD),
        ('left', EXP)
    )
    
    @_('ignored_newlines globals_aux')
    def globals(self, p):
        return p[1]

    @_('statement globals_aux',  'statements', 'empty')
    def globals_aux(self, p):
        if len(p) == 1:
            return Seq(p[0].lineno, p[0])
        return Seq(p[0].lineno, p[0], p[1])
        
    @_('INT_V', 'FLOAT_V', 'BOOL_V', 'STRING_V')
    def const(self, p):
        value, type = p[0]
        return Const(p.lineno, value, type)

    @_('L_BRACKET expr tens_1')
    def tens(self, p):
        pass

    @_('R_BRACKET', 'COMMA expr tens_1')
    def tens_1(self, p):
        pass

    @_('ID tens_id_1')
    def tens_id(self,p):
        return Access(p.lineno, Id(p.lineno, p[0]), p[1])

    @_('L_BRACKET expr R_BRACKET tens_id_1', 'L_BRACKET expr R_BRACKET')
    def tens_id_1(self, p):
        if len(p) == 3:
            return Seq(p.lineno, p[1])
        return Seq(p.lineno, p[1], p[3])

    @_('ignored_newlines L_BRACE ignored_newlines block_1 R_BRACE ignored_newlines')
    def block(self, p):
        return p[3]

    @_('statement block_1', 'empty')
    def block_1(self, p):
        if len(p) == 2:
            return Seq(p[0].lineno, p[0], p[1])
        return Seq(p[0].lineno, p[0])

    @_('INT_T', 'FLOAT_T', 'STRING_T', 'BOOL_T', 'GPU_INT_T', 'GPU_FLOAT_T','GPU_BOOL_T')
    def const_type(self, p):
        return p[0]
    
    @_('t_expr', 'expr OR t_expr')
    def expr(self, p):
        if(len(p) == 1):
            return p[0]
        else:
            return BinExpr(p.lineno, p[0], p[1], p[2])

    @_('g_expr', 't_expr AND g_expr')
    def t_expr(self, p):
        if(len(p) == 1):
            return p[0]
        else:
            return BinExpr(p.lineno, p[0], p[1], p[2])

    @_('m_expr', 'm_expr comparison m_expr')
    def g_expr(self, p):
        if(len(p) == 1):
            return p[0]
        else:
            comp, lineno = p[1]
            return BinExpr(lineno, p[0], comp, p[2])

    @_('EQ', 'NOT_EQ', 'GT', 'LT', 'GEQT', 'LEQT')
    def comparison(self, p):
        return p[0], p.lineno

    @_('term', 'm_expr PLUS term', 'm_expr MINUS term')
    def m_expr(self, p):
        if(len(p) == 1):
            return p[0]
        else:
            return BinExpr(p.lineno, p[0], p[1], p[2])

    @_('exp_factor', 'term MULT exp_factor', 'term DIV exp_factor', 'term MOD exp_factor')
    def term(self, p):
        if(len(p) == 1):
            return p[0]
        else:
            return BinExpr(p.lineno, p[0], p[1], p[2])

    @_('factor', 'exp_factor EXP factor')
    def exp_factor(self, p):
        if(len(p) == 1):
            return p[0]
        else:
            return BinExpr(p.lineno, p[0], p[1], p[2])

    @_('factor_1', 'NOT factor_1', 'PLUS factor_1', 'MINUS factor_1')
    def factor(self, p):
        if len(p) == 1:
            return p[0]
        else:
            return UnExpr(p.lineno, p[0], p[1])

    @_('L_PAREN expr R_PAREN', 'const', 'func_call', 'tens', 'tens_id', 'read_line', 'read_file')
    def factor_1(self, p):
        if len(p) == 3:
            return p[1]
        else:
            return p[0]

    @_('ID')
    def factor_1(self, p):
        return Id(p.lineno, p[0])

    @_('READ_LINE L_PAREN dim_const R_PAREN')
    def read_line(self, p):
        return IOFunc(p.lineno, p[0], return_type=p[2])
    
    @_('PRINT L_PAREN func_call_1')
    def print_rule(self, p):
        return IOFunc(p.lineno, p[0], args_seq=p[2])

    @_('const_type var_dims', 'const_type')
    def dim_const(self, p ):
        if len(p) == 2:
            return DimConst(-1, p[0], p[1])

        return DimConst(-1, p[0], Seq(-1, Empty()))

    @_('READ_FILE L_PAREN dim_const COMMA expr R_PAREN')
    def read_file(self, p):
        return IOFunc(p.lineno, p[0], dim_const=p[2], args_seq=Seq(p.lineno, p[4]))

    @_('WRITE_FILE L_PAREN func_call_1')
    def write_file(self, p):
        return IOFunc(p.lineno, p[0], args_seq=p[2])

    @_('ID L_PAREN func_call_1')
    def func_call(self, p):
        return FuncCall(p.lineno, p[0], p[2])

    @_('R_PAREN', 'expr R_PAREN', 'expr COMMA func_call_1')
    def func_call_1(self, p):
        if len(p) == 1:
            return Empty()
        elif len(p) == 2:
            return Seq(p.lineno, p[0])
        elif len(p) == 3:
            return Seq(p.lineno, p[0], p[2])

    @_('ID ASSIG expr')
    def assign(self, p):
        return Assign(p.lineno, Id(p.lineno, p[0]), p[2])
    
    @_('tens_id ASSIG expr')
    def assign(self, p):
        return Assign(p.lineno, p[0], p[2])
    
    @_('LET var_1')
    def var(self, p):
        return p[1]

    @_('var_2', 'var_2 COMMA var_1')
    def var_1(self, p):
        if len(p) == 1:
            return Seq(p[0].lineno, p[0])
        return Seq(p.lineno, p[0], p[2])

    @_('var_3', 'var_3 ASSIG expr', 'tens_decl', 'tens_decl ASSIG expr')
    def var_2(self, p):
        if len(p) == 3:
            p[0].do_assign(p[2])
        return p[0]

    @_('ID COLON const_type')
    def var_3(self, p):
        return VarDecl(p.lineno, Id(p.lineno, p[0]), p[2])

    @_('ID var_dims COLON const_type')
    def tens_decl(self, p):
        return TensorDecl(p.lineno, Id(p.lineno, p[0]), p[3], p[1])

    @_('L_BRACKET INT_V R_BRACKET','L_BRACKET INT_V R_BRACKET var_dims')
    def var_dims(self, p):
        if len(p) == 3:
            return Seq(p.lineno, TensorDim(p.lineno, p[1][0]))
        return Seq(p.lineno, TensorDim(p.lineno, p[1][0]), p[3])

    @_('WHILE L_PAREN expr R_PAREN block')
    def while_loop(self, p):
        return While(p.lineno, p[2], p[4])

    @_('FOR L_PAREN var SEMICOLON expr SEMICOLON assign R_PAREN block')
    def for_loop(self, p):
        return For(p.lineno, p[2], p[4], p[6], p[8])

    @_('cond_if', 'cond_if_else', 'cond_if_else_if')
    def cond(self, p):
        return p[0]

    @_('IF L_PAREN expr R_PAREN block')
    def simple_if(self, p):
        return If.IfSeqAux(p.lineno, p[2], p[4])

    @_('ELSE block')
    def simple_else(self, p):
        return If.ElseAux(p.lineno, p[1])

    @_('ELSE_IF L_PAREN expr R_PAREN block complex_else_if')
    def simple_else_if(self, p):
        return If.IfSeqAux(p.lineno, p[2], p[4], p[5])

    @_('simple_else_if', 'empty')
    def complex_else_if(self, p):
        return p[0]

    @_('simple_if')
    def cond_if(self, p):
        return If(p[0].lineno, p[0])

    @_('simple_if simple_else')
    def cond_if_else(self, p):
        return If(p[0].lineno, p[0].with_last(p[1]))

    @_('simple_if simple_else_if', 'simple_if simple_else_if simple_else')
    def cond_if_else_if(self, p):
        if len(p) == 2:
            return If(p[0].lineno, p[0].with_last(p[1]))
        return If(p[0].lineno, p[0].with_last(p[1].with_last(p[2])))

    @_('LET ID L_PAREN func_params R_PAREN COLON func_type block')
    def func(self, p):
        return FuncDecl(p.lineno, Id(p.lineno, p[1]), p[6], p[3], p[7])

    @_('func_params_1', 'empty')
    def func_params(self, p):
        return p[0]

    @_('ID COLON const_type ', 'ID COLON const_type COMMA func_params_1')
    def func_params_1(self, p):
        if len(p) == 3:
            return Seq(p.lineno, VarDecl(p.lineno, Id(p.lineno, p[0]), p[2]))
        return Seq(p.lineno, VarDecl(p.lineno, Id(p.lineno, p[0]), p[2]), p[4])

    @_('const_type', 'VOID')
    def func_type(self, p):
        return p[0]

    @_('RETURN expr')
    def ret(self, p):
        return Ret(p.lineno, p[1])

    @_('statements eos', 'block_statements')
    def statement(self, p):
        return p[0]

    @_('var', 'assign', 'print_rule', 
        'write_file', 'func_call', 'ret')
    def statements(self, p):
        return p[0]
    
    @_('while_loop', 'for_loop', 'cond', 'func')
    def block_statements(self, p):
        return p[0]

    @_('SEMICOLON ignored_newlines','NEWLINE ignored_newlines')
    def eos(self, p):
        pass

    @_('NEWLINE ignored_newlines', 'empty')
    def ignored_newlines(self, p):
        pass

    @_('')
    def empty(self, p):
        return Empty()

    def error(self, p):
        if p:
            raise ParhlException(f"Syntax error at {p.type}", p.lineno)
        raise ParhlException("Syntax error", "EOF")