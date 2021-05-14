<template>
  <!-- TODO: Improve layout. Populate with actual data.  -->
  <div id='report'>
        <h1>Fisher Habitat Retention Guidance</h1>
        
        <hr>

        <div><b>Forest License: </b>A93054</div>
        <div><b>Cutting Permit: </b>93054</div>
        <div><b>Analysis Date: </b>2021-05-14</div>
        <div><b>Retention Spatial Data Version: </b>210215</div>

        <br>

        <h2>Summary Table</h2>

        <div><b>Proposed Cutblock Area (ha): </b>{{shapeArea}}</div>
        <br>

        <div><b>Harvest Impact Warning: </b>{{harvestImpactWarning}}</div>
        <br>

        <div><b>Denning Habitat</b></div>
        <div><b>Acb >52 cm dbh or At >40 cm dbh: </b>{{denningPrimary}}</div>
        <div><b>Contigency: next-largest diameter Acb or At: </b>{{denningContingency}}</div> 
        <br>

        <div><b>Branch Resting Habitat</b></div>
        <div><b>Sw >31 cm dbh or Sb >17 cm dbh with rust brooms: </b>{{branchRestingPrimary}}</div>
        <div><b>Contigency: next-largest diameter Sw or any Sw with rust broom infection: </b>{{branchRestingContingency}}</div>
        <br>

        <div><b>Cavity Resting Habitat</b></div>
        <!-- TODO: If values are 0, render: <div>No retention needed for this habitat feature.</div> -->
        <!-- TODO: What is the correct text here? -->
        <div><b>???: </b>{{cavityRestingPrimary}}</div>
        <div><b>Contigency: ???: </b>{{cavityRestingContingency}}</div>
        <br>

        <div><b>Coarse Woody Debris Resting Habitat</b></div>
        <div><b>Retention: </b><small>hard logs >35 cm diameter, >7 m in length, and elevated 25-50 cm above ground. If trees >35 cm do not occur in the harvest area (i.e., in cruise data), 2 or more smaller trees totalling >35 cm diameter may be placed alongside each other and elevated 25-50 cm above ground.</small> <b>{{debrisRestingPieces}}</b></div>
        <div><b>Creation: </b><small>piles that are at least 3m x 5m and 2m high built with logs >10 cm diam. (no tops or fines), jumbled like pick-up sticks, with 1/3 of logs >20 cm diam. and >3 m long</small> <b>{{debrisRestingPiles}}</b></div>
        <br>

        <!-- TODO: How to render each warning/caution area? -->
        <div><b>Warning Areas</b></div>
        <div>???</div>
        <br>

  </div>
</template>

<script>
export default {
  name: "Report",
  data: function() {
    return {
      shapeArea: 244.4,
      harvestImpactWarning: false,
      denningPrimary: 1650,
      denningContingency: 6599,
      branchRestingPrimary: 55,
      branchRestingContingency:221,
      cavityRestingPrimary: 0,
      cavityRestingContingency: 0,
      debrisRestingPieces: 342,
      debrisRestingPiles: 99,
      cautions: [],
      warnings: []
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#report {
  text-align: left;
}
</style>
