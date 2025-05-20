import pandas as pd
from scipy.stats import binomtest
from numpy import where
import os
import csv

import scipy.stats

model = "o1"
typ = "orig"
classic = "Zebra"



def eval_qa(model):
    wrong_format = 0
    all_count = 0
    for classic in ["Einstein", "Zebra"]:
        for typ in ["orig", "orig_NL", "lexical_replacements", "domain_replacements"]:
            per_item_df = pd.DataFrame()
            per_step_df = pd.DataFrame()

            eval_file = f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-zeroShot/qa_format/solution_steps/eval/{classic}_{typ}_zeroShot_eval.tsv"

            eval_df = pd.read_csv(eval_file, sep="\t")

            wrong_format += list(eval_df["format"]).count(False)
            count = len(list(eval_df["format"]))
            all_count += count

            item_accs = []
            item_p_vals = []
            item_wrong_format = []

            items = list(set(eval_df["target"]))
            steps = []
            #print(items)
            for item in items:
                item_df = eval_df[(eval_df["target"]==item) & (eval_df["format"]==True)]
                steps.append(list(item_df["step"])[0])
                correct = list(item_df["correct"]).count(True)
                all_pred = len(list(item_df["correct"]))

                if all_pred != 0:
                    acc = correct/all_pred
                    p_val = binomtest(k=correct, n=all_pred, p=0.2, alternative="greater").pvalue
                    item_wrong_format.append(True)
                else:
                    acc = 0.0
                    p_val = 0.0
                    item_wrong_format.append(False)

                item_accs.append(acc)
                item_p_vals.append(p_val)

            per_item_df["model"] = [model for item in items]
            per_item_df["setup"] = [typ for item in items]
            per_item_df["item"] = items
            per_item_df["step"] = steps
            per_item_df["wrong_format"] = item_wrong_format
            per_item_df["acc"] = item_accs
            per_item_df["p-val"] = item_p_vals
            per_item_df ["sig"] = ["**" if p<0.01 else "*" if p<0.05 else "" for p in per_item_df["p-val"]]
            #per_item_df["<0.01"] = where(per_item_df["p-val"] < 0.01, True, False)
            #per_item_df["<0.001"] = where(per_item_df["p-val"] < 0.001, True, False)

            per_item_df.sort_values(by="step", ascending=True, inplace=True)
            print(per_item_df)
            step_accs = []
            step_p_vals = []
            step_wrong_format = []

            steps = list(set(eval_df["step"]))

            for step in steps:
                step_df = eval_df[(eval_df["step"]==step)&eval_df["format"]==True]

                correct = list(step_df["correct"]).count(True)
                all_pred = len(list(step_df["correct"]))

                if all_pred != 0:
                    acc = correct/all_pred
                    p_val = binomtest(k=correct, n=all_pred, p=0.2, alternative="greater").pvalue
                    step_wrong_format.append(True)
                else:
                    acc = 0.0
                    p_val = 0.0
                    step_wrong_format.append(False)

                step_accs.append(acc)
                step_p_vals.append(p_val)

            per_step_df["model"] = [model for item in steps]
            per_step_df["setup"] = [typ for item in steps]
            per_step_df["step"] = steps
            per_step_df["wrong_format"] = step_wrong_format
            per_step_df["acc"] = step_accs
            per_step_df["p-val"] = step_p_vals
            per_step_df ["sig"] = ["**" if p<0.01 else "*" if p<0.05 else "" for p in per_step_df["p-val"]]
            #per_step_df["<0.001"] = where(per_step_df["p-val"] < 0.001, True, False)

            item_dir = f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-zeroShot/qa_format/solution_steps/general_metrics/per_item"
            step_dir = f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-zeroShot/qa_format/solution_steps/general_metrics/per_step"

            try:
                os.makedirs(item_dir)
                os.makedirs(step_dir)
            except:
                pass

            item_out = f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-zeroShot/qa_format/solution_steps/general_metrics/per_item/{model}_{classic}_{typ}_item_eval.tsv"
            step_out = f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-zeroShot/qa_format/solution_steps/general_metrics/per_step/{model}_{classic}_{typ}_item_eval.tsv"

            per_item_df.to_csv(item_out, sep="\t", index=False)
            per_step_df.to_csv(step_out, sep="\t", index=False)

    print(model, wrong_format/all_count)

