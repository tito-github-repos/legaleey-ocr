import boto3
from trp import Document
import botocore.exceptions

s3BucketName= "tito-users-dev"
PlaindocumentName = "form-1-page.pdf"
# FormdocumentName = "form-1-page.pdf"
# TabledocumentName = "form-1-page.pdf"

# amazon textract client
textractmodule = boto3.client('textract', region_name='us-east-1')

# 1. plain text detection form document

response = textractmodule.detect_document_text(
    Document={
        "S3Object" : {
            "Bucket" : s3BucketName,
            "Name" : PlaindocumentName
        }
    }
) 
print("................print plaintext detected text ..........................")

for item in response ["Blocks"]:
    if item["BlockType"] == "LINE":
        print( item["Text"])

# 2. Form detection from document
response= textractmodule.analyze_document(
     Document={
        "S3Object" : {
            "Bucket" : s3BucketName,
            "Name" : PlaindocumentName
        }
    },
    FeatureTypes=["FORMS"]
)
doc = Document(response)
print("................Print Form detected text ................")
for page in doc.pages:
    for field in page.form.fields:
        print("key: {}, value: {}". format(field.key, field.value))

# 3. Table detection from documents:

response = textractmodule.analyze_document(
    Document = {
        "S3Object" :{  'Bucket' : s3BucketName,
        'Name' : PlaindocumentName
        }
      
    },
    FeatureTypes = ["TABLES"]

)
doc = Document(response)
print ("................print table detected text .......................")
for page in doc.pages:
    for table in page.tables:
        for r, row in enumerate(table.rows):
            itemName=""
            for c, cell in enumerate(row.cells):
                print("Table[{}] [{}] = {}".format(r, c, cell.text))

