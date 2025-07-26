# 📘 approach.md

## 🔍 Challenge Summary
The task is to extract structured content from unstructured PDF documents. Each PDF must be converted into a corresponding JSON file that includes:
- A `title`: representative of the document’s main heading (usually from the top 60% of page 1 or 2)
- An `outline`: a list of section headings, each with a `level`, `text`, and `page`

## 🎯 Goals of Our Solution
1. Extract meaningful and non-generic headings.
2. Normalize heading levels (e.g., cap at H4).
3. Avoid noise like addresses, websites, or metadata ("Contact:", "RSVP:", etc.).
4. Ensure high-quality titles even when they appear in bold clusters or in multiple lines.
5. Work robustly across simple, complex, and large PDFs.

---

## 🧠 Core Approach

### 1. **Text Extraction and Analysis**
We use **PyMuPDF (fitz)** to extract:
- **Text blocks** along with font sizes, position, and structure.
- This gives us fine-grained control over layout and hierarchy.

### 2. **Body Font Size Detection**
We compute the **most common font size** to represent the "body text size".
- Anything with significantly larger font is treated as a potential heading.

```python
body_size = Counter(font_sizes).most_common(1)[0][0]
```

### 3. **Heading Detection**
We assign heading levels (H1–H4) based on relative font size above body font.
- Larger font → H1
- Slightly larger → H2/H3/H4
- Levels > H4 are **promoted upward** to stay within H1–H4 only.

We filter out:
- Duplicated headings across pages.
- Headings that appear below the **60% vertical threshold** of a page.
- Headings that are **too short, too generic**, or contain known metadata labels.

### 4. **Title Extraction**
From the **top 60% of the first two pages**, we:
- Identify the **largest font size block(s)** with meaningful multi-word text.
- Merge adjacent blocks of similar font sizes into one coherent title.

We avoid:
- Pages with only logos
- Bottom-of-page headers/footers
- Generic metadata ("Version 1.0", etc.)

### 5. **Metadata Label Filtering**
We filter out heading blocks where the first word is a **generic label** like:
- `Address:`, `Website:`, `RSVP:`, `Contact:`, `Email:`, `Date:`

This avoids:
- Extracting full addresses or URLs as headings.
- Label-only headings like `Phone:` being marked as H1 incorrectly.

---

## ✅ Strengths of Our Approach

| Feature                          | Supported? |
|----------------------------------|------------|
| Cap heading levels at H4         | ✅          |
| Avoid metadata, address, URL     | ✅          |
| Avoid bottom-of-page titles      | ✅          |
| Title detection from top blocks  | ✅          |
| Works on multi-page PDFs         | ✅          |
| Repeated heading removal         | ✅          |
| Portable & fast                  | ✅          |

---

## 🧪 Testing Strategy

We validated the solution across:

### ✅ Simple PDFs
- Flat layout, few clear H1/H2 headings.
- Expected high title accuracy.

### ✅ Complex PDFs
- Multi-column layout.
- Tables with fake headings were **correctly ignored**.

### ✅ Large PDFs (≥ 50 pages)
- Memory and speed were tested under 10-second constraint.
- Headings and titles extracted consistently.

---

## 🛠 Libraries & Tools

| Tool        | Use Case                           |
|-------------|-------------------------------------|
| `PyMuPDF`   | Text and layout extraction          |
| `re`        | Text cleanup, whitespace filtering  |
| `collections.Counter` | Font size frequency detection |

---

## 📦 Docker & File Structure

- `/app/input` – Read-only directory for input PDFs
- `/app/output` – Output directory for structured JSON
- Code runs inside a container without network or GPU

---

## 🔄 Output JSON Schema

```json
{
  "title": "string",
  "outline": [
    {
      "level": "H1 | H2 | H3 | H4",
      "text": "string",
      "page": number
    }
  ]
}
```



