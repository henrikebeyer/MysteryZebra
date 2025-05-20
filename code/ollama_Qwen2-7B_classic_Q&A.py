import ollama
import re
import csv
import sys
import pandas as pd

#classic = sys.argv[1]
#type = sys.argv[2]

#if type == "orig":

Einstein_step_dict = {"norwegian":1, "milk":1,
                      "blue":2,
                      "green":3, "coffee":3, "white":3,
                      "british":4, "red":4, "yellow":4,
                      "dunhill":5, "horse":5,
                      "danish":6, "tea":6, "cat":6, "beer":6, "bluemaster":6, "water":6, "blend":6,
                      "german":7, "prince":7, "swedish":7, "dog":7,
                      "bird":9, "pall-mall":9,
                      "fish":9}


Zebra_step_dict = {"norwegian":1, "milk":1,
                   "blue":2,
                   "yellow":3, "kools":3, "horse":3,
                   "ukrainian":4, "tea":4,
                   "water":5,
                   "ivory":6, "green":6, "coffee":6,
                   "orange-juice":7, "lucky-strike":7,
                   "japanese":8, "parliament":8, "spanish":8, "dog":8, "old-gold":8, "snails":8, "red":8, "english":8,
                   "fox":9, "chesterfield":9,
                   "zebra":10}

classic = "Zebra"
type = "orig_NL"
n = ""

puzzle_file = f"/home/oenni/Dokumente/LLM_reasoning/Puzzles_Natural_Language/Puzzles_orig/Puzzles_{classic}_{type}/{classic}_{n}{type}"

with open(puzzle_file, "r") as fin:
    puzzle = fin.read().strip("\n")

#out_file = f"/home/henrike/LLM_reasoning/testing_results/LLaMa3.1-70B-zeroShot/{type}_puzzles/{classic}_{type}/{classic}_{type}_zeroShot.tsv"

layout = puzzle.split("\n\n")[0].split("::.")[1]

if classic == "Zebra" and type == "orig":
    clues = puzzle.split(":\n\n")[1].split(".::")[0]
else:
    clues = puzzle.split("\n\n")[1].replace("##1","").replace(".:: Answer", "")
grid = [line.lower().strip().split("|")[1:5+2] for line in puzzle.split(".:: Answer ::.")[-1].split("\n")[2:5+2]]
for n in range(5):
    for m in range(5+1):
        grid[n][m] = grid[n][m].lower().strip()

original_file = f"/home/oenni/Dokumente/LLM_reasoning/Puzzles_Natural_Language/Puzzles_orig/Puzzles_{classic}_orig_NL/{classic}_orig_NL"
with open(original_file, "r") as fin:
    puzzle = fin.read().strip("\n")

#out_file = f"/home/henrike/LLM_reasoning/testing_results/LLaMa3.1-70B-zeroShot/{type}_puzzles/{classic}_{type}/{classic}_{type}_zeroShot.tsv"

#layout_orig = puzzle.split("\n\n")[0].split("::.")[1]

#print("orig layout", layout_orig)

#if classic == "Zebra" and type == "orig":
#    clues = puzzle.split(":\n\n")[1].split(".::")[0]
#else:
#    clues = puzzle.split("\n\n")[1].replace("##1","").replace(".:: Answer", "")
grid_orig = [line.lower().strip().split("|")[1:5+2] for line in puzzle.split(".:: Answer ::.")[-1].split("\n")[2:5+2]]
for n in range(5):
    for m in range(5+1):
        grid_orig[n][m] = grid_orig[n][m].lower().strip()

item_dict = {}

for row_orig, row in zip(grid_orig, grid):
    for col in range(1,5+1):
        item_dict[row[col]] = row_orig[col]

for k, v in item_dict.items():
    print(k,v)

items = ", ".join(list(re.findall(": [A-Za-z-7& ,]+", layout.replace("  ", " ")))).replace(": ","").replace(" and ", ", ").replace(" or ", ", ").split(", ")

print("puzzle layout", layout)
#print(clues)
print(items)
#print(answer)



for item in items:
    question = item.lower().strip()

    #print(question)
    #print(item_dict[question])

    
    solution = 0

    for line in grid:
        if question in line:
            solution = line.index(question.lower())

    #print(solution)
    #if classic == "Zebra":
        #print("in solution step:", Zebra_step_dict[item_dict[question]])
    #else:
        #print("in solution step:", Einstein_step_dict[item_dict[question]])

    #for i in [1, 2, 3]:
    prompt = f"Solve the following logic puzzle: {layout}\n{clues} \n\n After solving tell me where is **{question}**. Give the answer in the format **{question}:Num**."


    words = prompt.split()
    (print(words))
    print(len(words))
    #print(prompt)

    #print(prompt)
    """answer = ollama.generate(model='mistral:latest', prompt=prompt)

    response = answer["response"]

    print(response)"""

    #with open(out_file, "a") as fout:
    #    csv_writer = csv.writer(fout, delimiter="\t")
    #    csv_writer.writerow([f"{classic}_{type}_{i}", response])"""