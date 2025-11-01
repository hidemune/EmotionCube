了解しました。
以下は、あなたの `screensave.py` とプロジェクト *EmotionCube / Heart of Flesh* の思想・構造を
学術的かつ芸術的に統合したドキュメント案です。
そのまま `README_philosophy.md` としてGitHubに追加できます。

---

# 🧠 README_philosophy.md

## *Heart of Flesh — The Visible Architecture of Emotion*

by **Hidemune Tanaka**

---

### 🌌 概要

**EmotionCube / Heart of Flesh** は、
人間の「肉の心」を可視化するための実験的スクリーンセーバーです。

この作品は単なる視覚エフェクトではなく、
**感情・言語・神経・信仰の交差点**に位置する哲学的シミュレータです。

> “I will remove the heart of stone from your flesh and give you a heart of flesh.”
> ― *Ezekiel 36:26*

---

## 🧩 基本構造

### 1. 感情空間の三次元構成

各感情は `emotion.csv` に定義された **三軸ベクトル (x, y, z)** によって表されます。
この3軸は、人間の内的バランスを次のように投影しています：

| 軸  | 対象         | 意味                 |
| -- | ---------- | ------------------ |
| X軸 | 愛 ↔ 自責     | 「他者への共感」と「自己省察」の振動 |
| Y軸 | 高ぶり ↔ 畏れ   | 「力」と「謙遜」の心理的対位     |
| Z軸 | 自分に近い ↔ 遠い | 「内的自己」と「外界」の距離感    |

これらは従来の心理学的モデル（PlutchikやRussell）を超え、
**“感情の幾何学”** として再構成されています。

---

### 2. 感情点群と光

`draw_points()` 関数によって描かれる各点は、
**ひとつの感情素子（Emotion Particle）**を表します。

* 点の色は、座標値をRGBに変換することで、
  「感情の波長」を可視光として表現。
* 光の揺らぎは、感情が内外の刺激と**共鳴する動的存在**であることを示します。

> 光は、心の状態そのもの。
> すべての感情は、観測者との距離で輝きを変える。

---

### 3. ラベルの八面体配置

空間には16の感情ラベルが配置されています：

```
Joy, Trust, Sadness, Disgust, Fear, Anticipation,
Anger, Surprise, Optimism, Submission,
Contempt, Disapproval, Aggressiveness, Awe, Remorse, Love
```

これらは**Plutchikの感情輪**を3Dに展開した構造であり、
**感情の均衡と対立を幾何的張力**として表しています。

空間の回転は、感情構造が静止点を持たないこと──
すなわち「生きた心（Living Heart）」を意味します。

---

### 4. 回転と非周期性

回転軸 `(0.486, 0.726, 0)` は意図的に**無理数比方向**を採用。
これにより、表示は決して同じ状態に戻らず、
**「永遠の再生成（perpetual regeneration）」** を象徴します。

> 肉の心は、完全な周期を持たない。
> それは、絶えず変化しながらも崩壊しないリズムである。

---

### 5. 神経科学的背景

フッタに示される研究テーマ：

> “Research into the relationship between (The brain’s reward system including the hippocampus and amygdala) and (Language).”

これは感情処理と意味生成の中枢（扁桃体・海馬）に着目した仮説モデルです。
EmotionCubeは、言語的記号（Word）を座標に変換することで、
**「言葉が脳内で感情構造をどう形成するか」**を可視的に実験する装置でもあります。

---

## 🕊️ 神学的・倫理的次元

この作品の核心にあるのは、「石の心」と「肉の心」の対比です。

| 石の心       | 肉の心          |
| --------- | ------------ |
| 反応しない・防御的 | 共鳴し、変化を受け入れる |
| 形式・律法     | 生命・共感        |
| 外部の神      | 内なる神         |
| 分離        | 統合           |

EmotionCubeは、**“愛と知の統合”**を視覚的に表現することで、
「創世記3:22」で封印された“いのちの木”を、**内面に再発芽させる試み**でもあります。

---

## 💫 アートとしてのメッセージ

> “--- [ Heart of Flesh ] Sample ---
> Data provided by Hidemune TANAKA”

この署名は、
人間の精神的創造が「神のかたちの模倣」であることを示唆しています。
作品を起動することは、外界のスクリーンを通して
**自分自身の心の地図を観測する行為**です。

> あなたの心が動くとき、この宇宙もまたわずかに回転している。

---

## 🧩 構想のキーワード

* **三次元感情構造 / 3D Emotional Geometry**
* **光による心の再生 / Photonic Regeneration of the Heart**
* **内的エデン / Inner Eden**
* **感情共鳴モデル / Resonant Empathy Model**
* **知覚と倫理の融合 / Cognitive–Ethical Integration**

---

## 🪶 作者より

> “肉の心は、外に探すものではなく、内で発芽させるもの。
> それを見つめるために、私はスクリーンに心を映しました。”
> — Hidemune Tanaka

---

## 📘 補足

技術詳細は [`screensave.py`](./screensave.py) を参照。
理論背景については [SlideShare論文](https://www.slideshare.net/slideshow/tcsengpptx/264247829) を併読してください。

---

### 🌟 ライセンス提案（哲学的ライセンス）

本作品は MIT ライセンスに準拠しますが、
次の一文を加えることを推奨します：

> 本ソフトウェアを用いる者は、自己と他者を同じように愛することを意図し、
> その心においてのみ「再配布」が許される。

---

もし望まれれば、この哲学版READMEを英語にも翻訳して
`README_philosophy_en.md` として整形することもできます。
英語版も作成しますか？
