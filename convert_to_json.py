import pandas as pd
import json

EXCEL_FILE = "data/Waffestry_Menu_Updated.xlsx"
OUTPUT_JSON = "data/chunks.json"

def convert_waffestry_menu_to_chunks(excel_file, output_file):
    df = pd.read_excel(excel_file)

    # Clean headers by stripping spaces and lowercasing for matching
    df.columns = [col.strip() for col in df.columns]

    print("Detected Columns:", df.columns.tolist())  # DEBUG

    # Map columns using partial keyword matching
    col_map = {}
    for col in df.columns:
        col_lower = col.lower()
        if "name" in col_lower:
            col_map["name"] = col
        elif "description" in col_lower:
            col_map["description"] = col
        elif "classic" in col_lower:
            col_map["classic"] = col
        elif "chocolate" in col_lower and "classic" not in col_lower:
            col_map["chocolate"] = col
        elif "red velvet" in col_lower:
            col_map["redvelvet"] = col

    required_keys = ["name", "description", "classic", "chocolate", "redvelvet"]
    for key in required_keys:
        if key not in col_map:
            raise ValueError(f"Missing expected column for: {key}")

    chunks = []
    for idx, row in df.iterrows():
        name = str(row.get(col_map["name"], "")).strip()
        description = str(row.get(col_map["description"], "")).strip()
        price_classic = str(row.get(col_map["classic"], "")).strip()
        price_chocolate = str(row.get(col_map["chocolate"], "")).strip()
        price_redvelvet = str(row.get(col_map["redvelvet"], "")).strip()

        if not name:
            continue

        chunk_text = (
            f"{name} | {description} | "
            f"Price Classic: ₹{price_classic} | "
            f"Price Chocolate: ₹{price_chocolate} | "
            f"Price Red Velvet: ₹{price_redvelvet}"
        )
        chunks.append({"content": chunk_text})

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)

    print(f"Chunks saved to {output_file} | Total Chunks: {len(chunks)}")

if __name__ == "__main__":
    convert_waffestry_menu_to_chunks(EXCEL_FILE, OUTPUT_JSON)
