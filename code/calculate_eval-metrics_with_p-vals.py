import pandas as pd
import numpy as np
import scipy
from math import sqrt
import os

model = "o1"
setup = "zeroShot"
typ = "orig"



def variance(n, d, k):
    # input: 
    #       - n: items per domain 
    #       - d: domains

    #print(k)
    V = (2*n -1) / ((n**2) * d * k)
    return(V)

format = 0
all_preds = 0

def eval_classic(model, classic, setup):

    format = 0
    all_preds = 0

    eval_classic = pd.DataFrame()
    norm_score_df = pd.DataFrame()  
    var_df = pd.DataFrame()  

    types = []
    accs = []
    avg_scores = []
    max_scores = []
    min_scores = []
    target_scores = []
    norm_scores = []
    vars = []
    exp_val = []
    format_wrong = []

    for typ in ["orig", "orig_NL", "1domain_replacements", "2domain_replacements", "3domain_replacements", "4domain_replacements", "5domain_replacements", "lexical_replacements"]: 
        types.append(f"{classic}-{typ}")
        prediction_file = f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-{setup}/eval/{classic}_{typ}_solution_eval.tsv"
        prediction_df = pd.read_csv(prediction_file, sep="\t")
        preds = len(prediction_df["correct"])
        all_preds += preds
        prediction_df = prediction_df[prediction_df["formatting"]==True]
        correct_format = len(prediction_df["correct"])
        format += preds - len(prediction_df["correct"])
        #print(prediction_df)

        correct = list(prediction_df["correct"])
        score = list(prediction_df["score"])

        if len(correct) != 0:

            accs.append(correct.count(True)/len(correct))
            avg_scores.append(sum(score) / len(score))
            max_scores.append(max(score))
            min_scores.append(min(score))
            target_scores.append(25)
            exp_val.append(1/5)
            norm_scores.append(avg_scores[-1]/target_scores[-1])
            vars.append(variance(n=5, d=5, k=correct_format))
            format_wrong.append(False)

        else:
            accs.append(0.0)
            avg_scores.append(0.0)
            max_scores.append(0.0)
            min_scores.append(0.0)
            target_scores.append(25)
            exp_val.append(1/5)
            norm_scores.append(0.0)
            vars.append(0.0)
            format_wrong.append(True)


    eval_classic["typ"] = types
    eval_classic[f"acc"] = accs
    eval_classic[f"target_score"] = target_scores
    eval_classic[f"avg_score"] = avg_scores
    eval_classic[f"max_score"] = max_scores
    eval_classic[f"min_score"] = min_scores
    eval_classic[f"norm_score"] = norm_scores
    eval_classic[f"variance"] = vars
    eval_classic[f"format_wrong"] = format_wrong

    #print(eval_classic)

    norm_score_df["typ"] = types
    norm_score_df[f"norm_score"] = norm_scores

    var_df["typ"] = types
    var_df[f"variance"] = vars

    var_df["E"] = exp_val

    var_df["m"] = norm_score_df["norm_score"]
    v_sqrt = [sqrt(v) for v in list(var_df["variance"])]
    var_df["v_sqrt"] = v_sqrt
    var_df["z-score"] = abs(var_df["m"]-var_df["E"])/var_df["v_sqrt"]
    var_df["p-val"] = scipy.stats.norm.sf(abs(var_df["z-score"]))
    var_df["sig"] = ["**" if p<0.01 else "*" if p<0.05 else "" for p in var_df["p-val"]]
    
    #np.where(var_df["p-val"] < 0.05, True, False)
    #var_df["<0.01"] = np.where(var_df["p-val"] < 0.01, True, False)
    #var_df["<0.001"] = np.where(var_df["p-val"] < 0.001, True, False)

    #print(classic, typ)
    print(var_df)

    out_dir = f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-{setup}/general_metrics/"
    try:
        os.makedirs(out_dir)
    except:
        pass


    #print(eval_classic)
    eval_classic.to_csv(f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-{setup}/general_metrics/{model}_{setup}_{classic}_eval_cleaned.tsv", sep="\t", index=False)
    norm_score_df.to_csv(f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-{setup}/general_metrics/{model}_{setup}_{classic}_norm_scores.tsv", sep="\t", index=False)
    var_df.to_csv(f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-{setup}/general_metrics/{model}_{setup}_{classic}_p-vals.tsv", sep="\t", index=False)

    return [format, all_preds]

for classic in ["Einstein", "Zebra"]:
    output = eval_classic(model=model, classic=classic, setup="zeroShot")
    format += output[0]
    all_preds += output[1]


def eval_generated(model, typ):
    pred_sum = 0
    format = 0
    eval_df_all_sizes = pd.DataFrame()
    norm_score_df = pd.DataFrame()
    var_df = pd.DataFrame()
    for level in range(1, 13):
        if level in [1, 3, 4, 5, 8]:
            row_lower = 1
            col_lower = 2
        elif level in [2, 7]:
            row_lower = 1
            col_lower = 3
        elif level in [6, 9]:
            row_lower = 2
            col_lower = 2
        elif level in [10, 11, 12]:
            row_lower = 3
            col_lower = 3
        sizes = []
        accs = []
        avg_scores = []
        max_scores = []
        min_scores = []
        target_scores = []
        exp_val = []
        norm_scores = []
        vars = []
        format_wrong = []
        for row in range(1, 8):
            for col in range(2, 8):
                sizes.append(f"{row}x{col}")
                exp_val.append(1/col)
        eval_df_all_sizes["sizes"] = sizes
        eval_df_all_sizes["E"] = exp_val
        #sizes.append("level_avg")
        norm_score_df["sizes"] = sizes
        norm_score_df["E"] = exp_val
        #sizes.append("p-val_level_avg")
        var_df["size"] = sizes
        var_df["E"] = exp_val
        for row in range(1, 8):
            for col in range(2, 8):
                #print("level", level, row, "x", col)
                if row < row_lower or col < col_lower:
                    accs.append(None)
                    avg_scores.append(None)
                    max_scores.append(None)
                    min_scores.append(None)
                    target_scores.append(None)
                    norm_scores.append(None)
                    vars.append(None)
                    format_wrong.append(None)
                else:

                    prediction_file = f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-{setup}/{typ}_puzzles/Level{level}/eval/{row}x{col}-level{level}_{typ}_solution_eval.tsv"
                    prediction_df = pd.read_csv(prediction_file, sep="\t")
                    preds = len(prediction_df["correct"])
                    pred_sum += preds
                    prediction_df = prediction_df[prediction_df["formatting"]==True]
                    correct_format = len(prediction_df["correct"])
                    format += preds - correct_format
                    #print(prediction_df)

                    correct = list(prediction_df["correct"])
                    score = list(prediction_df["score"])

                    if len(correct) != 0:

                        accs.append(correct.count(True)/len(correct))
                        avg_scores.append(sum(score) / len(score))
                        max_scores.append(max(score))
                        min_scores.append(min(score))
                        target_scores.append(row*col)
                        norm_scores.append((avg_scores[-1] / target_scores[-1]))
                        vars.append(variance(n = col, d = row, k = correct_format))
                        #print("n =", col, "d = ", row, "k = ", correct_format)
                        #print("n =", cols, "d = ", rows, "k = ", correct_format)
                        #print(variance(n = col, d = row, k = correct_format))
                        format_wrong.append(False)

                    else:
                        accs.append(0.0)
                        avg_scores.append(0.0)
                        max_scores.append(0.0)
                        min_scores.append(0.0)
                        target_scores.append(row*col)
                        norm_scores.append(0.0)
                        vars.append(0.0)
                        format_wrong.append(True)


        eval_df_all_sizes[f"Lv{level}-acc"] = accs
        eval_df_all_sizes[f"Lv{level}-target_score"] = target_scores
        eval_df_all_sizes[f"Lv{level}-avg_score"] = avg_scores
        eval_df_all_sizes[f"Lv{level}-max_score"] = max_scores
        eval_df_all_sizes[f"Lv{level}-min_score"] = min_scores
        eval_df_all_sizes[f"Lv{level}-norm_score"] = norm_scores
        eval_df_all_sizes[f"Lv{level}-norm_score_var"] = vars
        eval_df_all_sizes[f"Lv{level}-format_wrong"] = format_wrong

        #norm_scores.append(sum(list(filter(None, norm_scores)))/((len(list(filter(None, norm_scores))))))
        #vars.append(sum(list(filter(None, vars)))/((len(list(filter(None, vars))))**2))

        norm_scores = norm_scores
        vars = vars
        norm_score_df[f"Lv{level}-norm_score"] = norm_scores
        var_df[f"Lv{level}-norm_score_var"] = vars
        
        
    norm_cols = [f"Lv{level}-norm_score" for level in range(1, 13)]
    var_cols = [f"Lv{level}-norm_score_var" for level in range(1, 13)]
    
    # significances over levels:
    level_norm_score_df = norm_score_df.drop(["sizes","E"], axis=1).transpose()
    E_level = []
    for level in range(1, 13):
        exps = []
        if level in [1, 3, 4, 5, 8]:
            row_lower = 1
            col_lower = 2
        elif level in [2, 7]:
            row_lower = 1
            col_lower = 3
        elif level in [6, 9]:
            row_lower = 2
            col_lower = 2
        elif level in [10, 11, 12]:
            row_lower = 3
            col_lower = 3
        for row in range(row_lower, 8):
            for col in range(col_lower,8):
                exps.append(1/col)

        E_level.append(sum(exps)/len(exps))

    level_norm_score_df["Level_avg"] = level_norm_score_df.sum(axis=1, numeric_only=True)/level_norm_score_df.count(axis=1, numeric_only=True)
    level_norm_score_df["E"] = E_level

    #print(level_norm_score_df)

    level_var_df = norm_score_df.drop(["sizes", "E"], axis=1).transpose()
    level_var_df[f"var"] = level_var_df.sum(axis=1, numeric_only=True)/(level_var_df.count(axis=1, numeric_only=True)**2)
    level_var_df["m"] = level_norm_score_df["Level_avg"]
    level_var_df["E"] = E_level
    v_sqrt = [sqrt(v) for v in list(level_var_df[f"var"])]
    level_var_df["v_sqrt"] = v_sqrt
    level_var_df["z-score"] = abs(level_var_df["m"]-level_var_df["E"])/level_var_df["v_sqrt"]
    level_var_df["p-val"] = scipy.stats.norm.sf(abs(level_var_df["z-score"]))
    level_var_df["sig"] = ["**" if p<0.01 else "*" if p<0.05 else "" for p in level_var_df["p-val"]]
    
    level_norm_score_df.to_csv(f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-zeroShot/orig_puzzles/general_metrics/{typ}_level_norm_scores.tsv", sep="\t", index=False)
    level_var_df.to_csv(f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-zeroShot/orig_puzzles/general_metrics/{typ}_level_vars_p-vals.tsv", sep="\t", index=False)
    

    norm_score_df[f"norm_score_size_avg"] = norm_score_df[norm_cols].sum(axis=1, numeric_only=True)/(norm_score_df[norm_cols].count(axis=1, numeric_only=True))
    norm_score_df.loc[norm_score_df["norm_score_size_avg"] > 1.0, "norm_score_size_avg"] = 1.0
    var_df["j"] = var_df[var_cols].count(axis=1, numeric_only=True)
    var_df[f"norm_score_size_var"] = var_df[var_cols].sum(axis=1, numeric_only=True)/(var_df[var_cols].count(axis=1, numeric_only=True)**2)
    
    var_df["m"] = norm_score_df["norm_score_size_avg"]
    v_sqrt = [sqrt(v) for v in list(var_df[f"norm_score_size_var"])]
    var_df["v_sqrt"] = v_sqrt
    var_df["z-score_size"] = abs(var_df["m"]-var_df["E"])/var_df["v_sqrt"]
    var_df["p-val_size"] = scipy.stats.norm.sf(abs(var_df["z-score_size"]))
    var_df["sig"] = ["**" if p<0.01 else "*" if p<0.05 else "" for p in var_df["p-val_size"]]

    
    #norm_score_df["sizes"] = list(eval_df_all_sizes["sizes"]).append("level_avg")
    #var_df["sizes"] = list(eval_df_all_sizes["sizes"]).append("level_avg")

    #print(norm_score_df)
    #print(var_df)

    #print(eval_df_all_sizes)
    #eval_df_all_sizes.to_csv(f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-zeroShot/orig_puzzles/general_metrics/all_levels_{typ}_eval_cleaned.tsv", sep="\t", index=False)
    #norm_score_df.to_csv(f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-zeroShot/orig_puzzles/general_metrics/all_levels_{typ}_norm_scores.tsv", sep="\t", index=False)
    #var_df.to_csv(f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-zeroShot/orig_puzzles/general_metrics/all_levels_{typ}_vars_p-vals.tsv", sep="\t", index=False)

#for model in ["Qwen2", "Qwen2-72B", "Mistral"]:
#eval_generated(model=model, typ=typ)