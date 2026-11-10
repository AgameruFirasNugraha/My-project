from px import *
from props_a import F

# ----------------------------------------------------------------- vegetation
def tree_dead(seed, W=150, n=7):
    s = S(W, W); rng = np.random.default_rng(seed); c = W // 2
    def br(x, y, a, L, w, dep):
        for i in range(int(L)):
            a += rng.normal(0, .09); x += math.cos(a); y += math.sin(a); r_ = max(0, int(round(w)))
            s.circ(int(x), int(y), r_, '#2a1e18')
            if r_ >= 1: s.pt(int(x) - 1, int(y) - 1, '#53402f')
            if dep > 0 and i > L * .2 and rng.random() < .13: br(x, y, a + rng.choice([-1, 1]) * rng.uniform(.5, 1.0), L * .62, w * .68, dep - 1)
        if dep > 0: br(x, y, a + rng.normal(0, .25), L * .55, w * .7, dep - 1)
    for k in range(n): br(c, c, k * (6.28 / n) + rng.normal(0, .3), W * .24, 2.7, 3)
    s.circ(c, c, 9, '#0e0a08'); s.circ(c, c, 8, '#3c2c22'); s.circ(c - 1, c - 1, 6, '#53402f'); s.circ(c, c, 3, '#2a1e18'); s.circ(c, c, 1, '#0e0a08')
    return finalize(s.im, pad=4, grunge=.2, sd=(9, 11), sa=95)

