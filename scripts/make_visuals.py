#!/usr/bin/env python3
"""Generate the presentation graphics used by README.md.

Outputs to docs/:
  hero.png        banner: title + stats + a strip of real frames
  anatomy.png     three crops of one frame, showing what the panel reports
  rr.svg          R:R of the 15 structured signals
  timeline.svg    posting activity per month

Only Pillow is required. Everything is drawn from data already in the repo,
so re-running this after a new export gives fresh graphics.
"""

import json
import os

from PIL import Image, ImageDraw, ImageFont

DOCS = "docs"
FONT_DIR = "/System/Library/Fonts/Supplemental"
BG = (11, 14, 20)
FG = (232, 238, 245)
MUTED = (138, 150, 168)
CYAN = (34, 211, 238)
AMBER = (245, 197, 24)


def font(name, size):
    for candidate in (os.path.join(FONT_DIR, name), os.path.join("/System/Library/Fonts", name)):
        if os.path.exists(candidate):
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def hero(frames, stats):
    width, height = 1600, 560
    canvas = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(canvas)

    # accent rule
    draw.rectangle([0, 0, width, 6], fill=CYAN)

    draw.text((70, 96), "ALGO NDS", font=font("Arial Bold.ttf", 104), fill=FG)
    draw.text((74, 226), "Precision entries from nodal structure",
              font=font("Arial.ttf", 34), fill=CYAN)
    draw.text((74, 292), "Price is not read as candles. It is read as a sequence of",
              font=font("Arial.ttf", 24), fill=MUTED)
    draw.text((74, 324), "displacements between computed nodes — and the next node",
              font=font("Arial.ttf", 24), fill=MUTED)
    draw.text((74, 356), "is the target.",
              font=font("Arial.ttf", 24), fill=MUTED)

    # stat pills
    x = 74
    for value, label in stats:
        draw.text((x, 438), value, font=font("Arial Bold.ttf", 40), fill=AMBER)
        draw.text((x, 488), label, font=font("Arial.ttf", 20), fill=MUTED)
        x += 210

    # right-hand collage
    thumbs = frames[:2]
    if thumbs:
        tw, th, gap = 340, 230, 16
        start_x = width - (tw + gap) * len(thumbs) - 60 + gap
        y = 118
        for i, path in enumerate(thumbs):
            try:
                im = Image.open(path).convert("RGB")
            except OSError:
                continue
            ratio = max(tw / im.width, th / im.height)
            im = im.resize((int(im.width * ratio) + 1, int(im.height * ratio) + 1))
            left = (im.width - tw) // 2
            top = (im.height - th) // 2
            im = im.crop((left, top, left + tw, top + th))
            canvas.paste(im, (start_x + i * (tw + gap), y))
            draw.rectangle([start_x + i * (tw + gap), y, start_x + i * (tw + gap) + tw, y + th],
                           outline=(45, 55, 72), width=2)

    canvas.save(os.path.join(DOCS, "hero.png"), quality=92)


def anatomy(source):
    """Three crops of one real frame, stacked with captions."""
    im = Image.open(source).convert("RGB")
    w, h = im.size

    panel = im.crop((0, 0, w, 120))
    levels = im.crop((int(w * 0.86), int(h * 0.33), w, int(h * 0.80)))
    hooks = im.crop((int(w * 0.22), int(h * 0.28), int(w * 0.62), int(h * 0.66)))

    blocks = [
        (panel, "1 · PRICE / PREDICTION / FRACTAL — the three numbers the engine recomputes on every candle"),
        (levels, "2 · TP / ENTRY / SL — the next node becomes the target, the stop is sized from GARCH volatility"),
        (hooks, "3 · HOOK− / HOOK+ — where the sequence flips and the read is invalidated"),
    ]

    pad, cap_h = 34, 52
    target_w = 1500
    rendered = []
    for crop, caption in blocks:
        ratio = target_w / crop.width
        resized = crop.resize((target_w, max(1, int(crop.height * ratio))))
        rendered.append((resized, caption))

    total_h = pad + sum(c.height + cap_h for c, _ in rendered) + pad
    canvas = Image.new("RGB", (target_w + pad * 2, total_h), BG)
    draw = ImageDraw.Draw(canvas)
    cap_font = font("Arial.ttf", 21)

    y = pad
    for crop, caption in rendered:
        canvas.paste(crop, (pad, y + cap_h))
        draw.text((pad, y + 14), caption, font=cap_font, fill=MUTED)
        y += crop.height + cap_h
        draw.rectangle([pad, y - 6, pad + target_w, y - 6], fill=(30, 38, 52))

    canvas.save(os.path.join(DOCS, "anatomy.png"), quality=92)


