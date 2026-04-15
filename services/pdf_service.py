import fitz
import re
from collections import Counter
from utils.text_cleaner import clean_text
from utils.chunker import chunk_text

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