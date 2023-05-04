import argparse
import csv
import json

def read_csv(path):
    data = {}
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            # Use uuid as key
            data[row['uuid']] = row
    return data

def generate_json(items, groups, output):
    result = {}
    for item_uuid, item in items.items():
        # Retrieving the group name
        group_name = groups[item['group_id']]['group']
        
        # Generating a title entry
        title_key = f"{item_uuid}_title"
        result[title_key] = {"string": item['title']}
        
        # Generating a description entry
        description_key = f"{item_uuid}_description"
        result[description_key] = {"string": item['description'], "context": group_name}
    
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

def main():
    parser = argparse.ArgumentParser(description='Convert two CSV files to a structured JSON file.')
    parser.add_argument('items_csv', help='Path to the items.csv file.')
    parser.add_argument('groups_csv', help='Path to the groups.csv file.')
    parser.add_argument('-o', '--output', dest='output', help='Path to the output structured JSON file.')

    args = parser.parse_args()

    items = read_csv(args.items_csv)
    groups = read_csv(args.groups_csv)
    generate_json(items, groups, args.output)

if __name__ == '__main__':
    main()