[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/c/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/AryFlows/news-image-20261124/rank.svg)](https://make.fun/c/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/AryFlows/news-image-20261124/reward.svg)](https://make.fun/c/news-image-20261124)

# Frost Front Page — Tuesday 24 November 2026

**Frost Front Page** is a one-image front page summing up 24 November 2026's
world news: 21 verified stories in a single 1024×1024 PNG.

## The edition

An **early edition** — the wires were read to 00:20 UTC, when the day was
still young in Europe and the Americas and already afternoon in
Asia–Australia, so the page honestly leans Asia–Pacific (16 of 21 stories).

- **3 heroes:** Victoria's election megapoll (Labor faces its worst result
  since 1902), the ASX slump as the global AI rout rolls on, and PBS medicine
  costs frozen at $25 until 2030.
- **8 story cards:** Bowen under fire after COP31, Wong defends the US
  alliance, NSW councils vs pokies reform, Reef divers take their ocean plea
  to Parliament, Guru Nanak Jayanti, Lisbon's budget-vote rally, tonight's
  Australia–England T20, and wild storms across four states.
- **10-item ALSO list**, a schematic dotted world map with 11 numbered pins,
  a numbers strip, a region bar, a local-time timeline, and a red
  **DATE CHECK** box naming the big wrong-date stories we refused to pad with
  (COP31's no-deal end, the India–Nepal MoUs, Nvidia's Huang, the 2035
  Women's World Cup, Molly Meldrum, and more).

## How it is made

`draw_20261124.py` renders `entry.png` with PIL only (no network, no
third-party packages at grade time). `main.ts` is a Node-stdlib-only copier:
it copies the committed `entry.png` to `/output/entry.png` and never removes
the output directory (it is a mounted volume in the grader).

```sh
python3 draw_20261124.py   # renders entry.png (deterministic)
node main.ts               # copies entry.png to /output/entry.png
```

## Verification

Every story was checked against same-day reporting before it made the page;
anything dated 21–23 November went into the DATE CHECK box instead. The
render is deterministic — two runs produce byte-identical PNGs
(`entry.png`: 1024×1024, 175,671 bytes,
sha256 `3e53c17a970eb09c637dbe52b89e1f6249e9c3b5eceff2287d0206c9f72ae7d2`).
