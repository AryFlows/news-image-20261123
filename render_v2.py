#!/usr/bin/env python3
"""Render the Frost Front Page for Monday 23 November 2026.

A one-page newspaper front page: 21 stories verified for 23 November
2026 (3 heroes, 6 cards, 12 briefs), a numbered world map, and a DATE
CHECK box listing the big stories left out because they happened on
another day. Deterministic output: same bytes every run.
"""
import hashlib
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (20, 33, 61)
RED = (185, 28, 28)
BLUE = (29, 78, 216)
GOLD = (176, 124, 16)
GREY = (90, 90, 90)
LIGHT = (214, 206, 188)
MAPSEA = (233, 236, 240)
MAPLAND = (196, 205, 214)

FD = "/usr/share/fonts/truetype/dejavu"
F_BIG = ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", 54)
F_MED = ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", 26)
F_HEAD = ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", 19)
F_SUB = ImageFont.truetype(f"{FD}/DejaVuSans.ttf", 15)
F_CARD = ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", 17)
F_CSUB = ImageFont.truetype(f"{FD}/DejaVuSans.ttf", 13)
F_BRIEF = ImageFont.truetype(f"{FD}/DejaVuSans.ttf", 13)
F_BLEAD = ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", 13)
F_KICK = ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", 13)
F_DATE = ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", 16)
F_SMALL = ImageFont.truetype(f"{FD}/DejaVuSans.ttf", 11)
F_PIN = ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", 10)
F_FOOT = ImageFont.truetype(f"{FD}/DejaVuSans.ttf", 12)

# (num, kicker, headline, sub, lon, lat, accent)
HEROES = [
    (1, "MARKETS", "ASIA ACTS TO HALT THE AI ROUT",
     "Taiwan bans short sales; China cuts margin rules; Seoul readies "
     "funds as the sell-off spreads.",
     139.7, 35.7, RED),
    (2, "UKRAINE", "DYMER TOLL RISES TO 11",
     "Rescuers dig on as the Kyiv region mourns Sunday's strike on a "
     "block of flats; a boy of 7 is pulled out alive.",
     30.5, 50.5, BLUE),
    (3, "LIBYA", "UKRAINE CLAIMS WARSHIP SUNK OFF LIBYA",
     "Zelenskyy: seven sea drones sank the corvette Merkury at Benghazi; "
     "a Ka-27 helicopter was destroyed with it.",
     20.0, 32.1, GOLD),
]

CARDS = [
    (4, "BELGIUM", "AIRPORTS SHUT BY STRIKE",
     "ATC walks out 7am-9pm; 60,000 passengers hit, 429 flights axed.",
     4.4, 50.8),
    (5, "YEMEN", "SAUDI STRIKE KILLS 6 IN HODEIDA",
     "Monday attack on the port.",
     42.9, 14.8),
    (6, "TURKEY", "MARCH FOR PRESS FREEDOM",
     "Thousands in Istanbul protest the Sozcu TV raid; third takeover "
     "in a year.", 28.9, 41.0),
    (7, "BRAZIL", "BOLSONARO STABLE IN ICU",
     "Day 3 with a bowel blockage; surgery not ruled out.",
     -47.9, -15.8),
    (8, "SUDAN", "UN CONDEMNS SUDAN STRIKES",
     "Khartoum drones killed children.",
     32.5, 15.6),
    (9, "INDONESIA", "24 DEAD IN FACTORY FIRE CONFIRMED",
     "30 still missing; search goes on.",
     106.3, -6.4),
]

