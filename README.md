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

For using all functionalities of this package and re-running evaluations, a [DeepLabCut](https://github.com/DeepLabCut/DeepLabCut/blob/master/docs/installation.md) installation is additionally required.

To re-evaluate all available models, run 

``` bash
$ python -m benchmark
```

from the repository root.

To manually build the documentation, run

``` bash
$ make deploy
```
