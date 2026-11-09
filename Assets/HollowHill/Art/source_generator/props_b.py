from px import *
from props_a import F, sheet_poly

BL = [(46, 7, 9), (70, 11, 14), (98, 17, 20), (130, 26, 30)]

def ragged(im, seed, p=.42, band=2):
    a = np.array(im); al = a[..., 3] > 0; inner = ero(al, band, False); rng = np.random.default_rng(seed)
    drop = al & ~inner & (rng.random(al.shape) < p); a[drop, 3] = 0
    return Image.fromarray(a, 'RGBA')

def pool(w, h, seed, sc=1.0):
    s = S(w, h); cx, cy = w / 2, h / 2; rx, ry = w / 2 - 3, h / 2 - 3
    s.blob(cx, cy, rx * sc, ry * sc, seed, (46, 7, 9, 245), .38, 22); s.blob(cx, cy, rx * .86 * sc, ry * .86 * sc, seed, (70, 11, 14, 255), .38, 22)
    s.blob(cx - 1, cy - 1, rx * .6 * sc, ry * .6 * sc, seed, (98, 17, 20, 255), .38, 22)
    rng = np.random.default_rng(seed)
    for _ in range(int(w / 6)):
        a = rng.uniform(0, 6.28); r0 = rx * .9; L = rng.integers(3, 8); s.l([(cx + math.cos(a) * r0, cy + math.sin(a) * r0 * ry / rx), (cx + math.cos(a) * (r0 + L), cy + math.sin(a) * (r0 + L) * ry / rx)], (70, 11, 14, 255)); s.pt(int(cx + math.cos(a) * (r0 + L)), int(cy + math.sin(a) * (r0 + L) * ry / rx), (46, 7, 9, 255))
    s.l([(cx - rx * .35, cy - ry * .3), (cx - rx * .1, cy - ry * .42)], (190, 70, 70, 190)); s.pt(int(cx - rx * .3), int(cy - ry * .2), (200, 90, 90, 200))
    return ragged(s.im, seed)

def splatter(w, h, seed):
    s = S(w, h); rng = np.random.default_rng(seed); cx, cy = w / 2, h / 2
    for _ in range(int(w * .9)):
        a = rng.normal(0, 1.8) if False else rng.uniform(0, 6.28); d = abs(rng.normal(0, w * .22)); x = cx + math.cos(a) * d; y = cy + math.sin(a) * d; r_ = max(1, int(3 - d / (w * .13)))
        c = BL[min(3, int(rng.integers(0, 3)) + (1 if d < w * .1 else 0))]; s.e(int(x - r_), int(y - r_), int(x + r_), int(y + r_), c + (240,))
        if d > w * .08 and rng.random() < .5: s.l([(cx + math.cos(a) * d * .5, cy + math.sin(a) * d * .5), (x, y)], BL[0] + (210,))
    s.blob(cx, cy, w * .1, h * .1, seed, BL[2] + (255,)); return s.im

def handprint(s, x, y, ang, alpha=240, c=(92, 13, 17)):
    L = Image.new('RGBA', (22, 28), (0, 0, 0, 0)); d = ImageDraw.Draw(L); col = c + (alpha,)
    d.ellipse([5, 13, 16, 25], fill=col)
    for fx, fy, fl in ((4, 3, 11), (8, 0, 14), (12, 1, 13), (16, 4, 10)): d.rectangle([fx, fy, fx + 2, fy + fl], fill=col)
    d.polygon([(3, 16), (0, 11), (2, 9), (6, 15)], fill=col)
    for k in range(6): d.point((6 + k * 2 % 9, 16 + k % 6), fill=(c[0] + 40, c[1] + 5, c[2] + 5, alpha))
    L = L.rotate(ang, expand=True, resample=Image.NEAREST); s.im.alpha_composite(L, (int(x), int(y)))

def handprints(seed=3):
    s = S(46, 38)
    handprint(s, 2, 8, 20, 240); handprint(s, 22, 2, -14, 220); handprint(s, 30, 14, 40, 170); return ragged(s.im, seed, .2, 1)

def drag(seed=4):
    W, H = 30, 130; s = S(W, H); rng = np.random.default_rng(seed); L = []; R = []
    for i in range(0, H - 18, 2):
        t = i / (H - 18); cx = 15 + math.sin(t * 5 + 1) * 6; w = 3.5 + 2.5 * math.sin(t * 9) ** 2 + (1.5 if i % 7 == 0 else 0); L.append((cx - w, i + 4)); R.append((cx + w, i + 4))
    pts = L + R[::-1]; s.p(pts, (46, 7, 9, 235)); s.p([(x + 1.2, y) for x, y in L] + [(x - 1.2, y) for x, y in R[::-1]], (70, 11, 14, 255))
    for k in range(5): xo = rng.uniform(-3, 3); s.l([(L[0][0] + 5 + xo + math.sin(i * .1) * 0, 8 + k * 6) for i in range(1)] + [(15 + xo, H - 30)], (98, 17, 20, 90))
    handprint(s, 6, H - 36, 8, 235); handprint(s, 11, H - 52, -10, 120); return ragged(s.im, seed, .35, 2)

