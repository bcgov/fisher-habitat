<template>
  <div id="app">
    <b-navbar toggleable="lg" type="dark" variant="info" fixed>
      <b-navbar-brand href="#/"><img id="logo" alt="BC Government" src="./assets/bc_logo.png" width="200px"></b-navbar-brand>
      <div><a href="#/report">Report</a></div>
    </b-navbar>
    <router-view></router-view>
  </div>
</template>

<script>

export default {
  name: 'FisherHabitat'
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
