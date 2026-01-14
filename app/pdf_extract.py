import pdfplumber
import re
import pandas as pd

def extract_provider_report(pdf_path: str) -> dict:
    with pdfplumber.open(pdf_path) as pdf:
        full_text = "\n".join(
            page.extract_text() or "" for page in pdf.pages
        )

    # --- Provider name ---
    name_match = re.search(r"Provider name\s*:\s*(.+)", full_text)
    provider_name = name_match.group(1).strip() if name_match else None

    # --- Provider number ---
    number_match = re.search(r"Provider number\s*:\s*(\d+)", full_text)
    provider_number = number_match.group(1) if number_match else None

    # --- Quarterly expenses ---
    quarterly_data = []
    quarter_pattern = re.compile(r"(Q[1-4])\s+(\d+)\s+(\d+)\s+(\d+)")

    for match in quarter_pattern.finditer(full_text):
        quarterly_data.append({
            "quarter": match.group(1),
            "Ambulatory": int(match.group(2)),
            "Hospital": int(match.group(3)),
            "Other/NA": int(match.group(4)),
        })

    df_quarters = pd.DataFrame(quarterly_data)

    return {
        "provider_name": provider_name,
        "provider_number": provider_number,
        "provider_expenses_by_quarter": df_quarters.to_dict(orient="records")
    }
