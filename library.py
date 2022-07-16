import csv
import json

from custom_exceptions import ValidationException

ITEMS_CSV_COLUMNS_HELP_TEXT = (
    "Filename at position 1 must be a valid .csv file and should have the following "
    "columns (|uuid|,|title|,|description|,|group_id|). "
    "Run python main.py -h  for usage instructions"
)
GROUPS_CSV_COLUMNS_HELP_TEXT = (
    "Filename at position 2 must be a valid .CSV file and should have the following "
    "columns (|uuid|, |group|). Run python main.py -h  for usage instructions "
)


def lookup_group_id_in_csv_file(groups_csv_file, group_id):
    with open(groups_csv_file, "r") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",", quotechar="|")
        for row in reader:
            try:
                if row["uuid"] == group_id:
                    return row["group"]
            except KeyError:
                raise ValidationException(f"Bad Input: {GROUPS_CSV_COLUMNS_HELP_TEXT}")
        return None


def convert_csv_to_json(items_csv_file, groups_csv_file, output_json_file):
    data = {}
    with open(items_csv_file, encoding="utf-8") as input_file:
        try:
            csv_reader = csv.DictReader(input_file, delimiter=",", quotechar="|")
            for row in csv_reader:
                row_uuid = row["uuid"]
                data[f"{row_uuid}_title"] = {"string": row["title"]}
                data[f"{row_uuid}_description"] = {
                    "string": row["description"],
                    "context": lookup_group_id_in_csv_file(
                        groups_csv_file, row["group_id"]
                    ),
                }
        except KeyError:
            raise ValidationException(f"Bad Input: {ITEMS_CSV_COLUMNS_HELP_TEXT}")

    # Write data to Output JSON
    with open(output_json_file, "w", encoding="utf-8") as json_file:
        json_file.write(json.dumps(data, indent=4))
