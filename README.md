# にゃんこ用語マンガ 🐈

用語を入れたら、**先輩シャム猫×後輩黒猫の4コマ漫画**で解説してくれるサイトを自動生成するCLI。

- Claude Code CLI（`claude -p`）で脚本生成
- SVG埋め込みでキャラ固定（同じ2匹がずっと出てくる）
- GitHub Pages で公開
- LINE共有URLを自動で吐く

公開URL: https://musclelove-777.github.io/term-cat-manga/

## 使い方

```bash
# 1本生成して push まで自動
python make.py "Docker"

# ローカルだけ（pushしない）
python make.py --no-push "プロキシ"

# index.html だけ作り直し
python make.py --rebuild-index
```

## 構成

```
107_用語漫画解説/
├── make.py              # CLI本体
├── lib/
│   ├── characters.py    # 2匹の猫SVG（5表情×2キャラ）
│   └── render.py        # HTMLレンダラ
├── template/style.css   # 4コマレイアウト
├── data/terms.json      # 生成済み用語の登録簿
└── docs/                # GitHub Pages公開ディレクトリ
    ├── index.html       # 用語一覧（自動生成）
    └── <slug>/index.html
```

## キャラ

- **先輩**: シャム猫（クリーム×ブラウンポイント、青目）。物知り、敬語まじり、`〜だにゃ`を時々
- **後輩**: 黒猫（緑目、目大きめ）。元気、フランク、質問役

表情は normal / explain / surprise / think / happy の5種、`lib/characters.py` でSVGとして定義。

## LINE共有

各ページの「📲 LINEで共有」ボタンが LINE のテキスト共有URL（`https://line.me/R/msg/text/?...`）を開く。タップ→トーク選択→送信、で完結。
