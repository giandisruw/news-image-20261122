#!/usr/bin/env python3
"""Draw the front page for Sunday 22 November 2026.

Self-contained: reads nothing but the story text below, uses only the
standard library plus Pillow, touches no network, no clock and no
randomness, so running it twice produces identical bytes. Writes
entry.png next to this file (or to the path in --out).
"""

import argparse
import os
import sys

from PIL import Image, ImageDraw, ImageFont

PAGE_W = 1024
PAGE_H = 1024
SIDE = 36
COL_W = PAGE_W - 2 * SIDE  # 952

PAPER = (248, 244, 232)
INK = (17, 17, 17)
ACCENT = (138, 20, 20)
MUTED = (98, 92, 82)
BAND = (26, 26, 26)
BAND_TEXT = (241, 239, 231)

LIB = "/usr/share/fonts/truetype/liberation"


def load(name, size):
    return ImageFont.truetype(os.path.join(LIB, name), size)


SERIF_BOLD = "LiberationSerif-Bold.ttf"
SERIF_REG = "LiberationSerif-Regular.ttf"
SERIF_ITAL = "LiberationSerif-Italic.ttf"
SANS_BOLD = "LiberationSans-Bold.ttf"
SANS_REG = "LiberationSans-Regular.ttf"

F_NAMEPLATE = load(SERIF_BOLD, 80)
F_DATELINE = load(SANS_BOLD, 26)
F_STRAP = load(SANS_REG, 14)
F_LABEL = load(SANS_BOLD, 19)
F_TOP_HEAD = load(SERIF_BOLD, 48)
F_TOP_DEK = load(SERIF_ITAL, 22)
F_TOP_TEXT = load(SERIF_REG, 16)
F_STRIP = load(SANS_BOLD, 14)
F_HEAD = load(SERIF_BOLD, 29)
F_HEAD_SMALL = load(SERIF_BOLD, 23)
F_TEXT = load(SERIF_REG, 16)
F_TEXT_SMALL = load(SERIF_REG, 15)
F_TAPE = load(SANS_BOLD, 15)
F_FOOT = load(SANS_REG, 13)


def fit_lines(draw, text, face, width):
    """Greedy wrap of one paragraph into lines no wider than width."""
    out = []
    for chunk in text.split("\n"):
        words = chunk.split()
        if not words:
            out.append("")
            continue
        line = words[0]
        for word in words[1:]:
            test = line + " " + word
            if draw.textlength(test, font=face) <= width:
                line = test
            else:
                out.append(line)
                line = word
        out.append(line)
    return out


def draw_para(draw, x, y, width, text, face, step, colour=INK):
    for line in fit_lines(draw, text, face, width):
        draw.text((x, y), line, font=face, fill=colour)
        y += step
    return y


def hline(draw, y, weight=2, x0=None, x1=None):
    x0 = SIDE if x0 is None else x0
    x1 = PAGE_W - SIDE if x1 is None else x1
    draw.line([(x0, y), (x1, y)], fill=INK, width=weight)
    return y + weight


def double_hline(draw, y):
    hline(draw, y, 3)
    hline(draw, y + 6, 1)
    return y + 10


def draw_label(draw, x, y, text):
    draw.text((x, y), text, font=F_LABEL, fill=ACCENT)
    return y + 26


def draw_story(draw, x, y, width, label, headline, body,
               head_face, head_step, body_face=F_TEXT, body_step=20):
    y = draw_label(draw, x, y, label)
    for line in fit_lines(draw, headline, head_face, width):
        draw.text((x, y), line, font=head_face, fill=INK)
        y += head_step
    y += 2
    return draw_para(draw, x, y, width, body, body_face, body_step)


# ---------------------------------------------------------------- stories

TOP_LABEL = "GULF OF FINLAND  \u2014  THE BALTIC SEA"
TOP_HEAD = "DRONES SET RUSSIAN SHIP ABLAZE"
TOP_DEK = ("Finland says Ukraine was likely behind the strike on the "
           "sanctioned Sparta II \u2014 as the war's shadow spreads "
           "across the Baltic.")
