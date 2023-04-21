import csv
import re
from dataclasses import dataclass

@dataclass
class Apartment:
    listing_url: str
    thumbnail_url: str
    price_pcm: int
    address: str
    description: str

def validate_url(url):
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    return bool(pattern.match(url))

def validate_price(price):
    pattern = re.compile(r'^£\d{1,3}(?:,\d{3})*\s?pcm$')
    return bool(pattern.match(price))

def parse_price(price):
    return int(price[1:-4].replace(",", ""))

def validate_fields(row, fieldnames):
    for field in fieldnames:
        if field not in row:
            raise KeyError(f"Field {field} is missing")

def load_apartments(file_path):
    apartments = []
    required_fields = ['Title_link', 'Thumbnail', 'Title', 'propertyCard-address', 'propertyCard-link']

    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                row = {k.strip('\ufeff'):v for k,v in row.items()}
                validate_fields(row, required_fields)

                if not validate_url(row['Title_link']):
                    raise ValueError("Invalid listing_url", row['Title_link'])
                if not validate_url(row['Thumbnail']):
                    raise ValueError("Invalid thumbnail_url", row['Thumbnail'])
                if not validate_price(row['Title']):
                    raise ValueError("Invalid price_pcm", row['Title'])
                if not row['propertyCard-address']:
                    raise ValueError("Empty address", row['propertyCard-address'])

                apartment = Apartment(
                    listing_url=row['Title_link'],
                    thumbnail_url=row['Thumbnail'],
                    price_pcm=parse_price(row['Title']),
                    address=row['propertyCard-address'],
                    description=row['propertyCard-link']
                )
                apartments.append(apartment)

            except (ValueError, KeyError) as e:
                print(f"Row skipped: {e}")

    return apartments

file_path = 'apartments.csv'
apartments = load_apartments(file_path)
for apartment in apartments:
    print(apartment)
