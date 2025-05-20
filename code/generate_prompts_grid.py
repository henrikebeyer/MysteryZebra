import re
import csv
import os
#from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, ConfusionMatrixDisplay
import pandas as pd

def generate_prompt(classic, type, n, x):
    if type == "lexical_replacements":
        puzzle_file = f"/home/oenni/Dokumente/LLM_reasoning/Puzzles_Natural_Language/Puzzles_{type}/Puzzles_{classic}_{type}/{classic}_{type}_Natural_Language-{x}"
    elif type == "domain_replacements":
        puzzle_file = f"/home/oenni/Dokumente/LLM_reasoning/Puzzles_Natural_Language/Puzzles_{type}/Puzzles_{classic}_{type}/{classic}_{n}{type}_Natural_Language-{x}"
    else:
        puzzle_file = f"/home/oenni/Dokumente/LLM_reasoning/Puzzles_Natural_Language/Puzzles_orig/Puzzles_{classic}_{type}/{classic}_{type}" 
    with open(puzzle_file, "r") as fin:
        puzzle = fin.read().strip("\n")

    try:
        out_directory = f"/home/oenni/Dokumente/LLM_reasoning/prompts/grid/{classic}"
        os.makedirs(out_directory)
    except:
        pass

    #puzzle_file = f"/home/henrike/LLM_reasoning/Puzzles_Natural_Language/Puzzles_{type}/Puzzles_{classic}_{type}/{classic}_{type}


    out_file = f"/home/oenni/Dokumente/LLM_reasoning/prompts/grid/{classic}/{classic}_{n}{type}_prompts-{x}.tsv"

    # extract solution grid from original for reference
    grid = [line.lower().strip().split("|")[1:5+2] for line in puzzle.split(".:: Answer ::.")[-1].split("\n")[1:5+2]]
    for n in range(1, 6):
        grid[n][0] = "|"+grid[n][0].replace("\t", " ")
        for m in range(1, 6):
            grid[n][m] = " "*9

    for n in range(6):
        grid[n] = "|".join(grid[n]).replace("\t", " "*4)

    grid = "|\n".join(grid)
    grid = "|"+grid

    layout = puzzle.split("\n\n")[0].split("::.")[1]

    # extract clues from target puzzle
    if classic == "Zebra" and type == "orig":
        clues = puzzle.split(":\n\n")[1].split(".::")[0]
    else:
        clues = puzzle.split("\n\n")[1].replace("##1","").replace(".:: Answer", "")

    # create list of items in the puzzle
    items = ", ".join(list(re.findall(": [A-Za-z-7& ,]+", layout))).replace(": ","").replace(" and ", ", ").replace(" or ", ", ").split(", ")


    #print(layout)
    #print(clues)
    #print(grid)
    #print(answer)

    prompt = f"Please solve the following logic puzzle in the following table: \n\n{grid} \n\nPuzzle: \n {layout}\n\n{clues}. Please put '#############' around the final solution table."

    with open(out_file, "a") as fout:
        writer = csv.writer(fout, delimiter="\t")
        writer.writerow([f"{classic}-{type}-{x}", prompt])

for classic in ["Einstein", "Zebra"]:
    for type in ["orig", "orig_NL", "lexical_replacements", "domain_replacements"]:
        if type in ["lexical_replacements", "domain_replacements"]:
            for i in range(3):
                if type == "domain_replacements":
                    for n in range(1, 6):
                        generate_prompt(classic, type, n=n, x=i)
                else:
                    generate_prompt(classic, type, n="", x=i)
        else:
            generate_prompt(classic, type, "", "")