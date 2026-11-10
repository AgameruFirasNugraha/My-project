from px import *

A, B = 22, 68   # wall bar 47 px thick (~0.78 m), centred in tile

def cap_tex(style, seed=5):
    if style == 'plaster':
        s = S(T, T, wrap=True); s.setim(tex(T, T, P['plaster'], seed, 1.6, .12, 1.0, -.02))
        s.speck(seed + 1, .02, ['#262822', '#a4a68c']); s.stain(seed + 2, (14, 12, 8), thr=.62, gain=5, maxa=.55, scale=1.4)
        s.stain(seed + 3, (70, 90, 60), thr=.78, gain=9, maxa=.35, scale=2.4); return s.im
    if style == 'brick':
        s = S(T, T, wrap=True); rng = np.random.default_rng(seed)
        for j in range(13):
            off = (j % 2) * 6
            for i in range(7):
                s.im.paste(tex(13, 7, P['brick'], int(rng.integers(1 << 30)), .5, .16, .45, rng.uniform(-.1, .12)), ((i * 13 + off) % T, j * 7))
                if (i * 13 + off) % T + 13 > T: s.im.paste(tex(13, 7, P['brick'], int(rng.integers(1 << 30)), .5, .16, .45, 0), ((i * 13 + off) % T - T, j * 7))
        s.setim(s.im)
        for j in range(13):
            s.r(0, j * 7, T - 1, j * 7, '#1d1311')
            for i in range(8): s.r((i * 13 + (j % 2) * 6) % T, j * 7, (i * 13 + (j % 2) * 6) % T, j * 7 + 6, '#1d1311')
        s.stain(seed + 2, (10, 8, 6), thr=.58, gain=5, maxa=.6, scale=1.4); s.stain(seed + 3, (60, 90, 55), thr=.8, gain=9, maxa=.4, scale=2.5); return s.im
    s = S(T, T, wrap=True); s.setim(tex(T, T, P['concrete'], seed, 1.5, .12, 1.1))
    for y in range(6, T, 13): s.r(0, y, T - 1, y, (8, 9, 10, 70)); s.r(0, y + 1, T - 1, y + 1, (150, 158, 164, 22))
    for x in range(10, T, 26):
        for y in range(10, T, 26): s.circ(x, y, 1, '#0c0d0e')
    s.stain(seed + 2, (8, 8, 8), thr=.6, gain=5, maxa=.6, scale=1.4); s.stain(seed + 3, (100, 56, 26), thr=.8, gain=9, maxa=.4, scale=2.2)
    s.speck(seed + 4, .015, ['#0e1012', '#8a9096']); return s.im

def wmask(m, x0=0, x1=T):
    a = np.zeros((T, x1 - x0), bool)
    a[A:B + 1, :] = True
    return a

def wall_mask(m):
    a = np.zeros((T, T), bool); a[A:B + 1, A:B + 1] = True
    if m & 1: a[0:A, A:B + 1] = True
    if m & 2: a[A:B + 1, B + 1:] = True
    if m & 4: a[B + 1:, A:B + 1] = True
    if m & 8: a[A:B + 1, 0:A] = True
    return a

CAPS = {}
def cap(style):
    if style not in CAPS: CAPS[style] = cap_tex(style)
    return CAPS[style]

def shade_cap(arr, a, style):
    inner = ero(a, 3); band = a & ~inner
    f = np.where(band, 0.78, 1.0)[..., None]
    arr[..., :3] = (arr[..., :3] * f).astype(np.uint8)
    lift = inner & ero(a, 5)
    arr[lift, :3] = np.minimum(255, arr[lift, :3] * 1.07).astype(np.uint8)
    return arr

