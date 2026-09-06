import json
import os
import re

# Relative paths from project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_PATH = os.path.join(BASE_DIR, "input", "raw-text.txt")
OUTPUT_PATH = os.path.join(BASE_DIR, "output", "sample-output.json")

# -------------------------------------------------------------------
# REGEX PATTERNS & VALIDATION RULES
# -------------------------------------------------------------------
# Strict Email Regex (prevents consecutive dots like 'invalid..email')
EMAIL_REGEX = r"\b[a-zA-Z0-9_%+-]+(?:\.[a-zA-Z0-9_%+-]+)*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"

# ALU Domain Specific Sub-patterns
ALU_OFFICIAL_REGEX = r"@alueducation\.com$"
ALU_ALUMNI_REGEX = r"@alumni\.alueducation\.com$"
ALU_SI_REGEX = r"@si\.alueducation\.com$"

# Credit Cards (15-16 digits formatted with spaces, dashes, or plain)
CREDIT_CARD_REGEX = r"\b(?:\d{4}[-\s]?){3}\d{4}\b|\b\d{15,16}\b"

# Strict Phone Regex (Rwandan +250/07 numbers)
PHONE_REGEX = r"(?:\+250\s?7\d{2}\s?\d{3}\s?\d{3}\b)|(?:\b07\d{8}\b)"

# Valid URLs (HTTP/HTTPS)
URL_REGEX = r"https?://[a-zA-Z0-9.-]+(?::\d+)?(?:/[^\s]*)?"

def mask_email(email):
    """Masks email local part: user@domain.com -> u***r@domain.com"""
    parts = email.split("@")
    local, domain = parts[0], parts[1]
    if len(local) <= 2:
        masked_local = local[0] + "*" * (len(local) - 1)
    else:
        masked_local = local[0] + "*" * (len(local) - 2) + local[-1]
    return f"{masked_local}@{domain}"

def mask_credit_card(card):
    """Masks credit card numbers: keeps only the last 4 digits visible"""
    digits = re.sub(r"\D", "", card)
    if len(digits) >= 4:
        return "*" * (len(digits) - 4) + digits[-4:]
    return "****"

def main():
    if not os.path.exists(INPUT_PATH):
        print(f"Error: Input file not found at {INPUT_PATH}")
        return

    with open(INPUT_PATH, "r", encoding="utf-8") as file:
        raw_text = file.read()

    # Extract raw matches using regex
    all_emails = re.findall(EMAIL_REGEX, raw_text)
    credit_cards = re.findall(CREDIT_CARD_REGEX, raw_text)
    phones = re.findall(PHONE_REGEX, raw_text)
    urls = re.findall(URL_REGEX, raw_text)

    # Filter and mask ALU subcategory emails
    official_alu = [mask_email(e) for e in all_emails if re.search(ALU_OFFICIAL_REGEX, e)]
    alumni_alu = [mask_email(e) for e in all_emails if re.search(ALU_ALUMNI_REGEX, e)]
    si_alu = [mask_email(e) for e in all_emails if re.search(ALU_SI_REGEX, e)]

    # Mask general PII fields
    masked_emails = [mask_email(e) for e in all_emails]
    masked_cards = [mask_credit_card(c) for c in credit_cards]

    # Build final output object
    output_data = {
        "metadata": {
            "total_emails_found": len(all_emails),
            "total_credit_cards_found": len(credit_cards),
            "total_phones_found": len(phones),
            "total_urls_found": len(urls),
        },
        "extracted_data": {
            "masked_emails": masked_emails,
            "alu_official_emails": official_alu,
            "alu_alumni_emails": alumni_alu,
            "alu_si_emails": si_alu,
            "masked_credit_cards": masked_cards,
            "urls": urls,
            "phones": phones,
        },
        "security_notice": "All PII fields (emails and payment cards) have been masked across all categories.",
    }

    # Write processed data to output JSON
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as out_file:
        json.dump(output_data, out_file, indent=4)

    print(f"Extraction successfully completed. Results saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
