import re

def translate_puzzle(rows, cols, level, type, num, n):
    translated_puzzles = []
    puzzle_file = f"/home/oenni/Dokumente/LLM_reasoning/Riddles/Puzzles_{type}/Puzzles_Level{level}_{type}/{rows}x{cols}-level{level}_{num}{type}{n}"


    with open(puzzle_file, "r") as fin:
        puzzles = fin.read().split("#################################")

    # dictionary to replace puzzle instructions
    instruction_dict = {
                "Nationality: ": 
                    f"There are {cols} different nationalities: "
                    ,
                "Food: ": 
                    f"There {cols} different types of food: "
                ,
                "Pet: ": 
                    f"{cols} different pets are kept: "
                ,
                "Job: ": 
                    f"The people have {cols} different jobs:  "
                ,
                "Beverage: ": 
                    f"There are {cols} different favourite beverages: "
                ,
                "Transport: ": 
                    f"The people use {cols} different means of transport: "
                ,

                "Music-Genre: ": f"The people prefer {cols} different music-genres: ",
                

                "Movie-Genre: ": f"The people perfer {cols} different movie-genres: ",
                
                "Sport: ": 
                    f"The people prefer {cols} different types of sport: "
                ,
                "Hobby: ": 
                    f"The people have {cols} different hobbies: "
                ,
                # added for zebra and einstein puzzle based on a list from wikipedia
                "Color: ": 
                    f"There are {cols} different favourite colors: "
                ,
                # added for zebra and einstein puzzle based on a list from wikipedia
                "Cigar: ": 
                    f"{cols} different brands of cigars are smoked: "
                ,
                # added to allow more diverse replacements for sizes up to 7 domains
                "Flower: ": 
                    f"The people grow {cols} different varities of flowers: "
                ,
                # added to allow more diverse replacements for sizes up to 7 domains
                "Birthday: ": 
                    f"The people's birthday is in {cols} different months: ",

                "Game: " :
                    f"{cols} different games are played: "

    }

    # dictionary to replace semi-fromal signs from the clues
    sign_dict = {"!=": "is not",
                    "==": "is"}

    for puzzle in puzzles:
    
        replaced_text = puzzle
        for k, v in instruction_dict.items():
            replaced_text = replaced_text.replace(k, v)

        items = set(re.findall("[A-Za-z-]+:[A-Za-z-7&]+", puzzle))
        
        for domain_item in items:
            domain = domain_item.split(":")[0]
            item = domain_item.split(":")[1]

            # adaptible item dictionary to perform the desired replacements for each item and domain
            item_dict = {
                        f"Job:{item}" : f"the {item}",
                        f"Transport:{item}": f"the person driving the {item}",
                        f"Beverage:{item}": f"the person drinking {item}",
                        f"Movie-Genre:{item}": f"the person watching {item} movies",
                        f"Nationality:{item}": f"the {item}",
                        f"Food:{item}": f"the person eating {item}",
                        f"Pet:{item}": f"the owner of the {item}",
                        f"Music-Genre:{item}": f"the fan of {item}",
                        f"Sport:{item}": f"the person who's sport is {item}",
                        f"Hobby:{item}": f"the person who's hobby is {item}",
                        f"Color:{item}": f"the person who likes {item}",
                        f"Cigar:{item}": f"the {item}-smoker",
                        f"Flower:{item}": f"the person who grows{item}",
                        f"Birthday:{item}": f"the person who's birthday is in {item}",
                        f"House:{item}": f"the {item} house",
                        f"City:{item}": f"the person traveling to {item}",
                        f"Game:{item}": f"the person playing {item}"
                        
            }

            replaced_text = replaced_text.replace(domain_item, item_dict[f"{domain}:{item}"])

        
        
        for k, v in sign_dict.items():
            replaced_text = replaced_text.replace(f" {k} ", f" {v} ")

        translated_puzzles.append(replaced_text)

    output_riddle_file = f"/home/oenni/Dokumente/LLM_reasoning/Puzzles_Natural_Language/Puzzles_{type}/Puzzles_Level{level}_{type}_Natural_Language/{rows}x{cols}-level{level}_{num}{type}_Natural_Language{n}"
    with open(output_riddle_file, "w") as fout:
        fout.write("#################################\n".join(translated_puzzles))