BRIEFS = [
    (10, "SEOUL", "Education minister quits over AI exam-cheating scandal.", 127.0, 37.5),
    (11, "SEOUL", "Exports top $1 trillion for the first time.", 130.0, 36.5),
    (12, "JAPAN", "China warns citizens off Mount Fuji; $75,000 reward in climber hunt.", 138.7, 35.4),
    (13, "BRAZIL", "Supercell storm devastates the town of Tupancireta.", -53.8, -29.0),
    (14, "GAZA", "War left a 'toxic wasteland', a new report says.", 34.5, 31.5),
    (15, "TECH", "Meta AI chief: superintelligence is 'arriving'.", -122.1, 37.5),
    (16, "CRICKET", "New Zealand frustrate India as first Test ends in a draw.", 77.0, 28.0),
    (17, "WASHINGTON", "Spy chief defends Trump calling Putin 'friend'.", -77.0, 38.9),
    (18, "CONGO", "Fighting near Ebola zone disrupts the response.", 23.0, -2.5),
    (19, "INDIA", "Tata Steel buys a $1.67bn stake in top pipe maker.", 72.8, 19.0),
    (20, "IOWA", "Army to detonate unstable explosives despite court order.", -93.6, 42.0),
    (21, "ENERGY", "US energy exports hit records as oil market watches surplus.", -95.4, 29.8),
]

EXCLUDED = [
    "COP31 collapse - ended Sun 22 Nov",
    "Alcaraz wins ATP Finals - Sun 22 Nov",
    "Liverpool 4-0 Man Utd - Sun 22 Nov",
    "Marquez 8th MotoGP title - Sun 22 Nov",
    "'El Chapo Isidro' captured - Fri 20 Nov",
    "Riemann proof claimed - Fri 20 Nov",
    "Shenzhen peace declaration - Thu 19 Nov",
    "Denmark rapper plot - announced Fri 20 Nov",
    "EU-Rwanda deportation hub - Mon 16 Nov",
    "South Sudan: 24 killed - Sat-Sun 22 Nov",
]

# Simplified continent outlines as (lon, lat) points.
N_AMERICA = [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80),
    (-85, 80), (-80, 73), (-76, 62), (-70, 58), (-65, 60), (-60, 52),
    (-55, 47), (-60, 45), (-70, 42), (-75, 35), (-80, 32), (-81, 26),
    (-84, 30), (-90, 29), (-97, 26), (-105, 22), (-110, 24), (-115, 29),
    (-120, 34), (-125, 40), (-124, 48), (-130, 55), (-145, 60),
    (-155, 58), (-165, 60)]
GREENLAND = [(-58, 64), (-45, 60), (-40, 65), (-30, 68), (-22, 70),
    (-25, 76), (-35, 80), (-50, 78), (-58, 74), (-60, 70)]
S_AMERICA = [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12),
    (-72, -18), (-70, -23), (-70, -30), (-72, -37), (-73, -44),
    (-70, -50), (-68, -55), (-65, -55), (-62, -48), (-58, -38),
    (-52, -32), (-48, -28), (-41, -23), (-35, -9), (-35, -6),
    (-40, -3), (-44, -2), (-50, 0), (-55, 5), (-60, 8), (-68, 11),
    (-72, 12), (-77, 8)]
AFRICA = [(-6, 35), (-10, 31), (-15, 27), (-17, 21), (-17, 15), (-13, 8),
    (-8, 5), (-4, 5), (6, 4), (9, 4), (13, 0), (12, -6), (13, -12),
    (14, -17), (12, -18), (16, -23), (18, -29), (20, -35), (26, -34),
    (32, -29), (35, -24), (36, -18), (40, -15), (40, -10), (42, -4),
    (46, -1), (51, 2), (51, 11), (48, 11), (43, 12), (39, 15), (37, 18),
    (35, 22), (32, 31), (30, 31), (25, 32), (20, 33), (11, 34), (10, 37),
    (0, 36)]
