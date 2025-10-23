# Production code: matrix_mul.py
# Pure-Python matrix generation and multiplication functions (importable).
from typing import List, Optional
import random

Matrix = List[List[float]]

def random_matrix(n: int, seed: Optional[int] = None) -> Matrix:
    """Return an n x n matrix with random floats in [0,1)."""
    if seed is not None:
        rnd = random.Random(seed)
        return [[rnd.random() for _ in range(n)] for _ in range(n)]
    return [[random.random() for _ in range(n)] for _ in range(n)]

def zeros_matrix(n: int) -> Matrix:
    return [[0.0 for _ in range(n)] for _ in range(n)]

def multiply(A: Matrix, B: Matrix, order: str = "ikj") -> Matrix:
    """
    Multiply square matrices A and B and return result C.
    order: one of 'ijk', 'ikj', 'kij', 'kji', 'jik', 'jki'
    """
    n = len(A)
    C = zeros_matrix(n)

    if order == "ikj":
        for i in range(n):
            Ai = A[i]
            Ci = C[i]
            for k in range(n):
                aik = Ai[k]
                Bk = B[k]
                for j in range(n):
                    Ci[j] += aik * Bk[j]
    elif order == "ijk":
        for i in range(n):
            Ci = C[i]
            for j in range(n):
                s = 0.0
                for k in range(n):
                    s += A[i][k] * B[k][j]
                Ci[j] = s
    elif order == "kij":
        for k in range(n):
            Bk = B[k]
            for i in range(n):
                aik = A[i][k]
                Ci = C[i]
                for j in range(n):
                    Ci[j] += aik * Bk[j]
    elif order == "kji":
        for k in range(n):
            Bk = B[k]
            for j in range(n):
                bkj = Bk[j]
                for i in range(n):
                    C[i][j] += A[i][k] * bkj
    elif order == "jik":
        for j in range(n):
            for i in range(n):
                s = 0.0
                for k in range(n):
                    s += A[i][k] * B[k][j]
                C[i][j] = s
    elif order == "jki":
        for j in range(n):
            for k in range(n):
                bkj = B[k][j]
                for i in range(n):
                    C[i][j] += A[i][k] * bkj
    else:
        raise ValueError(f"Unknown order: {order}")

    return C

def equal_within(A: Matrix, B: Matrix, eps: float = 1e-9) -> bool:
    n = len(A)
    for i in range(n):
        for j in range(n):
            if abs(A[i][j] - B[i][j]) > eps:
                return False
    return True