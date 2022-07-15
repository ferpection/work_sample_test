import sys
import pandas as pd
import argparse

import util

argparser = argparse.ArgumentParser(
    description="""CSV to Structured JSON Parser:
                    Program that converts csv files of a specific format to a Structured JSON format""")
argparser.add_argument(
    "items_file", help="""Path to CSV file that contains the items in the format:
                        |uuid|,|title|,|description|,|group_id| 
                        |<uuid>|,|<title>|,|<description>|,|<group uuid>|...""",
                        type=argparse.FileType('r', encoding='UTF-8'))
argparser.add_argument(
    "groups_file", help="""Path to CSV file that contains the groups in the format:
                        |uuid|,|group| 
                        |<uuid>|,|<group_text>|...""", type=argparse.FileType('r', encoding='UTF-8'))
argparser.add_argument(
    "-o", help="""Path to output file,
                    if you don't specify a value then the output would be written to 
                    'output.json' in the same directory""", default='output.json',
                     type=argparse.FileType('w', encoding='UTF-8'))

args = argparser.parse_args()

items = pd.read_csv(args.items_file)
groups = pd.read_csv(args.groups_file)

if util.is_valid_frame(items, {'|uuid|','|title|','|description|','|group_id|'}) is False:
    print("""The CSV file for items is invalid please, pass a csv file with the headers:
    |uuid|,|title|,|description|,|group_id| """)
    sys.exit()

if util.is_valid_frame(groups, {'|uuid|','|group|'}) is False:
    print("""The CSV file for items is invalid please, pass a csv file with the headers:
          |uuid|,|group| """)
    sys.exit()

structured_items = util.convert(items, groups)

util.write_json(structured_items, args.o)

print("Conversion seems to have happened successfully and result is saved at : "+str(args.o.name))
