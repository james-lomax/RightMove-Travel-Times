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
    required_fields = ['Address', 'Description', 'Price', 'ListingUrl']

    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for index, row in enumerate(reader):
            row_num = index + 1
            try:
                validate_fields(row, required_fields)

                if not validate_url(row['ListingUrl']):
                    raise ValueError("Invalid listing_url", row['ListingUrl'])
                if not validate_price(row['Price']):
                    raise ValueError("Invalid price_pcm", row['Price'])
                if not row['Address']:
                    raise ValueError("Empty address", row['Address'])
                
                thumbnail_url = ""
                for thumbnail_key in ['Thumbnail', 'Thumbnail2', 'Thumbnail3', 'Thumbnail4']:
                    if thumbnail_key in row and row[thumbnail_key].startswith('https://media.rightmove.co.uk:443/dir/crop/'):
                        thumbnail_url = row[thumbnail_key]
                        break
                
                if not thumbnail_url:
                    print(f"WARNING: Could not find thumbnail URL in row {row_num}")

                apartment = Apartment(
                    listing_url=row['ListingUrl'],
                    thumbnail_url=thumbnail_url,
                    price_pcm=parse_price(row['Price']),
                    address=row['Address'],
                    description=row['Description']
                )
                apartments.append(apartment)

            except (ValueError, KeyError) as e:
                print(f"Row {row_num} skipped: {e}")

    return apartments

# file_path = 'apartments.csv'
# apartments = load_apartments(file_path)
# for apartment in apartments:
#     print(apartment)
