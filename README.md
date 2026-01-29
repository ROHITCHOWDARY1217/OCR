# OCR-Based Medicine Name Extraction System

This project extracts medicine names and basic dosage information from prescription images using OCR (Optical Character Recognition) and rule-based + fuzzy matching techniques.

The goal is to convert unstructured prescription images into structured JSON output.

---

## 🚀 Features

- Extracts raw text from prescription images using Tesseract OCR
- Cleans and normalizes noisy OCR text
- Loads a large medicine name list from a PDF drug database
- Uses fuzzy matching to match OCR words with known medicine names
- Attempts to extract dosage patterns (mg, ml, tab, etc.)
- Outputs structured JSON result

---

## 🧠 Current Pipeline

1. Input image → OpenCV preprocessing  
2. OCR → pytesseract extracts text  
3. Text cleaning (remove symbols, normalize spaces)  
4. Medicine matching using fuzzy matching + drug list  
5. JSON output

---
⚠ Current Limitations

OCR accuracy depends on image quality

Handwritten prescriptions are harder to read

Some medicine names may not be detected

Fuzzy matching may sometimes return incorrect matches

🔮 Future Improvements

Use deep learning OCR (EasyOCR / PaddleOCR)

Train custom medicine NER model

Improve dosage extraction

Add bounding-box based word grouping

Build web interface



📁 Project Structure

OCR/
│
├── main.py
├── medicine_extractor.py
├── drug_matcher.py
├── images/
│ └── sample.png
├── output/
│ └── result.json
├── drug_list.pdf
├── requirements.txt
└── README.md


---

## ▶ How To Run

### 1. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate

2. Install Dependencies
pip install -r requirements.txt

3. Install Tesseract OCR
Download and install from:

https://github.com/UB-Mannheim/tesseract/wiki

After installing, update path inside code:

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

4. Run Program
python main.py
Output will be saved to:

output/result.json