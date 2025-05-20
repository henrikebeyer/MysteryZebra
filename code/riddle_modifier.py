facts_path = "/home/oenni/Dokumente/LLM_reasoning/Riddles/Einstein_orig/Einstein_orig_facts.txt"
rules_path = "/home/oenni/Dokumente/LLM_reasoning/Riddles/Einstein_orig/Einstein_orig_rules.txt"

with open(rules_path, "r") as fin:
    rules = fin.read().split("\n")

with open(facts_path, "r") as fin:
    facts = fin.read().split("\n")

categories=[]
for fact in facts[:-1]:
    cats = fact.split(": ")[-1].replace(" and", ",").replace(" or",",").replace(".","").split(", ")
    categories.append(cats)

for rule in rules:
    print(rule)