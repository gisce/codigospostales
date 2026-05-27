# -*- coding: utf-8 -*-
import argparse
from collections import defaultdict
import csv
import json


def main(zipcodes_path, output_path):
    zipcodes = defaultdict(list)

    with open(zipcodes_path, 'r') as f:
        reader = csv.DictReader(f, delimiter=';')

        for row in reader:
            zipcode = row.get('zipcode')
            if not zipcode:
                continue

            zipcodes[zipcode].append({
                'city': row.get('city', '').decode('utf-8').strip(),
                'ine': row.get('ine', '').decode('utf-8').strip(),
                'inep': row.get('inep', '').decode('utf-8').strip()
            })

    with open(output_path, 'wb') as f:
        f.write(b"# -*- coding: utf-8 -*-\n")
        f.write(b"ZIPCODES = {\n")
        for zipcode, entries in zipcodes.items():
            key_prefix = u"    '{}': [".format(zipcode)
            padding = u" " * len(key_prefix)
            for i, entry in enumerate(entries):
                entry_str = json.dumps(entry, ensure_ascii=False, sort_keys=True)
                if len(entries) == 1:
                    line = u"{}{}],\n".format(key_prefix, entry_str)
                elif i == 0:
                    line = u"{}{},\n".format(key_prefix, entry_str)
                elif i == len(entries) - 1:
                    line = u"{}{}],\n".format(padding, entry_str)
                else:
                    line = u"{}{},\n".format(padding, entry_str)
                f.write(line.encode('utf-8'))
        f.write(b"}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process zipcodes and cities data.')
    parser.add_argument('zipcodes_path', type=str, help='Path to the TRAM file')
    parser.add_argument('output_path', type=str, help='Path to save the output CSV file')

    args = parser.parse_args()
    main(args.zipcodes_path, args.output_path)
