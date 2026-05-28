# -*- encoding: utf-8 -*-
import pandas as pd
import argparse


def main(tram_path, nomdef_path, output_path):

    with open(tram_path, 'rb') as f:
        data = f.read().decode('iso-8859-1')

    lines = data.splitlines()
    lines = [
        {
            'ine': line[0:5],
            'zipcode': line[42:47],
            'pob': line[78:82],
            'city': line[110:135],
            'inep': line[13:17] + line[18:20]
        } for line in lines
    ]
    zipcodes = pd.DataFrame(lines)

    zipcodes = zipcodes.drop_duplicates()
    zipcodes = zipcodes[~zipcodes['city'].str.contains('DISEMINADO', na=False)]
    zipcodes['city'] = zipcodes['city'].apply(lambda x: x.strip())


    with open(nomdef_path, 'rb') as f:
        data = f.read().decode('utf-8')

    lines = data.splitlines()
    lines = [
        {
            'ine': line[0:5],
            'pob': line[5:9],
            'city': line[11:81],
            'inep': line[5:11],
        } for line in lines
    ]
    cities = pd.DataFrame(lines)
    cities = cities.drop_duplicates()
    cities = cities[~cities['city'].str.contains('DISEMINADO', na=False)]
    cities = cities[~cities['inep'].str.endswith('99', na=False)]
    cities['city'] = cities['city'].apply(lambda x: x.strip())

    # Merge data frames
    merged = zipcodes.merge(
        cities,
        how='left',
        on=['ine', 'pob'],
        indicator=True
    )

    # Fix left only cities
    merged['city'] = merged['city_y'].combine_first(merged['city_x'])
    merged['inep'] = merged['inep_y'].combine_first(merged['inep_x'])
    merged = merged.drop(columns=['city_x', 'city_y', 'inep_x', 'inep_y', '_merge'])

    merged = merged[~merged['inep'].str.endswith('99', na=False)]
    merged = merged.drop_duplicates()

    # Export to CSV
    merged.to_csv(output_path, index=None, sep=';', columns=['ine', 'zipcode', 'inep', 'city'], encoding='utf-8')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process zipcodes and cities data.')
    parser.add_argument('tram_path', type=str, help='Path to the TRAM file')
    parser.add_argument('nomdef_path', type=str, help='Path to the Nomdef file')
    parser.add_argument('output_path', type=str, help='Path to save the output CSV file')

    args = parser.parse_args()
    main(args.tram_path, args.nomdef_path, args.output_path)
