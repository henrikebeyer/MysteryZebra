import pandas as pd
import os

model = "R1"
setup = "zeroShot"
typ = "orig"
level = 2

rows = 1
cols = 3

format = 0
all_preds = 0

def eval_classic(model, classic, typ, setup):

    format = 0
    all_preds = 0

    eval_classic = pd.DataFrame()

    accs = []
    avg_scores = []
    max_scores = []
    min_scores = []
    target_scores = []
    norm_scores = []
    format_wrong = []
    prediction_file = f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-{setup}/eval/{classic}_{typ}_solution_eval.tsv"
    prediction_df = pd.read_csv(prediction_file, sep="\t")
    preds = len(prediction_df["correct"])
    all_preds += preds
    prediction_df = prediction_df[prediction_df["formatting"]==True]
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
        norm_scores.append(avg_scores[-1]/target_scores[-1])
        format_wrong.append(False)

    else:
        accs.append(0.0)
        avg_scores.append(0.0)
        max_scores.append(0.0)
        min_scores.append(0.0)
        target_scores.append(25)
        norm_scores.append(0.0)
        format_wrong.append(True)


    eval_classic[f"acc"] = accs
    eval_classic[f"target_score"] = target_scores
    eval_classic[f"avg_score"] = avg_scores
    eval_classic[f"max_score"] = max_scores
    eval_classic[f"min_score"] = min_scores
    eval_classic[f"norm_score"] = norm_scores
    eval_classic[f"format_wrong"] = format_wrong

    print(eval_classic)
    eval_classic.to_csv(f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-{setup}/general_metrics/{model}_{setup}_{classic}_{typ}_eval_cleaned.tsv", sep="\t", index=False)

    return [format, all_preds]

for classic in ["Einstein", "Zebra"]:
    for typ in ["orig", "orig_NL", "lexical_replacements", "domain_replacements"]:
        if typ == "domain_replacements":
            for num in range(1,6):
                output = eval_classic(model=model, classic=classic, typ=f"{num}{typ}", setup="zeroShot")
                format += output[0]
                all_preds += output[1]
        else:
            output = eval_classic(model=model, classic=classic, typ=typ, setup="zeroShot")
            format += output[0]
            all_preds += output[1]

typ = "orig"
eval_df_all_sizes = pd.DataFrame()
for level in [1, 3, 4, 5, 8]:
    sizes = []
    accs = []
    avg_scores = []
    max_scores = []
    min_scores = []
    target_scores = []
    norm_scores = []
    format_wrong = []
    for row in range(1, 8):
        for col in range(2, 8):
            sizes.append(f"{row}x{col}")
    eval_df_all_sizes["sizes"] = sizes
    for row in range(1, 8):
        for col in range(2, 8):
            prediction_file = f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-{setup}/{typ}_puzzles/Level{level}/eval/{row}x{col}-level{level}_{typ}_solution_eval.tsv"
            prediction_df = pd.read_csv(prediction_file, sep="\t")
            preds = len(prediction_df["correct"])
            all_preds += preds
            prediction_df = prediction_df[prediction_df["formatting"]==True]
            format += preds - len(prediction_df["correct"])
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
                format_wrong.append(False)

            else:
                accs.append(0.0)
                avg_scores.append(0.0)
                max_scores.append(0.0)
                min_scores.append(0.0)
                target_scores.append(row*col)
                norm_scores.append(0.0)
                format_wrong.append(True)


    eval_df_all_sizes[f"Lv{level}-acc"] = accs
    eval_df_all_sizes[f"Lv{level}-target_score"] = target_scores
    eval_df_all_sizes[f"Lv{level}-avg_score"] = avg_scores
    eval_df_all_sizes[f"Lv{level}-max_score"] = max_scores
    eval_df_all_sizes[f"Lv{level}-min_score"] = min_scores
    eval_df_all_sizes[f"Lv{level}-norm_score"] = norm_scores
    eval_df_all_sizes[f"Lv{level}-format_wrong"] = format_wrong


print(eval_df_all_sizes)

eval_df_all_sizes.to_csv(f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-zeroShot/orig_puzzles/general_metrics/Level_1-3-4-5-8_{typ}_eval_cleaned.tsv", sep="\t", index=False)

eval_df_3_cols = pd.DataFrame()
for level in [2, 7]:
    sizes = []
    accs = []
    avg_scores = []
    max_scores = []
    min_scores = []
    target_scores = []
    norm_scores = []
    format_wrong = []
    for row in range(1, 8):
        for col in range(3, 8):
            sizes.append(f"{row}x{col}")
    eval_df_3_cols["sizes"] = sizes
    for row in range(1, 8):
        for col in range(3, 8):
            prediction_file = f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-{setup}/{typ}_puzzles/Level{level}/eval/{row}x{col}-level{level}_{typ}_solution_eval.tsv"
            prediction_df = pd.read_csv(prediction_file, sep="\t")
            preds = len(prediction_df["correct"])
            all_preds += preds
            prediction_df = prediction_df[prediction_df["formatting"]==True]
            format += preds - len(prediction_df["correct"])

            correct = list(prediction_df["correct"])
            score = list(prediction_df["score"])

            if len(correct) != 0:

                accs.append(correct.count(True)/len(correct))
                avg_scores.append(sum(score) / len(score))
                max_scores.append(max(score))
                min_scores.append(min(score))
                target_scores.append(row*col)
                norm_scores.append((sum(score) / len(score))/(row*col))
                format_wrong.append(False)

            else:
                accs.append(0.0)
                avg_scores.append(0.0)
                max_scores.append(0.0)
                min_scores.append(0.0)
                target_scores.append(row*col)
                norm_scores.append(0.0)
                format_wrong.append(True)


    eval_df_3_cols[f"Lv{level}-acc"] = accs
    eval_df_3_cols[f"Lv{level}-target_score"] = target_scores
    eval_df_3_cols[f"Lv{level}-avg_score"] = avg_scores
    eval_df_3_cols[f"Lv{level}-max_score"] = max_scores
    eval_df_3_cols[f"Lv{level}-min_score"] = min_scores
    eval_df_3_cols[f"Lv{level}-norm_score"] = norm_scores
    eval_df_3_cols[f"Lv{level}-format_wrong"] = format_wrong
    
    


print(eval_df_3_cols)
eval_df_3_cols.to_csv(f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-zeroShot/orig_puzzles/general_metrics/Level_2-7_{typ}_eval_cleaned.tsv", sep="\t", index=False)

eval_df_2x2 = pd.DataFrame()
for level in [6, 9]:
    sizes = []
    accs = []
    avg_scores = []
    max_scores = []
    min_scores = []
    target_scores = []
    norm_scores = []
    format_wrong = []
    for row in range(2, 8):
        for col in range(2, 8):
            sizes.append(f"{row}x{col}")
    eval_df_2x2["sizes"] = sizes
    for row in range(2, 8):
        for col in range(2, 8):
            prediction_file = f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-{setup}/{typ}_puzzles/Level{level}/eval/{row}x{col}-level{level}_{typ}_solution_eval.tsv"
            prediction_df = pd.read_csv(prediction_file, sep="\t")
            preds = len(prediction_df["correct"])
            all_preds += preds
            prediction_df = prediction_df[prediction_df["formatting"]==True]
            format += preds - len(prediction_df["correct"])

            correct = list(prediction_df["correct"])
            score = list(prediction_df["score"])

            if len(correct) != 0:

                accs.append(correct.count(True)/len(correct))
                avg_scores.append(sum(score) / len(score))
                max_scores.append(max(score))
                min_scores.append(min(score))
                target_scores.append(row*col)
                norm_scores.append((sum(score) / len(score))/(row*col))
                format_wrong.append(False)

            else:
                accs.append(0.0)
                avg_scores.append(0.0)
                max_scores.append(0.0)
                min_scores.append(0.0)
                target_scores.append(row*col)
                norm_scores.append(0.0)
                format_wrong.append(True)


    eval_df_2x2[f"Lv{level}-acc"] = accs
    eval_df_2x2[f"Lv{level}-target_score"] = target_scores
    eval_df_2x2[f"Lv{level}-avg_score"] = avg_scores
    eval_df_2x2[f"Lv{level}-max_score"] = max_scores
    eval_df_2x2[f"Lv{level}-min_score"] = min_scores
    eval_df_2x2[f"Lv{level}-norm_score"] = norm_scores
    eval_df_2x2[f"Lv{level}-format_wrong"] = format_wrong
    
print(eval_df_2x2)
eval_df_2x2.to_csv(f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-zeroShot/orig_puzzles/general_metrics/Level_6-9_{typ}_eval_cleaned.tsv", sep="\t", index=False)

eval_df_3x3 = pd.DataFrame()
for level in [10, 11, 12]:
    sizes = []
    accs = []
    avg_scores = []
    max_scores = []
    min_scores = []
    target_scores = []
    norm_scores = []
    format_wrong = []
    for row in range(3, 8):
        for col in range(3, 8):
            sizes.append(f"{row}x{col}")
    eval_df_3x3["sizes"] = sizes
    for row in range(3, 8):
        for col in range(3, 8):
            prediction_file = f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-{setup}/{typ}_puzzles/Level{level}/eval/{row}x{col}-level{level}_{typ}_solution_eval.tsv"
            prediction_df = pd.read_csv(prediction_file, sep="\t")
            preds = len(prediction_df["correct"])
            all_preds += preds
            prediction_df = prediction_df[prediction_df["formatting"]==True]
            format += preds - len(prediction_df["correct"])

            correct = list(prediction_df["correct"])
            score = list(prediction_df["score"])

            if len(correct) != 0:
                accs.append(correct.count(True)/len(correct))
                avg_scores.append(sum(score) / len(score))
                max_scores.append(max(score))
                min_scores.append(min(score))
                target_scores.append(row*col)
                norm_scores.append((sum(score) / len(score))/(row*col))
                format_wrong.append(False)

            else:
                accs.append(0.0)
                avg_scores.append(0.0)
                max_scores.append(0.0)
                min_scores.append(0.0)
                target_scores.append(row*col)
                norm_scores.append(0.0)
                format_wrong.append(True)


    eval_df_3x3[f"Lv{level}-acc"] = accs
    eval_df_3x3[f"Lv{level}-target_score"] = target_scores
    eval_df_3x3[f"Lv{level}-avg_score"] = avg_scores
    eval_df_3x3[f"Lv{level}-max_score"] = max_scores
    eval_df_3x3[f"Lv{level}-min_score"] = min_scores
    eval_df_3x3[f"Lv{level}-norm_score"] = norm_scores
    eval_df_3x3[f"Lv{level}-format_wrong"] = format_wrong
    

print(eval_df_3x3)
eval_df_3x3.to_csv(f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-zeroShot/orig_puzzles/general_metrics/Level_10-11-12_{typ}_eval_cleaned.tsv", sep="\t", index=False)

print(format, all_preds, format/all_preds)