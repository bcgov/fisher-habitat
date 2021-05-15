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
          <button :disabled="!file" type="button" class="btn btn-primary" v-on:click="uploadFile">Upload File</button>
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
      habitatInfo: null,
      file: null,
      activeLayers: []
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

      const resetOnDrawUpdate = () => {
        this.resetShapes()
        this.habitatInfo = null
      }

      this.map.on('draw.delete', resetOnDrawUpdate)
      this.map.on('draw.create', resetOnDrawUpdate)
      this.map.on('draw.update', resetOnDrawUpdate)

      this.map.on('load', () => {
        this.loadLayers()
      })

      this.map.on('click', 'fisher_range', (e) => {
        let f = this.map.queryRenderedFeatures(e.point, { layers: this.activeLayers })
        if (f.length) {
          return
        }
        
        console.log(this.draw.getMode())
        if (this.draw.getMode() === 'draw_polygon') {
          return
        }

        new maplibregl.Popup()
        .setLngLat(e.lngLat)
        .setHTML(this.popupHTML(e))
        .addTo(this.map)
      })
    },

    generateReport: function () {
      console.log('update report:');
      this.resetShapes()
      console.log(this.draw.getAll());
      
      axios.post(`${API_BASE_URL}/v1/process_drawing`,  { shape: JSON.stringify(this.draw.getAll())})
      .then(response => {
        this.habitatInfo = response.data
        this.addLayer('yellow-warnings', response.data.yellow_polygons, '#e1ad01', true)
        this.addLayer('red-warnings', response.data.red_polygons, 'red', true)
      })
    },

    harvestImpactPopup (e) {
        var coordinates = e.lngLat
        var description = e.features[0].properties.harvest_im
        
        while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
        coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360
        }
        
        new maplibregl.Popup()
        .setLngLat(coordinates)
        .setHTML(description)
        .addTo(this.map)
    },
    harvestImpactHoverOn () {
      this.map.getCanvas().style.cursor = 'pointer'
    },
    harvestImpactHoverOff () {
      this.map.getCanvas().style.cursor = ''
    },
    addLayer (id, geojson, color="#0080ff", createPopup=false) {
      this.map.addSource(id, {
          type: 'geojson',
          data: geojson
        })

        // Add a new layer to visualize the polygon.
      this.map.addLayer({
        'id': id,
        'type': 'fill',
        'source': id, // reference the data source
        'layout': {},
        'paint': {
        'fill-color': color, // blue color fill
        'fill-opacity': 0.5
        }
      })
        // Add a black outline around the polygon.
      this.map.addLayer({
        'id': `${id}outline`,
        'type': 'line',
        'source': id,
        'layout': {},
        'paint': {
          'line-color': '#000',
          'line-width': 1
        }
      })

      this.activeLayers.push(id)

      if (createPopup) {

        this.map.on('click', id, this.harvestImpactPopup)
        
        // Change the cursor to a pointer when the mouse is over the places layer.
        this.map.on('mouseenter', id, () => this.harvestImpactHoverOn);
        
        // Change it back to a pointer when it leaves.
        this.map.on('mouseleave', id, () => this.harvestImpactHoverOff);
      }

    },

    removeLayer (id) {
      this.map.removeLayer(id)
      this.map.removeLayer(`${id}outline`)
      this.map.removeSource(id)
      if (['yellow-warnings', 'red-warnings'].includes(id)) {
        this.map.off('click', id, this.harvestImpactPopup)
        this.map.off('mouseenter', id, this.harvestImpactHoverOn)
        this.map.off('mouseleave', id, this.harvestImpactHoverOff)
      }

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
            'fill-color': 'hsla(220,82%,28%,0.15)',
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
            'fill-color': 'hsla(294,82%,28%,0.10)',
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
    this.resetShapes()
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
        this.habitatInfo = response.data
        this.addLayer('yellow-warnings', response.data.yellow_polygons, '#e1ad01', true)
        this.addLayer('red-warnings', response.data.red_polygons, 'red', true)
      })
    },
    resetShapes() {
        let mapLayer = this.map.getLayer('cutblock')
        if(typeof mapLayer !== 'undefined') {
          // Remove map layer & source.
          this.removeLayer('cutblock')
        }

        mapLayer = this.map.getLayer('yellow-warnings')
        if(typeof mapLayer !== 'undefined') {
          // Remove map layer & source.
          this.removeLayer('yellow-warnings')
        }

        mapLayer = this.map.getLayer('red-warnings')
        if(typeof mapLayer !== 'undefined') {
          // Remove map layer & source.
          this.removeLayer('red-warnings')
        }
        this.activeLayers = []
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
