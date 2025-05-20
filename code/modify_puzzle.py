import re
import random
import string

# dictionary of domains and items in a domain
kinds_dict = {
            "Nationality": {
                "american", "argentine", "australian", "brazilian", "british",
                "canadian", "chinese", "colombian", "dutch", "egyptian",
                "french", "german", "indian", "indonesian", "italian",
                "japanese", "malaysian", "mexican", "nigerian", "pakistani",
                "polish", "russian", "spanish", "thai", "turkish",
            },
            "Food": {
                "apple", "apricot", "artichoke", "asparagus", "avocado",
                "banana", "blueberry", "broccoli", "cabbage", "carrot",
                "cauliflower", "cherry", "corn", "cranberry", "cucumber",
                "eggplant", "garlic", "grapefruit", "grapes", "kale",
                "kiwi", "lemon", "lettuce", "lime", "mango",
                "nectarine", "onion", "orange", "papaya", "peach",
                "pear", "peas", "pepper", "pineapple", "plum",
                "pomegranate", "potato", "pumpkin", "radish", "raspberry",
                "spinach", "strawberry", "tomato", "watermelon", "zucchini",
            },
            "Pet": {
                "bird", "cat", "chinchilla", "dog", "ferret",
                "fish", "frog", "goat", "goldfish", "guinea-pig",
                "hamster", "hedgehog", "horse", "lizard", "mouse",
                "pony", "rabbit", "rat", "snake", "turtle",
            },
            "Job": {
                "accountant", "analyst", "architect", "bartender", "chef",
                "coach", "dancer", "designer", "doctor", "dressmaker",
                "electrician", "engineer", "entrepreneur", "firefighter", "fisherman",
                "freelancer", "journalist", "lawyer", "librarian", "manager",
                "mechanic", "musician", "nurse", "paramedic", "photographer",
                "pilot", "police-officer", "project-manager", "scientist", "security-guard",
                "social-worker", "software-developer", "teacher", "videographer", "writer",
            },
            "Beverage": {
                "7up", "almond-milk", "coffee", "cola", "fanta",
                "hot-chocolate", "iced-tea", "juice", "lemonade", "milk",
                "mirinda", "soy-milk", "sprite", "tea", "water",
            },
            "Transport": {
                "airplane", "bike", "boat", "bus", "car",
                "helicopter", "jet-ski", "motorbike", "quad-bike", "roller",
                "scooter", "ship", "skateboard", "snowmobile",
                "subway", "taxi", "train", "tram", "trike", "van",
            },
            "Music-Genre": {
                "ambient", "blues", "classical", "country", "d&b",
                "disco", "dubstep", "electronic", "folk", "funk",
                "gospel", "hip-hop", "house", "indie", "jazz",
                "metal", "pop", "punk", "r&b", "reggae",
                "rock", "salsa", "soul", "techno", "trance",
            },
            "Movie-Genre": {
                "action", "adventure", "animation", "comedy", "crime",
                "disaster", "documentary", "drama", "epic", "family",
                "fantasy", "horror", "martial-arts", "musical", "mystery",
                "romance", "satire", "scientific", "sports", "spy",
                "superhero", "thriller", "time-travel", "western", "zombie",
            },
            "Sport": {
                "badminton", "baseball", "basketball", "biathlon", "climbing",
                "cricket", "cycling", "golf", "handball", "ice-hockey",
                "lacrosse", "parkour", "rowing", "rugby", "sailing",
                "skateboarding", "skiing", "snowboarding", "soccer", "surfing",
                "swimming", "tennis", "volleyball", "water-polo", "weightlifting",
            },
            "Hobby": {
                "baking", "board-games", "camping", "card-games", "chess",
                "collecting", "cooking", "dancing", "drawing", "filmmaking",
                "fishing", "gardening", "hiking", "magic-tricks", "photography",
                "puzzles", "reading", "rock-climbing", "singing", "skydiving",
                "sudoku", "traveling", "video-games", "woodworking", "writing",
            },
            # added for zebra and einstein puzzle based on a list from wikipedia
            "Color": {
                "blue", "green", "red", "white", "yellow", "ivory", "turquise",
                "orange", "grey", "black", "pink", "purple", "brown", "light-blue",
                "azure", "amber", "aquamarine", "apricot", "blood-red", "lilac",
                "coral", "fuchsia", "mauve", "chestnut", "ebony", "emerald",
                "lavender"
            },
            # added for zebra and einstein puzzle based on a list from wikipedia
            "Cigar": {
                "bluemaster", "dunhill", "pall-mall", "prince", "blend",
                "alhambra", "aristoff", "baccarat", "bongani", "bolivar",
                "cain", "chaman", "davidoff", "dannemann", "fonseca", 
                "game", "havana", "montecristo", "old-henry", "oliveros",
                "ritmeester", "siglo", "swisher", "tiparillo", "vegafina"
            },
            # added to allow more diverse replacements for sizes up to 7 domains
            "Flower": {
                "rose", "amaryllis", "begonia", "lily", "iris", "sunflower",
                "dahlia", "azalea", "poppy", "daisy", "tulip", "orchid",
                "orchid", "daffodil", "bellflower", "aconite", "zinnia",
                "balloon-flower", "marigold"
            },
            # added to allow more diverse replacements for sizes up to 7 domains
            "Birthday": {
                "january", "february", "march", "april", "may", "june",
                "july", "august", "september", "october", "november",
                "december"
            },
            # added to allow more diverse replacements
            "House" : {
                "victorian", "colonial", "tower", "modern", "craftsman", 
                "wooden", "palace", "townhouse", "futuristic", "cottage",
                "farmhouse", "ranch-style", "gothic-revival", "art-deco",
                "cape-cod"
            },
            # added to allow more diverse replacements
            "Game": {
                "mah-jongg", "monopoly", "chess", "go", "scrabble",
                "billiard", "bridge", "poker", "domino", "backgammon",
                "snooker", "canasta", "whist"
            },
            # added to allow more diverse replacements
            "City": {
                "new-york", "berlin", "paris", "london", "prague", 
                "san-francisco", "hamburg", "colone", "hannover",
                "edinburgh", "liverpool", "rome", "venice", "marseilles",
                "nizza", "boston", "miami"
            }
}

