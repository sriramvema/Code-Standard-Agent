from anthropic import Anthropic
import json
import os

client = Anthropic(api_key="XXXXXXXXX")
def clean(code):
    clean_prompt = """
    You are an AI that converts BAD, messy, chaotic, unoptimized code into clean code that follows coding standards.
    Rules:
    - Use descriptive, meaningful variable names
    - Use consistent indentation
    - Remove unused imports
    - Use small, single-purpose functions
    - Avoid deeply nested code
    - Comments should be meaningful
    - Only return the code
    - DO NOT wrap the code in backticks. Output ONLY the raw code.

    Here is the code you should convert: {code}.
    """

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=300,
        messages=[{"role": "user", "content": clean_prompt}],
    )

    clean_code = response.content[0].text.strip()
    return clean_code

def messy():
    messy_prompt = """
    You are an AI that generates BAD, messy, chaotic, unoptimized code.
    Rules:
    - Unnecessary indentation
    - Ugly variable names
    - Useless comments
    - Dead code
    - Anti-patterns
    - Only output the code.
    - 10 to 25 lines of code
    - DO NOT wrap the code in backticks. Output ONLY the raw code.

    Generate a messy Python function.
    """

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=300,
        messages=[{"role": "user", "content": messy_prompt}],
    )

    messy_code = response.content[0].text.strip()
    clean_code = clean(messy_code)
    data = {
        "messy_code": messy_code,
        "clean_code": clean_code
    }
    return data

dataset = []
for i in range(0, 100):
    dataset.append(messy())
    print(i, " complete")

with open("paired_codes.json", "w") as f:
    json.dump(dataset, f, indent=2)

print("Code saved → paired_codes.json")
