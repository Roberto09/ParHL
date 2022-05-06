class Typed():
    def __init__(self, name, type):
        self.name = name
        self.type = type

class Var(Typed):
    def __init__(self, name, type):
        super().__init__(name, type)

class Func(Typed):
    def __init__(self, name, type):
        super().__init__(name, type)
        self.vars = {} # name : Var
        self.funcs = {} # name : Func


""" Function Directory abstraction
FuncDir generates a tree of Vars and Funcs which will remain available in the glob_func property.
"""
class FuncDir:
    def __init__(self):
        self.glob_func = Func('glob', 'void')
        self.func_stack = [self.glob_func]

    def start_func_stack(self, name, type):
        # We only care about the most inner scope when it comes to re-definitions. 
        assert (name not in self.func_stack[-1].vars) and (name not in self.func_stack[-1].funcs)
        nxt_func = Func(name, type)
        self.func_stack[-1].funcs[name] = nxt_func
        self.func_stack.append(nxt_func)

    def end_func_stack(self, name=None): 
        if name is not None:
            assert self.func_stack[-1].name == name
        self.func_stack.pop()

    def add_var(self, name, type):
        # We only care about the most inner scope when it comes to re-definitions.
        assert name not in self.func_stack[-1].vars and name not in self.func_stack[-1].funcs
        var = Var(name, type)
        self.func_stack[-1].vars[name] = var

    def _find_in_ordered_scopes(self, name, attr):
        """
        This allows us to find an id (name) in an attr of the func_stack.
        This follows the idea of finding the variable prioritizing the most inner scopes.
        """
        for attrs in map(lambda f: getattr(f, attr), reversed(self.func_stack)):
            if name in attrs:
                return attrs[name]
        raise Exception(f"{attr} with id {name} not found")

    def get_var(self, name):
        return self._find_in_ordered_scopes(name, "vars")
    
    def get_func(self, name):
        return self._find_in_ordered_scopes(name, "funcs")

    
