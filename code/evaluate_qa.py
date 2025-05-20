import pandas as pd
import re
import os
from numpy import where

#model = "LLaMa3.1-70B"
#typ = "orig"
#classic = "Einstein"
#n = ""

def reformat_GPT(model, classic, typ):
    prediction_file = f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-zeroShot/qa_format/solution_steps/{typ}_puzzles/{classic}_{typ}/{classic}_{typ}_zeroShot.tsv"
    prediction_df = pd.read_csv(prediction_file, sep="\t", names=["id", "target", "step", "pred", "solution"])
    #print(prediction_df)

    #correct_step = [int(solution.split(":")[1]) for solution in prediction_df["solution"]]
    #prediction_df["step"] = correct_step

    for step in sorted(set(prediction_df["solution"])):
        print(step)
    
    #for i in range(1, 4):
    #    pred_ids = [f"Einstein_orig_{item}-{i}" for item in list(prediction_df["target"])]
    #    pred_df = prediction_df[["target", "step", f"pred{i}", "solution"]]
    #    pred_df.loc[:,"id"] = pred_ids
    #    pred_df = pred_df.rename(columns={f"pred{i}":"pred"}, errors="raise")
    #    pred_df = pred_df.loc[:, ["id", "target", "step", "pred", "solution"]]
    #    df_list.append(pred_df)

    #pred_df = pd.concat(df_list)

    #print(pred_df)

    #prediction_df.to_csv(prediction_file, sep="\t", index=False)
    #pred_df.to_csv(prediction_file, sep="\t", index=False)

#for model in ["ChatGPT", "o1"]:
#    for classic in ["Einstein", "Zebra"]:
#        for typ in ["orig", "orig_NL", "lexical_replacements", "domain_replacements"]:
#            print(model, classic, typ)
#            reformat_GPT(model, classic, typ)


def eval_QA(model, classic, typ):

    words = 0
    # read in prediction dataframe
    prediction_file = f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-zeroShot/qa_format/solution_steps/{typ}_puzzles/{classic}_{typ}/{classic}_{typ}_zeroShot.tsv"
    prediction_df = pd.read_csv(prediction_file, sep="\t", names=["id", "target", "step", "pred", "solution"])

    #print(prediction_df)

    # extract columns with predictions and correct solution
    preds = prediction_df["pred"]
    solutions = prediction_df["solution"]
    items = prediction_df["target"]

    # create lists for target columns to capture correct and 
    pred_item = []
    format = []

    for pred, solution_item, solution in zip(preds, items, solutions):
        pred = pred.lower().replace("**", "").replace(" house ", "").replace("num = ", "").replace("num", "").replace("#", "").replace("(", "").replace(")","").replace("position", "").replace("=", ":").replace("ukranian", "ukrainian").replace("orange juice", "orange-juice").replace(" is:", ":").replace(".","")
        solution_item = solution_item.lower().replace("ukranian", "ukrainian")
        solution = solution.replace("ukranian", "ukrainian").replace("brit:","british:").replace("dane:","danish:").replace("swede:","swedish:").replace("cats:","cat:").replace("birds:","bird:").replace("horses","horse").replace("dogs:","dog:")
        pattern = solution_item+r"\s*:\s*p?\s?n?c?b?\d+"
        matches = list(re.findall(pattern, pred))

        translation_dict = {"brit:":"british:",
                            "dane:":"danish:",
                            "swede:":"swedish:",
                            "cats:":"cat:",
                            "birds":"bird:",
                            "horses":"horse",
                            "dogs:":"dog:"}
        
        words += len(pred.split())
        #print(matches)
        """if matches != []:
            match = matches[-1].strip().replace("  ", "").replace(" ", "").replace(":b", ":").replace(":c",":").replace(":p",":").replace("\n","").replace("brit:","british:").replace("dane:","danish:").replace("swede:","swedish:").replace("cats:","cat:").replace("birds:","bird:").replace("horses","horse").replace("dogs:","dog:").replace("pallmall", "pall mall")
            #print(match)
            if match == solution:
                pred_item.append(match)
                format.append(True)
            else:
                pred_item.append(match)
                format.append(True)

        elif matches == []:
            #print(model, classic, typ)
            #print(pred.split("\n")[-1], solution_item)
            format.append(False)
            pred_item.append(None)

    prediction_df["pred_item"] = pred_item
    prediction_df["format"] = format
    prediction_df["correct"] = where(prediction_df["pred_item"]==prediction_df["solution"], True, False)
    print(prediction_df[prediction_df["target"]=="milk"])

    #print(prediction_df)

    out_dir = f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-zeroShot/qa_format/solution_steps/eval"
    try:
        os.makedirs(out_dir)
    except:
        pass

    out_file = f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-zeroShot/qa_format/solution_steps/eval/{classic}_{typ}_zeroShot_eval.tsv"

    prediction_df.to_csv(out_file, sep="\t", index=False)"""
        
    return(words)


word_ct = 0
for model in ["ChatGPT", "o1"]: #, "LLaMa3", "LLaMa3.1-70B", "LLaMa3.3-70B", "Mistral", "Qwen2-72B", "Qwen2"]:
    for classic in ["Einstein", "Zebra"]:
        for typ in ["orig", "orig_NL", "lexical_replacements", "domain_replacements"]:
            word_ct+=eval_QA(model=model, classic=classic, typ=typ)

print(word_ct/2)