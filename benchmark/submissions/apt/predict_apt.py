from deeplabcut import benchmark
from deeplabcut.benchmark.benchmarks import TriMouseBenchmark, MarmosetBenchmark, ParentingMouseBenchmark, FishBenchmark #, DLCBenchMixin
from benchmark.baselines.deeplabcut import DLCBenchMixin
import json

code="https://github.com/kristinbranson/APT.git"

def get_names():
  return "GRONe", "MMPose-CiD", "DeTR+GRONe"

def get_prefix(name):
  if name == "GRONe":
    prefix = 'grone'
  elif name == "MMPose-CiD":
    prefix = 'cid'
  elif name == "DeTR+GRONe":
    prefix = 'mdn_bbox'

  return prefix

@benchmark.register
class APTTriMouse(DLCBenchMixin, TriMouseBenchmark):
  def names(self):
    return get_names()

  def get_predictions(self,name):
    prefix = get_prefix(name)

    res_file = f'data/{prefix}_trimice_test.json'
    with open(res_file) as f:
      return json.load(f)


@benchmark.register
class APTMarmoset(DLCBenchMixin, MarmosetBenchmark):
  def names(self):
    return get_names()

  def get_predictions(self,name):
    prefix = get_prefix(name)

    res_file = f'data/{prefix}_marmoset_test.json'
    with open(res_file) as f:
      return json.load(f)


@benchmark.register
class APTParenting(DLCBenchMixin, ParentingMouseBenchmark):
  def names(self):
    return get_names()

  def get_predictions(self,name):
    prefix = get_prefix(name)

    res_file = f'data/{prefix}_parenting_test.json'
    with open(res_file) as f:
      return json.load(f)


@benchmark.register
class APTFish(DLCBenchMixin, FishBenchmark):
  def names(self):
    return get_names()

  def get_predictions(self,name):
    prefix = get_prefix(name)

    res_file = f'data/{prefix}_fish_test.json'
    with open(res_file) as f:
      return json.load(f)


