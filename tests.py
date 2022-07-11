import csv
import json
import os
import types

import item_reader
import group_reader
import output_writer

from main import Converter


def test_can_read_items_from_csv():
    reader = item_reader.CsvDataSource()
    result = reader.read("test_items.csv")
    assert isinstance(result, types.GeneratorType)
    assert next(result) == {'uuid': '001', 'title': 'one', 'description': 'first item', 'group_id': '1'}


def test_can_read_items_from_json():
    reader = item_reader.JSONDataSource()
    result = reader.read("test_items.json")
    assert isinstance(result, list)
    assert result[0] == {'uuid': '001', 'title': 'one', 'description': 'first item', 'group_id': '1'}


def test_can_read_groups_from_csv():
    reader = group_reader.CsvDataSource()
    result = reader.read("test_groups.csv")
    assert isinstance(result, dict)
    assert result == {'1': "group one", "2": "group two"}


def test_can_read_groups_from_json():
    reader = group_reader.JSONDataSource()
    result = reader.read("test_groups.json")
    assert isinstance(result, dict)
    assert result == {'1': "group one", "2": "group two"}


def test_can_join_items_groups():
    converter = Converter(item_reader.CsvDataSource(), group_reader.JSONDataSource())
    result = converter.join_item_groups("test_items.csv", "test_groups.json")
    assert isinstance(result, list)
    assert result == [{'uuid': '001', 'title': 'one', 'description': 'first item', 'context': 'group one'},
                   {'uuid': '002', 'title': 'two', 'description': 'second item', 'context': 'group one'},
                   {'uuid': '003', 'title': 'three', 'description': 'third item', 'context': 'group two'}]


def test_can_write_to_csv():
    output_data = [{'uuid': '001', 'title': 'one', 'description': 'first item', 'context': 'group one'},
                   {'uuid': '002', 'title': 'two', 'description': 'second item', 'context': 'group one'},
                   {'uuid': '003', 'title': 'three', 'description': 'third item', 'context': 'group two'}]
    writer = output_writer.CsvWriter()
    output_file = "temp.csv"
    try:
        writer.write(output_data, output_file)
        with open(output_file) as file:
            contents = [content for content in csv.DictReader(file)]
    finally:
        os.remove(output_file)
    assert output_data == contents


def test_can_write_to_json():
    output_data = [{'uuid': '001', 'title': 'one', 'description': 'first item', 'context': 'group one'},
                   {'uuid': '002', 'title': 'two', 'description': 'second item', 'context': 'group one'},
                   {'uuid': '003', 'title': 'three', 'description': 'third item', 'context': 'group two'}]

    structured_output = [{"001_title": {"string": "one"},
                          "001_description": {"string": "first item", "context": "group one"}},
                         {"002_title": {"string": "two"}, "002_description":
                             {"string": "second item", "context": "group one"}},
                         {"003_title": {"string": "three"},
                          "003_description": {"string": "third item", "context": "group two"}}]

    writer = output_writer.StructuredJSONWriter()
    output_file = "temp.json"
    try:
        writer.write(output_data, output_file)
        with open(output_file) as file:
            contents = [content for content in json.load(file)]
    finally:
        os.remove(output_file)
    assert structured_output == contents
