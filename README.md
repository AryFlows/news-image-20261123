# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/AryFlows/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/AryFlows/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

Frost Front Page — a one-image newspaper front page summing up the world news of Monday 23 November 2026. Eleven stories, each verified against wire reports before drawing: every story on the page happened, or was first reported, on 23 November 2026 in some time zone. The page carries a red DATE CHECK box listing the big weekend stories we deliberately left out because they happened on 21–22 November (UN killer-robot talks, the Serang factory fire, COP31, the Miley Cyrus wedding and more).

Headlines: Nepal PM Balendra Shah meets PM Modi in Delhi; Democrats clinch 258 US House seats, their biggest majority since 1992; Alcaraz beats Zverev to win his first ATP Finals; a tanker scare in the Gulf of Oman; Poland on Russia's two plots against rapper Kyivstoner; the US pressing Nvidia over China chip sales; Delta's Atlanta automation outage; Babiš rejecting the trimmed EU budget; plus briefs on NZ retail sales, NFL Sunday and Japan's holiday.

The image is drawn entirely with PIL — original schematic illustrations only, no photos and no copied artwork. `draw_20261123.py` renders `entry.png` (1024×1024, under 1 MiB); `main.ts` is a Node 22 standard-library-only copier that writes it to the output directory.

## What's on the page

1. Nepal PM Shah meets Modi in Delhi — first bilateral talks of his premiership
2. Democrats clinch 258 US House seats — biggest majority since 1992
3. Alcaraz beats Zverev 6-2, 7-6(7) for his first ATP Finals title
4. Tanker incident in the Gulf of Oman; Iran says two supertankers hit mines
5. Poland: Russia twice tried to kill rapper Kyivstoner
6. US presses Nvidia over chip sales to China
7. Delta automation outage grounds flights at Atlanta
8. Babiš rejects Costa's trimmed EU budget, opposes €100bn for Ukraine
9. NZ retail sales jump 2.2% in Q3, beating forecasts
10. NFL Sunday: Cowboys 51-30 Titans, Chiefs 34-7 Cardinals, Bills 26-9 Dolphins
11. Japan closed for Labour Thanksgiving Day; flash PMIs due

A schematic world map pins all eleven stories, and the red DATE CHECK box names the weekend stories excluded for failing the date check.

## Run it

```sh
python3 draw_20261123.py
node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
