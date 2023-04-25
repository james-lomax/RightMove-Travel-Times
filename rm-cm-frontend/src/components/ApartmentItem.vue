<template>
<v-card class="mx-auto mb-4" max-width="900">
    <v-row>
        <v-col cols="4">
            <a :href="apartment.listing_url" target="_blank">
                <v-img :src="apartment.thumbnail_url" :alt="apartment.address" aspect-ratio="1.5"></v-img>
            </a>
        </v-col>
        <v-col cols="8">
        <v-card-title>
            <a :href="apartment.listing_url" target="_blank">{{ apartment.address }}</a>
            <span v-if="suspicious_address">⚠️ Sus address</span>
        </v-card-title>
        <v-card-subtitle>Price: £{{ apartment.price_pcm }} per month</v-card-subtitle>
        <v-table>
            <template v-slot:default>
            <thead>
                <tr>
                <th>Destination</th>
                <th>Walk</th>
                <th>Transit</th>
                <th>Bike</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(journey, destination) in journeys" :key="destination">
                <td class="journey-cell">{{ destination }}</td>
                <td class="journey-cell">{{ journey.travel_times.walk_travel_time_minutes }} mins</td>
                <td class="journey-cell">{{ journey.travel_times.transit_time_minutes }} mins</td>
                <td class="journey-cell">{{ journey.travel_times.bike_time_minutes }} mins</td>
                </tr>
            </tbody>
            </template>
        </v-table>
        </v-col>
    </v-row>
</v-card>
</template>
  
<script>
export default {
name: "ApartmentItem",
props: {
    apartment: {
    type: Object,
    required: true,
    },
    journeys: {
    type: Object,
    required: true,
    },
    suspicious_address: {
        type: Boolean,
        required: true
    }
},
};
</script>
  
<style scoped>
a {
text-decoration: none;
color: inherit;
}

a:hover {
text-decoration: underline;
}

.journey-cell {
  padding-left: 5px;
  padding-right: 5px;
}
</style>
  