def footprints(seed=5):
    W, H = 30, 130; s = S(W, H)
    for i in range(10):
        x = 15 + (-6 if i % 2 == 0 else 6); y = 6 + i * 12; a = int(255 * (1 - i / 11) * .9)
        s.e(x - 3, y, x + 3, y + 9, (92, 13, 17, a)); s.e(x - 2, y + 10, x + 2, y + 14, (92, 13, 17, int(a * .9)))
        for k in range(4): s.pt(x - 2 + k, y - 1, (92, 13, 17, a))
    return ragged(s.im, seed, .25, 1)

def chalk(seed=6, kind=0):
    W, H = 52, 82; s = S(W, H); C_ = (232, 232, 214, 225)
    pts = [(21, 15), (14, 18), (6, 24), (3, 36), (7, 38), (10, 30), (15, 27), (15, 47), (13, 64), (11, 76), (18, 77), (22, 60), (26, 52), (30, 60), (34, 77), (41, 76), (39, 64), (37, 47), (37, 27), (42, 30), (45, 38), (49, 36), (46, 24), (38, 18), (31, 15)]
    s.l(pts + [pts[0]], C_); s.e(19, 3, 33, 15, (0, 0, 0, 0)); s.d.ellipse([19, 3, 33, 15], outline=C_)
    im = s.im
    if kind: im = im.transpose(Image.FLIP_LEFT_RIGHT).rotate(32, expand=True, resample=Image.NEAREST)
    a = np.array(im); rng = np.random.default_rng(seed); a[(a[..., 3] > 0) & (rng.random(a.shape[:2]) < .14), 3] = 0
    return Image.fromarray(a, 'RGBA')

def evidence_marker(n, seed=7):
    s = S(12, 14); s.p([(1, 12), (3, 1), (8, 1), (10, 12)], '#b8982a'); s.p([(3, 12), (4, 3), (7, 3), (8, 12)], '#d8b83a'); s.r(1, 12, 10, 13, '#7a6418')
    s.text(3, 2, str(n), '#2a1a08', 8); return finalize(s.im, pad=3, sd=(2, 2), sa=100, grunge=.1)

def tally(seed=8):
    W, H = 56, 40; s = S(W, H)
    for g, (gx, gy) in enumerate(((4, 3), (4, 19), (30, 8))):
        for k in range(4): x = gx + k * 5; s.l([(x, gy), (x + 1, gy + 11)], (214, 208, 180, 200)); s.l([(x + 1, gy), (x + 2, gy + 11)], (10, 8, 6, 160))
        if g < 2 or True: s.l([(gx - 2, gy + 9), (gx + 18, gy + 1)], (214, 208, 180, 200)); s.l([(gx - 2, gy + 10), (gx + 18, gy + 2)], (10, 8, 6, 160))
    for k in range(3): x = 36 + k * 5; s.l([(x, 26), (x + 1, 37)], (214, 208, 180, 200)); s.l([(x + 1, 26), (x + 2, 37)], (10, 8, 6, 160))
    return s.im

def claw(seed=9):
    W, H = 44, 54; s = S(W, H); rng = np.random.default_rng(seed)
    for k in range(4):
        pts = [(6 + k * 8 + math.sin(t) * 3 + t * .8, 2 + t * 4.2) for t in np.linspace(0, 11, 14)]
        s.l(pts, (8, 6, 6, 235), 2); s.l([(x - 1, y) for x, y in pts], (210, 204, 176, 190)); s.l([(x, y + 4) for x, y in pts[:-3]], (210, 204, 176, 60))
    for _ in range(26): s.pt(int(rng.integers(2, 42)), int(rng.integers(4, 52)), (200, 192, 168, 190))
    return s.im

def spiral(seed=10):
    s = S(44, 44)
    pts = [(22 + math.cos(t) * t * 1.65, 22 + math.sin(t) * t * 1.65) for t in np.linspace(0, 13, 120)]
    s.l(pts, (8, 6, 6, 220), 2); s.l([(x - 1, y - 1) for x, y in pts], (206, 198, 170, 210)); return ragged(s.im, seed, .25, 1)

def paint_text(t, w, h, seed, size=9, col=(112, 16, 20)):
    s = S(w, h); s.text(3, 2, t, col + (255,), size, 1, seed)
    a = np.array(s.im); rng = np.random.default_rng(seed); ys, xs = np.nonzero(a[..., 3] > 0)
    for x in np.unique(xs):
        if rng.random() < .24:
            y0 = ys[xs == x].max(); L = int(rng.integers(3, 10))
            for k in range(L): 
                if y0 + 1 + k < h: a[y0 + 1 + k, x] = col + (int(230 - k * 18),)
    return Image.fromarray(a, 'RGBA')

