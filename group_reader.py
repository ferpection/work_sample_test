import csv
import json


def get_data_source(file: str):
    if file.lower().endswith('.csv'):
        return CsvDataSource()
    elif file.lower().endswith('.json'):
        return JSONDataSource()
    else:
        raise Exception('file type must be json or csv')


class DataSource:

    def read(self, file):
        pass


class CsvDataSource(DataSource):

    def read(self, file):
        groups = {}
        with open(file, 'r') as cf:
            for row in csv.DictReader(cf, quotechar="|"):
                groups[row['uuid']] = row['group']
        return groups


class JSONDataSource(DataSource):

    def read(self, file):
        groups = {}
        with open(file, 'r') as cf:
            for line in json.load(cf):
                groups[line['uuid']] = line['group']

        return groups
