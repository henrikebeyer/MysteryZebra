"""
Experimental code to run grid-format experiments for Part2 of Mystery Zebra

System Variables:
1 - model name as appearing in ollama
2 - level (1-12)
3 - number of rows (1-7)
4 - number of columns (2-7)
5 - number of experimental runs to be run per puzzle
"""
import ollama
import re
import csv
import sys
import os
import ast
import pandas as pd

model = sys.argv[1]
level = sys.argv[2]
rows = sys.argv[3]
cols = sys.argv[4]
runs = sys.argv[5]

puzzle_file = f"../Puzzles_Natural_Language/Puzzles_orig/Puzzles_Level{level}_orig_Natural_Language/{rows}x{cols}-level{level}_orig_Natural_Language"

try:
    out_dir = f"../Model_testing/{model}-zeroShot/Pt2/Level{level}"
    os.makedirs(out_dir)
except:
    pass

puzzle_df = pd.read_csv(puzzle_file)

puzzles = puzzle_df["Clues"]
solutions = puzzle_df["SolutionGrid"]

for puzzle, solution in zip(puzzles, solutions):
    solution = ast.literal_eval(solution)
    first_line = [str(i) for i in range(1, cols)]
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
        for i in range(1, cols):
            if i != 5:
                empty_grid += " "*11 + "|"
            else:
                empty_grid += " "*11 + "|\n"
    

    prompt = f"Please solve the following logic puzzle in the following table: \n\n{empty_grid}\n\nPuzzle: \n{puzzle}.\n\nPlease put '#############' around the final solution table."

    for j in range(runs):
        answer = ollama.generate(model=model, prompt=prompt)
        response = answer["response"]

        

        with open(f"{out_dir}/{rows}x{cols}_level{level}_orig_zeroShot-{j}.csv", "a") as fout:
            csv_writer = csv.writer(fout)
            csv_writer.writerow([f"{rows}x{cols}_level{level}_{i}", response, solution])