##################################################################################
####### These are the replacement functions for the self-created puzzles #########
##################################################################################

# this function does the lexical replacement of kinds within a domain for the self-created puzzles
# it takes the number of rows and columns, the level of the target puzzle for the obfuscation and the number of alternative versions to be created
def replace_lexical(rows, cols, level, n):
    puzzle_file = f"/home/oenni/Dokumente/LLM_reasoning/Riddles/Puzzles_orig/Puzzles_Level{level}_orig/{rows}x{cols}-level{level}_orig" # define the file where the original puzzle is with rows, cols and level

    # iterate for n times to match the target amount of obfuscated versions to be created
    for i in range(n):
        manipulated_puzzles = [] # place-holder list for all riddles with replacements to be created
        with open(puzzle_file, "r") as fin:
            puzzles = fin.read().split("#################################") # split the file into the single puzzles with help of the separation marker

        # iterate over all puzzles 
        for puzzle in puzzles[:-1]: #the last one in the split list is empty because of formatting of the puzzle files
            items = set(re.findall("[A-Za-z-]+: [A-Za-z-7& ,]+", puzzle)) # identify all domains and kinds for the given puzzle
            #print(items)

            replacements = {} # place-holder dict for the replacements to take place
            banned = [] # list to store used kinds (from the original puzzle and selected ones) to avoid duplicates
            for item in items:
                domain = item.split(": ")[0] # separate the domains from the kinds
                kinds = item.split(": ")[1].split(", ") # extract the kinds as a list
                banned += kinds # add all kinds to the banned list to avoid duplicates during replacement
                for kind in kinds: # iterate to replace every kind of a domain
                    replacement = kind
                    while replacement==kind or replacement in banned: # make sure that only an un-used kind is selected as a replacement
                        replacement = random.choice(list(kinds_dict[domain])) # the replacement is randomly selected from the same domain

                    replacements[kind] = replacement # write the replacement to a dict with the original kind as key
                    banned.append(replacement) # add the chosen kind to the list of banned kinds

            #print(replacements)
            # perform the replacement
            replaced_text = puzzle
            for k, v in replacements.items():
                replaced_text = replaced_text.replace(f":{k}",f":{v}")
                replaced_text = replaced_text.replace(f" {k}", f" {v}")
                replaced_text = replaced_text.replace(f" {k} ", f" {v} ")
            
            # append the replaced puzzle to the list of manipulated puzzles for the file
            manipulated_puzzles.append(replaced_text)

            #print(replaced_text)
        # write out all obfuscated puzzles with the same separation marker
        output_riddle_file = f"/home/oenni/Dokumente/LLM_reasoning/Riddles/Puzzles_lexical_replacements/Puzzles_Level{level}_lexical_replacements/{rows}x{cols}-level{level}_lexical_replacements-{i}"
        with open(output_riddle_file, "w") as fout:
            fout.write("#################################\n".join(manipulated_puzzles))