# ---------------------------------------------------------------- decay
def debris(w, h, seed, n=9, rub=False):
    s = S(w, h); rng = np.random.default_rng(seed)
    for k in range(n):
        cx, cy = rng.integers(10, w - 10), rng.integers(8, h - 8); r_ = rng.integers(3, 9); pts = [(cx + math.cos(a) * r_ * rng.uniform(.6, 1.2), cy + math.sin(a) * r_ * rng.uniform(.6, 1.2)) for a in np.linspace(0, 6.28, 6, endpoint=False)]
        rp = P['brick'] if (rub and k % 3 == 0) else P['plaster']; i = int(rng.integers(2, 5)); s.p(pts, rp[i]); s.p([(x - .8, y - .8) for x, y in pts[:4]], rp[min(5, i + 1)]); s.p([(x + 1, y + 1) for x, y in pts[3:]], rp[max(0, i - 2)])
    for k in range(3): x, y = rng.integers(6, w - 20), rng.integers(6, h - 6); a = rng.uniform(-.6, .6); s.l([(x, y), (x + math.cos(a) * 18, y + math.sin(a) * 18)], '#503523', 2); s.l([(x, y - 1), (x + math.cos(a) * 18, y + math.sin(a) * 18 - 1)], '#82603f')
    out = finalize(s.im, pad=4, grunge=.2, sd=(2, 3)); dust = S(out.width, out.height); rng2 = np.random.default_rng(seed + 1)
    for _ in range(int(w * h * .03)): dust.pt(int(rng2.integers(0, out.width)), int(rng2.integers(0, out.height)), (190, 190, 170, 70))
    out.alpha_composite(dust.im); return out

def beam(seed=11):
    s = S(100, 18); s.bev(0, 2, 90, 15, '#503523', '#82603f', '#150e0a'); s.tx(2, 4, 88, 13, P['wood'], seed, scale=3, dither=.1)
    s.p([(90, 2), (99, 5), (94, 8), (99, 12), (91, 15)], '#68472f'); s.l([(90, 2), (99, 5)], '#a07a52')
    for x in (20, 55): s.circ(x, 9, 1, '#15191d'); s.l([(x, 9), (x + 3, 7)], '#6b6b60')
    return finalize(s.im, pad=4, grunge=.3, sd=(2, 4))

def glass(seed, w=40, h=32):
    s = S(w, h); rng = np.random.default_rng(seed)
    for _ in range(13):
        cx, cy = rng.integers(4, w - 4), rng.integers(4, h - 4); a = rng.uniform(0, 6.28); r_ = rng.integers(2, 6)
        pts = [(cx + math.cos(a) * r_, cy + math.sin(a) * r_), (cx + math.cos(a + 2.2) * r_ * .6, cy + math.sin(a + 2.2) * r_ * .6), (cx + math.cos(a + 4.1) * r_ * .9, cy + math.sin(a + 4.1) * r_ * .9)]
        s.p([(x + 1, y + 1) for x, y in pts], (0, 0, 0, 90)); s.p(pts, (150, 190, 198, 150)); s.l([pts[0], pts[1]], (240, 252, 255, 230)); s.pt(cx, cy, (255, 255, 255, 255))
    return s.im

def puddle(seed, w=56, h=40):
    s = S(w, h); s.blob(w / 2, h / 2, w / 2 - 3, h / 2 - 3, seed, (7, 15, 18, 230), .35, 20); s.blob(w / 2, h / 2, w / 2 - 6, h / 2 - 5, seed, (24, 43, 52, 255), .35, 20); s.blob(w / 2 - 2, h / 2 - 1, w / 3, h / 3, seed, (35, 60, 72, 255), .35, 20)
    s.l([(10, 12), (20, 10)], (190, 225, 235, 190)); s.l([(w - 22, h - 14), (w - 12, h - 15)], (190, 225, 235, 120)); s.d.arc([w / 2 - 8, h / 2 - 5, w / 2 + 8, h / 2 + 5], 0, 360, fill=(140, 180, 190, 90)); return ragged(s.im, seed, .3, 1)

def mold(seed, w=54, h=44, col=None):
    yy, xx = np.mgrid[0:h, 0:w]; d = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2); n = fbm(w, h, seed, 1.6)
    v = (1 - d) * 1.2 + (n - .5) * .9; a = np.zeros((h, w, 4), np.uint8); rp = col or P['moss']
    q = quant(np.clip(v, 0, .99), rp[:4], .25); aa = np.array(q); m = v > .18; a[m] = aa[m]; a[..., 3] = np.where(v > .18, np.clip(120 + v * 130, 0, 235), 0).astype(np.uint8)
    dark = v > .75; a[dark, :3] = (8, 12, 8); return Image.fromarray(a, 'RGBA')

