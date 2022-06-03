"""
Must of this functions were obtained from Pytorch's code.
We use them as helper functions in Parhl.
Original code comes from: https://github.com/pytorch/pytorch
"""

from typing import List, TypeVar, Union
number = TypeVar('number', bound=Union[int, float])

def broadcast(a: List[int], b: List[int]):
    dimsA = len(a)
    dimsB = len(b)
    ndim = max(dimsA, dimsB)
    expandedSizes: List[int] = []

    for i in range(ndim):
        offset = ndim - 1 - i
        dimA = dimsA - 1 - offset
        dimB = dimsB - 1 - offset
        sizeA = a[dimA] if (dimA >= 0) else 1
        sizeB = b[dimB] if (dimB >= 0) else 1

        if sizeA != sizeB and sizeA != 1 and sizeB != 1:
            # TODO: only assertion error is bound in C++ compilation right now
            raise AssertionError(
                "The size of tensor a {} must match the size of tensor b ("
                "{}) at non-singleton dimension {}".format(sizeA, sizeB, i)
            )

        expandedSizes.append(sizeB if sizeA == 1 else sizeA)
    return expandedSizes

def maybe_wrap_dim(dim: int, dim_post_expr: int, wrap_scalar: bool = True):
    if dim_post_expr <= 0:
        assert wrap_scalar
        dim_post_expr = 1
    min = -dim_post_expr
    max = dim_post_expr - 1
    assert not (dim < min or dim > max)
    if dim < 0:
        dim += dim_post_expr
    return dim

def unsqueeze(li: List[int], dim: int):
    dim = maybe_wrap_dim(dim, len(li) + 1)
    out = _copy(li)
    out.insert(dim, 1)
    return out

def squeeze(li: List[int], dim: int):
    out: List[int] = []
    wrapped_dim = maybe_wrap_dim(dim, len(li))
    for i in range(len(li)):
        if i == wrapped_dim:
            if li[i] != 1:
                out.append(li[i])
        else:
            out.append(li[i])
    return out

def dot(self: List[int], tensor: List[int]):
    assert len(self) == 1 and len(tensor) == 1
    assert self[0] == tensor[0]
    out: List[int] = []
    return out

def matmul(tensor1: List[int], tensor2: List[int]):
    dim_tensor1 = len(tensor1)
    dim_tensor2 = len(tensor2)
    if dim_tensor1 == 1 and dim_tensor2 == 1:
        return dot(tensor1, tensor2)
    elif dim_tensor1 == 2 and dim_tensor2 == 1:
        return mv(tensor1, tensor2)
    elif dim_tensor1 == 1 and dim_tensor2 == 2:
        return squeeze(mm(unsqueeze(tensor1, 0), tensor2), 0)
    elif dim_tensor1 == 2 and dim_tensor2 == 2:
        return mm(tensor1, tensor2)
    elif dim_tensor1 >= 1 and dim_tensor2 >= 1:
        # We are multiplying b1 x n x m1 by x2 x m2 x p (where b1 can be a list);
        # we track m1 vs m2 separately even though they must match for nicer error messages
        n = tensor1[-2] if dim_tensor1 > 1 else 1
        m1 = tensor1[-1]
        batch_tensor1: List[int] = []
        # TODO: handling of slice
        for i in range(dim_tensor1 - 2):
            batch_tensor1.append(tensor1[i])
        m2 = tensor2[-1] if dim_tensor2 > 1 else 1
        p = tensor2[-1]
        batch_tensor2: List[int] = []
        # TODO: handling of slice
        for i in range(dim_tensor2 - 2):
            batch_tensor2.append(tensor2[i])

        # expand the batch portion (i.e. cut off matrix dimensions and expand rest)
        expand_batch_portion = broadcast(batch_tensor1, batch_tensor2)

        # todo: copy ?
        output_shape = expand_batch_portion
        if dim_tensor1 > 1:
            output_shape.append(n)

        if dim_tensor2 > 1:
            output_shape.append(p)

        return output_shape
    else:
        assert False, "both  arguments to matmul need to be at least 1D"

def matpow(tensor1: List[int], _: List[int]):
    return matmul(tensor1, tensor1)

def mv(self: List[int], vec: List[int]):
    assert len(self) == 2 and len(vec) == 1
    assert self[1] == vec[0]
    # TODO: return self
    return [self[0]]

def mm(self: List[int], mat2: List[int]):
    assert len(self) == 2, "self must be a matrix"
    assert len(mat2) == 2, "mat2 must be a matrix"

    assert self[1] == mat2[0]
    return [self[0], mat2[1]]

def unsqueeze(li: List[int], dim: int):
    dim = maybe_wrap_dim(dim, len(li) + 1)
    out = _copy(li)
    out.insert(dim, 1)
    return out
