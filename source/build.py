from jinja2 import Environment, FileSystemLoader, select_autoescape

import os
import sys
sys.path.append("..")
import benchmark


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
    results = benchmark.loadcache()
    df = results.toframe().reset_index()[["method", "benchmark", "RMSE", "mAP"]].rename(
        columns=dict(
            benchmark = "Dataset",
            method = "Model",
            RMSE = "Pose - RSME",
            mAP = "Pose - mAP"
        )
    ).round(3).fillna('--')
    return df

env = Environment(loader=FileSystemLoader("_templates"), autoescape=select_autoescape())
template = env.get_template("index.html")

df = load_paper_results()

os.makedirs("generated", exist_ok=True)
header = df.columns
descriptions = {"Model": "The model name"}
header = [(name, descriptions.get(name, None)) for name in header]
with open("generated/table.html", "w") as file:
    index = template.render(columns=header, table=df.values)
    file.write(index)
