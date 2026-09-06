# ALU Regex Data Extraction and PII Sanitization

This project automatically extracts, categorizes, and masks sensitive personal data (emails, credit cards, URLs, and phone numbers) from raw text input files.

---

## How It Works

### 1. Data Extraction Rules
* **Emails:** Matches standard email address structures (`user@domain.com`).
* **Credit Cards:** Matches 15 and 16-digit card numbers with or without space/dash delimiters.
* **URLs:** Identifies valid `http://` and `https://` web addresses.
* **Phone Numbers:** Extracts Rwandan (`+250...` / `07...`) and international formats without conflicting with credit card matches.

### 2. ALU Domain Sorting
Extracted emails are grouped into specific categories based on domain suffix:
* **Official:** `@alueducation.com`
* **Alumni:** `@alumni.alueducation.com`
* **Peer Tutors / SI:** `@si.alueducation.com`

### 3. Security & PII Protection
Sensitive fields are masked prior to writing the output JSON file:
* **Credit Cards:** Replaced with asterisks, keeping only the final 4 digits visible (e.g., `************8472`).
* **Emails:** Local username parts are anonymized (e.g., `s*****t@alueducation.com`).

---

## How to Run the Project

1. **Navigate to the project directory:**
   ```bash
   cd alu-regex-data-extraction_SiaVirginie
