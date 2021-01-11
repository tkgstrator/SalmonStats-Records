<template>
  <div class="page coop-overfishing">
    <header class="navigation-bar">
      <h1>
        <nuxt-link to="/ocean">
          <font-awesome-icon icon="tools" size="lg" class="oceancalc-button" />
        </nuxt-link>
        Salmon Run Records
      </h1>
    </header>
    <div class="coop-overfishing-header">
      <h2><span>Salmon Run</span></h2>
      <h3><span>LanPlay Records</span></h3>
    </div>
    <div class="coop-overfishing-list-wrapper">
      <div id="coop-overfishing-records"></div>
    </div>
  </div>
</template>

<script>
const BASE_STAGE_URL = "https://app.splatoon2.nintendo.net/images/coop_stage/"
const STAGE_URL = { shakeup: "65c68c6f0641cc5654434b78a6f10b0ad32ccdee.png", shakeship: "e07d73b7d9f0c64e552b34a2e6c29b8564c63388.png", shakehouse: "6d68f5baa75f3a94e5e9bfb89b82e7377e3ecd2c.png", shakelift: "e9f7c7b35e6d46778cd3cbc0d89bd7e1bc3be493.png", shakeride: "50064ec6e97aac91e70df5fc2cfecf61ad8615fd.png" }
const WATER_WORD = { 0: { ja: "干潮", en: "LT" }, 1: { ja: "通常", en: "NT" }, 2: { ja: "満潮", en: "HT" } }
const EVENT_WORD = { 0: { ja: "イベントなし", en: "No Event" }, 1: { ja: "ラッシュ", en: "Rush" }, 2: { ja: "キンシャケ探し", en: "Goldie Seeking" }, 3: { ja: "グリル発進", en: "Griller" }, 4: { ja: "ハコビヤ襲来", en: "Mothership" }, 5: { ja: "霧", en: "Fog" }, 6: { ja: "ドスコイ大量発生", en: "Cohock Charge" } }
const TITLE_WORD = { 0: { ja: "", en: "Total Golden Eggs"}, 1: { ja: "", en: "Total Golden Eggs(No Night)"}}
const STAGE_WORD = { shakeup: { ja: "シェケナダム", en: "Spawning Grounds" }, shakeship: { ja: "難破船ドン・ブラコ", en: "Marooner's Bay" }, shakehouse: { ja: "海上集落シャケト場", en: "Lost Outpost" }, shakelift: { ja: "トキシラズいぶし工房", en: "Salmonid Smokeyard" }, shakeride: { ja: "朽ちた方舟 ポラリス", en: "Ruins of Ark Polaris" } }
const BASE_WEAPON_URL = "https://app.splatoon2.nintendo.net/images/weapon/"
const BASE_COOP_WEAPON_URL = "https://app.splatoon2.nintendo.net/images/coop_weapons/"
const WEAPONS = {
  0: "32d41a5d14de756c3e5a1ee97a9bd8fcb9e69bf5.png",
  10: "91b6666bcbfccc204d86f21222a8db22a27d08d0.png",
  20: "e5a97d52f12a83a037526588363021f2c1f718b0.png",
  30: "c6ab7ebff7af7f7604eb53a12851da880b1ec2c7.png",
  40: "e1d09fc9502a81c82137c8dcd5a872eb872af697.png",
  50: "df04ddaf086cea94491df553a6d2550230a4da3c.png",
  60: "1f2b1db5917ef7a4e62f0e15b8805275e33f2179.png",
  70: "2e2b59379b8f14cfed0600f84590be0ecad707b6.png",
  80: "df90f6065594378690647c23d42440e2de89c99d.png",
  90: "007fb7ed50e76dde495ffb0747421b50dfce8aa3.png",
  200: "3f840ce3cc5ac0b8cbf7451079b57e807d8b95f1.png",
  210: "cfafc8bc42bcd89058fdb22b7b943fb9f893adb8.png",
  220: "109b2b851481510eaacb50afc8ce9fb79b7f20ad.png",
  230: "2b684d81508ca5286060767e29dd81ca38303f43.png",
  240: "72bdcf5f6077bd7149832153034b3f43d16ac461.png",
  250: "8f64580bb033ba86fa0179179cfeb56b5544fda6.png",
  300: "202724be5bb5e59457227d087d7c48a32c01db24.png",
  310: "45e8847cbaf09bdc86c6e6627236286781b09f0f.png",
  400: "b9901d49ef3229d3e62d58fc3e1edc8c48da6873.png",
  1000: "123db7c37066e10e2c437656db2a26f18898e6b6.png",
  1010: "1041dbdd11b3036671148d47c2e0798cecf3dba2.png",
  1020: "3d274190988ad20dd1b02825448edbb6e12c720c.png",
  1030: "e32ed68bb18628c5ede5816a2fbc2b8fcdd04124.png",
  1100: "1f94c29067c918ac9143b756dc607ff0f8cf4e63.png",
  1110: "f1d5740dfb7d87f7e43974bbe5585445368741b8.png",
  2000: "5a0a20324f1374a363363d721a605849e36ffff2.png",
  2010: "1ed94885bef2b0e498ed4dd76bea9064c85cfc94.png",
  2020: "0ec07bb00918f071975b35191e0860152bdcb321.png",
  2030: "a6279990ad871fccdd9f2a64a2951f8726f45c48.png",
  2040: "fd4b89e84b375f01290185f2236dbee935dd1682.png",
  2050: "6ecbbb897d6c59a5c03097216ef4f803366ea6fa.png",
  2060: "26d523e6eee3d57dc6c5f531dfc1747ffd46b8b8.png",
  3000: "3963a3fb1ff8038a42072e913587fc6f9aa00d71.png",
  3010: "ad921a57ab1b7721c50873c082bb34591b61021c.png",
  3020: "27a026e7dec5a068777bb7883f50451aec799d71.png",
  3030: "2835f6d61a4296b4ac3876337884a0c453a4fa4f.png",
  3040: "6f1c2a339db6ec0dccb65704adee2db93c768245.png",
  4000: "2a1c5ca0e68919b4d655bd860cac3b2942b95498.png",
  4010: "6f42c9f8fde07510a01072a669125545f6effb99.png",
  4020: "e34bbd580e49695b97d5fc4464cc901d4fe08ce5.png",
  4030: "f208b6222acb5014ab96285e9b9a3e98039c884b.png",
  4040: "d79b99092aa03dc249b1f767197c1ecbda9d3cd7.png",
  5000: "cc4bc30ff53bf2b45bd5e3dadceb39d52b95761f.png",
  5010: "bb5caf24e43f8c7ceb126670bf24fd3aa9a3c3fc.png",
  5020: "7d6032f0ceee14c4607385b848c6e486b84a2865.png",
  5030: "aaead5ff0b63cdcb989b211d649b2552bb3e3a1b.png",
  5040: "ba750d284eb067abdc995435c3358eed4e6f90fa.png",
  6000: "f1fa6db2e21f32cd1c2cd093ec24f1a450d4650c.png",
  6010: "cdb032aa993f4836580ce4edac06de0138833299.png",
  6020: "15fe3fe6bbec24ddb5fdc3ffd06585bc82440531.png",
  20000: "db39203d81d60a7370d3ae966bc02ed14398366f.png",
  20010: "7d5ff3a57c3c3aaf28217bc3a79e02d665f13ba7.png",
  20020: "95077fe72924bcd64f37cd43aa49a12cd6329a7e.png",
  20030: "c2c0653d3246ea6df2b595c68e907f68eda49b08.png"
}

