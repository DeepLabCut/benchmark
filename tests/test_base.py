import benchmark
import benchmark.base

def test_result():
    result = benchmark.base.Result("foo", "bar")
    restored = result.fromdict(result.todict())
    assert restored == result
    assert result.benchmark_version == benchmark.__version__

def test_collection():

    collection = benchmark.base.ResultCollection()

    result1 = benchmark.base.Result("foo", "bar", root_mean_squared_error=42)
    result2 = benchmark.base.Result("foo", "baz")
    result_dup = benchmark.base.Result("foo", "bar", root_mean_squared_error=43)

    assert len(collection) == 0
    collection.add(result1)
    assert len(collection) == 1
    collection.add(result2)
    assert len(collection) == 2
    assert result1 in collection
    assert result2 in collection
    assert result_dup in collection

    restored = collection.fromdicts(collection.todicts())

    assert restored == collection