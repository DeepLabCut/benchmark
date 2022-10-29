DeepLabCut Benchmark
====================

[`[[ benchmark.deeplabcut.org ]]` ](https://benchmark.deeplabcut.org)

Welcome to the DeepLabCut benchmark!
This repo hosts all submitted results, which are available at [benchmark.deeplabcut.org](https://benchmark.deeplabcut.org).
If you are interested in submitting to the benchmark, please find detailed instructions on [benchmark.deeplabcut.org/submission](https://benchmark.deeplabcut.org/submission).


Quickstart for developers
-------------------------

The mandatory requirements for *building the benchmark page* can be installed via

``` bash
$ pip install -r requirements.txt
```

The (non-public) ground truth data needs to be present in `data/`. Check that this is the case by running

``` bash
find data -type f
benchmark/data/CollectedData_Mackenzie.h5
benchmark/data/CollectedData_Daniel.h5
benchmark/data/CollectedData_Valentina.h5
benchmark/data/CollectedData_Mostafizur.h5
```

For using all functionalities of this package and re-running evaluations, a [DeepLabCut](https://github.com/DeepLabCut/DeepLabCut/blob/master/docs/installation.md) installation is additionally required.

Check that the package works as expected by running

``` bash
python -m pytest tests
```

which should finish without errors or warnings.

To re-evaluate all available models, run 

``` bash
$ python -m benchmark
```

or, if you want to run in debugging mode,

``` bash
python -m benchmark --nocache --onerror raise
```

from the repository root. 

To manually build the documentation, run

``` bash
$ make deploy
```