def pigeon(seed=12):
    s = S(26, 20); s.p([(2, 8), (10, 2), (14, 5), (14, 15), (9, 18), (2, 12)], '#6b6a5f'); s.p([(14, 5), (24, 2), (23, 8), (15, 12)], '#8b8a7c'); s.p([(14, 15), (24, 18), (22, 12), (15, 11)], '#5a594f')
    s.circ(18, 10, 3, '#7b7a6d'); s.pt(19, 9, '#c0392b'); s.l([(21, 10), (24, 10)], '#a06a30'); s.l([(4, 10), (0, 7)], '#4a493f'); s.l([(6, 14), (2, 16)], '#4a493f')
    for k in range(4): s.l([(10 + k * 3, 4 + k % 2), (9 + k * 3, 8)], '#9c9b8c')
    s.blob(12, 10, 2, 2, 1, (92, 14, 16, 200)); return finalize(s.im, pad=4, grunge=.1, sd=(2, 2), sa=95)

def feathers(seed=13):
    s = S(40, 30); rng = np.random.default_rng(seed)
    for _ in range(7):
        x, y = rng.integers(4, 34), rng.integers(4, 24); a = rng.uniform(0, 6.28); L = rng.integers(4, 7)
        s.l([(x, y), (x + math.cos(a) * L, y + math.sin(a) * L)], (170, 170, 156, 230)); s.l([(x, y + 1), (x + math.cos(a) * L, y + 1 + math.sin(a) * L)], (120, 120, 108, 200))
    return s.im

def roots(seed=14):
    W, H = 70, 50; s = S(W, H); rng = np.random.default_rng(seed)
    def br(x, y, a, L, wd, dep):
        if dep == 0 or L < 3: return
        for i in range(int(L)):
            a += rng.normal(0, .12); x += math.cos(a); y += math.sin(a)
            s.circ(int(x), int(y), max(0, int(wd)), '#2a1e18'); s.pt(int(x - 1), int(y - 1), '#53402f')
            if rng.random() < .05: br(x, y, a + rng.choice([-.8, .8]), L * .6, wd * .7, dep - 1)
        br(x, y, a, L * .5, wd * .6, dep - 1)
    for k in range(3): br(4, 10 + k * 14, rng.normal(0, .4), 28, 2.2, 3)
    for k in range(5): s.crack(seed + k, rng.integers(4, 60), rng.integers(4, 40), 12, dark=(6, 5, 5))
    return finalize(s.im, pad=3, grunge=.3, sd=(2, 3), sa=90)

def vines(seed=15):
    W = H = 56; s = S(W, H); rng = np.random.default_rng(seed)
    def vine(x, y, a, L, dep):
        for i in range(int(L)):
            a += rng.normal(0, .16); x += math.cos(a); y += math.sin(a)
            s.pt(int(x), int(y), '#1b3b27'); s.pt(int(x) + 1, int(y), '#264022')
            if i % 5 == 0: lx = x + rng.integers(-3, 4); ly = y + rng.integers(-3, 4); s.e(int(lx), int(ly), int(lx) + 3, int(ly) + 2, '#36582f'); s.pt(int(lx), int(ly), '#5b8a46')
            if dep and rng.random() < .07: vine(x, y, a + rng.choice([-1, 1]) * .9, L * .45, dep - 1)
    vine(0, 4, .5, 56, 2); vine(4, 0, 1.1, 56, 2); vine(0, 20, .2, 40, 1); return finalize(s.im, pad=2, shadow=True, sd=(2, 3), sa=80, outline=False, rim=False)

def papers(seed, n=6, w=64, h=44):
    s = S(w, h); rng = np.random.default_rng(seed)
    for k in range(n):
        cx, cy = rng.integers(14, w - 14), rng.integers(10, h - 10); a = rng.uniform(0, 6.28); c, sn = math.cos(a), math.sin(a)
        def T_(x, y): return (cx + x * c - y * sn, cy + x * sn + y * c)
        s.p([T_(-9, -6), T_(9, -6), T_(9, 6), T_(-9, 6)], P['paper'][int(rng.integers(2, 5))])
        for j in range(3): s.l([T_(-7, -3 + j * 3), T_(6 - rng.integers(0, 5), -3 + j * 3)], '#4a4636')
        if rng.random() < .25: s.blob(*T_(3, 2), 2, 2, k, (96, 14, 16, 230))
    return finalize(s.im, pad=3, outline=False, rim=False, sd=(1, 2), sa=90)

