<script>
import json from "/public/assets/json/records.json"
import weapons from "/public/assets/json/weapons.json"
import style from "/public/assets/sass/style.scss"
import splatnet2 from "/public/assets/sass/splatnet2.scss"
import salmonrecords from "/public/assets/sass/salmonrecords.scss"

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
      // json: json,
      // weapons: weapons
    }
  },
  mounted() {
    const stage = ["wave", "shakeup", "shakeship", "shakehouse", "shakelift", "shakeride"]
    var table = document.createElement("table")
    var tr = document.createElement("tr")
    var thead = document.createElement("thead")
    
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

    // データの表示
    const shiftType = "grizzco"
    const recordType = "golden_eggs"

    STAGE_TYPE.forEach(stageId => {
      const waves = json[stageId][shiftType][recordType]["waves"]
      var tr = document.createElement("tr")
      WATER_TYPE.forEach(waterLevel => {
        EVENT_TYPE.forEach(eventType => {
          const wave = waves.filter(wave => wave["water_level"] == waterLevel && wave["event_type"] == eventType)
          // 記錄がある場合（まあ、ないことはないか）
          if (wave.length != 0) {
            // コンポーネント
            const record = wave[0]
            var td = document.createElement("td")
            // 金イクラか赤イクラの画像
            var eggs = document.createElement("p")
            // 金イクラ数
            var span = document.createElement("span")
            // ブキリスト
            var ul = document.createElement("ul")
            // クラスの設定
            eggs.className = "eggs"
            span.className = "golden_ikura_num"
            ul.className = "weapons"
            
            span.textContent = record["golden_eggs"]
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
            eggs.appendChild(span)
            td.appendChild(eggs)
            td.appendChild(ul)
            tr.appendChild(td)
          }
        })
      })
      table.appendChild(tr)
    })
    document.getElementById("coop-overfishing-records").appendChild(table)
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
    <div class="coop-overfishing-list-wrapper">
      <div id="coop-overfishing-records"></div>
    </div>
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  /* margin-top: 60px; */
}
</style>