TOP_LEFT = ("GULF OF FINLAND \u2014 Two drones struck the sanctioned "
            "Russian cargo ship Sparta II on Saturday morning, west of "
            "Gogland island. The ship caught fire and drifted into "
            "Finnish waters.")
TOP_RIGHT = ("All 16 crew were evacuated to lifeboats and then to a "
             "nearby Russian ship. Finland tightened air and sea rules "
             "in the eastern gulf, and a Russian helicopter was also "
             "reported inside Finnish airspace.")
TOP_STRIP = ("2 DRONES HIT SPARTA II  \u00b7  16 CREW SAFE  \u00b7  "
             "BOUND FOR KALININGRAD  \u00b7  US-SANCTIONED SHIP")

PAIR_A = [
    ("KRYVYI RIH",
     "DOUBLE-TAP KILLS TWO",
     "A Russian attack on President Zelenskyy's hometown killed a "
     "7-year-old boy and a 20-year-old paramedic and wounded 60, "
     "hitting rescuers as they worked. About 25 apartment blocks, a "
     "hospital and schools were damaged."),
    ("SINALOA",
     "MEXICO SEIZES \u2018EL CHAPO ISIDRO\u2019",
     "Mexican forces captured FBI most-wanted cartel boss Fausto "
     "Isidro Meza Flores in Guasave, with US intelligence help. "
     "Eleven people died in the fighting \u2014 four soldiers and "
     "seven gunmen \u2014 as cartel roadblocks burned."),
]

TRIO = [
    ("PERU",
     "6.9 QUAKE SHAKES PERU",
     "A magnitude 6.9 earthquake struck central Peru at 00:09 UTC on "
     "Saturday, 34 km north of Junin. It was felt in Lima; no damage "
     "or casualties were reported."),
    ("ANTALYA",
     "COP31 PAST DEADLINE",
     "Climate talks ran into overtime with no deal, as the draft "
     "dropped all mention of fossil fuels. The EU warned it would "
     "be \u201ca good deal or no deal at all\u201d."),
    ("WASHINGTON",
     "FBI DATABASE HACKED",
     "Hackers broke into the FBI's National Crime Information "
     "Center, used by police across the US. Trump called it "
     "\u201cnot good\u201d; it is the second FBI breach in months."),
]

PAIR_B = [
    ("TOKYO",
     "ASIAN MARKETS PLUNGE",
     "Japan's Nikkei fell 5.06% and South Korea's Kospi 5.21% on "
     "Friday as the AI sell-off spread from Wall Street. Taiwan's "
     "Taiex lost 6.2% in a day and 17.5% in the week."),
    ("BASRA",
     "PLANT FIRE KILLS FOUR",
     "At least four people were killed and 35 injured when a gas "
     "pipeline blast set the Hartha power station ablaze on "
     "Saturday. The fire spread to nearby homes."),
]

TAPE_LINES = [
    "HORMUZ \u00b7 Two more tankers hit by unknown projectiles near "
    "Khasab on Saturday, 50 minutes apart \u00b7 No casualties reported",
    "SHENZHEN \u00b7 Trump posts \u201cThe Great Powers 1945, 2026\u201d, "
    "pairing Yalta with his summit with Xi and Putin",
    "KYIV \u00b7 Zelenskyy rebukes Trump for calling Putin a \u2018friend\u2019 "
    "\u2014 \u201cTo us, he is the killer\u201d",
]


