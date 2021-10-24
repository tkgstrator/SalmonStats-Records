<script>
import json from "./assets/json/records.json"
import weapons from "./assets/json/weapons.json"

const BASE_STAGE_URL = "https://app.splatoon2.nintendo.net/images/coop_stage/"
const STAGE_URL = { 
  shakeup: "65c68c6f0641cc5654434b78a6f10b0ad32ccdee.png",
  shakeship: "e07d73b7d9f0c64e552b34a2e6c29b8564c63388.png",
  shakehouse: "6d68f5baa75f3a94e5e9bfb89b82e7377e3ecd2c.png",
  shakelift: "e9f7c7b35e6d46778cd3cbc0d89bd7e1bc3be493.png",
  shakeride: "50064ec6e97aac91e70df5fc2cfecf61ad8615fd.png"
  }
const STAGE_TYPE = [
  5000,
  5001,
  5002,
  5003,
  5004
]
const SHIFT_TYPE = [
  "normal",
  "random1",
  "random4",
  "grizzco"
]
const RECORD_TYPE = [
  "power_eggs",
  "golden_eggs"
]
const EVENT_TYPE = [
  "-",
  "rush",
  "goldie-seeking",
  "griller",
  "the-mothership",
  "fog",
  "cohock-charge"
]
const WATER_TYPE = [
  "low",
  "normal",
  "high"
]
const WATER_WORD = { 0: { ja: "干潮", en: "LT" }, 1: { ja: "通常", en: "NT" }, 2: { ja: "満潮", en: "HT" } }
const EVENT_WORD = { 0: { ja: "イベントなし", en: "No Event" }, 1: { ja: "ラッシュ", en: "Rush" }, 2: { ja: "キンシャケ探し", en: "Goldie Seeking" }, 3: { ja: "グリル発進", en: "Griller" }, 4: { ja: "ハコビヤ襲来", en: "Mothership" }, 5: { ja: "霧", en: "Fog" }, 6: { ja: "ドスコイ大量発生", en: "Cohock Charge" } }
const TITLE_WORD = { 0: { ja: "", en: "Total Golden Eggs"}, 1: { ja: "", en: "Total Golden Eggs(No Night)"}}
const STAGE_WORD = { shakeup: { ja: "シェケナダム", en: "Spawning Grounds" }, shakeship: { ja: "難破船ドン・ブラコ", en: "Marooner's Bay" }, shakehouse: { ja: "海上集落シャケト場", en: "Lost Outpost" }, shakelift: { ja: "トキシラズいぶし工房", en: "Salmonid Smokeyard" }, shakeride: { ja: "朽ちた方舟 ポラリス", en: "Ruins of Ark Polaris" } }
const BASE_WEAPON_URL = "https://app.splatoon2.nintendo.net/images/weapon/"
const BASE_COOP_WEAPON_URL = "https://app.splatoon2.nintendo.net/images/coop_weapons/"

