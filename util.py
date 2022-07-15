import pandas as pd
import json

def is_valid_frame(dataFrame, expected_columns):
    return dataFrame.empty is False and expected_columns.issubset(dataFrame.columns)
        
def read_csv(file_path):
    return pd.read_csv(file_path, sep=',')

def clr(text):
    return text.replace('|', '')

def write_json(data, output_file):
    json.dump(data, output_file, ensure_ascii=False, indent=4, default=str)

def convert(items, groups):
    # prevent weird 'auto-names' that pandas uses to resolve name clashes when we join the two datasets
    groups.rename({'|uuid|': 'group_uuid'}, axis='columns', inplace=True)

    # get the two related datasets into one like a regular SQL join for RDBMSes
    full_set = pd.merge(items, groups, how='inner',
                        left_on='|group_id|', right_on='group_uuid')

    structured_items = {}

    for row in zip(full_set['|uuid|'],
                   full_set['|title|'],
                   full_set['|description|'],
                   full_set['|group|']):

        structured_items.update({
            clr(row[0])+'_title': {"string":  clr(row[1])},
            clr(row[0])+'_description': {"string": clr(row[2]), "context": clr(row[3])}
        })

    return structured_items