def render():
    img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- nameplate -----------------------------------------------------
    y = 20
    name = "THE WORLD"
    nw = d.textlength(name, font=F_NAMEPLATE)
    d.text(((PAGE_W - nw) / 2, y), name, font=F_NAMEPLATE, fill=INK)
    y += 86
    dateline = "SUNDAY  22  NOVEMBER  2026"
    dw = d.textlength(dateline, font=F_DATELINE)
    d.text(((PAGE_W - dw) / 2, y), dateline, font=F_DATELINE, fill=ACCENT)
    y += 34
    strap = "THE DAY\u2019S WORLD NEWS IN ONE PAGE"
    sw = d.textlength(strap, font=F_STRAP)
    d.text(((PAGE_W - sw) / 2, y), strap, font=F_STRAP, fill=MUTED)
    y += 18
    y = double_hline(d, y)
    y += 4

    # ---- top story -----------------------------------------------------
    y = draw_label(d, SIDE, y, TOP_LABEL)
    for line in fit_lines(d, TOP_HEAD, F_TOP_HEAD, COL_W):
        d.text((SIDE, y), line, font=F_TOP_HEAD, fill=INK)
        y += 54
    y += 2
    y = draw_para(d, SIDE, y, COL_W, TOP_DEK, F_TOP_DEK, 27)
    y += 6
    half = (COL_W - 24) // 2
    end_l = draw_para(d, SIDE, y, half, TOP_LEFT, F_TOP_TEXT, 20)
    end_r = draw_para(d, SIDE + half + 24, y, half, TOP_RIGHT, F_TOP_TEXT, 20)
    y = max(end_l, end_r) + 5
    sw = d.textlength(TOP_STRIP, font=F_STRIP)
    d.text(((PAGE_W - sw) / 2, y), TOP_STRIP, font=F_STRIP, fill=ACCENT)
    y += 20
    y = hline(d, y, 2)
    y += 6

    # ---- pair A: two stories ------------------------------------------
    half = (COL_W - 28) // 2
    e1 = draw_story(d, SIDE, y, half, PAIR_A[0][0], PAIR_A[0][1],
                    PAIR_A[0][2], F_HEAD, 33)
    e2 = draw_story(d, SIDE + half + 28, y, half, PAIR_A[1][0],
                    PAIR_A[1][1], PAIR_A[1][2], F_HEAD, 33)
    y = max(e1, e2) + 3
    y = hline(d, y, 1)
    y += 6

    # ---- trio: three stories ------------------------------------------
    third = (COL_W - 2 * 24) // 3
    ends = []
    for i, (label, head, body) in enumerate(TRIO):
        x = SIDE + i * (third + 24)
        ends.append(draw_story(d, x, y, third, label, head, body,
                               F_HEAD_SMALL, 27, F_TEXT_SMALL, 18))
    y = max(ends) + 3
    y = hline(d, y, 1)
    y += 6

    # ---- pair B: two stories ------------------------------------------
    half = (COL_W - 28) // 2
    e1 = draw_story(d, SIDE, y, half, PAIR_B[0][0], PAIR_B[0][1],
                    PAIR_B[0][2], F_HEAD, 33, F_TEXT, 19)
    e2 = draw_story(d, SIDE + half + 28, y, half, PAIR_B[1][0],
                    PAIR_B[1][1], PAIR_B[1][2], F_HEAD, 33, F_TEXT, 19)
    y = max(e1, e2) + 4

    # ---- news tape ------------------------------------------------------
    band_top = y
    band_h = 84
    d.rectangle([(SIDE, band_top), (PAGE_W - SIDE, band_top + band_h)],
                fill=BAND)
    ty = band_top + 8
    for line in TAPE_LINES:
        for seg in fit_lines(d, line, F_TAPE, COL_W - 20):
            d.text((SIDE + 10, ty), seg, font=F_TAPE, fill=BAND_TEXT)
            ty += 20
    y = band_top + band_h + 6

    # ---- footer: what the page covers and where it comes from ----------
    foot = ("REPORTED 21\u201322 NOVEMBER 2026  \u00b7  SOURCES: REUTERS, AP, "
            "CNN, USGS, UKMTO, IRAQ SECURITY MEDIA CELL")
    fw = d.textlength(foot, font=F_FOOT)
    d.text(((PAGE_W - fw) / 2, y), foot, font=F_FOOT, fill=MUTED)
    y += 14

    if y > PAGE_H - 8:
        raise SystemExit("layout overflow: content ends at y=%d" % y)
    return img


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    args = ap.parse_args(argv)
    out = args.out or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = render()
    img.save(out, format="PNG", optimize=True)
    print("wrote %s (%dx%d)" % (out, PAGE_W, PAGE_H))
    return 0


if __name__ == "__main__":
    sys.exit(main())
