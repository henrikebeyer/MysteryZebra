""" Evaluation Script for the """

import pandas as pd
import re
import os

model = "o1"
setup = "zeroShot"
typ = "orig"
level = 3

rows = 1
cols = 5
re.MULTILINE

def extract_table_to_dict(markdown):
        """
        Extracts data from a table into a dictionary.

        Args:
        - table (list of lists): A 2D list representing the table (e.g., from a CSV or manually input).

        Returns:
        - dict: A dictionary with the first column as keys and corresponding row/column data as values.
        """

        lines = markdown.lower().replace("#","").replace("position", "").replace("drink", "beverage").replace(" music ", "music-genre").replace("vehicle", "transport").strip().split('\n')
        table = [line.split('|')[1:] for line in lines]  # Split by '|' and ignore the first empty column
        table = [[cell.strip() for cell in row] for row in table]  # Strip leading/trailing spaces from each cell
        #print(table)
        result = {}

        helper_header = [""]+[str(i) for i in range(1,len(table[0])-1)] + [""] # first [""] and -1 needs to be removed sometimes
        #print(helper_header)
        key_1 = ""
        x = 1
        #if table [0] == helper_header:
        #print("here")
        for row in table:
            if row != []:
                key = row[0].lower()  # First column is key
                #print(key)
                if len(key)>0 and key[0] != "-":
                    values = row[1:-1]  # Rest of the columns are values
                    # Only add non-empty values
                    result[key] = [v.lower() for v in values]

                    
        return result