# Here we call the above function to perform the replacements for all created puzzles

#replace_lexical(rows=1, cols=5, level=2, n=1)

#################################################
##### Obfuscations for levels 1, 3, 4, 5, 8 #####
#################################################
#for lv in [1, 3, 4, 5, 8]:
#    for i in range(1, 8):
#        for j in range(2, 8):
#            replace_lexical(rows=i, cols=j, level=lv, n=20)

########################################
##### Obfuscations for levels 2, 7 #####
########################################
#for lv in [2, 7]:
#    for i in range (1, 8):
#        for j in range(3, 8):
#            replace_lexical(rows=i, cols=j, level=lv, n=20)

##############################################
##### Obfuscations for levels 10, 11, 12 #####
##############################################
#for lv in [10, 11, 12]:
#    for i in range(3, 8):
#        for j in range(3, 8):
#            replace_lexical(rows=i, cols=j, level=lv, n=20)

########################################
##### Obfuscations for levels 6, 9 #####
########################################
#for lv in [6, 9]:
#    for i in range(2, 8):
#        for j in range(2, 8):
#            replace_lexical(rows=i, cols=j, level=lv, n=20)

# this function does the domain replacements for a defined amount of domains
# it takes the number of rows, columns and the level of the target puzzle for the obfuscation, the number of domains to be replaced abd the number of alternative versions to be created
def replace_domains(rows, cols, level, num, n):
    # check if the defined amount of replacements is possible for the chosen puzzle size
    if rows < num:
        return("There are only", rows, "domains in the riddle. You cannot replace", num, "domains.")

    riddle_file = f"/home/oenni/Dokumente/LLM_reasoning/Riddles/Puzzles_orig/Puzzles_Level{level}_orig/{rows}x{cols}-level{level}_orig" # define the file where the original puzzle is with rows, cols and level
    with open(riddle_file, "r") as fin:
            puzzles = fin.read().split("#################################") # split the file into single puzzles with help of the separation marker

    # iterate for n times to match the target amound of obfuscated versions to be created
    for i in range(n):
        manipulated_puzzles = [] # place-holder list for all riddles with replacements to be created
        # iterate over all puzzles
        for puzzle in puzzles[:-1]: # the last in the lsit is empty because of formatting of the puzzle files
            items = set(re.findall("[A-Za-z-]+: [A-Za-z-7& ,]+", puzzle)) # identify all domains and kinds for the given puzzle

            domain_dict = {} # place-holder dict to store the domain replacements
            replacement_kinds = {} # place-holder dict to store the kind replacements
                
            banned = [item.split(": ")[0] for item in items] # add all domains to the list of banned items

            #print(puzzle, items, len(list(items)), num)
            target_items = random.sample(list(items), num) # randomly select the desired amount of domains (defined by num) to be replaced

            # iterate over all items selected for the replacement
            for item in target_items:

                # select a replacement domain
                domain = item.split(": ")[0] # extract the domain from the item string
                new_domain = domain 
                while new_domain == domain or new_domain in banned: # make sure that only an allowed domain is chosen
                    new_domain = random.choice(list(kinds_dict.keys()))
                    
                domain_dict[domain] = new_domain # add the new domain to the domain dict with the original domain as key
                banned.append(new_domain) # add the new domain to the banned items

                # select replacement kinds 
                kinds = item.split(": ")[1].split(", ") # extract the kinds from the target-item
                banned += kinds # add the old kinds to the list of banned items
                #print(kinds)

                # replace every kind of the target-items
                for kind in kinds:
                    new_kind = kind
                    while new_kind == kind or new_kind in banned: # make sure that the new kind is not banned
                        new_kind = random.choice(list(kinds_dict[new_domain])) # select the new kind from the new domain!!!!
                    replacement_kinds[kind] = new_kind # add the new kind to the replacement dictionary for kinds with the old kind as the key
                    banned.append(new_kind) # add the new kind to the list of banned items

            replaced_text = puzzle

            # perform the replacement for domains
            for k,v in domain_dict.items():
                replaced_text = replaced_text.replace(f"{k}:",f"{v}:")

            # perform the replacement for the kinds of the domains
            for k,v in replacement_kinds.items():
                replaced_text = replaced_text.replace(f":{k}",f":{v}")
                replaced_text = replaced_text.replace(f" {k}", f" {v}")
                replaced_text = replaced_text.replace(f" {k} ", f" {v} ")

            manipulated_puzzles.append(replaced_text) # add the obfuscated puzzle to the list of manipulated puzzles

        #print(len(manipulated_puzzles))
        # write out all obfuscated puzzles with the same separation marker
        output_riddle_file = f"/home/oenni/Dokumente/LLM_reasoning/Riddles/Puzzles_domain_replacements/Puzzles_Level{level}_domain_replacements/{rows}x{cols}-level{level}_{num}domain_replacements-{i}"
        with open(output_riddle_file, "w") as fout:
            fout.write("#################################\n".join(manipulated_puzzles))

