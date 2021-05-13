<template>
  <div id="app">
    <b-navbar toggleable="lg" type="dark" variant="info" fixed>
      <b-navbar-brand href="#"><img id="logo" alt="BC Government" src="./assets/bc_logo.png" width="200px"></b-navbar-brand>
    </b-navbar>
    <Map/>
  </div>
</template>

<script>
import Map from './components/Map.vue'

export default {
  name: 'FisherHabitat',
  components: {
    Map
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #234075;
}

#logo{
  margin-left: 20px;
}

#app .bg-info {
  background-color: #234075 !important;
}


</style>
