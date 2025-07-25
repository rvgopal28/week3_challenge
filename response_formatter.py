# response_formatter.py

import re

def format_adaptive_response(raw_response):
    """
    Curates the raw Adaptive RAG response into a clean, user-friendly format.
    Special handling for Waffle & Beverage descriptions with prices.
    """

    lines = raw_response.strip().split("\n")
    formatted_sections = []
    current_section = ""

    # Pattern matchers
    price_pattern = re.compile(r"(?:₹|Rs\.?)\s?\d+")
    item_header_keywords = ["waffle", "coffee", "offer", "combo", "promotion"]

    for line in lines:
        line_clean = line.strip()

        # Identify item headers (e.g., KitKat Waffle)
        if any(kw in line_clean.lower() for kw in item_header_keywords) and not price_pattern.search(line_clean):
            if current_section:
                formatted_sections.append(current_section.strip())
                current_section = ""
            current_section += f"### 🍽️ {line_clean}\n"

        # Identify flavor/price lines
        elif price_pattern.search(line_clean):
            prices = price_pattern.findall(line_clean)
            flavors = re.findall(r"Classic|Chocolate|Red Velvet|Original|Combo|Meal", line_clean, re.IGNORECASE)
            if flavors:
                flavor_price_lines = "\n".join([f"• {flavor} – {price}" for flavor, price in zip(flavors, prices)])
                current_section += f"{flavor_price_lines}\n"
            else:
                current_section += f"• Price: {prices[0]}\n"

        else:
            # Regular description lines
            current_section += f"{line_clean}\n"

    # Append last section if exists
    if current_section:
        formatted_sections.append(current_section.strip())

    # Join with line breaks
    final_output = "\n\n".join(formatted_sections)
    return final_output

# Example usage:
if __name__ == "__main__":
    raw = '''A KitKat Waffle is a delicious dessert topped with real KitKat chunks and drizzled with chocolate sauce, creating a perfect mix of crispiness and creaminess. It comes in three flavors: Classic priced at ₹176, Chocolate priced at ₹190, and Red Velvet also priced at ₹190.

On the other hand, a KitKat Coffee is a refreshing drink made by blending crunchy KitKat into chilled coffee, giving it a cool and chocolatey flavor that is simply irresistible. It is priced at ₹146.'''
    print(format_adaptive_response(raw))