#for model in ["ChatGPT", "o1", "LLaMa3", "LLaMa3.1-70B", "LLaMa3.3-70B", "Mistral", "Qwen2-72B", "Qwen2"]:
#    eval_qa(model)

#def summary_eval(models):
models = ["LLaMa3"]
classic = "Einstein"

for model in models:
    orig_grids = ["orig", "orig_NL"]
    manip_grids = ["lexical_replacements", "domain_replacements"]
    for grid_setup in orig_grids:
        eval_file = f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-zeroShot/qa_format/solution_steps/eval/{classic}_{typ}_zeroShot_eval.tsv"



def get_eval_metrics_classic(model, classic, typ, n):
    prediction_file = f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-zeroShot/qa_format/eval/{classic}_{n}{typ}_zeroShot_eval.tsv"
    prediction_df = pd.read_csv(prediction_file, sep="\t")

    #print(prediction_df.head())

    format = list(prediction_df["format"])

    format_counter = format.count(False)
    elem_counter = len(format)

    
    correct = list(prediction_df["correct"])

    if classic == "Zebra":
        pos1_df = prediction_df[prediction_df["solution"].str.endswith("1")]
        pos5_df = prediction_df[prediction_df["solution"].str.endswith("5")]

        format_pos1 = list(pos1_df["format"]).count(False)
        format_pos5 = list(pos5_df["format"]).count(False)


        correct_pos1 = list(pos1_df["correct"])
        correct_pos5 = list(pos5_df["correct"])

        pos1_acc = correct_pos1.count(True)/len(correct_pos1)
        pos5_acc = correct_pos5.count(True)/len(correct_pos5)

        try:
            out_dir = f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-zeroShot/qa_format/general_metrics/"
            os.makedirs(out_dir)
        except:
            pass

        out_file = f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-zeroShot/qa_format/general_metrics/{classic}_{n}{typ}_zeroShot_general.tsv"

        with open(out_file, "w") as fout:
            writer = csv.writer(fout, delimiter="\t")
            writer.writerow(["setup", "acc_pos1", "acc_pos5", "wrong_format_pos1", "wrong_format_pos5"])
            writer.writerow([f"{model}_{classic}_{n}{typ}", pos1_acc, pos5_acc, format_pos1, format_pos5])

    else:

        acc = correct.count(True)/len(correct)

        try:
            out_dir = f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-zeroShot/qa_format/general_metrics/"
            os.makedirs(out_dir)
        except:
            pass

        out_file = f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-zeroShot/qa_format/general_metrics/{classic}_{n}{typ}_zeroShot_general.tsv"

        with open(out_file, "w") as fout:
            writer = csv.writer(fout, delimiter="\t")
            writer.writerow(["setup", "acc", "wrong_format", "elem_counter"])
            writer.writerow([f"{model}_{classic}_{n}{typ}", acc, format_counter, elem_counter])

    return format_counter, elem_counter
"""
for model in ["LLaMa3", "LLaMa3.1-70B", "LLaMa3.3-70B", "Mistral", "Qwen2-72B", "Qwen2"]:
    format_counts = 0
    elem_counts = 0
    for classic in ["Zebra"]:
        for typ in ["orig", "orig_NL", "lexical_replacements", "domain_replacements"]:
            if typ == "domain_replacements":
                for n in range (1, 6):
                    print(model, classic, typ, n)
                    format_counter, elem_counter = get_eval_metrics_classic(model, classic, typ, n)
                    format_counts += format_counter
                    elem_counts += elem_counter
            else:
                print(model, classic, typ)
                format_counter, elem_counter = get_eval_metrics_classic(model, classic, typ, n="")
                format_counts += format_counter
                elem_counts += elem_counter
    print(format_counts, elem_counts, format_counts/elem_counts)
    """