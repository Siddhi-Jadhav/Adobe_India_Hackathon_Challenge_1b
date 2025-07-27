import fitz  # PyMuPDF
import os
import json
import re

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"

def extract_title(doc):
    for page_num in range(min(3, len(doc))):  # Check first 3 pages
        blocks = doc.load_page(page_num).get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        if span["size"] > 15:  # Arbitrary threshold
                            return span["text"]
    return "Untitled Document"

def determine_heading_level(font_size):
    if font_size >= 16:
        return "H1"
    elif font_size >= 13:
        return "H2"
    elif font_size >= 11:
        return "H3"
    else:
        return None

def extract_outline(doc):
    outline = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    level = determine_heading_level(span["size"])
                    text = span["text"].strip()
                    if level and text and re.match(r'^[A-Z0-9].{2,}', text):
                        outline.append({
                            "level": level,
                            "text": text,
                            "page": page_num + 1
                        })
    return outline

def process_pdf_file(pdf_path):
    doc = fitz.open(pdf_path)
    title = extract_title(doc)
    outline = extract_outline(doc)
    return {"title": title, "outline": outline}

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(INPUT_DIR, filename)
            result = process_pdf_file(pdf_path)
            json_filename = os.path.splitext(filename)[0] + ".json"
            with open(os.path.join(OUTPUT_DIR, json_filename), "w") as f:
                json.dump(result, f, indent=2)

if __name__ == "__main__":
    main()
