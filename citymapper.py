import json
import requests


API_BASE_URL = "https://api.external.citymapper.com"
ENDPOINT = "/api/1/traveltimes"
CACHE_FILE = "travel_times_cache.json"

with open('citymapper_api_key.txt', 'r') as file:
    API_KEY = file.read().strip()


def generate_cache_key(start_coords, end_coords):
    return f"{start_coords}-{end_coords}"


def cache_response(cache_key, response):
    try:
        with open(CACHE_FILE, 'r') as file:
            cache_data = json.load(file)
    except FileNotFoundError:
        cache_data = {}

    cache_data[cache_key] = response

    with open(CACHE_FILE, 'w') as file:
        json.dump(cache_data, file)


def get_cached_response(cache_key):
    try:
        with open(CACHE_FILE, 'r') as file:
            cache_data = json.load(file)
            return cache_data.get(cache_key)
    except FileNotFoundError:
        return None


def get_travel_times(start_coords, end_coords):
    cache_key = generate_cache_key(start_coords, end_coords)
    cached_response = get_cached_response(cache_key)

    if cached_response:
        return cached_response

    headers = {
        'Citymapper-Partner-Key': API_KEY
    }
    params = {
        'start': ','.join(map(str, start_coords)),
        'end': ','.join(map(str, end_coords)),
        'traveltime_types': 'walk,bike,transit'
    }
    url = API_BASE_URL + ENDPOINT
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        response_data = response.json()
        cache_response(cache_key, response_data)
        return response_data
    else:
        raise Exception(f"Request failed with status code {response.status_code}")


start_coords = [51.518276,-0.110500]
end_coords = [51.519953,-0.311123]

travel_times = get_travel_times(start_coords, end_coords)
print(travel_times)