import csv
import json


def get_writer(filename: str):
    if filename.lower().endswith('.csv'):
        return CsvWriter()
    elif filename.lower().endswith('.json'):
        return StructuredJSONWriter()
    else:
        raise Exception('file type must be json or csv')


class Writer:

    def write(self, data, output_file):
        pass


class CsvWriter(Writer):

    def write(self, data, output_file):
        with open(output_file, 'w+') as file:
            fields = data[0].keys()
            dict_writer = csv.DictWriter(file, fields)
            dict_writer.writeheader()
            dict_writer.writerows(data)


class StructuredJSONWriter(Writer):

    def write(self, data, output_file):
        with open(output_file, 'w+') as file:
            structured_dict = self._to_structured(data)
            json.dump(structured_dict, file)

    @staticmethod
    def _to_structured(dataset):
        structured_data = []
        for data in dataset:
            uuid_title = f"{data['uuid']}_title"
            title = data['title']
            uuid_description = f"{data['uuid']}_description"
            description = data['description']
            context = data['context']

            structured_data.append({
                uuid_title: {
                    'string': title
                },
                uuid_description: {
                    'string': description,
                    'context': context
                }
            })

        return structured_data
