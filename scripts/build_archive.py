#!/usr/bin/env python3
"""
Build the Algo NDS signal archive from a Telegram Desktop JSON export.

Usage:
    python3 scripts/build_archive.py "/path/to/DataExport_YYYY-MM-DD" [--chat "Chat name"]

What it does
------------
1. Reads result.json from the export.
2. Takes every photo message of the selected chat and groups photos posted in
   the same minute (a "before / after" pair is usually two photos in one post).
3. Writes one folder per group under archive/YYYY-MM/YYYY-MM-DD_HHMM/ with the
   image(s) and a meta.json holding the verbatim caption + timestamp.
4. Writes data/screenshots.json (machine readable index).
5. Writes data/signals.json (structured signals parsed from message text).
6. Regenerates INDEX.md and SIGNALS.md tables.

Nothing is invented: every field comes straight from the export. Fields that the
export does not contain (pair, timeframe, outcome) are left null.
"""

import argparse
import json
import os
import re
import shutil
import sys
from datetime import datetime

ARCHIVE_DIR = "archive"
DATA_DIR = "data"


def flatten(text):
    """Telegram exports rich text as a list of strings and dicts."""
    if isinstance(text, str):
        return text
    if not text:
        return ""
    out = []
    for part in text:
        if isinstance(part, str):
            out.append(part)
        elif isinstance(part, dict):
            out.append(part.get("text", ""))
    return "".join(out)


