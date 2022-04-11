# %%

import sys
import unittest.mock

MOCK_MODULES = [
    'statsmodels',
    'statsmodels.api',
    'pytables'
]
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

MULTI_KEYPOINTS = {
    'trimouse': ('snout', 'leftear', 'rightear', 'shoulder', 'spine1', 'spine2', 'spine3', 'spine4', 'tailbase', 'tail1', 'tail2', 'tailend'),
    'pups': ('end1', 'interm1', 'interm2', 'interm3', 'end2'),
    'marmosets': ('Front', 'Right', 'Middle', 'Left', 'FL1', 'BL1', 'FR1', 'BR1', 'BL2', 'BR2', 'FL2', 'FR2', 'Body1', 'Body2', 'Body3'),
    'fish': ('tip', 'gill', 'peduncle', 'caudaltip', 'dfin1', 'dfin2', 'dfintip'),
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
        df.drop('single', level='individuals', axis=1, inplace=True)
    except KeyError:
        pass
    n_animals = len(df.columns.get_level_values('individuals').unique())

    with open(pickle_file, 'rb') as f:
        assemblies_pred, _, image_paths = pickle.load(f)
    if isinstance(image_paths[0], str):
        image_paths = [tuple(im.split('/')) for im in image_paths]
    ground_truth = (df.loc[image_paths]
                    .to_numpy()
                    .reshape((len(image_paths), n_animals, -1, 2)))
    temp = np.ones((*ground_truth.shape[:3], 3))
    temp[..., :2] = ground_truth
    assemblies_gt = inferenceutils._parse_ground_truth_data(temp)

    with open(metadata_file, 'rb') as f:
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
    return oks['mAP']

def conv_obj_to_assemblies(eval_results_obj, keypoint_names):
    """
    from memory, I think we had chatted about something like this
    {
        img1: {
            animal1: {
                kpt1: xy,
                kpt2: xy,
            },
            animal2: {
                kpt1: xy,
                kpt2: xy,
                kpt4: xy,
            },
        },
        img2: ...
    }
    that piece of code just shows you how that can be converted
    into something DLC likes.

    ex: conv_obj_to_assemblies(obj, ('kpt1', 'kpt2', 'kpt3', 'kpt4'))
    """
    assemblies = {}
    for image_path, results in eval_results_obj.items():
        lst = []
        for pose in results.values():
            ass = inferenceutils.Assembly(len(keypoint_names))
            for kpt, xy in pose.items():
                joint = inferenceutils.Joint(
                    pos=(xy), label=keypoint_names.index(kpt),
                )
                ass.add_joint(joint)
            lst.append(ass)
        assemblies[image_path] = lst
    return assemblies

def calc_map_from_obj(
    eval_results_obj,
    dataset_name,
    h5_file,
    oks_sigma=0.1,
    margin=0,
    symmetric_kpts=None,
):
    """Calculate mAP from the pure-Python (pydantic?) interface to results (for all the submission to come)."""
    kpts = MULTI_KEYPOINTS[dataset_name]
    assemblies_pred = conv_obj_to_assemblies(eval_results_obj, kpts)
    assemblies_gt = inferenceutils.parse_ground_truth_data_file(h5_file)
    imnames = pd.read_hdf(h5_file).index.to_list()
    assemblies_gt = {imnames[k]: v for k, v in assemblies_gt.items()}
    oks = inferenceutils.evaluate_assembly(
        assemblies_pred,
        assemblies_gt,
        oks_sigma,
        margin=margin,
        symmetric_kpts=symmetric_kpts,
    )
    return oks['mAP']

def calc_rmse(
    full_pickle_file,
    h5_file,
    metadata_file,
):
    """Calc prediction errors from DLC output files."""
    with open(metadata_file, 'rb') as f:
        inds_test = pickle.load(f)[2]
    gt = evaluate_multianimal._format_gt_data(h5_file)
    images_test = [list(gt['annotations'])[i] for i in inds_test]
    with open(full_pickle_file, 'rb') as f:
        data = pickle.load(f)
    meta = data.pop('metadata')
    if isinstance(list(data)[0], tuple):
        data = {os.path.join(*k): v for k, v in data.items()}
    preds = defaultdict(dict)
    preds['metadata']['keypoints'] = meta['all_joints_names']
    preds['predictions'] = {
        k: v['prediction'] for k, v in data.items() if k in images_test
    }
    errors = evaluate_multianimal.calc_prediction_errors(preds, gt)
    return np.nanmean(errors[..., 0])

def calc_rmse_from_obj(
    eval_results_obj,
    dataset_name,
    h5_file,
):
    """Calc prediction errors for submissions."""
    kpts = MULTI_KEYPOINTS[dataset_name]
    assemblies_pred = conv_obj_to_assemblies(eval_results_obj, kpts)
    preds = defaultdict(dict)
    preds['metadata']['keypoints'] = kpts
    for image, assemblies in assemblies_pred.items():
        data = np.stack([a.data for a in assemblies]).swapaxes(0, 1)
        temp = {
            'coordinates': tuple([list(data[..., :2])]),
            'confidence': list(np.expand_dims(data[..., 2], axis=2)),
        }
        preds['predictions'][image] = temp
    gt = evaluate_multianimal._format_gt_data(h5_file)
    errors = evaluate_multianimal.calc_prediction_errors(preds, gt)
    return np.nanmean(errors[..., 0])


class BenchmarkDataset():

    def compute_pose_rmse():
        pass

    def compute_pose_map():
        pass

class MultiMouseDataset():
    gt_file = 'data/h5/CollectedData_Daniel.h5'
    metadata_file = 'data/pickles/Documentation_data-MultiMouse_70shuffle1.pickle'
    name = "tri-Mouse"

class PupsDataset():
    gt_file = 'data/h5/CollectedData_Mostafizur.h5'
    metadata_file = 'data/pickles/Documentation_data-CrackingParenting_70shuffle1.pickle'
    name = "parenting"

class MarmosetDataset():
    gt_file = 'data/h5/CollectedData_Mackenzie.h5'
    metadata_file = 'data/pickles/Documentation_data-Marmoset_70shuffle1.pickle'
    name = "marmosets"

class FishDataset():
    gt_file = 'data/h5/CollectedData_Valentina.h5'
    metadata_file = 'data/pickles/Documentation_data-Schooling_70shuffle1.pickle'
    name = "fish"

class DLCEvaluation(MultiMouseDataset):

    _files = [
        'data/pickles/DLC_effnet_b7_MultiMouseJun22shuffle1_30000-snapshot-30000_assemblies.pickle',
        'data/pickles/DLC_dlcrnetms5_MultiMouseJun22shuffle1_30000-snapshot-30000_assemblies.pickle',
        'data/pickles/DLC_resnet50_MultiMouseJun22shuffle1_30000-snapshot-30000_assemblies.pickle',
    ]

    def ...:
        e = calc_rmse(pickle_file.replace('assemblies', 'full'), gt_file, metadata_file)
        m = calc_map(pickle_file, gt_file, metadata_file)

class DLCPupsDataset():
    pickle_files = [
        'data/pickles/DLC_effnet_b7_CrackingParentingMar24shuffle1_30000-snapshot-30000_assemblies.pickle',
        'data/pickles/DLC_effnet_b7_s4_CrackingParentingMar24shuffle1_30000-snapshot-30000_assemblies.pickle',
        'data/pickles/DLC_dlcrnetms5_CrackingParentingMar24shuffle1_30000-snapshot-30000_assemblies.pickle',
    ]

    def ...:
        e = calc_rmse(pickle_file.replace('assemblies', 'full'), gt_file, metadata_file)
        m = calc_map(pickle_file, gt_file, metadata_file, 0.15, 10, [[0, 4], [1, 3]])

class Marmosets():
    pickle_files = [
        'data/pickles/DLC_effnet_b7_MarmosetMay7shuffle1_200000-snapshot-200000_assemblies.pickle',
        'data/pickles/DLC_effnet_b7_s4_MarmosetMay7shuffle1_200000-snapshot-200000_assemblies.pickle',
        'data/pickles/DLC_dlcrnetms5_MarmosetMay7shuffle1_200000-snapshot-200000_assemblies.pickle',
        'data/pickles/DLC_dlcrnetms5_s4_MarmosetMay7shuffle1_200000-snapshot-200000_assemblies.pickle',
    ]
    for pickle_file in pickle_files:
        e = calc_rmse(pickle_file.replace('assemblies', 'full'), gt_file, metadata_file)
        m = calc_map(pickle_file, gt_file, metadata_file)
        print(e, m)

class Fish():
    # %%
    # Fish
    pickle_files = [
        'data/pickles/DLC_effnet_b7_SchoolingMay7shuffle1_30000-snapshot-30000_assemblies.pickle',
        'data/pickles/DLC_resnet50_SchoolingMay7shuffle1_30000-snapshot-30000_assemblies.pickle',
        'data/pickles/DLC_dlcrnetms5_SchoolingMay7shuffle1_30000-snapshot-30000_assemblies.pickle',
    ]
    for pickle_file in pickle_files:
        e = calc_rmse(pickle_file.replace('assemblies', 'full'), gt_file, metadata_file)
        m = calc_map(pickle_file, gt_file, metadata_file, drop_kpts=[4, 5])
        print(e, m)
    # %%
