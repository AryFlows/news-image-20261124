#!/usr/bin/env python3
"""Render the Frost Front Page for 24 November 2026.

Draws a 1024x1024 front page with PIL only. Every story on the page was
verified as happening (or first reported) on 24 November 2026 in some
timezone; the red DATE CHECK box lists the big wrong-date stories that were
deliberately left out. Output is deterministic: same input, same bytes.
"""
import hashlib
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (248, 244, 232)
INK = (25, 25, 25)
RED = (179, 38, 30)
NAVY = (31, 58, 95)
STEEL = (74, 107, 138)
GOLD = (176, 124, 12)
RULE = (201, 194, 176)
DOT = (154, 168, 181)
CARD_BG = (255, 255, 255)
MUTED = (90, 90, 84)

FDIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FDIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
MONO_B = lambda s: font("DejaVuSansMono-Bold.ttf", s)
MONO = lambda s: font("DejaVuSansMono.ttf", s)

WIRES = "00:20 UTC"

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def wrap(text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text(x, y, s, fnt, fill=INK, anchor="la"):
    d.text((x, y), s, font=fnt, fill=fill, anchor=anchor)


def hline(y, x0=28, x1=996, fill=INK, width=1):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def vline(x, y0, y1, fill=RULE, width=1):
    d.line([(x, y0), (x, y1)], fill=fill, width=width)


# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 6], fill=RED)
text(W // 2, 14, "FROST FRONT PAGE", SERIF_B(54), anchor="ma")
text(28, 72, "TUESDAY 24 NOVEMBER 2026", SANS_B(15))
text(W // 2, 72, "EARLY EDITION  •  WIRES READ TO " + WIRES, SANS_B(15), anchor="ma")
text(996, 72, "$100  •  TOP 50 PAID", SANS_B(15), anchor="ra")
hline(92, fill=INK, width=2)
hline(95, fill=INK, width=1)

# ------------------------------------------------------------- numbers strip
NUMBERS = [
    ("8,570.6", "ASX 200  −0.26%"),
    ("−3.7%", "S&P 500, FRI"),
    ("20%", "LABOR PRIMARY, VIC"),
    ("$25", "PBS CAP TO 2030"),
    ("28 NOV", "VICTORIA VOTES"),
    ("21", "STORIES VERIFIED"),
]
nx, nw = 28, 968 // 6
for i, (val, lab) in enumerate(NUMBERS):
    cx = nx + i * nw
    text(cx + 8, 100, val, SANS_B(20), fill=NAVY)
    text(cx + 8, 122, lab, MONO(10), fill=MUTED)
    if i:
        vline(cx, 100, 134)
hline(138, fill=RULE, width=1)

# ------------------------------------------------------------------- heroes
HEROES = [
    {
        "n": "1", "pin": "MELBOURNE",
        "kicker": "VICTORIA POLL",
        "head": "Labor faces worst Vic result since 1902",
        "body": ("YouGov megapoll: Coalition 31, One Nation 21, Labor 20, "
                 "Greens 16; two-party 58–42. RedBridge model: Labor ~30 "
                 "seats. Polls open Saturday 28 Nov."),
        "chart": "split",
    },
    {
        "n": "2", "pin": "SYDNEY",
        "kicker": "MARKETS",
        "head": "ASX slumps again as AI rout rolls on",
        "body": ("Shares fall at Tuesday open; eighth straight losing "
                 "session to Monday (−0.26%, 8,570.6). Wall Street in "
                 "correction after Friday's 3.7% S&P slide."),
        "chart": "line",
    },
    {
        "n": "3", "pin": "CANBERRA",
        "kicker": "COST OF LIVING",
        "head": "Scripts frozen at $25 until 2030",
        "body": ("Medicine costs held in a cost-of-living win: the PBS "
                 "co-payment cap is extended four more years, so every "
                 "Australian pays no more at the chemist."),
        "chart": "pills",
    },
]
HX = [28, 354, 680]
HW = 316
HY, HH = 144, 168
for (hx, hero) in zip(HX, HEROES):
    d.rectangle([hx, HY, hx + HW, HY + HH], outline=INK, width=2, fill=CARD_BG)
    d.rectangle([hx, HY, hx + HW, HY + 24], fill=NAVY)
    text(hx + 10, HY + 5, hero["n"] + "  •  " + hero["kicker"], SANS_B(12), fill=(255, 255, 255))
    text(hx + HW - 10, HY + 5, hero["pin"], MONO(10), fill=(255, 255, 255), anchor="ra")
    y = HY + 30
    for ln in wrap(hero["head"], SANS_B(20), HW - 20):
        text(hx + 10, y, ln, SANS_B(20))
        y += 23
    y += 2
    for ln in wrap(hero["body"], SANS(12), HW - 20):
        text(hx + 10, y, ln, SANS(12), fill=(45, 45, 45))
        y += 15
    # illustration strip at the bottom of the hero box
    iy0, iy1 = HY + HH - 34, HY + HH - 6
    ix0, ix1 = hx + 10, hx + HW - 10
    d.rectangle([ix0, iy0, ix1, iy1], outline=RULE, width=1, fill=(244, 241, 232))
    if hero["chart"] == "split":
        # Two-party preferred: Coalition 58, Labor 42 — one split bar.
        bar_w = ix1 - ix0
        split = int(bar_w * 58 / 100)
        d.rectangle([ix0, iy0 + 6, ix0 + split, iy1 - 8], fill=NAVY)
        d.rectangle([ix0 + split, iy0 + 6, ix1, iy1 - 8], fill=STEEL)
        text(ix0 + 6, iy0 + 8, "COAL 58", MONO_B(10), fill=(255, 255, 255))
        text(ix1 - 6, iy0 + 8, "LAB 42", MONO_B(10), fill=(255, 255, 255), anchor="ra")
    elif hero["chart"] == "line":
        pts = [(ix0 + 10 + i * 52, iy0 + 6 + i * 4) for i in range(5)]
        pts[-1] = (ix0 + 10 + 4 * 52, iy1 - 8)
        d.line(pts, fill=RED, width=3)
        for px, py in pts:
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED)
        text(ix1 - 6, iy0 + 2, "−0.26% MON", MONO_B(10), fill=RED, anchor="ra")
    else:
        # pill bottle with a cross
        d.rounded_rectangle([ix0 + 8, iy0 + 4, ix0 + 34, iy1 - 4], radius=3, outline=NAVY, width=2, fill=(255, 255, 255))
        d.rectangle([ix0 + 13, iy0 + 1, ix0 + 29, iy0 + 5], fill=NAVY)
        d.rectangle([ix0 + 19, iy0 + 8, ix0 + 23, iy1 - 8], fill=RED)
        d.rectangle([ix0 + 13, iy0 + 12, ix0 + 29, iy0 + 16], fill=RED)
        for j, lab in enumerate(["$25 CAP", "TO 2030", "PBS"]):
            text(ix0 + 44 + j * 78, iy0 + 8, lab, MONO_B(11), fill=NAVY)

# ---------------------------------------------------------------------- map
MAP_Y0, MAP_Y1 = 322, 452
text(28, MAP_Y0, "WHERE TODAY HAPPENED", SANS_B(12), fill=NAVY)
text(996, MAP_Y0, "PINS 1–11  •  SCHEMATIC, NOT TO SCALE", MONO(10), fill=MUTED, anchor="ra")
MY0, MY1 = MAP_Y0 + 18, MAP_Y1
MX0, MX1 = 28, 996


def project(lon, lat):
    x = MX0 + (lon + 180.0) / 360.0 * (MX1 - MX0)
    y = MY0 + (75.0 - lat) / (75.0 + 55.0) * (MY1 - MY0)
    return x, y


LAND = [
    (-168, -52, 15, 72), (-80, -35, -55, 10), (-10, 40, 36, 70),
    (-18, 52, -35, 35), (40, 180, 5, 75), (95, 141, -10, 25),
    (68, 90, 8, 35), (113, 154, -40, -10), (-5, 2, 50, 59),
    (129, 146, 31, 45), (166, 178, -47, -34), (95, 141, -11, 6),
    (-55, -20, 60, 84),
]
gx = MX0
while gx < MX1:
    gy = MY0
    while gy < MY1:
        lon = (gx - MX0) / (MX1 - MX0) * 360.0 - 180.0
        lat = 75.0 - (gy - MY0) / (MY1 - MY0) * 130.0
        if any(a <= lon <= b and c <= lat <= dd for a, b, c, dd in LAND):
            d.ellipse([gx - 1, gy - 1, gx + 1, gy + 1], fill=DOT)
        gy += 6
    gx += 6
for lab, lon, lat in [("N. AMERICA", -100, 45), ("S. AMERICA", -60, -15),
                      ("EUROPE", 15, 55), ("AFRICA", 20, 5),
                      ("ASIA", 90, 50), ("AUSTRALIA", 118, -28)]:
    lx, ly = project(lon, lat)
    text(lx, ly, lab, MONO(9), fill=MUTED, anchor="ma")

# One dot per city; several stories share a city, so the label lists them all.
PINS = [
    (144.96, -37.81, "1", -18, -14), (151.21, -33.87, "2·6", 10, -14),
    (149.13, -35.28, "3·4·5", -6, 10), (146.80, -19.26, "7", 10, -6),
    (77.21, 28.61, "8", -12, -14), (-9.14, 38.72, "9", -12, -14),
    (153.43, -28.02, "10", 10, -4), (143.00, -32.00, "11", -18, 4),
]
for lon, lat, nums, dx, dy in PINS:
    px, py = project(lon, lat)
    d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=(255, 255, 255), width=1)
    text(px + dx, py + dy, nums, SANS_B(11), fill=RED)
hline(MAP_Y1 + 4, fill=RULE, width=1)

# --------------------------------------------------------------------- cards
CARDS = [
    ("4", "CANBERRA", "BOWEN UNDER FIRE",
     "Coalition: climate minister 'should go' after COP31 collapse",
     "Opposition blames Chris Bowen for the Antalya failure; the "
     "government defends its delegation as talks end with no deal."),
    ("5", "CANBERRA", "US ALLIANCE",
     "'Cannot abandon the US', Wong tells Labor critics",
     "Foreign minister Penny Wong defends the alliance amid Trump "
     "turmoil, saying the security partnership still serves Australia."),
    ("6", "SYDNEY", "POKIES FIGHT",
     "Councils put Minns on notice over pokies reform",
     "NSW councils demand action on poker machines, urging the state "
     "to put communities ahead of gambling industry profits."),
    ("7", "QUEENSLAND", "REEF PLEA",
     "Reef divers take ocean plea to Parliament",
     "Fresh from COP31, Great Barrier Reef and Ningaloo divers meet MPs "
     "24–25 Nov as another hot summer approaches."),
    ("8", "INDIA", "GURU NANAK JAYANTI",
     "Guru Nanak Jayanti observed across India",
     "Sikh festival marks Guru Nanak's birth; schools shut in several "
     "states for the public holiday."),
    ("9", "LISBON • 10:30 TODAY", "BUDGET VOTE",
     "Unions rally at parliament as budget vote looms",
     "CGTP returns to the Assembly for the 2027 budget's final vote, "
     "days after Saturday's rain-soaked cost-of-living march."),
    ("10", "GOLD COAST • TONIGHT", "T20 CRICKET",
     "Australia v England, 2nd T20 tonight",
     "Second T20 of the series under lights on the Gold Coast; the "
     "hosts look to press home their advantage."),
    ("11", "AUSTRALIA • TODAY", "SEVERE WEATHER",
     "Wild storms, floods likely in four states",
     "Storm front crosses the east; millions told to prepare for "
     "flash flooding as wild weather hits four states."),
]
CX = [28, 272, 516, 760]
CW = 234
CY, CH = 464, 128
for i, (num, place, kick, head, body) in enumerate(CARDS):
    cx = CX[i % 4]
    cy = CY + (i // 4) * (CH + 8)
    d.rectangle([cx, cy, cx + CW, cy + CH], outline=INK, width=1, fill=CARD_BG)
    d.rectangle([cx, cy, cx + CW, cy + 20], fill=STEEL)
    text(cx + 8, cy + 4, num + "  •  " + kick, SANS_B(10), fill=(255, 255, 255))
    text(cx + CW - 8, cy + 4, place, MONO(8), fill=(255, 255, 255), anchor="ra")
    y = cy + 26
    for ln in wrap(head, SANS_B(13), CW - 16):
        text(cx + 8, y, ln, SANS_B(13))
        y += 15
    y += 2
    for ln in wrap(body, SANS(11), CW - 16):
        text(cx + 8, y, ln, SANS(11), fill=(45, 45, 45))
        y += 13

# ---------------------------------------------------------------- ALSO list
AY = 736
text(28, AY, "ALSO TODAY — IN ONE LINE", SANS_B(13), fill=NAVY)
hline(AY + 18, fill=RULE, width=1)
ALSO = [
    "QLD: Two killed in head-on crash after a welfare check.",
    "Snow falls on alpine slopes weeks before summer.",
    "Fiery ram-raid destroys agency; police call it suspicious.",
    "Middle Corridor reshapes Eurasian geopolitics — analysis out today.",
    "Pakistan's water crisis: scarcity, or something else? — analysis out today.",
    "Asbestos warning for DIY renovators; awareness week runs 23–29 Nov.",
    "Teen fighting for life after schoolies incident in Qld.",
    "Travel industry plea to halt $230m travel-tax hike.",
    "Portugal's parliament holds final vote on 2027 budget today.",
    "Straw poll in premier's seat: Liberal 41%, Labor 26% (early voting).",
]
for i, item in enumerate(ALSO):
    col = i % 2
    row = i // 2
    ax = 28 + col * 484
    ay = AY + 24 + row * 17
    text(ax, ay, "•  " + item, SANS(11), fill=(45, 45, 45))
hline(AY + 24 + 5 * 17 + 4, fill=RULE, width=1)

# ---------------------------------------------------------------- region bar
RY = 850
text(28, RY, "WHERE THE NEWS CAME FROM", SANS_B(11), fill=NAVY)
REGIONS = [("AUSTRALIA & OCEANIA  16", 16, NAVY), ("ASIA  3", 3, STEEL),
           ("EUROPE  2", 2, GOLD), ("AMERICAS  0", 0, RULE),
           ("AFRICA  0", 0, RULE), ("MIDDLE EAST  0", 0, RULE)]
bx, bw_total = 28, 968
total = 21
x = bx
for lab, v, col in REGIONS:
    wseg = max(int(v / total * bw_total), 0)
    if wseg > 0:
        d.rectangle([x, RY + 16, x + wseg, RY + 30], fill=col)
    x += wseg
text(28, RY + 34, "Australia & Oceania 16   •   Asia 3   •   Europe 2   •   Americas 0   •   Africa 0   •   Middle East 0",
     MONO(10), fill=MUTED)

# ------------------------------------------------------------------ timeline
TY = 884
hline(TY, fill=RULE, width=1)
text(28, TY + 6, "TODAY, IN LOCAL TIME", SANS_B(11), fill=NAVY)
text(28, TY + 22,
     "10:00 AEDT  ASX opens lower  •  10:30 WET  Lisbon rally at parliament  •  19:00 AEDT  T20, Gold Coast  •  SAT 28 NOV  Victoria votes",
     MONO(10), fill=(45, 45, 45))

# ---------------------------------------------------------------- DATE CHECK
DY = 920
d.rectangle([28, DY, 996, 996], outline=RED, width=2, fill=(253, 238, 236))
text(28 + 10, DY + 6, "DATE CHECK — THESE BIG STORIES ARE NOT 24 NOVEMBER. WE LEFT THEM OUT.", SANS_B(12), fill=RED)
EXCLUDED = [
    "COP31 ends with no deal — 22 Nov",
    "India–Nepal 8 MoUs, Saryu-Kamala train — 23 Nov",
    "Nvidia reinstates Huang as CEO — 23 Nov",
    "UK to host 2035 Women's World Cup — 23 Nov",
    "Molly Meldrum dies, 83 — 23 Nov",
    "Ukraine claims sinking corvette off Libya — 22–23 Nov",
    "Sparta II cargo ship hit by drones — 21 Nov",
    "Lisbon cost-of-living march — 21 Nov",
    "NZ–India Test ends in a draw — 23 Nov",
    "Oxfam: Gaza a 'toxic wasteland' — 23 Nov",
]
for i, item in enumerate(EXCLUDED):
    col = i % 2
    row = i // 2
    ax = 28 + 10 + col * 484
    ay = DY + 26 + row * 9
    text(ax, ay, "✕  " + item, SANS(10), fill=(90, 30, 26))

# --------------------------------------------------------------------- footer
text(28, 1004,
     "Early edition: 21 stories verified to " + WIRES + ", 24 Nov 2026. Sources: AAP, Reuters, News Corp, Hockey India, Medianet. Drawn with PIL; no photograph.",
     SANS(10), fill=MUTED)
text(996, 1004, "FROST FRONT PAGE", MONO_B(10), fill=MUTED, anchor="ra")

img.save(OUT)
data = open(OUT, "rb").read()
print("saved", OUT, len(data), "bytes",
      hashlib.sha256(data).hexdigest())
print("size", img.size)
