<template>
  <v-container>
    <ApartmentItem
      v-for="apartmentData in apartments"
      :key="apartmentData.apartment.listing_url"
      :apartment="apartmentData.apartment"
      :journeys="apartmentData.journeys"
    ></ApartmentItem>
  </v-container>
</template>

<script>
import ApartmentItem from "@/components/ApartmentItem.vue";

export default {
  name: "ApartmentList",
  components: {
    ApartmentItem,
  },
  data() {
    return {
      apartments: [
      {
            "apartment": {
                "listing_url": "https://www.rightmove.co.uk/properties/133891604#/?channel=RES_LET",
                "thumbnail_url": "https://media.rightmove.co.uk:443/dir/crop/10:9-16:9/118k/117484/133891604/117484_LND210457_L_IMG_00_0000_max_476x317.jpeg",
                "price_pcm": 815,
                "address": "Northesk House, Tent Street, E1",
                "description": "Double Room in Flat Share- Whitechapel Rent is \u00a3815 per month INCLUDING ALL BILLS **ZERO DEPOSIT OPTION AVAILABLE** Brand New Flooring & Furniture Provided!!! Sharing with 2 Female Tenants The Flat comprises of four Large Double Roo..."
            },
            "journeys": {
                "Work": {
                    "travel_times": {
                        "walk_travel_time_minutes": 61,
                        "transit_time_minutes": 27,
                        "bike_time_minutes": 22
                    }
                }
            }
        },
        {
            "apartment": {
                "listing_url": "https://www.rightmove.co.uk/properties/133916501#/?channel=RES_LET",
                "thumbnail_url": "https://media.rightmove.co.uk:443/dir/crop/10:9-16:9/157k/156386/133916501/156386_11955373_IMG_00_0000_max_476x317.jpeg",
                "price_pcm": 1240,
                "address": "Hosta House, Beaumont Road, E10",
                "description": "** L&Q ONLY ACCEPTS EMAIL ENQUIRIES FOR THIS APARTMENT, PLEASE KINDLY DO NOT CALL. ** This property is offered on the Intermediate Market Rent scheme and eligibility criteria will apply. L&Q are pleased to present this two bedroom, second floor apartment in Leyton. This apartme..."
            },
            "journeys": {
                "Work": {
                    "travel_times": {
                        "walk_travel_time_minutes": 152,
                        "transit_time_minutes": 49,
                        "bike_time_minutes": 52
                    }
                }
            }
        },
      ],
    };
  },
};
</script>
