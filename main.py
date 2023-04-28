import argparse
import json
from convertor import format_data

parser = argparse.ArgumentParser(description='Perform some operation.')
parser.add_argument('items', metavar='items', type=str, help='file containing the items data')
parser.add_argument('groups', metavar='groups', type=str, help='file containing the groups data')
parser.add_argument('-o', '--output', metavar='output', type=str, help='write the result to the specified output file. Defaults to `output.json`')

args = parser.parse_args()

output = args.output or 'output.json'
with open(output, "w", encoding="utf-8") as json_file:
    json.dump(format_data(args.items, args.groups), json_file, ensure_ascii=False)

