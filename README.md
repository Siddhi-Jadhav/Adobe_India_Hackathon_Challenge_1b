# 📄 Adobe Connecting the Dots – Round 1B Submission

## 🎯 Problem Statement: Persona-Driven Document Intelligence

The objective of **Round 1B** is to build an intelligent system that extracts and ranks the most relevant sections from a collection of PDFs, based on a given persona and their job-to-be-done. The output should be a structured, ranked, and context-aware JSON summary.

---

## 🛠️ Solution Overview

Our system takes in:
- A set of PDFs
- A JSON input with persona and task definition

It returns:
- Metadata
- Ranked section-level and sub-section-level outputs
- Relevant refined text passages based on semantic similarity

Key Components:
- Text extraction with **PyMuPDF**
- Relevance scoring using **TF-IDF + Cosine Similarity**
- Timestamped, persona-aware output in JSON format

---

## 📂 Project Structure

Challenge_1b/
├── input/ # Folder with input PDFs and challenge1b_input.json
│ ├── file1.pdf
│ └── challenge1b_input.json
├── output/ # Folder for saving challenge1b_output.json
├── run.py # Entry-point script that calls 
├── Dockerfile # Container setup for AMD64-compatible systems
└── README.md # Project documentation

yaml
Copy
Edit

---

## 🚀 How to Run

### 🐳 Docker-Based Execution (Recommended)

Make sure your current directory contains the following:
- `input/` folder with PDFs and `challenge1b_input.json`
- `Dockerfile`, `run.py`, and `pp.py` in the root

### ✅ Build the Docker Image

```bash
docker build --platform linux/amd64 -t challenge1b-solution .
▶️ Run the Docker Container
bash
Copy
Edit
docker run --rm \
  -v "$(pwd)/input:/app/input" \
  -v "$(pwd)/output:/app/output" \
  --network none \
  challenge1b-solution
🪟 On Windows PowerShell:

powershell
Copy
Edit
docker run --rm `
  -v "${PWD}/input:/app/input" `
  -v "${PWD}/output:/app/output" `
  --network none `
  challenge1b-solution
🧠 How It Works
Preprocessing:

PDFs are read and parsed page by page.

All text blocks are extracted with positional data.

Persona Relevance Scoring:

The persona and job text are converted into TF-IDF vectors.

Each section/subsection of the documents is compared to this using cosine similarity.

Ranking & Extraction:

Sections are ranked using their similarity scores.

Top sections and corresponding text are written in challenge1b_output.json.

📤 Output Format
The output is a structured JSON file saved to output/challenge1b_output.json. It contains:

Input metadata

Ranked section details

Refined sub-section text

Processing timestamp

Refer to the official problem sample for format details.

📦 Dependencies (installed inside Docker)
PyMuPDF

scikit-learn

numpy

re, json, datetime, os

No external APIs or internet access are used.

🧪 Evaluation Criteria
✅ Persona + job relevance

✅ Semantic ranking accuracy

✅ Clean JSON output with metadata and ranked content

✅ Compliant with time and model size constraints

👨‍💻 Author
This project was built for Adobe India Hackathon 2025 - Round 1B by the submitting team. All logic is contained locally and packaged via Docker.
