import ollama
import re
import csv
import sys
import ast
import os
import pandas as pd

#model = sys.argv[1]
#classic = sys.argv[2]
#type = sys.argv[3]
#n = sys.argv[4]

step_dict = {"Einstein": {"norwegian":1, "milk":1,
                          "blue":2,
                          "green":3, "coffee":3, "white":3,
                          "british":4, "red":4, "yellow":4,
                          "dunhill":5, "horse":5,
                          "danish":6, "tea":6, "cat":6, "beer":6, "bluemaster":6, "water":6, "blend":6,
                          "german":7, "prince":7, "swedish":7, "dog":7,
                          "bird":8, "pall-mall":8,
                          "fish":9},
            "Zebra":{"norwegian":1, "milk":1,
                   "blue":2,
                   "yellow":3, "kools":3, "horse":3,
                   "ukrainian":4, "tea":4,
                   "water":5,
                   "ivory":6, "green":6, "coffee":6,
                   "orange-juice":7, "lucky-strike":7,
                   "japanese":8, "parliament":8, "spanish":8, "dog":8, "old-gold":8, "snails":8, "red":8, "english":8,
                   "fox":9, "chesterfield":9,
                   "zebra":10}
}

classic = "Zebra"
typ = "orig"

# we need the original puzzle for reference of positions in the solution grid
original_file = f"../corpus/part1/{classic}/{classic}_orig_NL.csv"
puzzle_file = f"../corpus/part1/{classic}/{classic}_{typ}.csv"

try:
    out_dir = f"../Model_testing/{model}-zeroShot/case_study/{typ}_puzzles/{classic}_lexical_replacements"
    os.makedirs(out_dir)
except:
    pass

puzzle_df = pd.read_csv(puzzle_file)
orig_df = pd.read_csv(original_file)
orig_grid = ast.literal_eval(orig_df["SolutionGrid"][0])

puzzles = puzzle_df["Clues"]
solutions = puzzle_df["SolutionGrid"]
idx = puzzle_df["ID"]

for id, puzzle, solution in zip(idx, puzzles, solutions):
    # match up items in original and manipulated puzzle
    item_dict = {}
    solution_dict = {}
    puzzle_grid = ast.literal_eval(solution)

    for orig_items, puzzle_items in zip(orig_grid.values(), puzzle_grid.values()):
        for orig_item, puzzle_item, i in zip(orig_items, puzzle_items, range(6)):
            item_dict[puzzle_item] = orig_item
            solution_dict[puzzle_item] = i
    
    for item in item_dict.keys():
        prompt = f"Solve the following logic puzzle: \n\n{puzzle}\n\nAfter solving tell me where is **{item}**. Give the answer in the format **{item}:Num**."

        answer = ollama.generate(model=model, prompt=prompt)
        response = answer["response"]

        print(item, step_dict[classic][item_dict[item]])

        with open(f"{out_dir}/{classic}_{typ}_zeroShot.tsv", "a") as fout:
            csv_writer = csv.writer(fout, delimiter="\t")
            csv_writer.writerow([id, item, step_dict[classic][item_dict[item]], response, f"{item}:{solution_dict[item]}"])
