<template>
  <div class="page oceancalc">
    <header class="navigation-bar">
      <h1>Ocean Calc</h1>
    </header>
    <div class="oceancalc-header">
      <h2><span>Salmon Run</span></h2>
      <!-- <h3><span>LanPlay Records</span></h3> -->
    </div>
    <div id="content">
      <div class="input-control">
      <label>{{ $t(`initialseed`)}} {{ $t(`hex`)}}</label>
      <input class="oceancalc-input-seed" @input="validate" v-model="mInputSeed" maxlength="8">
      </div>
      <ul class="oceancalc-option">
        <template v-for="(name, idx) in ['shakeup', 'shakeship', 'shakehouse', 'shakelift', 'shakeride']">
        <li @click="stage=idx" :key="name">
          <input type="radio" name="stage" :checked="stage==idx">
          <label>{{ $t(`stage.${name}`) }}</label>
          </li>
          </template>
      </ul>
      </div>
    <div class="coop-overfishing-list-wrapper">
        <table class="oceancalc-table">
          <thead>
            <tr>
              <th>Description</th>
              <th>Wave1</th>
              <th>Wave2</th>
              <th>Wave3</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(cycle, index) in waves" :key="index">
              <template v-if="index < 2">
              <td>{{ $t(`${cycle.type}`) }}</td>
              <td>{{ $t(`${cycle.wave1}`) }}</td>
              <td>{{ $t(`${cycle.wave2}`) }}</td>
              <td>{{ $t(`${cycle.wave3}`) }}</td>
              </template>
              <template v-if="index >= 2">
              <td>{{ cycle.type }}</td>
              <td>{{ $t(`${cycle.wave1}`) }}</td>
              <td>{{ $t(`${cycle.wave2}`) }}</td>
              <td>{{ $t(`${cycle.wave3}`) }}</td>
              </template>
              </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
class Wave {
  constructor() {
    this.event = [0, 0, 0]
    this.tide = [1, 1, 1]
  }
}

class Prob {
  constructor() {
    this.event = [18, 1, 1, 1, 1, 1, 1];
    this.tide = [1, 3, 1]
  }
}

const mWaveArray = [
  [-2, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, -1, -1, -1, -1], // 20
  [-2, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, -1, -1], // 22
  [-2, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0], // 24
]

class Ocean {
  constructor() {
    // this.rnd = new Random() // 乱数生成器
    // this.seed = 0 // Oceanクラスの初期シード
    this.mAppearId = -1
    this.mAppearIdMax = 3
  }

  // ゲームシードを読み込み
  init(seed) {
    this.seed = seed // シード情報を保存する
    this.rnd = new Random() // 乱数生成器
    this.rnd.init(seed)
    this.rnd.getU32() // 一回無駄打ち
  }

  // キンシャケ探しのアタリ位置を出力するプログラム（35回分出力するので絶対足りる）
  getGeyserPos(stage, tide) {
    let mReuse = [] // 乱数を再利用するかどうか
    let mSucc = [] // カンケツセンの位置をシャッフルする
    let mPosition = [] // アタリ位置を出力する

    switch (tide) {
      case 1:
        switch (stage) {
          case 0:
            mReuse = [true, true, true, true, true, true, true, true, true]
            mSucc = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
            break
          case 1:
            mReuse = [true, true, true, true, true, true, true, true]
            mSucc = ["A", "B", "C", "D", "E", "F", "G", "H"]
            break
          case 2:
            mReuse = [true, true, true, true, true, true, true, true, true]
            mSucc = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
            break
          case 3:
            mReuse = [true, true, true, true, true, true, true]
            mSucc = ["A", "B", "C", "D", "E", "F", "G"]
            break
          case 4:
            mReuse = [true, true, true, true, true, true, true]
            mSucc = ["A", "B", "C", "D", "E", "F", "G"]
            break
        }
        break
      case 2:
        switch (stage) {
          case 0:
            mReuse = [true, true, true, true, true]
            mSucc = ["E", "F", "G", "H", "I"]
            break
          case 1:
            mReuse = [true, false, true, true]
            mSucc = ["E", "F", "G", "H"]
            break
          case 2:
            mReuse = [false, true, true, true, true]
            mSucc = ["A", "B", "G", "H", "I"]
            break
          case 3:
            mReuse = [true, true, true, true, true]
            mSucc = ["C", "D", "E", "F", "G"]
            break
          case 4:
            mReuse = [false, false, false, false]
            mSucc = ["D", "E", "F", "G"]
            break
        }
        break
    }

    this.rnd.init(this.seed)
    for (let idx = 0; idx < 35; ++idx) {
      for (let sel = mSucc.length - 1; sel > 0; --sel) {
        let index = parseInt((this.rnd.getU32() * (sel + 1)) / Math.pow(2, 0x20))
        swap(mSucc, index, sel)
        swap(mReuse, index, sel)
      }
      mPosition += mSucc[0]
      if (mReuse[0])
        this.rnd.getU32() // ゴール位置決定用に一回使う
    }
    return mPosition
  }

