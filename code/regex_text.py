import re

# Sample text
sample_text = """
#############
|        |     1     |    2    |
| Food   | Asparagus | Spinach |
#############
"""

# Complete RegEx to match the whole table structure
pattern = r'(\|([\w\W]*?\|){1,8}\n){1,10}+'#(?:\s*\n\|[\s\S]*?\|){1,5})'
#pattern = r'#############\n(\|[\s\S]*?\|(?:\s*\n\|[\s\S]*?\|){1,7})\n#############'
#pattern = r'#############\n\|.*\|.*\d+.*\|.*\d+.*\|\n\|.*[A-Za-z]+.*\|.*[A-Za-z]+.*\|.*[A-Za-z]+.*\|\n#############'

# Find the exact match of the table
match = re.search(pattern, sample_text)

if match:
    matched_string = match.group(0)  # Get the entire matched string
    print("Matched Table Structure:")
    print(matched_string)
else:
    print("No match found.")


import re

# Sample text with a table that has up to 7 rows and columns
sample_text = """Let's solve the puzzle!

From the given information, we know:

1. The person eating asparagus is on the left of the person eating spinach.

This means we can create a diagram to represent the seating arrangement:

|A |? | S

Where A represents the person eating asparagus, and S represents the person eating spinach.

Since there are only two types of food, we can fill in the remaining information:

|A | B | S

Now, we can label the columns:

|        |     1     |    2    |
| Food   | Asparagus | Spinach |

#############
|        |     1     |    2    |
| Food   | Asparagus | Spinach |

The final solution table is:

#############
|        |     1     |    2    |
| Food   | Asparagus | Spinach |

Let me know if you have any further questions or if there's anything else I can help you with!"""


"""
|                |     1      |     2       |     3       |   4     |     5      |     6       |   7    |
| Food           | apple      | corn        | cranberry   | garlic  | lime       | mango       | orange |
| Movie-Genre    | action     | comedy      | epic        | fantasy | scientific | sports      | superhero |
| Music-Genre    | blues      | electronic  | house       | indie   | rock       | soul        | trance |
| Sport          | badminton  | basketball  | biathlon    | cycling | rowing     | rugby       | tennis |
"""




# Adapted RegEx to match the whole table structure with any content up to 7 columns and 7 rows
#pattern = r'/\|(\s*\w+\s*){1,7}\|(\s*\w+\s*){1,7}\|(\s*\w+\s*){1,7}\|(\s*\w+\s*){1,7}\|(\s*\w+\s*){1,7}\|(\s*\w+\s*){1,7}\|(\s*\w+\s*){1,7}\|/'

# Find the exact match of the table
match = re.findall(pattern, sample_text)

#for match in match:
print("matched: ")
print(match[-1][0])
#if match:
#    matched_string = match.group(0)  # Get the entire matched string
#    print("Matched Table Structure:")
#    print(matched_string)
#else:
#    print("No match found.")

import re

# Sample text with a table structure
sample_text = """
#############
|               |  1  |   2   |
| Music-Genre   | R&B | house |
#############
"""

# Adapted RegEx to match the whole table structure with any content (up to 7 columns and 7 rows)
pattern = r'#############\n(\|[\s\S]*?\|(?:\s*\n\|[\s\S]*?\|){0,6})\n#############'

# Find the exact match of the table
match = re.search(pattern, sample_text)

if match:
    matched_string = match.group(0)  # Get the entire matched string
    print("Matched Table Structure:")
    print(matched_string)
else:
    print("No match found.")


import re

# Sample text with a table structure with surrounding borders
sample_text_with_borders = """
#############
|               |  1  |   2   |
| Music-Genre   | R&B | house |
#############
"""

# Sample text with a table structure without surrounding borders
sample_text_without_borders = """
|               |  1  |   2   |
| Music-Genre   | R&B | house |
"""

# Adapted RegEx to match the whole table structure with optional borders
pattern = r'^(?:#############\n)?(\|[\s\S]*?\|(?:\s*\n\|[\s\S]*?\|){0,6})\n?(?:#############)?$'

# Test with both samples
for sample_text in [sample_text_with_borders, sample_text_without_borders]:
    match = re.match(pattern, sample_text.strip())  # Use re.match() to check from the start

    if match:
        matched_string = match.group(0)  # Get the entire matched string
        print("Matched Table Structure:")
        print(matched_string)
    else:
        print("No match found.")