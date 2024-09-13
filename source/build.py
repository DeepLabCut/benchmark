import os
import sys

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape

sys.path.append("..")
import deeplabcut.benchmark

dataset_names = {
    "trimouse": "TRI-MOUSE",
    "parenting": "PARENTING",
    "marmosets": "MARMOSETS",
    "fish": "FISH",
}


def load_paper_results():
    import pandas as pd

    df = pd.read_csv("_static/results.tsv", sep="\t")
    df.columns = [
        "Model",
        "Code",
        "Dataset",
        "Pose - RMSE",
        "Pose - mAP",
    ]
    return df.fillna("--")


def load_benchmark_data():
    results = deeplabcut.benchmark.loadcache(
        "../.results", on_missing="raise"
    ).toframe()
    # TODO(niels): Get the code from the results DataFrame
    df = (
        results.reset_index()[["method", "code", "benchmark", "RMSE", "mAP"]]
        .rename(
            columns=dict(
                benchmark="Dataset", method="Model", RMSE="RMSE (detections)", mAP="mAP"
            )
        )
        .round(3)
        .fillna("--")
    )
    # TODO(stes): Move this post-hoc correction directly into the benchmark API
    df["Dataset"] = df["Dataset"].apply(lambda v: dataset_names.get(v, v))
    df["Model"] = df["Model"].apply(lambda v: f"- {v}")

    index_names = ["Model", "Dataset"]
    reference_results = load_paper_results().set_index(index_names)
    df = df.set_index(index_names)
    df.loc[reference_results.index, "RMSE (assembly)"] = reference_results[
        "Pose - RMSE"
    ]

    def _add_links(line):
        line["Model"] = '<a href="{code}" target="_blank">{Model}</a>'.format(**line)
        return line

    df = df.reset_index().apply(_add_links, axis=1)
    return df[["Model", "Dataset", "RMSE (assembly)", "RMSE (detections)", "mAP"]]


df = load_benchmark_data()
df = df.fillna("-")

for dataset in dataset_names.values():
    env = Environment(
        loader=FileSystemLoader("_templates"), autoescape=select_autoescape()
    )
    template = env.get_template("index.html")

    df_benchmark = df[df["Dataset"] == dataset]
    df_benchmark: pd.DataFrame

    # TODO(niels): Should we keep the dataset column in the tables?
    # df_benchmark = df_benchmark.drop("Dataset", axis=1)

    os.makedirs("generated", exist_ok=True)
    header = df_benchmark.columns
    descriptions = {"Model": "The model name"}
    header = [(name, descriptions.get(name, None)) for name in header]
    with open(f"generated/table{dataset}.html", "w") as file:
        index = template.render(table_id=dataset, columns=header, table=df_benchmark.values)
        file.write(index)
