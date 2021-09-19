from jinja2 import Environment, FileSystemLoader, select_autoescape

import os
import sys
sys.path.append("..")
import deeplabcut.benchmark

dataset_names = {
    'trimouse' : 'TRI-MOUSE',
    'parenting' : 'PARENTING',
    'marmosets' : 'MARMOSETS',
    'fish' : 'FISH'
}

def load_paper_results():
    import numpy as np
    import pandas as pd
    import tabulate

    df = pd.read_csv('_static/results.tsv', sep = '\t')
    df.columns=[
            "Model",
            "Code",
            "Dataset",
            "Pose - RMSE",
            "Pose - mAP",
            #"reID - Acc",
            #"Tracking MOTA - w/o ID",
            #"Tracking MOTA - w/ ID",
    ]
    return df.fillna('--')

def load_benchmark_data():
    results = deeplabcut.benchmark.loadcache('../.results', on_missing = 'raise').toframe()
    #TODO(stes): Add this to the benchmark table in a coming update
    results['Code'] = 'https://github.com/DeepLabCut/DeepLabCut'
    df = results.reset_index()[["method", "Code", "benchmark", "RMSE", "mAP"]].rename(
        columns=dict(
            benchmark = "Dataset",
            method = "Model",
            RMSE = "RMSE (detections)",
            mAP = "mAP"
        )
    ).round(3).fillna('--')
    # TODO(stes): Move this post-hoc correction directly into the benchmark API
    df['Dataset'] = df['Dataset'].apply(lambda v: dataset_names.get(v, v))
    df['Model'] = df['Model'].apply(lambda v: f'- {v}')

    index_names = ['Model', 'Dataset']
    reference_results = load_paper_results().set_index(index_names)
    df = df.set_index(index_names)
    df.loc[reference_results.index, 'RMSE (assembly)'] = reference_results['Pose - RMSE']

    def _add_links(line):
        line["Model"] = '<a href="{Code}" target="_blank">{Model}</a>'.format(**line)
        return line
    df = df.reset_index().apply(_add_links, axis = 1)
    return df[["Model", "Dataset" , "RMSE (assembly)", "RMSE (detections)", "mAP"]]

env = Environment(loader=FileSystemLoader("_templates"), autoescape=select_autoescape())
template = env.get_template("index.html")

df = load_benchmark_data()

os.makedirs("generated", exist_ok=True)
header = df.columns
descriptions = {"Model": "The model name"}
header = [(name, descriptions.get(name, None)) for name in header]
with open("generated/table.html", "w") as file:
    index = template.render(columns=header, table=df.values)
    file.write(index)
