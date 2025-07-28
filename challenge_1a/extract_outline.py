import fitz  # PyMuPDF
import os
import json
import unicodedata

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
                            text = span["text"].strip()
                            if is_valid_heading(text):
                                return text
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

def is_valid_heading(text):
    # Normalize Unicode (NFKC covers Japanese full-width to half-width)
    normalized = unicodedata.normalize("NFKC", text)
    # Check if text has at least 2 alphanumeric or Japanese characters
    return any(char.isalnum() for char in normalized) and len(normalized) > 2

def extract_outline(doc):
    outline = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    text = span["text"].strip()
                    level = determine_heading_level(span["size"])
                    if level and is_valid_heading(text):
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
            with open(os.path.join(OUTPUT_DIR, json_filename), "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
