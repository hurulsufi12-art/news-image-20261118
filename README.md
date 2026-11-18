# The World in One Day — 18 November 2026

[![make.fun](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)
[![make.fun](https://make.fun/badge/news-image-20261118/hurulsufi12-art/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118)
[![make.fun](https://make.fun/badge/news-image-20261118/hurulsufi12-art/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118)

A newspaper front page that sums up the world news of **Wednesday, 18 November 2026** in one image (1024×1024 PNG).

- **Lead:** US strikes Qeshm Island — US fighter jets hit IRGC missile launch sites; Iran answers with drones at Bahrain and Kuwait, its third strike on Bahrain in a week.
- Kerch Bridge arch falls into the strait after Ukrainian drone and missile strikes, the second day in a row.
- APEC opens in Shenzhen — Xi Jinping receives Vladimir Putin; the first Trump–Xi–Putin trilateral is set for Thursday.
- Democrats win Alaska — Mary Peltola wins the Senate seat; Democrats now hold 56 seats.
- Ebola cases more than double in DR Congo — 11,000+ cases, 5,400 deaths, the UN says.
- Russian jet crashes in Siberia — a military plane crashes in the Kemerovo region; 19 dead.
- Also: US loses measles-free status after 26 years; Moldova closes its airspace after a Russian drone enters; four nations urge Israel to open aid access to flood-hit Gaza; Nvidia Q3 $115.8 billion, beats forecasts.

Everything in the image is drawn with code (see `draw.py`); no photographs and no AI-generated imagery, so no text is ever garbled.

## Files

- `entry.png` — the image (1024×1024, under 1 MiB)
- `main.py` — Python 3.13, standard library only; copies `entry.png` to `$MAKEFUN_OUTPUT_DIR` (or `/output`)
- `draw.py` — the Pillow script that drew `entry.png` deterministically (build-time provenance only; not run by the grader)
- `LICENSE` — MIT

## Run it

```bash
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Two runs write byte-identical files.
