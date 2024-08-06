import boto3

def extract_text_from_image(image_path):
    client = boto3.client('textract')

    with open(image_path, 'rb') as image_file:
        image_bytes = image_file.read()

    response = client.detect_document_text(
        Document={'Bytes': image_bytes}
    )

    text = ''
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE': 
            text += item['Text'] + '\n'

    return text

if __name__ == "__main__":
    image_path = './source/images.jpg'  
    extracted_text = extract_text_from_image(image_path)
    print(extracted_text)
