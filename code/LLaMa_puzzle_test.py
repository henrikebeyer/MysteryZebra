import re
import csv
import transformers
import torch
#from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, ConfusionMatrixDisplay
import pandas as pd

rows = 3
cols = 6

puzzle_file = f"/home/oenni/Dokumente/LLM_reasoning/Puzzles_Natural_Language/Puzzles_orig/Puzzles_Level1_orig_Natural_Language/{rows}x{cols}-level1_orig_Natural_Language"

with open(puzzle_file, "r") as fin:
    puzzles = fin.read().strip("\n").split("#################################\n")[:-1]


model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
torch.cuda.is_available()

pipeline = transformers.pipeline("text-generation", 
                                 model=model_id, 
                                 model_kwargs={"torch_dtype":torch.float16}, 
                                 device_map="auto",
                                )



out_file = f"/home/oenni/Dokumente/LLM_reasoning/Model_testing/LLaMa3-8B-Instruct-zeroShot/{rows}x{cols}-level1_orig_solution.tsv"
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

    terminators = [
        pipeline.tokenizer.eos_token_id,
        pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]

    outputs = pipeline(
        messages,
        max_new_tokens=10000,
        eos_token_id=terminators,
        do_sample=True,
        temperature=0.1,
        top_p=0.9,
    )
    response = outputs[0]["generated_text"][-1]["content"]

    #print(response)

    with open(out_file, "a") as fout:
        csv_writer = csv.writer(fout, delimiter="\t")
        if i == 1:
            csv_writer.writerow(["Puzzle-ID", "LLaMa-8B-Instruct output"])
        csv_writer.writerow([f"Lv1-{rows}x{cols}-{i}", response])

    i+= 1
    #predictions.append(response)