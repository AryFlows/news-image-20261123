#!/usr/bin/env python3
"""Frost Front Page — Monday 23 November 2026.

Draws a 1024x1024 newspaper front page with PIL only. Every story on the
page happened, or was first reported, on Monday 23 November 2026 in some
time zone (verified against wire reports before drawing). Stories that
failed the date check are listed in the red DATE CHECK box, not in the
news columns. No photos, no copied artwork: every illustration is an
original schematic drawn with PIL shapes.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (248, 244, 235)
INK = (25, 25, 25)
MUTED = (107, 98, 87)
RED = (180, 35, 24)
NAVY = (29, 53, 87)
LINE = (25, 25, 25)
HAIR = (190, 182, 168)
SKY = (216, 226, 232)
LAND = (203, 214, 205)
COURT = (96, 160, 110)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=None, max_lines=None):
    """Draw wrapped text; returns the y just below the last line."""
    if leading is None:
        leading = fnt.size + 5
    lines = wrap(draw, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def chip(draw, x, y, num, size=24):
    draw.ellipse([x, y, x + size, y + size], fill=RED)
    f = font(SANS_B, 13)
    tw = draw.textlength(str(num), font=f)
    th = f.size
    draw.text((x + (size - tw) / 2, y + (size - th) / 2 - 1),
              str(num), font=f, fill=(255, 255, 255))


def hero_art_nepal(draw, x, y, w, h):
    """Two flagpoles, a dome skyline and a rising sun — Delhi talks."""
    draw.rectangle([x, y + h - 6, x + w, y + h], fill=NAVY)
    # dome (Rashtrapati Bhavan silhouette)
    cx = x + w // 2
    draw.polygon([(cx - 52, y + h - 6), (cx - 52, y + 26),
                  (cx - 30, y + 26), (cx - 30, y + 12),
                  (cx + 30, y + 12), (cx + 30, y + 26),
                  (cx + 52, y + h - 6)], fill=(255, 255, 255),
                 outline=NAVY)
    draw.pieslice([cx - 26, y - 2, cx + 26, y + 34], 180, 360, fill=RED)
    draw.line([cx, y - 8, cx, y - 2], fill=INK, width=2)
    # sun
    draw.ellipse([x + w - 34, y + 2, x + w - 12, y + 24], fill=(232, 164, 32))
    # Nepal flag (crimson pennons) on the left pole
    draw.line([x + 8, y + 8, x + 8, y + h - 6], fill=INK, width=2)
    draw.polygon([(x + 8, y + 8), (x + 34, y + 16), (x + 8, y + 24)],
                 fill=(220, 20, 60))
    draw.polygon([(x + 8, y + 24), (x + 30, y + 31), (x + 8, y + 38)],
                 fill=(220, 20, 60))
    # India flag (saffron / white / green) on the right pole
    draw.line([x + w - 8, y + 8, x + w - 8, y + h - 6], fill=INK, width=2)
    for i, col in enumerate([(255, 153, 51), (255, 255, 255), (19, 136, 8)]):
        draw.rectangle([x + w - 38, y + 8 + i * 9, x + w - 8, y + 17 + i * 9],
                       fill=col, outline=INK)


def hero_art_capitol(draw, x, y, w, h):
    """Capitol dome schematic with a 258 seat tally."""
    draw.rectangle([x, y + h - 6, x + w, y + h], fill=NAVY)
    cx = x + w // 2
    draw.rectangle([cx - 62, y + 30, cx + 62, y + h - 6], fill=(255, 255, 255),
                   outline=NAVY)
    draw.pieslice([cx - 34, y - 4, cx + 34, y + 40], 180, 360, fill=(255, 255, 255),
                  outline=NAVY)
    draw.rectangle([cx - 3, y - 10, cx + 3, y - 2], fill=NAVY)
    for i in range(-2, 3):
        lx = cx + i * 22
        draw.line([lx, y + 34, lx, y + h - 10], fill=NAVY, width=3)


def hero_art_tennis(draw, x, y, w, h):
    """Tennis court from above, ball arcing over the net."""
    draw.rectangle([x, y, x + w, y + h], fill=COURT)
    draw.rectangle([x + 14, y + 6, x + w - 14, y + h - 6], outline=(255, 255, 255),
                   width=2)
    draw.line([x + 14, y + h // 2, x + w - 14, y + h // 2], fill=(255, 255, 255),
              width=3)
    draw.line([x + w // 2, y + 6, x + w // 2, y + h - 6], fill=(255, 255, 255),
              width=1)
    # ball arc
    pts = []
    for t in range(0, 21):
        px = x + 20 + (w - 40) * t / 20
        py = y + h - 14 - (h - 22) * (1 - ((t - 10) / 10.0) ** 2)
        pts.append((px, py))
    draw.line(pts, fill=(255, 255, 255), width=2)
    draw.ellipse([x + w - 34, y + 6, x + w - 16, y + 24], fill=(204, 255, 0),
                 outline=INK)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    f_mast = font(SERIF_B, 54)
    f_date = font(SANS_B, 17)
    f_sub = font(SANS, 13)
    f_kick = font(SANS_B, 12)
    f_head = font(SERIF_B, 21)
    f_hero_body = font(SANS, 12)
    f_body = font(SANS, 13)
    f_med_head = font(SERIF_B, 18)
    f_med_body = font(SANS, 13)
    f_sec = font(SANS_B, 13)
    f_pin = font(SANS_B, 11)

    # ---- masthead ----
    title = "FROST FRONT PAGE"
    tw = d.textlength(title, font=f_mast)
    d.text(((W - tw) / 2, 14), title, font=f_mast, fill=INK)
    sub = "MONDAY 23 NOVEMBER 2026  ·  11 VERIFIED STORIES  ·  5 REGIONS"
    tw = d.textlength(sub, font=f_date)
    d.text(((W - tw) / 2, 74), sub, font=f_date, fill=RED)
    regions = "ASIA 2   ·   NORTH AMERICA 4   ·   EUROPE 3   ·   MIDDLE EAST 1   ·   OCEANIA 1"
    tw = d.textlength(regions, font=f_sub)
    d.text(((W - tw) / 2, 98), regions, font=f_sub, fill=MUTED)
    d.line([24, 116, 1000, 116], fill=LINE, width=3)
    d.line([24, 121, 1000, 121], fill=LINE, width=1)

    # ---- heroes ----
    heroes = [
        ("1", "DIPLOMACY · DELHI", "NEPAL'S NEW PM MEETS MODI IN DELHI",
         "Balendra Shah holds his first bilateral talks abroad since taking "
         "office in March — energy, trade and connectivity on the agenda.",
         hero_art_nepal),
        ("2", "USA · HOUSE OF REPRESENTATIVES", "DEMOCRATS CLINCH 258 SEATS",
         "AP calls North Carolina for Chuck Hubbard, giving Democrats "
         "their biggest House majority since 1992. Four races still "
         "uncalled.",
         hero_art_capitol),
        ("3", "SPORT · TURIN", "ALCARAZ WINS FIRST ATP FINALS",
         "Carlos Alcaraz beats world No. 1 Alexander Zverev 6-2, 7-6(7) "
         "in Turin, saving three set points. Zverev still ends the year "
         "No. 1.",
         hero_art_tennis),
    ]
    hx = [24, 354, 684]
    hw = 314
    hy, hh = 132, 196
    for (num, kick, head, body, art), x in zip(heroes, hx):
        d.rectangle([x, hy, x + hw, hy + hh], outline=LINE, width=1)
        d.rectangle([x, hy, x + hw, hy + 3], fill=RED)
        chip(d, x + 10, hy + 12, num)
        d.text((x + 42, hy + 16), kick, font=f_kick, fill=RED)
        y = hy + 42
        y = para(d, x + 10, y, head, f_head, hw - 20, leading=25, max_lines=2)
        y = para(d, x + 10, y + 4, body, f_hero_body, hw - 20, leading=16,
                 max_lines=3)
        art(d, x + 10, hy + hh - 50, hw - 20, 42)

    # ---- medium cards ----
    d.text((24, 336), "MORE FROM MONDAY", font=f_sec, fill=NAVY)
    d.line([180, 343, 1000, 343], fill=HAIR, width=1)
    mediums = [
        ("4", "TANKER SCARE IN THE GULF",
         "UKMTO reports a tanker incident with military forces in the Gulf "
         "of Oman. Iran says two supertankers hit mines east of Hormuz."),
        ("5", "RUSSIA 'TWICE TRIED TO KILL RAPPER'",
         "Poland reveals Moscow targeted rapper Kyivstoner in Warsaw in "
         "August, after a second plot was foiled in Denmark."),
        ("6", "US PRESSES NVIDIA OVER CHINA CHIPS",
         "Treasury chief Bessent demands answers on chip sales to China "
         "and who ran compliance."),
        ("7", "DELTA GLITCH GROUNDS ATLANTA",
         "An automation failure for weight-and-balance maths forces a "
         "ground stop at the world's busiest airport."),
        ("8", "BABIS REJECTS TRIMMED EU BUDGET",
         "Czech PM calls Costa's €1.78tn plan unacceptable and opposes "
         "€100bn for Ukraine, days before leaders meet in Brussels."),
    ]
    mx = [24, 520]
    mw = 480
    my = [356, 436, 516]
    mh = 72
    for i, (num, head, body) in enumerate(mediums):
        col, row = i % 2, i // 2
        x, y = mx[col], my[row]
        d.rectangle([x, y, x + mw, y + mh], outline=LINE, width=1)
        chip(d, x + 8, y + 8, num, size=22)
        d.text((x + 38, y + 9), head, font=f_med_head, fill=INK)
        para(d, x + 38, y + 34, body, f_med_body, mw - 48, leading=16,
             max_lines=2)
    # by-the-numbers cell (bottom right of the grid)
    x, y = mx[1], my[2]
    d.rectangle([x, y, x + mw, y + mh], fill=NAVY)
    d.text((x + 12, y + 8), "BY THE NUMBERS", font=f_sec, fill=(255, 255, 255))
    stats = "258 House seats  ·  6-2, 7-6(7) in Turin  ·  NZ sales +2.2%"
    d.text((x + 12, y + 30), stats, font=font(SANS, 12), fill=(255, 255, 255))
    d.text((x + 12, y + 50), "4 races uncalled  ·  2 tankers hit mines  ·  Prescott 5 TDs",
           font=font(SANS, 12), fill=(200, 210, 225))

    # ---- world map panel ----
    px, py, pw, ph = 24, 600, 500, 232
    d.rectangle([px, py, px + pw, py + ph], outline=LINE, width=1)
    d.text((px + 10, py + 8), "THE WORLD TODAY — 11 STORIES PINNED",
           font=f_sec, fill=NAVY)
    d.rectangle([px + 10, py + 30, px + pw - 10, py + ph - 10], fill=SKY)
    # schematic continents (abstract polygons, not traced)
    continents = [
        [(60, 655), (150, 648), (185, 668), (168, 700), (140, 722),
         (118, 748), (95, 736), (70, 702), (55, 676)],
        [(150, 738), (186, 732), (200, 762), (186, 802), (160, 796),
         (146, 762)],
        [(255, 652), (300, 646), (316, 666), (296, 686), (270, 682),
         (250, 666)],
        [(255, 696), (310, 691), (330, 716), (316, 762), (286, 792),
         (260, 756), (248, 722)],
        [(320, 652), (430, 641), (480, 662), (490, 692), (450, 712),
         (420, 702), (400, 722), (370, 706), (340, 691), (325, 671)],
        [(430, 772), (480, 766), (490, 786), (460, 796), (435, 789)],
    ]
    for poly in continents:
        d.polygon(poly, fill=LAND, outline=NAVY)
    pins = {
        1: (395, 688), 2: (140, 688), 3: (280, 672), 4: (360, 700),
        5: (298, 655), 6: (72, 682), 7: (128, 700), 8: (258, 658),
        9: (492, 798), 10: (96, 714), 11: (455, 668),
    }
    for num, (cx, cy) in pins.items():
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=RED,
                  outline=(255, 255, 255))
        tw = d.textlength(str(num), font=f_pin)
        d.text((cx - tw / 2, cy - 6), str(num), font=f_pin,
               fill=(255, 255, 255))

    # ---- briefs column ----
    bx, by, bw = 540, 600, 460
    d.rectangle([bx, by, bx + bw, by + 232], outline=LINE, width=1)
    d.text((bx + 12, by + 8), "BRIEFS", font=f_sec, fill=NAVY)
    d.line([bx + 12, by + 30, bx + bw - 12, by + 30], fill=HAIR, width=1)
    briefs = [
        ("9", "NZ RETAIL SALES JUMP 2.2%.",
         "Third-quarter sales beat forecasts after a 0.5% fall in Q2 — "
         "the first release of the new week, out overnight in Wellington."),
        ("10", "NFL SUNDAY: COWBOYS 51-30.",
         "Dak Prescott accounts for five touchdowns against Tennessee. "
         "Chiefs rout the Cardinals 34-7; Bills beat Miami 26-9."),
        ("11", "JAPAN SHUT FOR HOLIDAY.",
         "Tokyo is closed for Labour Thanksgiving Day, thinning Asian "
         "trade. Flash PMIs due in Europe and the US today."),
    ]
    yy = by + 36
    for i, (num, head, body) in enumerate(briefs):
        chip(d, bx + 12, yy, num, size=22)
        d.text((bx + 42, yy + 2), head, font=f_med_head, fill=INK)
        yy = para(d, bx + 42, yy + 26, body, f_med_body, bw - 54,
                  leading=15, max_lines=2)
        yy += 6
        if i < 2:
            d.line([bx + 12, yy, bx + bw - 12, yy], fill=HAIR, width=1)
            yy += 6

    # ---- date check box ----
    dx, dy, dw, dh = 24, 844, 976, 112
    d.rectangle([dx, dy, dx + dw, dy + dh], outline=RED, width=2)
    d.text((dx + 10, dy + 7),
           "DATE CHECK — STORIES WE LEFT OUT (WRONG DATE)",
           font=font(SANS_B, 13), fill=RED)
    excluded = (
        "UN killer-robot talks ended Sat 21 Nov · Serang factory fire broke out "
        "Sat 21 Nov, toll updates Sun 22 Nov · COP31 collapse Sun 22 Nov · "
        "'El Chapo Isidro' captured Fri 20 Nov · Sparta II fire Sat 21 Nov · "
        "Dymer drone strike Sun 22 Nov · Corvette Merkury sunk Sun 22 Nov · "
        "India 720/9d Test record Sun 22 Nov · Verstappen Las Vegas GP Sun "
        "22 Nov · Liverpool v Man Utd Sun 22 Nov · Lisbon march Sat 21 Nov · "
        "Myanmar ASEAN rebuke Sat 21 Nov · WHO Ebola warning Sun 22 Nov · "
        "Miley Cyrus wedding Sat 21 Nov · Tom Jackson died Fri 20 Nov · "
        "Eisenkot condemnation Sun 22 Nov · S. Sudan attack Sat 21 Nov · "
        "Modi IIT Patna AI centre Sat 21 Nov · Anupama snooker title Sat "
        "21 Nov · Amit Shah Arunachal push Sun 22 Nov · Wadkute dies Sun "
        "22 Nov · Dar US-Iran interview Sat 21 Nov · EU budget plan Sat "
        "21 Nov · US intel chief on Putin Sun 22 Nov.")
    para(d, dx + 10, dy + 28, excluded, font(SANS, 11), dw - 20, leading=14)

    # ---- footer ----
    d.line([24, 968, 1000, 968], fill=LINE, width=1)
    foot_l = "Early edition — stories verified to 00:14 UTC, Mon 23 Nov 2026."
    foot_r = "Drawn with PIL · No photos · 11 stories"
    d.text((24, 976), foot_l, font=font(SANS, 12), fill=MUTED)
    tw = d.textlength(foot_r, font=font(SANS, 12))
    d.text((1000 - tw, 976), foot_r, font=font(SANS, 12), fill=MUTED)
    d.text((24, 994),
           "Every story on this page happened, or was first reported, on 23 November 2026 in some time zone.",
           font=font(SANS, 11), fill=MUTED)

    img.save(OUT, "PNG")
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