def translate_classic_puzzle(classic, type, num, n):
    translated_puzzles = []
    puzzle_file = f"/home/oenni/Dokumente/LLM_reasoning/Riddles/Puzzles_{type}/{classic}_{type}/{classic}_{num}{type}{n}"


    with open(puzzle_file, "r") as fin:
        puzzles = fin.read().split("#################################")

    # dictionary to replace puzzle instructions
    instruction_dict = {
                "Nationality: ": 
                    f"There are 5 different nationalities: "
                    ,
                "Food: ": 
                    f"There 5 different types of food: "
                ,
                "Pet: ": 
                    f"5 different pets are kept: "
                ,
                "Job: ": 
                    f"The people have 5 different jobs:  "
                ,
                "Beverage: ": 
                    f"There are 5 different favourite beverages: "
                ,
                "Transport: ": 
                    f"The people use 5 different means of transport: "
                ,

                "Music-Genre: ": f"The people prefer 5 different music-genres: ",
                

                "Movie-Genre: ": f"The people perfer 5 different movie-genres: ",
                
                "Sport: ": 
                    f"The people prefer 5 different types of sport: "
                ,
                "Hobby: ": 
                    f"The people have 5 different hobbies: "
                ,
                # added for zebra and einstein puzzle based on a list from wikipedia
                "Color: ": 
                    f"There are 5 different favourite colors: "
                ,
                # added for zebra and einstein puzzle based on a list from wikipedia
                "Cigar: ": 
                    f"5 different brands of cigars are smoked: "
                ,
                # added to allow more diverse replacements for sizes up to 7 domains
                "Flower: ": 
                    f"The people grow 5 different varities of flowers: "
                ,
                # added to allow more diverse replacements for sizes up to 7 domains
                "Birthday: ": 
                    f"The people's birthday is in 5 different months: ",

                "Game: " :
                    f"5 different games are played: "

    }

    # dictionary to replace semi-fromal signs from the clues
    sign_dict = {"!=": "is not",
                    "==": "is"}

    for puzzle in puzzles:
    
        replaced_text = puzzle
        for k, v in instruction_dict.items():
            replaced_text = replaced_text.replace(k, v)

        items = set(re.findall("[A-Za-z-]+:[A-Za-z-7&]+", puzzle))
        
        for domain_item in items:
            domain = domain_item.split(":")[0]
            item = domain_item.split(":")[1]

            # adaptible item dictionary to perform the desired replacements for each item and domain
            item_dict = {
                        f"Job:{item}" : f"the {item}",
                        f"Transport:{item}": f"the person driving the {item}",
                        f"Beverage:{item}": f"the person drinking {item}",
                        f"Movie-Genre:{item}": f"the person watching {item} movies",
                        f"Nationality:{item}": f"the {item}",
                        f"Food:{item}": f"the person eating {item}",
                        f"Pet:{item}": f"the owner of the {item}",
                        f"Music-Genre:{item}": f"the fan of {item}",
                        f"Sport:{item}": f"the person who's sport is {item}",
                        f"Hobby:{item}": f"the person who's hobby is {item}",
                        f"Color:{item}": f"the person who likes {item}",
                        f"Cigar:{item}": f"the {item}-smoker",
                        f"Flower:{item}": f"the person who grows{item}",
                        f"Birthday:{item}": f"the person who's birthday is in {item}",
                        f"House:{item}": f"the {item} house",
                        f"City:{item}": f"the person traveling to {item}",
                        f"Game:{item}": f"the person playing {item}"
                        
            }

            replaced_text = replaced_text.replace(domain_item, item_dict[f"{domain}:{item}"])

        
        
        for k, v in sign_dict.items():
            replaced_text = replaced_text.replace(f" {k} ", f" {v} ")

        translated_puzzles.append(replaced_text)

    output_riddle_file = f"/home/oenni/Dokumente/LLM_reasoning/Puzzles_Natural_Language/Puzzles_{type}/Puzzles_{classic}_{type}_Natural_Language/{classic}_{num}{type}_Natural_Language{n}"
    with open(output_riddle_file, "w") as fout:
        fout.write("#################################\n".join(translated_puzzles))

#################################################
##### Translations for classic_puzzles #####
#################################################
##### Original Puzzle ###########################
#################################################
for classic in ["Zebra", "Einstein"]:
    translate_classic_puzzle(classic=classic, type="orig", num="", n="")

#################################################
##### Lexical Puzzle ############################
#################################################
for classic in ["Zebra", "Einstein"]:
    for x in range(20):
        translate_classic_puzzle(classic=classic, type="lexical_replacements", num="", n="-"+str(x))

#################################################
##### Domain Replacement Puzzle #################
#################################################
for classic in ["Zebra", "Einstein"]:
    for num in range(1, 6):
        for x in range(20):
            translate_classic_puzzle(classic=classic, type="domain_replacements", num=num, n="-"+str(x))

#################################################
##### Translations for levels 1, 3, 4, 5, 8 #####
#################################################
##### Original Puzzle ###########################
#################################################
#for lv in [1, 3, 4, 5, 8]:
#    for i in range(1, 8):
#        for j in range(2, 8):
#            translate_puzzle(i, j, level=lv, type="orig", num="", n="")

