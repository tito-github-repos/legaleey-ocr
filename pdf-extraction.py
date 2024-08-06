from pdfminer.high_level import extract_text
import os
import datetime 

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file.
    
    Args:
    pdf_path (str): The path to the PDF file.
    
    Returns:
    str: The extracted text from the PDF.
    """
    if not os.path.exists (pdf_path):
        raise FileNotFoundError(f"The specified PDF file does not exist: {pdf_path}")

    try:
        # Extract text from the PDF
        text = extract_text(pdf_path)
        return text
    except Exception as e:
        raise RuntimeError(f"An error occurred while extracting text from the PDF: {e}")

def main():
    # Path to the PDF file
    pdf_path = './source/word.pdf'
    start_time=datetime.datetime.now()
    
    try:
        # Extract text from the PDF
        text = extract_text_from_pdf(pdf_path)
        
        # Print the extracted text
        if text:
            print("Extracted Text:\n", text)
        else:
            print("No text found in the PDF.")
    except Exception as e:
        print(e)
    
    endtime = datetime.datetime.now()

    print(endtime - start_time)
if __name__ == "__main__":
    main()
