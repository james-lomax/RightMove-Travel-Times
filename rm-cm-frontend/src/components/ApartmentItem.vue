<template>
    <div class="apartment-item">
      <a :href="apartment.listing_url" target="_blank">
        <img :src="apartment.thumbnail_url" alt="Apartment Thumbnail" />
        <h3>{{ apartment.address }}</h3>
      </a>
      <p>Price per month: £{{ apartment.price_pcm }}</p>
      <p>Description: {{ apartment.description }}</p>
      <div class="journeys">
        <h4>Journeys to Work:</h4>
        <p>Walking: {{ journeys.Work.travel_times.walk_travel_time_minutes }} minutes</p>
        <p>Transit: {{ journeys.Work.travel_times.transit_time_minutes }} minutes</p>
        <p>Biking: {{ journeys.Work.travel_times.bike_time_minutes }} minutes</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      apartment: Object,
      journeys: Object,
    },
  };
  </script>
  
  <style scoped>
  .apartment-item {
    border: 1px solid #ccc;
    padding: 16px;
    margin-bottom: 16px;
  }
  
  .apartment-item img {
    width: 100%;
    max-height: 200px;
    object-fit: cover;
  }
  
  .apartment-item h3 {
    margin: 8px 0;
    color: #333;
  }
  
  .apartment-item a {
    text-decoration: none;
  }
  
  .journeys {
    margin-top: 8px;
  }
  </style>
  