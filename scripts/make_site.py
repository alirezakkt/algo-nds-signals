#!/usr/bin/env python3
"""Build the visual one-pager (index.html) + thumbnails used by GitHub Pages.

Outputs:
  index.html            the gallery site (dark, image-first)
  docs/thumbs/*.jpg     ~460px wide thumbnails, generated from archive/

The page is a single file with inline CSS/JS and an embedded copy of the
screenshot + signal data, so it works as a static GitHub Pages site with no
build step and no external dependencies.
"""

import html
import json
import os

from PIL import Image

FEATURED = {
    "2025-09-28_1732", "2025-10-01_1050", "2025-10-03_1351", "2025-10-08_2150",
    "2025-10-17_1406", "2025-10-17_1801", "2025-11-12_1600", "2025-11-30_2041",
    "2025-12-21_1454", "2026-02-15_1238", "2026-02-20_1941", "2026-06-29_1105",
}

THUMB_W = 640
THUMB_Q = 80
THUMBS = os.path.join("docs", "thumbs")


def make_thumbs(shots):
    os.makedirs(THUMBS, exist_ok=True)
    # clean stale thumbs
    for name in os.listdir(THUMBS):
        if name.endswith(".jpg"):
            os.remove(os.path.join(THUMBS, name))

    for index, shot in enumerate(shots, start=1):
        shot["thumbs"] = []
        for k, image in enumerate(shot["images"], start=1):
            src = os.path.join(shot["folder"], image)
            out_name = f"{index:03d}-{k}.jpg" if len(shot["images"]) > 1 else f"{index:03d}.jpg"
            out = os.path.join(THUMBS, out_name)
            im = Image.open(src).convert("RGB")
            if im.width > THUMB_W:
                height = round(im.height * THUMB_W / im.width)
                im = im.resize((THUMB_W, height), Image.LANCZOS)
            im.save(out, "JPEG", quality=THUMB_Q, optimize=True)
            shot["thumbs"].append(os.path.join(THUMBS, out_name))


PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Algo NDS — node-based price structure</title>
<meta name="description" content="202 annotated charts from an NDS engine: nodes, sequences, structure-based targets, volatility-based stops.">
<style>
  :root{--bg:#0b0e14;--panel:#121722;--line:#1e2735;--fg:#e8eef5;--muted:#8a96a8;--cyan:#22d3ee;--amber:#f5c518}
  *{box-sizing:border-box}
  html,body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
  a{color:var(--cyan);text-decoration:none}
  .wrap{max-width:1240px;margin:0 auto;padding:0 24px}
  header{padding:72px 0 40px;border-bottom:1px solid var(--line)}
  .kicker{color:var(--cyan);letter-spacing:.18em;text-transform:uppercase;font-size:12px;font-weight:700}
  h1{margin:14px 0 10px;font-size:clamp(44px,7vw,88px);line-height:.95;letter-spacing:-.03em}
  .lede{max-width:640px;color:var(--muted);font-size:19px}
  .stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin:36px 0 0}
  .stat{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:18px}
  .stat b{display:block;color:var(--amber);font-size:34px;line-height:1.1;letter-spacing:-.02em}
  .stat span{color:var(--muted);font-size:13px}
  section{padding:64px 0;border-bottom:1px solid var(--line)}
  h2{font-size:13px;letter-spacing:.18em;text-transform:uppercase;color:var(--muted);font-weight:700;margin:0 0 26px}
  .two{display:grid;grid-template-columns:1.1fr 1fr;gap:32px;align-items:center}
  .card{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:26px}
  .steps{display:grid;gap:10px}
  .step{display:flex;gap:14px;align-items:baseline;border-bottom:1px dashed var(--line);padding-bottom:10px}
  .step:last-child{border:0}
  .step i{color:var(--cyan);font-style:normal;font-weight:700;font-size:13px;min-width:24px}
  .step b{min-width:104px;font-size:14px;letter-spacing:.04em}
  .step span{color:var(--muted);font-size:14px}
  .scroll{overflow-x:auto}
  table{border-collapse:collapse;width:100%;font-size:14px}
  th,td{text-align:left;padding:9px 12px;border-bottom:1px solid var(--line);white-space:nowrap}
  th{color:var(--muted);font-weight:600;font-size:12px;letter-spacing:.08em;text-transform:uppercase}
  td.num{text-align:right;font-variant-numeric:tabular-nums}
  .buy{color:#22d3ee}.sell{color:#f5c518}
  figure{margin:0}
  figure img{width:100%;display:block;border-radius:14px;border:1px solid var(--line)}
  .filters{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:22px}
  .chip{background:var(--panel);border:1px solid var(--line);color:var(--muted);border-radius:999px;padding:7px 15px;font-size:13px;cursor:pointer;transition:.15s}
  .chip:hover{border-color:var(--cyan);color:var(--fg)}
  .chip.on{background:var(--cyan);border-color:var(--cyan);color:#04222a;font-weight:700}
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px}
  .tile{position:relative;border-radius:12px;overflow:hidden;border:1px solid var(--line);cursor:zoom-in;background:#000;aspect-ratio:16/10}
  .tile img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .35s ease,opacity .2s}
  .tile:hover img{transform:scale(1.06)}
  .tile .meta{position:absolute;inset:auto 0 0 0;padding:26px 12px 9px;font-size:11px;color:#dfe7f1;
    background:linear-gradient(transparent,rgba(4,6,10,.92));display:flex;justify-content:space-between;gap:8px}
  .tile .pair{position:absolute;top:8px;left:8px;background:var(--amber);color:#141414;font-size:10px;
    font-weight:800;padding:3px 7px;border-radius:5px;letter-spacing:.06em}
  .count{color:var(--muted);font-size:13px;margin:0 0 16px}
  .grid.cases{grid-template-columns:repeat(auto-fill,minmax(430px,1fr));gap:16px}
  .case{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:13px;cursor:zoom-in;transition:border-color .15s}
  .case:hover{border-color:var(--cyan)}
  .case-head{display:flex;justify-content:space-between;align-items:baseline;gap:10px;margin-bottom:10px}
  .case-head b{font-size:14px}
  .case-head span{color:var(--muted);font-size:12px}
  .strip{display:grid;grid-template-columns:repeat(4,1fr);gap:4px}
  .strip img{width:100%;aspect-ratio:16/10;object-fit:cover;border-radius:6px;display:block}
  .more{display:flex;align-items:center;justify-content:center;background:#0b0e14;
    border:1px dashed var(--line);border-radius:6px;color:var(--muted);font-size:13px}
  #lb{position:fixed;inset:0;background:#06080d;display:none;z-index:50;padding:28px;overflow:auto}
  #lb.open{display:block}
  #lb .inner{max-width:1080px;margin:0 auto}
  #lb img{width:100%;border-radius:10px;margin-bottom:12px;border:1px solid var(--line)}
  #lb .cap{color:var(--muted);font-size:14px;margin:0 0 4px}
  #lb .head{display:flex;justify-content:space-between;align-items:center;gap:16px;margin-bottom:14px}
  #lb button{background:var(--panel);border:1px solid var(--line);color:var(--fg);border-radius:8px;
    padding:8px 14px;cursor:pointer;font-size:14px}
  #lb button:hover{border-color:var(--cyan)}
  footer{padding:48px 0 72px;color:var(--muted);font-size:13px}
  @media(max-width:820px){.two{grid-template-columns:1fr}}
</style>
</head>
<body>
<header>
  <div class="wrap">
    <div class="kicker">Algo NDS · node-based structure</div>
    <h1>Price is a sequence.<br>Not a shape.</h1>
    <p class="lede">Swing points are computed, not eyeballed. The next node becomes the target;
      measured volatility becomes the stop. Below: the full working record.</p>
    <div class="stats">__STATS__</div>
  </div>
</header>

<section>
  <div class="wrap">
    <div>
      <h2>How a signal is built</h2>
      <div class="card steps">
        <div class="step"><i>01</i><b>NODES</b><span>swing points via second derivative</span></div>
        <div class="step"><i>02</i><b>SEQUENCE</b><span>frame the legs — which displacement is in play</span></div>
        <div class="step"><i>03</i><b>SYMMETRY</b><span>project geometry: where the next leg lands</span></div>
        <div class="step"><i>04</i><b>TARGET</b><span>next node = TP — structure decides the exit</span></div>
        <div class="step"><i>05</i><b>STOP</b><span>GARCH volatility = SL — measured, not chosen</span></div>
        <div class="step"><i>06</i><b>TRIGGER</b><span>fire inside the retracement zone, depth recorded</span></div>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>The signals</h2>
    <p class="count">15 machine-readable signals · 13–22 Dec 2025 · entry, target, stop and the reason it fired</p>
    <div class="scroll">
      <table>
        <thead><tr><th>Date</th><th>Symbol</th><th>Side</th><th>Entry</th><th>TP</th><th>SL</th><th>R:R</th><th>Reason</th></tr></thead>
        <tbody>__SIGNALS__</tbody>
      </table>
    </div>
  </div>
</section>

<section>
  <div class="wrap two">
    <figure><img src="docs/rr.svg" alt="Designed R:R per signal"></figure>
    <figure><img src="docs/timeline.svg" alt="Posts per month"></figure>
  </div>
</section>

