# ALU Regex Data Extraction & Secure Validation

This is a Python project I built for an assignment at African Leadership University. It uses regular expressions to parse messy text, extract structured information (like emails, phone numbers, and credit cards), and mask sensitive PII data before saving it.

## Folder structure

alu-regex-data-extraction_SiaVirginie/
├── input/
│   └── raw-text.txt        # sample text to test the program on
├── src/
│   └── main.py              # extraction and validation logic
├── output/
│   └── sample-output.json   # generated report
└── README.md

## How to run it

No external libraries are required. It runs on standard Python 3.8+.

cd alu-regex-data-extraction_SiaVirginie
python3 src/main.py

The script reads input/raw-text.txt, runs the extraction logic, prints a quick summary in the terminal, and exports the final JSON to output/sample-output.json.

## What it extracts

- Emails: Validates address formats and groups them into ALU categories (alu_official, alu_alumni, alu_si).
- Credit cards: Matches card patterns and verifies them with a Luhn checksum. Invalid numbers are separated into a rejected list.
- URLs: Catches both http/https links and basic www links.
- Phone numbers: Extracts Rwandan local and international formats (+250 / 07).
- Times: Handles both 24-hour (14:45) and 12-hour (2:30 PM) formats.
- Hashtags: Finds standard hashtags while ignoring empty symbols like ##.

## How the logic works

- Email filtering: Rejects bad formats like missing @ or double dots (domain..com).
- Card verification: Checking the digit pattern isn't enough, so I added a Luhn algorithm check to confirm if card numbers are mathematically valid.
- Phone matching: Avoids confusing credit card digit groups with phone numbers.
- Time constraints: Bounded range rules ensure values like 23:61 get ignored.

## Security & Privacy

- Basic attack detection: Flags lines containing common attack payloads (like <script> tags or SQL comments) before processing.
- Data masking: Masks email user parts and credit card numbers (e.g. s*****e@alueducation.com and ************4242) so sensitive details are never saved in plain text.

## Test data

The file input/raw-text.txt contains realistic support ticket samples with mixed email formats, valid and invalid credit cards, phone numbers, and a few edge cases to test how the script handles bad inputs.

