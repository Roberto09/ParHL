from .parhl_exceptions import ParhlException
from functools import reduce
from ..lexer import type_token_to_mem_id 

class Typed():
    def __init__(self, name, type):
        self.name = name
        self.type = type
    
    def __repr__(self):
        return f"name: {self.name}, type: {self.type}"
class Var(Typed):
    def __init__(self, name, type, mem_dir):
        super().__init__(name, type)
        self.mem_dir = mem_dir # "location" in instance memory

    def __repr__(self):
        return f"({super().__repr__()}, mem_dir: {self.mem_dir})"

    def to_ir_repr(self):
        return self.mem_dir 

class Tensor(Var):
    def __init__(self, name, type, mem_dir, addr_vars=[], dims=[]):
        super().__init__(name, type, mem_dir)
        self.dims = dims
        self.addr_vars = addr_vars

    def __repr__(self):
        return f"({super().__repr__()}, BaseAddress: {self.addr_vars}, Dims: {self.dims})"

# Tensor consts do not represent a space in memory, but points to a set 
# of mem_dirs that will be used to assign values to a tensor
class TensorConst(Typed):
    def __init__(self, name, type, mem_dirs, dims):
        super().__init__(name, type)
        self.mem_dirs = mem_dirs
        self.dims = dims

    def __repr__(self):
        return f"({super().__repr__()}, MemDirs: {self.mem_dirs}, dims: {self.dims})"

class Block():
    _ID_COUNTER = 0
    def __init__(self):
        self.vars: dict[str, Var] = {} # name : Var
        self.funcs: dict[str, Func] = {} # name : Func
        self.blocks: list[Block] = [] # Block
        self.temps: dict[str, Var] = {} # name : var
        self.consts = {
            'BOOL_T': {}, # val : var
            'INT_T': {}, # val : var
            'FLOAT_T': {}, # val : var
            'STRING_T': {}, # val : var
        } 
        self.temp_counters: dict[str, int] = { # type : next_temp/total_temps
            'INT_T': 0,
            'FLOAT_T': 0,
            'BOOL_T': 0,
            'STRING_T': 0,
            'GPU_INT_T': 0,
            'GPU_FLOAT_T': 0,
            'GPU_BOOL_T': 0,
        }
        self.cpu_var_counter = {
            'INT_T' : 0,
            'FLOAT_T' : 0,
            'STRING_T' : 0,
            'BOOL_T' : 0,
        }
        self.gpu_var_counter = {
            "GPU_INT_T" : 0,
            "GPU_FLOAT_T" : 0,
            "GPU_BOOL_T" : 0,
        }
        self.id = Block._ID_COUNTER; Block._ID_COUNTER += 1
    
    def __repr__(self):
        return f"(block, id:{self.id} vars: {list(self.vars.values())}, funcs: {list(self.funcs.values())}, blocks:{self.blocks}, consts: {self.consts})"

    # Tuple meaning (func_id, var_num, [0-1]: dereference, type)
    def get_new_memdir(self, type, offset=1):
        var_counter = self.cpu_var_counter if type[:3] != "GPU" else self.gpu_var_counter
        new_mem_dir = (self.id, var_counter[type], 0, type_token_to_mem_id[type]) # Func, var, dereference
        var_counter[type] += offset
        return new_mem_dir

    def self_to_ir_repr(self):
        consts_ir_repr = {k: [(k, v.to_ir_repr()) for k, v in v.items()] for k, v in self.consts.items()}
        return [self.cpu_var_counter, consts_ir_repr, self.gpu_var_counter] # (# vars, consts table)
    
    def to_ir_repr(self):
        curr_func = {self.id: self.self_to_ir_repr()}
        all_funcs = reduce(lambda x,y : x|y, [curr_func]+[b.to_ir_repr() for b in list(self.funcs.values()) + self.blocks])
        return all_funcs

class Func(Typed, Block):
    def __init__(self, name, type, q_index, func_var=None):
        super().__init__(name, type)
        super(Typed, self).__init__()
        self.q_index = q_index
        self.func_var=func_var

    def __repr__(self):
        return f"({super().__repr__()}, {super(Typed, self).__repr__()}, q_index: {self.q_index}, vars: {list(self.vars.values())}, funcs: {list(self.funcs.values())}, blocks:{self.blocks})"

    def set_params(self, params: list[Var]= []):
        self.params = params

    def self_to_ir_repr(self):
        return super().self_to_ir_repr() + ([self.func_var.mem_dir if self.func_var else None])

