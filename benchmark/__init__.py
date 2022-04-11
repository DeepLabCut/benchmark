__version__ = "0.0.1a"

import json
import os
from typing import Container

from benchmark.base import Benchmark, Result, ResultCollection

DATA_ROOT = os.path.join(os.path.dirname(__file__), "data")
CACHE = os.path.join(os.path.dirname(__file__), ".results")

__registry = []


def register(cls):
    """Add a benchmark to the list of evaluations to run.

    Apply this function as a decorator to a class. Note that the
    class needs to be a subclass of the ``benchmark.base.Benchmark``
    base class.

    In most situations, it will be a subclass of one of the pre-defined
    benchmarks in ``benchmark.benchmarks``.

    Throws:
        ``ValueError`` if the decorator is applied to a class that is
        not a subclass of ``benchmark.base.Benchmark``.
    """
    if not issubclass(cls, Benchmark):
        raise ValueError(
            f"Can only register subclasses of {type(Benchmark)}, " f"but got {cls}."
        )
    __registry.append(cls)


def evaluate(
    include_benchmarks: Container[str] = None,
    results: ResultCollection = None,
    on_error="return",
) -> ResultCollection:
    """Run evaluation for all benchmarks and methods.

    Note that in order for your custom benchmark to be included during
    evaluation, the following conditions need to be met:

        - The benchmark subclassed one of the benchmark definitions in
          in ``benchmark.benchmarks``
        - The benchmark is registered by applying the ``@benchmark.register``
          decorator to the class
        - The benchmark was imported. This is done automatically for all
          benchmarks that are defined in submodules or subpackages of the
          ``benchmark.submissions`` module. For all other locations, make
          sure to manually import the packages **before** calling the
          ``evaluate()`` function.

    Args:
        include_benchmarks:
            If ``None``, run all benchmarks that were discovered. If a container
            is passed, only include methods that were defined on benchmarks with
            the specified names. E.g., ``include_benchmarks = ["trimouse"]`` would
            only evaluate methods of the trimouse benchmark dataset.
        on_error:
            see documentation in ``benchmark.base.Benchmark.evaluate()``

    Returns:
        A collection of all results, which can be printed or exported to
        ``pd.DataFrame`` or ``json`` file formats.
    """
    if results is None:
        results = ResultCollection()
    for benchmark_cls in __registry:
        if include_benchmarks is not None:
            if benchmark_cls.name not in include_benchmarks:
                continue
        benchmark = benchmark_cls()
        for name in benchmark.names():
            if Result(method_name=name, benchmark_name=benchmark_cls.name) in results:
                continue
            else:
                result = benchmark.evaluate(name, on_error=on_error)
                results.add(result)
    return results


def get_filepath(basename: str):
    return os.path.join(DATA_ROOT, basename)


def savecache(results: ResultCollection):
    with open(CACHE, "w") as fh:
        json.dump(results.todicts(), fh, indent=2)


def loadcache() -> ResultCollection:
    if not os.path.exists(CACHE):
        return ResultCollection()
    with open(CACHE, "r") as fh:
        try:
            data = json.load(fh)
        except json.decoder.JSONDecodeError:
            return ResultCollection()
    return ResultCollection.fromdicts(data)


"""TODO(stes): Refactor __registry or remove this function
def from_name(name: str, *args, **kwargs):
    if name not in __registry:
        raise ValueError(
            f"Benchmark with name {name} is not defined. "
            f"Valid benchmark names: {tuple(__registry.keys())}."
        )
    cls = __registry[name]
    return cls(*args, **kwargs)
"""

# Submissions will use the get_filepath and register functions defined above,
# hence to avoid circular imports, import statements needs to be moved to end
# of __init__.
import benchmark.submissions
