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
        center: [-127.6476, 53.7267], // starting position [lng, lat]
        zoom: 4.7 // starting zoom
      });

      this.map.on('load', () => {
        // Load Fisher Range layer
        this.map.addSource('fisher_range', {
          type: 'vector',
          tiles: ['http://localhost:7800/public.fisher_range/{z}/{x}/{y}.pbf'],
          'source-layer': 'fisher_range',
          'minzoom': 0,
          'maxzoom': 22
        })

        let layer = {
          'id': 'fisher_range',
          'type': 'fill',
          'source': 'fisher_range',
          'source-layer': 'public.fisher_range',
          'layout': {'visibility': 'visible'},
          'paint': {
            'fill-color': 'hsla(220,82%,28%,0.69)',
            // 'fill-outline-color': 'hsla(219,100%,15%,0.84)'
            'fill-outline-color': [
              'interpolate',
              ['linear'],
              ['zoom'],
              5,
              'hsla(0, 0%, 55%, 0)',
              10,
              'hsl(0, 0%, 19%)'
            ]
          }
        }
        this.map.addLayer(layer);
      })
    }
  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#map {
  position: absolute;
  top: 80px;
  right: 0;
  bottom: 0;
  left: 0;
}
</style>