def cobweb(seed=16):
    s = S(40, 40); C_ = (225, 225, 215, 150)
    for k in range(7): a = k * (math.pi / 2) / 6; s.l([(0, 0), (math.cos(a) * 38, math.sin(a) * 38)], C_)
    for r_ in (8, 15, 22, 30, 38):
        pts = []
        for k in range(7): a = k * (math.pi / 2) / 6; rr = r_ * (0.82 if 0 < k < 6 else 1); pts.append((math.cos(a) * rr, math.sin(a) * rr))
        s.l(pts, C_)
    return s.im

def stain_decal(seed, w, h, col, a=150):
    yy, xx = np.mgrid[0:h, 0:w]; d = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2); n = fbm(w, h, seed, 1.7); v = (1 - d) * 1.1 + (n - .5) * .8
    arr = np.zeros((h, w, 4), np.uint8); lv = np.round(np.clip(v * 1.4, 0, 1) * 4) / 4; arr[..., :3] = col; arr[..., 3] = (lv * a).astype(np.uint8)
    ring = (v > .2) & (v < .28); arr[ring, :3] = (col[0] * .5, col[1] * .5, col[2] * .5); arr[ring, 3] = int(a * 1.1) if a * 1.1 < 255 else 255; return Image.fromarray(arr, 'RGBA')

# ---------------------------------------------------------------- 90s
def camcorder(rec=True, seed=17):
    s = S(30, 18); s.bev(2, 3, 20, 15, '#2e353c', '#5f6b76', '#08090a'); s.bev(18, 5, 28, 13, '#15191d', '#444d56', '#050607'); s.circ(24, 9, 3, '#050607'); s.circ(24, 9, 2, '#22464f'); s.pt(23, 8, '#c8f0f5')
    s.bev(4, 0, 12, 4, '#444d56', '#8794a0', '#15191d'); s.r(5, 7, 14, 12, '#1d2227'); s.pt(16, 5, '#e03030' if rec else '#4a1010'); s.l([(2, 8), (0, 14)], '#15191d', 2); s.r(7, 14, 15, 16, '#0a0d0f')
    out = finalize(s.im, pad=4, grunge=.15, sd=(2, 3))
    if rec:
        g = S(out.width, out.height); g.circ(4 + 16, 4 + 5, 3, (255, 40, 40, 60)); out.alpha_composite(g.im)
    return out

def vhs(seed=18):
    s = S(20, 11); s.bev(0, 0, 19, 10, '#15191d', '#444d56', '#050607'); s.r(3, 2, 16, 6, '#c6c5b3'); s.r(4, 3, 10, 3, '#8a1a1a'); s.l([(4, 5), (14, 5)], '#4a4636'); s.circ(5, 8, 1, '#050607'); s.circ(14, 8, 1, '#050607'); s.r(7, 8, 12, 9, '#2e353c')
    return finalize(s.im, pad=3, grunge=.2, sd=(2, 2), sa=95)

def walkman(seed=19):
    s = S(16, 12); s.bev(0, 0, 15, 11, '#a58a2a', '#d8be52', '#4a3a0c'); s.bev(2, 2, 9, 9, '#15191d', '#444d56', '#050607'); s.r(11, 2, 14, 3, '#2a1a0e'); s.circ(12, 7, 1, '#c0392b'); s.l([(15, 3), (20, 6)], '#15191d')
    return finalize(s.im, pad=4, grunge=.2, sd=(2, 2), sa=95)

def pager(seed=20):
    s = S(10, 8); s.bev(0, 0, 9, 7, '#23282d', '#5f6b76', '#08090a'); s.r(2, 1, 7, 3, '#7a9a6a'); s.pt(3, 5, '#c0392b'); s.pt(6, 5, '#8794a0')
    return finalize(s.im, pad=3, sd=(1, 2), sa=95)

def polaroid(seed=21):
    s = S(16, 19); s.bev(0, 0, 15, 18, '#dddcc8', '#ffffff', '#6b6a5f'); s.r(2, 2, 13, 12, '#15191d'); s.circ(7, 7, 3, '#2a2d2b'); s.circ(7, 6, 2, '#6a6a5e'); s.r(5, 10, 9, 12, '#3a3a34'); s.pt(6, 6, '#0a0a0a'); s.pt(8, 6, '#0a0a0a')
    s.blob(3, 15, 1, 1, 1, (96, 14, 16, 220)); return rot(finalize(s.im, pad=3, grunge=.15, sd=(2, 2), sa=95), 0).rotate(18, expand=True, resample=Image.NEAREST)

def maglite(on=False, seed=22):
    s = S(10, 34); s.bev(2, 7, 7, 31, '#23282d', '#5f6b76', '#08090a')
    for y in (11, 14, 24, 27): s.r(2, y, 7, y, '#08090a')
    s.bev(0, 0, 9, 8, '#444d56', '#98a6b1', '#15191d'); s.circ(4, 3, 3, '#e8e4c8' if on else '#6f7c87'); s.r(2, 31, 7, 33, '#15191d'); s.r(3, 8, 3, 30, (255, 255, 255, 60))
    return finalize(s.im, pad=3, grunge=.15, sd=(2, 3))

