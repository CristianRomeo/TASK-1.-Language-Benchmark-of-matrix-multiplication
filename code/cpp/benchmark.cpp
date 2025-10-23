
#include <iostream>
#include <chrono>
#include <vector>
#include <numeric>
#include <cmath>
#include "matrix_mul.h"

int main(int argc, char **argv)
{
    int n = 256;
    int runs = 3;
    std::string order = "ikj";
    unsigned long long seed = 0;
    bool seeded = false;
    bool verify = false;

    for (int i = 1; i < argc; ++i)
    {
        std::string a = argv[i];
        if (a == "--n" && i + 1 < argc)
            n = std::atoi(argv[++i]);
        else if (a == "--runs" && i + 1 < argc)
            runs = std::atoi(argv[++i]);
        else if (a == "--order" && i + 1 < argc)
            order = argv[++i];
        else if (a == "--seed" && i + 1 < argc)
        {
            seed = static_cast<unsigned long long>(std::atoll(argv[++i]));
            seeded = true;
        }
        else if (a == "--verify")
            verify = true;
    }

    // Warmup
    random_matrix(std::min(16, n), seeded ? seed : 0, seeded);

    std::vector<double> times;
    for (int r = 0; r < runs; ++r)
    {
        Matrix A = random_matrix(n, seeded ? seed + r : 0, seeded);
        Matrix B = random_matrix(n, seeded ? seed + r + 1 : 0, seeded);

        auto t0 = std::chrono::high_resolution_clock::now();
        Matrix C = multiply(A, B, order);
        auto t1 = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double> diff = t1 - t0;
        double secs = diff.count();
        times.push_back(secs);
        std::cout << "Run " << (r + 1) << "/" << runs << ": " << secs << " s\n";

        if (verify && n <= 128 && r == 0)
        {
            Matrix Cref = multiply(A, B, "ijk");
            bool ok = true;
            for (int i = 0; i < n && ok; ++i)
                for (int j = 0; j < n; ++j)
                    if (std::fabs(C[i][j] - Cref[i][j]) > 1e-6)
                    {
                        ok = false;
                        break;
                    }
            std::cout << "Verify: " << (ok ? "OK" : "MISMATCH") << "\n";
        }
    }

    double sum = std::accumulate(times.begin(), times.end(), 0.0);
    double mean = sum / times.size();
    std::cout << "Mean time: " << mean << " s\n";
    return 0;
}