  // 出現するオオモノの種類を返す関数
  getEnemyId(mFlg) {
    let mRareId = "none"
    const mRareType = ["steelhead", "flyfish", "scrapper", "steeleel", "tower", "maws", "drizzler"] // オオモノテーブルだけどこれで合っているのかは謎
    let rnd = new Random()
    rnd.init(this.rnd.getU32())
    if (mFlg != 1)
      return mRareId
    for (let mProb = 0; mProb < mRareType.length; ++mProb) {
      if (!(parseInt((rnd.getU32() * (mProb + 1)) / Math.pow(2, 0x20))))
        mRareId = mRareType[mProb]
    }
    return mRareId
  }

  getAppearId(index, id) {
    let random = [0, 0]
    let v4 = 0
    let v5 = 0
    let v6 = 0
    let w6 = 0
    let x6 = 0
    let v7 = [1, 2, 3]
    let w7 = [1, 2, 3]
    let x7 = [1, 2, 3]
    let v8 = 0
    let w8 = 0
    let x8 = 0
    let v9 = 0 // v7の値を保存しておく
    let w9 = 0 // w7の値を保存しておく
    let x9 = 0
    let v10 = 0
    let x10 = 0
    let v11 = 0
    let x11 = 0
    let v12 = 0
    let x12 = 0
    let v17 = 0
    let idx = 0 // v7のポインタみたいなやつ
    let result = 0 // リターンする値（引数は変更できないんだが、クソか？

    // id == -1, -2のときだけここに入る
    if (id != -3) {
      if (id == -2)
        id = this.mAppearId // this.mAppearIdは-1で初期化されているので-1が返る
      else if (id == -1) {
        console.log("Initialize mAppearId")
        v4 = this.mAppearIdMax
        if (v4 < 1)
          return -1 // 恐らくここでリターンすることはない
        random[0] = rnd.getU32()
        v6 = this.mAppearIdMax
        if (!v6)
          return -1 // ここでリターンすることもなさそう
        v8 = parseInt((random[0] * v4) / Math.pow(2, 0x20))
        while (1) {
          v9 = v7[idx]
          v10 = Math.max(0, v8 - 1)
          v11 = v8 == 0 ? v7[idx] : id
          v12 = v9 == -1 ? 5 : v8 == 0 ? 1 : 0
          if (v9 != -1) {
            v8 = LODWORD(v10)
            id = v11
          }
          if ((v12 & 7) != 5 && v12 & 7)
            break
          --v6
          ++idx
          if (!v6)
            return -1 // v6 == 0になったら-1を返す
        }
        if (!v12)
          return -1
      }
      return id
    }
    // 恐らくこちらしか使われないと考えて良い

    v5 = this.mAppearId // 前使っていた値を利用する（乱数消費前に
    w6 = this.mAppearIdMax
    idx = 0

    if (!(v5 & 0x80000000)) {
      if (!w6)
        return v5 // w6は常に3なのでここを満たすことはない
      w8 = w6 - 1 // これ、常に2が入っているのでは？
      do {
        v17 = w8 // これ、毎回v17を2で初期化してるだけでは？
        w9 = w7[idx]
        if (w7[idx] < v5)
          break
        w6 -= (w9 == v5 ? 1 : 0) // 0か1を引く
        if (w9 == v5)
          break
        w8 = v17 - 1 // v17は常に2なので、これはw8に常に1を代入しているだけ
        ++idx
      } while (v17)
      // w9はどんどん大きくなるから確実にBreakに入ると思うんですけど？
    }
    if (w6 < 1)
      return v5 // ここでリターンすることもない

    // 第一段階の計算が終わる
    idx = 0 // idxを初期化（多分増えているので）
    random[1] = this.rnd.getU32()
    console.log("RN->", random[1].toString(16).toUpperCase(), "(", index, ") : W6->", w6, "V5->", v5)
    x6 = this.mAppearIdMax
    if (!x6)
      return v5 // ここでリターンすることはない
    x8 = parseInt((random[1] * w6) / Math.pow(2, 0x20))
    while (1) {
      x9 = x7[idx]
      x10 = Math.max(0, x8 - 1)
      x11 = x8 == 0 ? x7[idx] : id
      x12 = x9 == v5 ? 5 : x8 == 0 ? 1 : 0
      if (x9 != v5) {
        x8 = LODWORD(x10)
        id = x11
      }
      if ((x12 & 7) != 5 && x12 & 7)
        break
      --x6
      ++idx
      if (!x6)
        return v5 // 前と同じ値を返す
    }
    if (!x12)
      return v5
    return id
  }

