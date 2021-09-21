from jinja2 import Environment, FileSystemLoader, select_autoescape


def example_data():
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


env = Environment(loader=FileSystemLoader("_templates"), autoescape=select_autoescape())
template = env.get_template("index.html")


import os

df = example_data()
os.makedirs("generated", exist_ok=True)
header = df.columns
descriptions = {"Model": "The model name"}
header = [(name, descriptions.get(name, None)) for name in header]
with open("generated/table.html", "w") as file:
    index = template.render(columns=header, table=df.values)
    file.write(index)
