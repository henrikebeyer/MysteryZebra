"""This piece of code transforms the .txt files produced by the puzzle generator and manipulated by the puzzle manipulator into a .csv for easy processing"""

import pandas as pd
import os

def reformat_classic_grid(classic, typ):
    # prepare out directory for the corpus files
    try:
        out_directory = f"../corpus/part1/{classic}"
        os.makedirs(out_directory)
    except:
        pass
    
    puzzles = []
    clue_list = []
    grids = []
    idx = []

    # read in all the puzzles
    if typ == "orig" or typ == "orig_NL":
        puzzle_file = f"../Puzzles_Natural_Language/Puzzles_orig/Puzzles_{classic}_{typ}/{classic}_{typ}"
        idx.append(f"Pt1_{classic}_{typ}")
        with open(puzzle_file, "r") as fin:
            puzzle = fin.read().strip("\n")
            puzzles.append(puzzle)
    else:
        for x in range(3):
            if typ == "domain_replacements":
                for n in range(1,6):
                    puzzle_file = f"../Puzzles_Natural_Language/Puzzles_{typ}/Puzzles_{classic}_{typ}/{classic}_{n}{typ}_Natural_Language-{x}"
                    idx.append(f"Pt1_{classic}_{n}{typ}-{x}")
                    with open(puzzle_file, "r") as fin:
                        puzzle = fin.read().strip("\n")
                    puzzles.append(puzzle)
            else:
                puzzle_file = f"../Puzzles_Natural_Language/Puzzles_{typ}/Puzzles_{classic}_{typ}/{classic}_{typ}_Natural_Language-{x}"
                idx.append(f"Pt1_{classic}_{typ}-{x}")
                with open(puzzle_file, "r") as fin:
                    puzzle = fin.read().strip("\n")
                puzzles.append(puzzle)
    
    # separate clues from solution grids
    for id, puzzle in zip(idx, puzzles):
        grid = {}
        print(id)
        grid_list = [line.lower().strip().replace("\t","").split("|")[1:5+2] for line in puzzle.split(".:: Answer ::.")[-1].split("\n")[1:5+2]]
        for line in grid_list[1:]:
            line = [item.strip() for item in line]
            grid[line[0]] = line[1:]
        
        clues = puzzle.replace(".:: Answer ::.","").replace("\n\n","\n").split("\n")
        if id.split("_")[-1] != "orig" and id.split("_")[1] == "Zebra":
            clues = ("\n".join(clues[2:21]).strip())
        else:
            clues = ("\n".join(clues[2:22]).strip())

        grids.append(grid)
        clue_list.append(clues)
        print(clues, "\n\n")

    data = {"ID":idx, "Clues":clue_list, "SolutionGrid":grids}
    out_df = pd.DataFrame(data = data)
    
    if typ == "domain_replacements":
        for n in range(1, 6):
            out_df.to_csv(f"{out_directory}/{classic}_{n}{typ}.csv", index=False)
    else:
        out_df.to_csv(f"{out_directory}/{classic}_{typ}.csv", index=False)

typs = ["orig", "orig_NL", "lexical_replacements", "domain_replacements"]
for classic in ["Einstein", "Zebra"]:
    for typ in typs:
        reformat_classic_grid(classic, typ)

def reformat_pt2(level, row, col):
    try:
        out_directory = f"../corpus/part2/level{level}"
        os.makedirs(out_directory)
    except:
        pass

    grids = []
    clue_list = []
    idx = []

    puzzle_file = f"../Puzzles_Natural_Language/Puzzles_orig/Puzzles_Level{level}_orig_Natural_Language/{row}x{col}-level{level}_orig_Natural_Language"

    with open(puzzle_file, "r") as fin:
        puzzles = fin.read().strip("\n").replace(f"##{level}","").split("#################################\n")[:-1]

    for i, pzl in zip(range(10), puzzles[:10]):
        grid = {}
        id = f"Pt1_{row}x{col}_level{level}-{i}"
        clues = pzl.split(".:: Answer ::.")[0].split("::.")[1].strip()
        grid_lines = [line.split("|") for line in pzl.split(".:: Answer ::.")[1].split("|\n")[1:row+1]]
        for line in grid_lines:
            line = [item.strip() for item in line]
            grid[line[1]] = line[2:]

        idx.append(id)
        clue_list.append(clues)
        grids.append(grid)

    data = {"ID":idx, "Clues":clue_list, "SolutionGrid":grids}
    out_df = pd.DataFrame(data=data)

    out_df.to_csv(f"{out_directory}/Pt2_{row}x{col}_level{level}.csv", index=False)
        

#################################################
##### levels 1, 3, 4, 5, 8 #####
#################################################
# for lv in [1, 3, 4, 5, 8]:#[1, 3, 4, 5, 8]:
#     for i in range(1,8):
#         for j in range(2,8):
#             print("level=", lv, i, "x", j)
#             reformat_pt2(level=lv, row=i, col=j)

########################################
#####levels 2, 7 #####
########################################
# for lv in [2, 7]:
#     for i in range (1, 8):
#         for j in range(3, 8):
#             print("level=", lv, i, "x", j)
#             reformat_pt2(level=lv, row=i, col=j)

##############################################
##### levels 10, 11, 12 #####
##############################################
# for lv in [10, 11, 12]: #[10, 11, 12]:
#     for i in range(3, 8):
#         for j in range(3, 8):
#             print("level=", lv, i, "x", j)
#             reformat_pt2(level=lv, row=i, col=j)
########################################
##### levels 6, 9 #####
########################################
# for lv in [6, 9]: #[6, 9]:
#     for i in range(2, 8):
#         for j in range(2, 8):
#             print("level=", lv, i, "x", j)
#             reformat_pt2(level=lv, row=i, col=j)