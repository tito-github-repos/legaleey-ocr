from pdf2image import convert_from_path
from pytesseract import image_to_string
import datetime 
def convert_pdf_to_img(pdf_file):
    return convert_from_path(pdf_file)

def convert_image_to_text(file):
    text = image_to_string(file)
    return text

def get_text_from_any_pdf(pdf_file):
    images = convert_pdf_to_img(pdf_file)
    final_text = ""
    for pg, img in enumerate(images):
        text = convert_image_to_text(img)
        final_text += text
    return final_text

# Path to the PDF file
path_to_pdf =  './source/word.pdf'
start_time=datetime.datetime.now()

# Extract text from the PDF
extracted_text = get_text_from_any_pdf(path_to_pdf)

# Save the extracted text to a single file
with open('text-new.txt', 'w') as text_file:
    text_file.write(extracted_text)
endtime = datetime.datetime.now()

# Print the extracted text
print(extracted_text)
print(endtime - start_time)