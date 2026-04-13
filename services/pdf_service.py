import fitz
import re
from collections import Counter

def extract_text(filepath):
    pdf = fitz.open(filepath)
    full_text = ""
    for page in pdf:
        full_text += page.get_text()

    pdf.close()
    return full_text

def classify_document(text):
    greek = ["α", "β", "γ", "δ", "θ", "λ", "μ", "π", "σ", "ω", "Σ", "Δ", "Ω"]
    math_symbols = ["∫", "∑", "√", "∞", "∂", "≈", "≠", "≤", "≥"]
    latex = ["\\frac", "\\int", "\\sum", "\\alpha", "\\beta", "\\sqrt"]

    targets = greek + math_symbols + latex

    if any(target in text for target in targets):
        return "math"
    return "text"

def clean_text(text):
    line_list = text.splitlines()
    
    count_line = Counter(line_list)


    
    for i,line in enumerate(line_list):
        num_only = re.match("^\d+$",line.strip())

        if len(line) < 30 or num_only or count_line[line] >=3:
            line_list[i] = ""

    return " ".join(line_list)
    
def chunk_text(text, chunk_size = 3000):
    chunk = []
    lines = text.strip().split()

    for i in range(0, len(lines), chunk_size):
        chunk.append(" ".join(lines[i:i+chunk_size])) #chunks text into 1000 word range

    return chunk

def process_pdf(filepath):
    text = extract_text(filepath)
    doc_type = classify_document(text)
    cleaned_text = clean_text(text)
    chunks = chunk_text(cleaned_text)

    processed_pdf = {
        "cleaned_text" : cleaned_text,
        "chunks" : chunks,
        "doc_type" : doc_type
    }
    return processed_pdf