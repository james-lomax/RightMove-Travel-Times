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
    };
  },
  mounted() {
    this.updateData()
  },
  methods: {
    async updateData() {
      let rsp = await fetch('http://localhost:3095/output.json')
      let data = await rsp.json()
      this.apartments = data.apartments
    }
  }
};
</script>