def load_chat(export_dir, chat_name=None):
    with open(os.path.join(export_dir, "result.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    chats = data["chats"]["list"]
    if chat_name:
        for chat in chats:
            if chat.get("name") == chat_name:
                return chat, data
        sys.exit(f'chat not found: {chat_name!r} — available: {[c.get("name") for c in chats]}')
    # default: the chat with the most messages
    return max(chats, key=lambda c: len(c.get("messages", []))), data


def group_photos(photos):
    """Group consecutive photo messages posted within the same minute."""
    groups, current = [], []
    for msg in photos:
        key = msg["date"][:16]
        if current and current[-1]["date"][:16] == key:
            current.append(msg)
        else:
            if current:
                groups.append(current)
            current = [msg]
    if current:
        groups.append(current)
    return groups


def parse_signals(messages):
    """Pull structured 'NDS SIGNAL' blocks out of message text."""
    signals = []
    for msg in messages:
        text = flatten(msg.get("text"))
        if "NDS SIGNAL" not in text:
            continue

        def grab(pattern):
            m = re.search(pattern, text)
            return m.group(1).strip() if m else None

        side = grab(r"Side:\s*(BUY|SELL)")
        signals.append({
            "date": msg["date"],
            "message_id": msg.get("id"),
            "symbol": grab(r"💎\s*(\S+)"),
            "side": side.lower() if side else None,
            "entry": float(grab(r"Entry:\s*([\d.]+)")) if grab(r"Entry:\s*([\d.]+)") else None,
            "tp": float(grab(r"TP:\s*([\d.]+)")) if grab(r"TP:\s*([\d.]+)") else None,
            "sl": float(grab(r"SL:\s*([\d.]+)")) if grab(r"SL:\s*([\d.]+)") else None,
            "rr": float(grab(r"R:R:\s*([\d.]+)")) if grab(r"R:R:\s*([\d.]+)") else None,
            "reason": grab(r"Reason:\s*(.+)"),
            # the export never states the outcome — do not guess it
            "outcome": None,
            "raw": text,
        })
    return signals


def build(export_dir, chat_name):
    chat, _ = load_chat(export_dir, chat_name)
    messages = chat.get("messages", [])
    photos = [m for m in messages if m.get("photo")]

    for directory in (ARCHIVE_DIR, DATA_DIR):
        if os.path.isdir(directory):
            shutil.rmtree(directory)
    os.makedirs(ARCHIVE_DIR)
    os.makedirs(DATA_DIR)

    entries = []
    for group in group_photos(photos):
        first = group[0]
        stamp = first["date"][:16].replace("T", "_").replace(":", "")
        month = first["date"][:7]
        folder = os.path.join(ARCHIVE_DIR, month, stamp)
        os.makedirs(folder, exist_ok=True)

        images = []
        for index, msg in enumerate(group, start=1):
            src = os.path.join(export_dir, msg["photo"])
            name = f"{index:02d}.jpg"
            shutil.copyfile(src, os.path.join(folder, name))
            images.append(name)

        meta = {
            "date": first["date"],
            "date_unixtime": first.get("date_unixtime"),
            "message_id": first.get("id"),
            "from": first.get("from"),
            "caption": flatten(first.get("text")).strip(),
            "caption_other": [flatten(m.get("text")).strip() for m in group[1:] if flatten(m.get("text")).strip()],
            "images": images,
            "folder": folder,
        }
        with open(os.path.join(folder, "meta.json"), "w", encoding="utf-8") as fh:
            json.dump(meta, fh, ensure_ascii=False, indent=2)
        entries.append(meta)

    with open(os.path.join(DATA_DIR, "screenshots.json"), "w", encoding="utf-8") as fh:
        json.dump(entries, fh, ensure_ascii=False, indent=2)

    signals = parse_signals(messages)
    with open(os.path.join(DATA_DIR, "signals.json"), "w", encoding="utf-8") as fh:
        json.dump(signals, fh, ensure_ascii=False, indent=2)

    write_index(entries)
    write_signals_table(signals)
    write_highlights(entries)

    print(f"chat: {chat.get('name')} | messages: {len(messages)} | photos: {len(photos)}")
    print(f"groups: {len(entries)} | images: {sum(len(e['images']) for e in entries)} | signals: {len(signals)}")


def write_index(entries):
    lines = ["# Screenshot index", "",
             "Every screenshot in the archive, in chronological order. "
             "Captions are verbatim from the original post (Persian where the original was Persian).", "",
             "| # | Date | Time | Caption | Files |", "|---|---|---|---|---|"]
    for i, e in enumerate(entries, start=1):
        dt = datetime.fromisoformat(e["date"])
        caption = (e["caption"] or "—").replace("|", "\\|").replace("\n", " ")[:80]
        link = os.path.join(e["folder"], "")
        lines.append(f"| {i} | {dt:%Y-%m-%d} | {dt:%H:%M} | [{caption}]({link}) | {len(e['images'])} |")
    with open("INDEX.md", "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def write_signals_table(signals):
    lines = ["# Structured signals", "",
             "Machine-readable signals posted by the engine (the `NDS SIGNAL` block format). "
             "Entry / TP / SL / R:R are exactly as posted; the export carries no outcome field, "
             "so results are not claimed here.", "",
             "| Date | Symbol | Side | Entry | TP | SL | R:R | Reason |", "|---|---|---|---|---|---|---|---|"]
    for s in signals:
        lines.append(
            f"| {s['date'][:16].replace('T', ' ')} | {s['symbol'] or '—'} | {(s['side'] or '—').upper()} | "
            f"{s['entry']} | {s['tp']} | {s['sl']} | {s['rr']} | {s['reason'] or '—'} |"
        )
    with open("SIGNALS.md", "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


HIGHLIGHTS = [
    # (caption substring or None, why)
    ("", ""),
]


def write_highlights(entries):
    """Pick a handful of representative frames and write HIGHLIGHTS.md."""
    picks = []
    for e in entries:
        if e["caption"] and any(k in e["caption"] for k in ("نمونه سیگنال", "NMT Algo", "TP", "نتیجه")):
            picks.append(e)
    picks = picks[:8]
    lines = ["# Highlights", "",
             "A few frames that show the system end to end.", ""]
    for e in picks:
        dt = datetime.fromisoformat(e["date"])
        lines.append(f"### {dt:%Y-%m-%d %H:%M} — {e['caption'] or 'no caption'}")
        for img in e["images"]:
            lines.append(f"![{dt:%Y-%m-%d %H:%M}]({os.path.join(e['folder'], img)})")
        lines.append("")
    with open("HIGHLIGHTS.md", "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("export_dir")
    parser.add_argument("--chat", default=None)
    args = parser.parse_args()
    build(args.export_dir, args.chat)
