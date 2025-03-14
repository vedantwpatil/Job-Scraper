import csv

promt_path = "./prompt.txt"
prompt = ""
with open(promt_path, "r") as file:
    for line in file:
        prompt += line
print(prompt)