""" Function Directory abstraction
FuncDir generates a tree of Vars and Funcs which will remain available in the glob_func property.
"""
class FuncDir:
    def __init__(self):
        self.glob_func = Func('glob', 'void', 0)
        self.func_stack = [self.glob_func]

    @property
    def curr_scope(self):
        return self.func_stack[-1]
    
    @property
    def curr_func(self):
        i = -1
        while(not isinstance(self.func_stack[i], Func)):
            i -= 1
        return self.func_stack[i]

    def start_func_stack(self, name, type, q_index):
        # We only care about the most inner scope when it comes to re-definitions. 
        if name in self.curr_scope.vars or name in self.curr_scope.funcs:
            raise ParhlException(f"Id '{name}' already declared in this scope")
        if type == 'VOID': 
            nxt_func = Func(name, type, q_index)
        else: 
            # Create "temp" (so its unaccessable by programmer) var at scope with to store return values
            func_var = self.new_temp(type)
            nxt_func = Func(name, type, q_index, func_var)
        self.func_stack[-1].funcs[name] = nxt_func

        self.func_stack.append(nxt_func)

    def end_func_stack(self, name=None): 
        if name is not None:
            assert self.func_stack[-1].name == name
        self.func_stack.pop()

    def set_func_params(self, params):
        self.func_stack[-1].params = params

    def start_block_stack(self):
        nxt_block = Block()
        self.func_stack[-1].blocks.append(nxt_block)
        self.func_stack.append(nxt_block)

    def end_block_stack(self):
        self.func_stack.pop()

    def add_tensor(self, name, type, rs):
        # We only care about the most inner scope when it comes to re-definitions.
        if name in self.curr_scope.vars or name in self.curr_scope.funcs:
            raise ParhlException(f"Id '{name}' already declared in this scope")
        # Obtain location of next memory of specified type
        m0 = reduce((lambda x, y: x*y), rs)
        size = len(rs)
        dims =[{}] * size
        m = m0
        for i, r in enumerate(rs):
            m = m//r
            dims[i] = {
                'n': r, #For semantic validation
                'limit': self.get_or_new_const('INT_T', r),
                'm':  self.get_or_new_const('INT_T', m),
            }
        base_mem_dir = self.curr_scope.get_new_memdir(type, m0)
        addr_vars = [
            self.get_or_new_const("INT_T", base_mem_dir[0]),
            self.get_or_new_const("INT_T", base_mem_dir[1]),
            self.get_or_new_const("INT_T", base_mem_dir[2]),
            self.get_or_new_const("INT_T", type_token_to_mem_id[type]),
        ]
        var = Tensor(name, type, base_mem_dir, addr_vars, dims=dims)
        self.curr_scope.vars[name] = var
        return var

    def add_var(self, name, type):
        # We only care about the most inner scope when it comes to re-definitions.
        if name in self.curr_scope.vars or name in self.curr_scope.funcs:
            raise ParhlException(f"Id '{name}' already declared in this scope")
        # Obtain location of next memory of specified type
        var = Var(name, type, self.curr_scope.get_new_memdir(type))
        self.curr_scope.vars[name] = var
        return var

    def get_or_new_const(self, type, value):
        for func in reversed(self.func_stack):
            if func.consts[type].get(value) != None:
                return func.consts[type][value]
        # Was not found
        var = self.new_temp(type)
        self.func_stack[-1].consts[type][value] = var
        return var
        
    def new_temp(self, type):
        temp_var_name = type + str(self.curr_scope.temp_counters[type])
        temp_var = Var(temp_var_name, type, self.curr_scope.get_new_memdir(type))
        self.curr_scope.temps[temp_var_name] = temp_var
        self.curr_scope.temp_counters[type] += 1
        return temp_var
    
    def new_tens_const(self, type, mem_dirs, dims):
        return TensorConst("TENS_CONST", type,  mem_dirs, dims)

    def new_tens_temp(self, type, dims):
        temp_var_name = "TENS_" + type + str(self.curr_scope.temp_counters[type])
        total_vars = reduce(lambda x, y: x*y, dims)
        dims_dict = [{'n': dim} for dim in dims]
        temp_var = Tensor(temp_var_name, type, self.curr_scope.get_new_memdir(type, total_vars), dims=dims_dict)
        return temp_var

    def _find_in_ordered_scopes(self, name, attr):
        """
        This allows us to find an id (name) in an attr of the func_stack.
        This follows the idea of finding the variable prioritizing the most inner scopes.
        """ 
        for attrs in map(lambda f: getattr(f, attr), reversed(self.func_stack)):
            if name in attrs:
                return attrs[name]
        raise ParhlException(f"{attr} with id {name} not found")

    def get_var(self, name):
        return self._find_in_ordered_scopes(name, "vars")

    def get_temp(self, name):
        return self.func_stack[-1].temps[name]

    def get_func(self, name):
        return self._find_in_ordered_scopes(name, "funcs")

    def __repr__(self):
        return f"FuncDir - func_stack: {self.func_stack}"

    def to_ir_repr(self):
        funcs_dict = self.glob_func.to_ir_repr()
        return {"func_dir": [funcs_dict[i] for i in range(len(funcs_dict))]}