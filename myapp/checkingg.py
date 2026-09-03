# from transformers import BlipProcessor, BlipForConditionalGeneration
# from transformers import AutoTokenizer, AutoModelForCausalLM
# from PIL import Image
# import torch
#
# # Load image captioning model
# processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
# model_img = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
#
# # Load code generation model
# tokenizer = AutoTokenizer.from_pretrained("Salesforce/codegen-350M-multi")
# model_code = AutoModelForCausalLM.from_pretrained("Salesforce/codegen-350M-multi")
#
# # Load image
# image = Image.open("ui image.jpg").convert('RGB')
#
# # Step 1: Generate description
# inputs = processor(images=image, return_tensors="pt")
# out = model_img.generate(**inputs)
# description = processor.decode(out[0], skip_special_tokens=True)
#
# print("UI Description:", description)
#
# # Step 2: Convert description → code
# # prompt = f"""
# # Convert this UI description into clean HTML code:
# #
# # # {description}
# #
# # HTML Code:
# # """
# prompt = f"""
# Convert this UI description into clean HTML code:
#
# registration page with name as text filed, dob as date filed, gender as radio, username as text and password as password filed with nice design include blue background
#
# HTML Code:
# """
#
# inputs = tokenizer(prompt, return_tensors="pt")
# outputs = model_code.generate(**inputs, max_length=2048)
#
# code = tokenizer.decode(outputs[0], skip_special_tokens=True)
# print(code)

# =========================================
# TEXT → HTML GENERATOR (LIGHTWEIGHT MODEL)
# =========================================

from transformers import pipeline

# ------------------------------
# Load Small Model (Fast + CPU)
# ------------------------------
print("Loading lightweight model...")

generator = pipeline(
    "text-generation",
    model="tiiuae/falcon-rw-1b",   # small and efficient
    device=-1  # CPU mode
)

# ------------------------------
# Function: Text → HTML
# ------------------------------
def text_to_html(text):

    prompt = f"""
You are a professional web designer.

Convert the following text into a complete HTML5 page with:
- Clean HTML structure
- Internal CSS styling
- Attractive UI (gradient background, card layout)
- Use headings, paragraphs, and lists properly

ONLY RETURN HTML CODE.

TEXT:
{text}

HTML:
"""

    result = generator(
        prompt,
        max_length=600,
        temperature=0.7,
        top_p=0.9,
        do_sample=True
    )

    generated_text = result[0]['generated_text']

    # Try extracting only HTML content
    start = generated_text.lower().find("<!doctype html>")
    if start != -1:
        return generated_text[start:]
    else:
        return generated_text


# ------------------------------
# Main Execution
# ------------------------------
if __name__ == "__main__":

    # Input text
    input_text = """
Welcome to My AI Website

This platform includes:
- Machine Learning
- Deep Learning
- Web Development

We provide innovative solutions using AI.
Contact us for more information.
"""

    print("\nGenerating HTML...\n")

    html_output = text_to_html(input_text)

    # Save to file
    output_file = "output.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_output)

    print(f"✅ HTML successfully generated and saved as '{output_file}'")