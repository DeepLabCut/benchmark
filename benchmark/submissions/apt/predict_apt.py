import json

import numpy as np

from deeplabcut import benchmark
from deeplabcut.benchmark.benchmarks import TriMouseBenchmark, MarmosetBenchmark, ParentingMouseBenchmark, FishBenchmark 


code = "https://github.com/kristinbranson/APT.git"
data_root = "benchmark/submissions/apt/data"


def get_names():
  return "GRONe", "MMPose-CiD", "DeTR+GRONe", "DeTR+Hrformer"

def get_prefix(name):
  if name == "GRONe":
    prefix = 'grone'
  elif name == "MMPose-CiD":
    prefix = 'cid'
  elif name == "DeTR+GRONe":
    prefix = 'mdn_bbox'
  elif name == "DeTR+Hrformer":
    prefix = 'hrformer_bbox'

  return prefix


def parse_predictions(data: dict) -> dict:
  """Sets the data into the expected format for the DeepLabCut benchmark

  Not needed if the "score"/"pose" keys are added to the JSON files
  """
  rng = np.random.default_rng(0)

  predictions = {}
  for img, poses in data.items():
    img_predictions = []

    # give first prediction base score 0.95, second 0.9, third 0.85, ...
    score_steps = np.linspace(0.95, 0, 20)

    # so that all scores are different and sorting is deterministic
    score_offset = rng.random(1) / 50

    for i, pose in enumerate(poses):
      # get random score
      idv_score = np.clip(score_steps[i] + score_offset, 0, 1).item()

      img_predictions.append(
        {
          "pose": pose,
          "score": idv_score,
        }
      )
    predictions[img] = tuple(img_predictions)

  return predictions


@benchmark.register
class APTTriMouse(TriMouseBenchmark):
  code = code

  def names(self):
    return get_names()

  def get_predictions(self,name):
    prefix = get_prefix(name)

    res_file = f'{data_root}/{prefix}_trimice_test.json'
    with open(res_file) as f:
      return parse_predictions(json.load(f))


@benchmark.register
class APTMarmoset(MarmosetBenchmark):
  code = code

  def names(self):
    return get_names()

  def get_predictions(self,name):
    prefix = get_prefix(name)

    res_file = f'{data_root}/{prefix}_marmoset_test.json'
    with open(res_file) as f:
      return parse_predictions(json.load(f))


@benchmark.register
class APTParenting(ParentingMouseBenchmark):
  code = code

  def names(self):
    return get_names()
    #return "GRONe", "DeTR+GRONe", "DeTR+Hrformer"

  def get_predictions(self,name):
    prefix = get_prefix(name)

    res_file = f'{data_root}/{prefix}_parenting_test.json'
    with open(res_file) as f:
      return parse_predictions(json.load(f))


@benchmark.register
class APTFish(FishBenchmark):
  code = code

  def names(self):
    return get_names()

  def get_predictions(self,name):
    prefix = get_prefix(name)

    res_file = f'{data_root}/{prefix}_fish_test.json'
    with open(res_file) as f:
      return parse_predictions(json.load(f))


