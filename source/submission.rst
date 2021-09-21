How to submit your models to the benchmark
==========================================

.. note::

   The ``deeplabcut.benchmark`` package is not yet publicly released. Instructions on this page will be
   updated accordingly after release. The package will be part of DeepLabCut.

Submitting a model
------------------

We offer two evaluation types: To get started, file-based evaluations are easy to integrate into existing code bases. 


File-based Evaluations
^^^^^^^^^^^^^^^^^^^^^^


.. note::

   This section is a draft. More instructions will be added soon.

File-based evaluations are the easiest form to get started with the DLC Benchmark. You can develop and evaluate your model in your own compute environment, and simply submit an evaluation file to the DLC Benchmark.

No additional packages are needed besides the latest version of ``deeplabcut``.

.. code::

   import deeplabcut.benchmark

   # Load the challenge dataset(s) for your choice:
   challenge = deeplabcut.benchmark.Challenge('maDLC')

   # Load your model: This contains your custom code, computing predictions
   # based on the passed images.
   class MyModel(deeplabcut.benchmark.Model):

      def prepare(self):
         # Set up your model here
         self.model = make_my_custom_model()

      def predict(self, video):
         # Compute the keypoints with the model you loaded in prepare()
         keypoints = self.model(video)
         return keypoints

   # Evaluate your model on the benchmark
   results = challenge.evaluate(predict_pose)

   # Check the results
   print(results.summary())


If you are happy with the results, upload your results to the benchmark:

.. code:: python

   results.upload()



Code-based Evaluations
^^^^^^^^^^^^^^^^^^^^^^

.. note::

   This section is a draft. More instructions will be added soon.

We use Docker_ for code-based evaluations, to ensure maximum flexibility for developers and reproducibility of results across platforms.

To prepare your submission, your codebase should have a ``Dockerfile`` in its top-level directory with build instructions. We strongly recommend to keep the image size added by the ``Dockerfile`` small by making use of containers from the Dockerhub_.

After preparing your codebase, run the benchmark with

.. code:: 

   $ python -m deeplabcut.benchmark evaluate /path/to/codebase --challenge maDLC


which writes a result file to the current directory.
Check the results using

.. code::

   $ python -m deeplabcut.benchmark summary

and upload your results to the benchmark page using

.. code::

   $ python -m deeplabcut.benchmark upload



.. _DockerHub: https://hub.docker.com/