"""
Correctness: every vectorized.* function must match its loops.* counterpart
on random inputs.

Style: vectorized.py must contain no `for`/`while` statements at all — that's
the actual constraint from tonight's session, enforced instead of trusted.
"""

import ast
import inspect
import pathlib

import numpy as np
import pytest

from exercises import loops, vectorized

rng = np.random.default_rng(0)

n, m, d, k, batch = 5, 4, 3, 6, 2


def _pair(shape_a, shape_b):
    return rng.normal(size=shape_a), rng.normal(size=shape_b)


CASES = {
    "vector_add": _pair((n,), (n,)),
    "dot": _pair((n,), (n,)),
    "matvec": _pair((n, m), (m,)),
    "matmul": _pair((n, k), (k, m)),
    "outer": _pair((n,), (m,)),
    "pairwise_sq_dists": _pair((n, d), (m, d)),
    "row_l2_normalize": (rng.normal(size=(n, d)) + 0.1,),  # avoid zero rows
    "softmax": (rng.normal(size=(n, d)),),
    "weighted_row_average": (rng.normal(size=(n, d)), rng.uniform(0.1, 1.0, size=n)),
    "batch_matmul": _pair((batch, n, k), (batch, k, m)),
}


@pytest.mark.parametrize("name", CASES.keys())
def test_matches_loop_reference(name):
    fn_loop = getattr(loops, name)
    fn_vec = getattr(vectorized, name)
    args = CASES[name]
    expected = fn_loop(*args)
    actual = fn_vec(*args)
    np.testing.assert_allclose(actual, expected, rtol=1e-10, atol=1e-10)


def test_no_loops_over_data():
    src = pathlib.Path(inspect.getfile(vectorized)).read_text()
    tree = ast.parse(src)
    offenders = [
        f"line {node.lineno}"
        for node in ast.walk(tree)
        if isinstance(node, (ast.For, ast.While))
    ]
    assert not offenders, f"found explicit loop(s) in vectorized.py: {offenders}"
