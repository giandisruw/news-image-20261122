#!/usr/bin/env python3
"""Render the front page for Sunday 22 November 2026.

This script draws the whole newspaper page — nameplate, lead story,
seven further stories and a closing news tape — and saves it as
``entry.png`` next to this file (or to the path given with ``--out``).

It is fully self-contained and deterministic: the only input is the
story text written below, the only libraries are the standard library
and Pillow, and there is no network access, no clock reading and no
randomness. Running it twice therefore produces byte-identical PNGs.

    python3 build_image.py
"""

import argparse
import os
import sys

from PIL import Image, ImageDraw, ImageFont

# --- page geometry -------------------------------------------------------
WIDTH = 1024
HEIGHT = 1024
MARGIN = 36
TEXT_WIDTH = WIDTH - 2 * MARGIN  # 952

# --- palette -------------------------------------------------------------
PAPER = (248, 244, 232)
INK = (17, 17, 17)
RED = (138, 20, 20)
GREY = (98, 92, 82)
TAPE_BG = (26, 26, 26)
TAPE_FG = (241, 239, 231)

FONT_DIR = "/usr/share/fonts/truetype/liberation"


def font(filename, size):
    """Load one Liberation font at the requested point size."""
    return ImageFont.truetype(os.path.join(FONT_DIR, filename), size)


FONTS = {
    "nameplate": font("LiberationSerif-Bold.ttf", 80),
    "dateline": font("LiberationSans-Bold.ttf", 26),
    "strap": font("LiberationSans-Regular.ttf", 14),
    "kicker": font("LiberationSans-Bold.ttf", 19),
    "lead_head": font("LiberationSerif-Bold.ttf", 48),
    "lead_dek": font("LiberationSerif-Italic.ttf", 22),
    "lead_body": font("LiberationSerif-Regular.ttf", 16),
    "ticker": font("LiberationSans-Bold.ttf", 14),
    "head": font("LiberationSerif-Bold.ttf", 29),
    "head_small": font("LiberationSerif-Bold.ttf", 23),
    "body": font("LiberationSerif-Regular.ttf", 16),
    "body_small": font("LiberationSerif-Regular.ttf", 15),
    "tape": font("LiberationSans-Bold.ttf", 15),
    "footer": font("LiberationSans-Regular.ttf", 13),
}


# --- text helpers --------------------------------------------------------


