from PIL import Image, ImageDraw
import random, math

MAP_PATH = r'c:/Users/Ana/Desktop/prueba/my-portfolio/src/assets/fondo.png'
OUT_PATH = r'c:/Users/Ana/Desktop/prueba/my-portfolio/src/assets/tileset_stardew_32.png'
TILE = 32
COLS = 4
ROWS = 2
W = TILE * COLS
H = TILE * ROWS

# Palette anchors tuned from the map style (vibrant, Stardew-like)
GRASS_BASE = [(120, 192, 78), (106, 178, 66), (134, 205, 89)]
DIRT_BASE = [(179, 115, 62), (197, 132, 74), (156, 95, 52)]
WATER_BASE = [(78, 170, 224), (56, 149, 210), (98, 192, 237)]
TREE_FOLIAGE = [(64, 126, 53), (83, 150, 62), (49, 105, 44)]
TREE_TRUNK = (110, 74, 43)

rng = random.Random(42)

# Read map to slightly bias colors toward current project style
try:
    mp = Image.open(MAP_PATH).convert('RGB').resize((256, 128))
    px = list(mp.getdata())
    greens = [p for p in px if p[1] > p[0] and p[1] > p[2]]
    blues = [p for p in px if p[2] > p[1] and p[2] > p[0]]
    browns = [p for p in px if p[0] > p[2] and p[1] > p[2]]
    def avg(lst, fallback):
        if not lst:
            return fallback
        n = len(lst)
        return (sum(p[0] for p in lst)//n, sum(p[1] for p in lst)//n, sum(p[2] for p in lst)//n)
    gavg = avg(greens, (120, 190, 80))
    bavg = avg(blues, (80, 170, 220))
    davg = avg(browns, (180, 120, 70))
    GRASS_BASE = [
        tuple(min(255, max(0, int(0.55*c + 0.45*a))) for c, a in zip(col, gavg))
        for col in GRASS_BASE
    ]
    WATER_BASE = [
        tuple(min(255, max(0, int(0.6*c + 0.4*a))) for c, a in zip(col, bavg))
        for col in WATER_BASE
    ]
    DIRT_BASE = [
        tuple(min(255, max(0, int(0.6*c + 0.4*a))) for c, a in zip(col, davg))
        for col in DIRT_BASE
    ]
except Exception:
    pass


def clamp(v):
    return 0 if v < 0 else (255 if v > 255 else int(v))

def mix(c1, c2, t):
    return tuple(clamp(c1[i] * (1 - t) + c2[i] * t) for i in range(3))

def add(c, d):
    return tuple(clamp(c[i] + d) for i in range(3))

# Periodic value for seamless tiling: depends on sin/cos cycles over 32px.
def periodic_noise(x, y, seed=0):
    a = math.sin((x + seed * 3) * 2 * math.pi / TILE)
    b = math.cos((y + seed * 5) * 2 * math.pi / TILE)
    c = math.sin((x + y + seed * 7) * 2 * math.pi / TILE)
    d = math.cos((x - y + seed * 11) * 2 * math.pi / TILE)
    return (a + b + 0.6 * c + 0.6 * d) / 3.2


def make_grass(var_idx):
    im = Image.new('RGBA', (TILE, TILE), (0, 0, 0, 255))
    px = im.load()
    base = GRASS_BASE[var_idx % len(GRASS_BASE)]
    alt1 = add(base, 16)
    alt2 = add(base, -18)

    for y in range(TILE):
        for x in range(TILE):
            n = periodic_noise(x, y, var_idx + 1)
            n2 = periodic_noise(x, y, var_idx + 9)
            c = mix(base, alt1, (n + 1) * 0.5 * 0.35)
            c = mix(c, alt2, (n2 + 1) * 0.5 * 0.3)
            if ((x * 7 + y * 11 + var_idx * 13) % 31) == 0:
                c = add(c, 22)
            px[x, y] = (*c, 255)

    # A few tiny flowers/leaf dots, periodic-safe coordinates
    accents = [
        (3 + var_idx, 5 + 2 * var_idx, (245, 231, 125)),
        (17 + var_idx, 19 + var_idx, (238, 147, 170)),
        (26 - var_idx, 11 + var_idx, (178, 226, 135)),
    ]
    for ax, ay, col in accents:
        ax %= TILE
        ay %= TILE
        px[ax, ay] = (*col, 255)
        px[(ax + 1) % TILE, ay] = (*add(col, -20), 255)
    return im


def make_dirt(var_idx):
    im = Image.new('RGBA', (TILE, TILE), (0, 0, 0, 255))
    px = im.load()
    base = DIRT_BASE[var_idx % len(DIRT_BASE)]
    warm = add(base, 22)
    dark = add(base, -24)

    for y in range(TILE):
        for x in range(TILE):
            n = periodic_noise(x, y, 20 + var_idx)
            n2 = periodic_noise(x, y, 27 + var_idx)
            c = mix(base, warm, (n + 1) * 0.5 * 0.45)
            c = mix(c, dark, (n2 + 1) * 0.5 * 0.35)
            if ((x * 5 + y * 9 + var_idx * 7) % 37) == 0:
                c = add(c, -30)
            px[x, y] = (*c, 255)

    # Pebbles
    for i in range(10):
        x = (i * 9 + var_idx * 7) % TILE
        y = (i * 13 + var_idx * 3) % TILE
        col = add(base, 30 if i % 2 == 0 else -28)
        px[x, y] = (*col, 255)
    return im


def make_water_with_bank():
    # Horizontal bank tile: upper ~22px water, lower ~10px dirt, anti-aliased transition.
    im = Image.new('RGBA', (TILE, TILE), (0, 0, 0, 255))
    px = im.load()
    water_base = WATER_BASE[0]
    water_light = WATER_BASE[2]
    water_dark = WATER_BASE[1]
    dirt = DIRT_BASE[1]

    bank_y = 22
    for y in range(TILE):
        for x in range(TILE):
            if y < bank_y - 1:
                n = periodic_noise(x, y, 50)
                n2 = periodic_noise(x, y, 53)
                c = mix(water_base, water_light, (n + 1) * 0.5 * 0.5)
                c = mix(c, water_dark, (n2 + 1) * 0.5 * 0.35)
                # subtle wave sparkles
                if ((x * 3 + y * 7) % 29) == 0:
                    c = add(c, 24)
            elif y <= bank_y + 1:
                t = (y - (bank_y - 1)) / 2.5
                wc = mix(water_base, water_light, (periodic_noise(x, y, 54) + 1) * 0.25)
                dc = mix(dirt, add(dirt, -22), (periodic_noise(x, y, 55) + 1) * 0.35)
                c = mix(wc, dc, t)
            else:
                n = periodic_noise(x, y, 56)
                c = mix(dirt, add(dirt, 18), (n + 1) * 0.5 * 0.35)
                if ((x * 11 + y * 5) % 31) == 0:
                    c = add(c, -26)
            px[x, y] = (*c, 255)

    # shoreline foam dashes (periodic)
    for x in range(0, TILE, 5):
        y = bank_y - 1 + (1 if (x // 5) % 2 == 0 else 0)
        px[x % TILE, y] = (214, 239, 250, 255)
        px[(x + 1) % TILE, y] = (193, 226, 242, 255)
    return im


def draw_tree(canopy_color, trunk_color, variant=0):
    im = Image.new('RGBA', (TILE, TILE), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)

    # trunk
    tx = 15 if variant == 0 else 14
    d.rectangle([tx, 20, tx + 3, 31], fill=trunk_color + (255,))
    d.rectangle([tx + 1, 22, tx + 2, 31], fill=add(trunk_color, 18) + (255,))

    # canopy blobs
    if variant == 0:
        blobs = [(16, 11, 9), (10, 14, 7), (22, 14, 7), (16, 18, 8)]
    else:
        blobs = [(16, 9, 8), (11, 13, 7), (21, 13, 7), (16, 17, 9), (16, 22, 6)]

    for i, (cx, cy, r) in enumerate(blobs):
        col = canopy_color if i % 2 == 0 else add(canopy_color, 20)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col + (255,))

    # darker underside for depth
    d.ellipse([8, 16, 24, 28], fill=add(canopy_color, -25) + (220,))

    # highlight pixels for pixel-art feel
    px = im.load()
    highlights = [(11, 8), (19, 7), (23, 12), (8, 14), (15, 5)] if variant == 0 else [(14, 6), (20, 10), (9, 12), (23, 15), (16, 3)]
    for x, y in highlights:
        px[x % TILE, y % TILE] = add(canopy_color, 38) + (255,)

    return im

# Build tiles
canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0))
tiles = [
    make_grass(0),
    make_grass(1),
    make_grass(2),
    make_dirt(0),
    make_dirt(1),
    make_water_with_bank(),
    draw_tree(TREE_FOLIAGE[1], TREE_TRUNK, 0),
    draw_tree(TREE_FOLIAGE[0], TREE_TRUNK, 1),
]

for i, tile in enumerate(tiles):
    x = (i % COLS) * TILE
    y = (i // COLS) * TILE
    canvas.alpha_composite(tile, (x, y))

canvas.save(OUT_PATH, format='PNG')
print(OUT_PATH)
