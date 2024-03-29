import os
import typing as t
from dataclasses_json import dataclass_json
from dataclasses import dataclass

from citymapper import TravelTimes, get_travel_times
from config import load_config
from apartments import Apartment, load_apartments
from geodecode import get_lat_lon_cached, is_address_just_london
from browseai import get_latest_task_data


@dataclass_json
@dataclass
class Journey:
    travel_times: TravelTimes


@dataclass_json
@dataclass
class AnnotatedApartment:
    apartment: Apartment
    journeys: t.Dict[str, Journey]
    suspicious_address: bool


@dataclass_json
@dataclass
class StateRoot:
    apartments: t.List[AnnotatedApartment]


def compute_journey(start_address, end_address) -> Journey:
    start_coords = get_lat_lon_cached(start_address)
    end_coords = get_lat_lon_cached(end_address)
    return Journey(
        travel_times=get_travel_times(start_coords, end_coords)
    )


def annotate_apartment(apartment, config):
    return AnnotatedApartment(
        apartment=apartment,
        journeys={
            dst.name: compute_journey(apartment.address, dst.address)
            for dst in config.destinations
        },
        suspicious_address=is_address_just_london(apartment.address)
    )


def annotate_apartments(apartments):
    config = load_config()
    
    # Override addresses where the geodecode fails
    for apartment in apartments:
        if apartment.listing_url in config.address_overrides:
            apartment.address = config.address_overrides[apartment.listing_url]

    annotated = []
    for apartment in apartments:
        print(f'Processing apartment at {apartment.address}')
        try:
            annotated.append(annotate_apartment(apartment, config))
        except Exception as e:
            print(f'Could not annotate apartment at {apartment.address}: {e}')
    return annotated


print("Downloading latest data...")
properties_data = get_latest_task_data(os.environ.get('BROWSE_AI_ROBOT_ID'))
print("Computing trips...")
apartments = load_apartments(properties_data['capturedLists']['Properties'])
# Deduplicate rows
apartments = list({a.listing_url: a for a in apartments}.values())
annotated = annotate_apartments(apartments)
print(f"DONE. Annotated {len(annotated)}/{len(apartments)} apartments successfully.")

with open('../rm-cm-frontend/public/apartments.json', 'w') as f:
    f.write(StateRoot(apartments=annotated).to_json())
