"""OGP 画像（1200x630）を作り、ページの 390x844 スクショを撮る。
使い方: shoot.py og <repo_dir>  /  shoot.py shot <url> <out_prefix>"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

mode = sys.argv[1]
with sync_playwright() as p:
    b = p.chromium.launch()
    if mode == "og":
        repo = Path(sys.argv[2]).resolve()
        html = f'''<!doctype html><html><head>
<link href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@700&family=Cormorant+Garamond:wght@500;600&display=block" rel="stylesheet">
<style>*{{margin:0}}body{{width:1200px;height:630px;background:radial-gradient(110% 90% at 50% -10%,#1f1d18 0%,#0e0e0f 50%,#050505 100%);
color:#f4f1ea;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:"Shippori Mincho",serif}}
.fnt{{font-family:"Cormorant Garamond";letter-spacing:.42em;color:#d8bd84;font-size:24px;margin-bottom:14px}}
h1{{font-size:56px;letter-spacing:.12em;font-weight:700}} h1 span{{font-family:"Cormorant Garamond";font-weight:500;color:#d8bd84;letter-spacing:.2em;margin-right:24px}}
.row{{display:flex;gap:56px;margin-top:44px}} .row img{{width:190px;height:190px}}</style></head><body>
<div class="fnt">FUNCTIONAL NEURO TRAINING</div><h1><span>ADVANCE</span>アプリ集</h1>
<div class="row"><img src="file:///tmp/fnt_advance_apps/icons/out/neck-any-512.png"><img src="file:///tmp/fnt_advance_apps/icons/out/vorc-any-512.png"><img src="file:///tmp/fnt_advance_apps/icons/out/svv-any-512.png"></div>
</body></html>'''
        tmp = Path("/tmp/fnt_advance_apps/og.html"); tmp.write_text(html)
        pg = b.new_page(viewport={"width": 1200, "height": 630})
        pg.goto(f"file://{tmp}"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(800)
        pg.screenshot(path=str(repo / "og.png"))
    else:
        url, out = sys.argv[2], sys.argv[3]
        pg = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
        pg.goto(url, wait_until="networkidle"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(500)
        sw = pg.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
        print("scrollWidth/clientWidth", sw)
        pg.screenshot(path=f"{out}-top.png")
        pg.screenshot(path=f"{out}-full.png", full_page=True)
    b.close()
