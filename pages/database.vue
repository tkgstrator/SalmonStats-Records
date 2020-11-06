<template>
  <div class="page oceancalc">
    <header class="navigation-bar">
      <h1>
        <nuxt-link to="/">
          <font-awesome-icon icon="bars" size="lg" class="oceancalc-button" />
        </nuxt-link>
        Database
        <nuxt-link to="/ocean">
          <font-awesome-icon icon="tools" size="lg" class="oceancalc-button" />
        </nuxt-link>
      </h1>
    </header>
    <div class="oceancalc-header">
      <!-- <h2><span>Salmon Run</span></h2> -->
      <h3><span>Enemy Appear Probability</span></h3>
      <table class="oceancalc-table">
        <thead>
          <tr>
            <th>Appear ID</th>
            <th>1</th>
            <th>2</th>
            <th>3</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <th>1st</th>
            <th>22.52%</th>
            <th>38.74%</th>
            <th>38.74%</th>
          </tr>
          <tr>
            <th>Whole time</th>
            <th>24.90%</th>
            <th>34.55%</th>
            <th>37.55%</th>
          </tr>
        </tbody>
      </table>
      <h3><span>Specific Seeds</span></h3>
    </div>
    <div id="content">
      <div class="coop-overfishing-list-wrapper">
        <table class="oceancalc-table">
          <thead>
            <tr>
              <th>Description</th>
              <th>Number of Seeds</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(cycle, index) in seeds" :key="index">
              <td>{{ $t(`${cycle.desc}`) }}</td>
              <td>{{ $t(`${cycle.value}`) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  data: () => ({
    seeds: [
      {
        desc: "All High Tide (No Event)",
        value: 14487007,
      },
      {
        desc: "All Low Tide (No Event)",
        value: 14495708,
      },
      {
        desc: "All High Tide (No Event & Appear ID 2)",
        value: 8555,
      },
      {
        desc: "All High Tide (No Event & Appear ID 3)",
        value: 8298,
      },
      {
        desc: "High Tide Rush (Fix Appear ID)",
        value: 2627,
      },
      {
        desc: "Normal Rush (Fix Appear ID)",
        value: "-",
      },
      {
        desc: "High Tide Goldie Seeking(10+)",
        value: 143,
      },
      {
        desc: "Normal Goldie Seeking(8+)",
        value: 163
      }
    ]
  }),
  created() {
  },
  methods: {
  }
}
</script>

<style lang="scss">
@import "~assets/sass/style.scss";
@import "~assets/sass/splatnet2.scss";
@import "~assets/sass/salmonrecords.scss";
</style>