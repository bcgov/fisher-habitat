<template>
  <div id='map'></div>
</template>

<script>
import maplibregl from 'maplibre-gl'; // or "const maplibregl = require('maplibre-gl');"
console.dir(maplibregl)

export default {
  name: 'Map',
  mounted () {
    console.log('in init')

    this.createMap()
  },
  methods: {
    createMap: function () {

      console.log('in create map')

      this.map = new maplibregl.Map({
        container: 'map',
        style: 'https://api.maptiler.com/maps/outdoor/?key=Jit3oGuugSBYRmzQu0Qw#-0.2/0.00000/-2.36049', // #-0.2/0.00000/-2.36049
        center: [-74.5, 40], // starting position [lng, lat]
        zoom: 9 // starting zoom
      });

      console.dir(this.map)
    }
  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
