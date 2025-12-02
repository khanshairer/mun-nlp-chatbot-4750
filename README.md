# MUN NLP Faculty Chatbot  
COMP 4750 – Natural Language Processing (Fall 2025)  
Memorial University of Newfoundland  

A classical NLP chatbot that answers questions about MUN faculty.  
It uses regex-based intent detection, natural-language name extraction, and an SQLite database imported from your faculty Excel dataset.

---

## ✨ Features

- Faculty lookup by:
  - Email  
  - Office / Room  
  - Phone number  
  - Position / Title  
  - Faculty / Department  
  - Full summary of all details  
- Smart name extraction:
  - “What is Dr. Todd Wareham’s email?”
  - “Where is Professor Jane Smith’s office?”
  - “Tell me about Pranjal”
  - “info about pranjal patra”
  - “who’s room is EN-2008?”
- Robust matching:
  - Handles “Wareham, Todd” vs “Todd Wareham”
  - Case-insensitive
  - Handles `'s`, “about”, “info”, “for”, “of”
- Flask web interface with chat UI
- Excel → SQLite importer script

---

## 📸 Screenshots & Media

### Logo
(Place `logo.png` here)

### Demo GIF
(Place `demo.gif` here)

---

## 🚀 Installation

```bash
pip install -r requirements.txt
Import faculty dataset:
python import_faculty_from_excel.py
Run chatbot:
python app.py
Then open:
http://127.0.0.1:5000

## 📁 Project Structure
mun-nlp-chatbot-4750/
│
├── app.py
├── db.py
├── import_faculty_from_excel.py
├── data/
│   └── all_faculty_full_combined.xlsx
├── nlp/
│    ├── intent.py
│    ├── engine.py
│    ├── fsa.py
│    ├── morph.py
│    └── tokenizer.py
├── static/
│    ├── style.css
│    └── app.js
├── templates/
│    └── index.html
│
├── README.md
└── LICENSE

## 🧑‍💻 Example Queries
“What is Dr. Todd Wareham’s email?”
“Where is Wareham’s office?”
“Tell me about Pranjal Patra”
“Who’s room is EN-2008?”
“What is Hatcher’s phone number?”
“Which faculty is Professor X in?”

## 📜 License
Released under the MIT License (see LICENSE file).

## 👨‍🏫 Instructor
Dr. Todd Wareham

## 👥 Authors
Sharier Khan
Md Mamun Rashid
