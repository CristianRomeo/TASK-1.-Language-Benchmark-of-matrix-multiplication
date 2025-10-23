// Small self-contained C++ test program using assert
// Save as: code/cpp/tests/test_matrix.cpp
#include <iostream>
#include <cmath>
#include <cassert>
#include "matrix_mul.h"

bool equalWithin(const Matrix &A, const Matrix &B, double eps = 1e-9)
{
    int n = (int)A.size();
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            if (std::fabs(A[i][j] - B[i][j]) > eps)
                return false;
    return true;
}

Matrix referenceMultiply(const Matrix &A, const Matrix &B)
{
    int n = (int)A.size();
    Matrix C = zeros_matrix(n);
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
        {
            double s = 0.0;
            for (int k = 0; k < n; ++k)
                s += A[i][k] * B[k][j];
            C[i][j] = s;
        }
    return C;
}

int main()
{
    // small deterministic matrices
    Matrix A = {{1.0, 2.0, 3.0}, {4.0, 5.0, 6.0}, {7.0, 8.0, 9.0}};
    Matrix B = {{9.0, 8.0, 7.0}, {6.0, 5.0, 4.0}, {3.0, 2.0, 1.0}};

    Matrix ref = referenceMultiply(A, B);
    Matrix C = multiply(A, B, "ikj");
    assert(equalWithin(C, ref) && "ikj failed");

    C = multiply(A, B, "ijk");
    assert(equalWithin(C, ref) && "ijk failed");

    C = multiply(A, B, "kij");
    assert(equalWithin(C, ref) && "kij failed");

    // test seeded randomness reproducibility
    Matrix R1 = random_matrix(4, 42, true);
    Matrix R2 = random_matrix(4, 42, true);
    assert(equalWithin(R1, R2, 0.0) && "random seed reproducibility failed");

    std::cout << "ALL C++ TESTS PASSED\n";
    return 0;
}