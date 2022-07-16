import csv
import json
import os
import subprocess
import unittest
from tempfile import NamedTemporaryFile

from library import ITEMS_CSV_COLUMNS_HELP_TEXT


class TestCsvToJsonConversion(unittest.TestCase):
    def setUp(self):
        super().setUp()

        # ###############################
        # Create some temporary test files
        # ###############################

        # Generate a good input file with all columns
        with NamedTemporaryFile(
            "w", encoding="UTF8", newline="", suffix=".csv", delete=False
        ) as fp:
            self.good_input_items_file = fp
            header = ["|uuid|", "|title|", "|description|", "|group_id|"]
            data = [
                "|f19c962e-eec0-455f-baa9-c0ba6986d01b|",
                "|autem deserunt quo quaerat deleniti|",
                "|aut soluta repudiandae numquam accusantium pariatur culpa fugiat ducimus laudantium consequatur quam "
                "rerum dolorem beatae cum eius magni in architecto nihil similique odit été distinctio eligendi alias "
                "optio asperiores incidunt unde quaerat dolor a animi sapiente vel saepe ad iusto doloribus libero "
                "voluptates voluptate explicabo velit officiis praesentium accusamus possimus|",
                "|cbfd812d-7b13-4b1c-8193-82a521ce6fb6|",
            ]
            input_items_csv_writer = csv.writer(self.good_input_items_file)
            input_items_csv_writer.writerow(header)
            input_items_csv_writer.writerow(data)

        # Generate expected good json output file
        with NamedTemporaryFile(suffix=".json", delete=False) as fp:
            self.good_output_json = fp

        self.expected_json = {
            "f19c962e-eec0-455f-baa9-c0ba6986d01b_title": {
                "string": "autem deserunt quo quaerat deleniti"
            },
            "f19c962e-eec0-455f-baa9-c0ba6986d01b_description": {
                "string": "aut soluta repudiandae numquam accusantium pariatur culpa fugiat ducimus laudantium "
                "consequatur quam rerum dolorem beatae cum eius magni in architecto nihil similique odit "
                "été distinctio eligendi alias optio asperiores incidunt unde quaerat dolor a animi "
                "sapiente vel saepe ad iusto doloribus libero voluptates voluptate explicabo velit officiis "
                "praesentium accusamus possimus",
                "context": "nesciunt quidem iure",
            },
        }

        # Generate a bad input file with missing column group_id
        with NamedTemporaryFile(
            "w", encoding="UTF8", newline="", suffix=".csv", delete=False
        ) as fp:
            self.bad_input_items_file = fp

            bad_header = ["|uuid|", "|title|", "|description|"]
            bad_data = [
                "|f19c962e-eec0-455f-baa9-c0ba6986d01b|",
                "|autem deserunt quo quaerat deleniti|",
                "|aut soluta repudiandae numquam accusantium pariatur culpa fugiat ducimus laudantium consequatur quam "
                "rerum dolorem beatae cum eius magni in architecto nihil similique odit été distinctio eligendi alias "
                "optio asperiores incidunt unde quaerat dolor a animi sapiente vel saepe ad iusto doloribus libero "
                "voluptates voluptate explicabo velit officiis praesentium accusamus possimus|",
            ]
            bad_input_items_csv_writer = csv.writer(self.bad_input_items_file)
            bad_input_items_csv_writer.writerow(bad_header)
            bad_input_items_csv_writer.writerow(bad_data)

        # Generate expected bad json output file

        with NamedTemporaryFile(suffix=".json", delete=False) as fp:
            self.bad_output_json = fp

        # Generate the Groups File
        with NamedTemporaryFile(
            "w", encoding="UTF8", newline="", suffix=".csv", delete=False
        ) as fp:
            self.input_groups_file = fp

            group_header = ["|uuid|", "|group|"]
            group_data = [
                "|cbfd812d-7b13-4b1c-8193-82a521ce6fb6|",
                "|nesciunt quidem iure|",
            ]
            group_items_csv_writer = csv.writer(self.input_groups_file)
            group_items_csv_writer.writerow(group_header)
            group_items_csv_writer.writerow(group_data)

        # Generate file with invalid file extension
        with NamedTemporaryFile(
            "w", encoding="UTF8", newline="", suffix=".txt", delete=False
        ) as fp:
            self.bad_extension_input_items_file = fp

    def tearDown(self):
        super().tearDown()

        # Delete our test files

        os.unlink(self.input_groups_file.name)

        os.unlink(self.good_input_items_file.name)
        os.unlink(self.good_output_json.name)

        os.unlink(self.bad_input_items_file.name)
        os.unlink(self.bad_output_json.name)

        os.unlink(self.bad_extension_input_items_file.name)

    def test_e2e_conversion_with_good_input_file(self):
        result = subprocess.run(
            [
                "python",
                "main.py",
                self.good_input_items_file.name,
                self.input_groups_file.name,
                "-o",
                self.good_output_json.name,
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0)
        with open(self.good_output_json.name, mode="r") as output_file:
            converted_json = json.load(output_file)
            self.assertEqual(self.expected_json, converted_json)

    def test_e2e_conversion_with_bad_input_file(self):
        """
        Test valid .csv file but with incorrect headers
        """
        result = subprocess.run(
            [
                "python",
                "main.py",
                self.bad_input_items_file.name,
                self.input_groups_file.name,
                "-o",
                self.bad_output_json.name,
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        self.assertIn(
            ITEMS_CSV_COLUMNS_HELP_TEXT,
            result.stderr,
        )

    def test_e2e_conversion_with_bad_extension_input_file(self):
        """
        Test with a none CSV file, in this case a .TXT file
        """
        result = subprocess.run(
            [
                "python",
                "main.py",
                self.bad_extension_input_items_file.name,
                self.input_groups_file.name,
                "-o",
                self.bad_output_json.name,
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        self.assertIn(
            ITEMS_CSV_COLUMNS_HELP_TEXT,
            result.stderr,
        )

    def test_e2e_conversion_with_none_existent_input_file(self):
        result = subprocess.run(
            [
                "python",
                "main.py",
                "no_file.csv",
                self.input_groups_file.name,
                "-o",
                self.bad_output_json.name,
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        self.assertIn(
            "no_file.csv path does not exist",
            result.stderr,
        )


if __name__ == "__main__":
    unittest.main()