def eval_classic(model, setup, n, typ, classic):
    words = 0
    prediction_file = f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-{setup}/{model}-{classic}_{n}{typ}_{setup}.tsv"

    # get the solution grid as a dictionary
    solutions = []
    if typ in ["orig", "orig_NL"]:
        for i in range(3):
            solution_file = f"/home/oenni/Dokumente/LLM_reasoning/Puzzles_Natural_Language/Puzzles_orig/Puzzles_{classic}_{typ}/{classic}_{typ}"

            with open(solution_file, "r") as fin:
                solution_puzzles = [puzzle.split(".:: Answer ::.")[-1].strip() for puzzle in fin.read().split("#################################\n")[:10]]

            for puzzle in solution_puzzles:

                solution_list = [line.strip("|").split("|") for line in puzzle.split("\n")[1:]]

                solution_dict = {}
                for line in solution_list:
                    for i in range(len(line)):
                        line[i] = line[i].strip().lower()
                    solution_dict[line[0]] = line[1:]

                solutions.append(solution_dict)
    else:
        for i in [0, 1, 2]:
            solution_file = f"/home/oenni/Dokumente/LLM_reasoning/Puzzles_Natural_Language/Puzzles_{typ}/Puzzles_{classic}_{typ}/{classic}_{n}{typ}_Natural_Language-{i}"

            with open(solution_file, "r") as fin:
                solution_puzzles = [puzzle.split(".:: Answer ::.")[-1].strip() for puzzle in fin.read().split("#################################\n")[:10]]
            for puzzle in solution_puzzles:

                solution_list = [line.strip("|").split("|") for line in puzzle.split("\n")[1:]]

                solution_dict = {}
                for line in solution_list:
                    for i in range(len(line)):
                        line[i] = line[i].strip().lower()
                    solution_dict[line[0]] = line[1:]

                solutions.append(solution_dict)

    #print(solution_dict)

    # get the clean predicted grids
    prediction_df = pd.read_csv(prediction_file, sep="\t",header=0, names=["id", "output", "solution"])
    
    #print(prediction_df)


    preds = prediction_df["output"]
    #print(preds[1])

    #print(preds[8])

    # Define the pattern
    pattern = r'((\|(.*?\|){1,8}?\n){2,9})'

    predictions = []
  

    # Sample text input
    for text in preds:
        if typ=="orig" and classic=="Einstein" and not "NL" in prediction_file:
            text = text.lower().replace("dane","danish").replace("brit ", "british ").replace("swede","swedish").replace("cats", "cat").replace("birds", "bird").replace("dogs","dog").replace("pall mall", "pall-mall").replace("horses","horse")
        elif typ == "orig" and classic=="Zebra" and "NL" in prediction_file:
            text = text.lower().replace("parliaments", "parliament").replace("chesterfields", "chesterfield")
        elif typ == "orig" and classic=="Zebra" and not "NL" in prediction_file:
            text = text.lower().replace("englishman", "english").replace("spaniard", "spanish").replace("parliaments", "parliament").replace("chesterfields", "chesterfield").replace("orange juice", "orange-juice").replace("old gold", "old-gold").replace("lucky strike", "lucky-strike")
        elif n==2 and typ == "domain_replacements" and classic=="Einstein":
            text = text.lower().replace("new york", "new-york").replace("ice hockey", "ice-hockey").replace("swede", "swedish").replace("chesterfields", "chesterfield").replace("orange juice", "orange-juice").replace("old gold", "old-gold").replace("lucky strike", "lucky-strike")
        elif n==3 and typ == "domain_replacements" and classic=="Einstein":
            text = text.lower().replace("san francisco", "san-francisco").replace("new york","new-york").replace("nurseerman", "nurseryman").replace("swede","swedish")
        #if not text.startswith("To solve this logic puzzle, we need to systematically place each piece of information into the table and deduce the correct positions step-by-step."): # add in this line for lv 1 5x3
        # Use re.findall to extract the table content
        text = text.replace("lucky strike", "lucky-strike")
        words += len(text.split())
        #matches = list(re.findall(pattern, text.strip()))

        # Print the results
        #for match in matches:
        #    print(match.strip(),"\n")
        #print("\n\n")
        """if len(matches) >= 1:    
            predictions.append(extract_table_to_dict(matches[-1][0]))
            #print(matches[-1])
        elif len(matches) == 0:
            predictions.append({})
            #print(matches[-1])
        #else: 
        #    predictions.append({})

    #for pred in predictions:
        #print(pred)
    #print("\n")
    correct = []
    scores = []
    formatting = []
    #print(len(solutions))
    for solution, pred in zip(solutions, predictions):
        #print(pred)
        score = 0
        target_score = 25
        if not all(domain in list(pred.keys()) for domain in list(solution.keys())):
            print(i)
            #print(solution.keys())
            #for k_pred, v_pred in pred.items():
                #print(k_pred, v_pred)
            pred = {}
        i += 1
        if pred != {}:
            formatting.append(True)
            for key in solution.keys():
                for pred_item, solution_item in zip(pred[key], solution[key]):
                    solution_item = solution_item.replace("ukranian", "ukrainian").replace("chesterfields", "chesterfield").replace("parliaments", "parliament").replace("pall mall", "pall-mall").replace("dogs", "dog").replace("cats", "cat").replace("horses", "horse").replace("birds", "bird").replace("brit", "british").replace("swede", "swedish").replace("dane", "danish").replace("britishish", "british").replace("parliamentss", "parliaments").replace("chesterfieldss", "chesterfields")
                    pred_item = pred_item.replace("old gold", "old-gold").replace("orange juice", "orange-juice").replace("lucky strike", "lucky-strike")
                    if len(pred_item) > 1:
                        if pred_item == solution_item:
                            score += 1
                        else:
                            print(pred_item, solution_item)
                    else:
                        if pred_item != "" and (pred_item[0] == solution_item[0]):
                            score += 1
        else:
            formatting.append(False)
        scores.append(score)
        if score == target_score:
            correct.append(True)
        else:
            correct.append(False)

    #print(len(predictions))
    #print(formatting)
    prediction_df["predicted_grid"] = predictions
    prediction_df["formatting"] = formatting
    prediction_df["score"] = scores
    prediction_df["correct"] = correct

    print(prediction_df)

    out_dir = f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-{setup}/eval/"
    try:
        os.makedirs(out_dir)
    except:
        pass"""

    return(words)
    #prediction_df.to_csv(f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-{setup}/eval/{classic}_{n}{typ}_solution_eval.tsv", sep="\t", index=False)

word_ct = 0

for model in ["o1"]:
    for classic in ["Zebra", "Einstein"]:
        for typ in ["orig", "orig_NL", "lexical_replacements", "domain_replacements"]:
            print(classic, typ)
            if typ == "domain_replacements":
                for n in range(1, 6):
                    print(n)
                    word_ct += eval_classic(setup=setup, model=model, n=n, typ=typ, classic=classic)
            else:
                word_ct += eval_classic(setup=setup, model=model, n="", typ=typ, classic=classic)

print(word_ct)

#eval_classic(setup=setup, model=model, n=5, typ="domain_replacements", classic="Zebra")

