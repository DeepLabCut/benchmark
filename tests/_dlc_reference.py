"""Reference results for computing DLC errors from raw predictions."""

import sys
import unittest.mock

MOCK_MODULES = ["statsmodels", "statsmodels.api", "pytables"]
for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = unittest.mock.MagicMock()

import numpy as np
import os
import pandas as pd
import pickle
from collections import defaultdict
from deeplabcut.pose_estimation_tensorflow.lib import inferenceutils
from deeplabcut.pose_estimation_tensorflow.core import evaluate_multianimal
from deeplabcut.utils.conversioncode import guarantee_multiindex_rows

import deeplabcut.benchmark.utils

MULTI_KEYPOINTS = {
    "trimouse": (
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
    ),
    "pups": ("end1", "interm1", "interm2", "interm3", "end2"),
    "marmosets": (
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
    ),
    "fish": ("tip", "gill", "peduncle", "caudaltip", "dfin1", "dfin2", "dfintip"),
}


def calc_map(
    pickle_file,
    h5_file,
    metadata_file,
    oks_sigma=0.1,
    margin=0,
    symmetric_kpts=None,
    drop_kpts=None,
):
    """Calculate mAP from DLC output files."""
    df = pd.read_hdf(h5_file)
    guarantee_multiindex_rows(df)
    try:
        df.drop("single", level="individuals", axis=1, inplace=True)
    except KeyError:
        pass
    n_animals = len(df.columns.get_level_values("individuals").unique())

    with open(pickle_file, "rb") as f:
        assemblies_pred, _, image_paths = pickle.load(f)
    if isinstance(image_paths[0], str):
        image_paths = [tuple(im.split("/")) for im in image_paths]
    ground_truth = (
        df.loc[image_paths].to_numpy().reshape((len(image_paths), n_animals, -1, 2))
    )
    temp = np.ones((*ground_truth.shape[:3], 3))
    temp[..., :2] = ground_truth
    assemblies_gt = inferenceutils._parse_ground_truth_data(temp)

    with open(metadata_file, "rb") as f:
        inds_test = pickle.load(f)[2]
    assemblies_gt_test = {k: v for k, v in assemblies_gt.items() if k in inds_test}

    if drop_kpts:
        temp = {}
        for k, v in assemblies_gt_test.items():
            lst = []
            for a in v:
                arr = np.delete(a.data[:, :3], drop_kpts, axis=0)
                a = inferenceutils.Assembly.from_array(arr)
                lst.append(a)
            temp[k] = lst
        assemblies_gt_test = temp

    oks = inferenceutils.evaluate_assembly(
        assemblies_pred,
        assemblies_gt_test,
        oks_sigma,
        margin=margin,
        symmetric_kpts=symmetric_kpts,
    )
    return oks["mAP"]

def calc_rmse(
    full_pickle_file,
    h5_file,
    metadata_file,
):
    """Calc prediction errors from DLC output files."""
    with open(metadata_file, "rb") as f:
        inds_test = pickle.load(f)[2]
    gt = evaluate_multianimal._format_gt_data(h5_file)
    images_test = [list(gt["annotations"])[i] for i in inds_test]
    with open(full_pickle_file, "rb") as f:
        data = pickle.load(f)
    meta = data.pop("metadata")
    if isinstance(list(data)[0], tuple):
        data = {os.path.join(*k): v for k, v in data.items()}
    preds = defaultdict(dict)
    preds["metadata"]["keypoints"] = meta["all_joints_names"]
    preds["predictions"] = {
        k: v["prediction"] for k, v in data.items() if k in images_test
    }
    errors = evaluate_multianimal.calc_prediction_errors(preds, gt)
    return np.nanmean(errors[..., 0])