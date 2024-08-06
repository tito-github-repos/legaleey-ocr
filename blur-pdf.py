from pdf2image import convert_from_path
from pytesseract import image_to_string
from PIL import Image
import cv2
import numpy as np

# Path to the PDF file
pdf_path = "./source/word.pdf"

# Convert PDF pages to images
pages = convert_from_path(pdf_path, dpi=300)

all_text = ""

# Process each page image
for i, page in enumerate(pages):
    # Convert PIL image to OpenCV format (NumPy array)
    img = np.array(page)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  
    img = cv2.resize(img, (560, 900))  

    # Apply adaptive thresholding
    adaptive_result = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                            cv2.THRESH_BINARY, 45, 5)

    # Convert back to PIL format for Tesseract
    processed_image = Image.fromarray(adaptive_result)

    # Extract text from the processed image
    extracted_text = image_to_string(processed_image, config='--psm 6')
    print(f"Extracted text: {extracted_text}")

    # Append the extracted text to the overall text
    all_text += extracted_text + "\n"  

# Save the extracted text to a file
output_file_path = 'blur-pdf.txt'
try:
    with open(output_file_path, 'w') as text_file:
        text_file.write(all_text)
    print(f"Text successfully written to {output_file_path}")
except IOError as e:
    print(f"Error writing to file: {e}")
