<template>
  <div>
    <div id='map'></div>
    <div class="report">
      <Report :habitatInfo="habitatInfo"></Report>

      <div class="save-button">
        <button type="button" class="btn btn-primary" v-on:click="generateReport">Generate Report</button>
      </div>

        <div class="file-up">
          <div>Upload Cut Block ZIP File:</div>
          <!-- Plain mode -->
          <b-form-file v-model="file" class="mt-3" plain></b-form-file>
        </div>

        <div class="save-button">
          <button type="button" class="btn btn-primary" v-on:click="uploadFile">Upload File</button>
        </div>
    </div>
  </div>
</template>

<script>
import maplibregl from 'maplibre-gl'; // or "const maplibregl = require('maplibre-gl');"
import MapboxDraw from '@mapbox/mapbox-gl-draw';

import { TILE_SERVER_FISHER } from "../consts"
import Report from "./Report";
import axios from 'axios';
import {API_BASE_URL} from '../consts'

export default {
  name: 'Map',
  components: {Report},
  mounted() {
    this.createMap()
  },
  data () {
    return {
      file: null,
      habitatInfo: null
    }
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
        [-140.06, 47.30], // [west, south]
        [-113.03, 61.00]  // [east, north]
      ];

      // Set the map's max bounds.
      this.map.setMaxBounds(bounds);

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

      this.map.on('load', () => {
        this.loadLayers()
      })

      this.map.on('click', 'fisher_range', (e) => {
        new maplibregl.Popup()
        .setLngLat(e.lngLat)
        .setHTML(this.popupHTML(e))
        .addTo(this.map)
      })
    },

    generateReport: function () {
      const drawnCutblock = this.draw.getAll();
      axios.post(`${API_BASE_URL}/v1/process_drawing`,  { shape: JSON.stringify(drawnCutblock)})
      .then(response => {
        this.updateCutBlockLayers(response.data);
        this.habitatInfo = response.data
      })
    },
    loadLayers: function () {

      const loadCutBlock = () => { 
        this.map.addSource("cutblock", { type:'geojson', data: {"type": "FeatureCollection", "features": []}});
        this.map.addSource("yellow_polygons", { type:'geojson', data: {"type": "FeatureCollection", "features": []}});
        this.map.addSource("red_polygons", { type:'geojson', data: {"type": "FeatureCollection", "features": []}});

        this.map.addLayer({
          'id': "yellow_polygons",
          'type': 'fill',
          'source': "yellow_polygons",
          'layout': {},
          'paint': {
            'fill-color': '#fffe00',
            'fill-opacity': 0.5
          }
        });

        this.map.addLayer({
          'id': "red_polygons",
          'type': 'fill',
          'source': "red_polygons",
          'layout': {},
          'paint': {
            'fill-color': '#ff0000',
            'fill-opacity': 0.5
          }
        });

        // Add a black outline around the polygon.
        this.map.addLayer({
          'id': "cutblock",
          'type': 'line',
          'source': "cutblock",
          'layout': {},
          'paint': {
            'line-color': '#000',
            'line-width': 2
          }
        });
      }

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
      loadCutBlock()
    },
    popupHTML: function(info) {

     return `<div class="popup">
        <div><strong>FISHER RANGE</strong></div>
        <div><span><strong>BCSEE Repo:</strong></span><span>  <a href="${info.features[0].properties['bcsee_repo']}" target="_blank">Link</a></span></div>
        <div><span><strong>eng_name:</strong></span><span>  ${info.features[0].properties['eng_name']}</span></div>
        <div><span><strong>bgc:</strong></span><span>  ${info.features[0].properties['bgc']}</span></div>
        <div><span><strong>ecosecti_1:</strong></span><span>  ${info.features[0].properties['ecosecti_1']}</span></div>
        <div><span><strong>ecosecti_2:</strong></span><span>  ${info.features[0].properties['ecosecti_2']}</span></div>
        <div><span><strong>ecosection:</strong></span><span>  ${info.features[0].properties['ecosection']}</span></div>
        <div><span><strong>elcode:</strong></span><span>  ${info.features[0].properties['elcode']}</span></div>
        <div><span><strong>element_su:</strong></span><span>  ${info.features[0].properties['element_su']}</span></div>
        <div><span><strong>parent_eco:</strong></span><span>  ${info.features[0].properties['parent_eco']}</span></div>
        <div><span><strong>presence_1:</strong></span><span>  ${info.features[0].properties['presence_1']}</span></div>
        <div><span><strong>presence_c:</strong></span><span>  ${info.features[0].properties['presence_c']}</span></div>
        <div><span><strong>sci_name:</strong></span><span>  ${info.features[0].properties['sci_name']}</span></div>
        <div><span><strong>Shape Area:</strong></span><span>  ${info.features[0].properties['shape_area']}</span></div>
        <div><span><strong>shape_leng:</strong></span><span>  ${info.features[0].properties['shape_leng']}</span></div>
     </div>`
    },

    uploadFile: function () {
    let formData = new FormData();
    formData.append('shape', this.file);
    axios.post(`${API_BASE_URL}/v1/process_file`, 
      formData,
             {
              headers: {
                  'Content-Type': 'multipart/form-data'
              }
            }
       )
      .then(response => {
        this.updateCutBlockLayers(response.data);
        this.habitatInfo = response.data;
      })
    },
    updateCutBlockLayers: function(data) {
      this.map.getSource('cutblock').setData(data.cutblock);
      this.map.getSource('yellow_polygons').setData(data.yellow_polygons);
      this.map.getSource('red_polygons').setData(data.red_polygons);
    }
  }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

  .file-up {
    text-align: left;
    padding-top: 20px;
    padding-bottom: 20px;
  }
  .save-button {
    text-align: left;
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
  .report {
    height: 125px;
    width: calc(100vw - 70%);
    position: absolute;
    top: 80px;
    left: 0px;
    background-color: rgba(255, 255, 255, 0.8);
    padding: 15px;
  }

  p {
    text-align: left;
    margin: 0;
    font-size: 20px;
  }

  .mapboxgl-popup {
    max-width: 400px;
    font: 12px/20px 'Helvetica Neue', Arial, Helvetica, sans-serif;
  }


#map {
  position: absolute;
  top: 80px;
  right: 0;
  bottom: 0;
  left: calc(100vw - 70%);
}
</style>
