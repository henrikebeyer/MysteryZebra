import re
import csv
from transformers import AutoModelForCausalLM, AutoTokenizer
#from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, ConfusionMatrixDisplay
import pandas as pd

puzzle_file = "/home/oenni/Dokumente/LLM_reasoning/Puzzles_Natural_Language/Puzzles_orig/Puzzles_Level1_orig_Natural_Language/1x2-level1_orig_Natural_Language"

with open(puzzle_file, "r") as fin:
    puzzles = fin.read().strip("\n").split("#################################\n")[:-1]


model_name = "Qwen/Qwen2.5-7B-Instruct"

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)

tokenizer = AutoTokenizer.from_pretrained(model_name)

out_file = "/home/oenni/Dokumente/LLM_reasoning/Model_testing/Qwen2-zeroShot/2x3-level1_orig_solution.tsv"
i = 1
for puzzle in puzzles[:10]:
    clues = puzzle.split("::.")[1].replace("##1","").replace(".:: Answer", "")
    answer = puzzle.split(".:: Answer ::.")[-1]

    items = ", ".join(list(re.findall(": [A-Za-z-7& ,]+", clues))).replace(": ","").split(", ")

    print(clues)
    print(items)
    print(answer)

    empty = answer

    for item in items:
        empty=empty.replace(item, " "*len(item))

    
    messages = [
    {"role": "user", "content": f"Please solve the following logic puzzle in the following table: \n\n {empty} \n\n Puzzle: \n {clues}. Please put '#############' around the final solution table."}]

    #print(messages)

    text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=10000,
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    with open(out_file, "a") as fout:
        csv_writer = csv.writer(fout, delimiter="\t")
        csv_writer.writerow([f"Lv1-1x2-{i}", response])

    i+= 1
    #predictions.append(response)