const url = "https://script.googleusercontent.com/macros/echo?user_content_key=ummdOBdAeKIIvWWalKMFmUeUGjzsB0NVpWdeYai1h1R0eB5u5dAHS3VFk_W8Q0O9IYxjHo5NeMPd7-ER5BG3d_69WarY2r8hm5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnNODCIGpCvTIG_y73l0eN6DXTL7am_LUGn2yZvQU_kJ211U6kHKox2FF9vc0kMk0UwA5oRoKKJbw&lib=MM2j9I9WqXTpiAIT5WzJb5jD0sxkqxnr0"
let keys = ["wave", "shakeup", "shakeship", "shakehouse", "shakelift", "shakeride"]

export default {
  async mounted() {
    const response = await fetch(url)
    let json = await response.json()

    // テーブルを作成する
    var table = document.createElement("table")
    // ヘッダーを作成する
    var tr = document.createElement("tr")
    var thead = document.createElement("thead")

    keys.forEach(key => {
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
    });
    table.appendChild(thead)

    // ステージごとにデータを整形
    let data = []
    for (let id = 0; id <= 4; id++) {
      let value = json.filter(function (item) {
        return item["stage_id"] == id
      })
      data.push(value)
    }

    for (let i = 0; i < 18; i++) {
      var tr = document.createElement("tr")

      // イベント名追加
      var td = document.createElement("th")
      if (data[0][i]["water_level"] != 3) {
        let title = document.createElement("p")
        title.className = "event_type"

        if (data[0][i]["event_type"] == 6)
          title.textContent = EVENT_WORD[data[0][i]["event_type"]]["en"]
        else
          title.textContent = WATER_WORD[data[0][i]["water_level"]]["en"] + " " + EVENT_WORD[data[0][i]["event_type"]]["en"]
        td.appendChild(title)
        // td.appendChild(event)
      }
      tr.appendChild(td)

      if (data[0][i]["water_level"] == 3) {
        let title = document.createElement("p")
        title.className = "title"
        title.textContent = TITLE_WORD[data[0][i]["event_type"]]["en"]
        td.appendChild(title)
      }

      // 各種レコードを載せる
      for (let id = 0; id <= 4; id++) { // idはステージID
        const weapon_list = data[id][i]["weapon_list"].split(",")
        const golden_ikura_num = data[id][i]["golden_ikura_num"]
        const seed = data[id][i]["seed"] // ゲームシード情報（ないかもしれない）
        const link = data[id][i]["movie"] // LanPlayだとリザルト取得できないので多分ある

        var td = document.createElement("td")
        var eggs = document.createElement("p")
        var span = document.createElement("span")

        if (golden_ikura_num >= 0) {
          eggs.className = "eggs"
          span.className = "golden_ikura_num"
          // ここもうちょいかっこよく書きたいよね
          span.textContent = data[id][i]["golden_ikura_num"]
          eggs.appendChild(span)
          td.appendChild(eggs)
          var ul = document.createElement("ul")
          ul.className = "weapons"

          weapon_list.forEach(weapon => {
            var li = document.createElement("li")
            var img = document.createElement("img")
            img.src = BASE_WEAPON_URL + WEAPONS[weapon.trim()]
            li.appendChild(img)
            ul.appendChild(li)
          })
          td.appendChild(ul)
          var links = document.createElement("p")
          var video = document.createElement("a")
          var img = document.createElement("img")
          links.className = "links"
          img.src = "https://gungeespla.github.io/salmon_run_records/assets/img/link-video.png"
          video.href = link
          video.appendChild(img)
          links.appendChild(video)
          td.appendChild(links)
        } else {
          eggs.className = "norecords"
          span.textContent = "-"
          eggs.appendChild(span)
          td.appendChild(eggs)
        }

        tr.appendChild(td)
      }
      table.appendChild(tr)
    }
    document.getElementById("coop-overfishing-records").appendChild(table)
  }
};
</script>

<style lang="scss">
@import "~assets/sass/style.scss";
@import "~assets/sass/splatnet2.scss";
@import "~assets/sass/salmonrecords.scss";
</style>