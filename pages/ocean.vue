t pu<template>
  <div class="page oceancalc">
    <header class="navigation-bar">
      <h1>
        <nuxt-link to="/">
          <font-awesome-icon icon="bars" size="lg" class="oceancalc-button" />
        </nuxt-link>
        Ocean Calc
        <nuxt-link to="/database">
          <font-awesome-icon icon="database" size="lg" class="oceancalc-button" />
        </nuxt-link>
        </h1>
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
    let mDest = [] // カンケツセンのゴール位置
    let mPosition = [] // アタリ位置を出力する

    switch (tide) {
      case 1:
        switch (stage) {
          case 0:
            mReuse = [true, true, true, true, true, true, true, true, true]
            mSucc = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
            mDest = [
              ["1", "G", "D", "4"], // A
              ["E", "2", "D", "I"], // B Complete
              ["E", "D", "H", "G"], // C Complete
              ["C", "A"], // D Complete
              ["C", "H", "B"], // E
              ["A", "G", "H", "B"], // F
              ["F", "C", "A"], // G Complete
              ["I", "C", "E", "F"], // H
              ["H", "B", "A"] // I Complete
            ]
            break
          case 1:
            mReuse = [true, true, true, true, true, true, true, true]
            mSucc = ["A", "B", "C", "D", "E", "F", "G", "H"]
            mDest = [
              ["1", "2"],
              ["1", "2"],
              ["1", "2"],
              ["1", "2"],
              ["1", "2"],
              ["1", "2"],
              ["1", "2"],
              ["1", "2"]
            ]
            break
          case 2:
            mReuse = [true, true, true, true, true, true, true, true, true]
            mSucc = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
            mDest = [
              ["C", "E"],
              ["D", "F", "G", "H"],
              ["A", "D", "I", "F"],
              ["G", "B", "I", "C"],
              ["A", "G", "D", "F"],
              ["H", "B", "G", "I"],
              ["D", "I", "F", "B"],
              ["F", "I", "B", "E"],
              ["G", "D", "F", "C"]
            ]
            break
          case 3:
            mReuse = [true, true, true, true, true, true, true]
            mSucc = ["A", "B", "C", "D", "E", "F", "G"]
            mDest = [
              ["F", "G", "B", "C"],
              ["A", "E", "D"],
              ["F", "A", "G", "E"],
              ["B", "F", "G"],
              ["B", "C"],
              ["A", "D"],
              ["A", "D", "C"]
            ]
            break
          case 4:
            mReuse = [true, true, true, true, true, true, true]
            mSucc = ["A", "B", "C", "D", "E", "F", "G"]
            mDest = [
              ["1", "2"],
              ["G"],
              ["1", "2", "3"],
              ["1", "2"],
              ["A"],
              ["C"],
              ["B"]
            ]
            break
        }
        break
      case 2:
        switch (stage) {
          case 0:
            mReuse = [true, true, true, true, true]
            mSucc = ["E", "F", "G", "H", "I"]
            mDest = [
              ["H", "H"],
              ["G", "H"],
              ["F", "F"],
              ["I", "F"],
              ["H", "G"]
            ]
            break
          case 1:
            mReuse = [true, false, true, true]
            mSucc = ["E", "F", "G", "H"]
            mDest = [
              ["-"],
              ["-"],
              ["-"],
              ["-"],
            ]
            break
          case 2:
            mReuse = [false, true, true, true, true]
            mSucc = ["A", "B", "G", "H", "I"]
            mDest = [
              ["H", "H"],
              ["G", "H"],
              ["I", "F"],
              ["I", "F"],
              ["G", "H"]
            ]
            break
          case 3:
            mReuse = [true, true, true, true, true]
            mSucc = ["C", "D", "E", "F", "G"]
            mDest = [
              ["G", "E"],
              ["F", "G"],
              ["C", "C"],
              ["D", "D"],
              ["D", "C"]
            ]
            break
          case 4:
            mReuse = [false, false, false, false]
            mSucc = ["D", "E", "F", "G"]
            mDest = [
              ["G"],
              ["F"],
              ["G"],
              ["F"]
            ]
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
        swap(mDest, index, sel)
      }
      if (mReuse[0]) {
        let index = parseInt((this.rnd.getU32() * mDest[0].length) / Math.pow(2, 0x20))  // ゴール位置決定用に一回使う
        mPosition.push(mSucc[0] + ", " + mDest[0][index])
      }
      else {
        mPosition.push(mSucc[0] + ", " + mDest[0][0])
        // mPosition += (mSucc[0] + mDest[0][0])
      }
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
        // console.log("Initialize mAppearId")
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
    // console.log("RN->", random[1].toString(16).toUpperCase(), "(", index, ") : W6->", w6, "V5->", v5)
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

  getEnemyIds(wave, event) {
    const mRareType = ["steelhead", "flyfish", "scrapper", "steeleel", "tower", "maws", "drizzler"] // オオモノテーブルだけどこれで合っているのかは謎
    let mRareArray = []
    let mRareId = "none"
    let mCount = 0
    let mGoldieCount = 0
    mWaveArray[wave].forEach((mFlg, index) => {
      switch (mFlg) {
        case -2: // 一番最初の初期化は乱数だけ消費する
          if (event != 4) {
            this.mAppearId = this.getAppearId(index, -3)
            mRareArray.push("none")
          } else {
            mRareArray.push("none")
          }
          break
        case -1: // その他は何もせず無を出力
          mRareArray.push("none")
          break
        case 0: // 0なら乱数を消費して湧き方向を変化させる
          if (event != 4) {
            let mAppearId = this.getAppearId(index, -3)
            this.mAppearId = mAppearId
            mRareArray.push(mAppearId)
          } else {
            mRareArray.push("none")
          }
          break;
        case 1: // 1なら乱数を消費してオオモノを出現させる
          switch (event) {
            case 1:
              mRareArray.push("none")
              break
            case 3:
              mRareArray.push("none")
              break
            case 4:
              mRareArray.push("none")
              break
            case 5:
              mCount++
              // 5の倍数のときはキンシャケを出現してリターン
              if (mCount % 5 == 0) {
                mRareArray.push("goldie")
                mGoldieCount += 1
                this.rnd.getU32()
                break
              }
            default:
              let rnd = new Random() // オオモノ出現用乱数生成器
              const random = this.rnd.getU32()
              rnd.init(random) // WAVE乱数で初期化する
              for (let mProb = 0; mProb < mRareType.length; ++mProb) {
                if (!(parseInt((rnd.getU32() * (mProb + 1)) / Math.pow(2, 0x20))))
                  mRareId = mRareType[mProb]
              }
              mRareArray.push(mRareId)
          }
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
          let random = grnd.getU32()
          // console.log("Random Number->", random.toString(16))
          if ((random * sum / Math.pow(2, 32)) < mProb.event[event])
            mWave.event[wave] = event
        }
        for (let tide = 0, sum = 0; tide < 3; ++tide) {
          if ((tide == 0) && (1 <= mWave.event[wave] && (mWave.event[wave] <= 3)))
            continue;
          sum += mProb.tide[tide];
          let random = grnd.getU32()
          // console.log("Random Number->", random.toString(16))
          if ((random * sum / Math.pow(2, 32)) < mProb.tide[tide])
            mWave.event[wave] == 6 ? mWave.tide[wave] = 0 : mWave.tide[wave] = tide
        }
      }

      this.waves.push({ type: "tide", wave1: tide(mWave.tide[0]), wave2: tide(mWave.tide[1]), wave3: tide(mWave.tide[2]) })
      this.waves.push({ type: "event", wave1: event(mWave.event[0]), wave2: event(mWave.event[1]), wave3: event(mWave.event[2]) })

      grnd.init(this.mInitialSeed) // 初期シードでゲーム乱数生成器を初期化
      grnd.getU32() // 謎の一発乱数消費
      mGameSeed.push(grnd.getU32())
      mGameSeed.push(grnd.getU32())

      this.waves.push({ type: "mWaveSeed", wave1: mGameSeed[0], wave2: mGameSeed[1], wave3: mGameSeed[2]})
      // // 全WAVEを計算する
      let ocean = [new Ocean(), new Ocean(), new Ocean()]
      ocean[0].init(mGameSeed[0])
      ocean[1].init(mGameSeed[1])
      ocean[2].init(mGameSeed[2])

      // オオモノ湧き方向と種類の予測用配列
      let mEnemyArray = [[], [], []]

      for (let wave = 0; wave < 3; ++wave) {
        const event = mWave.event[wave]
        if (event == 2) {
          const tide = mWave.tide[wave]
          mEnemyArray[wave] = ocean[wave].getGeyserPos(this.stage, tide)
          // console.log("WAVE", wave, mEnemyArray[wave])
        }
        else {
          mEnemyArray[wave] = ocean[wave].getEnemyIds(wave, event)
          // t console.log("WAVE", wave, mEnemyArray[wave])
        }
      }
      // console.log(mEnemyArray)
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
@import "~assets/sass/style.scss";
@import "~assets/sass/splatnet2.scss";
@import "~assets/sass/salmonrecords.scss";
</style>