def eval_preds(model, setup, typ, level, rows, cols):
    solution_file = f"/home/oenni/Dokumente/LLM_reasoning/Puzzles_Natural_Language/Puzzles_{typ}/Puzzles_Level{level}_{typ}_Natural_Language/{rows}x{cols}-level{level}_{typ}_Natural_Language"

    prediction_file = f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-{setup}/orig_puzzles/Level{level}/{rows}x{cols}-level{level}_{typ}_solution.tsv"

    # get the solution grid as a dictionary
    solutions = []

    with open(solution_file, "r") as fin:
        solution_puzzles = [puzzle.split(".:: Answer ::.")[-1].strip() for puzzle in fin.read().split("#################################\n")[:10]]

    for puzzle in solution_puzzles:

        solution_list = [line.strip("|").split("|") for line in puzzle.split("\n")[1:]]

        solution_dict = {}
        for line in solution_list:
            for i in range(len(line)):
                line[i] = line[i].strip().lower()
            solution_dict[line[0]] = line[1:]

        solutions.append(solution_dict)


    #print(solution_dict)

    # get the clean predicted grids
    prediction_df = pd.read_csv(prediction_file, sep="\t", names=["Puzzle-ID", "output"])
    
    #print(prediction_df)


    preds = prediction_df["output"]

    #print(preds[8])

    # Define the pattern
    #pattern =  r"(?:#{13}\n)?((?:\|(?:.*?\|){0,20}+\n)+)(?:#{13}\n)"
    #pattern = pattern = r'#############\n(\|[\s\S]*?\|(?:\s*\n\|[\s\S]*?\|){0,7})\n?#############'
    pattern = r'((\|(.*?\|){1,8}?\n){2,9})'


    predictions = []

    

    # Sample text input
    #i= 0
    for text in preds:
        
        #print(i)
        #i+=1
        #print(text)
        #if not text.startswith("To solve this logic puzzle, we need to systematically place each piece of information into the table and deduce the correct positions step-by-step."): # add in this line for lv 1 5x3
        # Use re.findall to extract the table content
        matches = re.findall(pattern, text, )
        
        # Print the results
        #for match in matches:
            #print(match.strip(),"\n")
        #print("\n\n")
        if len(matches) >= 1:
        #    print(type(matches[-1]))    
            #print(matches[-1].group(0))
            tbl = re.sub(r'\|(\s?-+?\s?\|){1,8}\n', '', str(matches[-1][0]))
            predictions.append(extract_table_to_dict(tbl))
            #print(tbl)
            #print("\n\n")
        elif len(matches) == 0:
            predictions.append({})
            #print(matches[-1])
        #else: 
        #    predictions.append({})

    #for pred in predictions:
        #print(pred)
    correct = []
    scores = []
    formatting = []
    i = 0
    for solution, pred in zip(solutions, predictions):
        score = 0
        correct.append(pred == solution)
        if not all(domain in list(pred.keys()) for domain in list(solution.keys())):
            print(i)
            print(solution.keys())
            for k_pred, v_pred in pred.items():
                print(k_pred, v_pred)
            pred = {}
        i += 1
        if pred != {}:
            formatting.append(True)
            for pred_row, solution_row in zip(solution.values(), pred.values()):
                for pred_item, solution_item in zip(pred_row, solution_row):
                    #print(pred_item, solution_item)
                    if len(pred_item) > 1:
                        if pred_item == solution_item:
                            score += 1
                    else:
                        if pred_item[0] == solution_item[0]:
                            score += 1
        else:
            formatting.append(False)
        scores.append(score)

    #print(len(predictions))

    prediction_df["predicted_grid"] = predictions

    prediction_df["formatting"] = formatting
    prediction_df["score"] = scores
    prediction_df["correct"] = correct

    print(prediction_df)
    prediction_df.to_csv(f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/{model}-{setup}/{typ}_puzzles/Level{level}/eval/{rows}x{cols}-level{level}_{typ}_solution_eval.tsv", sep="\t", index=False)

#eval_preds(model=model, setup=setup, typ=typ, level=1, rows=5, cols=3)

#################################################
##### Obfuscations for levels 1, 3, 4, 5, 8 #####
#################################################
#for lv in [1, 3, 4, 5, 8]:#[1, 3, 4, 5, 8]:
#    for i in range(1,8):
#        for j in range(2,8):
#            print("level=", lv, i, "x", j)
#            eval_preds(model=model, setup=setup, typ=typ, level=lv, rows=i, cols=j)

########################################
##### Obfuscations for levels 2, 7 #####
########################################
#for lv in [2, 7]:
#    for i in range (1, 8):
#        for j in range(3, 8):
#            print("level=", lv, i, "x", j)
#            eval_preds(model=model, setup=setup, typ=typ, level=lv, rows=i, cols=j)

##############################################
##### Obfuscations for levels 10, 11, 12 #####
##############################################
#for lv in [10, 11, 12]: #[10, 11, 12]:
#    for i in range(3, 8):
#        for j in range(3, 8):
#            print("level=", lv, i, "x", j)
#            eval_preds(model=model, setup=setup, typ=typ, level=lv, rows=i, cols=j)

########################################
##### Obfuscations for levels 6, 9 #####
########################################
#for lv in [6, 9]: #[6, 9]:
#    for i in range(2, 8):
#        for j in range(2, 8):
#            print("level=", lv, i, "x", j)
#            eval_preds(model=model, setup=setup, typ=typ, level=lv, rows=i, cols=j)