# Here we call the above function to perform the obfuscations for all created puzzles
#################################################
##### Obfuscations for levels 1, 3, 4, 5, 8 #####
#################################################
#for lv in [1, 3, 4, 5, 8]:
#    for i in range(1, 8):
#        for j in range(2, 8):
#            for x in range(1,i+1):
#                print("call with level=",lv, "rows=", i, "cols=",j, "num=", x)
#                replace_domains(rows=i, cols=j, level=lv, num=x, n=20)

#replace_domains(rows=1, cols=5, level=7, num=1)

########################################
##### Obfuscations for levels 2, 7 #####
########################################
#for lv in [2, 7]:
#    for i in range (1, 8):
#        for j in range(3, 8):
#            for x in range(1,i+1):
#                print("call with level=",lv, "rows=", i, "cols=",j, "num=", x)
#                replace_domains(rows=i, cols=j, level=lv, num=x, n=20)

##############################################
##### Obfuscations for levels 10, 11, 12 #####
##############################################
#for lv in [12]:
#    for i in range(3, 8):
#        for j in range(3, 8):
#            for x in range(1, i+1):
#                print("call with level=",lv, "rows=", i, "cols=",j, "num=", x)
#                replace_domains(rows=i, cols=j, level=lv, num=x, n=20)

########################################
##### Obfuscations for levels 6, 9 #####
########################################
#for lv in [6, 9]:
#    for i in range(2, 8):
#        for j in range(2, 8):
#           for x in range(1, i+1):
#               print("call with level=",lv, "rows=", i, "cols=",j, "num=", x)
#               replace_domains(rows=i, cols=j, level=lv, n=20, num=x)