export default {
  methods: {
  },
    data() {
    return {
      shiftType: 0,
      recordType: 0
    }
  },
  methods: {
    getWaveInfo(waterLevel, eventType) {
      switch (waterLevel) {
        case "low":
          waterLevel = "LT"
          break
        case "normal":
          waterLevel = "NT"
          break
        case "high":
          waterLevel = "HT"
          break
      }
      switch (eventType) {
        case "-":
          eventType = "-"
          break
        case "rush":
          eventType = "Rush"
          break
        case "goldie-seeking":
          eventType = "Goldie Seeking"
          break
        case "griller":
          eventType = "Griller"
          break
        case "the-mothership":
          eventType = "The mothership"
          break
        case "fog":
          eventType = "Fog"
          break
        case "cohock-charge":
          eventType = "Cohock Charge"
          break
      }
      return `${waterLevel} ${eventType}`
    },
    generate() {
      const el = document.getElementById("salmonstats-record")
      if (el != null) {
        el.remove()
      }
      let shiftType = "normal"
      let recordType = "golden_eggs"

      switch (this.shiftType) {
        case 0:
          shiftType = "normal" 
          break
        case 1:
          shiftType = "random1" 
          break
        case 2:
          shiftType = "random4" 
          break
        case 3:
          shiftType = "grizzco" 
          break
      }
      switch (this.recordType) {
        case 0:
          recordType = "power_eggs" 
          break
        case 1:
          recordType = "golden_eggs" 
          break
      }
    const stage = ["wave", "shakeup", "shakeship", "shakehouse", "shakelift", "shakeride"]
    var table = document.createElement("table")
    var tbody = document.createElement("tbody")
    var thead = document.createElement("thead")

    table.id = "salmonstats-record"
    
    stage.forEach(key => {
      var th = document.createElement("th")
      if (key != "wave") {
        var img = document.createElement("img")
        var name = document.createElement("p")
        img.src = BASE_STAGE_URL + STAGE_URL[key]
        name.textContent = STAGE_WORD[key]["en"]
        th.appendChild(img)
        th.appendChild(name)
      }
      thead.appendChild(th)
    })
    table.appendChild(thead)

    EVENT_TYPE.forEach(eventType => {
      WATER_TYPE.forEach(waterLevel => {
        // 存在する組み合わせかどうか
        if (!((waterLevel == "low" && eventType == "rush") || (waterLevel == "low" && eventType == "goldie-seeking") || (waterLevel == "low" && eventType == "griller") || (waterLevel != "low" && eventType == "cohock-charge"))) {
        // if (true) {
          var tr = document.createElement("tr")
          // WAVE情報
          var td = document.createElement("th")
          var span = document.createElement("span")
          span.textContent = this.getWaveInfo(waterLevel, eventType)
          td.appendChild(span)
          tr.appendChild(td)
          
          // 記錄作成
          STAGE_TYPE.forEach(stageId => {
            // コンポーネント
            var td = document.createElement("td")
            var eggs = document.createElement("p")
            var span = document.createElement("span")
            var recordTime = document.createElement("p")
            var ul = document.createElement("ul")

            const waves = json[stageId][shiftType][recordType]["waves"]
            const wave = waves.filter(wave => wave["water_level"] == waterLevel && wave["event_type"] == eventType)

            // 存在する組み合わせかどうか
            // 記錄がある場合（まあ、ないことはないか）
            if (wave.length != 0) {
              // コンポーネント
              const record = wave[0]
              const dateTime = new Date(record["start_time"] * 1000)
              // console.log(dateTime.toLocaleDateString())
              recordTime.textContent = dateTime.toLocaleDateString()
              recordTime.className = "play_time"
              switch (this.recordType) {
                case 0:
                  eggs.className = "power_eggs"
                  span.className = "power_ikura_num"
                  span.textContent = record["ikura_num"]
                  break
                case 1:
                  eggs.className = "golden_eggs"
                  span.className = "golden_ikura_num"
                  span.textContent = record["golden_ikura_num"]
                  break
              }
              ul.className = "weapons"

              // ブキを追加
              record["weapon_list"].forEach(weaponId => {
                var li = document.createElement("li")
                var img = document.createElement("img")
                if (weaponId >= 0) {
                  img.src = BASE_WEAPON_URL + weapons[weaponId]
                } else {
                  img.src = BASE_COOP_WEAPON_URL + weapons[weaponId]
                }
                li.appendChild(img)
                ul.appendChild(li)
              })
              // コンポーネントを整理
              eggs.appendChild(span)
              td.appendChild(eggs)
              td.appendChild(recordTime)
              td.appendChild(ul)
              tr.appendChild(td)
            }
          })
          tbody.appendChild(tr)
        }
      })
    })
    table.appendChild(tbody)
    document.getElementById("coop-overfishing-records").appendChild(table)
    }
  },
  mounted() {
    this.generate(0)
  },
  watch: {
    shiftType: {
      handler: function (newValue, oldValue) {
        this.generate()
      }
    },
    recordType: {
      handler: function (newValue, oldValue) {
        this.generate()
      }
    },
  }
}
</script>

<template>
  <div class="page coop-overfishing">
    <header class="navigation-bar">
      <h1>
        <nuxt-link to="/ocean">
          <font-awesome-icon icon="tools" size="lg" class="oceancalc-button" />
        </nuxt-link>
        Salmon Stats Records
      </h1>
    </header>
    <div class="coop-overfishing-header">
      <h2><span>Salmon Run</span></h2>
      <h3><span>Salmon Stats Records</span></h3>
    </div>
    <div id="content">
     <div class="input-control">
       <div>
      <ul class="oceancalc-option">
        <template v-for="(name, index) in ['Normal', 'Random 1', 'Random 4', 'Grizzco']">
        <li @click="this.shiftType=index">
          <input type="radio" :checked="index==this.shiftType">
          <label>{{ name }}</label>
          </li>
          </template>
      </ul>
       </div>
       <div>
      <ul class="oceancalc-option">
        <template v-for="(name, index) in ['Power Eggs', 'Golden Eggs']">
        <li @click="this.recordType=index">
          <input type="radio" :checked="index==this.recordType">
          <label>{{ name }}</label>
          </li>
          </template>
      </ul>
      </div>
     </div>
     </div>
    <div class="coop-overfishing-list-wrapper">
      <div id="coop-overfishing-records"></div>
    </div>
  </div>
</template>

<style lang="scss">
</style>