EURASIA = [(-10, 36), (-9, 43), (-2, 48), (-4, 50), (0, 51), (3, 53),
    (7, 54), (8, 57), (10, 59), (5, 60), (5, 62), (10, 64), (13, 66),
    (18, 69), (25, 71), (30, 70), (35, 67), (40, 66), (45, 68), (50, 69),
    (55, 69), (60, 70), (68, 73), (75, 73), (85, 75), (95, 76), (105, 77),
    (110, 74), (120, 73), (130, 72), (140, 72), (150, 70), (158, 69),
    (162, 66), (170, 66), (178, 65), (178, 64), (170, 60), (162, 59),
    (158, 52), (150, 59), (142, 55), (140, 50), (138, 46), (135, 44),
    (132, 43), (130, 42), (128, 38), (126, 36), (122, 38), (120, 34),
    (122, 30), (120, 27), (115, 23), (110, 21), (108, 18), (105, 10),
    (103, 8), (100, 8), (98, 12), (97, 16), (94, 17), (91, 22), (89, 22),
    (86, 20), (82, 17), (80, 15), (80, 13), (77, 8), (76, 10), (73, 16),
    (70, 20), (67, 25), (62, 25), (58, 25), (56, 27), (54, 26), (52, 25),
    (50, 29), (48, 30), (48, 29), (50, 26), (55, 24), (58, 22), (55, 17),
    (52, 15), (48, 14), (45, 13), (43, 12), (42, 15), (40, 20), (39, 24),
    (38, 28), (36, 29), (35, 31), (36, 36), (33, 35), (30, 36), (27, 37),
    (23, 36), (20, 38), (22, 40), (19, 42), (15, 44), (12, 44), (10, 44),
    (8, 44), (3, 43), (0, 40), (-2, 37), (-6, 36)]
AUSTRALIA = [(114, -22), (114, -30), (115, -35), (120, -34), (124, -33),
    (129, -32), (132, -32), (135, -35), (138, -35), (140, -38), (145, -38),
    (150, -37), (153, -32), (153, -27), (150, -23), (146, -19), (142, -15),
    (142, -11), (137, -12), (135, -15), (132, -12), (130, -13), (126, -14),
    (122, -17), (118, -20)]
CONTINENTS = [N_AMERICA, GREENLAND, S_AMERICA, AFRICA, EURASIA, AUSTRALIA]

MAP = (684, 344, 316, 276)  # x, y, w, h of the map panel


def project(lon, lat):
    mx, my, mw, mh = MAP
    x = mx + (lon + 180.0) / 360.0 * mw
    y = my + (85.0 - lat) / 145.0 * mh
    return x, y


def wrap(text, font, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if font.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text(d, xy, s, font, fill=INK, anchor="la"):
    d.text(xy, s, font=font, fill=fill, anchor=anchor)


def num_badge(d, x, y, n, r=13, fill=RED):
    d.ellipse([x - r, y - r, x + r, y + r], fill=fill)
    s = str(n)
    w = F_PIN.getlength(s)
    d.text((x - w / 2, y - 7), s, font=F_PIN, fill=(255, 255, 255))


def draw_header(d):
    text(d, (24, 18), "FROST FRONT PAGE", F_BIG, INK)
    text(d, (1000, 26), "MONDAY 23 NOVEMBER 2026", F_DATE, RED, anchor="ra")
    text(d, (1000, 52), "THE WORLD IN ONE PAGE", F_KICK, INK, anchor="ra")
    d.line([(24, 92), (1000, 92)], fill=RED, width=4)
    text(d, (24, 98), "21 stories verified for 23 November 2026  |  No story from another day",
         F_SMALL, GREY)


def draw_hero(d, x, y, w, h, num, kicker, headline, sub, accent):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=LIGHT, width=2)
    d.rectangle([x, y, x + w, y + 8], fill=accent)
    num_badge(d, x + 24, y + 34, num, r=15)
    text(d, (x + 46, y + 24), kicker, F_KICK, accent)
    lines = wrap(headline, F_MED, w - 28)
    ly = y + 56
    for ln in lines[:2]:
        text(d, (x + 14, ly), ln, F_MED, INK)
        ly += 30
    slines = wrap(sub, F_SUB, w - 28)
    for ln in slines[:3]:
        text(d, (x + 14, ly), ln, F_SUB, INK)
        ly += 19


def draw_card(d, x, y, w, h, num, kicker, headline, sub):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=LIGHT, width=1)
    num_badge(d, x + 18, y + 22, num, r=12)
    text(d, (x + 36, y + 13), kicker, F_KICK, RED)
    lines = wrap(headline, F_CARD, w - 24)
    ly = y + 38
    for ln in lines[:2]:
        text(d, (x + 12, ly), ln, F_CARD, INK)
        ly += 21
    slines = wrap(sub, F_CSUB, w - 24)
    for ln in slines[:2]:
        text(d, (x + 12, ly), ln, F_CSUB, GREY)
        ly += 16


