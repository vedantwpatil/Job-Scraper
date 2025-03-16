# Formatting the data so it can be used by Scrapy
import re
import os
import csv


def extract_code_block(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    # Find content between triple backticks
    pattern = r"```\s*([\s\S]*?)\s*```"
    match = re.search(pattern, content)
    if match:
        csv_content = match.group(1)
        return csv_content
    else:
        return "No code block found in the file."


def clean_and_validate_csv(csv_content):
    # Split the content into lines
    lines = csv_content.strip().split("\n")
    cleaned_lines = []

    for line_num, line in enumerate(lines, 1):
        # Skip empty lines
        if not line.strip():
            continue

        # Parse the line as CSV
        reader = csv.reader([line])
        row = next(reader)

        # Check if we have fewer than 3 columns
        if len(row) < 3:
            print(f"Warning: Line {line_num} has fewer than 3 columns: {row}")
            continue

        # Handle extra columns by keeping only the first 3
        if len(row) > 3:
            print(
                f"Fixed: Line {line_num} had {len(row)} columns, trimming to 3: {row}"
            )
            row = row[:3]

        # Clean each column
        company_name = row[0].strip()

        # Clean domain - remove parentheses and whitespace
        domain = row[1].strip()
        domain = re.sub(r"[\(\)]", "", domain)  # Remove parentheses

        # Clean URL
        url = row[2].strip()

        # Create a new clean row
        cleaned_row = f"{company_name},{domain},{url}"
        cleaned_lines.append(cleaned_row)

    return "\n".join(cleaned_lines)


def save_csv_content(csv_content, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(csv_content)


# Ensure that the file exists
file_path = "./urls-to-crawl.csv"
if not os.path.exists(file_path):
    raise FileNotFoundError(f"Prompt file not found: {file_path}")

input_file = "./urls-to-crawl.csv"
output_file = "./urls-to-crawl-cleaned.csv"

# Extract content
raw_csv_content = extract_code_block(input_file)

# Clean and validate
cleaned_csv_content = clean_and_validate_csv(raw_csv_content)

# Save cleaned content
save_csv_content(cleaned_csv_content, output_file)

print(f"CSV content extracted, cleaned, and saved to {output_file}")

# Extra validation step - read the output file to check formatting
print("\nValidating the cleaned file...")
with open(output_file, "r") as file:
    reader = csv.reader(file)
    for i, row in enumerate(reader, 1):
        if len(row) != 3:
            # print(f"Error: Row {i} in cleaned file still has {len(row)} columns: {row}")
            pass
        else:
            company, domain, url = row
            # print(f"Row {i}: Company='{company}', Domain='{domain}', URL='{url}'")

print("\nValidation complete!")
