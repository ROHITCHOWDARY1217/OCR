import fitz   # PyMuPDF
import re
from rapidfuzz import process
import re

def load_drug_list_from_pdf(pdf_path):
    drug_set = set()

    doc = fitz.open(pdf_path)

    for page in doc:
        text = page.get_text()
        lines = text.split("\n")

        for line in lines:
            word = line.strip().lower()
            if len(word) > 2:
                drug_set.add(word)

    return drug_set


# Load once when file runs
DRUG_DB = load_drug_list_from_pdf("drug_list.pdf")




def extract_medicines(text):
    medicines = []

    lines = text.split("\n")

    for line in lines:
        line_lower = line.lower()

        # Look only at lines that contain medicine keywords
        if any(k in line_lower for k in ["tab", "cap", "syp", "syrup", "inj"]):

            # Extract possible medicine word AFTER keyword
            match_name = re.search(
                r"(tab|cap|syp|syrup|inj)\s+([a-zA-Z]{3,})",
                line_lower
            )

            if match_name:
                raw_med = match_name.group(2)

                # Fuzzy match only this word
                match, score, _ = process.extractOne(raw_med, DRUG_DB)

                if score > 85:
                    dose_match = re.search(
                        r"\d+\s?mg|\d+\s?ml|\d+\s?tab|\d+\s?tabs?",
                        line_lower
                    )

                    dosage = dose_match.group() if dose_match else "Not specified"

                    medicines.append({
                        "name": match.capitalize(),
                        "dosage": dosage
                    })

                else:
                    # fallback → keep OCR word itself
                    medicines.append({
                        "name": raw_med.capitalize(),
                        "dosage": "Not specified"
                    })

    return medicines