# this function does the replacements for direction clues
# it takes the number of rows, columns and the level of the target puzzle for the obfuscation
# in addition a direction key [Compass_points, Numeric] is taken, which clarifys how the direciton clues will be replaced
# there is only one obfuscated version possible for each direction key
def manipulate_directions(rows, cols, level, direction_key):
    riddle_file = f"/home/oenni/Dokumente/LLM_reasoning/Riddles/Puzzles_orig/Puzzles_Level{level}_orig/{rows}x{cols}-level{level}_orig" # define the file where the original puzzle is with rows, cols and level

    manipulated_puzzles = [] # place-holder list to store all obfuscated puzzles

    # direction_dict to store the information on how to translate from left/right direction keys
    direction_dict = {
        "Compass_Points":{
            " on ": " to ",
            "right":"east", 
            "left":"west",
            "to the far west" : "at the western end",
            "to the far east" : "at the eastern end"
            }, 
        "Numeric":{
            "to the right of":"in a numerically higher position to",
            "to the left of":"in a numerically lower position to",
            "on the far right":"in the numericaly highest position",
            "on the far left":"in the numerically lowest position",
            }}

    # read in the target puzzles
    with open(riddle_file, "r") as fin:
        puzzles = fin.read().split("#################################") # split the file into single puzzles with help of the separation marker

    # iterate over all puzzles
    for puzzle in puzzles[:-1]: # the last item in the list is empty due to the formatting of the puzzle files
        replaced_text = puzzle

        # perform the replacement for the specified direction key
        for k,v in direction_dict[direction_key].items():
            replaced_text = replaced_text.replace(k,v)

        # append the obfuscated version to the list of manipulated puzzle
        manipulated_puzzles.append(replaced_text)

    # write out the obfuscated puzzles with the same separation marker
    output_riddle_file = f"/home/oenni/Dokumente/LLM_reasoning/Riddles/Puzzles_directions_replacements/{direction_key}_directions_replacements/Puzzles_Level{level}_directions_replacements/{rows}x{cols}-level{level}_{direction_key}"
    with open(output_riddle_file, "w") as fout:
        fout.write("#################################\n".join(manipulated_puzzles))

#################################################
##### Obfuscations for levels 1, 3, 4, 5, 8 #####
#################################################
#for lv in [1, 3, 4, 5, 8]:
#    for i in range(1, 8):
#        for j in range(2, 8):
#            print("call with level=",lv, "rows=", i, "cols=",j)
#            manipulate_directions(rows=i, cols=j, level=lv, direction_key="Compass_Points")
#            manipulate_directions(rows=i, cols=j, level=lv, direction_key="Numeric")

########################################
##### Obfuscations for levels 2, 7 #####
########################################
#for lv in [2, 7]:
#    for i in range (1, 8):
#        for j in range(3, 8):
#            print("call with level=",lv, "rows=", i, "cols=",j)
#            manipulate_directions(rows=i, cols=j, level=lv, direction_key="Compass_Points")
#            manipulate_directions(rows=i, cols=j, level=lv, direction_key="Numeric")


##############################################
##### Obfuscations for levels 10, 11, 12 #####
##############################################
#for lv in [10, 11, 12]:
#    for i in range(3, 8):
#        for j in range(3, 8):
#            print("call with level=",lv, "rows=", i, "cols=",j)
#            manipulate_directions(rows=i, cols=j, level=lv, direction_key="Compass_Points")
#            manipulate_directions(rows=i, cols=j, level=lv, direction_key="Numeric")