def vending(seed=23):
    s = S(46, 46); s.bev(0, 0, 45, 45, '#7a1a1e', '#b8444a', '#2a0508'); s.tx(2, 2, 43, 43, RP('#2a0508', '#4a0c10', '#6a1216', '#8a1a1e'), seed, scale=2, dither=.1)
    for k in range(8): s.r(6, 6 + k * 3, 39, 6 + k * 3, '#1a0306')
    s.bev(30, 32, 42, 43, '#2e353c', '#8794a0', '#08090a'); s.r(33, 35, 39, 37, '#0e1a1f'); s.r(6, 34, 26, 42, '#15191d'); s.stain(seed, (20, 8, 6), thr=.55, gain=5, maxa=.6, scale=1.6)
    return finalize(s.im, pad=5, grunge=.3)

def newspaper(seed=24):
    s = S(34, 26); s.p([(1, 4), (17, 1), (17, 22), (2, 24)], '#b5af8f'); s.p([(17, 1), (33, 4), (32, 24), (17, 22)], '#c6c0a0'); s.l([(17, 1), (17, 22)], '#6b6650')
    s.r(4, 5, 15, 8, '#2a2820'); s.r(20, 5, 30, 8, '#2a2820'); s.r(4, 10, 8, 16, '#5a5642')
    for y in (10, 12, 14, 16, 18, 20): s.l([(10, y), (15, y)], '#6b6650'); s.l([(20, y), (30, y)], '#6b6650')
    return rot(finalize(s.im, pad=3, grunge=.2, outline=False, sd=(2, 2), sa=90), 0).rotate(-10, expand=True, resample=Image.NEAREST)

def police_tape(seed=25, w=96):
    s = S(w, 12); pts = [(x, 6 + math.sin(x / 9) * 2) for x in range(0, w, 2)]
    top = [(x, y - 3) for x, y in pts]; bot = [(x, y + 3) for x, y in pts]; s.p(top + bot[::-1], '#d8b83a')
    for x in range(0, w, 8): s.p([(x, 0), (x + 4, 0), (x + 1, 12), (x - 3, 12)], '#15130d')
    s.l(top, '#e8d060'); s.l(bot, '#7a6418'); return finalize(s.im, pad=3, outline=False, rim=False, sd=(1, 3), sa=80)

def cassette(seed=26):
    s = S(20, 13); s.bev(0, 0, 19, 12, '#23282d', '#5f6b76', '#08090a'); s.r(2, 1, 17, 6, '#c6c5b3'); s.r(3, 2, 16, 2, '#8a1a1a'); s.circ(6, 8, 2, '#050607'); s.circ(13, 8, 2, '#050607'); s.circ(6, 8, 1, '#8a8a7a'); s.circ(13, 8, 1, '#8a8a7a'); s.l([(4, 4), (15, 4)], '#4a4636')
    return finalize(s.im, pad=3, grunge=.15, sd=(2, 2), sa=95)

# ---------------------------------------------------------------- dynamic frames
def neon(state, seed=27):
    W, H = 96, 18; s = S(W, H); s.bev(0, 3, W - 1, 14, '#444d56', '#8794a0', '#15191d'); s.r(3, 5, W - 4, 12, '#1d2227')
    if state == 'on': s.r(4, 6, W - 5, 11, '#e8f0e0'); s.r(4, 7, W - 5, 9, '#ffffff'); s.r(4, 11, W - 5, 11, '#b8c8b0')
    elif state == 'dim': s.r(4, 6, W - 5, 11, '#6f7c70'); s.r(4, 7, W - 5, 9, '#98a898')
    elif state == 'half': s.r(4, 6, 38, 11, '#e8f0e0'); s.r(4, 7, 38, 9, '#ffffff'); s.r(39, 6, W - 5, 11, '#2a312c')
    elif state == 'off': s.r(4, 6, W - 5, 11, '#2a312c'); s.l([(8, 7), (80, 7)], (160, 170, 160, 70))
    elif state == 'broken': s.r(4, 6, 50, 11, '#2a312c'); s.p([(50, 6), (60, 8), (54, 11), (50, 11)], '#2a312c'); s.l([(52, 12), (58, 17)], '#2a312c', 2)
    for x in (2, W - 5): s.bev(x, 1, x + 3, 16, '#5f6b76', '#98a6b1', '#1d2227')
    return finalize(s.im, pad=4, grunge=.2, sd=(2, 4))