def rr_chart(signals):
    signals = sorted([s for s in signals if s.get("rr")], key=lambda s: s["rr"])
    bar_h, gap, left, right, top = 26, 12, 190, 90, 74
    width = 1000
    height = top + len(signals) * (bar_h + gap) + 60
    max_rr = max(s["rr"] for s in signals)
    plot_w = width - left - right

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
             f'viewBox="0 0 {width} {height}" font-family="Helvetica,Arial,sans-serif">',
             f'<rect width="{width}" height="{height}" fill="#0b0e14"/>',
             f'<text x="24" y="38" fill="#e8eef5" font-size="20" font-weight="bold">'
             f'Designed R:R per signal</text>',
             f'<text x="24" y="60" fill="#8a96a8" font-size="13">'
             f'13–22 Dec 2025 · target at the next node · stop at GARCH volatility</text>']

    for i, s in enumerate(signals):
        y = top + i * (bar_h + gap)
        w = (s["rr"] / max_rr) * plot_w
        colour = "#22d3ee" if s["side"] == "buy" else "#f5c518"
        label = f'{s["symbol"]} · {s["side"].upper()}'
        parts.append(f'<text x="24" y="{y + bar_h - 8}" fill="#c7d2e0" font-size="13">{label}</text>')
        parts.append(f'<rect x="{left}" y="{y}" width="{w:.1f}" height="{bar_h}" rx="4" fill="{colour}" opacity="0.9"/>')
        parts.append(f'<text x="{left + w + 10:.1f}" y="{y + bar_h - 8}" fill="#e8eef5" '
                     f'font-size="13" font-weight="bold">{s["rr"]:.2f}</text>')

    avg = sum(s["rr"] for s in signals) / len(signals)
    avg_x = left + (avg / max_rr) * plot_w
    parts.append(f'<line x1="{avg_x:.1f}" y1="{top - 8}" x2="{avg_x:.1f}" '
                 f'y2="{height - 40}" stroke="#8a96a8" stroke-dasharray="4 4"/>')
    parts.append(f'<text x="{avg_x + 6:.1f}" y="{height - 22}" fill="#8a96a8" font-size="12">'
                 f'avg {avg:.2f}R</text>')
    parts.append("</svg>")

    with open(os.path.join(DOCS, "rr.svg"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(parts))


def timeline(shots):
    counts = {}
    for shot in shots:
        counts[shot["date"][:7]] = counts.get(shot["date"][:7], 0) + 1

    months = []
    year, month = 2025, 9
    while (year, month) <= (2026, 10):
        months.append(f"{year}-{month:02d}")
        month += 1
        if month == 13:
            year, month = year + 1, 1

    width, height = 1000, 300
    left, right, top, bottom = 56, 30, 56, 64
    plot_w = width - left - right
    plot_h = height - top - bottom
    max_c = max(counts.values())
    slot = plot_w / len(months)

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
             f'viewBox="0 0 {width} {height}" font-family="Helvetica,Arial,sans-serif">',
             f'<rect width="{width}" height="{height}" fill="#0b0e14"/>',
             f'<text x="24" y="32" fill="#e8eef5" font-size="20" font-weight="bold">'
             f'Posts per month</text>',
             f'<line x1="{left}" y1="{top + plot_h}" x2="{width - right}" y2="{top + plot_h}" '
             f'stroke="#2a3444"/>']

    for i, key in enumerate(months):
        value = counts.get(key, 0)
        x = left + i * slot + slot * 0.2
        bar_w = slot * 0.6
        h = (value / max_c) * plot_h if value else 0
        if h:
            parts.append(f'<rect x="{x:.1f}" y="{top + plot_h - h:.1f}" width="{bar_w:.1f}" '
                         f'height="{h:.1f}" rx="3" fill="#22d3ee" opacity="0.85"/>')
            parts.append(f'<text x="{x + bar_w / 2:.1f}" y="{top + plot_h - h - 7:.1f}" '
                         f'fill="#e8eef5" font-size="12" text-anchor="middle">{value}</text>')
        else:
            parts.append(f'<text x="{x + bar_w / 2:.1f}" y="{top + plot_h - 7}" '
                         f'fill="#4a5566" font-size="11" text-anchor="middle">·</text>')
        label = key[2:].replace("-", "/")
        parts.append(f'<text x="{x + bar_w / 2:.1f}" y="{height - 34}" fill="#8a96a8" '
                     f'font-size="11" text-anchor="middle">{label}</text>')

    parts.append("</svg>")
    with open(os.path.join(DOCS, "timeline.svg"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(parts))


def main():
    os.makedirs(DOCS, exist_ok=True)
    shots = json.load(open("data/screenshots.json", encoding="utf-8"))
    signals = json.load(open("data/signals.json", encoding="utf-8"))

    picks = [
        "archive/2025-11/2025-11-30_2041/01.jpg",   # engine panel with TP / ENTRY / SL
        "archive/2025-10/2025-10-01_1050/01.jpg",   # early overlay
        "archive/2026-02/2026-02-15_1238/01.jpg",   # AI prediction readout
    ]
    frames = [p for p in picks if os.path.exists(p)]

    hero(frames, [
        (str(len(shots)), "timestamped posts"),
        (str(sum(len(s["images"]) for s in shots)), "charts archived"),
        (str(len(signals)), "structured signals"),
        (f'{sum(s["rr"] for s in signals) / len(signals):.2f}R', "average design R:R"),
    ])
    rr_chart(signals)
    timeline(shots)
    print("wrote docs/hero.png, docs/rr.svg, docs/timeline.svg")


if __name__ == "__main__":
    main()