########################################
##### Obfuscations for levels 6, 9 #####
########################################
#for lv in [6, 9]:
#    for i in range(2, 8):
#        for j in range(2, 8):
#           print("call with level=",lv, "rows=", i, "cols=",j)
#           manipulate_directions(rows=i, cols=j, level=lv, direction_key="Compass_Points")
#           manipulate_directions(rows=i, cols=j, level=lv, direction_key="Numeric")


################################################################################################
####### These are the replacement functions for the classic Zebra and Einstein puzzles #########
################################################################################################
# for these puzzles, there are no sizes or levels and only one puzzle per file

# this function does the lexical replacement for kinds within a domain for the classic Einstein and Zebra puzzles
# the input is the name of the classic puzzle and the number of obfuscated versions to be created
def classic_replace_lexical(classic, n):
    riddle_file = f"/home/oenni/Dokumente/LLM_reasoning/Riddles/Puzzles_orig/{classic}_orig/{classic}_orig" # it is important that the files are formatted according to the same rules as the self-created ones

    # iterate for n times to create the desired number of obfuscated versions
    for i in range(n):
        with open(riddle_file, "r") as fin:
            puzzle = fin.read() # there is just one puzzle per file, so no need to split puzzles

        items = set(re.findall("[A-Za-z-]+: [A-Za-z-7 ,]+", puzzle)) # extract the items

        replacements = {} # place-holder dictionary for the replacements to take place

        for item in items: # iterate over all items
            banned = [] # list to trace all banned items
            domain = item.split(": ")[0] # extract the domain from the item string
            kinds = item.split(": ")[1].split(", ") # extract the kinds from the item string
            banned += kinds # add all kinds to the list of banned items
            for kind in kinds: # iterate over all identified kinds of a domain
                replacement = kind
                while replacement==kind or replacement in banned: # make sure that no banned kind is selected
                    replacement = random.choice(list(kinds_dict[domain])) # randomly select a new kind from the same domain

                replacements[kind] = replacement # write the selected kind to the replacement dict with the original kind as the key
                banned.append(replacement) # add the selected kind to the list of banned items to avoid duplicates

        replaced_text = puzzle

        # perform the replacement
        for k, v in replacements.items():
            replaced_text = replaced_text.replace(k, v)

        # write out the obfuscated puzzle
        output_riddle_file = f"/home/oenni/Dokumente/LLM_reasoning/Riddles/Puzzles_lexical_replacements/{classic}_lexical_replacements/{classic}_lexical_replacements-{i}"
        with open(output_riddle_file, "w") as fout:
            fout.write(replaced_text)

# call the function above for the Zebra and Einstein puzzle
################################
##### Lexical obfuscations #####
################################
#for type in ["Einstein", "Zebra"]:
#    classic_replace_lexical(type, n=20)

