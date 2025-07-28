# Adobe India Hackathon: Document Processing Solutions

## Challenge Overview
This project addresses Adobe's "Connecting the Dots" hackathon challenges to transform static PDFs into intelligent, structured documents. The solution comprises two distinct but complementary components:

1. **Round 1A**: PDF Structure Extraction
2. **Round 1B**: Persona-Driven Content Analysis

## Technical Requirements

### System Constraints
- **Platform**: AMD64 (x86_64) architecture
- **Execution**: CPU-only, no GPU acceleration
- **Network**: Strictly offline operation
- **Resource Limits**:
  - Round 1A: ≤200MB memory, ≤10s per 50-page PDF
  - Round 1B: ≤1GB memory, ≤60s for 5 documents

### Dependencies
- Python 3.8+
- PyMuPDF (fitz)
- scikit-learn
- Unicode normalization libraries

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
```

2. Build the Docker image:
```bash
docker build --platform linux/amd64 -t adobe-hackathon:latest .
```

## Usage

### For Round 1A (Structure Extraction)
Place PDF files in the `./input` directory and run:
```bash
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  adobe-hackathon:latest
```

Output files will be generated in `./output` with matching names (e.g., `document.pdf` → `document.json`).

### For Round 1B (Content Analysis)
Create `challenge1b_input.json` in the `./input` directory with this format:
```json
{
  "documents": [{"filename": "document1.pdf"}],
  "persona": {"role": "Researcher"},
  "job_to_be_done": {"task": "Find relevant studies"}
}
```

Run the same Docker command as above. Results will appear in `./output/challenge1b_output.json`.

## Output Specifications

### Round 1A Output
```json
{
  "title": "Document Title",
  "outline": [
    {"level": "H1", "text": "Main Section", "page": 1},
    {"level": "H2", "text": "Subsection", "page": 2}
  ]
}
```

### Round 1B Output
```json
{
  "metadata": {
    "input_documents": ["document1.pdf"],
    "persona": "Researcher",
    "job_to_be_done": "Find relevant studies",
    "processing_timestamp": "2025-03-15T12:00:00Z"
  },
  "extracted_sections": [
    {
      "document": "document1.pdf",
      "section_title": "Methodology",
      "importance_rank": 1,
      "page_number": 3
    }
  ],
  "subsection_analysis": [
    {
      "document": "document1.pdf",
      "refined_text": "The study employed a...",
      "page_number": 3
    }
  ]
}
```

## Testing

Sample test files are available in the [Public Dataset Folder](https://github.com/jhaaj08/Adobe-India-Hackathon25.git).

To verify correct operation:
1. Place sample PDFs in `./input`
2. Run the Docker container
3. Check `./output` for generated JSON files

## Performance Characteristics

| Metric                 | Round 1A       | Round 1B       |
|------------------------|----------------|----------------|
| Processing Time        | ≤10s per PDF   | ≤60s for 5 PDFs|
| Memory Usage           | ≤200MB         | ≤1GB           |
| Output Latency         | Immediate      | <1s after processing |
| Multilingual Support   | Yes (EN/JP)    | Yes (All languages) |

## Troubleshooting

Common issues and solutions:

1. **No output files**:
   - Verify PDFs are in `./input`
   - Check file permissions on mounted volumes

2. **Incomplete outlines**:
   - Ensure PDFs have properly tagged headings
   - Test with the provided sample PDFs

3. **Performance issues**:
   - Reduce PDF page count if approaching time limits
   - Verify running on AMD64 architecture

## License
This project is developed specifically for the Adobe India Hackathon 2025. All rights reserved by the participating team.
