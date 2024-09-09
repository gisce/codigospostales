import pandas as pd
import argparse


def main(tram_path, nomdef_path, output_path):

    with open(tram_path, 'rb') as f:
        data = f.read().decode('iso-8859-1')

    lines = data.split('\r\n')
    lines = [
        {
            'ine': line[0:5],
            'zipcode': line[42:47],
            'pob': line[78:82],
            'city': line[110:135]
        } for line in lines
    ]
    zipcodes = pd.DataFrame(lines)

    zipcodes = zipcodes.drop_duplicates()
    zipcodes = zipcodes[~zipcodes['city'].str.contains('DISEMINADO', na=False)]
    zipcodes['city'] = zipcodes['city'].apply(lambda x: x.strip())


    with open(nomdef_path, 'rb') as f:
        data = f.read().decode('iso-8859-1')

    lines = data.split('\r\n')
    lines = [
        {
            'ine': line[0:5],
            'pob': line[5:9],
            'city': line[11:81]
        } for line in lines
    ]
    cities = pd.DataFrame(lines)
    cities = cities.drop_duplicates()
    cities = cities[~cities['city'].str.contains('DISEMINADO', na=False)]
    cities['city'] = cities['city'].apply(lambda x: x.strip())

    # Merge data frames
    merged = zipcodes.merge(
        cities,
        how='left',
        on=['ine', 'pob'],
        indicator=True
    )

    # Fix left only cities
    merged['city'] = merged.apply(lambda row: not pd.isna(row['city_y']) and row['city_y'] or row['city_x'], axis='columns')

    # Export to CSV
    merged.to_csv(output_path, index=None, sep=';', columns=['ine', 'zipcode', 'city'], encoding='utf-8')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process zipcodes and cities data.')
    parser.add_argument('tram_path', type=str, help='Path to the TRAM file')
    parser.add_argument('nomdef_path', type=str, help='Path to the Nomdef file')
    parser.add_argument('output_path', type=str, help='Path to save the output CSV file')

    args = parser.parse_args()
    main(args.tram_path, args.nomdef_path, args.output_path)