def wall_raw(m, style, seed=1, dmg=0, tile=None):
    a = wall_mask(m) if tile is None else tile
    arr = np.array(cap(style).copy() if tile is None else cap_wide(style, a.shape[1]))
    arr[..., 3] = np.where(a, 255, 0)
    arr = shade_cap(arr, a, style)
    im = Image.fromarray(arr, 'RGBA'); s = S(im.width, im.height); s.setim(im)
    rng = np.random.default_rng(seed)
    if dmg:
        under = 'brick' if style != 'brick' else 'concrete'; brk = np.array(cap(under)); 
        n = fbm(im.width, im.height, seed + 3, 2.2); mm = (n > 1 - .16 * dmg) & a
        arr2 = np.array(s.im); arr2[mm] = brk[:im.height, :im.width][mm] if im.width <= T else arr2[mm]
        ed = mm & ~ero(mm, 1, False); arr2[ed] = (200, 196, 170, 255); s.setim(Image.fromarray(arr2, 'RGBA'))
        for k in range(dmg): s.crack(seed + 10 + k, rng.integers(A, B), rng.integers(A, B), 22, dark=(10, 8, 6))
        s.stain(seed + 5, (8, 8, 6), thr=.6, gain=6, maxa=.55, scale=1.5)
    return s.im

def cap_wide(style, w):
    c = cap(style); out = Image.new('RGBA', (w, T))
    for x in range(0, w, T): out.paste(c, (x, 0))
    return out

def bake_wall(im, grunge=.12, seed=1):
    return finalize(im, pad=0, edge=True, grunge=grunge, seed=seed, sd=(4, 5), sa=120)

def build_walls(sh):
    styles = [('plaster', 'wall_int'), ('brick', 'wall_ext'), ('concrete', 'wall_tunnel')]
    for style, pre in styles:
        for m in range(16): sh.add(f'{pre}_{m:02d}', bake_wall(wall_raw(m, style, seed=m + 1)), mask=m)
        for v in range(3):
            sh.add(f'{pre}_h_dmg{v}', bake_wall(wall_raw(10, style, seed=40 + v, dmg=v + 1), seed=v), mask=10)
            sh.add(f'{pre}_v_dmg{v}', bake_wall(wall_raw(5, style, seed=50 + v, dmg=v + 1), seed=v), mask=5)

# ------------------------------------------------------------------ doors / windows
def door_tex(w, h, seed, kind='wood'):
    if kind == 'wood':
        t = S(w, h); t.setim(tex(w, h, P['wood'], seed, 1.0, .12, 1.3))
        for x in range(8, w, 9): t.r(x, 0, x, h - 1, '#150e0a')
        return t.im
    t = S(w, h); t.setim(tex(w, h, P['pgreen'], seed, 1.4, .14, 1.1)); return t.im

def wood_door_closed(seed=3, style='plaster', boarded=False):
    s = S(T, T); s.setim(wall_raw(10, style, seed)); arr = np.array(s.im)
    arr[A:B + 1, 15:76] = (0, 0, 0, 0); s.setim(Image.fromarray(arr, 'RGBA'))
    s.bev(15, A, 20, B, '#3b271a'); s.bev(71, A, 76, B, '#3b271a')
    s.paste(door_tex(50, 33, seed), 21, 29); s.r(21, 29, 70, 29, '#150e0a'); s.r(21, 61, 70, 61, '#150e0a'); s.r(21, 30, 70, 30, '#8a6340')
    s.r(24, 34, 67, 56, (0, 0, 0, 55)); s.r(24, 34, 67, 34, (160, 120, 80, 70)); s.r(24, 34, 24, 56, (160, 120, 80, 70))
    for y in (33, 57): s.r(21, y, 25, y + 3, '#23282d'); s.pt(22, y, '#6b7782')
    s.circ(64, 46, 2, '#a67c28'); s.pt(63, 45, '#e8c864'); s.circ(64, 46, 3, (0, 0, 0, 0))
    s.stain(seed + 1, (10, 8, 6), thr=.55, gain=5, maxa=.7, scale=1.4)
    if boarded:
        for k, (y, ang) in enumerate([(33, -2), (44, 1), (55, -1)]):
            s.p([(14, y), (77, y + ang), (77, y + ang + 7), (14, y + 7)], '#4a3523'); s.r(14, y, 77, y, '#7a5a3a'); s.r(14, y + 7, 77, y + 7, '#140d09')
            for xx in (20, 48, 72): s.circ(xx, y + 3, 1, '#9aa0a5')
        s.text(26, 38, 'KEEP OUT', '#6b1014', 7, 1, seed)
    return s.im

