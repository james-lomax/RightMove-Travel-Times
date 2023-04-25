<template>
  <v-container>
    <v-row>
      <v-col>
        <v-select
          :items="sortOptions"
          v-model="selectedSortOption"
          label="Sort by"
          @change="sortApartments"
          outlined
        ></v-select>
      </v-col>
    </v-row>
    <ApartmentItem
      v-for="apartmentData in sortedApartments"
      :key="apartmentData.apartment.listing_url"
      :apartment="apartmentData.apartment"
      :journeys="apartmentData.journeys"
    ></ApartmentItem>
  </v-container>
</template>

<script>
import ApartmentItem from "@/components/ApartmentItem.vue";

function travelTimeForJourney(journey, mode) {
  if (mode == 'walk') {
    return journey.travel_times.walk_travel_time_minutes
  } else if (mode == 'transit') {
    return journey.travel_times.transit_time_minutes
  } else if (mode == 'bike') {
    return journey.travel_times.bike_time_minutes
  } else {
    throw new Error("wtf")
  }
}

function travelTimeForApartment(apartment, mode) {
  return Object.values(apartment.journeys)
    .map((j) => travelTimeForJourney(j, mode))
    .reduce((a, x) => Math.max(a, x), 0)
}

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
            "listing_url": "",
            "thumbnail_url": "",
            "price_pcm": 999,
            "address": "Loading listings..",
            "description": ""
          },
          "journeys": {
          }
        },
      ],
      sortOptions: [
        "price",
        "walk",
        "transit",
        "bike",
      ],
      selectedSortOption: "price",
    };
  },
  computed: {
    sortedApartments() {
      return this.sortApartments(this.apartments);
    },
  },
  mounted() {
    this.updateData()
  },
  methods: {
    async updateData() {
      let rsp = await fetch('output.json')
      let data = await rsp.json()
      this.apartments = data.apartments
    },
    sortApartments(apartments) {
      const sortBy = this.selectedSortOption;
      if (sortBy == 'price') {
        return apartments.slice().sort((a, b) => {
          return a.apartment.price_pcm - b.apartment.price_pcm;
        })
      } else {
        return this.sortByTravelTime(apartments, sortBy)
      }
    },
    sortByTravelTime(apartments, mode) {
      return apartments.slice().sort((a, b) => {
        let av = travelTimeForApartment(a, mode)
        let bv = travelTimeForApartment(b, mode)
        return av - bv
      })
    },
  },
};
</script>