  getEnemyIds(wave) {
    const mRareType = ["steelhead", "flyfish", "scrapper", "steeleel", "tower", "maws", "drizzler"] // オオモノテーブルだけどこれで合っているのかは謎
    let mRareArray = []
    let mRareId = "none"
    mWaveArray[wave].forEach((mFlg, index) => {
      switch (mFlg) {
        case -2: // 一番最初の初期化は乱数だけ消費する
          // this.rnd.getU32()
          this.mAppearId = this.getAppearId(index, -3)
          // mRareArray.push(this.mAppearId)
          mRareArray.push("none")
          break
        case -1: // その他は何もせず無を出力
          mRareArray.push("none")
          break
        case 0: // 0なら乱数を消費して湧き方向を変化させる
          let mAppearId = this.getAppearId(index, -3)
          this.mAppearId = mAppearId
          mRareArray.push(mAppearId)
          break;
        case 1: // 1なら乱数を消費してオオモノを出現させる
          let rnd = new Random() // オオモノ出現用乱数生成器
          const random = this.rnd.getU32()
          // console.log("Enemy RNG", random.toString(16).toUpperCase(), this.rnd)
          rnd.init(random) // WAVE乱数を一つ消費する
          for (let mProb = 0; mProb < mRareType.length; ++mProb) {
            if (!(parseInt((rnd.getU32() * (mProb + 1)) / Math.pow(2, 0x20))))
              mRareId = mRareType[mProb]
          }
          mRareArray.push(mRareId)
          break;
        default:
          break;
      }
    })
    return mRareArray
  }
}

class Random {
  constructor() { }

  init(seed) {
    this.mSeed1 = (Math.imul(0x6C078965, (seed ^ (seed >>> 30))) + 1) >>> 0;
    this.mSeed2 = (Math.imul(0x6C078965, (this.mSeed1 ^ (this.mSeed1 >>> 30))) + 2) >>> 0;
    this.mSeed3 = (Math.imul(0x6C078965, (this.mSeed2 ^ (this.mSeed2 >>> 30))) + 3) >>> 0;
    this.mSeed4 = (Math.imul(0x6C078965, (this.mSeed3 ^ (this.mSeed3 >>> 30))) + 4) >>> 0;
  }

