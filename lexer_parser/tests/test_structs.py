import pytest
from ..lexer import ParhlLexer
from ..structs.var_dir import FuncDir
from uuid import uuid4 as gen_id

def assert_typed_equal(typed, name, type):
    assert typed.name == name and typed.type == type 

def test_vars():
    func_dir = FuncDir()
    name1, type1 = "new_var", "int"
    name2, type2 = "other_var", "string"
    func_dir.add_var(name1, type1)
    func_dir.add_var(name2, type2)
    assert_typed_equal(func_dir.get_var(name1), name1, type1)
    assert_typed_equal(func_dir.get_var(name2), name2, type2)
    with pytest.raises(Exception):
        func_dir.add_var(name1, "float")
    with pytest.raises(Exception):
        func_dir.get_var("not exist")

def test_funcs():
    func_dir = FuncDir()
    name1, type1 = "new_func", "int"
    name2, type2 = "other_func", "string"
    func_dir.start_func_stack(name1, type1)
    func_dir.end_func_stack(name1)
    func_dir.start_func_stack(name2, type2)
    func_dir.end_func_stack(name2)
    assert_typed_equal(func_dir.get_func(name1), name1, type1)
    assert_typed_equal(func_dir.get_func(name2), name2, type2)
    with pytest.raises(Exception):
        func_dir.start_func_stack(name1, "float")
    with pytest.raises(Exception):
        func_dir.get_func("not exist")

def add_n_vars(func_dir, n):
    names_types = [(gen_id(), gen_id()) for i in range(n)]
    for name, type in names_types:
        func_dir.add_var(name, type)
    return names_types

def add_func_with_n_vars(func_dir, n):
    func_name, func_type = gen_id(), gen_id()
    func_dir.start_func_stack(func_name, func_type)
    names_types = add_n_vars(func_dir, n)
    return func_name, func_type, names_types


def test_combined():
    """
    f1() { # aka glob
        f2() {
            ...
        }
        f3() {
            ...
            f4() {
                ...
            }
        }
    }
    """
    func_dir = FuncDir()
    num_vars = 5
    
    # func_1 is global
    f1vs = add_n_vars(func_dir, num_vars)
    
    f2n, f2t, f2vs = add_func_with_n_vars(func_dir, num_vars)
    func_dir.end_func_stack(f2n)

    f3n, f3t, f3vs = add_func_with_n_vars(func_dir, num_vars)

    f4n, f4t, f4vs = add_func_with_n_vars(func_dir, num_vars)

    for n, t in f1vs + f3vs + f4vs:
        assert_typed_equal(func_dir.get_var(n), n, t)
    for n, _ in f2vs:
        with pytest.raises(Exception):
            func_dir.get_var(n)

    func_dir.end_func_stack(f4n)
    func_dir.end_func_stack(f3n)

    assert_typed_equal(func_dir.get_func(f2n), f2n, f2t)
    assert_typed_equal(func_dir.get_func(f3n), f3n, f3t)