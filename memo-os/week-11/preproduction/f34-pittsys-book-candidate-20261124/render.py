"""Set F34 from the Week 11 reader manuscript, keeping all figures as editable type."""
from functools import cache
from pathlib import Path
import subprocess

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent
MANUSCRIPT = ROOT.parent / "W11_READER_LETTERING_2026-11-24.md"
W, H = 1080, 1920
LEFT, RIGHT = 60, 1020
PAPER, INK, COPPER, LINE = "#f3ebd6", "#222620", "#84401e", "#a49672"
DARK, WHITE, GOLD = "#182b26", "#fff4dd", "#dfb578"


@cache
def font(style, size):
    name = {"text": "Nimbus Sans Narrow", "label": "Nimbus Sans Narrow:style=Bold",
            "display": "Nimbus Roman", "quote": "Nimbus Roman:style=Italic"}[style]
    path = subprocess.check_output(["fc-match", "-f", "%{file}", name], text=True)
    return ImageFont.truetype(path, size)


def put(x, y, text, style, size, color, anchor="lt"):
    f = font(style, size)
    box = draw.textbbox((x, y), text, font=f, anchor=anchor)
    assert box[0] >= 0 and box[2] <= W and box[3] <= H, (text, box)
    draw.text((x, y), text, fill=color, font=f, anchor=anchor)


def paragraph(text, y, style, size, line_height, color, width=RIGHT-LEFT):
    f = font(style, size)
    lines = []
    for word in text.split():
        if lines and f.getlength(lines[-1] + " " + word) <= width:
            lines[-1] += " " + word
        else:
            lines.append(word)
    for line in lines:
        put(LEFT, y, line, style, size, color)
        y += line_height
    return y


def rule(y):
    draw.line((LEFT, y, RIGHT, y), fill=LINE, width=2)


source = MANUSCRIPT.read_text().split("## F34 · ", 1)[1].split("## F35", 1)[0].strip()
title, body = source.split("\n\n", 1)
board, markets, off_board, undeclared, terms, first_quote, settlement, last_quote = body.split("\n\n")
rows = [[c.strip() for c in row.strip("|").split("|")] for row in markets.splitlines()]
im = Image.new("RGB", (W, H), PAPER)
draw = ImageDraw.Draw(im)
draw.rectangle((0, 0, W, 185), fill=DARK)
put(LEFT, 35, "SCHEMIN’ ’26", "label", 37, WHITE)
put(W//2, 38, "One Last Crossing", "quote", 34, WHITE, "mt")
put(RIGHT, 35, "WEEK 11   /   34", "label", 35, WHITE, "rt")
put(LEFT, 89, title, "display", 99, WHITE)
photo = Image.open(ROOT / "plate.png").convert("RGB")
im.paste(ImageOps.fit(photo, (W, 635), method=Image.Resampling.LANCZOS, centering=(0.5, 0.53)), (0, 193))
put(LEFT, 856, board.strip("*"), "display", 61, INK)
put(LEFT, 939, rows[0][0].upper(), "label", 31, COPPER)
put(RIGHT, 939, rows[0][1].upper(), "label", 31, COPPER, "rt")
y = 988
for sides, total in rows[2:]:
    rule(y-13)
    put(LEFT, y, sides, "text", 42, INK)
    put(RIGHT, y, total, "label", 42, INK, "rt")
    y += 57
rule(y-12)
y = paragraph(off_board, y+8, "label", 34, 39, INK) + 9
y = paragraph(undeclared, y, "text", 34, 39, INK) + 13
y = paragraph(terms, y, "text", 34, 39, INK) + 14
y = paragraph(first_quote, y, "quote", 39, 43, COPPER) + 13
heading, proceeds = settlement.split("** · ", 1)
draw.rectangle((0, y, W, H), fill=DARK)
y += 25
put(LEFT, y, heading.strip("*").upper(), "label", 32, GOLD)
y += 54
y = paragraph(proceeds, y, "text", 42, 47, WHITE) + 19
y = paragraph(last_quote, y, "quote", 43, 46, WHITE)
assert y < H-12, y
im.save(ROOT / "F34.png", optimize=True)
im.resize((390, 693), Image.Resampling.LANCZOS).save(ROOT / "F34-390.png", optimize=True)
