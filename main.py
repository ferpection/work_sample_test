import argparse
import csv
import json

# Create command line arguments parser
def parse():
    parser = argparse.ArgumentParser(
        prog='csv2json',
        description='Transform CSV files to structured JSON.',
        epilog='Enjoy the program! :)'
    )
    parser.add_argument('items', type=str, help='Path to items CSV file')
    parser.add_argument('groups', type=str, help='Path to groups CSV file')
    parser.add_argument('-o', '--output', type=str, help='Path to output JSON file')
    return parser.parse_args()

# Load CSV file
def load_csv_file(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
        return [row for row in reader]

# Transform CSV data to a structured hash
def transform_to_hash(items, groups):
    data = {}
    for item in items:
        item_uuid = item['uuid']
        data[f"{item_uuid}_title"] = {
            "string": item['title']
        }
        for group in groups:
            if group['uuid'] == item['group_id']:
                data[f"{item_uuid}_description"] = {
                    "string": item['description'],
                    "context": group['group']
                }
                break
    return data

# Save the structured hash to JSON file
def save_to_json(data, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)

# Main function to run the program
def main():
    args = parse()
    items = load_csv_file(args.items)
    groups = load_csv_file(args.groups)
    data = transform_to_hash(items, groups)
    save_to_json(data, args.output)

if __name__ == '__main__':
    main()
