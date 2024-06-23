import os
import google.generativeai as genai
from PIL import Image

# Configure the Google AI API
genai.configure(api_key="AIzaSyDfOITonyTn3IepaZmOWsP4HnVy5V5tpkA")

def input_image_setup(image_path):
    try:
        with open(image_path, "rb") as image_file:
            bytes_data = image_file.read()
        mime_type = Image.open(image_path).format.lower()
        if mime_type == 'jpeg':
            mime_type = 'jpg'
        image_parts = [
            {
                "mime_type": f"image/{mime_type}",
                "data": bytes_data
            }
        ]
        return image_parts
    except Exception as e:
        print(f"Error reading image file {image_path}: {e}")
        return None

# Create the model configuration
generation_config = {
    "temperature": 0.9,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="Act as an OCR Expert",
)

# Prepare the prompt
prompt_template = "Extract all the text present in the given image."

def extract_data_from_image(image_path):
    image_data = input_image_setup(image_path)
    if not image_data:
        return None
    prompt = prompt_template
    input_data = image_data + [{"mime_type": "text/plain", "data": prompt.encode("utf-8-sig")}]

    try:
        response = model.generate_content(input_data)
        extracted_text = response.text
        return extracted_text.strip()
    except Exception as e:
        print(f"Error extracting data from image {image_path}: {e}")
        return None

def process_images(image_folder):
    # image_paths = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
    results = []
    # for image_path in image_paths:
    print(f"Processing image: {image_folder}")
    extracted_text = extract_data_from_image(image_folder)
    if extracted_text:
        print(f"Extracted text:\n{extracted_text}\n")
        results.append([image_folder, extracted_text])
    else:
        print(f"Failed to extract data for image: {image_folder}")
    return results

# results = process_images(image_folder)

