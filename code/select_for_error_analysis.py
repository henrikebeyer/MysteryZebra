import pandas as pd

model = "R1"

df_list = []

for classic in ["Einstein", "Zebra"]:
    for obfuscation in ["orig_NL", "lexical_replacements", "domain_replacements","orig"]:
        if obfuscation == "domain_replacements":
            for i in range(1,6):
                prediction_file = f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-zeroShot/eval/{classic}_{i}{obfuscation}_solution_eval.tsv"
                prediction_df = pd.read_csv(prediction_file, sep="\t")
                df_list.append(prediction_df)
        else:
            prediction_file = f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-zeroShot/eval/{classic}_{obfuscation}_solution_eval.tsv"
            prediction_df = pd.read_csv(prediction_file, sep="\t")
            df_list.append(prediction_df)

if model not in ["o1", "ChatGPT", "R1"]:
    for level in [1, 3, 4, 5, 8]:
        for row in range(1, 6):
            for col in range(2, 6):
                prediction_file = f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-zeroShot/orig_puzzles/Level{level}/eval/{row}x{col}-level{level}_orig_solution_eval.tsv"
                prediction_df = pd.read_csv(prediction_file, sep="\t")
                df_list.append(prediction_df)

    for level in [2, 7]:
        for row in range(1, 6):
            for col in range(3, 6):
                prediction_file = f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-zeroShot/orig_puzzles/Level{level}/eval/{row}x{col}-level{level}_orig_solution_eval.tsv"
                prediction_df = pd.read_csv(prediction_file, sep="\t")
                df_list.append(prediction_df)

    for level in [6, 9]:
        for row in range(2, 6):
            for col in range(2, 6):
                prediction_file = f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-zeroShot/orig_puzzles/Level{level}/eval/{row}x{col}-level{level}_orig_solution_eval.tsv"
                prediction_df = pd.read_csv(prediction_file, sep="\t")
                df_list.append(prediction_df)

    for level in [10, 11, 12]:
        for row in range(3, 6):
            for col in range(3, 6):
                prediction_file = f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-zeroShot/orig_puzzles/Level{level}/eval/{row}x{col}-level{level}_orig_solution_eval.tsv"
                prediction_df = pd.read_csv(prediction_file, sep="\t")
                df_list.append(prediction_df)

all_pred = pd.concat(df_list)

false_pred = all_pred[all_pred["correct"]==False]

if model in ["ChatGPT", "o1", "R1"]:
    error_analysis = false_pred.sample(n = 20)

else:
    error_analysis = false_pred.sample(n=50)

error_analysis.to_csv(f"/home/oenni/Dokumente/LLM_reasoning/error_analysis/{model}-zeroShot_error_analysis.tsv", index=False, sep="\t")