def wood_door_open(seed=3, style='plaster'):
    H = T + 46; s = S(T, H); s.setim(Image.new('RGBA', (T, H), (0, 0, 0, 0))); s.paste(wall_raw(10, style, seed), 0, 0)
    arr = np.array(s.im); arr[A:B + 1, 15:76] = (0, 0, 0, 0); s.setim(Image.fromarray(arr, 'RGBA'))
    s.bev(15, A, 20, B, '#3b271a'); s.bev(71, A, 76, B, '#3b271a')
    s.r(21, 40, 70, 40, '#2c2f31'); s.r(21, 41, 70, 41, '#767d83'); s.r(21, 55, 70, 55, '#2c2f31')   # threshold plate
    L = Image.new('RGBA', (60, 8), (0, 0, 0, 0)); ls = S(60, 8); ls.setim(door_tex(60, 8, seed)); ls.r(0, 0, 59, 0, '#8a6340'); ls.r(0, 7, 59, 7, '#150e0a'); ls.r(55, 3, 57, 4, '#a67c28')
    lf = ls.im.rotate(-80, expand=True, resample=Image.NEAREST); s.paste(lf, 12, 64)
    return s.im

def door_broken(seed=7, style='plaster'):
    H = T + 40; s = S(T, H); s.paste(wall_raw(10, style, seed), 0, 0)
    arr = np.array(s.im); arr[A:B + 1, 15:76] = (0, 0, 0, 0); s.setim(Image.fromarray(arr, 'RGBA'))
    s.bev(15, A, 20, B, '#3b271a'); s.r(71, A, 76, A + 14, '#3b271a'); s.p([(71, A + 14), (76, A + 14), (74, A + 20), (71, A + 18)], '#3b271a')
    t = door_tex(40, 52, seed); m = Image.new('L', (40, 52), 0); ImageDraw.Draw(m).polygon([(0, 0), (40, 0), (36, 18), (40, 30), (31, 52), (6, 52), (0, 38), (5, 20)], fill=255)
    d = Image.new('RGBA', (40, 52), (0, 0, 0, 0)); d.paste(t, (0, 0), m); d = d.rotate(-62, expand=True, resample=Image.NEAREST); s.paste(d, 10, 56)
    for i in range(6): s.l([(14 + i * 7, 62), (11 + i * 9, 72)], '#8a6340')
    s.speck(seed, .03, ['#150e0a', '#8a6340']); return s.im

def steel_door(seed=4, state='closed', style='plaster', peep=True):
    H = T + (46 if state == 'open' else 0); s = S(T, H); s.paste(wall_raw(10, style, seed), 0, 0)
    arr = np.array(s.im); arr[A:B + 1, 15:76] = (0, 0, 0, 0); s.setim(Image.fromarray(arr, 'RGBA'))
    s.bev(15, A, 20, B, '#444d56'); s.bev(71, A, 76, B, '#444d56')
    if state == 'closed':
        d = S(50, 33); d.setim(tex(50, 33, P['pgreen'], seed, 1.4, .14, 1.1)); d.r(0, 0, 49, 0, '#7f957f'); d.r(0, 32, 49, 32, '#101914')
        d.r(0, 0, 0, 32, '#7f957f'); d.r(49, 0, 49, 32, '#101914')
        for x in (4, 45):
            for y in (4, 28): d.circ(x, y, 1, '#14201a'); d.pt(x - 1, y - 1, '#a5bba5')
        d.r(6, 8, 43, 25, (0, 0, 0, 50)); d.r(6, 8, 43, 8, (200, 230, 200, 40))
        if peep: d.r(20, 13, 31, 16, '#050706'); d.r(20, 12, 31, 12, '#8aa08a')
        d.circ(42, 22, 3, '#6b7782'); d.circ(42, 22, 1, '#15191d'); d.r(36, 20, 39, 24, '#a67c28')
        s.paste(d, 21, 29); s.stain(seed + 3, (60, 30, 12), thr=.6, gain=6, maxa=.55, scale=1.5)
    else:
        d = S(60, 8); d.setim(tex(60, 8, P['pgreen'], seed, 1.4, .14, 1.1)); d.r(0, 0, 59, 0, '#7f957f'); d.r(0, 7, 59, 7, '#101914')
        for x in (5, 30, 54): d.circ(x, 4, 1, '#14201a')
        s.paste(d.im.rotate(-85, expand=True, resample=Image.NEAREST), 10, 62)
    return s.im

