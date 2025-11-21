from anthropic import Anthropic
import json
import os

client = Anthropic(api_key="XXXXXXX")
def clean(code):
    clean_prompt = f"""
    You are an AI trained to rewrite messy Python code while preserving EXACT FUNCTIONALITY.

    ### HARD RULES ###
    - DO NOT CHANGE what the function does.
    - DO NOT change return values.
    - DO NOT change math, string manipulation, loops, or logic.
    - The cleaned code MUST behave identically when executed.
    - Only rewrite STYLE, not behavior.

    ### STYLE RULES ###
    - Improve variable names but keep semantics identical
    - Maintain original algorithm
    - Keep same inputs and same outputs
    - Use consistent indentation
    - Remove unused imports
    - Remove dead code
    - Improve comments, but do not delete meaningful ones
    - Output ONLY the code, no explanations, no backticks

    ### CODE TO CLEAN
    {code}
    """

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1500,
        messages=[{"role": "user", "content": clean_prompt}],
    )

    clean_code = response.content[0].text.strip()
    return clean_code

def messy():
    messy_prompt = """
    Produce messy Python code that still implements a REAL function.

    The code MUST:
    - perform a real operation (math, string manipulation, sorting, filtering, etc.)
    - contain unnecessary indentation
    - contain bad variable names
    - contain unnecessary variables
    - contain dead code
    - contain ugly comments
    - follow the SAME algorithm from start to finish
    - Output ONLY the code, no explanations, no backticks

    Do NOT create random unrelated behavior.
    """

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1500,
        messages=[{"role": "user", "content": messy_prompt}],
    )

    messy_code = response.content[0].text.strip()
    clean_code = clean(messy_code)
    data = {
        "messy_code": messy_code,
        "clean_code": clean_code
    }
    return data

with open("paired_codes.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

for i in range(2600):
    pair = messy()
    dataset.append(pair)
    with open("paired_codes.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(pair) + "\n")
    print(i+1, " complete")

with open("paired_codes.json", "w") as f:
    json.dump(dataset, f, indent=2)

print("Code saved → paired_codes.json")