def pendant(frame, seed=28):
    ang = math.sin(frame / 6 * 2 * math.pi) * 9; s = S(40, 40); c = 20
    s.l([(c, c - 16), (c + ang * .35, c)], '#15191d'); s.circ(c, c - 16, 2, '#444d56')
    shade = S(40, 40); shade.circ(c, c, 12, '#2a3a2a'); shade.circ(c, c, 11, '#4e6150'); shade.circ(c, c, 8, '#657a66'); shade.circ(c - 2, c - 2, 5, '#7f957f'); shade.circ(c, c, 3, '#ffe9a6'); shade.pt(c - 1, c - 1, '#ffffff')
    s.paste(shade.im.transform((40, 40), Image.AFFINE, (1, 0, -ang * .55, 0, 1, 0), resample=Image.NEAREST), 0, 0)
    return finalize(s.im, pad=6, grunge=.1, sd=(int(3 + ang * .5), 6), sa=110)

def phone_frame(k, seed=29):
    s = S(26, 22); dx = (-1, 0, 1, 0)[k % 4]; dy = (0, -1, 0, 1)[k % 4]
    s.rr(2 + dx, 5 + dy, 23 + dx, 20 + dy, '#15191d', 3); s.circ(12 + dx, 13 + dy, 6, '#2e353c'); s.circ(12 + dx, 13 + dy, 4, '#15191d')
    for j in range(8): a = j * .75; s.pt(int(12 + dx + math.cos(a) * 5), int(13 + dy + math.sin(a) * 5), '#c6c5b3')
    s.rr(0 + dx, 0 + dy - (1 if k % 2 else 0), 25 + dx, 6 + dy - (1 if k % 2 else 0), '#23282d', 2); s.l([(3 + dx, 3 + dy), (22 + dx, 3 + dy)], '#5f6b76')
    return finalize(s.im, pad=4, grunge=.15, sd=(2, 3))

# ---------------------------------------------------------------- pickups
def ammo(seed=30):
    s = S(26, 18); s.bev(0, 4, 25, 17, '#5a5a30', '#8a8a4a', '#1e1e0c'); s.r(3, 7, 22, 14, '#a59f80'); s.r(5, 9, 20, 9, '#4a4636'); s.r(5, 12, 14, 12, '#4a4636'); s.r(17, 11, 20, 13, '#8a1a1a')
    for k in range(6): s.r(3 + k * 3, 0, 4 + k * 3, 4, '#a67c28'); s.r(3 + k * 3, 0, 4 + k * 3, 1, '#d8b060')
    return finalize(s.im, pad=3, grunge=.2, sd=(2, 2))

def firstaid(seed=31):
    s = S(26, 22); s.bev(0, 0, 25, 21, '#aaa999', '#dddcc8', '#4d4c44'); s.r(10, 4, 15, 17, '#8a1a1a'); s.r(5, 9, 20, 12, '#8a1a1a'); s.r(10, 4, 15, 4, '#b84040'); s.r(5, 9, 20, 9, '#b84040')
    s.bev(10, 0, 15, 2, '#6f7c87', '#c3ced6', '#2e353c'); s.stain(seed, (50, 36, 20), thr=.6, gain=6, maxa=.5, scale=2)
    return finalize(s.im, pad=3, grunge=.2, sd=(2, 2))

def battery(seed=32):
    s = S(18, 14)
    for y, c in ((1, '#a67c28'), (8, '#a67c28')): s.bev(0, y, 14, y + 4, '#15191d', '#444d56', '#050607'); s.r(14, y + 1, 16, y + 3, c); s.r(2, y + 1, 9, y + 3, c); s.r(2, y + 2, 9, y + 2, '#e8c864')
    return finalize(s.im, pad=3, sd=(2, 2))

def key_brass(seed=33):
    s = S(24, 10); s.circ(4, 5, 4, '#a67c28'); s.circ(4, 5, 2, (0, 0, 0, 0)); s.circ(4, 5, 1, '#15130d'); s.r(8, 4, 20, 6, '#a67c28'); s.r(8, 4, 20, 4, '#e8c864'); s.r(16, 6, 18, 9, '#a67c28'); s.r(19, 6, 20, 8, '#a67c28'); s.pt(3, 3, '#fff2b0')
    return finalize(s.im, pad=3, sd=(2, 2))

def note(seed=34):
    s = S(18, 22); s.p([(1, 1), (16, 0), (17, 20), (0, 21)], '#b5af8f'); s.p([(1, 1), (8, 0), (8, 21), (0, 21)], '#c6c0a0')
    for y in range(4, 19, 3): s.l([(3, y), (13 - (y % 4), y)], '#4a3a2a')
    s.blob(12, 17, 2, 2, 3, (96, 14, 16, 230)); return finalize(s.im, pad=3, outline=True, sd=(2, 2), sa=90)

def glow(seed=0, col=(255, 235, 170), size=56):
    yy, xx = np.mgrid[0:size, 0:size]; d = np.sqrt((xx - size / 2) ** 2 + (yy - size / 2) ** 2) / (size / 2); a = np.clip(1 - d, 0, 1) ** 2.2
    arr = np.zeros((size, size, 4), np.uint8); arr[..., :3] = col; arr[..., 3] = (a * 150).astype(np.uint8); return Image.fromarray(arr, 'RGBA')