def double_door(seed=5, open_=False, style='plaster', kind='wood'):
    W = 2 * T; H = T + (50 if open_ else 0); s = S(W, H); s.setim(Image.new('RGBA', (W, H), (0, 0, 0, 0)))
    wm = np.zeros((T, W), bool); wm[A:B + 1, :] = True
    s.paste(wall_raw(0, style, seed, tile=wm), 0, 0)
    arr = np.array(s.im); arr[A:B + 1, 22:160] = (0, 0, 0, 0); s.setim(Image.fromarray(arr, 'RGBA'))
    s.bev(22, A, 28, B, '#3b271a'); s.bev(154, A, 160, B, '#3b271a'); s.bev(22, A, 160, A + 3, '#3b271a')
    if not open_:
        for k, x0 in enumerate((29, 92)):
            d = S(62, 33); d.setim(door_tex(62, 33, seed + k, kind)); d.r(0, 0, 61, 0, '#8a6340'); d.r(0, 32, 61, 32, '#150e0a'); d.r(0, 0, 0, 32, '#8a6340'); d.r(61, 0, 61, 32, '#150e0a')
            d.r(8, 7, 53, 25, (0, 0, 0, 55)); d.r(8, 7, 53, 7, (160, 120, 80, 70)); s.paste(d, x0, 29)
        s.circ(88, 46, 3, '#a67c28'); s.circ(94, 46, 3, '#a67c28'); s.pt(87, 45, '#e8c864'); s.pt(93, 45, '#e8c864'); s.r(88, 44, 94, 48, '#15191d')
    else:
        for k, (x0, ang) in enumerate(((20, -100), (162, 100))):
            d = S(58, 8); d.setim(door_tex(58, 8, seed + k, kind)); d.r(0, 0, 57, 0, '#8a6340'); d.r(0, 7, 57, 7, '#150e0a')
            r_ = d.im.rotate(ang, expand=True, resample=Image.NEAREST); s.paste(r_, x0 - (r_.width if k == 1 else 0) + (6 if k == 1 else -2), 66)
        s.r(32, 40, 152, 41, '#767d83')
    s.stain(seed + 9, (10, 8, 6), thr=.58, gain=5, maxa=.55, scale=1.3); return s.im

def window_barred(seed=6, style='plaster', broken=False):
    s = S(T, T); s.paste(wall_raw(10, style, seed), 0, 0)
    arr = np.array(s.im); arr[A:B + 1, 24:67] = (0, 0, 0, 0); s.setim(Image.fromarray(arr, 'RGBA'))
    s.bev(22, A, 66, A + 4, '#8d8f7c', '#b9bba3', '#3c3d34'); s.bev(22, B - 4, 66, B, '#8d8f7c', '#b9bba3', '#3c3d34')   # sill
    g = tex(41, 37, P['glass'], seed, 1.5, .14, 1.2); gs = S(41, 37); gs.setim(g)
    for k in range(-3, 4): gs.l([(k * 12, 36), (k * 12 + 30, 0)], (190, 230, 235, 40))
    s.paste(gs, 25, A + 5)
    if broken:
        rng = np.random.default_rng(seed)
        for k in range(3):
            cx, cy = 30 + k * 12, 38 + int(rng.integers(-3, 4)); pts = [(cx + int(rng.integers(-6, 7)), cy + int(rng.integers(-8, 9))) for _ in range(7)]
            s.p(pts, (0, 0, 0, 0) if False else '#05080a')
        for _ in range(14): s.l([(30 + int(rng.integers(0, 28)), A + 5 + int(rng.integers(0, 35)))] * 2, '#b9d5da')
        for k in range(4): s.l([(26 + k * 10, A + 6), (30 + k * 9, A + 20), (26 + k * 11, A + 34)], (230, 245, 248, 160))
    for x in (33, 45, 57):
        s.r(x - 1, A + 4, x + 1, B - 4, '#1b2024'); s.r(x - 1, A + 4, x - 1, B - 4, '#5f6b76'); s.pt(x, A + 5, '#8794a0')
    s.r(24, A + 4, 66, A + 4, '#2e353c'); s.r(24, B - 4, 66, B - 4, '#2e353c'); s.stain(seed + 5, (60, 30, 12), thr=.65, gain=6, maxa=.5, scale=1.6)
    return s.im

