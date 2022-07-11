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
        with open(file, 'r') as cf:
            for item in csv.DictReader(cf, quotechar="|"):
                yield item


class JSONDataSource(DataSource):

    def read(self, file):
        with open(file, 'r') as jf:
            return json.load(jf)

