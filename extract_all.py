import os
import sys
from pdfminer.high_level import extract_text as pdfminer_extract
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import io

# Paths
INPUT_DIR = r"c:\Users\pselv\Desktop\OCR\legaleey-ocr\input-pdf-file"
OUTPUT_DIR = r"c:\Users\pselv\Desktop\OCR\legaleey-ocr\output-text-file"

# Create output directory if it doesn't exist
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    print(f"Created output directory: {OUTPUT_DIR}", flush=True)

def is_text_rich(text, threshold=100):
    """Checks if the extracted text is substantial enough to be considered a text-based PDF."""
    if not text:
        return False
    # Remove whitespace and check length
    clean_text = "".join(text.split())
    return len(clean_text) > threshold

import fitz  # PyMuPDF
import easyocr

# Initialize EasyOCR reader (this will download model weights on first run if not present)
reader = easyocr.Reader(['en'])

from concurrent.futures import ThreadPoolExecutor
import functools

def process_single_page(page_idx, pdf_path):
    """Processes one page in a worker thread."""
    try:
        # Re-open doc per thread for safety
        doc = fitz.open(pdf_path)
        page = doc.load_page(page_idx)
        # 120 DPI is perfect for text OCR but much faster than 200
        pix = page.get_pixmap(dpi=120)
        img_bytes = pix.tobytes("png")
        result = reader.readtext(img_bytes, detail=0)
        doc.close()
        return "\n".join(result).strip()
    except Exception as e:
        print(f"      [Page Error] Page {page_idx+1} failed: {e}", flush=True)
        return ""

def extract_via_ocr(pdf_path):
    """Parallelized OCR using EasyOCR on CPU."""
    print(f"  [EasyOCR] Optimized Parallel Fallback for: {os.path.basename(pdf_path)}", flush=True)
    try:
        doc = fitz.open(pdf_path)
        max_pages = len(doc)
        doc.close()
        
        full_text_list = [None] * max_pages
        # Process pages in parallel (3 at a time is usually optimal for CPU-heavy tasks)
        with ThreadPoolExecutor(max_workers=3) as executor:
            pages_list = list(range(max_pages))
            partial_func = functools.partial(process_single_page, pdf_path=pdf_path)
            
            # Map pages to threads and collect results
            results = list(executor.map(partial_func, pages_list))
            
            for i, text in enumerate(results):
                if text:
                    full_text_list[i] = text
                    print(f"    Finished Page {i+1}/{max_pages}", flush=True)

        return "\n".join([t for t in full_text_list if t])
    except Exception as e:
        print(f"  [Error] Parallel EasyOCR failed for {pdf_path}: {e}", flush=True)
        return ""

def process_pdf(pdf_path):
    filename = os.path.basename(pdf_path)
    output_filename = os.path.splitext(filename)[0] + ".txt"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    # Skip if already exists
    if os.path.exists(output_path):
        print(f"Skipping (already exists): {filename}", flush=True)
        return

    print(f"Processing: {filename}", flush=True)
    
    try:
        # Step 1: Attempt direct text extraction
        extracted_text = pdfminer_extract(pdf_path)
        
        # Step 2: Decide if OCR is needed
        if not is_text_rich(extracted_text):
            # Fallback to OCR
            extracted_text = extract_via_ocr(pdf_path)
        else:
            print(f"  [Text] Success using direct extraction.", flush=True)

        # Step 3: Save to file
        if extracted_text.strip():
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(extracted_text)
            print(f"  [Done] Saved to {output_filename}", flush=True)
        else:
            print(f"  [Warning] No text extracted for {filename}", flush=True)

    except Exception as e:
        print(f"  [Error] Failed to process {filename}: {e}", flush=True)

def main():
    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".pdf")]
    print(f"Found {len(files)} PDF files in {INPUT_DIR}", flush=True)
    
    for i, filename in enumerate(files):
        pdf_path = os.path.join(INPUT_DIR, filename)
        process_pdf(pdf_path)
        print("-" * 20, flush=True)

if __name__ == "__main__":
    main()
