FROM python:3.10-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir pymupdf

# Copy your code
COPY process_pdfs.py .

# Run automatically on container start
CMD ["python", "process_pdfs.py"]
