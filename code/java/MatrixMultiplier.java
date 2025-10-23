package matrix;

import java.util.Random;

/**
 * Production code: matrix multiplier utilities.
 */
public class MatrixMultiplier {
    public static double[][] randomMatrix(int n, Long seed) {
        Random rnd = seed == null ? new Random() : new Random(seed);
        double[][] M = new double[n][n];
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                M[i][j] = rnd.nextDouble();
            }
        }
        return M;
    }

    public static double[][] zerosMatrix(int n) {
        return new double[n][n];
    }

    public static double[][] multiply(double[][] A, double[][] B, String order) {
        int n = A.length;
        double[][] C = zerosMatrix(n);

        switch (order) {
            case "ikj":
                for (int i = 0; i < n; ++i) {
                    double[] Ai = A[i];
                    double[] Ci = C[i];
                    for (int k = 0; k < n; ++k) {
                        double aik = Ai[k];
                        double[] Bk = B[k];
                        for (int j = 0; j < n; ++j) {
                            Ci[j] += aik * Bk[j];
                        }
                    }
                }
                break;
            case "ijk":
                for (int i = 0; i < n; ++i) {
                    for (int j = 0; j < n; ++j) {
                        double s = 0.0;
                        for (int k = 0; k < n; ++k) {
                            s += A[i][k] * B[k][j];
                        }
                        C[i][j] = s;
                    }
                }
                break;
            case "kij":
                for (int k = 0; k < n; ++k) {
                    double[] Bk = B[k];
                    for (int i = 0; i < n; ++i) {
                        double aik = A[i][k];
                        double[] Ci = C[i];
                        for (int j = 0; j < n; ++j) {
                            Ci[j] += aik * Bk[j];
                        }
                    }
                }
                break;
            default:
                throw new IllegalArgumentException("Unknown order: " + order);
        }
        return C;
    }

    public static boolean equalWithin(double[][] A, double[][] B, double eps) {
        int n = A.length;
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < n; ++j) {
                if (Math.abs(A[i][j] - B[i][j]) > eps) return false;
            }
        }
        return true;
    }
}