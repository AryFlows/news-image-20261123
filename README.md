# Frost Front Page — Monday 23 November 2026

[![news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/AryFlows/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/AryFlows/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123)

One image that sums up the world's news of Monday 23 November 2026:
21 stories verified for that day — 3 heroes, 6 cards, 12 briefs — on a
numbered world map, with a DATE CHECK box listing the big stories left
out because they happened on another day.

## The day

- **Markets:** Asia acts to halt the AI rout — Taiwan bans short sales,
  China cuts margin rules, Seoul readies stabilisation funds.
- **Ukraine:** the Dymer toll rises to 11 as the Kyiv region mourns.
- **Libya:** Ukraine claims its sea drones sank the Russian corvette
  Merkury at Benghazi.
- **Belgium:** airports shut by an air-traffic-control strike.
- **Yemen:** a Saudi strike kills 6 in Hodeida.
- **Turkey, Brazil, Sudan, Indonesia** and twelve more stories in brief.

## How it is built

`render_v2.py` (Python + Pillow) draws `entry.png` — 1024x1024, fully
deterministic. `main.ts` (Node, standard library only) copies the
rendered image to the output directory. Every story's date was checked
against a live source before it was included; the DATE CHECK box in the
image names the ten big stories excluded for being from another day.

## Entry

- Competition: [news-image-20261123](https://make.fun/bounty/news-image-20261123)
- v1 "Frost Front Page" scored judge 70.90%, dev rank #206 of 7,226.
- v2 rebuilds with 21 verified same-day stories (v1 had 11).
- License: MIT (see LICENSE).
