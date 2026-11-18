#!/usr/bin/env python3
"""Draw entry.png for news-image-20261118: a newspaper front page summing up
Wednesday 18 November 2026. Deterministic: fixed fonts, fixed geometry, no
randomness, no timestamps, no network. Run: python3 draw.py -> entry.png
(1024x1024, well under 1 MiB). Everything is drawn with code (Pillow
primitives); no photos, no AI-generated images."""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 36                      # side margin
CW = W - 2 * M              # content width = 952

PAPER = (251, 249, 242)     # warm newsprint white
INK = (20, 36, 62)          # navy
RED = (176, 30, 36)         # masthead red
GREY = (90, 100, 112)
LIGHT_GREY = (214, 214, 206)
SKY = (191, 217, 232)
SEA = (127, 168, 201)
SEA_DARK = (94, 138, 175)
STEEL = (70, 84, 100)
ORANGE = (224, 122, 31)
GOLD = (212, 160, 38)
SAND = (206, 184, 138)
LAND = (168, 178, 120)

FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, s, f, max_w):
    """Greedy word wrap to lines no wider than max_w."""
    words = s.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(draw, trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_one_line(draw, s, f_path, size, max_w):
    """Shrink font until the string fits on one line; return (font, size)."""
    while size > 12:
        f = font(f_path, size)
        if text_w(draw, s, f) <= max_w:
            return f, size
        size -= 1
    return font(f_path, 12), 12


def para(draw, x, y, s, f, color, max_w, leading):
    """Draw wrapped paragraph, return y after last line."""
    for line in wrap(draw, s, f, max_w):
        draw.text((x, y), line, font=f, fill=color)
        y += leading
    return y


# ---------------------------------------------------------------- icons
def icon_plane(d, x, y, s, color):
    """Simple airliner side view inside a s x s box at (x, y)."""
    d.ellipse([x + s * 0.08, y + s * 0.42, x + s * 0.92, y + s * 0.58], fill=color)
    d.polygon([(x + s * 0.88, y + s * 0.42), (x + s * 1.0, y + s * 0.50),
               (x + s * 0.88, y + s * 0.58)], fill=color)
    d.polygon([(x + s * 0.10, y + s * 0.44), (x + s * 0.22, y + s * 0.14),
               (x + s * 0.32, y + s * 0.44)], fill=color)
    d.polygon([(x + s * 0.42, y + s * 0.50), (x + s * 0.62, y + s * 0.86),
               (x + s * 0.74, y + s * 0.86), (x + s * 0.58, y + s * 0.50)], fill=color)
    d.polygon([(x + s * 0.12, y + s * 0.50), (x + s * 0.22, y + s * 0.74),
               (x + s * 0.30, y + s * 0.74), (x + s * 0.24, y + s * 0.50)], fill=color)
    for i in range(4):
        wx = x + s * (0.38 + 0.10 * i)
        d.ellipse([wx, y + s * 0.46, wx + s * 0.045, y + s * 0.505], fill=PAPER)


def icon_aid(d, x, y, s, color):
    """Aid box with a cross."""
    d.rectangle([x + s * 0.10, y + s * 0.28, x + s * 0.90, y + s * 0.92],
                outline=color, width=max(3, s // 16))
    d.line([x + s * 0.10, y + s * 0.28, x + s * 0.90, y + s * 0.28],
           fill=color, width=max(3, s // 16))
    d.rectangle([x + s * 0.42, y + s * 0.16, x + s * 0.58, y + s * 0.30],
                fill=color)
    cx, cy = x + s * 0.50, y + s * 0.60
    d.rectangle([cx - s * 0.07, cy - s * 0.16, cx + s * 0.07, cy + s * 0.16], fill=RED)
    d.rectangle([cx - s * 0.16, cy - s * 0.07, cx + s * 0.16, cy - s * 0.07], fill=RED)


def icon_bridge(d, x, y, s, color):
    """Arched bridge with a broken middle span."""
    # towers
    for tx in (x + s * 0.14, x + s * 0.72):
        d.rectangle([tx, y + s * 0.22, tx + s * 0.08, y + s * 0.72], fill=color)
    # deck: left and right segments, gap in the middle
    d.rectangle([x + s * 0.04, y + s * 0.30, x + s * 0.40, y + s * 0.38], fill=color)
    d.rectangle([x + s * 0.60, y + s * 0.30, x + s * 0.96, y + s * 0.38], fill=color)
    # fallen span, tilted into the water
    d.polygon([(x + s * 0.40, y + s * 0.32), (x + s * 0.60, y + s * 0.32),
               (x + s * 0.56, y + s * 0.58), (x + s * 0.44, y + s * 0.58)],
              fill=(120, 40, 44))
    # arch under the deck
    d.arc([x + s * 0.18, y + s * 0.38, x + s * 0.82, y + s * 0.82],
          start=0, end=180, fill=color, width=max(3, s // 18))
    # water
    for i in range(3):
        wx = x + s * (0.08 + 0.30 * i)
        d.arc([wx, y + s * 0.84, wx + s * 0.24, y + s * 0.96],
              start=180, end=360, fill=SEA_DARK, width=max(3, s // 18))


def icon_ballot(d, x, y, s, color):
    """Ballot box with a check mark."""
    # box
    d.rectangle([x + s * 0.14, y + s * 0.34, x + s * 0.86, y + s * 0.92],
                outline=color, width=max(3, s // 16))
    d.rectangle([x + s * 0.08, y + s * 0.24, x + s * 0.92, y + s * 0.34],
                fill=color)
    # slot
    d.rectangle([x + s * 0.36, y + s * 0.27, x + s * 0.64, y + s * 0.31],
                fill=PAPER)
    # check mark
    d.line([x + s * 0.28, y + s * 0.62, x + s * 0.44, y + s * 0.78,
            x + s * 0.74, y + s * 0.44], fill=RED,
           width=max(4, s // 12), joint="curve")


def icon_jet(d, x, y, s, color):
    """Fighter jet, top view, climbing."""
    d.polygon([(x + s * 0.50, y + s * 0.04), (x + s * 0.60, y + s * 0.62),
               (x + s * 0.50, y + s * 0.78), (x + s * 0.40, y + s * 0.62)], fill=color)
    d.polygon([(x + s * 0.42, y + s * 0.48), (x + s * 0.06, y + s * 0.86),
               (x + s * 0.24, y + s * 0.86), (x + s * 0.46, y + s * 0.62)], fill=color)
    d.polygon([(x + s * 0.58, y + s * 0.48), (x + s * 0.94, y + s * 0.86),
               (x + s * 0.76, y + s * 0.86), (x + s * 0.54, y + s * 0.62)], fill=color)
    d.polygon([(x + s * 0.42, y + s * 0.66), (x + s * 0.30, y + s * 0.94),
               (x + s * 0.44, y + s * 0.94)], fill=color)
    d.polygon([(x + s * 0.58, y + s * 0.66), (x + s * 0.70, y + s * 0.94),
               (x + s * 0.56, y + s * 0.94)], fill=color)
    d.ellipse([x + s * 0.46, y + s * 0.18, x + s * 0.54, y + s * 0.34], fill=PAPER)


def draw_qeshm(d, x, y, w, h):
    """Qeshm Island illustration: jets in the sky, explosions on the
    island, the sea below."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    # sun
    d.ellipse([x + w - 52, y + 14, x + w - 18, y + 48], fill=(240, 214, 130))
    # sea
    sea_y = y + int(h * 0.62)
    d.rectangle([x, sea_y, x + w, y + h], fill=SEA)
    for i in range(4):
        wx = x + 18 + i * 78
        d.arc([wx, sea_y + 16, wx + 56, sea_y + 36], start=180, end=360,
              fill=SEA_DARK, width=3)
    # island: low elongated landmass across the sea
    isl_y = sea_y - 18
    d.polygon([(x + 8, sea_y + 6), (x + 60, isl_y - 6), (x + 190, isl_y - 22),
               (x + 300, isl_y - 8), (x + w - 8, sea_y + 6)],
              fill=LAND)
    d.polygon([(x + 8, sea_y + 6), (x + 60, isl_y - 6), (x + 190, isl_y - 22),
               (x + 300, isl_y - 8), (x + w - 8, sea_y + 6)],
              outline=SAND, width=3)
    # two jets in the sky (small, side view), kept clear of the smoke
    for jx, jy, js in ((x + 44, y + 18, 44), (x + 150, y + 20, 36)):
        d.ellipse([jx, jy + js * 0.42, jx + js * 0.84, jy + js * 0.58], fill=INK)
        d.polygon([(jx + js * 0.80, jy + js * 0.42), (jx + js, jy + js * 0.50),
                   (jx + js * 0.80, jy + js * 0.58)], fill=INK)
        d.polygon([(jx + js * 0.06, jy + js * 0.44), (jx + js * 0.18, jy + js * 0.14),
                   (jx + js * 0.28, jy + js * 0.44)], fill=INK)
        d.polygon([(jx + js * 0.38, jy + js * 0.50), (jx + js * 0.56, jy + js * 0.86),
                   (jx + js * 0.68, jy + js * 0.86), (jx + js * 0.52, jy + js * 0.50)],
                  fill=INK)
    # explosions on the island: orange starbursts
    for ex, ey, r in ((x + 110, isl_y - 8, 26), (x + 250, isl_y - 14, 30)):
        pts = []
        for k in range(16):
            import math
            ang = math.pi * k / 8
            rr = r if k % 2 == 0 else r * 0.45
            pts.append((ex + rr * math.cos(ang), ey + rr * math.sin(ang)))
        d.polygon(pts, fill=ORANGE)
        d.polygon([(ex - r * 0.45, ey), (ex, ey - r * 0.45),
                   (ex + r * 0.45, ey), (ex, ey + r * 0.45)], fill=GOLD)
    # smoke puffs over the blasts
    for sx, sy, r in ((x + 110, isl_y - 48, 15), (x + 136, isl_y - 64, 19),
                      (x + 250, isl_y - 56, 17), (x + 276, isl_y - 74, 14)):
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(150, 150, 148))
    d.text((x + 10, y + h - 26), "QESHM ISLAND, IRAN",
           font=font(FONT_B, 15), fill=INK)


# ---------------------------------------------------------------- layout
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    y = 30
    # --- masthead ---
    f_mast = font(FONT_B, 62)
    mast = "THE WORLD IN ONE DAY"
    d.text(((W - text_w(d, mast, f_mast)) / 2, y), mast, font=f_mast, fill=INK)
    y += 78
    d.rectangle([M, y, W - M, y + 4], fill=RED)
    y += 14
    f_date = font(FONT_B, 36)
    date = "WEDNESDAY, 18 NOVEMBER 2026"
    d.text(((W - text_w(d, date, f_date)) / 2, y), date, font=f_date, fill=RED)
    y += 52
    d.rectangle([M, y, W - M, y + 2], fill=INK)
    y += 12

    # --- lead story: US strikes Qeshm Island ---
    f_kick = font(FONT_B, 18)
    d.text((M, y), "LEAD  •  MIDDLE EAST", font=f_kick, fill=RED)
    y += 26
    ill_w, ill_h = 360, 264
    ill_x, ill_y = W - M - ill_w, y
    draw_qeshm(d, ill_x, ill_y, ill_w, ill_h)
    tx = M
    tw = ill_x - 18 - M
    f_head = font(FONT_B, 42)
    head_lines = wrap(d, "US STRIKES QESHM ISLAND", f_head, tw)
    for line in head_lines:
        d.text((tx, y), line, font=f_head, fill=INK)
        y += 50
    y += 6
    f_body = font(FONT_R, 22)
    lead_sum = ("US fighter jets hit IRGC missile launch sites on Qeshm "
                "Island. Iran answers with drones at Bahrain and Kuwait, "
                "its third strike on Bahrain in a week.")
    y = para(d, tx, y, lead_sum, f_body, INK, tw, 29)
    lead_bottom = max(y, ill_y + ill_h) + 14
    d.rectangle([M, lead_bottom, W - M, lead_bottom + 2], fill=INK)
    y = lead_bottom + 14

    # --- grid of 4 stories, 2 columns ---
    stories = [
        ("UKRAINE", "KERCH BRIDGE ARCH FALLS",
         "The road arch of the Kerch Bridge collapses into the strait "
         "after Ukrainian drone and missile strikes, the second day in "
         "a row.",
         icon_bridge),
        ("ASIA", "APEC OPENS IN SHENZHEN",
         "Xi Jinping receives Vladimir Putin as the APEC summit opens; "
         "the first Trump-Xi-Putin trilateral is set for Thursday.",
         icon_plane),
        ("AMERICAS", "DEMOCRATS WIN ALASKA",
         "Mary Peltola wins Alaska's Senate seat; Democrats now hold "
         "56 seats.",
         icon_ballot),
        ("AFRICA", "EBOLA CASES MORE THAN DOUBLE",
         "Ebola in DR Congo has more than doubled in three months: "
         "11,000+ cases, 5,400 deaths, the UN says.",
         icon_aid),
    ]
    col_w = (CW - 20) // 2
    row_h = 140
    for i, (kick, head, summ, icon) in enumerate(stories):
        col = i % 2
        row = i // 2
        cx = M + col * (col_w + 20)
        cy = y + row * (row_h + 14)
        d.text((cx + 74, cy), kick, font=font(FONT_B, 16), fill=RED)
        f_h, _ = fit_one_line(d, head, FONT_B, 24, col_w - 74)
        d.text((cx + 74, cy + 20), head, font=f_h, fill=INK)
        para(d, cx + 74, cy + 50, summ, font(FONT_R, 19), INK,
             col_w - 74, 24)
        icon(d, cx, cy + 6, 62, INK)
        if col == 0:
            d.line([cx + col_w + 10, cy + 4, cx + col_w + 10, cy + row_h - 8],
                   fill=LIGHT_GREY, width=2)
    y = y + 2 * (row_h + 14) + 2

    # --- sixth story, full width ---
    d.rectangle([M, y, W - M, y + 2], fill=LIGHT_GREY)
    y += 10
    d.text((M + 74, y), "ASIA-PACIFIC", font=font(FONT_B, 16), fill=RED)
    f_h, _ = fit_one_line(d, "RUSSIAN JET CRASHES IN SIBERIA", FONT_B, 24, CW - 74)
    d.text((M + 74, y + 20), "RUSSIAN JET CRASHES IN SIBERIA", font=f_h, fill=INK)
    para(d, M + 74, y + 50,
         "A Russian military plane crashes in the Kemerovo region; 19 dead.",
         font(FONT_R, 19), INK, CW - 74, 24)
    icon_jet(d, M, y + 6, 62, INK)
    y += 104
    d.rectangle([M, y, W - M, y + 2], fill=INK)
    y += 12

    # --- ticker ---
    f_tick_b = font(FONT_B, 20)
    f_tick = font(FONT_R, 20)
    tick = ("US loses measles-free status after 26 years  •  "
            "Moldova closes its airspace after a Russian drone enters  •  "
            "Four nations urge Israel to open aid access to flood-hit Gaza  •  "
            "Nvidia Q3 $115.8 billion, beats forecasts")
    d.text((M, y), "ALSO:", font=f_tick_b, fill=RED)
    tx = M + text_w(d, "ALSO:  ", f_tick_b)
    y = para(d, tx, y, tick, f_tick, INK, W - M - tx, 26)
    y += 8
    d.rectangle([M, y, W - M, y + 4], fill=RED)

    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