def iron_gate(open_=False, seed=8):
    W = 2 * T; H = T + (45 if open_ else 0); s = S(W, H)
    for x0 in (0, W - 30):
        s.bev(x0, 24, x0 + 29, 64, '#4e5250', '#7c8280', '#1b1c1b')
        s.bev(x0 + 6, 30, x0 + 23, 58, '#646967', '#9aa09d', '#2a2c2b'); s.circ(x0 + 14, 44, 5, '#7c8280'); s.circ(x0 + 14, 44, 3, '#3b3e3c'); s.pt(x0 + 12, 42, '#c0c5c2')
    def leaf(x0, x1):
        s.r(x0, 38, x1, 41, '#1d1410'); s.r(x0, 38, x1, 38, '#7a4a28'); s.r(x0, 51, x1, 54, '#1d1410'); s.r(x0, 51, x1, 51, '#7a4a28')
        for x in range(x0 + 2, x1 - 1, 7):
            s.r(x, 42, x, 50, '#2a1a14'); s.r(x + 1, 42, x + 1, 50, '#150e0c')
            s.p([(x - 1, 36), (x + 1, 33), (x + 3, 36), (x + 1, 39)], '#3a2418'); s.pt(x + 1, 34, '#b07a4a'); s.pt(x, 36, '#7a4a28')
    if not open_:
        leaf(30, W // 2 - 3); leaf(W // 2 + 3, W - 31)
        s.circ(W // 2, 46, 9, '#2a1a14'); s.circ(W // 2, 46, 7, '#1b1514'); s.circ(W // 2, 46, 3, '#7a4a28'); s.pt(W // 2 - 1, 45, '#c88a52')
        s.l([(W // 2 - 14, 54), (W // 2 - 6, 62), (W // 2 + 2, 64), (W // 2 + 12, 58)], '#6b6b60', 2); s.r(W // 2 + 12, 57, W // 2 + 16, 62, '#a67c28'); s.pt(W // 2 + 13, 58, '#e8c864')
    else:
        for sx in (30, W - 38):
            g = S(8, 50); g.r(0, 0, 7, 49, '#1b1514'); g.r(0, 0, 0, 49, '#7a4a28'); g.r(7, 0, 7, 49, '#0c0908')
            for y in range(2, 50, 7): g.r(1, y, 6, y + 1, '#2a1a14'); g.pt(3, y, '#b07a4a')
            s.paste(g.im, sx, 66)
        s.l([(40, 56), (60, 72), (80, 64)], '#6b6b60', 2)
    s.stain(seed + 2, (70, 36, 16), thr=.6, gain=6, maxa=.55, scale=1.8); return s.im

def build_doors(sh):
    raws = [('door_wood_h_closed', wood_door_closed(3), 3), ('door_wood_h_open', wood_door_open(3), 3), ('door_wood_h_boarded', wood_door_closed(4, boarded=True), 4),
            ('door_wood_h_broken', door_broken(7), 7), ('door_steel_h_closed', steel_door(4, 'closed'), 4), ('door_steel_h_open', steel_door(5, 'open'), 5),
            ('door_cell_h_closed', steel_door(6, 'closed', peep=True), 6), ('window_barred_h', window_barred(6), 6), ('window_barred_h_broken', window_barred(9, broken=True), 9),
            ('window_barred_ext_h', window_barred(8, 'brick'), 8)]
    for n, raw, sd in raws:
        sh.add(n, bake_wall(raw, seed=sd))
        if n != 'window_barred_ext_h': sh.add(n.replace('_h', '_v'), bake_wall(rot(raw, 270), seed=sd))
    sh.add('door_double_h_closed', bake_wall(double_door(5, False), seed=5)); sh.add('door_double_h_open', bake_wall(double_door(6, True), seed=6))
    sh.add('door_double_steel_h_closed', bake_wall(double_door(7, False, kind='steel'), seed=7))
    sh.add('gate_iron_closed', finalize(iron_gate(False), pad=6, grunge=.15)); sh.add('gate_iron_open', finalize(iron_gate(True), pad=6, grunge=.15))

def build():
    w = Sheet('tiles_walls'); build_walls(w); w.save(cols=8)
    d = Sheet('tiles_doors_windows'); build_doors(d); d.save(maxw=2600)

if __name__ == '__main__':
    build()
