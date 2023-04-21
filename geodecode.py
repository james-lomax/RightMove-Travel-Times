import requests
import json
import os

cache_filename = "geocoding_cache.json"
api_key_filename = "google_maps_api_key.txt"

def load_api_key(filename):
    with open(filename, "r") as f:
        return f.read().strip()

def load_cache(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    else:
        return {}

def save_cache(filename, cache):
    with open(filename, "w") as f:
        json.dump(cache, f)

def get_lat_lon(address, api_key):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    payload = {"address": address, "key": api_key}
    response = requests.get(base_url, params=payload)

    if response.status_code == 200:
        data = response.json()
        if data["status"] == "OK":
            lat = data["results"][0]["geometry"]["location"]["lat"]
            lon = data["results"][0]["geometry"]["location"]["lng"]
            return lat, lon
        else:
            print("Error:", data["status"])
            return None
    else:
        print("Error: HTTP", response.status_code)
        return None

def get_lat_lon_cached(address, api_key):
    cache = load_cache(cache_filename)
    if address in cache:
        lat, lon = cache[address]
        print("Using cached coordinates.")
    else:
        lat, lon = get_lat_lon(address, api_key)
        if lat and lon:
            cache[address] = (lat, lon)
            save_cache(cache_filename, cache)
            print("Saved coordinates to cache.")
    return lat, lon

# Load the API key from the text file
api_key = load_api_key(api_key_filename)
address = "Finchley Road, Hampstead NW3"
lat, lon = get_lat_lon_cached(address, api_key)

if lat and lon:
    print("Latitude:", lat)
    print("Longitude:", lon)
else:
    print("Unable to get coordinates.")
