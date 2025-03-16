from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

# Ensure prompt exists and that prompt is valid
prompt_path = "./prompt.txt"
if not os.path.exists(prompt_path):
    raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
with open(prompt_path, "r") as file:
    prompt_content = file.read()

# Create prompt template and extract variables
chat_prompt = ChatPromptTemplate.from_template(prompt_content)
required_variables = chat_prompt.input_variables

# Debugging
# print(f"Prompt template requires these variables: {required_variables}")

# Create input values
input_values = {}
career_field = input("Enter the career field you want to search for jobs in ")

# There is only one input field so we only have to alter that
input_values[required_variables[0]] = career_field

# # Initialize model with explicit connection parameters
try:
    model = ChatOllama(
        model="deepseek-r1:14b",
        base_url="http://localhost:11434",
        temperature=0.7,
    )
    print("Created model")

    # Add string output parser to ensure we get text
    chain = chat_prompt | model | StrOutputParser()
    print("Created Chain")

    print("Generating urls")
    # Invoke with proper variables
    response = chain.invoke(input_values)
    print("Finished generating urls")

    # Write to CSV
    file_path = "urls-to-crawl.csv"
    with open(file_path, "w", newline="") as file:
        file.write(response)

    print(f"CSV File created successfully: {file_path}")

except Exception as e:
    print(f"Error: {str(e)}")
    if "model not found" in str(e).lower():
        print("Try pulling the model first with: ollama pull deepseek-r1:8b")
    elif "connection" in str(e).lower():
        print("Check if Ollama is running and accessible at http://localhost:11434")