  getU32() {
    let n = (this.mSeed1 ^ (this.mSeed1 << 11)) >>> 0;
    this.mSeed1 = this.mSeed2;
    this.mSeed2 = this.mSeed3;
    this.mSeed3 = this.mSeed4;
    this.mSeed4 = ((n ^ (n >>> 8) ^ this.mSeed4 ^ (this.mSeed4 >>> 19))) >>> 0;
    return this.mSeed4;
  }
}

export default {
  data: () => ({
    waves: [],
    mInitialSeed: 0x0,
    mInputSeed: 0x0,
    stage: 0,
  }),
  created() {
    const mInitialSeed = this.$route.query.seed
    if (mInitialSeed != null)
      this.mInitialSeed = mInitialSeed
    this.generate()
  },
  watch: {
    // 選択しているステージが変更されたら再計算を行う
    stage: {
      handler: function (newValue, oldValue) {
        this.stage = newValue
        this.generate()
      }
    },
    mInitialSeed: {
      handler: function (newValue, oldValue) {
        // this.$route.query.seed = newValue
        this.generate()
      }
    }
  },
  methods: {
    validate() {
      this.mInputSeed = this.mInputSeed.replace(/[^0-9, A-F, a-f]/g, "").toUpperCase()
      this.mInitialSeed = parseInt("0x" + this.mInputSeed)
    },
    generate() {
      // まずは全要素を空っぽにする
      this.waves.splice(0, this.waves.length)

      let mGameSeed = [this.mInitialSeed] // 各WAVEの乱数生成器を初期化するシード
      let grnd = new Random() // ゲーム乱数生成器
      grnd.init(this.mInitialSeed) // 初期シードでゲーム乱数生成器を初期化

      // 潮位とイベントを先読み
      let mWave = new Wave() // WAVE情報を保存するクラス
      const mProb = new Prob() // 確率情報をもっているクラス（配列でよくね？）

      // WAVE情報を検出
      for (let wave = 0; wave < 3; ++wave) {
        for (let event = 0, sum = 0; event < 7; ++event) {
          if ((wave > 0) && (mWave.event[wave - 1] != 0) && (mWave.event[wave - 1] == event))
            continue;
          sum += mProb.event[event]
          if ((grnd.getU32() * sum / Math.pow(2, 32)) < mProb.event[event])
            mWave.event[wave] = event
        }
        for (let tide = 0, sum = 0; tide < 3; ++tide) {
          if ((tide == 0) && (1 <= mWave.event[wave] && (mWave.event[wave] <= 3)))
            continue;
          sum += mProb.tide[tide];
          if ((grnd.getU32() * sum / Math.pow(2, 32)) < mProb.tide[tide])
            mWave.event[wave] == 6 ? mWave.tide[wave] = 0 : mWave.tide[wave] = tide
        }
      }

      this.waves.push({ type: "tide", wave1: tide(mWave.tide[0]), wave2: tide(mWave.tide[1]), wave3: tide(mWave.tide[2]) })
      this.waves.push({ type: "event", wave1: event(mWave.event[0]), wave2: event(mWave.event[1]), wave3: event(mWave.event[2]) })

      grnd.init(this.mInitialSeed) // 初期シードでゲーム乱数生成器を初期化
      grnd.getU32() // 謎の一発乱数消費
      mGameSeed.push(grnd.getU32())
      mGameSeed.push(grnd.getU32())

      // // 全WAVEを計算する
      let ocean = [new Ocean(), new Ocean(), new Ocean()]
      ocean[0].init(mGameSeed[0])
      ocean[1].init(mGameSeed[1])
      ocean[2].init(mGameSeed[2])

      // 予めキンシャケ探しとして考えてアタリ位置を計算
      let mEnemyArray = [[], [], []]

      for (let wave = 0; wave < 3; ++wave) {
        switch (mWave.event[wave]) {
          case 0:
          case 5:
          case 6:
            mEnemyArray[wave] = ocean[wave].getEnemyIds(wave)
            break
          case 2:
            const tide = mWave.tide[wave]
            mEnemyArray[wave] = ocean[wave].getGeyserPos(this.stage, tide)
            break
          default:
            let tmpArray = Array(35)
            tmpArray.fill("-")
            mEnemyArray[wave] = tmpArray
            break
        }
      }
      console.log(mEnemyArray)
      for (let idx = 0; idx < 35; ++idx) {
        this.waves.push({ type: `${idx + 1}`, wave1: mEnemyArray[0][idx], wave2: mEnemyArray[1][idx], wave3: mEnemyArray[2][idx] })
      }
    }
  }
}

