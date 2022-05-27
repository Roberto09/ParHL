from ast import Expression
from ..parhl_exceptions import ParhlException
from .Node import Node
from ..parse_context import ParseContext
from ..quadruples import Quadruple
from ...lexer import symbol_to_token

Expression = Node

class Assign(Expression):
    def __init__(self, line, left, right):
        super().__init__(line)
        self.left = left
        self.right = right
  
    def gen_impl(self, ctx: ParseContext):
        right_var = self.right.gen(ctx)
        left_var = self.left.gen(ctx)
        ctx.semantic_cube.get_type('ASSIG',left_var.type, right_var.type)
        ctx.add_quadruple(Quadruple('ASSIG', right_var.mem_dir, None, left_var.mem_dir))


class BinExpr(Expression):
    def __init__(self, line, left, op, right): 
        super().__init__(line)
        self.left = left
        self.right = right
        self.op = op

    def gen_impl(self, ctx: ParseContext):
        left_var = self.left.gen(ctx)
        right_var = self.right.gen(ctx)
        op_name = symbol_to_token[self.op]
        new_type = ctx.semantic_cube.get_type(op_name, left_var.type, right_var.type)
        temp_var = ctx.func_dir.new_temp(new_type)
        # Need to change names to mem_dirs when they are functioning
        ctx.add_quadruple(Quadruple(op_name, left_var.mem_dir, right_var.mem_dir, temp_var.mem_dir))
        return temp_var


# This implementation depends a bit on how we actually want to handle
# constants in memory and in quadruples. TBD.
class Const(Expression):
    def __init__(self, line, value, type):
        super().__init__(line)
        self.value = value
        self.token_type = type
        self.type = type.replace('V', 'T')
        
    def gen_impl(self, ctx: ParseContext):
        # Guardar en memoria de constantes
        return ctx.func_dir.new_temp(self.type, self.value)

class Id(Expression):
    def __init__(self, line, id):
        super().__init__(line)
        self.id = id
  
    def gen_impl(self, ctx: ParseContext):
        return ctx.func_dir.get_var(self.id)

class Access(Expression):
    def __init__(self, line, id_access, expr_seq):
        super().__init__(line)
        self.id_access = id_access
        self.expr_seq = expr_seq
    
    @property
    def id(self):
        return self.id_access.id

    def gen_impl(self, ctx: ParseContext):
        tens = ctx.func_dir.get_var(self.id)
        exprs = self.expr_seq.gen_ret_list(ctx)
        if len(tens.dims) != len(exprs):
            raise ParhlException('Not enough indices provided to array accessor')
        
        last = len(exprs) - 1
        total_var = ctx.func_dir.new_temp('INT_T',0)
        for i, var in enumerate(exprs):
            if var.type != 'INT_T':
                raise ParhlException(f"Expected integer at dimension {i} but got {var.type}")
            ctx.add_quadruple(Quadruple('VERIFY', tens.dims[i]['limit'].mem_dir, result=var.mem_dir))
            if i != last:
                new_temp = ctx.func_dir.new_temp('INT_T')
                ctx.add_quadruple(Quadruple('MULT', var.mem_dir, tens.dims[i]['m'].mem_dir, new_temp.mem_dir))
                ctx.add_quadruple(Quadruple('PLUS', new_temp.mem_dir, total_var.mem_dir, total_var.mem_dir))
            if i == last:
                base_mem_dir, new_temp = ctx.func_dir.new_address_temp(tens.type)
                ctx.add_quadruple(Quadruple('PLUS', total_var.mem_dir, tens.addr_var.mem_dir, base_mem_dir))
                return new_temp

class UnExpr(Expression):
    def __init__(self, line, op, right):
        super().__init__(line)
        self.op = op
        self.right = right

    def gen_impl(self, ctx: ParseContext):
        right_var = self.right.gen(ctx)
        op_name = symbol_to_token[self.op]
        new_type = ctx.semantic_cube.get_type(op_name, right_var.type)
        new_var = ctx.func_dir.new_temp(new_type)
        ctx.add_quadruple(Quadruple(op_name, right_var.mem_dir, None, new_var.name))
        return new_var
