from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate, PromptTemplate

import pandas as pd
import csv

promt_path = "./prompt.txt"
prompt = ""
with open(promt_path, "r") as file:
    for line in file:
        prompt += line

model_version = "deepseek-r1:8b"
model = ChatOllama(model=model_version)

chat_prompt = ChatPromptTemplate.from_template(prompt)
print(chat_prompt)

chain = chat_prompt | model
response = chain.invoke({})


csv_content = response.content

file_path = "urls-to-scrape.csv"

with open(file_path, "w", newline="") as file:
    file.write(csv_content)

print("CSV File created successfully: {file_path}")
