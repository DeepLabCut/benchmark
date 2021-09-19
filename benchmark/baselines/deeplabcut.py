"""Benchmark submission using multi-animal DeepLabCut (maDLC; Lauer et al. 2022, Nature Methods)"""

import pickle
import io
import numpy as np
import os
import pkgutil

from deeplabcut import benchmark
from deeplabcut.benchmark.benchmarks import (
    TriMouseBenchmark,
    MarmosetBenchmark,
    ParentingMouseBenchmark,
    FishBenchmark,
)


class _DLCDataset:
    def __init__(self, filename, keypoint_names, num_animals):
        self.keypoint_names = keypoint_names
        self.num_animals = num_animals
        data = io.BytesIO(pkgutil.get_data(__name__, filename))
        assemblies_, single_, filenames = pickle.load(data)
        n_multi_kpts = list(assemblies_.values())[0][0].xy.shape[0]
        try:
            n_unique_kpts = len(list(single_.values())[0])
        except IndexError:
            n_unique_kpts = 0
        n_kpts = n_multi_kpts + n_unique_kpts
        if isinstance(filenames[0], tuple):
            filenames = [os.path.join(*fname) for fname in filenames]
        self.__data = {}
        for i, name in enumerate(filenames):
            assemblies = []
            for a in assemblies_.get(i, []):
                data = np.full((n_kpts, 4), np.nan)
                data[:n_multi_kpts] = a.data
                assemblies.append((data, a.affinity))
            single = single_.get(i, [])
            if np.any(single):
                temp = np.full((n_kpts, 3), np.nan)
                temp[-n_unique_kpts:] = single
                single = [(temp, 1)]
            self.__data[name] = assemblies + single

    def keys(self):
        return tuple(self.__data.keys())

    def __getitem__(self, index):
        num_animals = len(self.__data[index])
        return tuple(
            {
                "pose": dict(
                    zip(
                        self.keypoint_names,
                        self.__data[index][animal_id][0][:, :2].tolist(),
                    )
                ),
                "score": self.__data[index][animal_id][1],
            }
            for animal_id in range(num_animals)
        )


class DLCBenchMixin:
    def names(self):
        return tuple(sorted(self._filenames.keys()))

    def get_predictions(self, key):
        filename = self._filenames[key]
        data = _DLCDataset(
            filename, keypoint_names=self.keypoint_names, num_animals=self.num_animals
        )
        return {key: data[key] for key in data.keys()}


@benchmark.register
class DLCTriMouse(DLCBenchMixin, TriMouseBenchmark):
    """TODO Add Model Description/Card."""

    keypoint_names = (
        "snout",
        "leftear",
        "rightear",
        "shoulder",
        "spine1",
        "spine2",
        "spine3",
        "spine4",
        "tailbase",
        "tail1",
        "tail2",
        "tailend",
    )

    code = "https://github.com/DeepLabCut/DeepLabCut"

    _filenames = {
        "EfficientNet B7_s4 (30k)": "data/DLC_effnet_b7_MultiMouseJun22shuffle1_30000-snapshot-30000_assemblies.pickle",
        "DLCRNet_ms4 (30k)": "data/DLC_dlcrnetms5_MultiMouseJun22shuffle1_30000-snapshot-30000_assemblies.pickle",
        "ResNet50 (30k)": "data/DLC_resnet50_MultiMouseJun22shuffle1_30000-snapshot-30000_assemblies.pickle",
    }


@benchmark.register
class MaDLCParentingMouse(DLCBenchMixin, ParentingMouseBenchmark):
    """TODO Add Model Description/Card."""

    keypoint_names = (
        "end1",
        "interm1",
        "interm2",
        "interm3",
        "end2",
        "snout",
        "leftear",
        "rightear",
        "shoulder",
        "spine1",
        "spine2",
        "spine3",
        "spine4",
        "tailbase",
        "tail1",
        "tail2",
        "tailend",
    )

    code = "https://github.com/DeepLabCut/DeepLabCut"

    _filenames = {
        "EfficientNet B7 (30k)": "data/DLC_effnet_b7_CrackingParentingMar24shuffle1_30000-snapshot-30000_assemblies.pickle",
        "EfficientNet B7_s4 (30k)": "data/DLC_effnet_b7_s4_CrackingParentingMar24shuffle1_30000-snapshot-30000_assemblies.pickle",
        "DLCRNet_ms4 (30k)": "data/DLC_dlcrnetms5_CrackingParentingMar24shuffle1_30000-snapshot-30000_assemblies.pickle",
    }


@benchmark.register
class MaDLCMarmosetBenchmark(DLCBenchMixin, MarmosetBenchmark):
    """TODO Add Model Description/Card."""

    keypoint_names = (
        "Front",
        "Right",
        "Middle",
        "Left",
        "FL1",
        "BL1",
        "FR1",
        "BR1",
        "BL2",
        "BR2",
        "FL2",
        "FR2",
        "Body1",
        "Body2",
        "Body3",
    )

    code = "https://github.com/DeepLabCut/DeepLabCut"

    _filenames = {
        "EfficientNet B7 (200k)": "data/DLC_effnet_b7_MarmosetMay7shuffle1_200000-snapshot-200000_assemblies.pickle",
        "EfficientNet B7_s4 (200k)": "data/DLC_effnet_b7_s4_MarmosetMay7shuffle1_200000-snapshot-200000_assemblies.pickle",
        "DLCRNet (200k)": "data/DLC_dlcrnetms5_MarmosetMay7shuffle1_200000-snapshot-200000_assemblies.pickle",
        "DLCRNet_ms4 (200k)": "data/DLC_dlcrnetms5_s4_MarmosetMay7shuffle1_200000-snapshot-200000_assemblies.pickle",
    }

@benchmark.register
class MaDLCFishBenchmark(DLCBenchMixin, FishBenchmark):
    """TODO Add Model Description/Card."""

    keypoint_names = "tip", "gill", "peduncle", "caudaltip", "dfintip"

    code = "https://github.com/DeepLabCut/DeepLabCut"

    _filenames = {
        "EfficientNet B7_s4 (30k)": "data/DLC_effnet_b7_SchoolingMay7shuffle1_30000-snapshot-30000_assemblies.pickle",
        "ResNet50_s4 (30k)": "data/DLC_resnet50_SchoolingMay7shuffle1_30000-snapshot-30000_assemblies.pickle",
        "DLCRNet_ms4 (30k)": "data/DLC_dlcrnetms5_SchoolingMay7shuffle1_30000-snapshot-30000_assemblies.pickle",
    }
