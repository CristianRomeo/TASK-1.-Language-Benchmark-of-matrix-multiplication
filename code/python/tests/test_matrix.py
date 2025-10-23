import unittest
from matrix_mul import random_matrix, zeros_matrix, multiply, equal_within

class TestMatrixMultiply(unittest.TestCase):
    def test_zeros_matrix(self):
        z = zeros_matrix(3)
        self.assertEqual(len(z), 3)
        for row in z:
            self.assertEqual(len(row), 3)
            for v in row:
                self.assertEqual(v, 0.0)

    def test_random_matrix_seed_reproducible(self):
        a = random_matrix(4, seed=123)
        b = random_matrix(4, seed=123)
        # reproducible with same seed
        self.assertTrue(equal_within(a, b, eps=0.0))

    def reference_multiply(self, A, B):
        n = len(A)
        C = [[0.0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                s = 0.0
                for k in range(n):
                    s += A[i][k] * B[k][j]
                C[i][j] = s
        return C

    def assert_matrix_equal(self, X, Y, eps=1e-9):
        self.assertTrue(equal_within(X, Y, eps=eps), "Matrices differ")

    def test_multiply_various_orders(self):
        # small deterministic test matrix (3x3)
        A = [[1.0, 2.0, 3.0],
             [4.0, 5.0, 6.0],
             [7.0, 8.0, 9.0]]
        B = [[9.0, 8.0, 7.0],
             [6.0, 5.0, 4.0],
             [3.0, 2.0, 1.0]]
        ref = self.reference_multiply(A, B)
        orders = ["ikj", "ijk", "kij", "kji", "jik", "jki"]
        for order in orders:
            with self.subTest(order=order):
                C = multiply(A, B, order=order)
                self.assert_matrix_equal(C, ref)

    def test_identity_and_zero(self):
        # identity x random == random
        n = 4
        I = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
        R = random_matrix(n, seed=42)
        C = multiply(I, R, order="ijk")
        self.assert_matrix_equal(C, R)

if __name__ == "__main__":
    unittest.main()