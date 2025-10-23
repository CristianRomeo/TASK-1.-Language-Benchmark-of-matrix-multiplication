# CLI benchmark: benchmark.py
# Usage:
#   python benchmark.py --n 128 --runs 5 --order ikj --seed 0 --verify
import argparse
import time
import statistics
from matrix_mul import random_matrix, multiply, equal_within

def run_once(n: int, order: str, seed: int = None):
    A = random_matrix(n, seed)
    B = random_matrix(n, None if seed is None else seed + 1)
    t0 = time.perf_counter()
    C = multiply(A, B, order=order)
    t1 = time.perf_counter()
    return (t1 - t0), A, B, C

def main():
    parser = argparse.ArgumentParser(description="Matrix multiplication benchmark (pure Python)")
    parser.add_argument("--n", type=int, default=256, help="matrix size n (n x n)")
    parser.add_argument("--runs", type=int, default=3, help="number of timed runs")
    parser.add_argument("--order", type=str, default="ikj", help="loop order: ikj, ijk, kij, kji, jik, jki")
    parser.add_argument("--seed", type=int, default=None, help="random seed (None = random)")
    parser.add_argument("--verify", action="store_true", help="verify result correctness for small n")
    args = parser.parse_args()

    # Warmup (small)
    try:
        run_once(min(32, args.n), args.order, args.seed)
    except Exception as e:
        print("Warmup failed:", e)

    times = []
    results = []
    for r in range(args.runs):
        t, A, B, C = run_once(args.n, args.order, None if args.seed is None else args.seed + r)
        times.append(t)
        results.append((A, B, C))
        print(f"Run {r+1}/{args.runs}: {t:.6f} s")

    mean = statistics.mean(times)
    median = statistics.median(times)
    stdev = statistics.stdev(times) if len(times) > 1 else 0.0

    print(f"\nSummary (n={args.n}, order={args.order}, runs={args.runs}):")
    print(f"  times: {', '.join(f'{t:.6f}' for t in times)}")
    print(f"  mean   = {mean:.6f} s")
    print(f"  median = {median:.6f} s")
    print(f"  stdev  = {stdev:.6f} s")

    if args.verify:
        if args.n > 128:
            print("  n too large for cheap verification; skipping verify.")
        else:
            A_ref, B_ref, C_ref = results[0]
            C_check = multiply(A_ref, B_ref, order="ijk")
            ok = equal_within(C_ref, C_check, eps=1e-6)
            print("  Verification:", "OK" if ok else "MISMATCH")

if __name__ == "__main__":
    main()