function tide(number) {
  switch (number) {
    case 0:
      return "low"
    case 1:
      return "normal"
    case 2:
      return "high"
  }
}

function event(number) {
  switch (number) {
    case 0:
      return "noevent"
    case 1:
      return "rush"
    case 2:
      return "goldie-seeking"
    case 3:
      return "the-griller"
    case 4:
      return "the-mothership"
    case 5:
      return "fog"
    case 6:
      return "cohock-charge"
    default:
      return
  }
}

function swap(array, x, y) {
  array[x] = [array[y], array[y] = array[x]][0];
  return array;
}

function LODWORD(x) {
  return (x & 0xFFFFFFFF)
}
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

body {
  text-align: center;
}

div {
  font-family: "Splatfont";
  display: block;
  margin: 0 auto;
  padding: 0 auto;

  .page {
    min-height: 100%;
    box-sizing: border-box;
  }

  .oceancalc {
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

  .oceancalc-header {
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
      object-fit: cover;
      background-image: url("~static/seedhack.png");
      background-repeat: no-repeat;
      background-size: contain;
      width: 300px;
      margin: 0 auto;
      height: 171px;
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

  .oceancalc-table {
    font-family: "Splatfont2";
    table-layout: fixed;
    color: #ddd;
    width: 100%;
    text-align: center;
  }

  #content {
    position: relative;
    display: block;

    .input-control {
      width: 80%;
      min-width: 400px;
      text-align: center;
      color: #fff;
      font-family: "Splatfont2";

      label {
        font-size: 1.1em;
        position: absolute;
        transform: translateY(-18px) scale(0.75);
        transform-origin: top left;
      }

      .oceancalc-input-seed {
        width: 300px;
        font-family: "Splatfont2";
        color: #fff;
        font-size: 1.25em;
        padding: 4px 0 2px;
        line-height: 1.2em;
        background: none;
        outline: none;
        border-bottom: 2.5px solid #cccccc;
        border-right: none;
        border-left: none;
        border-top: none;

        &::after {
          bottom: -1px;
          content: "__";
          left: 0;
          position: absolute;
          transition: 0.3s cubic-bezier(0.25, 0.8, 0.5, 1);
          width: 100%;
        }
      }
    }

    .oceancalc-option {
      display: inline-flex;
      font-family: "Splatfont2";
      font-size: 1.2em;
      width: 100%;
      max-width: 27em;
      list-style-type: none;
      flex-wrap: wrap;
      padding-bottom: 30px;

      li {
        display: list-item;
        width: 50%;
        text-align: left;
      }
    }
  }

  input[type="radio"] + label {
    cursor: pointer;
  }

  input[type="radio"]:checked + label {
    color: yellow;
  }

  input[type="radio"]:checked + label:before {
    background-image: url(data:image/png;base64,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);
  }

  input[type="radio"] + label::before {
    display: inline-block;
    letter-spacing: 0.5em;
    content: "";
    background-image: url(data:image/png;base64,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);
    background-repeat: no-repeat;
    background-size: contain;
    background-position: 0 0;
    width: 1em;
    height: 1em;
    margin-right: 0.4em;
    margin-bottom: -0.1em;
  }

  input[type="radio"] {
    display: none;
  }
}
</style>