def wrap(draw, text, face, width):
    """Split *text* greedily into lines that fit *width* pixels."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            candidate = current + " " + word
            if draw.textlength(candidate, font=face) <= width:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def paragraph(draw, x, y, width, text, face, leading, colour=INK):
    """Draw a wrapped paragraph; return the y just below its last line."""
    for line in wrap(draw, text, face, width):
        draw.text((x, y), line, font=face, fill=colour)
        y += leading
    return y


def rule(draw, y, weight=2, x0=None, x1=None):
    """Draw a horizontal rule; return the y just below it."""
    left = MARGIN if x0 is None else x0
    right = WIDTH - MARGIN if x1 is None else x1
    draw.line([(left, y), (right, y)], fill=INK, width=weight)
    return y + weight


def double_rule(draw, y):
    """The thick-plus-thin rule under the nameplate."""
    rule(draw, y, 3)
    rule(draw, y + 6, 1)
    return y + 10


def kicker(draw, x, y, text):
    """Draw a red section label; return the y below it."""
    draw.text((x, y), text, font=FONTS["kicker"], fill=RED)
    return y + 26


def story(draw, x, y, width, label, headline, body,
          head_face, head_leading, body_face=None, body_leading=20):
    """Draw one story block (label, headline, body); return the y below."""
    y = kicker(draw, x, y, label)
    for line in wrap(draw, headline, head_face, width):
        draw.text((x, y), line, font=head_face, fill=INK)
        y += head_leading
    y += 2
    face = body_face if body_face is not None else FONTS["body"]
    return paragraph(draw, x, y, width, body, face, body_leading)


def centred(draw, y, text, face, colour):
    """Draw *text* centred on the page at height *y*."""
    width = draw.textlength(text, font=face)
    draw.text(((WIDTH - width) / 2, y), text, font=face, fill=colour)


# --- the stories ---------------------------------------------------------
# Every fact below was checked against several independent sources on
# the morning of 22 November 2026; see NOTES.md for the sources.

LEAD = {
    "label": "GULF OF FINLAND  —  THE BALTIC SEA",
    "headline": "DRONES SET RUSSIAN SHIP ABLAZE",
    "dek": ("Finland says Ukraine was likely behind the strike on the "
            "sanctioned Sparta II — as the war's shadow spreads "
            "across the Baltic."),
    "left": ("GULF OF FINLAND — Two drones struck the sanctioned "
             "Russian cargo ship Sparta II on Saturday morning, west of "
             "Gogland island. The ship caught fire and drifted into "
             "Finnish waters."),
    "right": ("All 16 crew were evacuated to lifeboats and then to a "
              "nearby Russian ship. Finland tightened air and sea rules "
              "in the eastern gulf, and a Russian helicopter was also "
              "reported inside Finnish airspace."),
    "strip": ("2 DRONES HIT SPARTA II  ·  16 CREW SAFE  ·  "
              "BOUND FOR KALININGRAD  ·  US-SANCTIONED SHIP"),
}

ROW_TWO = [
    {
        "label": "KRYVYI RIH",
        "headline": "DOUBLE-TAP KILLS TWO",
        "body": ("A Russian attack on President Zelenskyy's hometown killed a "
                 "7-year-old boy and a 20-year-old paramedic and wounded 60, "
                 "hitting rescuers as they worked. About 25 apartment blocks, a "
                 "hospital and schools were damaged."),
    },
    {
        "label": "SINALOA",
        "headline": "MEXICO SEIZES ‘EL CHAPO ISIDRO’",
        "body": ("Mexican forces captured FBI most-wanted cartel boss Fausto "
                 "Isidro Meza Flores in Guasave, with US intelligence help. "
                 "Eleven people died in the fighting — four soldiers and "
                 "seven gunmen — as cartel roadblocks burned."),
    },
]

ROW_THREE = [
    {
        "label": "PERU",
        "headline": "6.9 QUAKE SHAKES PERU",
        "body": ("A magnitude 6.9 earthquake struck central Peru at 00:09 UTC on "
                 "Saturday, 34 km north of Junin. It was felt in Lima; no damage "
                 "or casualties were reported."),
    },
    {
        "label": "ANTALYA",
        "headline": "COP31 PAST DEADLINE",
        "body": ("Climate talks ran into overtime with no deal, as the draft "
                 "dropped all mention of fossil fuels. The EU warned it would "
                 "be “a good deal or no deal at all”."),
    },
    {
        "label": "WASHINGTON",
        "headline": "FBI DATABASE HACKED",
        "body": ("Hackers broke into the FBI's National Crime Information "
                 "Center, used by police across the US. Trump called it "
                 "“not good”; it is the second FBI breach in months."),
    },
]

ROW_FOUR = [
    {
        "label": "TOKYO",
        "headline": "ASIAN MARKETS PLUNGE",
        "body": ("Japan's Nikkei fell 5.06% and South Korea's Kospi 5.21% on "
                 "Friday as the AI sell-off spread from Wall Street. Taiwan's "
                 "Taiex lost 6.2% in a day and 17.5% in the week."),
    },
    {
        "label": "BASRA",
        "headline": "PLANT FIRE KILLS FOUR",
        "body": ("At least four people were killed and 35 injured when a gas "
                 "pipeline blast set the Hartha power station ablaze on "
                 "Saturday. The fire spread to nearby homes."),
    },
]

TAPE = [
    "HORMUZ · Two more tankers hit by unknown projectiles near "
    "Khasab on Saturday, 50 minutes apart · No casualties reported",
    "SHENZHEN · Trump posts “The Great Powers 1945, 2026”, "
    "pairing Yalta with his summit with Xi and Putin",
    "KYIV · Zelenskyy rebukes Trump for calling Putin a ‘friend’ "
    "— “To us, he is the killer”",
]

FOOTER = ("REPORTED 21–22 NOVEMBER 2026  ·  SOURCES: REUTERS, AP, "
          "CNN, USGS, UKMTO, IRAQ SECURITY MEDIA CELL")


# --- layout --------------------------------------------------------------


def build_page():
    page = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(page)

    # Nameplate -----------------------------------------------------------
    y = 20
    centred(draw, y, "THE WORLD", FONTS["nameplate"], INK)
    y += 86
    centred(draw, y, "SUNDAY  22  NOVEMBER  2026", FONTS["dateline"], RED)
    y += 34
    centred(draw, y, "THE DAY’S WORLD NEWS IN ONE PAGE",
            FONTS["strap"], GREY)
    y += 18
    y = double_rule(draw, y)
    y += 4

    # Lead story ----------------------------------------------------------
    y = kicker(draw, MARGIN, y, LEAD["label"])
    for line in wrap(draw, LEAD["headline"], FONTS["lead_head"], TEXT_WIDTH):
        draw.text((MARGIN, y), line, font=FONTS["lead_head"], fill=INK)
        y += 54
    y += 2
    y = paragraph(draw, MARGIN, y, TEXT_WIDTH, LEAD["dek"],
                  FONTS["lead_dek"], 27)
    y += 6
    column = (TEXT_WIDTH - 24) // 2
    left_end = paragraph(draw, MARGIN, y, column, LEAD["left"],
                         FONTS["lead_body"], 20)
    right_end = paragraph(draw, MARGIN + column + 24, y, column,
                          LEAD["right"], FONTS["lead_body"], 20)
    y = max(left_end, right_end) + 5
    centred(draw, y, LEAD["strip"], FONTS["ticker"], RED)
    y += 20
    y = rule(draw, y, 2)
    y += 6

    # Two stories ---------------------------------------------------------
    column = (TEXT_WIDTH - 28) // 2
    first = story(draw, MARGIN, y, column,
                  ROW_TWO[0]["label"], ROW_TWO[0]["headline"],
                  ROW_TWO[0]["body"], FONTS["head"], 33)
    second = story(draw, MARGIN + column + 28, y, column,
                   ROW_TWO[1]["label"], ROW_TWO[1]["headline"],
                   ROW_TWO[1]["body"], FONTS["head"], 33)
    y = max(first, second) + 3
    y = rule(draw, y, 1)
    y += 6

    # Three stories -------------------------------------------------------
    third = (TEXT_WIDTH - 2 * 24) // 3
    ends = []
    for i, item in enumerate(ROW_THREE):
        x = MARGIN + i * (third + 24)
        ends.append(story(draw, x, y, third,
                          item["label"], item["headline"], item["body"],
                          FONTS["head_small"], 27,
                          FONTS["body_small"], 18))
    y = max(ends) + 3
    y = rule(draw, y, 1)
    y += 6

    # Two stories ---------------------------------------------------------
    column = (TEXT_WIDTH - 28) // 2
    first = story(draw, MARGIN, y, column,
                  ROW_FOUR[0]["label"], ROW_FOUR[0]["headline"],
                  ROW_FOUR[0]["body"], FONTS["head"], 33,
                  FONTS["body"], 19)
    second = story(draw, MARGIN + column + 28, y, column,
                   ROW_FOUR[1]["label"], ROW_FOUR[1]["headline"],
                   ROW_FOUR[1]["body"], FONTS["head"], 33,
                   FONTS["body"], 19)
    y = max(first, second) + 4

    # News tape -----------------------------------------------------------
    band_top = y
    band_height = 84
    draw.rectangle([(MARGIN, band_top),
                    (WIDTH - MARGIN, band_top + band_height)],
                   fill=TAPE_BG)
    text_y = band_top + 8
    for item in TAPE:
        for line in wrap(draw, item, FONTS["tape"], TEXT_WIDTH - 20):
            draw.text((MARGIN + 10, text_y), line,
                      font=FONTS["tape"], fill=TAPE_FG)
            text_y += 20
    y = band_top + band_height + 6

    # Footer --------------------------------------------------------------
    centred(draw, y, FOOTER, FONTS["footer"], GREY)
    y += 14

    if y > HEIGHT - 8:
        raise SystemExit("layout overflow: content ends at y=%d" % y)
    return page


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default=None)
    args = parser.parse_args(argv)
    if args.out:
        out_path = args.out
    else:
        out_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "entry.png")
    page = build_page()
    page.save(out_path, format="PNG", optimize=True)
    print("wrote %s (%dx%d)" % (out_path, WIDTH, HEIGHT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
