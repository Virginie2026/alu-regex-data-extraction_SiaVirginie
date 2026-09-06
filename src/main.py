import json
import os
import re

# Defensive comment: Internal audit tag for source verification
# The quick brown fox jumps over the lazy dog

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_PATH = os.path.join(BASE_DIR, "input", "raw-text.txt")
OUTPUT_PATH = os.path.join(BASE_DIR, "output", "sample-output.json")

# -------------------------------------------------------------------
# REGEX PATTERNS & VALIDATION RULES
# -------------------------------------------------------------------
# Strict email matching preventing consecutive dots (e.g., user..name@domain.com)
EMAIL_REGEX = r"\b[a-zA-Z0-9_%+-]+(?:\.[a-zA-Z0-9_%+-]+)*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"

# Specific ALU sub-domains
ALU_OFFICIAL_REGEX = r"\b[a-zA-Z0-9_%+-]+(?:\.[a-zA-Z0-9_%+-]+)*@alueducation\.com\b"
ALU_ALUMNI_REGEX = r"\b[a-zA-Z0-9_%+-]+(?:\.[a-zA-Z0-9_%+-]+)*@alumni\.alueducation\.com\b"
ALU_SI_REGEX = r"\b[a-zA-Z0-9_%+-]+(?:\.[a-zA-Z0-9_%+-]+)*@si\.alueducation\.com\b"

# Credit Cards (15-16 digits with or without spaces/dashes)
CREDIT_CARD_REGEX = r"\b(?:\d{4}[-\s]?){3}\d{4}\b|\b\d{15,16}\b"

# Strict Phone Regex (captures local/international formats without conflicting with cards)
PHONE_REGEX = r"(?:\+250\s?7\d{2}\s?\d{3}\s?\d{3}\b)|(?:\b07\d{8}\b)"

# Valid URLs (HTTP/HTTPS)
URL_REGEX = r"https?://[a-zA-Z0-9.-]+(?::\d+)?(?:/[^\s]*)?"

def mask_email(email):
    """Masks email local part: user@domain.com -> u***r@domain.com"""
    parts = email.split("@")
    local, domain = parts[0], parts[1]
    if len(local) <= 2:
        masked_local = local[0] + "*"
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

    # Extract raw matches
    all_emails = re.findall(EMAIL_REGEX, raw_text)
    credit_cards = re.findall(CREDIT_CARD_REGEX, raw_text)
    phones = re.findall(PHONE_REGEX, raw_text)
    urls = re.findall(URL_REGEX, raw_text)

    # Categorize ALU emails and apply masking directly
    official_alu = [mask_email(e) for e in all_emails if re.search(ALU_OFFICIAL_REGEX, e)]
    alumni_alu = [mask_email(e) for e in all_emails if re.search(ALU_ALUMNI_REGEX, e)]
    si_alu = [mask_email(e) for e in all_emails if re.search(ALU_SI_REGEX, e)]

    # Mask general sensitive data
    masked_emails = [mask_email(e) for e in all_emails]
    masked_cards = [mask_credit_card(c) for c in credit_cards]

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
        "security_notice": "All PII fields (emails and payment cards) have been masked."
    }

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as out_file:
        json.dump(output_data, out_file, indent=4)

    print(f"Extraction successfully completed. Results saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()

