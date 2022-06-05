from lexer_parser.structs.semantic_cube import SemanticCube
from ..var_dir import Tensor, TensorConst
from ..parhl_exceptions import ParhlException
from .Node import Node
from ..parse_context import ParseContext
from ..quadruples import Quadruple
from ...lexer import symbol_to_token
from functools import reduce
from ..tensor_shape_utils import matmul, broadcast, matpow

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
        if type(right_var) == Tensor:
            if type(left_var) != Tensor:
                raise ParhlException('Cannot assign a tensor to a primitive')
            if [dim['n'] for dim in left_var.dims] != [dim['n'] for dim in right_var.dims]:
                raise ParhlException('Tensor assign failed: tensor dimensions do not match')
            
            total = reduce(lambda x,y: x*y, [dim['n'] for dim in right_var.dims])
            for i in range(0, total):
                origin_mem_dir = (right_var.mem_dir[0], right_var.mem_dir[1] + i, right_var.mem_dir[2], right_var.mem_dir[3])
                dest_mem_dir = (left_var.mem_dir[0], left_var.mem_dir[1] + i, left_var.mem_dir[2], left_var.mem_dir[3])
                ctx.add_quadruple(Quadruple('ASSIG', origin_mem_dir, result=dest_mem_dir))
        else: # regular primitive assign
            if type(left_var) == Tensor:
                raise ParhlException('Cannot assign a primitive to a tensor')
            ctx.add_quadruple(Quadruple('ASSIG', right_var.mem_dir, result=left_var.mem_dir))


class BinExpr(Expression):
    def __init__(self, line, left, op, right): 
        super().__init__(line)
        self.left = left
        self.right = right
        self.op = op

    def _gen_impl_tens(self, ctx:ParseContext, left_var, right_var, op_name):
        left_dims = [d['n'] for d in left_var.dims] if type(left_var) == Tensor else []
        right_dims = [d['n'] for d in right_var.dims] if type(right_var) == Tensor else []
        dims_res_func = broadcast
        if self.op == "**":
            dims_res_func = matmul
        elif self.op == "^":
            if type(right_var) == Tensor:
                SemanticCube.raise_type_error(f"tensor({left_var.type})", op_name, f"tensor({right_var.type})")
            elif right_var.type[-5:] != "INT_T":
                SemanticCube.raise_type_error(f"tensor({left_var.type})", op_name, f"{right_var.type}")
            dims_res_func = matpow
        try:
            res_dims = dims_res_func(left_dims, right_dims)
        except Exception:
            raise ParhlException(f"Can not perform {op_name} in tensors with dims {left_dims} and {right_dims}")
        new_type = ctx.semantic_cube.get_type(op_name, left_var.type, right_var.type)
        if len(res_dims) == 0:
            temp_var = ctx.func_dir.new_temp(new_type)
        else:
            temp_var = ctx.func_dir.new_tens_temp(new_type, res_dims)
        ctx.add_quadruple(Quadruple(op_name, (left_var.mem_dir, left_dims), (right_var.mem_dir, right_dims), temp_var.mem_dir))
        return temp_var

    def gen_impl(self, ctx: ParseContext):
        left_var = self.left.gen(ctx)
        right_var = self.right.gen(ctx)
        op_name = symbol_to_token[self.op]
        if type(left_var) == Tensor or type(right_var) == Tensor:
            return self._gen_impl_tens(ctx, left_var, right_var, op_name)
        new_type = ctx.semantic_cube.get_type(op_name, left_var.type, right_var.type)
        temp_var = ctx.func_dir.new_temp(new_type)
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
        const_var = ctx.func_dir.get_or_new_const(self.type, self.value)
        return const_var

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
        if type(tens) != Tensor:
            raise ParhlException(f"Identifier {tens.name} is not a tensor")
        if len(tens.dims) != len(exprs):
            raise ParhlException('Not enough indices provided to tensor accessor')
        
        last = len(exprs) - 1
        zero_var = ctx.func_dir.get_or_new_const('INT_T',0)
        total_var = ctx.func_dir.new_temp('INT_T');
        ctx.add_quadruple(Quadruple('ASSIG', zero_var.mem_dir, result=total_var.mem_dir))

        for i, var in enumerate(exprs):
            if var.type != 'INT_T':
                raise ParhlException(f"Expected integer at dimension {i} but got {var.type}")
            ctx.add_quadruple(Quadruple('VERIFY', tens.dims[i]['limit'].mem_dir, result=var.mem_dir))
            new_temp = ctx.func_dir.new_temp('INT_T')
            ctx.add_quadruple(Quadruple('MULT', var.mem_dir, tens.dims[i]['m'].mem_dir, new_temp.mem_dir))
            ctx.add_quadruple(Quadruple('PLUS', new_temp.mem_dir, total_var.mem_dir, total_var.mem_dir))
            if i == last:
                # Copy vars from base addr variables
                copy = [None] * len(tens.addr_vars)
                for i, addr_var in enumerate(tens.addr_vars):
                    copy[i] = ctx.func_dir.new_temp(addr_var.type)
                    ctx.add_quadruple(Quadruple('ASSIG', addr_var.mem_dir, result=copy[i].mem_dir))
                ctx.add_quadruple(Quadruple('PLUS', total_var.mem_dir, tens.addr_vars[1].mem_dir, copy[1].mem_dir))
                func, var, _, p_type = copy[0].mem_dir
                # copy[0] is actually a pointer
                copy[0].type = tens.type
                copy[0].mem_dir = (func, var, 1, p_type)
                return copy[0]

class UnExpr(Expression):
    def __init__(self, line, op, right):
        super().__init__(line)
        self.op = op
        self.right = right

    def _gen_impl_tens(self, ctx:ParseContext, right_var, op_name):
        right_dims = [d['n'] for d in right_var.dims] if type(right_var) == Tensor else []
        new_type = ctx.semantic_cube.get_type(op_name, right_var.type)
        temp_var = ctx.func_dir.new_tens_temp(new_type, right_dims)
        ctx.add_quadruple(Quadruple(op_name, (right_var.mem_dir, right_dims), None, temp_var.mem_dir))
        return temp_var

    def gen_impl(self, ctx: ParseContext):
        right_var = self.right.gen(ctx)
        op_name = symbol_to_token[self.op]
        if type(right_var) == Tensor:
            return self._gen_impl_tens(ctx, right_var, op_name)
        new_type = ctx.semantic_cube.get_type(op_name, right_var.type)
        new_var = ctx.func_dir.new_temp(new_type)
        ctx.add_quadruple(Quadruple(op_name, right_var.mem_dir, None, new_var.mem_dir))
        return new_var
