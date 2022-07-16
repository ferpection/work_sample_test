import argparse
import logging
import os
import pathlib
import sys

from custom_exceptions import ValidationException
from library import (
    convert_csv_to_json,
    ITEMS_CSV_COLUMNS_HELP_TEXT,
    GROUPS_CSV_COLUMNS_HELP_TEXT,
)


def main():

    parser = argparse.ArgumentParser(
        description="Convert two csv files (items.csv & groups.csv) to structured JSON. Where records in the data file"
        " are linked to the groups through a group_id. The delimiter used is the comma (,) with a pipe (|)"
        " as the quoting character for the CSV files",
    )
    parser.add_argument(
        "items_csv",
        type=str,
        metavar="Items.csv",
        help=f"Path to items csv file. {ITEMS_CSV_COLUMNS_HELP_TEXT}",
    )
    parser.add_argument(
        "groups_csv",
        metavar="Groups.csv",
        type=str,
        help=f"Path to groups csv file. {GROUPS_CSV_COLUMNS_HELP_TEXT}",
    )
    parser.add_argument(
        "-o",
        "--output_json",
        metavar="output.json",
        type=str,
        help="The name of the JSON file to be generated",
        required=True,
    )

    args = parser.parse_args()
    input_items_csv = args.items_csv
    input_groups_csv = args.groups_csv
    output_json = args.output_json

    if not os.path.isfile(input_items_csv):
        raise ValidationException(f"{input_items_csv} path does not exist")

    if not os.path.isfile(input_items_csv):
        raise ValidationException(f"{input_items_csv} path does not exist")
        sys.exit()

    if not (pathlib.Path(input_items_csv).suffix == ".csv"):
        raise ValidationException(
            f"{input_items_csv} must be a valid .CSV file. {ITEMS_CSV_COLUMNS_HELP_TEXT}"
        )

    if not (pathlib.Path(input_groups_csv).suffix == ".csv"):
        raise ValidationException(
            f"{input_groups_csv} must be a valid .CSV. {GROUPS_CSV_COLUMNS_HELP_TEXT}"
        )

    convert_csv_to_json(
        items_csv_file=input_items_csv,
        groups_csv_file=input_groups_csv,
        output_json_file=output_json,
    )


if __name__ == "__main__":
    try:
        main()
        print(f"Conversion completed successfully!")
    except ValidationException as e:
        logging.error(e)
        sys.exit()
    except Exception as e:
        logging.error(e)
        sys.exit()
