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
const WATER_WORD = { 0: { ja: "", en: "Low tide" }, 1: { ja: "", en: "Normal" }, 2: { ja: "", en: "High tide" } }
const EVENT_WORD = { 0: { ja: "", en: "No Event" }, 1: { ja: "", en: "Rush" }, 2: { ja: "", en: "Goldie Seeking" }, 3: { ja: "", en: "Griller" }, 4: { ja: "", en: "The Mothership" }, 5: { ja: "", en: "Fog" }, 6: { ja: "", en: "Cohock Charge" } }
const STAGE_WORD = { shakeup: { ja: "", en: "Spawning Grounds" }, shakeship: { ja: "", en: "Marooner's Bay" }, shakehouse: { ja: "", en: "Lost Outpost" }, shakelift: { ja: "", en: "Salmonid Smokeyard" }, shakeride: { ja: "", en: "Ruins of Ark Polaris" } }
const BASE_WEAPON_URL = "https://app.splatoon2.nintendo.net/images/weapon/"
const BASE_COOP_WEAPON_URL = "https://app.splatoon2.nintendo.net/images/coop_weapons/"
const WEAPONS = {
  0: "32d41a5d14de756c3e5a1ee97a9bd8fcb9e69bf5.png",
  10: "91b6666bcbfccc204d86f21222a8db22a27d08d0.png",
  20: "e5a97d52f12a83a037526588363021f2c1f718b0.png",
  30: "c6ab7ebff7af7f7604eb53a12851da880b1ec2c7.png",
  40: "e1d09fc9502a81c82137c8dcd5a872eb872af697.png",
  50: "df04ddaf086cea94491df553a6d2550230a4da3c.png",
  200: "3f840ce3cc5ac0b8cbf7451079b57e807d8b95f1.png",
  230: "2b684d81508ca5286060767e29dd81ca38303f43.png",
  1020: "3d274190988ad20dd1b02825448edbb6e12c720c.png",
  1110: "f1d5740dfb7d87f7e43974bbe5585445368741b8.png",
  2010: "1ed94885bef2b0e498ed4dd76bea9064c85cfc94.png",
  4030: "f208b6222acb5014ab96285e9b9a3e98039c884b.png",
  5000: "cc4bc30ff53bf2b45bd5e3dadceb39d52b95761f.png",
  5010: "bb5caf24e43f8c7ceb126670bf24fd3aa9a3c3fc.png",
  5020: "7d6032f0ceee14c4607385b848c6e486b84a2865.png",
  5030: "aaead5ff0b63cdcb989b211d649b2552bb3e3a1b.png",
  5040: "ba750d284eb067abdc995435c3358eed4e6f90fa.png",
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
      var td = document.createElement("td")
      if (data[0][i]["water_level"] != 3) {
        let water = document.createElement("p")
        let event = document.createElement("p")
        water.className = "water_level"
        event.className = "event_type"

        water.textContent = WATER_WORD[data[0][i]["water_level"]]["en"]
        event.textContent = EVENT_WORD[data[0][i]["event_type"]]["en"]
        td.appendChild(water)
        td.appendChild(event)
      }
      tr.appendChild(td)

      // 各種レコードを載せる
      for (let id = 0; id <= 4; id++) {
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
@font-face {
  font-family: "SplatFont";
  src: url("~@/assets/fonts/Splatfont.woff") format("woff"),
    url("~@/assets/fonts/Splatfont.woff2") format("woff2");
}
@font-face {
  font-family: "SplatFont2";
  src: url("~@/assets/fonts/Splatfont2.woff") format("woff"),
    url("~@/assets/fonts/Splatfont2.woff2") format("woff2");
}

div {
  font-family: "Splatfont";
  display: block;

  .page {
    min-height: 100%;
    box-sizing: border-box;
  }

  .coop-overfishing {
    position: relative;
    background-image: url(https://app.splatoon2.nintendo.net/images/bundled/8c15ceb605300fbc22963fabcb09fb22.png);
    background-size: 255px 127px;
    background-repeat: repeat;
    overflow: hidden;
    width: 100%;

    .navigation-bar {
      display: flex;
      flex-wrap: nowrap;
      position: relative;
      background-image: url(https://app.splatoon2.nintendo.net/images/bundled/26c8c0b675f643f384991434574baf71.png);
      background-size: 80px 80px;
      color: #fff;
      line-height: 48px;
      min-height: 48px;
      font-family: "Splatfont";
      z-index: 1000;

      & h1 {
        text-align: center;
        font-size: 18px;
        padding: 0 16px;
        flex-grow: 1;
        text-overflow: ellipsis;
        white-space: nowrap;
        overflow: hidden;
      }
    }
  }

  .coop-overfishing-header {
    position: relative;
    text-align: center;
    padding: 16px 0 30px;

    h3 {
      font-family: "Splatfont";
      min-width: 200px;
      background-position-x: 50%;
      background-position-y: center;
      box-sizing: border-box;
      color: #ff5033;

      span {
        padding-top: 12px;
        min-width: 200px;
        background-position: 50%;
        box-sizing: border-box;
        display: inline-block;
        background-image: url("https://app.splatoon2.nintendo.net/images/bundled/cc7454b6eb6b8e16852ed21f00e0fd40.png");
        background-size: 488px 52px;
        height: 52px;
        vertical-align: middle;
      }

      &::before {
        background-position: 0px center;
        width: 42px;
        content: "";
        display: inline-block;
        background-image: url("https://app.splatoon2.nintendo.net/images/bundled/cc7454b6eb6b8e16852ed21f00e0fd40.png");
        background-size: 488px 52px;
        height: 52px;
        vertical-align: middle;
      }

      &::after {
        background-position: 100% center;
        width: 42px;
        content: "";
        display: inline-block;
        background-size: 488px 52px;
        background-image: url("https://app.splatoon2.nintendo.net/images/bundled/cc7454b6eb6b8e16852ed21f00e0fd40.png");
        height: 52px;
        vertical-align: middle;
      }
    }

    h2 {
      position: relative;
      background-image: url("https://app.splatoon2.nintendo.net/images/bundled/a185b309f5cdad94942849070de04ce2.png");
      background-size: contain;
      width: 332px;
      margin: 0 auto;
      height: 112.5px;
      z-index: 1;

      & span {
        display: none;
      }
    }

    h3 {
      min-width: 200px;
      background-position-x: 50%;
      background-position-y: center;
      box-sizing: border-box;
      color: #ff5033;
    }
  }

  .coop-overfishing-list-wrapper {
    position: relative;
    background: #150909;
    padding-top: 16px;
    padding-bottom: 90px;
    padding-bottom: calc(constant(safe-area-inset-bottom) + 90px);
    padding-bottom: calc(env(safe-area-inset-bottom) + 90px);
    z-index: 1;

    &::before {
      // background: url(https://app.splatoon2.nintendo.net/images/bundled/b24ee02521f18ebe1bf8b05e1396c3dc.png);
      background: #150909;
      content: "";
      position: absolute;
      width: 100%;
      height: 20px;
      margin-top: -36px;
      left: 0;
      -webkit-mask-image: url("~static/3ff65812f7fc0aff176df4c78172691c.png");
      // mask-image: url(https://app.splatoon2.nintendo.net/images/bundled/3ff65812f7fc0aff176df4c78172691c.png);
      -webkit-mask-repeat: no-repeat;
      mask-repeat: no-repeat;
      -webkit-mask-size: 100% 100%;
      mask-size: 100% 100%;
    }
  }

  #coop-overfishing-records {
    table {
      font-family: "Splatfont2";
      // table-layout: auto;
      table-layout: fixed;
      width: 100%;
      max-width: 1200px;
      // text-align: center;
      background: #150909;
      // border-collapse: collapse;

      background-size: 40px 40px;
      padding: 0 4px;
      margin: 0 auto;
      margin-bottom: 24px;
      color: #fff;
    }

    thead {
      th {
        img {
          object-fit: scale-down;
          width: 100%;
          max-width: 12em;
          border-radius: 0.5em;
        }
      }

      p {
        font-size: 1.2em;
      }
    }

    td {
      display: float;
      background: rgba(255, 255, 255, 0.1);
      background-image: url(https://app.splatoon2.nintendo.net/images/bundled/b24ee02521f18ebe1bf8b05e1396c3dc.png);
      background-size: 40px 40px;
      border-radius: 0.5em;
      padding: 0.3em;
      border: 0.1em solid #150604;
      // height: 60px;
      vertical-align: middle;
      text-align: center;
      // width: 100px;

      &::before {
        white-space: pre;
      }
    }

    .eggs {
      font-size: 125%;
      color: yellow;
      text-shadow: 0.15em 0.15em 0 #000;

      &::before {
        display: inline-block;
        content: "";
        background: url(https://app.splatoon2.nintendo.net/images/bundled/3aa6fb4ec1534196ede450667c1183dc.png)
          50% no-repeat;
        background-repeat: no-repeat;
        background-position: 50%;
        background-size: contain;
        width: 1.2em;
        height: 1em;
        vertical-align: middle;
        margin-top: -0.1em;
        filter: drop-shadow(0.15em 0.15em 0 #000);
      }
    }

    .norecords {
      font-size: 125%;
      color: yellow;
      text-shadow: 0.15em 0.15em 0 #000;
    }

    .golden_ikura_num {
      &::before {
        content: "X";
        font-size: 0.6em;
        margin: 0 0.1em;
      }
    }

    ul {
      margin: 0;
      padding: 0;
    }

    .weapons {
      display: flex;
      width: 100%;
      list-style-type: none;
      justify-content: center;
      cursor: pointer;

      li {
        background: #000;
        width: 2em;
        height: 2em;
        border-radius: 1em;
      }

      li:not(:last-child) {
        margin-right: 0.2em;
      }

      img {
        width: 2em;
      }
    }

    @media (max-width: 1020px) {
      thead {
        p {
          display: none;
        }
      }
      .weapons {
        display: none;
      }
    }

    .links {
      img {
        width: 1.8em;
      }
    }
  }

  .coop-overfishing-title {
    text-align: center;
  }

  a {
    text-decoration: none;
    color: #ddd;
  }

  .oceancalc-button {
    cursor: pointer;
  }
}
</style>