package matrix;

public class Benchmark {
    public static void main(String[] args) {
        int n = 256;
        int runs = 3;
        String order = "ikj";
        Long seed = null;
        boolean verify = false;

        for (int i = 0; i < args.length; ++i) {
            switch (args[i]) {
                case "--n": n = Integer.parseInt(args[++i]); break;
                case "--runs": runs = Integer.parseInt(args[++i]); break;
                case "--order": order = args[++i]; break;
                case "--seed": seed = Long.parseLong(args[++i]); break;
                case "--verify": verify = true; break;
                default:
                    System.err.println("Unknown argument: " + args[i]);
            }
        }

        // Warmup
        System.out.println("Warmup...");
        MatrixMultiplier.multiply(MatrixMultiplier.randomMatrix(Math.min(16, n), seed),
                MatrixMultiplier.randomMatrix(Math.min(16, n), seed == null ? null : seed + 1), "ikj");

        double[] times = new double[runs];

        for (int r = 0; r < runs; ++r) {
            double[][] A = MatrixMultiplier.randomMatrix(n, seed == null ? null : seed + r);
            double[][] B = MatrixMultiplier.randomMatrix(n, seed == null ? null : seed + r + 1);
            long t0 = System.nanoTime();
            double[][] C = MatrixMultiplier.multiply(A, B, order);
            long t1 = System.nanoTime();
            double secs = (t1 - t0) / 1e9;
            times[r] = secs;
            System.out.printf("Run %d/%d: %.6f s%n", r+1, runs, secs);

            if (verify && n <= 128 && r == 0) {
                double[][] cref = MatrixMultiplier.multiply(A, B, "ijk");
                System.out.println("Verify: " + MatrixMultiplier.equalWithin(C, cref, 1e-6));
            }
        }

        double sum = 0.0;
        for (double t : times) sum += t;
        double mean = sum / runs;
        System.out.printf("Mean time: %.6f s%n", mean);
    }
}