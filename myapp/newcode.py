from transformers import BlipProcessor, BlipForConditionalGeneration
from transformers import AutoTokenizer, AutoModelForCausalLM
from PIL import Image
import torch

# Load image captioning model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model_img = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Load code generation model
tokenizer = AutoTokenizer.from_pretrained("Salesforce/codegen-350M-multi")
model_code = AutoModelForCausalLM.from_pretrained("Salesforce/codegen-350M-multi")
def image_based_gen(img_path):
    # Load image
    image = Image.open(img_path).convert('RGB')

    # Step 1: Generate description
    inputs = processor(images=image, return_tensors="pt")
    out = model_img.generate(**inputs)
    description = processor.decode(out[0], skip_special_tokens=True)

    print("UI Description:", description)

    return  description