// Simple self-contained Java test runner (no external test framework)
// Save under: code/java/tests/MatrixMultiplierTest.java
// Compile and run as described below.
package matrix.tests;

import matrix.MatrixMultiplier;

public class MatrixMultiplierTest {
    static boolean equalWithin(double[][] A, double[][] B, double eps) {
        int n = A.length;
        for (int i = 0; i < n; ++i)
            for (int j = 0; j < n; ++j)
                if (Math.abs(A[i][j] - B[i][j]) > eps) return false;
        return true;
    }

    static double[][] referenceMultiply(double[][] A, double[][] B) {
        int n = A.length;
        double[][] C = new double[n][n];
        for (int i = 0; i < n; ++i)
            for (int j = 0; j < n; ++j) {
                double s = 0.0;
                for (int k = 0; k < n; ++k) s += A[i][k] * B[k][j];
                C[i][j] = s;
            }
        return C;
    }

    static void assertMatrixEqual(double[][] X, double[][] Y, String msg) {
        if (!equalWithin(X, Y, 1e-9)) {
            System.err.println("ASSERT FAIL: " + msg);
            System.exit(2);
        }
    }

    public static void main(String[] args) {
        double[][] A = {
            {1.0,2.0,3.0},
            {4.0,5.0,6.0},
            {7.0,8.0,9.0}
        };
        double[][] B = {
            {9.0,8.0,7.0},
            {6.0,5.0,4.0},
            {3.0,2.0,1.0}
        };
        double[][] ref = referenceMultiply(A, B);
        String[] orders = {"ikj","ijk","kij"};

        for (String order : orders) {
            double[][] C = MatrixMultiplier.multiply(A, B, order);
            assertMatrixEqual(C, ref, "order=" + order);
        }

        // Test RNG reproducibility
        double[][] R1 = MatrixMultiplier.randomMatrix(4, 123L);
        double[][] R2 = MatrixMultiplier.randomMatrix(4, 123L);
        if (!equalWithin(R1, R2, 0.0)) {
            System.err.println("RNG reproducibility failed");
            System.exit(3);
        }

        System.out.println("ALL JAVA TESTS PASSED");
        System.exit(0);
    }
}