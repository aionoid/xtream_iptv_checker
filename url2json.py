import json


def convert_text_to_json(text_data):
    result = []
    current_entry = {}

    for line in text_data.split("\n"):
        line = line.strip()
        if not line:
            continue

        if "🌐" in line:
            # If we have a previous entry, add it to results
            if current_entry:
                result.append(current_entry)
                current_entry = {}

            url = line.split("🌐")[-1].strip()
            current_entry[url] = {}
        elif "👤" in line and "🔐" in line:
            if not current_entry:
                continue  # Skip if no URL defined yet

            parts = line.split("👤")[-1].split("🔐")
            username = parts[0].strip()
            password = parts[1].strip()

            # Get the last URL we were processing
            url = list(current_entry.keys())[-1]
            current_entry[url][username] = password

    # Add the last entry if exists
    if current_entry:
        result.append(current_entry)

    return result


# Read input from file
with open("raw.txt", "r", encoding="utf-8") as f:
    input_text = f.read()

# Convert the text to JSON structure
json_data = convert_text_to_json(input_text)

# Write output to file
with open("sites.json", "w", encoding="utf-8") as f:
    json.dump(json_data, f, indent=2, ensure_ascii=False)

print("Conversion complete! Results saved to sites.json")
