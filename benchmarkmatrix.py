# This is a standalone Python benchmark script.
# It uses the robust benchmark harness from benchmark.py
# and the *exact* multiplication logic from matrix.py.
#
# Usage:
#   python benchmark_standalone.py --n 128 --runs 5 --seed 0 --verify

import argparse
import time
import statistics
import random
from typing import List, Optional

# --- Matrix logic functions ---

Matrix = List[List[float]]

def random_matrix(n: int, seed: Optional[int] = None) -> Matrix:
    """Return an n x n matrix with random floats in [0,1)."""
    if seed is not None:
        rnd = random.Random(seed)
        return [[rnd.random() for _ in range(n)] for _ in range(n)]
    return [[random.random() for _ in range(n)] for _ in range(n)]

def zeros_matrix(n: int) -> Matrix:
    """Returns an n x n matrix of zeros."""
    return [[0 for _ in range(n)] for _ in range(n)]

def multiply(A: Matrix, B: Matrix) -> Matrix:
    """
    Multiply square matrices A and B using the
    EXACT (and buggy) logic from your original 'matrix.py'.
    Note the 'B[k][k]' instead of 'B[k][j]'.
    """
    n = len(A)
    C = zeros_matrix(n)

    for i in range(n):
        for j in range(n):
            for k in range(n):
                # The bug from your original matrix.py is replicated here:
                C[i][j] += A[i][k] * B[k][k] 
    
    return C

def equal_within(A: Matrix, B: Matrix, eps: float = 1e-9) -> bool:
    """Checks if two matrices are equal within a small tolerance."""
    n = len(A)
    for i in range(n):
        for j in range(n):
            if abs(A[i][j] - B[i][j]) > eps:
                return False
    return True

# --- Benchmark harness logic (from benchmark.py) ---

def run_once(n: int, seed: int = None):
    """
    Creates two random matrices, multiplies them, and returns the time taken.
    """
    # Use a seed for A and seed + 1 for B for reproducibility
    A = random_matrix(n, seed)
    B = random_matrix(n, None if seed is None else seed + 1)
    
    t0 = time.perf_counter()
    C = multiply(A, B) # Call the multiplication function
    t1 = time.perf_counter()
    
    return (t1 - t0), A, B, C

def main():
    """
    Main benchmark function. Parses arguments, runs benchmarks, and prints stats.
    """
    parser = argparse.ArgumentParser(description="Matrix multiplication benchmark (pure Python, from matrix.py logic)")
    parser.add_argument("--n", type=int, default=256, help="matrix size n (n x n)")
    parser.add_argument("--runs", type=int, default=100, help="number of timed runs")
    parser.add_argument("--seed", type=int, default=None, help="random seed (None = random)")
    parser.add_argument("--verify", action="store_true", help="verify result correctness")
    args = parser.parse_args()

    print(f"Running benchmark (logic from matrix.py): n={args.n}, runs={args.runs}")

    # Warmup (small run to let Python 'warm up')
    try:
        run_once(min(32, args.n), args.seed)
    except Exception as e:
        print("Warmup failed:", e)

    times = []
    results = []
    for r in range(args.runs):
        # Use a different seed for each run if a base seed is provided
        run_seed = None if args.seed is None else args.seed + r
        
        t, A, B, C = run_once(args.n, run_seed)
        
        times.append(t)
        results.append((A, B, C)) # Store results for verification
        print(f"Run {r+1}/{args.runs}: {t:.6f} s")

    # Calculate statistics
    mean = statistics.mean(times)
    median = statistics.median(times)
    stdev = statistics.stdev(times) if len(times) > 1 else 0.0

    print(f"\nSummary (n={args.n}, runs={args.runs}):")
    print(f"  times: {', '.join(f'{t:.6f}' for t in times)}")
    print(f"  mean   = {mean:.6f} s")
    print(f"  median = {median:.6f} s")
    print(f"  stdev  = {stdev:.6f} s")

    # Verification step
    if args.verify:
        if args.n > 128:
            print("  n too large for cheap verification; skipping verify.")
        else:
            print("  Verifying result...")
            A_ref, B_ref, C_ref = results[0] # Get results from first run
            
            # Run the *correct* 'ijk' multiplication for verification
            C_check_correct = zeros_matrix(args.n)
            for i in range(args.n):
                for j in range(args.n):
                    s = 0.0
                    for k in range(args.n):
                        s += A_ref[i][k] * B_ref[k][j] # Correct logic
                    C_check_correct[i][j] = s
            
            ok = equal_within(C_ref, C_check_correct, eps=1e-6)
            print(f"  Verification against *correct* 'ijk': {'OK' if ok else 'MISMATCH'}")
            if not ok:
                print("  NOTE: Mismatch is expected because this script benchmarks the B[k][k] bug from matrix.py.")


if __name__ == "__main__":
    main()