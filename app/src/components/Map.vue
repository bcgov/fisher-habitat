<template>
  <div id='map'></div>
</template>

<script>
import maplibregl from 'maplibre-gl'; // or "const maplibregl = require('maplibre-gl');"

export default {
  name: 'Map',
  mounted () {
    this.createMap()
  },
  methods: {
    createMap: function () {
      this.map = new maplibregl.Map({
        container: 'map',
        style: 'https://api.maptiler.com/maps/outdoor/style.json?key=Jit3oGuugSBYRmzQu0Qw',
        center: [-74.5, 40], // starting position [lng, lat]
        zoom: 9 // starting zoom
      });
    }
  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  #map {position: absolute; top: 0; right: 0; bottom: 0; left: 0;}
</style>
