<template>
  <div id='map'></div>
</template>

<script>
import maplibregl from 'maplibre-gl'; // or "const maplibregl = require('maplibre-gl');"
import MapboxDraw from '@mapbox/mapbox-gl-draw';

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
        center: [-127.6476, 53.7267], // starting position [lng, lat]
        zoom: 9 // starting zoom
      });

      var draw = new MapboxDraw({
        displayControlsDefault: false,
        controls: {
          polygon: true,
          trash: true
        }
      });

      this.map.addControl(draw);
    }
  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  #map {position: absolute; top: 80px; right: 0; bottom: 0; left: 0;}
</style>
