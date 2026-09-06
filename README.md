# ALU Data Extraction and Security Validation Assignment

**Student Name:** Sia Virginie Millimouno  
**Track:** Software Engineering

## Project Overview
In this assignment, I created a Python program that reads raw, messy log data from a file (`input/raw-text.txt`), extracts useful structured information using regular expressions (Regex), validates specific ALU email domains, and sanitizes sensitive data before saving the final output into a JSON file (`output/sample-output.json`).

---

## How the Code Works & Regex Explanations

### 1. Data Extraction Rules
- **Emails:** I used `\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b`. The `\b` at the start and end is important because it acts as a word boundary. This prevents the script from capturing unsafe text like HTML tags surrounding an email.
- **Credit Cards:** I used `\b(?:\d{4}[-\s]?){3}\d{4}\b|\b\d{15,16}\b` to handle card numbers written with spaces, dashes, or plain 15/16 digits.
- **URLs:** The pattern `https?://[a-zA-Z0-9.-]+...` checks for standard HTTP and HTTPS links while ignoring broken links (like `htp://`).
- **Phone Numbers:** Captures Rwandan and international formats with optional `+` prefixes and varying spaces or dashes.

### 2. ALU Domain Validation
After extracting all general emails, I filtered them into three categories using domain-specific regex rules:
- Official emails ending in `@alueducation.com`
- Alumni emails ending in `@alumni.alueducation.com`
- Peer tutors / SI emails ending in `@si.alueducation.com`

### 3. Security & Data Protection (Sanitization)
To make sure the output file is safe and complies with basic privacy standards:
- **Credit Cards Masking:** I wrote the `redact_credit_card()` function to remove non-digit characters and replace the first 12 numbers with `****-****-****-`, leaving only the last 4 digits visible.
- **Email Masking:** The `anonymize_email()` function hides part of the username (e.g., `s***t@domain.com`) so personal data isn't exposed in plain text in logs.
- **Rejection of Unsafe Input:** Injection attempts like `<script>alert('xss')</script>` or SQL payloads are automatically ignored because they don't match the boundary conditions of the regex patterns.

---

## How to Run the Project

1. Make sure you are in the project root directory:
   ```bash
   cd alu-regex-data-extraction_SiaVirginie