def tree_leafy(seed, W=150, rp=None, n=28):
    rp = rp or P['pine']; s = S(W, W); c = W / 2; rng = np.random.default_rng(seed)
    s.circ(int(c), int(c), int(W * .46), rp[0])
    for _ in range(n):
        a = rng.uniform(0, 6.28); d = rng.uniform(0, W * .30); x = c + math.cos(a) * d; y = c + math.sin(a) * d; r_ = int(rng.uniform(W * .10, W * .18))
        k = int(np.clip(1.6 + (-(x - c) - (y - c)) / (W * .35) * 1.4 + rng.normal(0, .5), 1, len(rp) - 1))
        s.circ(int(x), int(y), r_, rp[k]); s.circ(int(x - r_ * .3), int(y - r_ * .3), int(r_ * .55), rp[min(len(rp) - 1, k + 1)])
    rr = np.random.default_rng(seed + 3)
    for _ in range(W * W // 14):
        x, y = int(rr.integers(0, W)), int(rr.integers(0, W))
        if s.im.getpixel((x, y))[3]: s.pt(x, y, rp[int(rr.integers(0, len(rp)))])
    return finalize(s.im, pad=4, grunge=.15, sd=(10, 12), sa=100, outline=False)

def pine(seed, W=124):
    s = S(W, W); c = W // 2; rp = P['pine']
    for ring, (R, col) in enumerate([(58, rp[1]), (46, rp[2]), (34, rp[3]), (22, rp[4])]):
        pts = []; n = 16
        for k in range(n * 2): a = k * math.pi / n + ring * .2; r_ = R if k % 2 == 0 else R * .55; pts.append((c + math.cos(a) * r_, c + math.sin(a) * r_))
        s.p(pts, col)
        for k in range(0, n * 2, 2):
            a = k * math.pi / n + ring * .2
            if math.cos(a) + math.sin(a) < 0: s.l([(c, c), (c + math.cos(a) * R * .9, c + math.sin(a) * R * .9)], rp[min(4, ring + 1)])
    s.circ(c, c, 3, '#0e0a08'); return finalize(s.im, pad=4, grunge=.15, sd=(9, 11), sa=100)

def bush(dead=False, seed=1, W=50):
    s = S(W, W); rng = np.random.default_rng(seed); c = W // 2
    if dead:
        for k in range(18): a = rng.uniform(0, 6.28); L = rng.uniform(10, 22); pts = [(c, c), (c + math.cos(a) * L * .5 + rng.normal(0, 2), c + math.sin(a) * L * .5 + rng.normal(0, 2)), (c + math.cos(a) * L, c + math.sin(a) * L)]; s.l(pts, '#2a1e18', 1); s.l([(x - 1, y - 1) for x, y in pts], '#53402f')
    else:
        for _ in range(9): a = rng.uniform(0, 6.28); d = rng.uniform(0, 11); x = c + math.cos(a) * d; y = c + math.sin(a) * d; r_ = int(rng.uniform(6, 10)); k = int(rng.integers(1, 4)); s.circ(int(x), int(y), r_, P['moss'][k]); s.circ(int(x - 2), int(y - 2), r_ // 2, P['moss'][k + 1])
    return finalize(s.im, pad=3, grunge=.15, sd=(4, 5), sa=95, outline=not dead)

def stump(seed=2):
    s = S(32, 32); s.circ(16, 16, 14, '#1a1210'); s.circ(16, 16, 13, '#3c2c22'); s.circ(16, 16, 10, '#82603f')
    for r_ in (8, 6, 4, 2): s.circ(16, 16, r_, '#68472f' if r_ % 4 == 0 else '#82603f'); s.d.ellipse([16 - r_, 16 - r_, 16 + r_, 16 + r_], outline=C('#503523'))
    s.crack(seed, 16, 16, 10, dark=(30, 20, 12)); return finalize(s.im, pad=4, grunge=.2, sd=(4, 5))

def log(seed=3):
    s = S(100, 22); s.bev(6, 3, 93, 18, '#3c2c22', '#68472f', '#0e0a08'); s.tx(8, 5, 91, 16, P['bark'], seed, scale=4, dither=.1)
    for x in (6, 93): s.e(x - 4, 2, x + 4, 19, '#82603f'); s.d.ellipse([x - 2, 6, x + 2, 15], outline=C('#503523'))
    s.l([(40, 4), (44, 0)], '#3c2c22', 2); s.l([(70, 18), (73, 21)], '#3c2c22', 2); return finalize(s.im, pad=4, grunge=.25, sd=(3, 5))

# ----------------------------------------------------------------- landmarks
def fountain(seed=4):
    W = 164; s = S(W, W); c = W // 2
    s.circ(c, c, 78, '#1b1c1b'); s.circ(c, c, 76, '#7c8280'); s.circ(c, c, 72, '#646967'); s.circ(c, c, 64, '#4e5250'); s.circ(c, c, 60, '#2a2c2b')
    for a in np.linspace(0, 6.28, 30, endpoint=False): s.l([(c + math.cos(a) * 64, c + math.sin(a) * 64), (c + math.cos(a) * 75, c + math.sin(a) * 75)], '#3b3e3c')
    s.mtx(lambda d: d.ellipse([c - 58, c - 58, c + 58, c + 58], fill=255), P['water'], seed, scale=2.4, dither=.16, gain=1.2)
    rng = np.random.default_rng(seed)
    for _ in range(46): a = rng.uniform(0, 6.28); d_ = rng.uniform(8, 54); x = c + math.cos(a) * d_; y = c + math.sin(a) * d_; s.e(int(x), int(y), int(x) + 4, int(y) + 2, ['#4a2f14', '#6b4218', '#2f2b12'][int(rng.integers(0, 3))])
    for _ in range(30): a = rng.uniform(0, 6.28); d_ = rng.uniform(10, 54); x = c + math.cos(a) * d_; y = c + math.sin(a) * d_; s.l([(x, y), (x + rng.integers(3, 9), y)], (150, 190, 200, 70))
    s.blob(c + 30, c + 24, 14, 10, 3, (16, 40, 24, 190)); s.circ(c, c, 22, '#1b1c1b'); s.circ(c, c, 20, '#7c8280'); s.circ(c, c, 17, '#646967')
    for sgn in (-1, 1):
        pts = [(c, c - 4), (c + sgn * 22, c - 14), (c + sgn * 40, c - 6), (c + sgn * 38, c + 6), (c + sgn * 22, c + 4), (c, c + 6)]
        s.p(pts, '#9aa09d'); s.p([(c, c - 4), (c + sgn * 22, c - 14), (c + sgn * 28, c - 8), (c, c)], '#b9bfbc')
        for k in range(1, 6): s.l([(c + sgn * 4 * k, c - 4 + k), (c + sgn * (8 + 6 * k), c - 12 + 2 * k + 4)], '#646967')
    s.circ(c, c, 7, '#8a908d'); s.circ(c - 1, c - 1, 5, '#b9bfbc'); s.circ(c, c + 2, 3, '#4e5250'); s.l([(c - 3, c + 1), (c + 3, c + 1)], '#2a2c2b')
    s.crack(seed, c - 40, c + 50, 22, dark=(10, 10, 10)); s.stain(seed + 1, (20, 30, 14), thr=.6, gain=6, maxa=.5, scale=2.2)
    return finalize(s.im, pad=5, grunge=.2, sd=(7, 9), sa=100)

def flagpole(seed=5):
    W, H = 80, 44; s = S(W, H); s.circ(8, 22, 7, '#454a4f'); s.circ(8, 22, 5, '#767d83'); s.circ(8, 22, 2, '#15191d')
    top = [(8 + x, 20 + math.sin(x / 7) * 3 - x * .03) for x in range(0, 66, 2)]; bot = [(x, y + 18 - (x - 8) * .06) for x, y in top]
    s.p(top + bot[::-1], '#6b1a1e')
    for k in range(0, 18, 6): s.l([(x, y + k) for x, y in top], '#a59f80')
    s.p([(8, 20), (22, 20), (22, 34), (8, 34)], '#1c2230'); 
    s.l([(40, 28), (48, 34)], '#050607'); s.l([(52, 22), (60, 40)], '#050607'); s.stain(seed, (30, 24, 16), thr=.55, gain=5, maxa=.6, scale=2); return finalize(s.im, pad=4, grunge=.2, sd=(4, 6))

def streetlamp(seed=6):
    s = S(44, 28); s.circ(8, 14, 5, '#15191d'); s.circ(8, 14, 4, '#444d56'); s.circ(7, 13, 1, '#c3ced6'); s.l([(8, 14), (30, 14)], '#23282d', 3); s.l([(8, 13), (30, 13)], '#5f6b76')
    s.bev(28, 6, 42, 22, '#2e353c', '#8794a0', '#08090a'); s.bev(31, 9, 40, 19, '#a5864a', '#ffe9a6', '#5a421a'); s.pt(33, 11, '#ffffff'); return finalize(s.im, pad=4, grunge=.2, sd=(4, 6))

def fence(kind='iron', broken=False, seed=7):
    W, H = T, 26; s = S(W, H)
    if kind == 'iron':
        s.r(0, 10, W - 1, 12, '#1d1410'); s.r(0, 10, W - 1, 10, '#5a3a2a'); s.r(0, 18, W - 1, 19, '#1d1410')
        rng = np.random.default_rng(seed)
        for i, x in enumerate(range(3, W - 2, 7)):
            if broken and i in (3, 4, 9): continue
            if broken and i in (6, 7): s.l([(x, 4), (x + 3, 22)], '#1d1410', 2); continue
            s.r(x, 6, x + 1, 22, '#1d1410'); s.r(x, 6, x, 22, '#4a3020'); s.p([(x - 1, 4), (x, 0), (x + 2, 4), (x + 1, 6)], '#2a1a14'); s.pt(x, 1, '#b07a4a')
        for x in (0, W - 6): s.bev(x, 4, x + 5, 20, '#4e5250', '#9aa09d', '#1b1c1b'); s.circ(x + 3, 4, 2, '#7c8280')
    else:
        for x in (0, W - 5): s.bev(x, 6, x + 4, 22, '#444d56', '#8794a0', '#15191d')
        for y in range(7, 21, 2):
            for x in range(6, W - 6, 2):
                if (x + y) % 4 < 2 and not (broken and 30 < x < 56 and y > 11): s.pt(x, y, (150, 160, 168, 150))
        s.l([(0, 4), (W, 4)], '#6b7782'); 
        for x in range(2, W, 6): s.l([(x, 2), (x + 3, 6)], '#c3ced6'); s.l([(x + 3, 2), (x, 6)], '#8794a0')
        s.l([(0, 8), (W, 8)], '#8794a0'); s.l([(0, 22), (W, 22)], '#6b7782')
    return s.im

# ----------------------------------------------------------------- vehicles
def police_car(frame, door=True, seed=8):
    W, H = 196, 330; cx = 122; s = S(W, H)
    for y0 in (48, 244):
        for x0 in (cx - 61, cx + 55): s.bev(x0, y0, x0 + 6, y0 + 38, '#0a0a0a', '#2a2a2a', '#000000')
    body = [(cx - 50, 6), (cx + 50, 6), (cx + 56, 26), (cx + 56, 296), (cx + 50, 316), (cx - 50, 316), (cx - 56, 296), (cx - 56, 26)]
    s.p(body, '#14181c'); s.p([(cx - 47, 10), (cx + 47, 10), (cx + 52, 26), (cx + 52, 100), (cx - 52, 100), (cx - 52, 26)], '#1d2227')
    s.l([(cx - 30, 14), (cx - 30, 98)], '#14181c'); s.l([(cx + 30, 14), (cx + 30, 98)], '#14181c'); s.l([(cx - 40, 18), (cx - 12, 18)], (255, 255, 255, 40))
    for x in (cx - 44, cx + 32): s.bev(x, 8, x + 12, 13, '#a5864a', '#ffe9a6', '#5a421a')
    s.p([(cx - 44, 102), (cx + 44, 102), (cx + 37, 140), (cx - 37, 140)], '#0b161a'); s.p([(cx - 44, 102), (cx - 20, 102), (cx - 38, 140), (cx - 37, 140)], '#12262c')
    s.l([(cx - 28, 106), (cx - 6, 136)], (200, 235, 240, 120), 3); s.l([(cx + 4, 106), (cx + 20, 130)], (200, 235, 240, 70), 2); s.l([(cx + 14, 112), (cx + 30, 130), (cx + 26, 138)], (230, 245, 248, 170))
    s.mtx(lambda d: d.polygon([(cx - 38, 142), (cx + 38, 142), (cx + 41, 224), (cx - 41, 224)], fill=255), P['white'], seed, scale=3, dither=.12, gain=.3)
    s.l([(cx - 38, 142), (cx + 38, 142)], '#dddcc8'); s.l([(cx - 41, 224), (cx + 41, 224)], '#6b6a5f')
    s.p([(cx - 40, 226), (cx + 40, 226), (cx + 46, 254), (cx - 46, 254)], '#0b161a'); s.l([(cx - 30, 230), (cx - 14, 250)], (200, 235, 240, 90), 2)
    s.p([(cx - 50, 256), (cx + 50, 256), (cx + 54, 296), (cx + 48, 312), (cx - 48, 312), (cx - 54, 296)], '#1d2227'); s.r(cx - 3, 280, cx + 3, 284, '#98a6b1')
    for x in (cx - 48, cx + 36): s.bev(x, 306, x + 12, 311, '#7a1a1a', '#c04040', '#2a0808')
    s.bev(cx - 36, 172, cx + 36, 188, '#23282d', '#5f6b76', '#08090a')
    L = ('#ff3a3a', '#ffb0b0') if frame == 0 else ('#4a0e0e', '#7a2a2a'); R = ('#4a60ff', '#b0c0ff') if frame == 1 else ('#0e1a4a', '#2a3a7a')
    s.bev(cx - 34, 174, cx - 2, 186, L[0], L[1], '#2a0808'); s.bev(cx + 2, 174, cx + 34, 186, R[0], R[1], '#08102a')
    for x in (cx - 40, cx + 34): s.bev(x - 2, 98, x + 12, 104, '#23282d', '#5f6b76', '#08090a')
    s.bev(cx - 60, 96, cx - 52, 102, '#23282d', '#5f6b76', '#08090a'); s.bev(cx + 52, 96, cx + 60, 102, '#23282d', '#5f6b76', '#08090a')
    if door:
        h = (cx - 56, 106); tip = (h[0] - 44, h[1] + 34); s.l([h, tip], '#0a0d0f', 11); s.l([h, tip], '#b8b7a6', 8); s.l([(h[0] - 2, h[1] + 3), (tip[0] + 3, tip[1] - 3)], '#0b161a', 3); s.l([h, tip], '#dddcc8', 1)
    s.crack(seed, cx + 20, 200, 18, dark=(30, 30, 28)); s.stain(seed + 1, (40, 20, 10), thr=.7, gain=6, maxa=.35, scale=2.2); s.speck(seed + 2, .005, ['#0a0d0f', '#5f6b76'])
    out = finalize(s.im, pad=6, grunge=.3, sd=(8, 10), sa=105)
    g = S(out.width, out.height); col = (255, 50, 50) if frame == 0 else (70, 90, 255); gx = (cx - 18 if frame == 0 else cx + 18) + 6
    for r_, a in ((36, 26), (24, 40), (14, 60)): g.circ(gx, 186 + 6, r_, col + (a,))
    out.alpha_composite(g.im); return out

def ambulance(open_=False, seed=9):
    W, H = 188, 420; cx = 94; s = S(W, H)
    for y0 in (46, 284):
        for x0 in (cx - 66, cx + 60): s.bev(x0, y0, x0 + 6, y0 + 42, '#0a0a0a', '#2a2a2a', '#000000')
    s.mtx(lambda d: d.polygon([(cx - 60, 6), (cx + 60, 6), (cx + 64, 26), (cx + 64, 100), (cx - 64, 100), (cx - 64, 26)], fill=255), P['white'], seed, scale=2.5, dither=.12, gain=.3)
    s.p([(cx - 50, 40), (cx + 50, 40), (cx + 44, 76), (cx - 44, 76)], '#0b161a'); s.l([(cx - 34, 44), (cx - 12, 72)], (200, 235, 240, 110), 3)
    for x in (cx - 50, cx + 38): s.bev(x, 8, x + 12, 14, '#a5864a', '#ffe9a6', '#5a421a')
    s.mtx(lambda d: d.polygon([(cx - 62, 102), (cx + 62, 102), (cx + 66, 118), (cx + 66, 382), (cx - 66, 382), (cx - 66, 118)], fill=255), P['white'], seed + 1, scale=3, dither=.12, gain=.3)
    s.r(cx - 62, 110, cx - 54, 374, '#7a1a1a'); s.r(cx + 54, 110, cx + 62, 374, '#7a1a1a'); s.r(cx - 62, 110, cx - 62, 374, '#b84040')
    for y in (150, 210): s.bev(cx - 22, y, cx + 22, y + 26, '#8794a0', '#dde3e8', '#3c454c'); [s.r(cx - 18, y + 4 + k * 5, cx + 18, y + 5 + k * 5, '#2e353c') for k in range(4)]
    s.r(cx - 3, 120, cx + 3, 372, (0, 0, 0, 40)); s.bev(cx - 30, 330, cx + 30, 346, '#8a1a1a', '#c04040', '#2a0808'); s.r(cx - 3, 334, cx + 3, 342, '#dddcc8'); s.r(cx - 10, 337, cx + 10, 339, '#dddcc8')
    s.bev(cx - 34, 108, cx + 34, 120, '#23282d', '#5f6b76', '#08090a'); s.bev(cx - 32, 110, cx - 2, 118, '#ff3a3a', '#ffb0b0', '#2a0808'); s.bev(cx + 2, 110, cx + 32, 118, '#4a0e0e', '#7a2a2a', '#08102a')
    if open_:
        for sg in (-1, 1): a = (cx + sg * 66, 384); b = (cx + sg * 118, 408); s.l([a, b], '#0a0d0f', 10); s.l([a, b], '#d6d5c3', 7); s.l([(a[0], a[1] + 2), (b[0], b[1] + 2)], '#8a1a1a', 2)
        s.r(cx - 60, 384, cx + 60, 396, '#0a0c0e'); s.stain(seed + 5, (30, 10, 10), thr=.5, gain=5, maxa=.6, scale=2.2)
    s.stain(seed + 2, (36, 24, 14), thr=.7, gain=6, maxa=.4, scale=2.2); s.crack(seed, cx - 20, 250, 20, dark=(30, 30, 26)); s.blob(cx + 30, 300, 12, 8, 2, (96, 14, 16, 200))
    return finalize(s.im, pad=6, grunge=.35, sd=(9, 11), sa=105)

# ----------------------------------------------------------------- cemetery
def marker(n, seed):
    s = S(26, 26); s.bev(1, 1, 24, 24, '#4e5250', '#9aa09d', '#1b1c1b'); s.tx(3, 3, 22, 22, P['stone'], seed, scale=2.5, dither=.12)
    s.text(5, 6, f'{n:02d}', '#15171a', 11); s.stain(seed, (30, 54, 24), thr=.55, gain=6, maxa=.7, scale=3); s.crack(seed, 14, 4, 10, dark=(8, 8, 8))
    return rot(finalize(s.im, pad=4, grunge=.2, sd=(3, 4)), 0).rotate(int((seed % 5) - 2) * 3, expand=True, resample=Image.NEAREST)

def grave_open(seed=10):
    W, H = 56, 96; s = S(W, H); rng = np.random.default_rng(seed)
    s.blob(W / 2, H / 2, 26, 46, seed, '#35271b', .1); s.blob(W / 2, H / 2, 24, 44, seed, '#4b3825', .1)
    s.r(14, 14, 41, 82, '#050403'); s.r(14, 14, 41, 18, '#150f0a'); s.r(14, 14, 15, 82, '#241b14'); s.tx(16, 20, 39, 80, RP('#020202', '#050403', '#0a0806'), seed, scale=2, dither=.3)
    s.p([(18, 70), (30, 66), (38, 72), (24, 80)], '#2a1b12'); s.l([(18, 70), (30, 66)], '#503523')
    for _ in range(40): s.pt(int(rng.integers(4, 52)), int(rng.integers(4, 92)), '#654d33')
    s.l([(48, 34), (52, 8)], '#503523', 2); s.p([(48, 8), (56, 6), (55, 14), (49, 14)], '#8794a0'); return finalize(s.im, pad=4, grunge=.25, sd=(4, 5))

def grave_mound(seed=11):
    W, H = 40, 78; s = S(W, H); s.mtx(lambda d: d.rounded_rectangle([2, 2, W - 3, H - 3], radius=8, fill=255), P['dirt'], seed, scale=3, dither=.14, gain=1.3, bias=.05)
    s.l([(6, 10), (30, 8)], '#654d33'); s.l([(5, 40), (34, 42)], '#654d33'); s.speck(seed, .05, ['#150f0a', '#7c6040']); s.r(18, 8, 21, 28, '#503523'); s.r(12, 14, 27, 17, '#503523'); s.r(18, 8, 18, 28, '#82603f'); return finalize(s.im, pad=4, grunge=.2, sd=(3, 4))

def cross_wood(seed=12):
    s = S(26, 34); s.l([(10, 2), (10, 32)], '#150e0a', 5); s.l([(10, 2), (10, 32)], '#503523', 3); s.l([(2, 10), (20, 10)], '#150e0a', 5); s.l([(2, 10), (20, 10)], '#503523', 3); s.l([(9, 2), (9, 30)], '#82603f'); s.l([(2, 9), (19, 9)], '#82603f'); s.crack(seed, 10, 20, 6, dark=(10, 6, 4))
    return rot(finalize(s.im, pad=4, grunge=.3, sd=(4, 5)), 0).rotate(12, expand=True, resample=Image.NEAREST)

def flowers(seed=13):
    s = S(20, 20); rng = np.random.default_rng(seed)
    for _ in range(9): a = rng.uniform(0, 6.28); L = rng.uniform(4, 9); s.l([(10, 10), (10 + math.cos(a) * L, 10 + math.sin(a) * L)], '#3a3820'); s.circ(int(10 + math.cos(a) * L), int(10 + math.sin(a) * L), 1, ['#6a4a3a', '#7a6a4a', '#5a3a4a'][int(rng.integers(0, 3))])
    return finalize(s.im, pad=2, outline=False, rim=False, sd=(2, 2), sa=80)

# ----------------------------------------------------------------- yard objects
def greenhouse(broken=False, seed=14):
    W, H = 168, 108; s = S(W, H); rng = np.random.default_rng(seed)
    for gx in range(0, W, 14):
        for gy in range(0, H, 12):
            a = int(rng.integers(70, 120)); s.r(gx, gy, gx + 13, gy + 11, (60, 100, 90, a)); s.l([(gx + 2, gy + 9), (gx + 9, gy + 2)], (220, 250, 245, 90))
            if broken and rng.random() < .18: s.p([(gx + 1, gy + 1), (gx + 12, gy + 2), (gx + 10, gy + 10), (gx + 3, gy + 9), (gx + 5, gy + 5)], (4, 6, 6, 235)); s.l([(gx + 12, gy + 2), (gx + 7, gy + 6)], (230, 250, 250, 220))
    for gx in range(0, W + 1, 14): s.r(gx, 0, gx, H - 1, '#1b2024'); s.r(gx + 1 if gx < W else gx - 1, 0, gx + 1 if gx < W else gx - 1, H - 1, (130, 150, 160, 130))
    for gy in range(0, H + 1, 12): s.r(0, gy, W - 1, gy, '#1b2024')
    s.r(0, H // 2 - 1, W - 1, H // 2 + 1, '#2e353c'); s.r(0, H // 2 - 1, W - 1, H // 2 - 1, '#98a6b1'); s.stain(seed, (60, 90, 40), thr=.62, gain=7, maxa=.45, scale=2.4, within=False) if False else None
    return finalize(s.im, pad=4, outline=True, rim=True, grunge=.2, sd=(6, 8), sa=70)

def greenhouse_beds(seed=15):
    W, H = 168, 108; s = S(W, H); s.setim(tex(W, H, P['dirt'], seed, 2.5, .14, 1.3)); rng = np.random.default_rng(seed)
    for bx in (10, 100):
        s.bev(bx, 8, bx + 56, 100, '#3b271a', '#82603f', '#150e0a'); s.tx(bx + 3, 11, bx + 53, 97, P['dirt'], seed + bx, scale=3, dither=.14)
        for _ in range(26): x, y = bx + int(rng.integers(6, 50)), 12 + int(rng.integers(0, 84)); s.l([(x, y), (x + int(rng.integers(-3, 4)), y - int(rng.integers(4, 11)))], '#5a5030'); s.pt(x, y - 8, '#7d7650')
    for x, y in ((80, 20), (84, 60), (88, 90)): s.circ(x, y, 7, '#5d311a'); s.circ(x, y, 5, '#35271b'); s.l([(x, y), (x + 3, y - 8)], '#5a5030')
    s.stain(seed, (30, 54, 24), thr=.6, gain=6, maxa=.5, scale=2.4, within=False); return s.im

def scarecrow(seed=16):
    W = 54; s = S(W, W); c = W // 2
    s.l([(c, 4), (c, 50)], '#150e0a', 5); s.l([(c, 4), (c, 50)], '#503523', 3); s.l([(3, 20), (51, 20)], '#150e0a', 5); s.l([(3, 20), (51, 20)], '#503523', 3)
    s.p([(5, 16), (c, 14), (49, 16), (51, 28), (44, 24), (40, 34), (c, 40), (14, 34), (10, 24), (3, 28)], '#8a856a'); s.p([(5, 16), (c, 14), (c, 40), (14, 34), (10, 24), (3, 28)], '#aaa999')
    s.l([(c - 6, 30), (c - 8, 40)], '#6b6a5f'); s.l([(c + 8, 28), (c + 12, 38)], '#6b6a5f'); s.blob(c + 6, 30, 4, 3, 1, (80, 40, 20, 160))
    for k in range(7): s.l([(2 + k * 2, 28), (0 + k * 2, 34)], '#a59f80'); s.l([(48 + k, 27), (50 + k, 33)], '#a59f80')
    s.circ(c, 20, 10, '#2a1e18'); s.circ(c, 20, 9, '#6b5a3a'); s.circ(c - 1, 19, 6, '#8a7a50'); s.circ(c, 20, 3, '#3a2a18'); s.d.ellipse([c - 9, 11, c + 9, 29], outline=C('#35210f'))
    return finalize(s.im, pad=4, grunge=.3, sd=(5, 7))

def crow(seed, ang):
    s = S(20, 24); s.e(4, 6, 15, 20, '#15171a'); s.e(5, 7, 12, 16, '#2a2d33'); s.p([(4, 12), (0, 18), (4, 22)], '#0a0b0c'); s.p([(15, 12), (19, 18), (15, 22)], '#0a0b0c'); s.circ(10, 5, 3, '#15171a'); s.l([(10, 1), (10, -0)], '#a07a30'); s.pt(9, 4, '#c8c8c0')
    s.l([(7, 8), (6, 18)], (90, 100, 120, 120)); return rot(finalize(s.im, pad=3, grunge=.1, sd=(2, 3), sa=90), ang)

def wheelbarrow(seed=17):
    W, H = 34, 60; s = S(W, H); s.l([(8, 36), (4, 58)], '#503523', 3); s.l([(26, 36), (30, 58)], '#503523', 3); s.bev(12, 0, 22, 8, '#15191d', '#444d56', '#050607')
    s.p([(3, 8), (31, 8), (27, 40), (7, 40)], '#2e353c'); s.p([(6, 10), (28, 10), (25, 38), (9, 38)], '#6b3a1c'); s.p([(9, 13), (25, 13), (23, 35), (11, 35)], '#35271b'); s.tx(11, 15, 22, 33, P['dirt'], seed, scale=2); s.l([(5, 9), (29, 9)], '#a5602d')
    s.stain(seed, (100, 50, 20), thr=.5, gain=5, maxa=.6, scale=2.4); return F(s, .3)

def coal_pile(seed=18):
    W, H = 80, 66; s = S(W, H); rng = np.random.default_rng(seed); s.blob(W / 2, H / 2, 36, 28, seed, '#14181c', .25, 16)
    for _ in range(110):
        a = rng.uniform(0, 6.28); d = rng.uniform(0, 1) ** .6 * 30; x = W / 2 + math.cos(a) * d; y = H / 2 + math.sin(a) * d * .8; r_ = rng.uniform(1.5, 4); k = int(rng.integers(0, 3))
        pts = [(x + math.cos(t) * r_ * rng.uniform(.6, 1.2), y + math.sin(t) * r_ * rng.uniform(.6, 1.2)) for t in np.linspace(0, 6.28, 5, endpoint=False)]; s.p(pts, ['#0a0d0f', '#1d2227', '#2e353c'][k]); s.pt(int(x - 1), int(y - 1), '#8794a0' if rng.random() < .3 else '#444d56')
    s.l([(60, 10), (74, 4)], '#503523', 2); s.p([(74, 0), (80, 2), (78, 8), (72, 6)], '#8794a0'); return finalize(s.im, pad=4, grunge=.2, sd=(6, 8))

def chimney(seed=19):
    W = 48; s = S(W, W); c = W // 2
    s.bev(1, 1, W - 2, W - 2, '#5b2a22', '#925042', '#2b1311'); s.tx(3, 3, W - 4, W - 4, P['brick'], seed, scale=2.2, dither=.14)
    for y in range(3, W - 3, 5): s.r(3, y, W - 4, y, '#1d1311')
    s.circ(c, c, 15, '#2b1311'); s.circ(c, c, 14, '#8a8780'); s.circ(c, c, 11, '#4a4846'); s.circ(c, c, 8, '#0a0807'); s.circ(c, c, 5, '#000000')
    s.l([(c - 10, c - 8), (c - 4, c - 12)], (255, 255, 255, 70)); s.stain(seed, (6, 6, 6), thr=.5, gain=5, maxa=.7, scale=2.5); return F(s, .3)

def laundry(seed=20):
    W, H = 140, 40; s = S(W, H); rng = np.random.default_rng(seed)
    for x in (4, W - 5): s.circ(x, 20, 3, '#15191d'); s.circ(x, 20, 2, '#444d56')
    s.l([(4, 20), (W - 5, 20)], '#6b6a5f')
    for i, x in enumerate((12, 42, 72, 102)):
        h = 22 + int(rng.integers(-3, 4)); pts = [(x + k, 21 + math.sin(k / 3 + i) * 1.5) for k in range(0, 27)]; s.p(pts + [(x + 26, 21 + h), (x, 21 + h)], '#b5b4a2'); s.p(pts[:14] + [(x + 13, 21 + h), (x, 21 + h)], '#cfcfba')
        for k in range(1, 4): s.l([(x + k * 6, 22), (x + k * 6 + int(rng.integers(-1, 2)), 21 + h)], (90, 88, 76, 130))
        s.stain(seed + i, (50, 40, 24), thr=.7, gain=8, maxa=.4, scale=2, within=True)
        s.r(x + 3, 18, x + 4, 23, '#7a5a3a'); s.r(x + 20, 18, x + 21, 23, '#7a5a3a')
    s.blob(70, 36, 3, 2, 3, (96, 14, 16, 220)); return finalize(s.im, pad=4, outline=False, grunge=.15, sd=(6, 10), sa=85)

def tent(seed=21):
    W = 76; s = S(W, W); c = W // 2; cols = [('#a05a1c', '#c07a2c'), ('#7a4010', '#a05a1c')]
    for k in range(6):
        a0 = k * 1.047 - .52; a1 = a0 + 1.047; pts = [(c, c), (c + math.cos(a0) * 34, c + math.sin(a0) * 34), (c + math.cos((a0 + a1) / 2) * 36, c + math.sin((a0 + a1) / 2) * 36), (c + math.cos(a1) * 34, c + math.sin(a1) * 34)]
        s.p(pts, cols[k % 2][0] if (math.cos((a0 + a1) / 2) + math.sin((a0 + a1) / 2)) > 0 else cols[k % 2][1])
    s.circ(c, c, 4, '#2e353c'); s.p([(c + 8, c + 14), (c + 22, c + 8), (c + 26, c + 22), (c + 12, c + 24)], '#0a0807'); s.l([(c + 8, c + 14), (c + 26, c + 22)], '#c6c5b3'); s.stain(seed, (30, 20, 12), thr=.5, gain=5, maxa=.6, scale=2.4)
    for a in (.2, 2.4, 4.3): s.l([(c + math.cos(a) * 36, c + math.sin(a) * 36), (c + math.cos(a) * 42, c + math.sin(a) * 42)], '#c6c5b3')
    return finalize(s.im, pad=4, grunge=.25, sd=(6, 8))

def campfire(seed=22):
    W = 44; s = S(W, W); c = W // 2; rng = np.random.default_rng(seed)
    for k in range(9): a = k * .7; x = c + math.cos(a) * 17; y = c + math.sin(a) * 17; s.circ(int(x), int(y), 4, '#4e5250'); s.circ(int(x - 1), int(y - 1), 2, '#7c8280'); s.pt(int(x + 2), int(y + 2), '#1b1c1b')
    s.circ(c, c, 12, '#0c0b0a'); s.circ(c, c, 9, '#1d1b19'); s.l([(c - 8, c - 2), (c + 7, c + 4)], '#150e0a', 4); s.l([(c - 6, c + 6), (c + 6, c - 6)], '#150e0a', 3); s.speck(seed, .3, ['#3a3835', '#0a0908'])
    s.pt(c + 2, c, '#c86a1c'); s.pt(c - 3, c + 3, '#6a2a0c'); return finalize(s.im, pad=3, grunge=.2, sd=(4, 5), sa=90)

def sleeping_bag(seed=23):
    s = S(40, 76); s.mtx(lambda d: d.rounded_rectangle([2, 2, 37, 73], radius=14, fill=255), P['canvas'], seed, scale=2.5, dither=.14); s.rr(4, 4, 35, 22, '#3d3b30', 10)
    for y in range(12, 72, 11): s.l([(5, y), (34, y)], (0, 0, 0, 80)); s.l([(5, y + 1), (34, y + 1)], (255, 255, 230, 40))
    s.l([(19, 22), (19, 72)], '#15130d'); s.l([(18, 22), (18, 72)], '#8794a0'); s.stain(seed, (40, 30, 18), thr=.6, gain=6, maxa=.6, scale=2.4); return F(s, .3)

def backpack(seed=24):
    s = S(32, 38); s.rr(2, 2, 29, 35, '#3a4a3c', 6); s.rr(4, 4, 27, 33, '#4e6150', 5); s.rr(7, 18, 24, 31, '#3a4a3c', 3); s.r(9, 24, 22, 24, '#15191d'); s.bev(14, 8, 18, 12, '#8794a0', '#dde3e8', '#2e353c'); s.l([(2, 8), (0, 24)], '#15191d', 2); s.l([(29, 8), (31, 24)], '#15191d', 2); return F(s, .3)

def cooler(seed=25):
    s = S(44, 32); s.bev(0, 0, 43, 31, '#4e6a78', '#8aa8b8', '#1c2a32'); s.bev(4, 4, 39, 27, '#c6c5b3', '#ececd8', '#6b6a5f'); s.r(18, 0, 25, 4, '#2e353c'); s.stain(seed, (40, 30, 16), thr=.6, gain=6, maxa=.55, scale=2); return F(s, .3)

def bench_park(seed=26):
    s = S(70, 28); s.bev(0, 0, 69, 6, '#3b271a', '#82603f', '#150e0a'); [s.bev(2, y, 67, y + 3, '#503523', '#82603f', '#150e0a') for y in (10, 15, 20)]
    for x in (6, 60): s.r(x, 8, x + 3, 25, '#1d2227'); s.stain(seed, (30, 54, 24), thr=.6, gain=6, maxa=.5, scale=2.4); return F(s, .35)

def swing_set(seed=27):
    W, H = 104, 56; s = S(W, H)
    for x in (4, W - 8): s.bev(x, 0, x + 3, H - 1, '#6b3a1c', '#a5602d', '#2a130a')
    s.bev(4, 24, W - 5, 27, '#6b3a1c', '#a5602d', '#2a130a'); s.l([(36, 26), (36, 44)], '#444d56'); s.l([(40, 26), (40, 44)], '#444d56'); s.bev(30, 44, 46, 50, '#35210f', '#68472f', '#0a0604'); s.l([(66, 26), (62, 40)], '#444d56'); s.l([(70, 26), (74, 40)], '#444d56')
    s.stain(seed, (90, 44, 18), thr=.5, gain=5, maxa=.65, scale=2.4); return finalize(s.im, pad=4, grunge=.3, sd=(6, 8))

def dumpster(seed=28):
    W, H = 84, 50; s = S(W, H); s.bev(0, 0, W - 1, H - 1, '#3a4a3c', '#657a66', '#101914'); s.tx(2, 2, W - 3, H - 3, P['pgreen'], seed, scale=2.5, dither=.12)
    s.bev(4, 4, 44, H - 5, '#2a372d', '#4e6150', '#08100c'); s.p([(48, 4), (W - 4, 6), (W - 4, H - 6), (48, H - 4)], '#0a0d0b'); s.blob(62, 28, 9, 7, 3, '#2a1a10'); s.l([(52, 12), (70, 16)], '#c6c5b3'); s.stain(seed, (100, 50, 20), thr=.55, gain=6, maxa=.6, scale=2.4); return F(s, .4)

def crate(seed=29):
    s = S(34, 34); s.bev(0, 0, 33, 33, '#503523', '#82603f', '#150e0a'); s.tx(3, 3, 30, 30, P['wood'], seed, scale=2.5)
    for y in (10, 21): s.r(3, y, 30, y, '#150e0a')
    s.l([(3, 3), (30, 30)], '#35210f', 3); s.l([(30, 3), (3, 30)], '#35210f', 3); [s.pt(x, y, '#8a8a7a') for x, y in ((4, 4), (29, 4), (4, 29), (29, 29))]; return F(s, .3)

def barrel(seed=30):
    s = S(30, 30); s.circ(15, 15, 14, '#15191d'); s.circ(15, 15, 13, '#7a3a1a'); s.circ(15, 15, 11, '#9a5a2a'); s.circ(15, 15, 9, '#7a3a1a'); s.circ(15, 15, 6, '#2a130a'); s.circ(11, 11, 2, '#c08a5a'); s.circ(22, 20, 2, '#15191d'); s.l([(6, 8), (12, 4)], (255, 255, 255, 80))
    s.stain(seed, (70, 30, 10), thr=.5, gain=5, maxa=.6, scale=2.6); return F(s, .3)

def manhole(open_=False, seed=31):
    s = S(40, 40); s.circ(20, 20, 18, '#0a0d0f'); s.circ(20, 20, 17, '#2e353c')
    if not open_:
        s.circ(20, 20, 15, '#444d56'); s.circ(20, 20, 12, '#2e353c')
        for k in range(-3, 4): s.l([(20 + k * 4, 9), (20 + k * 4, 31)], '#1d2227'); s.l([(9, 20 + k * 4), (31, 20 + k * 4)], '#1d2227')
        s.l([(8, 12), (16, 6)], (255, 255, 255, 70)); s.stain(seed, (100, 50, 20), thr=.55, gain=6, maxa=.6, scale=2.4)
    else:
        s.circ(20, 20, 15, '#020202'); s.circ(20, 20, 11, '#000000'); s.p([(26, 22), (40, 14), (44, 28), (30, 36)], '#2e353c'); s.l([(26, 22), (40, 14)], '#8794a0')
    return finalize(s.im, pad=5, grunge=.25, sd=(4, 5))

def hydrant(seed=32):
    s = S(22, 22); s.circ(11, 11, 6, '#6b1a1a'); s.circ(11, 11, 5, '#8a2a2a'); s.circ(10, 10, 2, '#c05050'); s.bev(0, 8, 21, 13, '#6b1a1a', '#b84040', '#2a0808'); s.circ(11, 11, 2, '#2e353c'); return F(s, .3)

def tunnel_entrance(seed=33):
    W, H = T + 10, 112; s = S(W, H)
    s.bev(0, 0, W - 1, 20, '#4e5250', '#9aa09d', '#1b1c1b'); s.tx(2, 2, W - 3, 18, P['concrete'], seed, scale=2)
    for i in range(7):
        y = 22 + i * 12; f = 1 - i * .13; c = tuple(int(v * f) for v in (110, 118, 124)); s.r(8, y, W - 9, y + 9, c + (255,)); s.r(8, y, W - 9, y, tuple(int(v * 1.25) for v in c) + (255,)); s.r(8, y + 10, W - 9, y + 11, '#0a0b0c')
    s.r(8, 22, W - 9, H - 1, (0, 0, 0, 0)); s.r(8, 98, W - 9, H - 1, '#020202')
    for x in (4, W - 8): s.bev(x, 20, x + 3, H - 6, '#2e353c', '#8794a0', '#08090a'); s.r(x, 20, x + 3, H - 6, '#2e353c')
    s.r(3, 40, W - 4, 41, '#15191d'); s.text(30, 3, 'STEAM', '#e8c864', 8); s.r(8, 30, 14, 90, '#15191d')
    s.stain(seed, (30, 54, 24), thr=.62, gain=6, maxa=.5, scale=2.4); return finalize(s.im, pad=3, grunge=.25, sd=(4, 5))

def hydrant_dummy(): return None

# ----------------------------------------------------------------- roofs
def slate_tex(w, h, seed, moss=0.0, dmg=0.0, wrap=True):
    s = S(w, h, wrap=wrap); rng = np.random.default_rng(seed); rows = h // 7 + 1
    for j in range(rows):
        off = (j % 2) * 6
        for i in range(-1, w // 13 + 2):
            x = i * 13 + off; y = j * 7; tn = int(rng.integers(1, 4)); bad = rng.random() < dmg
            if bad:
                s.im.paste(tex(13, 7, RP('#050403', '#0a0705', '#150e0a'), int(rng.integers(1 << 30)), 1, .3), (x % w if wrap else x, y)); s.r(x, y + 3, x + 12, y + 3, '#2a1b12'); continue
            t_ = tex(13, 7, P['slate'][tn - 1:tn + 3], int(rng.integers(1 << 30)), .5, .15, .8)
            s.im.paste(t_, (x % w if wrap else x, y))
            if wrap and (x % w) + 13 > w: s.im.paste(t_, ((x % w) - w, y))
    s.setim(s.im)
    for j in range(rows):
        off = (j % 2) * 6; s.r(0, j * 7 + 6, w - 1, j * 7 + 6, '#06090b'); s.r(0, j * 7, w - 1, j * 7, (150, 170, 185, 60))
        for i in range(-1, w // 13 + 2): s.r(i * 13 + off, j * 7, i * 13 + off, j * 7 + 6, '#06090b')
    if moss: s.stain(seed + 5, (50, 90, 40), thr=.62, gain=7, maxa=.55 * moss, scale=2.2)
    s.stain(seed + 6, (6, 8, 8), thr=.62, gain=5, maxa=.5, scale=1.5); return s.im

def roof_tile(seed, moss=0, dmg=0, hole=False):
    s = S(T, T, wrap=True); s.setim(slate_tex(T, T, seed, moss, dmg))
    if hole:
        pts = [(24, 30), (40, 22), (58, 28), (66, 44), (56, 62), (36, 68), (22, 54)]
        s.p(pts, '#030201'); s.p([(x + 0, y + 0) for x, y in pts[:4]], '#0a0705')
        for k in range(3): s.l([(14 + k * 22, 10), (18 + k * 24, 80)], '#2a1b12', 3); s.l([(14 + k * 22, 10), (14 + k * 22, 80)], '#503523')
        s.p(pts, '#030201')
        for x, y in pts: s.l([(x, y), (x + int(np.random.default_rng(x).integers(-4, 5)), y + int(np.random.default_rng(y).integers(-4, 5)))], '#503523')
    return s.im

def shade(im, mask_fn, f):
    a = np.array(im).astype(np.float32); yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]; m = mask_fn(xx, yy); a[m, :3] *= f; return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')

def roof_tower(seed=40, W=170):
    base = slate_tex(W, W, seed, .25, .04, wrap=False); c = W // 2; faces = []
    out = Image.new('RGBA', (W, W), (0, 0, 0, 0)); yy, xx = np.mgrid[0:W, 0:W]; dx = xx - c; dy = yy - c
    face = np.where(np.abs(dx) > np.abs(dy), np.where(dx < 0, 3, 1), np.where(dy < 0, 0, 2))      # 0 N,1 E,2 S,3 W
    f = {0: 1.28, 3: 1.12, 1: .62, 2: .5}
    arr = np.array(base).astype(np.float32); 
    for k, v in f.items(): arr[face == k, :3] *= v
    inside = np.maximum(np.abs(dx), np.abs(dy)) <= c - 2; arr[..., 3] = np.where(inside, 255, 0)
    s = S(W, W); s.setim(Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), 'RGBA'))
    for ex, ey in ((0, 0), (W - 1, 0), (W - 1, W - 1), (0, W - 1)): s.l([(c, c), (ex, ey)], '#050709', 3); s.l([(c - 1, c - 1) if ex == 0 and ey == 0 else (c, c), (ex, ey)], '#4d5a65', 1)
    s.circ(c, c, 8, '#15191d'); s.circ(c, c, 6, '#444d56'); s.circ(c - 1, c - 1, 3, '#98a6b1'); s.l([(c, c), (c + 3, c + 3)], '#15191d', 2)
    for k in range(4): s.r(2, 2, W - 3, 4, '#050709') if k == 0 else None
    s.d.rectangle([1, 1, W - 2, W - 2], outline=C('#050709')); s.d.rectangle([2, 2, W - 3, W - 3], outline=C('#2e353c'))
    return finalize(s.im, pad=6, grunge=.2, sd=(10, 12), sa=105, edge=False)

def roof_wing(seed=41, W=277, H=140, ridge='h'):
    base = slate_tex(W, H, seed, .3, .05, wrap=False); arr = np.array(base).astype(np.float32); yy, xx = np.mgrid[0:H, 0:W]
    top = yy < H // 2; arr[top, :3] *= 1.22; arr[~top, :3] *= .55
    s = S(W, H); s.setim(Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), 'RGBA'))
    s.r(0, H // 2 - 3, W - 1, H // 2 + 3, '#0a0d10'); s.r(0, H // 2 - 2, W - 1, H // 2 - 2, '#8794a0'); s.r(0, H // 2 - 1, W - 1, H // 2 + 1, '#2e353c')
    for x in range(0, W, 14): s.r(x, H // 2 - 3, x + 1, H // 2 + 3, '#15191d')
    s.d.rectangle([0, 0, W - 1, H - 1], outline=C('#050709')); s.d.rectangle([1, 1, W - 2, H - 2], outline=C('#2e353c')); s.r(0, H - 4, W - 1, H - 1, '#08090a')
    rng = np.random.default_rng(seed)
    for k in range(3):
        x, y = int(rng.integers(20, W - 50)), int(rng.integers(8, H - 30)); s.p([(x, y), (x + 30, y - 2), (x + 26, y + 18), (x + 6, y + 16)], '#030201')
        for j in range(3): s.l([(x + 2, y + 3 + j * 5), (x + 28, y + 2 + j * 5)], '#503523')
    out = finalize(s.im, pad=6, grunge=.2, sd=(10, 12), sa=105)
    return out if ridge == 'h' else rot(out, 90)

def dormer(seed=42):
    W, H = 56, 62; s = S(W, H); s.p([(0, 0), (W - 1, 0), (W - 1, H - 1), (0, H - 1)], '#2e353c'); arr = np.array(slate_tex(W, H, seed, .2, 0, wrap=False)); arr[:H // 2, :, :3] = (arr[:H // 2, :, :3] * 1.2).clip(0, 255); arr[H // 2:, :, :3] = (arr[H // 2:, :, :3] * .55).astype(np.uint8)
    s.setim(Image.fromarray(arr, 'RGBA')); s.r(0, H // 2 - 2, W - 1, H // 2 + 2, '#2e353c'); s.r(0, H // 2 - 2, W - 1, H // 2 - 2, '#98a6b1'); s.bev(18, H - 6, 38, H - 1, '#0a1114', '#22464f', '#050709'); s.l([(22, H - 5), (28, H - 2)], (200, 235, 240, 110))
    return finalize(s.im, pad=5, grunge=.2, sd=(6, 8))

def build(veg, lm, veh, cem, yard, roof):
    for i, sd in enumerate((1, 2, 3)): veg.add(f'tree_elm_dead_{"abc"[i]}', tree_dead(sd, 150 + i * 14, 6 + i))
    veg.add('tree_oak_dark', tree_leafy(4, 158, P['moss'])); veg.add('tree_pine_dark_a', pine(5)); veg.add('tree_pine_dark_b', pine(6, 108)); veg.add('bush_overgrown', bush(False, 1)); veg.add('bush_dead', bush(True, 2)); veg.add('stump', stump()); veg.add('log_fallen', log())
    lm.add('fountain_angel_dry', fountain()); lm.add('flagpole_torn_flag', flagpole()); lm.add('streetlamp', streetlamp()); lm.add('hydrant', hydrant()); lm.add('manhole_closed', manhole(False)); lm.add('manhole_open', manhole(True)); lm.add('tunnel_entrance_stairs', tunnel_entrance())
    for n, im in (('fence_iron_h', fence('iron')), ('fence_iron_broken_h', fence('iron', True)), ('fence_chain_h', fence('chain')), ('fence_chain_torn_h', fence('chain', True))):
        lm.add(n, finalize(im, pad=3, grunge=.25, sd=(3, 5))); lm.add(n.replace('_h', '_v'), finalize(rot(im, 90), pad=3, grunge=.25, sd=(3, 5)))
    veh.add('vehicle_police_car_red', police_car(0)); veh.add('vehicle_police_car_blue', police_car(1)); veh.add('vehicle_police_car_doorclosed', police_car(0, False)); veh.add('vehicle_ambulance_closed', ambulance(False)); veh.add('vehicle_ambulance_rear_open', ambulance(True))
    for i, n in enumerate((7, 13, 21, 34)): cem.add(f'cemetery_marker_{n:02d}', marker(n, i + 1))
    cem.add('cemetery_grave_open', grave_open()); cem.add('cemetery_grave_fresh_mound', grave_mound()); cem.add('cemetery_cross_wood', cross_wood()); cem.add('cemetery_flowers_dead', flowers())
    yard.add('greenhouse_roof_intact', greenhouse(False)); yard.add('greenhouse_roof_broken', greenhouse(True, 15)); yard.add('greenhouse_interior_beds', greenhouse_beds())
    yard.add('scarecrow', scarecrow()); yard.add('crow_a', crow(1, 20)); yard.add('crow_b', crow(2, 200)); yard.add('wheelbarrow', wheelbarrow()); yard.add('coal_pile', coal_pile()); yard.add('chimney_top_round', chimney())
    yard.add('laundry_line_sheets', laundry()); yard.add('camp_tent', tent()); yard.add('camp_fire_dead', campfire()); yard.add('camp_sleeping_bag', sleeping_bag()); yard.add('camp_backpack', backpack()); yard.add('camp_cooler', cooler())
    yard.add('bench_park', bench_park()); yard.add('swing_set_airing_court', swing_set()); yard.add('dumpster', dumpster()); yard.add('crate_wood', crate()); yard.add('barrel_rust', barrel())
    roof.add('roof_slate_a', roof_tile(1)); roof.add('roof_slate_mossy', roof_tile(2, .9)); roof.add('roof_slate_damaged', roof_tile(3, .3, .14)); roof.add('roof_slate_hole', roof_tile(4, .3, .06, True))
    roof.add('roof_tower_pyramid', roof_tower()); roof.add('roof_wing_gable_h', roof_wing()); roof.add('roof_wing_gable_v', roof_wing(43, ridge='v')); roof.add('roof_dormer', dormer())

if __name__ == '__main__':
    sh = [Sheet(n) for n in ('props_vegetation', 'props_landmarks_fences', 'props_vehicles', 'props_cemetery', 'props_yard_camp', 'props_roofs')]
    build(*sh)
    for x in sh: x.save()
