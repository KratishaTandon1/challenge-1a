import fitz
import json
import re
from pathlib import Path
from collections import Counter

GENERIC_METADATA_LABELS = [
    "address", "phone", "email", "website", "contact", "date", "fax", "url"
]

def is_metadata_label(text):
    clean_text = text.lower().strip(": ").strip()
    return clean_text in GENERIC_METADATA_LABELS

def get_font_styles(doc):
    font_sizes = []
    for page in doc:
        blocks = page.get_text("dict").get("blocks", [])
        for b in blocks:
            if "lines" in b:
                for l in b["lines"]:
                    for s in l["spans"]:
                        font_sizes.extend([round(s["size"])] * len(s["text"].strip()))
    if not font_sizes:
        return 10, {}
    body_size = Counter(font_sizes).most_common(1)[0][0]
    unique_heading_sizes = sorted(set(s for s in font_sizes if s > body_size), reverse=True)
    size_to_level = {size: f"H{i+1}" for i, size in enumerate(unique_heading_sizes[:4])}
    return body_size, size_to_level

def normalize_levels(outline):
    """Promotes all heading levels to max H4, and promotes H5+ upward."""
    level_order = ["H1", "H2", "H3", "H4"]
    cleaned = []
    seen = set()
    for item in outline:
        if item["text"] in seen:
            continue
        seen.add(item["text"])
        try:
            idx = int(item["level"][1])
            item["level"] = level_order[min(idx - 1, 3)]  
            cleaned.append(item)
        except:
            continue
    all_levels = {entry['level'] for entry in cleaned}
    if "H1" not in all_levels and cleaned:
        min_level_idx = min(level_order.index(e['level']) for e in cleaned)
        for entry in cleaned:
            idx = level_order.index(entry["level"])
            new_idx = max(0, idx - min_level_idx)
            entry["level"] = level_order[new_idx]
    return cleaned

def extract_title(doc, body_size):
    candidate_lines = []
    used_blocks = set()
    for i in range(min(2, len(doc))):
        page = doc[i]
        blocks = page.get_text("dict").get("blocks", [])
        page_height = page.rect.height
        for block_idx, b in enumerate(blocks):
            if "lines" not in b or b["bbox"][1] > page_height * 0.6:
                continue
            spans = [s for l in b["lines"] for s in l["spans"]]
            if not spans:
                continue
            max_size = round(max(s["size"] for s in spans))
            text = " ".join(s["text"].strip() for s in spans)
            text = re.sub(r'\s+', ' ', text).strip()
            words = text.split()
            if not text or len(set(words)) < len(words) // 2:
                continue
            candidate_lines.append((max_size, b["bbox"][1], text, (i, block_idx)))
    if not candidate_lines:
        return "", set()
    candidate_lines.sort(key=lambda x: (-x[0], x[1]))
    top_size = candidate_lines[0][0]
    title_lines = []
    block_ids = set()
    for size, _, text, bid in candidate_lines:
        if abs(size - top_size) <= 1:
            title_lines.append(text)
            block_ids.add(bid)
        else:
            break
    return " ".join(title_lines).strip(), block_ids

def extract_content(pdf_path):
    doc = fitz.open(pdf_path)
    if not doc:
        return {"title": "", "outline": []}
    body_size, size_to_level = get_font_styles(doc)
    title, title_blocks = extract_title(doc, body_size)
    headings = []
    seen_texts = set()
    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict").get("blocks", [])
        for block_idx, b in enumerate(blocks):
            if (page_num, block_idx) in title_blocks or "lines" not in b:
                continue
            spans = [s for l in b["lines"] for s in l["spans"]]
            if not spans:
                continue
            max_size = round(max(s["size"] for s in spans))
            text = " ".join(s["text"].strip() for s in spans)
            text = re.sub(r'\s+', ' ', text).strip()
            words = text.split()
            if (
                not text
                or text in seen_texts
                or is_metadata_label(text.split()[0] if text else "")
                or len(set(words)) < len(words) // 2
                or sum(len(w) for w in words) / len(words) < 3
            ):
                continue
            if max_size > body_size:
                seen_texts.add(text)
                level = size_to_level.get(max_size, "H4")
                headings.append({"level": level, "text": text, "page": page_num})
    doc.close()
    return {"title": title, "outline": normalize_levels(headings)}

def process_all_pdfs():
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    if not input_dir.exists():
        print(f"❌ Input directory '{input_dir}' not found.")
        return
    output_dir.mkdir(exist_ok=True)
    pdf_files = list(input_dir.glob("*.pdf"))
    if not pdf_files:
        print("📂 No PDF files found.")
        return
    print(f"📄 Scanning PDFs in '{input_dir}'...")
    for pdf_file in pdf_files:
        print(f"🔍 Processing '{pdf_file.name}'...")
        try:
            result = extract_content(pdf_file)
            output_file = output_dir / f"{pdf_file.stem}.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=4, ensure_ascii=False)
            print(f"✅ Created: {output_file.name}")
        except Exception as e:
            print(f"❌ Error processing {pdf_file.name}: {e}")
    print("\n✅ All processing complete.")

if __name__ == "__main__":
    process_all_pdfs()
