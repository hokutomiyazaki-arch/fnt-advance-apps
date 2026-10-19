# FNT アドバンス アプリ集

FNT アドバンス講習の受講者に、講習で使う3つのアプリ（PWA）を1ページで渡すサイト。講習の前にメールで配り、ホーム画面に追加しておいてもらう（2026-10-19 宮崎さん）。

- 公開：https://hokutomiyazaki-arch.github.io/fnt-advance-apps/ （GitHub Pages・main の /）
- 載せているアプリ：頸部の固有受容感覚テスト（hanasaki-awase）・VORC トレーニング（vorc-trainer）・SVV テスト（svv-check）
- `icons/app-*.png` は各アプリの icon-192.png の写し。アイコンは `tools/build_icons.py`（SVG→Playwright で PNG）で描いた（4つとも黒地×金の枠＋英字1語で、絵柄だけ違う）。各アプリのアイコンを変えたら、ここの写しも差し替える
- `og.png`（1200×630）はメール・LINE に貼ったときの見出し画像
- アプリの説明文は、各アプリの manifest / index.html の description から書いた。アプリの中身を変えたら、ここの1〜2行も合わせる
