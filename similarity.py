# gt manual
import pytesseract
from PIL import Image
import boto3
import os

textract_client = boto3.client('textract')

def read_text_tesseract(image_path):
    text = pytesseract.image_to_string(Image.open(image_path), lang='eng')
    return text

def read_text_textract(image_path):
    with open(image_path, 'rb') as im:
        response = textract_client.detect_document_text(Document={'Bytes': im.read()})
    
    text = ''
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            text += item['Text'] + ' '
    
    return text.strip()

def jaccard_similarity(sentence1, sentence2):
    set1 = set(sentence1.split())
    set2 = set(sentence2.split())
    intersection_size = len(set1.intersection(set2))
    union_size = len(set1.union(set2))
    similarity = intersection_size / union_size if union_size != 0 else 0.0
    return similarity
ground_truth = {
    "images.jpg": " I SEE A LIGHT IN THE DARKNESS",
   
}
# Directory containing images
image_dir = "./image"

score_tesseract = 0
score_textract = 0
image_count = 0

for image_file in os.listdir(image_dir):
    image_path = os.path.join(image_dir, image_file)
    gt = ground_truth.get(image_file, "").replace('_', ' ')
    text_tesseract = read_text_tesseract(image_path).replace('\n', '').replace('!', '').replace('?', '').replace('.', '')
    text_textract = read_text_textract(image_path).replace('\n', '').replace('!', '').replace('?', '').replace('.', '')

   
    if image_count < 5:
        print(f"Image: {image_file}")
        print(f"Ground Truth: {gt}")
        print(f"Tesseract Text: {text_tesseract}")
        print(f"Textract Text: {text_textract}")
        print("------")

    if gt:  
        score_tesseract += jaccard_similarity(gt, text_tesseract)
        score_textract += jaccard_similarity(gt, text_textract)
    # print(score_tesseract)
    image_count += 1
# print(image_count)
average_score_tesseract = score_tesseract / image_count
average_score_textract = score_textract / image_count

print('Average Jaccard similarity score for Tesseract:', average_score_tesseract)
print('Average Jaccard similarity score for Textract:', average_score_textract)
