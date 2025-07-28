import os
import json
import fitz
import numpy as np
import re
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"
INPUT_JSON_PATH = os.path.join(INPUT_DIR, "challenge1b_input.json")
OUTPUT_JSON_PATH = os.path.join(OUTPUT_DIR, "challenge1b_output.json")

def extract_sections(pdf_path):
    """Extract sections from PDF with page numbers"""
    try:
        doc = fitz.open(pdf_path)
        sections = []
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text()
            
            # Extract sections names (all caps or title case)
            sections_names = re.findall(r'^([A-Z][A-Za-z\s\-]+)\n', text, re.MULTILINE)
            
            # Extract sections content
            for name in sections_names:
                # Find content after sections name
                pattern = re.compile(rf'{re.escape(name)}\n([\s\S]*?)(?=\n[A-Z][A-Za-z\s\-]+\n|\Z)')
                match = pattern.search(text)
                content = match.group(1).strip() if match else ""
                
                sections.append({
                    "page": page_num + 1,
                    "name": name.strip(),
                    "content": content
                })
                
        return sections
    except Exception as e:
        print(f"Error processing {pdf_path}: {str(e)}")
        return []

def create_input_json():
    """Generate input.json based on user input"""
    print("="*50)
    print("Adobe India Hackathon - Challenge 1B Input")
    print("="*50)
    
    # Get user input
    challenge_id = input("Enter challenge ID (e.g., round_1b_001): ")
    test_case_name = input("Enter test case name: ")
    description = input("Enter test case description: ")
    persona_role = input("Enter persona role (e.g., Food Contractor): ")
    job_task = input("Enter job to be done: ")
    
    # Get PDF files in input directory
    pdf_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".pdf")]
    
    # Create document list
    documents = [{"filename": f, "title": os.path.splitext(f)[0]} for f in pdf_files]
    
    # Create input data structure
    input_data = {
        "challenge_info": {
            "challenge_id": challenge_id,
            "test_case_name": test_case_name,
            "description": description
        },
        "documents": documents,
        "persona": {
            "role": persona_role
        },
        "job_to_be_done": {
            "task": job_task
        }
    }
    
    # Save to file
    with open(INPUT_JSON_PATH, "w") as f:
        json.dump(input_data, f, indent=2)
    print(f"Input JSON created at {INPUT_JSON_PATH}")
    
    return input_data

def main():
    # Create directories if needed
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Create or load input data
    if os.path.exists(INPUT_JSON_PATH):
        with open(INPUT_JSON_PATH, "r") as f:
            input_data = json.load(f)
        print("Loaded existing input.json")
    else:
        input_data = create_input_json()
    
    # Extract key information
    persona = input_data["persona"]["role"]
    job_task = input_data["job_to_be_done"]["task"]
    documents = input_data["documents"]
    
    # Process documents and extract sections
    all_sections = []
    for doc in documents:
        filename = doc["filename"]
        filepath = os.path.join(INPUT_DIR, filename)
        
        if not os.path.exists(filepath):
            print(f"PDF not found: {filename}")
            continue
            
        sections = extract_sections(filepath)
        for sections in sections:
            all_sections.append({
                "document": filename,
                "page": sections["page"],
                "name": sections["name"],
                "content": sections["content"]
            })
    
    # Prepare vectors for relevance ranking
    sections_names = [r["name"] for r in all_sections]
    sections_contents = [r["content"] for r in all_sections]
    
    # Create combined text for ranking
    combined_texts = [f"{name} {content}" for name, content in zip(sections_names, sections_contents)]
    
    # Initialize vectorizer
    vectorizer = TfidfVectorizer(stop_words='english', max_features=500)
    
    if combined_texts:
        # Fit and transform
        tfidf_matrix = vectorizer.fit_transform(combined_texts)
        
        # Create query vector
        query_text = f"{persona} {job_task}"
        query_vector = vectorizer.transform([query_text])
        
        # Calculate scores
        scores = cosine_similarity(query_vector, tfidf_matrix).flatten()
        
        # Add scores to sections
        for i, sections in enumerate(all_sections):
            sections["score"] = scores[i]
    else:
        for sections in all_sections:
            sections["score"] = 0
    
    # Sort sections by relevance
    all_sections.sort(key=lambda x: x["score"], reverse=True)
    
    # Prepare output
    output = {
        "metadata": {
            "input_documents": [doc["filename"] for doc in documents],
            "persona": persona,
            "job_to_be_done": job_task,
            "processing_timestamp": datetime.utcnow().isoformat() + "Z"
        },
        "extracted_sections": [
            {
                "document": sections["document"],
                "section_title": sections["name"],
                "importance_rank": i+1,
                "page_number": sections["page"]
            }
            for i, sections in enumerate(all_sections[:5])
        ],
        "subsection_analysis": [
            {
                "document": sections["document"],
                "refined_text": sections["content"][:500] + ("..." if len(sections["content"]) > 500 else ""),
                "page_number": sections["page"]
            }
            for sections in all_sections[:5]
        ]
    }
    
    # Save output
    with open(OUTPUT_JSON_PATH, "w") as f:
        json.dump(output, f, indent=2)
    print(f"Output JSON created at {OUTPUT_JSON_PATH}")
    print("Processing complete!")

if __name__ == "__main__":
    main()
