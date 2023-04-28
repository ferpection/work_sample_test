import csv

def read_csv_file (filename):
    with open(filename, newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        labels = [label.strip("|") for label in next(reader)]
        data = [
            {
                label: value.strip("|")
                for label, value in zip(labels, row)
            }
            for row in reader
        ]

    return data

def format_data(*files):
    items, groups = [read_csv_file(filename) for filename in list(files)] 

    result = []
    groups_dict = {group['uuid']: group['group'] for group in groups}
    
    for item in items:
        item_uuid = item['uuid']
        item_group = groups_dict.get(item['group_id'])
        
        result.append({
            f"{item_uuid}_title": {"string": item["title"]},
            f"{item_uuid}_description": {
                "string": item["description"],
                "context": item_group,
            },
        })

    return result
