"""
Rewrite every function in loops.py here using broadcasting, reductions,
and einsum. No `for`/`while` over the data — if you reach for an index
into an axis, that's the signal to stop and find the broadcast shape
instead.

Run `pytest` to check correctness against loops.py.
Run `ruff check .` for style.

Hints are in the docstrings. Delete them once you don't need them.
"""

import numpy as np


def vector_add(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    raise NotImplementedError


def dot(a: np.ndarray, b: np.ndarray) -> float:
    # np.dot / the @ operator, or (a * b).sum()
    raise NotImplementedError


def matvec(A: np.ndarray, x: np.ndarray) -> np.ndarray:
    # A @ x — but also try it as a broadcast-and-reduce to feel why @ exists
    raise NotImplementedError


def matmul(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    # A @ B, or np.einsum("ik,kj->ij", A, B)
    raise NotImplementedError


def outer(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    # reshape a to a column and let broadcasting do the rest
    raise NotImplementedError


def pairwise_sq_dists(X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    """
    (n,m) result from (n,d) and (m,d) inputs.
    ||x - y||^2 = ||x||^2 + ||y||^2 - 2 x.y — expand it and broadcast the
    three pieces against each other with shapes (n,1), (1,m), (n,m).
    """
    raise NotImplementedError


def row_l2_normalize(X: np.ndarray) -> np.ndarray:
    # norms per row, keepdims=True so it broadcasts back against X
    raise NotImplementedError


def softmax(X: np.ndarray) -> np.ndarray:
    # same keepdims trick, applied twice (max-subtract, then sum-divide)
    raise NotImplementedError


def weighted_row_average(X: np.ndarray, w: np.ndarray) -> np.ndarray:
    # np.einsum("i,ij->j", w, X) / w.sum(), or w @ X / w.sum()
    raise NotImplementedError


def batch_matmul(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    # np.einsum("bik,bkj->bij", A, B), or A @ B (matmul batches automatically)
    raise NotImplementedError
