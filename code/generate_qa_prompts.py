import pandas as pd
import os
import re
import csv

model_dict = {"LLaMa3-7B":"llama3.1",
              "LLaMa3.1-70B":"llama3.1:70b",
              "LLaMa3.3-70B":"llama3.3",
              "Mistral-7B":"mistral:latest",
              "Qwen2":"qwen2.5",
              "Qwen2-72B":"qwen2.5:72b"
              }

# dictionaries capturing solution steps for the canonical puzzles
Einstein_step_dict = {"norwegian":1, "milk":1,
                      "blue":2,
                      "green":3, "coffee":3, "white":3,
                      "british":4, "red":4, "yellow":4,
                      "dunhill":5, "horse":5,
                      "danish":6, "tea":6, "cat":6, "beer":6, "bluemaster":6, "water":6, "blend":6,
                      "german":7, "prince":7, "swedish":7, "dog":7,
                      "bird":8, "pall-mall":8,
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

# read in puzzle file

def generate_prompt(classic, type):

    if type == "lexical_replacements":
        puzzle_file = f"/home/oenni/Dokumente/LLM_reasoning/Puzzles_Natural_Language/Puzzles_{type}/Puzzles_{classic}_{type}/{classic}_{type}_Natural_Language-0"
    elif type == "domain_replacements":
        n = 5
        puzzle_file = f"/home/oenni/Dokumente/LLM_reasoning/Puzzles_Natural_Language/Puzzles_{type}/Puzzles_{classic}_{type}/{classic}_{n}{type}_Natural_Language-0"
    else:
        puzzle_file = f"/home/oenni/Dokumente/LLM_reasoning/Puzzles_Natural_Language/Puzzles_orig/Puzzles_{classic}_{type}/{classic}_{type}" 
    with open(puzzle_file, "r") as fin:
        puzzle = fin.read().strip("\n")

    # create output directory
    try:
        out_directory = f"/home/oenni/Dokumente/LLM_reasoning/prompts/QA/{classic}"
        os.makedirs(out_directory)
    except:
        pass

    # read in original puzzle for reference
    original_file = f"/home/oenni/Dokumente/LLM_reasoning/Puzzles_Natural_Language/Puzzles_orig/Puzzles_{classic}_orig_NL/{classic}_orig_NL"
    with open(original_file, "r") as fin:
        puzzle_orig = fin.read().strip("\n")


    out_file = f"/home/oenni/Dokumente/LLM_reasoning/prompts/QA/{classic}/{classic}_{type}_prompts.tsv"

    # extract solution grid from original for reference
    grid_orig = [line.lower().strip().split("|")[1:5+2] for line in puzzle_orig.split(".:: Answer ::.")[-1].split("\n")[2:5+2]]
    for n in range(5):
        for m in range(5+1):
            grid_orig[n][m] = grid_orig[n][m].lower().strip()

    # extract layout from target puzzle
    layout = puzzle.split("\n\n")[0].split("::.")[1]

    # extract clues from target puzzle
    if classic == "Zebra" and type == "orig":
        clues = puzzle.split(":\n\n")[1].split(".::")[0]
    else:
        clues = puzzle.split("\n\n")[1].replace("##1","").replace(".:: Answer", "")

    # extract solution grid from target puzzle
    grid = [line.lower().strip().split("|")[1:5+2] for line in puzzle.split(".:: Answer ::.")[-1].split("\n")[2:5+2]]
    for n in range(5):
        for m in range(5+1):
            grid[n][m] = grid[n][m].lower().strip()

    # create list of items in the puzzle
    items = ", ".join(list(re.findall(": [A-Za-z-7& ,]+", layout))).replace(": ","").replace(" and ", ", ").replace(" or ", ", ").split(", ")

    # create a dictionary of original and puzzle items for reference
    item_dict = {}
    for row_orig, row in zip(grid_orig, grid):
        for col in range(1,5+1):
            item_dict[row[col]] = row_orig[col]

    # iterate over all items in the puzzle
    for item in items:
        question = item.lower().strip()

        solution = 0

        for line in grid:
            if question in line:
                solution = line.index(question.lower())

        if classic == "Zebra":
            solution_step = Zebra_step_dict[item_dict[question]]
        else:
            solution_step = Einstein_step_dict[item_dict[question]]

        print("running", classic, type, "for:", question)

        
        prompt = f"Solve the following logic puzzle: {layout}\n{clues} \n\n After solving tell me where is **{question}**. Give the answer in the format **{question}:Num**."
        print(prompt)

        with open(out_file, "a") as fout:
            writer = csv.writer(fout, delimiter="\t")
            writer.writerow([prompt, question, f"{question}:{solution}", solution_step])

for classic in ["Einstein", "Zebra"]:
    for type in ["orig_NL", "lexical_replacements", "domain_replacements"]:
        generate_prompt(classic, type)