How to submit your models to the benchmark
==========================================

Overview
--------

Submission to the benchmark is simple and framework-agnostic:

   - Select one or more datasets from :doc:
   - Train a pose estimation model. The benchmark is framework agnostic, and you can
     use any codebase of your choice.
   - Your model should export predictions for all images in the **test datasets**.
     Package these predictions in a format of your choice
   - Implement a loader function using the ``benchmark`` API, and contribute your code
     along with your predictions as a pull request to the benchmark.


Preparing your submission
-------------------------

Your submission will be a pull request directly to the ``benchmark'' package.
The PR should have the following structure:

.. code::

   benchmark/
      submissions/
         <your-package-name>/
            __init__.py    # Empty file
            README.md      # Describe your contribution here
            LICENSE        # The license that applies to your contribution
            <file 1>.py    # Python modules needed for processing your
            ...            #  submission data
            data/
               <data>      # data files containing the predictions of your
               ...         # model. You can use any format.


The ``data`` sub-folder can contain the raw outputs from the pose estimation framework
of your choice. During evaluation, we crawl all ``*.py`` files in your submitted package 
for method definitions.

These looks as follows:

.. code:: python

   import benchmark
   from benchmark.benchmarks import TriMouseBenchmark

   @benchmark.register
   class YourSubmissionToTriMouse(DLCBenchMixin, TriMouseBenchmark):

      code = "link/to/your/code.git"

      def names(self):
         """An iterable of model names to evaluate."""
         return "FooNet-42", "BarNet-73"

      def get_predictions(self, name):
         """This function will receive one of the names returned by the 
         names() function, and should return a dictionary containing your 
         predictions.
         """
         return {
            "path/to/image.png" : (
               # animal 1
               {
                  "pose": {
                    "snout" : (12, 17),
                    "leftear" : (15, 13),
                    ...
                  },
                  "score": 0.9172,
               },
               # animal 2
               {
                  "pose": {
                     "snout" : (27, 138),
                     "leftear" : (23, 142),
                     ...
                  },
                  "score": 0.8534,
               },
            ),
            ...
         }

For more advanced use-cases, please refer to our :doc:`api`.


Testing your submission
-----------------------

You can test your submission by running

.. code:: bash

   $ python -m benchmark

from the repository root directory, which will generate a table with all 
available results. If your own submission does not appear, make sure that you
added your evaluation class to the benchmark with the ``@benchmark.register``
decorator.


Submission
----------

To submit, open a pull request directly in the benchmark repository:
https://github.com/DeepLabCut/benchmark/pulls


Troubleshooting
---------------

If you encounter difficulties during preparation of your submission that are not
covered in this tutorial, please open an issue in the benchmark repository:
https://github.com/DeepLabCut/benchmark_internal/issues