"""Generate the benchmark table"""

import argparse

import benchmark


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--include", nargs="+", default=None, required=False)
    parser.add_argument(
        "--onerror", 
        default="return", 
        required=False, 
        choices=("ignore", "return", "raise")
    )
    parser.add_argument("--nocache", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if not args.nocache:
        results = benchmark.loadcache()
    else:
        results = None
    results = benchmark.evaluate(
        include_benchmarks=args.include,
        results=results,
        on_error=args.onerror,
    )
    if not args.nocache:
        benchmark.savecache(results)
    print(results.toframe())
