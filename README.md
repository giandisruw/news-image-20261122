# THE WORLD — Sunday 22 November 2026

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/giandisruw/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/giandisruw/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

Built for the [make.fun](https://make.fun/bounty/news-image-20261122) news-image-20261122 bounty.

A one-page newspaper front page that sums up the world's news of
Sunday 22 November 2026, drawn by a Python program. Built for the
make.fun bounty `news-image-20261122` ("Sum up 22 November's world news
in one image").

## The image

The front page leads with drones setting the sanctioned Russian cargo
ship Sparta II ablaze in the Gulf of Finland — two drones struck the
ship on Saturday morning, the crew of 16 was evacuated, and Finland
says Ukraine was likely behind the attack.

The rest of the page covers the day's other big stories: the double-tap
strike on Kryvyi Rih that killed a 7-year-old boy and a paramedic,
Mexico's capture of FBI most-wanted cartel boss "El Chapo Isidro", a
magnitude 6.9 earthquake in Peru's Andes, the COP31 climate talks
running past their deadline with no deal, hackers breaking into the
FBI's crime database, Asian markets plunging as the AI sell-off spreads,
and a power-station fire in Basra that killed four people. A dark
ticker at the foot carries two more tankers hit near Hormuz, Trump's
"Great Powers 1945, 2026" post, and Zelenskyy's rebuke of Trump for
calling Putin a "friend".

Every fact on the page was checked against several independent sources
on the morning of 22 November 2026; see `NOTES.md` for the story-by-story
sources. Nothing in the image is dated before 21 November 2026.

## Stories at a glance

| Story | What happened |
|---|---|
| Drones hit Sparta II | Two drones struck the sanctioned Russian cargo ship in the Gulf of Finland; 16 crew evacuated |
| Kryvyi Rih strike | Double-tap attack killed a 7-year-old boy and a 20-year-old paramedic; 60 wounded |
| Mexico seizes cartel boss | FBI most-wanted "El Chapo Isidro" captured in Guasave; 11 dead in the fighting |
| Peru earthquake | Magnitude 6.9 quake in the Andes, felt in Lima; no damage or casualties reported |
| COP31 past deadline | Climate talks in overtime with no deal; draft drops all mention of fossil fuels |
| FBI database hacked | Hackers broke into the FBI's National Crime Information Center; second FBI breach in months |
| Asian markets plunge | Nikkei −5.06%, Kospi −5.21%, Taiex −6.2% in a day as the AI sell-off spreads |
| Basra plant fire | Gas pipeline blast at the Hartha power station killed 4 and injured 35 |

## How to run it

Requires Python 3.13 and Pillow, with the Liberation fonts installed
(the environment the bounty grader provides).

```sh
python3 main.py
```

That writes the front page to `/output/entry.png` (or to the directory
in `MAKEFUN_OUTPUT_DIR`). The image is a 1024×1024 PNG, well under the
1 MiB limit. The program uses no network, no clock and no randomness:
running it twice writes byte-identical output — the copy is verified
by size and by SHA-256 hash.

To render the image into this directory instead, run:

```sh
python3 build_image.py
```

## Tests (22 November 2026)

Ran `python3 -P -s main.py` from a different working directory, twice,
with `MAKEFUN_OUTPUT_DIR` set to two different folders. Both runs
exited 0 and wrote byte-identical output:

- `wrote /tmp/out1/entry.png (177657 bytes, sha256 382a676098b5c9316ac172f0155809d21394836487c463966b7441eb00327406)`
- `wrote /tmp/out2/entry.png (177657 bytes, sha256 382a676098b5c9316ac172f0155809d21394836487c463966b7441eb00327406)`

The bundled `entry.png` has the same hash. Image is 1024×1024 px,
177,657 bytes — under the 1 MiB limit. `main.py` imports standard
library only (no PIL, no local modules) and verifies the copy by both
size and SHA-256.

## Files

- `main.py` — the entrypoint: copies the bundled `entry.png` to `/output/entry.png` (stdlib only, no drawing at runtime)
- `build_image.py` — the drawing code and all story text
- `entry.png` — the rendered front page
- `NOTES.md` — research notes: every story with its sources
- `README.md` — this file
- `LICENSE` — MIT licence
