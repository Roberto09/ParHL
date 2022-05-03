
import pytest
from ..structs.semantic_cube import SemanticCube
from uuid import uuid4 as gen_id

@pytest.fixture(params = [
    ("OR", "BOOL_T", "BOOL_T", "BOOL_T"), # boolean binary
    ("NOT", "GPU_BOOL_T", "GPU_BOOL_T"), # boolean unary
    ("MULT", "INT_T", "GPU_FLOAT_T", "GPU_FLOAT_T"), # arithmetic unary
    ("PLUS", "GPU_FLOAT_T", "GPU_FLOAT_T"), # arithmetic unary
    ("MOD", "GPU_INT_T", "GPU_INT_T", "GPU_INT_T"), # mod binary
    ("EQ", "INT_T", "FLOAT_T", "BOOL_T"), # eq_noteq binary
    ("ASSIG", "INT_T", "FLOAT_T", "INT_T"), # assig binary
    ("GEQT", "FLOAT_T", "GPU_INT_T", "GPU_BOOL_T") # arithmetic comp binary
])
def valid_operation(request):
    return request.param

def test_valid_operations(valid_operation):
    semantic_cube = SemanticCube()
    operation = valid_operation
    if len(operation) == 4:
        op, t_arg1, t_arg2, t_res = operation
        assert semantic_cube.get_type(op, t_arg1, t_arg2) == t_res
    elif len(operation) == 3:
        op, t_arg1, t_res = operation
        assert semantic_cube.get_type(op, t_arg1) == t_res
    else:
        raise Exception("too much or too few symbols in operation")


@pytest.fixture(params = [
    ("OR", "INT_T", "BOOL_T"), # boolean binary
    ("NOT", "FLOAT_T"), # boolean unary
    ("MULT", "BOOL_T", "GPU_FLOAT_T"), # arithmetic unary
    ("PLUS", "BOOL_T"), # arithmetic unary
    ("MOD", "FLOAT_T", "GPU_INT_T"), # mod binary
    ("MOD", "INT_T"), # mod unary
    ("ASSIG", "INT_T", "BOOL_T"), # assig binary
    ("ASSIG", "BOOL_T",), # assig unary
    ("GEQT", "FLOAT_T", "GPU_BOOL_T"), # arithmetic comp binary
    ("GET", "FLOAT_T"), # arithmetic comp unary
])
def invalid_operation(request):
    return request.param

def test_invalid_operations(invalid_operation):
    semantic_cube = SemanticCube()
    operation = invalid_operation
    if len(operation) == 3:
        op, t_arg1, t_arg2 = operation
        with pytest.raises(Exception):
            semantic_cube.get_type(op, t_arg1, t_arg2)
    elif len(operation) == 2:
        op, t_arg1 = operation
        with pytest.raises(Exception):
            semantic_cube.get_type(op, t_arg1)
    else:
        raise Exception("too much or too few symbols in operation")