API Docs
========

High Level API
--------------

When implementing your own benchmarks, the most important functions are directly accessible
under the ``benchmark`` package.

.. automodule:: benchmark
   :members:
   :show-inheritance:


Available benchmark definitions
-------------------------------

.. automodule:: benchmark.benchmarks
   :members:
   :show-inheritance:


Metric calculation
------------------

The interface to ``DeepLabCut`` is implemented in the ``benchmark.metrics`` package.
For displaying results and testing your submission, it is not required to have DeepLabCut installed.
However, once you intend to (re-) evaluate, make sure to have a working DeepLabCut installation.

.. automodule:: benchmark.metrics
   :members:
   :show-inheritance: