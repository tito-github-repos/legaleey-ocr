import pytesseract
from PIL import Image
import boto3
import os

# Initialize Textract client
textract_client = boto3.client('textract')

def read_text_tesseract(image_path):
    try:
        text = pytesseract.image_to_string(Image.open(image_path), lang='eng')
        return text
    except Exception as e:
        print(f"Error reading image with Tesseract: {e}")
        return ""

def read_text_textract(image_path):
    try:
        with open(image_path, 'rb') as im:
            response = textract_client.detect_document_text(Document={'Bytes': im.read()})

        text = ''
        for item in response['Blocks']:
            if item['BlockType'] == 'LINE':
                text += item['Text'] + ' '

        return text.strip()
    except Exception as e:
        print(f"Error reading image with Textract: {e}")
        return ""

def calculate_precision_recall_f1(ground_truth, extracted_text):
    gt_words = set(ground_truth.lower().split())
    extracted_words = set(extracted_text.lower().split())

    true_positive = len(gt_words.intersection(extracted_words))
    false_positive = len(extracted_words - gt_words)
    false_negative = len(gt_words - extracted_words)

    precision = true_positive / (true_positive + false_positive) if (true_positive + false_positive) > 0 else 0
    recall = true_positive / (true_positive + false_negative) if (true_positive + false_negative) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return precision, recall, f1

# Ground truth text for images
ground_truth = {
    "images.jpg": "I SEE A LIGHT IN THE DARKNESS",
    "image2.jpg": "ANOTHER EXAMPLE TEXT",
   
}

# Directory containing images
image_dir = "./image"

precision_tesseract = 0
recall_tesseract = 0
f1_tesseract = 0

precision_textract = 0
recall_textract = 0
f1_textract = 0

image_count = 0

for image_file in os.listdir(image_dir):
    image_path = os.path.join(image_dir, image_file)
    gt = ground_truth.get(image_file, "").replace('_', ' ')
    text_tesseract = read_text_tesseract(image_path).replace('\n', ' ').strip()
    text_textract = read_text_textract(image_path).replace('\n', ' ').strip()

    if gt:  
        p_t, r_t, f1_t = calculate_precision_recall_f1(gt, text_tesseract)
        p_tex, r_tex, f1_tex = calculate_precision_recall_f1(gt, text_textract)

        precision_tesseract += p_t
        recall_tesseract += r_t
        f1_tesseract += f1_t

        precision_textract += p_tex
        recall_textract += r_tex
        f1_textract += f1_tex

    image_count += 1

average_precision_tesseract = precision_tesseract / image_count if image_count > 0 else 0
average_recall_tesseract = recall_tesseract / image_count if image_count > 0 else 0
average_f1_tesseract = f1_tesseract / image_count if image_count > 0 else 0

average_precision_textract = precision_textract / image_count if image_count > 0 else 0
average_recall_textract = recall_textract / image_count if image_count > 0 else 0
average_f1_textract = f1_textract / image_count if image_count > 0 else 0

print(f'Average Precision for Tesseract: {average_precision_tesseract:.4f}')
print(f'Average Recall for Tesseract: {average_recall_tesseract:.4f}')
print(f'Average F1 Score for Tesseract: {average_f1_tesseract:.4f}')

print(f'Average Precision for Textract: {average_precision_textract:.4f}')
print(f'Average Recall for Textract: {average_recall_textract:.4f}')
print(f'Average F1 Score for Textract: {average_f1_textract:.4f}')