# this fuction performs the replacement of a specified amount of domains from the Einstein and Zebra puzzles
# the input is the name of the classic puzzle and the number of domains to replace and the number of obfuscated versions to procude
def classic_replace_domains(classic, num, n):
    riddle_file = f"/home/oenni/Dokumente/LLM_reasoning/Riddles/Puzzles_orig/{classic}_orig/{classic}_orig" # it is importatnt the the files are formatted according to the same rules as the self-created ones

    # iterate for n times to create the desired number of obfuscated versions
    for i in range(n):
        with open(riddle_file, "r") as fin:
            puzzle = fin.read() # there is just one puzzle per file, so no need to split puzzles

        
        items = set(re.findall("[A-Za-z-]+: [A-Za-z-7 ,]+", puzzle)) # extract the items from the puzzle

        domain_dict = {} # place-holder dict for the domain replacements
        replacement_kinds = {} # place-holder dict for the kind replacements

        banned = [item.split(": ")[0] for item in items] # add all domains to the banned items
        if len(items) < num: # make sure that there are enough items to perform the desired transformation
            return("There are only", len(items), "domains in the riddle. You cannot replace", num, "domains.")

        # randomly select the specified number of items to replace
        target_items = random.sample(list(items), num)

        # iterate over all items chosen for replacement
        for item in target_items:

            # select a new domain
            domain = item.split(": ")[0] # extract the domain from the item string
            new_domain = domain
            
            while new_domain == domain or new_domain in banned: # make sure that no banned domain is chosen
                new_domain = random.choice(list(kinds_dict.keys()))
                
            domain_dict[domain] = new_domain # add the new domain to the domain dictionary with the old domain as the key
            banned.append(new_domain) # add the new domain to the banned items

            # select new kinds
            kinds = item.split(": ")[1].split(", ") # extract the kinds from the item string
            banned.append(kinds) # add all kinds to the banned items to avoid duplicates
            
            for kind in kinds: # iterate over all kinds
                new_kind = kind
                while new_kind == kind or new_kind in banned: # make sure that no banned item is chosen
                    new_kind = random.choice(list(kinds_dict[new_domain])) # select a new kind from the new domain
                replacement_kinds[kind] = new_kind # write the new kind to the dict of kind replacements with the original kind as key
                banned.append(new_kind) # add the new kind to the list of banned items

        replaced_text = puzzle

        # perform the replacement of the domains
        for k,v in domain_dict.items():
            replaced_text = replaced_text.replace(k,v)

        # perform the replacement of the kinds
        for k,v in replacement_kinds.items():
            replaced_text = replaced_text.replace(k,v)

    # write out the obfuscated puzzles
        output_riddle_file = f"/home/oenni/Dokumente/LLM_reasoning/Riddles/Puzzles_domain_replacements/{classic}_domain_replacements/{classic}_{num}domain_replacements-{i}"
        with open(output_riddle_file, "w") as fout:
            fout.write(replaced_text)

# call the function for the Zebra and Einstein puzzle
# Here we call the above function to perform the obfuscations for all created puzzles
################################################
##### Domain obfuscations Zebra & Einstein #####
################################################
#for type in ["Einstein", "Zebra"]:
#    for num in range(1, 6):
#        classic_replace_domains(type, num=num, n=20)

# this function lexically replaces direction clues for Einstein and Zebra
# the input is the name of the classic puzzle and the direction key for the way how the left/right direction clues will be replaced
# there is only one obfuscated version possible for each direction key
def classic_manipulate_directions(classic, direction_key):
    riddle_file = f"/home/oenni/Dokumente/LLM_reasoning/Riddles/{classic}_orig/{classic}_orig_rules_formatted" # it is importatnt the the files are formatted according to the same rules as the self-created ones

    # direction_dict to store the information on how to translate from left/right direction keys
    direction_dict = {
        "Compass_Points":{
            " on ": " to ",
            "right":"east", 
            "left":"west",
            "to the far west" : "at the western end",
            "to the far east" : "at the eastern end"
            }, 
        "Numeric":{
            "to the right of":"in a numerically higher position to",
            "to the left of":"in a numerically lower position to",
            "on the far right":"in the numericaly highest position",
            "on the far left":"in the numerically lowest position",
            "on the left or right of":"in a numerically lower or higher position to"
            }}

    with open(riddle_file, "r") as fin:
        puzzle = fin.read() # no need to split because only one puzzle per file

    # perform the replacement
    replaced_text = puzzle

    for k,v in direction_dict[direction_key].items():
        replaced_text = replaced_text.replace(k,v)

    # write out the obfuscated file
    #print(replaced_text)
    output_riddle_file = f"/home/oenni/Dokumente/LLM_reasoning/Riddles/Puzzles_directions_replacements/{direction_key}_directions_replacements/{classic}_directions_replacements/{classic}_directions_replacements_{direction_key}"
    
    with open(output_riddle_file, "w") as fout:
        fout.write(replaced_text)

##################################################
##### Direction Obfuscation Einstein & Zebra #####
##################################################
#for type in ["Einstein", "Zebra"]:
#    for direction_key in ["Compass_Points", "Numeric"]:
#        classic_manipulate_directions(type, direction_key=direction_key)