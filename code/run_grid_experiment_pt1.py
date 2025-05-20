"""
Experimental code to run grid-format experiments for Part1 of Mystery Zebra

System Variables:
1 - model name as appearing in ollama
2 - name of classic puzzle to be solved ["Einstein", "Zebra"]
3 - variant name ["orig", "orig_NL", "lexical_replacements", "domain_replacements]
4 - number of domains (1-5); only to be passed with "domain_replacements", otherwise pass empty string
"""
import ollama
import re
import csv
import sys
import os
import ast
import pandas as pd

model = sys.argv[1]
classic = sys.argv[2]
typ = sys.argv[3]
n = sys.argv[4]

puzzle_file = f"../corpus/part1/{classic}/{classic}_{n}{typ}.csv"

try:
    out_dir = f"../Model_testing/{model}-zeroShot/Pt1/{classic}"
    os.makedirs(out_dir)
except:
    pass

puzzle_df = pd.read_csv(puzzle_file)

puzzles = puzzle_df["Clues"]
solutions = puzzle_df["SolutionGrid"]

for puzzle, solution in zip(puzzles[:1], solutions):
    solution = ast.literal_eval(solution)
    first_line = [str(i) for i in range(1, 6)]
    first_col = solution.keys()
    max = 0
    for domain in first_col:
        if len(domain) > max:
            max = len(domain)
    empty_grid = ""
    empty_grid += "| " + " "*max + " |"
    for i in range(1, 6):
        if i != 5:
            empty_grid += " "*5 + str(i) + " "*5 + "|"
        else:
            empty_grid += " "*5 + str(i) + " "*5 + "|\n"
    for domain in first_col:
        diff = max - len(domain)
        empty_grid += "| " + domain + " "*diff + " |"
        for i in range(1, 6):
            if i != 5:
                empty_grid += " "*11 + "|"
            else:
                empty_grid += " "*11 + "|\n"
    

    prompt = f"Please solve the following logic puzzle in the following table: \n\n{empty_grid}\n\nPuzzle: \n{puzzle}.\n\nPlease put '#############' around the final solution table."

    for i in range(3):
        #answer = ollama.generate(model=model, prompt=prompt)
        #response = answer["response"]

        response = "Some dummy response"

        with open(f"{out_dir}/{classic}_{n}{typ}_zeroShot.csv", "a") as fout:
            csv_writer = csv.writer(fout)
            csv_writer.writerow([f"{classic}_{typ}_{i}", response, solution])