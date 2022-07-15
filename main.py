import argparse

import group_reader
import item_reader
import output_writer

parser = argparse.ArgumentParser()

parser.add_argument('items', help='json or csv file containing items')
parser.add_argument('groups', help='json or csv file containing groups')
parser.add_argument('--output_file', '-o', help='Output file', required=True)


class Converter:

    def __init__(self, items_source, groups_source, writer=None):
        self.items_source = items_source
        self.groups_source = groups_source
        self.writer = writer

    def join_item_groups(self, items_file, groups_file):
        items = self.items_source.read(items_file)
        groups = self.groups_source.read(groups_file)
        joined_data = []
        for item in items:
            item_dict = {
                'uuid': item['uuid'],
                'title': item['title'],
                'description': item['description'],
                'context': groups.get(item["group_id"])
            }

            joined_data.append(item_dict)
        return joined_data

    def write_to_output(self, joined_data, output_file):
        self.writer.write(joined_data, output_file)


if __name__ == '__main__':
    args = parser.parse_args()
    item_data_source = item_reader.get_data_source(args.items)
    group_data_source = group_reader.get_data_source(args.groups)
    output_writer = output_writer.get_writer(args.output_file)
    converter = Converter(item_data_source, group_data_source, output_writer)
    data = converter.join_item_groups(args.items, args.groups)
    converter.write_to_output(data, args.output_file)

