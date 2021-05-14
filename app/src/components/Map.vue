<template>
  <div>
    <div id='map'></div>
    <div id='actions'></div>
  </div>
</template>

<script>
import maplibregl from 'maplibre-gl'; // or "const maplibregl = require('maplibre-gl');"
import MapboxDraw from '@mapbox/mapbox-gl-draw';

const TILE_SERVER_FISHER = 'http://localhost:7800/'
export default {
  name: 'Map',
  mounted() {
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

      // Define bounds that conform to the `LngLatBoundsLike` object.
      var bounds = [
        [-141.06, 46.30], // [west, south]
        [-116.03, 62.00]  // [east, north]
      ];

      // Set the map's max bounds.
      this.map.setMaxBounds(bounds);

      var draw = new MapboxDraw({
        displayControlsDefault: false,
        controls: {
          polygon: true,
          trash: true
        }
      });

      this.map.addControl(draw);
      this.map.on('load', () => {
        this.loadLayers()
      })
    },
    loadLayers: function () {
      // Load Fisher Range layer
      const loadFisherRange = () => {
        this.map.addSource('fisher_range', {
          type: 'vector',
          tiles: [`${TILE_SERVER_FISHER}/public.fisher_range/{z}/{x}/{y}.pbf`],
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
            'fill-color': 'hsla(220,82%,28%,0.35)',
            'fill-outline-color': [
              'interpolate',
              ['linear'],
              ['zoom'],
              5,
              'hsla(219,100%,15%,0.1)',
              10,
              'hsl(219,100%,15%)'
            ]
          }
        }
        this.map.addLayer(layer);
      }

      const loadFisherFHE = () => {
        this.map.addSource('fisher_fhe', {
          type: 'vector',
          tiles: [`${TILE_SERVER_FISHER}/public.fisher_fhe/{z}/{x}/{y}.pbf`],
          'source-layer': 'fisher_fhe',
          'minzoom': 4,
          'maxzoom': 22
        })

        let layer = {
          'id': 'fisher_fhe',
          'type': 'fill',
          'source': 'fisher_fhe',
          'source-layer': 'public.fisher_fhe',
          'layout': {'visibility': 'visible'},
          'paint': {
            'fill-color': 'hsla(294,82%,28%,0.35)',
            'fill-outline-color': [
              'interpolate',
              ['linear'],
              ['zoom'],
              5,
              'hsla(308,64%,29%,0.1)',
              10,
              'hsl(339,100%,15%)'
            ]
          }
        }
        this.map.addLayer(layer);
      }

      loadFisherRange()
      loadFisherFHE()

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
