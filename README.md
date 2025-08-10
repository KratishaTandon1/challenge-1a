# Challenge 1a: PDF Processing Solution

## Overview
This is a **solution** for Challenge 1a of the Adobe India Hackathon 2025. The challenge requires implementing a PDF processing solution that extracts structured data from PDF documents and outputs JSON files. The solution is containerized using Docker and meets specific performance and resource constraints.

### Build Command
```bash
docker build --platform linux/amd64 -t <mysolutionname.someidentifier> .
```

### Run Command
```bash
docker run --rm `
  -v ${PWD}/input:/app/input `
  -v ${PWD}/output:/app/output `
  --network none `
  mysolutionname:somerandomidentifier
```

### Critical Constraints
- **Execution Time**: ≤ 10 seconds for a 50-page PDF
- **Model Size**: ≤ 200MB (if using ML models)
- **Network**: No internet access allowed during runtime execution
- **Runtime**: Must run on CPU (amd64) with 8 CPUs and 16 GB RAM
- **Architecture**: Must work on AMD64, not ARM-specific

### Satisfying Key Requirements
- **Automatic Processing**: Process all PDFs from `/app/input` directory
- **Output Format**: Generate `filename.json` for each `filename.pdf`
- **Input Directory**: Read-only access only
- **Open Source**: All libraries, models, and tools are open source
- **Cross-Platform**: Tested on both simple and complex PDFs

## Solution Structure
```
Challenge_1a/
├── sample_dataset/
│   ├── outputs/         # JSON files provided as outputs.
│   ├── pdfs/            # Input PDF files
│   └── schema/          # Output schema definition
│       └── output_schema.json
├── Dockerfile           # Docker container configuration
├── process_pdfs.py      # Sample processing script
└── README.md           # This file
```

## Implementation

### Current Solution
The provided `process_pdfs.py` is a **solution** that performs:
- PDF file scanning from input directory
- JSON data generation
- Output file creation in the specified format


### Performance Considerations
- **Memory Management**: Efficient handling of large PDFs
- **Processing Speed**: Optimize for sub-10-second execution
- **Resource Usage**: Stay within 16GB RAM constraint
- **CPU Utilization**: Efficient use of 8 CPU cores

### Validation Checklist
- [✓] All PDFs in input directory are processed
- [✓] JSON output files are generated for each PDF
- [✓] Output format matches required structure
- [✓] **Output conforms to schema** in `sample_dataset/schema/output_schema.json`
- [✓] Processing completes within 10 seconds for 50-page PDFs
- [✓] Solution works without internet access
- [✓] Memory usage stays within 16GB limit
- [✓] Compatible with AMD64 architecture

---
