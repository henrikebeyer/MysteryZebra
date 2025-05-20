import pandas as pd
import csv

error_dict = {}

for model in ["R1", "o1", "ChatGPT", "LLaMa3", "LLaMa3.1-70B", "LLaMa3.3-70B", "Qwen2-72B", "Qwen2", "Mistral"]:

    error_file = f"/home/oenni/Dokumente/LLM_reasoning/error_analysis/{model}-zeroShot_error_analysis.tsv"

    error_df = pd.read_csv(error_file, sep="\t")

    error_dict[model] = {"E1 ":0,
                        "E2 ":0,
                        "E3 ":0,
                        "E4 ":0,
                        "E5 ":0,
                        "E6 ":0,
                        "E7 ":0,
                        "E8":0,
                        "E9":0,
                        "E10":0,
                        "E11":0,
                        "E12":0,
                        "E13":0,
                        "E14":0,
                        "E15":0,
                        "E16":0,
                        "E17":0,
                        "E18":0}

    errors = error_df["Error"]

    for error in error_dict[model].keys():
        for error_list in errors:
            if error in str(error_list):
                error_dict[model][error]+=1

out_file = "/home/oenni/Dokumente/LLM_reasoning/error_analysis/error_source_summary.tsv"

with open (out_file, "w") as fout:
    writer = csv.writer(fout, delimiter="\t")
    writer.writerow(["model"]+list(error_dict["o1"].keys()))
    for model in error_dict.keys():
        writer.writerow([model]+list(error_dict[model].values()))