<section id="gallery">
  <div class="wrap">
    <h2>The archive</h2>
    <p class="count"><span id="shown">__COUNT__</span> charts · every post, in the order it was published</p>
    <div class="filters" id="filters"></div>
    <div class="grid" id="grid"></div>
  </div>
</section>

<footer>
  <div class="wrap">
    Educational research · not financial advice · not a signal service.
    The archive contains no outcome data: no win rate or PnL is claimed.
  </div>
</footer>

<div id="lb">
  <div class="inner">
    <div class="head">
      <span class="cap" id="lb-cap"></span>
      <span><button id="lb-prev">←</button> <button id="lb-next">→</button> <button id="lb-close">close</button></span>
    </div>
    <div id="lb-body"></div>
  </div>
</div>

<script id="data" type="application/json">__DATA__</script>
<script>
(function(){
  const DATA = JSON.parse(document.getElementById('data').textContent);
  const grid = document.getElementById('grid');
  const filters = document.getElementById('filters');
  const shown = document.getElementById('shown');
  let current = 'sessions', filtered = [], lbIndex = -1, lbStep = null;
  const SESSIONS = __SESSIONS__;

  const months = [...new Set(DATA.map(d => d.month))];
  const sum = arr => arr.reduce((n,d) => n + d.thumbs.length, 0);
  const multi = SESSIONS.length;
  const chipCount = k => k === 'sessions' ? multi
    : k === 'all' ? sum(DATA)
    : k === 'featured' ? sum(DATA.filter(d=>d.featured))
    : sum(DATA.filter(d=>d.month===k));
  const chips = [['sessions','Sessions'],['all','All charts'],['featured','Featured'],
                 ...months.map(m => [m, m.replace('-',' / ')])]
    .map(([k,l]) => [k, l + '  ' + chipCount(k)]);

  chips.forEach(([key,label]) => {
    const b = document.createElement('button');
    b.className = 'chip' + (key === current ? ' on' : '');
    b.textContent = label;
    b.onclick = () => { document.querySelectorAll('.chip').forEach(c => c.classList.remove('on'));
      b.classList.add('on'); current = key; render(); };
    filters.appendChild(b);
  });

  const MON = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  function humanDate(iso){
    const [y,m,d] = iso.split('-');
    return (+d) + ' ' + MON[+m - 1] + ' ' + y;
  }

  function render(){
    grid.innerHTML = '';
    if (current === 'sessions') { renderSessions(); return; }
    grid.className = 'grid';
    filtered = DATA.filter(d => current === 'all' ? true
      : current === 'featured' ? d.featured
      : d.month === current);
    shown.textContent = filtered.reduce((n,d) => n + d.thumbs.length, 0);
    const frag = document.createDocumentFragment();
    filtered.forEach((d, i) => {
      const t = document.createElement('div');
      t.className = 'tile';
      t.innerHTML = '<img loading="lazy" src="' + d.thumbs[0] + '" alt="">' +
        (d.thumbs.length > 1 ? '<span class="pair">PAIR</span>' : '') +
        '<div class="meta"><span>' + d.date + ' · ' + d.time + '</span><span>' + (d.symbol || '') + '</span></div>';
      t.onclick = () => openCard(i);
      frag.appendChild(t);
    });
    grid.appendChild(frag);
  }

  function renderSessions(){
    grid.className = 'grid cases';
    shown.textContent = SESSIONS.reduce((n,s) => n + s.frames, 0);
    const frag = document.createDocumentFragment();
    SESSIONS.forEach((s, idx) => {
      const el = document.createElement('div');
      el.className = 'case';
      const visible = Math.min(s.thumbs.length, 4);
      const shownImages = s.thumbs.length > 4 ? 3 : s.thumbs.length;
      const strip = s.thumbs.slice(0, shownImages).map(t => '<img loading="lazy" src="' + t + '" alt="">').join('');
      const extra = s.thumbs.length > 4 ? '<div class="more">+' + (s.thumbs.length - shownImages) + '</div>' : '';
      const cols = 'style="grid-template-columns:repeat(' + visible + ',1fr)"';
      el.innerHTML = '<div class="case-head"><b>' + humanDate(s.date) + '</b><span>' + s.frames +
        ' frames · ' + s.start.slice(11,16) + ' → ' + s.end.slice(11,16) +
        (s.symbols.length ? ' · ' + s.symbols.join(', ') : '') + '</span></div>' +
        '<div class="strip" ' + cols + '>' + strip + extra + '</div>';
      el.onclick = () => openSession(idx);
      frag.appendChild(el);
    });
    grid.appendChild(frag);
  }

  function showImages(urls, captionHtml){
    document.getElementById('lb-cap').innerHTML = captionHtml +
      ' · <a href="' + urls[0] + '" target="_blank" rel="noopener">open full size ↗</a>';
    document.getElementById('lb-body').innerHTML = urls.map(u => '<img loading="eager" src="' + u + '" alt="">').join('');
    document.getElementById('lb').classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function openCard(i){
    lbIndex = i; const d = filtered[i];
    showImages(d.full, d.date + ' ' + d.time + (d.caption ? ' — ' + d.caption : ''));
    lbStep = n => { lbIndex = (lbIndex + n + filtered.length) % filtered.length; openCard(lbIndex); };
  }

  function openSession(idx){
    const s = SESSIONS[idx];
    showImages(s.full, humanDate(s.date) + ' · ' + s.frames + ' frames · ' +
      s.start.slice(11,16) + ' → ' + s.end.slice(11,16));
    lbStep = n => { const next = (idx + n + SESSIONS.length) % SESSIONS.length; openSession(next); };
  }

  function close(){ document.getElementById('lb').classList.remove('open'); document.body.style.overflow = ''; }
  function step(n){ if (lbStep) lbStep(n); }

  document.getElementById('lb-close').onclick = close;
  document.getElementById('lb-prev').onclick = () => step(-1);
  document.getElementById('lb-next').onclick = () => step(1);
  document.addEventListener('keydown', e => {
    if (!document.getElementById('lb').classList.contains('open')) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowLeft') step(-1);
    if (e.key === 'ArrowRight') step(1);
  });
  document.getElementById('lb').addEventListener('click', e => { if (e.target.id === 'lb') close(); });

  render();
})();
</script>
</body>
</html>
"""


def main():
    shots = json.load(open("data/screenshots.json", encoding="utf-8"))
    signals = json.load(open("data/signals.json", encoding="utf-8"))

    # trim fields the page does not need, add thumbs
    slim = []
    for shot in shots:
        slim.append({
            "date": shot["date"][:10],
            "time": shot["date"][11:16],
            "month": shot["date"][:7],
            "caption": shot["caption"][:160],
            "symbol": "",
            "folder": shot["folder"],
            "images": shot["images"],
            "full": [os.path.join(shot["folder"], img) for img in shot["images"]],
            "featured": shot["folder"].split("/")[-1] in FEATURED,
        })

    make_thumbs(slim)

    # sessions: the frames that belong to one day's work (see scripts/link_images.py)
    try:
        linked = json.load(open("data/threads.json", encoding="utf-8"))
    except FileNotFoundError:
        linked = {"threads": []}
    by_folder = {entry["folder"]: entry for entry in slim}
    sessions = []
    for thread in linked["threads"]:
        if thread["frames"] < 2:
            continue
        thumbs, full = [], []
        for folder in thread["posts"]:
            entry = by_folder.get(folder)
            if not entry:
                continue
            thumbs += entry["thumbs"]
            full += entry["full"]
        sessions.append({
            "date": thread["date"],
            "frames": thread["frames"],
            "start": thread["start"],
            "end": thread["end"],
            "symbols": thread.get("symbols", []),
            "thumbs": thumbs,
            "full": full,
        })

    total = sum(len(s["thumbs"]) for s in slim)
    stats = [
        (str(total), "charts archived"),
        (str(len(slim)), "timestamped posts"),
        (str(len(signals)), "structured signals"),
        (f"{sum(s['rr'] for s in signals)/len(signals):.2f}R", "average design R:R"),
    ]
    stats_html = "".join(f'<div class="stat"><b>{v}</b><span>{k}</span></div>' for v, k in stats)

    rows = []
    for s in signals:
        rows.append(
            "<tr>"
            f"<td>{s['date'][:10]}</td>"
            f"<td>{html.escape(s['symbol'] or '—')}</td>"
            f"<td class='{s['side']}'>{(s['side'] or '').upper()}</td>"
            f"<td class='num'>{s['entry']}</td>"
            f"<td class='num'>{s['tp']}</td>"
            f"<td class='num'>{s['sl']}</td>"
            f"<td class='num'>{s['rr']:.2f}</td>"
            f"<td>{html.escape(s['reason'] or '—')}</td>"
            "</tr>"
        )

    page = (PAGE.replace("__STATS__", stats_html)
                .replace("__SIGNALS__", "".join(rows))
                .replace("__COUNT__", str(total))
                .replace("__SESSIONS__", json.dumps(sessions, ensure_ascii=False))
                .replace("__DATA__", json.dumps(slim, ensure_ascii=False)))

    with open("index.html", "w", encoding="utf-8") as fh:
        fh.write(page)

    print(f"index.html written | thumbs: {sum(len(s['thumbs']) for s in slim)} | "
          f"size: {os.path.getsize('index.html')/1024:.0f} KB")


if __name__ == "__main__":
    main()