def build(dec, decay, nin, dyn, pick):
    d = dec
    for i, sd in enumerate((1, 2, 3)): d.add(f'decal_blood_pool_{"abc"[i]}', pool(44 + i * 14, 36 + i * 12, sd * 11, 1))
    d.add('decal_blood_splatter_a', splatter(54, 54, 5)); d.add('decal_blood_splatter_b', splatter(40, 40, 6)); d.add('decal_blood_handprints', handprints()); d.add('decal_blood_drag', drag()); d.add('decal_blood_footprints', footprints())
    d.add('decal_chalk_body_a', chalk(6, 0)); d.add('decal_chalk_body_b', chalk(7, 1))
    for n in (1, 2, 3, 4): d.add(f'decal_evidence_marker_{n}', evidence_marker(n))
    d.add('decal_tally_marks', tally()); d.add('decal_claw_scratches', claw()); d.add('decal_spiral_scratch', spiral())
    d.add('decal_text_dont_look_up', paint_text("DON'T LOOK UP", 126, 26, 3)); d.add('decal_text_they_never_left', paint_text('THEY NEVER LEFT', 142, 26, 4)); d.add('decal_text_get_out', paint_text('GET OUT', 76, 26, 5, 11))
    d.add('decal_text_room_13', paint_text('ROOM 13', 76, 26, 6, 11, (150, 150, 130))); d.add('decal_text_help_us', paint_text('HELP US', 76, 26, 7, 11)); d.add('decal_text_he_watches', paint_text('HE WATCHES', 110, 26, 8, 10))
    c = decay
    c.add('decay_debris_plaster_a', debris(60, 46, 1)); c.add('decay_debris_plaster_b', debris(48, 40, 2, 7)); c.add('decay_rubble_pile', debris(70, 56, 3, 16, True)); c.add('decay_beam_fallen', beam())
    c.add('decay_glass_shards_a', glass(1)); c.add('decay_glass_shards_b', glass(2, 32, 26)); c.add('decay_puddle_a', puddle(1)); c.add('decay_puddle_b', puddle(2, 44, 34)); c.add('decay_puddle_c', puddle(3, 70, 46))
    c.add('decay_mold_a', mold(1)); c.add('decay_mold_b', mold(2, 40, 34)); c.add('decay_mold_corner', mold(3, 64, 50)); c.add('decay_water_stain', stain_decal(4, 70, 54, (28, 20, 10), 150)); c.add('decay_rust_stain', stain_decal(5, 50, 60, (110, 56, 22), 130))
    c.add('decay_pigeon_dead', pigeon()); c.add('decay_feathers', feathers()); c.add('decay_roots_floor', roots()); c.add('decay_vines_corner', vines()); c.add('decay_papers_a', papers(1)); c.add('decay_papers_b', papers(2, 9, 78, 52))
    cw = cobweb()
    for i, (n, im) in enumerate((('tl', cw), ('tr', cw.transpose(Image.FLIP_LEFT_RIGHT)), ('bl', cw.transpose(Image.FLIP_TOP_BOTTOM)), ('br', cw.transpose(Image.ROTATE_180)))): c.add(f'decay_cobweb_{n}', im)
    n_ = nin
    n_.add('item_camcorder_rec', camcorder(True)); n_.add('item_camcorder_off', camcorder(False)); n_.add('item_vhs_tape', vhs()); n_.add('item_walkman', walkman()); n_.add('item_pager', pager()); n_.add('item_polaroid', polaroid())
    n_.add('item_maglite_off', maglite(False)); n_.add('item_maglite_on', maglite(True)); n_.add('item_vending_machine', vending()); n_.add('item_newspaper_1993', newspaper()); n_.add('item_police_tape', police_tape()); n_.add('item_cassette', cassette())
    y = dyn
    for st in ('on', 'dim', 'half', 'off', 'broken'): y.add(f'anim_lamp_neon_{st}', neon(st))
    for k in range(6): y.add(f'anim_lamp_pendant_swing_{k}', pendant(k))
    for k in range(4): y.add(f'anim_phone_ring_{k}', phone_frame(k))
    p = pick
    p.add('pickup_ammo_box', ammo()); p.add('pickup_firstaid', firstaid()); p.add('pickup_battery', battery()); p.add('pickup_key_brass', key_brass()); p.add('pickup_note', note()); p.add('pickup_audio_tape', cassette(1)); p.add('pickup_glow_warm', glow(0, (255, 235, 170))); p.add('pickup_glow_green', glow(0, (170, 255, 190)))

if __name__ == '__main__':
    sh = [Sheet(n) for n in ('decals_blood_marks', 'decay_props', 'items_90s', 'anim_frames', 'pickups')]
    build(*sh)
    for x in sh: x.save()
