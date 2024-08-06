# import cv2

# img = cv2.imread("./source/blur.png")
# img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# img = cv2.resize(img, (560, 900))

# _, result = cv2.threshold(img, 20, 220, cv2.THRESH_BINARY)  #threshhold mean we have to change a color 0-255 0 means black 255 means wighht

# adaptive_result = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                                         cv2.THRESH_BINARY, 45, 5)

# cv2.imshow("result", result)
# cv2.imshow("original", img)
# cv2.imshow("adaptive", adaptive_result)
# cv2.waitKey(0)

import cv2
from pytesseract import image_to_string
# from pdf2image import convert_from_paths
from PIL import Image
import numpy as np

import datetime 
# Load and preprocess the image
img = cv2.imread("./source/blur.png")
start_time=datetime.datetime.now()
if img is None:
    print("Error: Image not loaded. Check the file path.")
    exit()

img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img = cv2.resize(img, (560, 900))


# Apply global thresholding
_, result = cv2.threshold(img, 20, 255, cv2.THRESH_BINARY)

# Apply adaptive thresholding
adaptive_result = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY, 45, 5)

cv2.imwrite("./source/adaptive_result.png", adaptive_result)

# Remove or comment out the display code
# cv2.imshow("result", result)
# cv2.imshow("original", img)
# cv2.imshow("adaptive", adaptive_result)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# Convert the adaptive threshold result to PIL Image format for Tesseract
processed_image = Image.fromarray(adaptive_result)

# Extract text from the processed image
extracted_text = image_to_string(processed_image, config='--psm 6')
print(f"Extracted text: {extracted_text}")

# Save the extracted text to a file
output_file_path = 'blur-png.txt'
try:
    with open(output_file_path, 'w') as text_file:
        text_file.write(extracted_text)
    print(f"Text successfully written to {output_file_path}")
except IOError as e:
    print(f"Error writing to file: {e}")
endtime = datetime.datetime.now()
print(endtime - start_time)