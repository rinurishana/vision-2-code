import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import re

# -------------------------------
# 1. Load Model
# -------------------------------
MODEL_NAME = "google/flan-t5-base"

print("Loading model... (first time may take time)")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

print("Model loaded on:", device)


# -------------------------------
# 2. Clean HTML Output
# -------------------------------
def clean_html(html):
    # Remove unwanted tokens or text
    html = html.strip()

    # Remove repeated tags or weird artifacts
    html = re.sub(r'\s+', ' ', html)

    # Ensure basic structure exists
    if "<html" not in html:
        html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Generated Page</title>
</head>
<body>
{html}
</body>
</html>
"""
    return html


# -------------------------------
# 3. Generate HTML from Text
# -------------------------------
def text_to_html(text):
    prompt = f"""
You are a professional web developer.

Convert the following plain text into a clean, well-structured HTML5 document.

Requirements:
- Use proper HTML tags (<html>, <head>, <body>)
- Add headings (<h1>, <h2>)
- Use lists if needed
- Add inline CSS for styling
- Make it visually clean

Text:
{text}

Return ONLY HTML code.
"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    ).to(device)

    outputs = model.generate(
        inputs.input_ids,
        max_length=1024,
        temperature=0.6,
        top_p=0.9,
        num_beams=6,
        early_stopping=True
    )

    html = tokenizer.decode(outputs[0], skip_special_tokens=True)
    html = clean_html(html)

    return html


# -------------------------------
# 4. Save HTML File
# -------------------------------
def save_html(html, filename="output.html"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"HTML saved as {filename}")


# -------------------------------
# 5. Main Function (CLI Support)
# -------------------------------
def main():
    print("\n=== TEXT TO HTML GENERATOR ===\n")

    print("Enter your text (type 'END' in new line to finish):\n")

    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)

    text = "\n".join(lines)

    if not text.strip():
        print("No input provided!")
        return

    print("\nGenerating HTML...\n")
    html = text_to_html(text)

    print("\nGenerated HTML:\n")
    print(html)

    save_html(html)


# -------------------------------
# Run Program
# -------------------------------