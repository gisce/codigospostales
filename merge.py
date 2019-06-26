import pandas as pd

# Import zipcodes
zipcodes = pd.read_csv(
    'cps.txt',
    sep=';',
    header=None,
    names=['ine', 'zipcode', 'pob', 'city'],
    dtype={'ine': str, 'zipcode': str, 'pob': str, 'city': str}
)
zipcodes['city'] = zipcodes['city'].apply(lambda x: str(x).strip())

# Import cities
cities = pd.read_csv(
    'pobs.txt',
    sep=';',
    header=None,
    names=['ine', 'pob', 'city'],
    dtype={'ine': str, 'pob': str, 'city': str}
)
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
merged.to_csv('zipcodes.csv', index=None, sep=';', columns=['ine', 'zipcode', 'city'])

