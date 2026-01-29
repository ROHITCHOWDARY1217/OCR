import cv2
import pytesseract
import re
from rapidfuzz import process, fuzz

from drug_matcher import extract_medicines

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


MEDICINE_DB = [
    "paracetamol",
    "ibuprofen",
    "amoxicillin",
    "azithromycin",
    "cetirizine",
    "metformin",
    "omeprazole",
    "pantoprazole",
    "atorvastatin",
    "dolo",
    "crocin"
]


def extract_text_from_image(image_path):
    img = cv2.imread(image_path)

    # Resize (important)
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Remove noise
    blur = cv2.GaussianBlur(gray, (5,5), 0)

    # Adaptive threshold
    thresh = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    # Morphological closing (connect broken letters)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    text = pytesseract.image_to_string(
        processed,
        config="--psm 6"
    )

    return text




def clean_text(text):
    text = text.lower()

    # remove unwanted symbols
    text = re.sub(r"[^a-z0-9\-\/\s]", " ", text)

    # fix multiple spaces
    text = re.sub(r"[ \t]+", " ", text)


    return text.strip()


def extract_dosages(text):
    patterns = [
        r"\b\d-\d-\d\b",     # 1-0-1
        r"\b\d/\d/\d\b",     # 1/0/1
        r"\b\d+x\d\b",       # 1x2
        r"\bonce daily\b",
        r"\btwice daily\b",
        r"\bbd\b",
        r"\btid\b"
    ]

    found = []
    for p in patterns:
        matches = re.findall(p, text)
        found.extend(matches)

    return list(set(found))



def process_prescription(image_path):
    raw = extract_text_from_image(image_path)
    clean = clean_text(raw)
    dosages = extract_dosages(clean)
    medicines = extract_medicines(clean)




    return {
        "cleaned_text": clean,
        "medicines": medicines,
        "dosages": dosages
    }

