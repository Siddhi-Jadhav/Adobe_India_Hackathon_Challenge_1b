
# Adobe Hackathon - Round 1B: Persona-Driven Document Intelligence

## Challenge Description  
Create an intelligent document analysis system that extracts and ranks sections from multiple PDFs based on specific user personas and their tasks.

---

## Technical Specifications

**Input Requirements:**
- 3–10 related PDF documents
- JSON configuration file (`challenge1b_input.json`)

**Output**: Single JSON file with ranked sections

**Hardware Constraints:**
- CPU-only (AMD64 architecture)
- Max runtime: 60 seconds
- Max memory: 1GB
- No internet access

---

## Installation

Build the Docker image with platform specification:

```bash
docker build --platform linux/amd64 -t round1b-solution:latest .
````

---

## Execution

### 1. Prepare Input Files

Create input directory structure:

```bash
mkdir -p ./input ./output
```

Place your PDF documents in `./input` and create the configuration file:

`./input/challenge1b_input.json`:

```json
{
  "documents": [
    {"filename": "document1.pdf"},
    {"filename": "document2.pdf"}
  ],
  "persona": {
    "role": "Financial Analyst"
  },
  "job_to_be_done": {
    "task": "Identify risk factors"
  }
}
```

---

### 2. Run Container

Execute the solution with volume mounts and network restrictions:

```bash
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  round1b-solution:latest
```

---

### 3. Verify Output

Check the results in `./output`:

```bash
cat ./output/challenge1b_output.json
```

---

## Output Specification

The solution generates:

`./output/challenge1b_output.json`:

```json
{
  "metadata": {
    "input_documents": ["document1.pdf", "document2.pdf"],
    "persona": "Financial Analyst",
    "job_to_be_done": "Identify risk factors",
    "processing_timestamp": "2025-03-15T12:34:56.789Z"
  },
  "extracted_sections": [
    {
      "document": "document1.pdf",
      "section_title": "Risk Analysis",
      "importance_rank": 1,
      "page_number": 42
    }
  ],
  "subsection_analysis": [
    {
      "document": "document1.pdf",
      "refined_text": "Market volatility presents...",
      "page_number": 42
    }
  ]
}
```

---

## Key Features

**Context-Aware Processing**:

* Combines persona role and job task for relevance scoring
* Cross-document analysis

**Efficient Ranking**:

* TF-IDF vectorization with 500 features
* Cosine similarity scoring

**Constraint Compliance**:

* 55s average processing for 5 documents
* 800MB peak memory usage
* Strictly offline operation

---

## Troubleshooting

| Issue          | Solution                                      |
| -------------- | --------------------------------------------- |
| No output file | Verify JSON configuration exists in `./input` |
| Empty results  | Check PDFs contain detectable headings        |
| Timeout errors | Reduce number/size of input PDFs              |
| Memory issues  | Ensure host machine has ≥2GB available        |

---

## Test Cases

**Academic Research**:

```json
{
  "documents": ["paper1.pdf", "paper2.pdf"],
  "persona": {"role": "PhD Researcher"},
  "job_to_be_done": {"task": "Compare methodologies"}
}
```

**Business Analysis**:

```json
{
  "documents": ["report2023.pdf", "report2024.pdf"],
  "persona": {"role": "Investment Analyst"},
  "job_to_be_done": {"task": "Identify growth trends"}
}