def draw_map(d):
    mx, my, mw, mh = MAP
    d.rectangle([mx - 12, my - 36, mx + mw + 12, my + mh + 12],
                fill=(255, 255, 255), outline=LIGHT, width=1)
    text(d, (mx - 12, my - 30), "WHERE IT HAPPENED", F_KICK, INK)
    text(d, (mx + mw + 12, my - 30), "21 STORIES", F_KICK, RED, anchor="ra")
    d.rectangle([mx, my, mx + mw, my + mh], fill=MAPSEA)
    for lon in range(-150, 181, 30):
        x = mx + (lon + 180.0) / 360.0 * mw
        d.line([(x, my), (x, my + mh)], fill=(225, 228, 232), width=1)
    for lat in range(-60, 91, 30):
        y = my + (85.0 - lat) / 145.0 * mh
        d.line([(mx, y), (mx + mw, y)], fill=(225, 228, 232), width=1)
    for poly in CONTINENTS:
        pts = [project(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=MAPLAND, outline=(150, 160, 172))
    all_stories = HEROES + CARDS + BRIEFS
    for story in all_stories:
        num = story[0]
        lon, lat = (story[4], story[5]) if len(story) >= 6 else (story[3], story[4])
        x, y = project(lon, lat)
        r = 8
        d.ellipse([x - r, y - r, x + r, y + r], fill=RED, outline=(255, 255, 255), width=1)
        s = str(num)
        w = F_PIN.getlength(s)
        d.text((x - w / 2, y - 6), s, font=F_PIN, fill=(255, 255, 255))


def draw_briefs(d):
    y0 = 648
    text(d, (24, y0), "IN BRIEF", F_KICK, INK)
    d.line([(24, y0 + 20), (1000, y0 + 20)], fill=INK, width=2)
    col_w, row_h = 318, 52
    for i, (num, kicker, body, _lon, _lat) in enumerate(BRIEFS):
        col, row = i % 3, i // 3
        x = 24 + col * (col_w + 11)
        y = y0 + 28 + row * row_h
        num_badge(d, x + 11, y + 9, num, r=10)
        text(d, (x + 26, y), kicker, F_KICK, RED)
        lines = wrap(body, F_BRIEF, col_w - 26)
        ly = y + 17
        for ln in lines[:2]:
            text(d, (x + 26, ly), ln, F_BRIEF, INK)
            ly += 16


def draw_datecheck(d):
    y0 = 900
    d.rectangle([24, y0, 1000, 996], fill=(238, 232, 216), outline=LIGHT, width=1)
    text(d, (36, y0 + 8), "DATE CHECK", F_KICK, RED)
    text(d, (150, y0 + 8), "Left out on purpose - big stories, wrong day:",
         F_SMALL, INK)
    for i, item in enumerate(EXCLUDED):
        col, row = i % 2, i // 2
        x = 36 + col * 480
        y = y0 + 28 + row * 13
        text(d, (x, y), "x  " + item, F_SMALL, GREY)
    text(d, (512, 1002), "Frost Front Page - Sources: Reuters, AP, AFP, Al Jazeera, CNN",
         F_FOOT, GREY, anchor="ma")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_header(d)
    hx, hw, hh = 24, 318, 188
    for i, (num, kick, head, sub, _lon, _lat, accent) in enumerate(HEROES):
        draw_hero(d, hx + i * (hw + 11), 122, hw, hh, num, kick, head, sub, accent)
    cx, cw, ch = 24, 318, 100
    for i, (num, kick, head, sub, _lon, _lat) in enumerate(CARDS):
        col, row = i % 2, i // 2
        draw_card(d, cx + col * (cw + 12), 322 + row * (ch + 10), cw, ch,
                  num, kick, head, sub)
    draw_map(d)
    draw_briefs(d)
    draw_datecheck(d)
    img.save("entry.png", format="PNG")
    data = open("entry.png", "rb").read()
    print("entry.png", len(data), "bytes",
          "sha256", hashlib.sha256(data).hexdigest()[:16])


if __name__ == "__main__":
    main()