#################################################
##### Lexical Puzzle ############################
#################################################
#for lv in [1, 3, 4, 5, 8]:
#    for i in range(1, 8):
#        for j in range(2, 8):
#            for x in range(20):
#                print(f"call with level={lv}, rows={i}, cols={j}, x={x}")
#                translate_puzzle(i, j, level=lv, type="lexical_replacements", num="", n="-"+str(x))

#################################################
##### Domain Replacement Puzzle #################
#################################################
#for lv in [1, 3, 4, 5, 8]:
#    for i in range(1, 8):
#        for j in range(2, 8):
#            for num in range(1, i+1):
#                for x in range(20):
#                    print(f"call with level={lv}, rows={i}, cols={j}, num={num}, x={x}")
#                    translate_puzzle(i, j, level=lv, type="domain_replacements", num=num, n="-"+str(x))



########################################
##### Translations for levels 2, 7 #####
########################################
##### Original Puzzle ##################
########################################
#for lv in [2, 7]:
#    for i in range (1, 8):
#        for j in range(3, 8):
#            print("call with level=",lv, "rows=", i, "cols=",j)
#            translate_puzzle(rows=i, cols=j, level=lv, type="orig", num="", n="")

########################################
##### Lexical Puzzle ###################
########################################
#for lv in [2, 7]:
#    for i in range(1, 8):
#        for j in range(3, 8):
#            for x in range(20):
#                print(f"call with level={lv}, rows={i}, cols={j}, x={x}")
#                translate_puzzle(i, j, level=lv, type="lexical_replacements", num="", n="-"+str(x))

########################################
##### Domain Replacement Puzzle ########
########################################
#for lv in [2, 7]:
#    for i in range(1, 8):
#        for j in range(3, 8):
#            for num in range(1, i):
#                for x in range(20):
#                    print(f"call with level={lv}, rows={i}, cols={j}, num={num}, x={x}")
#                    translate_puzzle(i, j, level=lv, type="domain_replacements", num=num, n="-"+str(x))



##############################################
##### Translations for levels 10, 11, 12 #####
##############################################
##### Original Puzzle ##################
########################################
#for lv in [10, 11, 12]:
#    for i in range(3, 8):
#        for j in range(3, 8):
#            print("call with level=",lv, "rows=", i, "cols=",j)
#            translate_puzzle(rows=i, cols=j, level=lv, type="orig", num="", n="")

########################################
##### Lexical Puzzle ###################
########################################
#for lv in [10, 11, 12]:
#    for i in range(3, 8):
#        for j in range(3, 8):
#            for x in range(20):
#                print(f"call with level={lv}, rows={i}, cols={j}, x={x}")
#                translate_puzzle(i, j, level=lv, type="lexical_replacements", num="", n="-"+str(x))

########################################
##### Domain Replacement Puzzle ########
########################################
#for lv in [2, 7]:
#    for i in range(1, 8):
#        for j in range(3, 8):
#            for num in range(1, i+1):
#                for x in range(20):
#                    print(f"call with level={lv}, rows={i}, cols={j}, num={num}, x={x}")
#                    translate_puzzle(i, j, level=lv, type="domain_replacements", num=num, n="-"+str(x))

############################################
##### Directions Replacement Puzzle ########
############################################
#for lv in [2, 7]:
#    for i in range(1, 8):
#        for j in range(3, 8):
#            for num in range(1, i+1):
#                for x in range(20):
#                    print(f"call with level={lv}, rows={i}, cols={j}, num={num}, x={x}")
#                    translate_puzzle(i, j, level=lv, type="Compass_Points_directions_replacements", num="", n="")


########################################
##### Translations for levels 6, 9 #####
########################################
##### Original Puzzle ##################
########################################
#for lv in [6, 9]:
#    for i in range(2, 8):
#        for j in range(2, 8):
#            print("call with level=",lv, "rows=", i, "cols=",j)
#            translate_puzzle(rows=i, cols=j, level=lv, type="orig", n="", num="")

########################################
##### Lexical Puzzle ###################
########################################
#for lv in [6, 9]:
#    for i in range(2, 8):
#        for j in range(2, 8):
#            for x in range(20):
#                print(f"call with level={lv}, rows={i}, cols={j}, x={x}")
#                translate_puzzle(i, j, level=lv, type="lexical_replacements", num="", n="-"+str(x))

########################################
##### Domain Replacement Puzzle ########
########################################
#for lv in [6, 9]:
#    for i in range(2, 8):
#        for j in range(2, 8):
#            for num in range(1, i+1):
#                for x in range(20):
#                    print(f"call with level={lv}, rows={i}, cols={j}, num={num}, x={x}")
#                    translate_puzzle(i, j, level=lv, type="domain_replacements", num=num, n="-"+str(x))
