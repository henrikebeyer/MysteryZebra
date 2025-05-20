import ollama
import re
import csv
import sys
import pandas as pd

#classic = sys.argv[1]
#type = sys.argv[2]

#if type == "orig":

level = 1
rows = 3
cols = 3

puzzle_file = f"/home/oenni/Dokumente/LLM_reasoning/Puzzles_Natural_Language/Puzzles_orig/Puzzles_Level{level}_orig_Natural_Language/{rows}x{cols}-level{level}_orig_Natural_Language"

with open(puzzle_file, "r") as fin:
    puzzles = fin.read().split("#################################\n")[:-1]



for puzzle in puzzles[:1]:

#out_file = f"/home/henrike/LLM_reasoning/testing_results/LLaMa3.1-70B-zeroShot/{type}_puzzles/{classic}_{type}/{classic}_{type}_zeroShot.tsv"

    layout = puzzle.split("1.")[0].split("::.")[1]
    clues = "1." + puzzle.split("1.")[1].split(".::")[0].replace("##1","").replace(".::Answer::.", "")
    grid = [line.lower().strip().split("|")[1:cols+2] for line in puzzle.split(".:: Answer ::.")[-1].split("\n")[2:rows+2]]
    for n in range(rows):
        for m in range(cols+1):
            grid[n][m] = grid[n][m].lower().strip()

    items = ", ".join(list(re.findall(": [A-Za-z-7& ,]+", layout))).replace(": ","").replace(" and ", ", ").replace(" or ", ", ").split(", ")

    print(clues)
    print(layout)
    #print(items)
    #print(grid)

    question = []
    for item in items:
        if item.lower() not in clues.lower().replace("spaniard", "spanish").replace("orange juice", "orange-juice").replace("ukrainian", "ukranian").replace("old gold", "old-gold").replace("lucky strike", "lucky-strike"):
            question.append(item.lower().strip())

    #print(question[0])
    #print(answer)

    if question != []:
        solution = 0

        for line in grid:
            if question[0] in line:
                solution = line.index(question[0].lower())
        prompt = f"Solve the following logic puzzle and tell me where is {question[0]}. Give the answer in the format ***{question[0]}:Num*** . If you cannot determine a position use 'NA' for Num. {layout}\n{clues}"
        
        words = len(prompt.split())
        #answer = ollama.generate(model='mistral:latest', prompt=prompt)

        #response = answer["response"]

        #print(response, question[0], ":", solution)

    #with open(out_file, "a") as fout:
    #    csv_writer = csv.writer(fout, delimiter="\t")
    #    csv_writer.writerow([f"{classic}_{type}_{i}", response])"""