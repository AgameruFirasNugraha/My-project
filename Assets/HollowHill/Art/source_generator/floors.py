from px import *

def mk(): return S(T, T, wrap=True)

# ------------------------------------------------------------------ interior
def plank(L, h, seed, tone):
    g = vnoise(L, h, max(1, L // 20), h // 2 + 1, seed); f = vnoise(L, h, max(1, L // 5), h, seed + 1)
    n = np.clip(0.08 + 0.55 * tone + 0.30 * g + 0.12 * f, 0, .999)
    a = np.array(quant(n, P['wood'], 0.12))
    a[0, :] = C('#150e0a'); a[:, 0] = C('#150e0a')
    a[1, 1:, :3] = np.minimum(255, a[1, 1:, :3] * 1.18).astype(np.uint8)
    a[-1, 1:, :3] = (a[-1, 1:, :3] * .72).astype(np.uint8)
    for yy in (3, h - 4):
        a[yy, 3] = C('#0f0b09'); a[yy, 4] = C('#6b6258')
    return Image.fromarray(a, 'RGBA')

def f_wood(seed, holes=0, stains=0.0):
    rng = np.random.default_rng(seed); s = mk()
    for r_ in range(7):
        row = Image.new('RGBA', (T, 13)); x = 0
        while x < T:
            L = int(rng.integers(28, 56))
            if T - x - L < 20: L = T - x
            L = min(L, T - x)
            row.paste(plank(L, 13, int(rng.integers(1 << 30)), rng.random()), (x, 0)); x += L
        s.im.paste(Image.fromarray(np.roll(np.array(row), int(rng.integers(0, T)), axis=1)), (0, r_ * 13))
    s.setim(s.im)
    for i in range(holes):
        rr = int(rng.integers(0, 7)); x0 = int(rng.integers(0, T)); L = int(rng.integers(16, 34))
        sub = tex(L, 11, RP('#090605', '#110c09', '#1b130e', '#271b13'), seed + i, scale=2, dither=.3)
        for ox in (x0, x0 - T): s.im.paste(sub, (ox, rr * 13 + 1))
        for k in range(5):
            xx = x0 + int(rng.integers(0, L)); s.pt(xx % T, rr * 13 + 1 + (0 if k % 2 else 10), '#8a6340')
    if stains:
        s.stain(seed + 3, (9, 7, 6), thr=.52, gain=5, maxa=.82 * stains, scale=1.3)
        s.stain(seed + 4, (62, 76, 54), thr=.7, gain=8, maxa=.5 * stains, scale=2.4)
    s.speck(seed + 5, .012, ['#140d09', '#7d5c3c'])
    s.crack(seed + 6, int(rng.integers(0, T)), int(rng.integers(0, T)), 22, dark=(12, 8, 6))
    return s.im

def f_lino(seed, wear=.4, peel=0.0):
    rng = np.random.default_rng(seed); s = mk()
    for i in range(7):
        for j in range(7):
            rp = P['lino'] if (i + j) % 2 == 0 else P['lino2']
            s.im.paste(tex(13, 13, rp, int(rng.integers(1 << 30)), scale=.4, dither=.14, gain=.8, bias=rng.uniform(-.12, .12)), (i * 13, j * 13))
    s.setim(s.im)
    for k in range(7): s.r(k * 13, 0, k * 13, T - 1, (0, 0, 0, 55)); s.r(0, k * 13, T - 1, k * 13, (0, 0, 0, 55))
    if peel:
        n = fbm(T, T, seed + 11, 1.1); m = n > 1 - peel
        conc = np.array(tex(T, T, P['concrete'], seed + 12, 1.3, .12)); arr = np.array(s.im)
        edge = m & ~ero(m, 1, False)
        arr[m] = conc[m]; arr[edge] = C('#6c6853'); s.setim(Image.fromarray(arr, 'RGBA'))
        s.im = s.im; s.d = ImageDraw.Draw(s.im, 'RGBA')
    for _ in range(int(26 * wear)):
        x, y = rng.integers(0, T, 2); L = int(rng.integers(5, 14)); a_ = rng.normal(.3, .35)
        s.l([(x, y), (x + L * math.cos(a_), y + L * math.sin(a_))], (190, 190, 150, 55))
    for _ in range(int(9 * wear)):
        x, y = rng.integers(0, T, 2); s.l([(x, y), (x + 5, y + 2), (x + 9, y + 1)], (8, 8, 6, 130))
    s.stain(seed + 2, (20, 15, 8), thr=.6, gain=5, maxa=.7 * wear, scale=1.4)
    s.stain(seed + 3, (105, 92, 40), thr=.74, gain=8, maxa=.4 * wear, scale=2)
    s.crack(seed + 4, int(rng.integers(0, T)), int(rng.integers(0, T)), 18)
    return s.im

def voronoi(seed, pts, jitter=.3):
    rng = np.random.default_rng(seed); cs = []
    gx, gy = pts
    for i in range(gx):
        for j in range(gy):
            cs.append(((i + .5 + rng.uniform(-jitter, jitter)) * T / gx, (j + .5 + rng.uniform(-jitter, jitter)) * T / gy, rng.random()))
    return cs

def vor_maps(cs, xs=1.0):
    yy, xx = np.mgrid[0:T, 0:T]; d = []
    for cx, cy, _ in cs:
        dx = np.abs(xx - cx); dx = np.minimum(dx, T - dx); dy = np.abs(yy - cy); dy = np.minimum(dy, T - dy)
        d.append(np.sqrt((dx * xs) ** 2 + dy ** 2))
    d = np.stack(d); idx = d.argmin(0); srt = np.sort(d, 0)
    return idx, srt[1] - srt[0], xx, yy

def f_hex(seed, dmg=.25):
    rng = np.random.default_rng(seed); cs = []
    for r_ in range(8):
        for c_ in range(7): cs.append(((c_ + .5 * (r_ % 2)) * 13 + 3, (r_ + .5) * T / 8, rng.random()))
    idx, edge, xx, yy = vor_maps(cs)
    tone = np.array([c[2] for c in cs])[idx]
    cxs = np.array([c[0] for c in cs])[idx]; cys = np.array([c[1] for c in cs])[idx]
    ddx = np.where(np.abs(xx - cxs) > T / 2, (xx - cxs) - np.sign(xx - cxs) * T, xx - cxs); ddy = np.where(np.abs(yy - cys) > T / 2, (yy - cys) - np.sign(yy - cys) * T, yy - cys)
    n = .5 + .28 * tone + .18 * (fbm(T, T, seed + 3, 3) - .5) - .014 * (ddx + ddy)
    arr = np.array(quant(np.clip(n, 0, .99), P['tilew'], .1))
    arr[edge < 1.7] = C('#1f2423'); arr[(edge >= 1.7) & (edge < 2.6) & (ddx + ddy > 0)] = (arr[(edge >= 1.7) & (edge < 2.6) & (ddx + ddy > 0)] * .8).astype(np.uint8)
    for k, cell in enumerate(cs):
        if rng.random() < dmg * .12: arr[idx == k] = C('#0e1111'); arr[(idx == k) & (edge < 2.4)] = C('#222726')
    s = mk(); s.setim(Image.fromarray(arr, 'RGBA'))
    s.stain(seed + 4, (14, 10, 6), thr=.55, gain=5, maxa=.75 * dmg * 2, scale=1.5)
    s.stain(seed + 5, (72, 40, 24), thr=.72, gain=8, maxa=.5 * dmg * 2, scale=2.2)
    for _ in range(int(5 * dmg * 4)): s.crack(int(rng.integers(1 << 30)), int(rng.integers(0, T)), int(rng.integers(0, T)), 12)
    return s.im

def f_conc(seed, wet=.4):
    s = mk(); s.setim(tex(T, T, P['concrete'], seed, 1.2, .1, 1.2))
    for p_ in (22, 68):
        s.r(0, p_, T - 1, p_, (6, 7, 8, 200)); s.r(0, p_ + 1, T - 1, p_ + 1, (120, 128, 134, 55)); s.r(p_, 0, p_, T - 1, (6, 7, 8, 200)); s.r(p_ + 1, 0, p_ + 1, T - 1, (120, 128, 134, 55))
    rng = np.random.default_rng(seed)
    for _ in range(5):
        x = int(rng.integers(0, T)); y = int(rng.integers(0, T)); s.l([(x, y), (x + int(rng.integers(-2, 3)), y + int(rng.integers(10, 30)))], (115, 62, 28, 90))
    n = fbm(T, T, seed + 9, 1.0); m = n > 1 - wet * .45
    w_ = np.array(tex(T, T, P['water'], seed + 10, 2, .15, 1.4)); arr = np.array(s.im)
    edge = m & ~ero(m, 1, False); arr[m] = w_[m]; arr[edge] = (6, 9, 11, 255)
    s.setim(Image.fromarray(arr, 'RGBA'))
    for _ in range(int(44 * wet)):
        x, y = int(rng.integers(0, T)), int(rng.integers(0, T))
        if m[y, x]: s.l([(x, y), (x + int(rng.integers(3, 9)), y)], (150, 190, 200, 70))
    s.crack(seed + 12, int(rng.integers(0, T)), int(rng.integers(0, T)), 26)
    s.speck(seed + 13, .01, ['#0e1012', '#8a9096'])
    return s.im

def f_flag(seed, moss=.3):
    cs = voronoi(seed, (3, 3), .28); idx, edge, xx, yy = vor_maps(cs)
    tone = np.array([c[2] for c in cs])[idx]
    n = .22 + .38 * tone + .28 * (fbm(T, T, seed + 3, 2.2) - .5)
    arr = np.array(quant(np.clip(n, 0, .99), P['stone'], .12))
    arr[(edge >= 1.3) & (edge < 3.2)] = (arr[(edge >= 1.3) & (edge < 3.2)] * .78).astype(np.uint8)
    arr[edge < 1.3] = C('#0c0d0c')
    mm = (fbm(T, T, seed + 8, 2.6) > 1 - moss * .5) & (edge < 3.6)
    arr[mm] = np.array(quant(np.clip(.35 + .5 * fbm(T, T, seed + 9, 4), 0, .99), P['moss'], .2))[mm]
    s = mk(); s.setim(Image.fromarray(arr, 'RGBA'))
    s.crack(seed + 5, 20, 40, 24); s.crack(seed + 6, 70, 20, 18); s.speck(seed + 7, .012, ['#101110', '#8a8f8c'])
    s.stain(seed + 8, (10, 8, 8), thr=.6, gain=5, maxa=.6, scale=1.4)
    return s.im

def f_morgue(seed, drain=False, dirt=.4):
    rng = np.random.default_rng(seed); s = mk()
    for i in range(7):
        for j in range(7):
            s.im.paste(tex(13, 13, P['tilec'], int(rng.integers(1 << 30)), .4, .12, .8, rng.uniform(-.1, .12)), (i * 13, j * 13))
    s.setim(s.im)
    for k in range(7):
        s.r(k * 13, 0, k * 13, T - 1, (14, 18, 19, 255)); s.r(0, k * 13, T - 1, k * 13, (14, 18, 19, 255))
        s.r(k * 13 + 1, 0, k * 13 + 1, T - 1, (190, 215, 220, 28)); s.r(0, k * 13 + 1, T - 1, k * 13 + 1, (190, 215, 220, 28))
    if drain:
        yy, xx = np.mgrid[0:T, 0:T]; d = np.sqrt((xx - 45) ** 2 + (yy - 45) ** 2); arr = np.array(s.im).astype(np.float32)
        arr[..., :3] *= np.clip(0.55 + d / 50, 0, 1)[..., None]; s.setim(Image.fromarray(arr.astype(np.uint8), 'RGBA'))
        s.circ(45, 45, 12, '#0d1112'); s.circ(45, 45, 10, '#58646b'); s.circ(45, 45, 9, '#2c353a')
        for k in range(-6, 7, 3): s.r(45 + k, 38, 45 + k, 52, '#0a0d0f'); s.pt(45 + k + 1, 39, '#8a99a1')
        s.l([(34, 45), (56, 45)], '#0a0d0f'); s.circ(45, 45, 2, '#9aa8b0')
    s.stain(seed + 2, (28, 10, 8), thr=.62, gain=5, maxa=.7 * dirt, scale=1.5)
    s.stain(seed + 3, (12, 14, 14), thr=.5, gain=4, maxa=.6 * dirt, scale=1)
    s.crack(seed + 4, 15, 60, 14); s.crack(seed + 5, 70, 20, 10)
    return s.im

def f_padded(seed, dirt=.5):
    s = mk(); yy, xx = np.mgrid[0:T, 0:T]
    u = (xx + yy) % 13; v = (xx - yy) % 13
    du = np.minimum(u, 13 - u); dv = np.minimum(v, 13 - v); m = np.minimum(du, dv)
    n = .42 + .18 * (fbm(T, T, seed, 3) - .5) + np.clip(m, 0, 5) * .035
    arr = np.array(quant(np.clip(n, 0, .99), P['paper'], .14))
    arr[m < 1] = C('#35322a'); arr[(m >= 1) & (m < 2)] = (arr[(m >= 1) & (m < 2)] * .82).astype(np.uint8)
    btn = (du < 2) & (dv < 2) & (np.minimum(du, dv) < 1.2)
    s.setim(Image.fromarray(arr, 'RGBA'))
    s.stain(seed + 1, (60, 44, 20), thr=.58, gain=5, maxa=.7 * dirt, scale=1.5)
    s.stain(seed + 2, (70, 18, 14), thr=.76, gain=9, maxa=.55 * dirt, scale=2.6)
    s.stain(seed + 3, (12, 10, 8), thr=.6, gain=6, maxa=.5, scale=1.2)
    s.crack(seed + 4, 30, 30, 14, dark=(18, 14, 10)); s.crack(seed + 5, 60, 70, 12, dark=(18, 14, 10))
    return s.im

def f_carpet(seed, wear=.5):
    s = mk(); yy, xx = np.mgrid[0:T, 0:T]
    rng = np.random.default_rng(seed)
    n = .45 + .2 * (fbm(T, T, seed, 4) - .5) + (rng.random((T, T)) - .5) * .22
    u = (xx + yy) % 26; v = (xx - yy) % 26
    pat = (np.minimum(u, 26 - u) < 1.5) | (np.minimum(v, 26 - v) < 1.5)
    n = n + pat * .13
    lane = np.exp(-((np.minimum(np.abs(xx - 45), T - np.abs(xx - 45))) / 11.0) ** 2) * wear * .3
    n = n + lane * (fbm(T, T, seed + 3, 5) * .8 + .2)
    s.setim(quant(np.clip(n, 0, .99), P['carpet'], .1))
    s.stain(seed + 4, (6, 6, 6), thr=.6, gain=5, maxa=.7, scale=1.4); s.stain(seed + 5, (12, 40, 40), thr=.8, gain=10, maxa=.4, scale=2.4)
    return s.im

def f_quarry(seed, grease=.5):
    rng = np.random.default_rng(seed); s = mk()
    for i in range(7):
        for j in range(7):
            s.im.paste(tex(13, 13, P['terra'], int(rng.integers(1 << 30)), .4, .14, .9, rng.uniform(-.12, .14)), (i * 13, j * 13))
    s.setim(s.im)
    for k in range(7): s.r(k * 13, 0, k * 13, T - 1, (14, 11, 9, 255)); s.r(0, k * 13, T - 1, k * 13, (14, 11, 9, 255))
    s.stain(seed + 2, (8, 6, 4), thr=.55, gain=5, maxa=.75 * grease, scale=1.5)
    s.stain(seed + 3, (96, 84, 30), thr=.78, gain=9, maxa=.45 * grease, scale=2.2)
    s.crack(seed + 4, 20, 70, 14); s.speck(seed + 5, .012, ['#120d0a', '#9a6a4c'])
    return s.im

# ------------------------------------------------------------------ exterior
def blades(s, seed, n, rp, L=(3, 6), spread=.45):
    rng = np.random.default_rng(seed)
    for _ in range(n):
        x, y = rng.random() * T, rng.random() * T; ln = rng.uniform(*L); a = rng.normal(0, spread)
        k = int(rng.integers(1, len(rp) - 1)); tip = rp[min(len(rp) - 1, k + 1 + int(rng.integers(0, 2)))]
        s.l([(x, y), (x + math.sin(a) * ln, y - math.cos(a) * ln)], rp[k]); s.pt(int(x + math.sin(a) * ln), int(y - math.cos(a) * ln), tip)

def f_grass(seed, dead=False, patches=0.0, leaves=0.0):
    rp = P['dgrass'] if dead else P['grass']; s = mk()
    s.setim(tex(T, T, rp, seed, 1.6, .16, 1.3, -.1))
    if patches:
        n = fbm(T, T, seed + 2, 1.4); m = n > 1 - patches * .5
        d = np.array(tex(T, T, P['dirt'], seed + 3, 2, .15)); arr = np.array(s.im); arr[m] = d[m]; s.setim(Image.fromarray(arr, 'RGBA'))
    blades(s, seed + 4, 520, rp)
    rng = np.random.default_rng(seed + 9)
    for _ in range(int(60 * (1 if dead else .4))): s.l([(float(rng.integers(0, T)), float(rng.integers(0, T)))] * 2, rp[0])
    if leaves:
        for _ in range(int(40 * leaves)):
            x, y = rng.random() * T, rng.random() * T; a = rng.uniform(0, 6.28); c = ['#4a2f14', '#6b4218', '#3b2610', '#55361a', '#2f2b12'][int(rng.integers(0, 5))]
            s.p([(x + math.cos(a) * 3, y + math.sin(a) * 3), (x + math.cos(a + 1.6), y + math.sin(a + 1.6)), (x - math.cos(a) * 3, y - math.sin(a) * 3), (x + math.cos(a - 1.6), y + math.sin(a - 1.6))], c)
    return s.im

def f_dirt(seed, path=False):
    s = mk(); s.setim(tex(T, T, P['dirt'], seed, 1.8, .14, 1.3))
    rng = np.random.default_rng(seed)
    if path:
        yy, xx = np.mgrid[0:T, 0:T]; arr = np.array(s.im).astype(np.float32)
        lane = np.exp(-((np.minimum(np.abs(xx - 45), T - np.abs(xx - 45))) / 14.) ** 2)
        arr[..., :3] *= (0.78 + .55 * lane)[..., None] * 1.0; arr = np.clip(arr, 0, 255)
        for rx in (30, 60): arr[:, rx:rx + 3, :3] *= .55
        s.setim(Image.fromarray(arr.astype(np.uint8), 'RGBA'))
    for _ in range(46):
        x, y = rng.integers(0, T, 2); w_ = int(rng.integers(2, 4)); s.e(x, y, x + w_, y + w_ - 1, '#6a5238'); s.pt(x + w_, y + w_ - 1, '#120d09')
    s.crack(seed + 2, 10, 20, 20, dark=(8, 6, 4)); s.speck(seed + 3, .02, ['#0f0b08', '#7c6040'])
    return s.im

def f_gravel(seed):
    s = mk(); s.setim(tex(T, T, P['concrete'][:3], seed, 2, .15, 1.0, -.1)); rng = np.random.default_rng(seed)
    for _ in range(420):
        x, y = int(rng.integers(0, T)), int(rng.integers(0, T)); w_ = int(rng.integers(2, 5)); c = P['concrete'][int(rng.integers(2, 6))]
        s.e(x, y, x + w_, y + w_ - 1, c); s.pt(x, y, shd(c, 1.5)); s.pt(x + w_, y + w_ - 1, '#0c0d0f')
    return s.im

def f_asphalt(seed, line=False, cracks=3):
    rp = RP('#0c0d0f', '#15171a', '#1e2125', '#292d32', '#363b41'); s = mk(); s.setim(tex(T, T, rp, seed, 2, .15, 1.2))
    rng = np.random.default_rng(seed); s.speck(seed + 1, .06, ['#464c53', '#0a0b0d', '#5a6068'])
    s.r(10, 50, 40, 70, (0, 0, 0, 38)); s.stain(seed + 2, (3, 3, 4), thr=.6, gain=5, maxa=.7, scale=1.2)
    for k in range(cracks): s.crack(seed + 5 + k, int(rng.integers(0, T)), int(rng.integers(0, T)), 34, dark=(3, 3, 4), light=(110, 112, 116))
    if line:
        for y0 in range(4, T, 46):
            for yy in range(y0, min(y0 + 30, T)):
                for xx in (43, 44, 45, 46, 47):
                    if rng.random() > .18: s.pt(xx, yy, '#9a8431' if rng.random() > .3 else '#6c5c20')
    return s.im

def f_pavers(seed, moss=.3):
    rng = np.random.default_rng(seed); s = mk()
    for j in range(7):
        off = (j % 2) * 6
        for i in range(7):
            s.im.paste(tex(13, 13, P['stone'], int(rng.integers(1 << 30)), .5, .12, .45, rng.uniform(-.08, .1)), ((i * 13 + off) % T, j * 13))
            if (i * 13 + off) % T + 13 > T: s.im.paste(tex(13, 13, P['stone'], int(rng.integers(1 << 30)), .5, .12, .45, .0), ((i * 13 + off) % T - T, j * 13))
    s.setim(s.im)
    for j in range(7):
        s.r(0, j * 13, T - 1, j * 13, '#0b0c0b')
        for i in range(8): s.r((i * 13 + (j % 2) * 6) % T, j * 13, (i * 13 + (j % 2) * 6) % T, j * 13 + 12, '#0b0c0b')
    mm = (fbm(T, T, seed + 3, 3) > 1 - moss * .45); arr = np.array(s.im)
    g = np.all(arr[..., :3] < 20, axis=2); sel = g & mm
    arr[sel] = np.array(quant(np.clip(.4 + .5 * fbm(T, T, seed + 4, 5), 0, .99), P['moss'], .2))[sel]
    s.setim(Image.fromarray(arr, 'RGBA')); s.crack(seed + 5, 30, 30, 14); s.stain(seed + 6, (8, 8, 8), thr=.6, gain=5, maxa=.5, scale=1.4)
    return s.im

def f_leaves(seed):
    s = mk(); s.setim(tex(T, T, P['dirt'], seed, 2, .14, 1.2, -.12)); rng = np.random.default_rng(seed)
    for _ in range(130):
        x, y = rng.random() * T, rng.random() * T; a = rng.uniform(0, 6.28); c = ['#4a2f14', '#6b4218', '#3b2610', '#55361a', '#2f2b12', '#7a5420'][int(rng.integers(0, 6))]
        s.p([(x + math.cos(a) * 3.5, y + math.sin(a) * 3.5), (x + math.cos(a + 1.6) * 1.6, y + math.sin(a + 1.6) * 1.6), (x - math.cos(a) * 3.5, y - math.sin(a) * 3.5), (x + math.cos(a - 1.6) * 1.6, y + math.sin(a - 1.6) * 1.6)], c)
        s.pt(int(x), int(y), shd(C(c), .6))
    return s.im

def f_furrows(seed):
    yy, xx = np.mgrid[0:T, 0:T]
    n = .5 + .5 * np.sin(2 * math.pi * yy / 13.0) * .5 + .28 * (fbm(T, T, seed, 3) - .5)
    s = mk(); s.setim(quant(np.clip(n * .9, 0, .99), P['dirt'], .14)); rng = np.random.default_rng(seed)
    for _ in range(26):
        x, y = int(rng.integers(0, T)), int(rng.integers(0, T)); s.l([(x, y), (x + int(rng.integers(-2, 3)), y - int(rng.integers(3, 8)))], '#5a5030')
    s.speck(seed + 2, .02, ['#0f0b08', '#6a5238'])
    return s.im

def f_water(seed):
    s = mk(); s.setim(tex(T, T, P['water'], seed, 2.5, .16, 1.2)); rng = np.random.default_rng(seed)
    for _ in range(60):
        x, y = int(rng.integers(0, T)), int(rng.integers(0, T)); s.l([(x, y), (x + int(rng.integers(3, 10)), y)], (130, 170, 180, 60))
    for _ in range(7):
        x, y = rng.integers(0, T, 2); s.e(x, y, x + 3, y + 2, '#3b2610')
    return s.im

def f_mud(seed):
    s = mk(); s.setim(tex(T, T, P['dirt'][:4], seed, 2, .12, 1.4, -.1)); rng = np.random.default_rng(seed)
    for _ in range(9):
        x, y = int(rng.integers(0, T)), int(rng.integers(0, T)); s.e(x, y, x + 12, y + 4, (8, 9, 10, 255)); s.l([(x + 2, y + 1), (x + 7, y + 1)], (140, 160, 168, 90))
    for k in range(5):
        x, y = 15 + k * 14, 10 + k * 15; s.e(x, y, x + 5, y + 8, '#0f0b08'); s.e(x + 6, y + 10, x + 11, y + 18, '#0f0b08')
    return s.im

def build():
    sh = Sheet('tiles_floor_interior')
    sh.add('floor_parquet_a', f_wood(1)); sh.add('floor_parquet_b', f_wood(2, 1, .3)); sh.add('floor_parquet_rotted', f_wood(3, 3, .9)); sh.add('floor_parquet_collapsed', f_wood(4, 5, 1.0))
    sh.add('floor_lino_a', f_lino(11, .3)); sh.add('floor_lino_b', f_lino(12, .6, .1)); sh.add('floor_lino_worn', f_lino(13, 1.0, .3)); sh.add('floor_lino_peeled', f_lino(14, .8, .55))
    sh.add('floor_hex_a', f_hex(21, .1)); sh.add('floor_hex_b', f_hex(22, .3)); sh.add('floor_hex_ruined', f_hex(23, .7))
    sh.add('floor_conc_a', f_conc(31, .2)); sh.add('floor_conc_wet', f_conc(32, .7)); sh.add('floor_conc_flooded', f_conc(33, 1.0))
    sh.add('floor_flag_a', f_flag(41, .15)); sh.add('floor_flag_mossy', f_flag(42, .8))
    sh.add('floor_morgue_a', f_morgue(51, False, .3)); sh.add('floor_morgue_b', f_morgue(52, False, .8)); sh.add('floor_morgue_drain', f_morgue(53, True, .7))
    sh.add('floor_padded_a', f_padded(61, .3)); sh.add('floor_padded_stained', f_padded(62, 1.0))
    sh.add('floor_carpet_a', f_carpet(71, .3)); sh.add('floor_carpet_worn', f_carpet(72, 1.0))
    sh.add('floor_quarry_a', f_quarry(81, .3)); sh.add('floor_quarry_greasy', f_quarry(82, 1.0))
    sh.save(cols=8)
    ex = Sheet('tiles_floor_exterior')
    for i, (n, im) in enumerate([('grass_a', f_grass(101)), ('grass_b', f_grass(102)), ('grass_c', f_grass(103, patches=.4)), ('grass_dead_a', f_grass(104, True)), ('grass_dead_b', f_grass(105, True, .3)),
                                 ('grass_leaves', f_grass(106, False, .0, 1.0)), ('cemetery_grass', f_grass(107, True, .3, .6)),
                                 ('dirt_a', f_dirt(111)), ('dirt_b', f_dirt(112)), ('dirt_path_v', f_dirt(113, True)), ('mud', f_mud(114)), ('leaves', f_leaves(115)), ('furrows', f_furrows(116)),
                                 ('gravel', f_gravel(121)), ('asphalt_a', f_asphalt(131)), ('asphalt_b', f_asphalt(132, cracks=6)), ('asphalt_line_v', f_asphalt(133, True, 2)),
                                 ('pavers_a', f_pavers(141, .15)), ('pavers_mossy', f_pavers(142, .9)), ('water_dark', f_water(151))]):
        ex.add('floor_' + n, im)
    ex.save(cols=8)

if __name__ == '__main__':
    build()
