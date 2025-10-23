#ifndef MATRIX_MUL_H
#define MATRIX_MUL_H

#include <vector>
#include <random>
#include <string>
#include <stdexcept>

using Matrix = std::vector<std::vector<double>>;

inline Matrix random_matrix(int n, unsigned long long seed = 0, bool seeded = false)
{
    std::mt19937_64 rng(seeded ? seed : std::random_device{}());
    std::uniform_real_distribution<double> dist(0.0, 1.0);
    Matrix M(n, std::vector<double>(n));
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            M[i][j] = dist(rng);
    return M;
}

inline Matrix zeros_matrix(int n)
{
    return Matrix(n, std::vector<double>(n, 0.0));
}

inline Matrix multiply(const Matrix &A, const Matrix &B, const std::string &order = "ikj")
{
    int n = static_cast<int>(A.size());
    Matrix C = zeros_matrix(n);

    if (order == "ikj")
    {
        for (int i = 0; i < n; ++i)
        {
            const auto &Ai = A[i];
            auto &Ci = C[i];
            for (int k = 0; k < n; ++k)
            {
                double aik = Ai[k];
                const auto &Bk = B[k];
                for (int j = 0; j < n; ++j)
                {
                    Ci[j] += aik * Bk[j];
                }
            }
        }
    }
    else if (order == "ijk")
    {
        for (int i = 0; i < n; ++i)
        {
            for (int j = 0; j < n; ++j)
            {
                double s = 0.0;
                for (int k = 0; k < n; ++k)
                    s += A[i][k] * B[k][j];
                C[i][j] = s;
            }
        }
    }
    else if (order == "kij")
    {
        for (int k = 0; k < n; ++k)
        {
            const auto &Bk = B[k];
            for (int i = 0; i < n; ++i)
            {
                double aik = A[i][k];
                auto &Ci = C[i];
                for (int j = 0; j < n; ++j)
                    Ci[j] += aik * Bk[j];
            }
        }
    }
    else
    {
        throw std::runtime_error("Unknown order: " + order);
    }
    return C;
}

#endif // MATRIX_MUL_H