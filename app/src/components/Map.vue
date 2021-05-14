<template>
  <div>
    <div id='map'></div>
    <div class="control-box">
      <p>Draw a polygon using the draw tools. &#128513; &#128073; &#128073;</p>
      <div class="save-button">
        <button type="button" class="btn btn-primary" v-on:click="savePollygons">Save All Pollygons</button>
      </div>
    </div>
  </div>
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

      this.draw = new MapboxDraw({
        displayControlsDefault: false,
        controls: {
          polygon: true,
          trash: true
        },
        styles: [
          // line stroke
          {
              "id": "gl-draw-line",
              "type": "line",
              "filter": ["all", ["==", "$type", "LineString"], ["!=", "mode", "static"]],
              "layout": {
                "line-cap": "round",
                "line-join": "round"
              },
              "paint": {
                "line-color": "#FF5733",
                "line-dasharray": [0.2, 2],
                "line-width": 3
              }
          },
          // polygon fill
          {
            "id": "gl-draw-polygon-fill",
            "type": "fill",
            "filter": ["all", ["==", "$type", "Polygon"], ["!=", "mode", "static"]],
            "paint": {
              "fill-color": "#FF5733",
              "fill-outline-color": "#FF5733",
              "fill-opacity": 0.1
            }
          },
          // polygon outline stroke
          // This doesn't style the first edge of the polygon, which uses the line stroke styling instead
          {
            "id": "gl-draw-polygon-stroke-active",
            "type": "line",
            "filter": ["all", ["==", "$type", "Polygon"], ["!=", "mode", "static"]],
            "layout": {
              "line-cap": "round",
              "line-join": "round"
            },
            "paint": {
              "line-color": "#FF5733",
              "line-dasharray": [0.2, 2],
              "line-width": 3
            }
          },
          // vertex point halos
          {
            "id": "gl-draw-polygon-and-line-vertex-halo-active",
            "type": "circle",
            "filter": ["all", ["==", "meta", "vertex"], ["==", "$type", "Point"], ["!=", "mode", "static"]],
            "paint": {
              "circle-radius": 7,
              "circle-color": "#FFF"
            }
          },
          // vertex points
          {
            "id": "gl-draw-polygon-and-line-vertex-active",
            "type": "circle",
            "filter": ["all", ["==", "meta", "vertex"], ["==", "$type", "Point"], ["!=", "mode", "static"]],
            "paint": {
              "circle-radius": 5,
              "circle-color": "#FF5733",
            }
          },
          // midpoint halos
          {
            "id": "gl-draw-polygon-and-line-midpoint-halo-active",
            "type": "circle",
            "filter": ["all", ["==", "meta", "midpoint"], ["==", "$type", "Point"], ["!=", "mode", "static"]],
            "paint": {
              "circle-radius": 6,
              "circle-color": "#FFF"
            }
          },
          // midpoint points
          {
            "id": "gl-draw-polygon-and-line-midpoint-active",
            "type": "circle",
            "filter": ["all", ["==", "meta", "midpoint"], ["==", "$type", "Point"], ["!=", "mode", "static"]],
            "paint": {
              "circle-radius": 4,
              "circle-color": "#FF5733",
            }
          },

          // INACTIVE (static, already drawn)
          // line stroke
          {
              "id": "gl-draw-line-static",
              "type": "line",
              "filter": ["all", ["==", "$type", "LineString"], ["==", "mode", "static"]],
              "layout": {
                "line-cap": "round",
                "line-join": "round"
              },
              "paint": {
                "line-color": "#000",
                "line-width": 3
              }
          },
          // polygon fill
          {
            "id": "gl-draw-polygon-fill-static",
            "type": "fill",
            "filter": ["all", ["==", "$type", "Polygon"], ["==", "mode", "static"]],
            "paint": {
              "fill-color": "#000",
              "fill-outline-color": "#000",
              "fill-opacity": 0.1
            }
          },
          // polygon outline
          {
            "id": "gl-draw-polygon-stroke-static",
            "type": "line",
            "filter": ["all", ["==", "$type", "Polygon"], ["==", "mode", "static"]],
            "layout": {
              "line-cap": "round",
              "line-join": "round"
            },
            "paint": {
              "line-color": "#000",
              "line-width": 3
            }
          }
        ],
      });

      this.map.addControl(this.draw);
    },
    savePollygons: function () {
      console.log(this.draw.getAll());
    }

  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  #map {position: absolute; top: 80px; right: 0; bottom: 0; left: 0;}
  .save-button {
    text-align: left;
    padding: 20px;
  }
  .control-box {
    height: 125px;
    width: 450px;
    position: absolute;
    top: 100px;
    right: 60px;
    background-color: rgba(255, 255, 255, 0.8);
    padding: 15px;
  }

  p {
    text-align: left;
    padding-left: 20px;
    font-family: 'Open Sans';
    margin: 0;
    font-size: 20px;
  }

</style>
