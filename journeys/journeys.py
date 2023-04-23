import typing as t
from dataclasses_json import dataclass_json
from dataclasses import dataclass

from citymapper import TravelTimes, get_travel_times
from config import load_config, ConfigDestination
from apartments import Apartment, load_apartments
from geodecode import get_lat_lon_cached


@dataclass_json
@dataclass
class Journey:
    travel_times: TravelTimes


@dataclass_json
@dataclass
class AnnotatedApartment:
    apartment: Apartment
    journeys: t.Dict[str, Journey]


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
        }
    )


def annotate_apartments(apartments):
    config = load_config()
    annotated = []
    for apartment in apartments:
        print(f'Processing apartment "{apartment.description}" at {apartment.address}')
        try:
            annotated.append(annotate_apartment(apartment, config))
        except Exception as e:
            print(f'Could not annotate apartment "{apartment.description}" at {apartment.address}: {e}')
    return annotated


apartments = load_apartments('apartments.csv')
annotated = annotate_apartments(apartments)

with open('output.json', 'w') as f:
    f.write(StateRoot(apartments=annotated).to_json())