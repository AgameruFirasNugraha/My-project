from px import *

def F(s, g=.25, **kw): return finalize(s, grunge=g, **kw)

def strap(s, x0, x1, y, bl=False):
    s.r(x0, y, x1, y + 2, '#35210f'); s.r(x0, y, x1, y, '#4d3118'); s.r(x0, y + 2, x1, y + 2, '#120a05')
    bx = x0 if bl else x1 - 4
    s.bev(bx, y - 1, bx + 4, y + 3, '#a67c28', '#e8c864', '#4d3510'); s.pt(bx + 2, y + 1, '#120a05')

def sheet_poly(s, pts, seed, hi=True):
    s.mtx(lambda d: d.polygon(pts, fill=255), P['sheet'], seed, scale=1.5, dither=.14, gain=.7)
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    rng = np.random.default_rng(seed)
    for _ in range(9):
        x = rng.integers(min(xs) + 3, max(xs) - 3); y = rng.integers(min(ys) + 3, max(ys) - 8)
        s.l([(x, y), (x + int(rng.integers(-5, 6)), y + int(rng.integers(5, 13)))], (30, 28, 22, 90))
        s.l([(x + 1, y), (x + 1 + int(rng.integers(-5, 6)), y + int(rng.integers(5, 13)))], (230, 228, 210, 60))

def bed(kind, seed=1):
    W, H = 54, 120; s = S(W, H)
    s.bev(0, 0, W - 1, H - 1, '#3a4a3c', '#657a66', '#1c2620'); s.speck(seed, .06, ['#7f6040', '#8a5a30'])
    for x, y in ((0, 0), (W - 5, 0), (0, H - 5), (W - 5, H - 5)): s.bev(x, y, x + 4, y + 4, '#2a372d', '#7f957f', '#101914'); s.pt(x + 2, y + 2, '#a5bba5')
    s.tx(5, 7, W - 6, H - 8, P['canvas'], seed, scale=1.1, dither=.14, gain=.9)
    s.r(5, 7, W - 6, 7, '#968f72'); s.r(5, 7, 5, H - 8, '#7b765c'); s.r(5, H - 8, W - 6, H - 8, '#1e1c15'); s.r(W - 6, 7, W - 6, H - 8, '#1e1c15')
    s.stain(seed + 3, (70, 56, 24), thr=.55, gain=5, maxa=.55, scale=1.5)
    s.bev(10, 10, W - 11, 28, '#aaa999', '#dddcc8', '#6b6a5f'); s.e(16, 14, W - 17, 25, (0, 0, 0, 28)); s.e(21, 16, 33, 22, (112, 92, 40, 70))
    if kind == 'strapped':
        for y, x1 in ((44, 19), (64, 23), (97, 20)): strap(s, 5, x1, y); strap(s, W - 6 - x1 + 5, W - 6, y, True)
        for x, y in ((12, 47), (40, 66), (10, 99)): s.blob(x, y, 4, 3, x, (80, 12, 14, 210)); s.blob(x + 1, y, 2, 1, x, (130, 24, 26, 220))
        s.l([(6, 100), (3, 114)], '#35210f', 2)
    elif kind == 'made':
        sheet_poly(s, [(6, 36), (W - 7, 36), (W - 7, H - 9), (6, H - 9)], seed); s.r(6, 36, W - 7, 41, '#c6c5b3'); s.r(6, 42, W - 7, 42, '#6b6a5f')
    elif kind == 'body':
        pts = [(18, 12), (27, 8), (36, 12), (37, 22), (42, 30), (44, 38), (43, 70), (40, 100), (36, 108), (31, 106), (27, 112), (24, 106), (19, 108), (15, 100), (11, 70), (10, 38), (12, 30), (17, 22)]
        sheet_poly(s, pts, seed); s.l([(16, 14), (13, 30), (12, 70), (15, 98)], (230, 228, 210, 90)); s.l([(40, 20), (42, 70), (38, 100)], (20, 18, 14, 110))
        s.blob(31, 48, 6, 7, 3, (92, 14, 16, 190)); s.blob(31, 48, 3, 4, 4, (140, 24, 26, 220)); s.blob(34, 62, 3, 2, 5, (92, 14, 16, 160))
    return s.im

def gurney(seed=2, body=False):
    W, H = 42, 114; s = S(W, H)
    s.bev(3, 0, W - 4, H - 1, '#6f7c87', '#c3ced6', '#2e353c')
    s.tx(7, 5, W - 8, H - 6, P['pgreen'], seed, scale=1.2, dither=.14); s.r(7, 5, W - 8, 5, '#7f957f')
    for y in (6, H - 9):
        s.bev(0, y, 3, y + 5, '#1d2227', '#444d56', '#0c0d0f'); s.bev(W - 4, y, W - 1, y + 5, '#1d2227', '#444d56', '#0c0d0f')
    if body: sheet_poly(s, [(13, 12), (21, 8), (29, 12), (29, 22), (33, 30), (34, 70), (30, 100), (25, 104), (21, 100), (17, 104), (11, 98), (8, 70), (8, 30), (13, 22)], seed); s.blob(22, 44, 5, 6, 3, (92, 14, 16, 190))
    else: sheet_poly(s, [(8, 50), (W - 9, 50), (W - 9, 105), (8, 105)], seed); s.r(8, 50, W - 9, 54, '#c6c5b3')
    return s.im

def wheelchair(seed=3):
    W, H = 40, 54; s = S(W, H)
    s.bev(0, 12, 4, 46, '#15191d', '#444d56', '#050607'); s.bev(W - 5, 12, W - 1, 46, '#15191d', '#444d56', '#050607')
    for y in range(14, 46, 6): s.pt(2, y, '#6b7782'); s.pt(W - 3, y, '#6b7782')
    s.l([(5, 28), (W - 6, 28)], '#444d56', 2); s.bev(6, 17, 8, 37, '#2e353c', '#6b7782', '#101316'); s.bev(W - 9, 17, W - 7, 37, '#2e353c', '#6b7782', '#101316')
    s.tx(9, 18, W - 10, 40, P['leather'], seed, scale=1.5, dither=.12); s.r(9, 18, W - 10, 18, '#4d3118'); s.r(9, 40, W - 10, 40, '#050302')
    s.bev(8, 12, W - 9, 16, '#2a1a0e', '#4d3118', '#0a0604'); s.r(7, 5, 9, 12, '#23282d'); s.r(W - 10, 5, W - 8, 12, '#23282d'); s.r(7, 5, 10, 6, '#6b7782'); s.r(W - 11, 5, W - 8, 6, '#6b7782')
    s.bev(12, 43, W - 13, 49, '#444d56', '#8794a0', '#1d2227'); s.circ(7, 46, 2, '#15191d'); s.circ(W - 8, 46, 2, '#15191d')
    return s.im

def straitjacket(seed=4):
    W = H = 38; s = S(W, H)
    s.mtx(lambda d: d.ellipse([6, 3, 32, 30], fill=255), P['canvas'], seed, scale=2, dither=.14)
    for sx, ex, ey in ((6, 29, 36), (32, 9, 36)):
        pts = [(sx, 14), ((sx + 19) // 2 + (3 if sx < 20 else -3), 24), (19, 28), (ex, ey)]
        s.l(pts, '#625e49', 7); s.l([(p[0] - 1, p[1] - 1) for p in pts], '#8a856a', 1); s.l([(p[0] + 2, p[1] + 2) for p in pts], '#34322a', 1)
    s.circ(19, 8, 4, '#15130d'); s.circ(19, 8, 3, '#262318'); s.l([(19, 12), (19, 28)], (30, 28, 20, 120)); s.l([(8, 20), (30, 20)], '#35210f', 1)
    for x, y in ((10, 33), (28, 33)): s.bev(x - 2, y, x + 2, y + 3, '#a67c28', '#e8c864', '#4d3510')
    s.stain(seed, (50, 38, 20), thr=.6, gain=6, maxa=.5, scale=2); return s.im

def iv_stand(seed=5):
    W = H = 30; s = S(W, H); cx = cy = 14
    for k in range(5):
        a = k * 1.2566 - 1.57; x = cx + math.cos(a) * 12; y = cy + math.sin(a) * 12
        s.l([(cx, cy), (x, y)], '#5f6b76', 2); s.circ(int(x), int(y), 2, '#15191d')
    s.circ(cx, cy, 3, '#8794a0'); s.circ(cx, cy, 1, '#dde3e8'); s.l([(cx, cy), (cx + 8, cy - 4)], '#8794a0')
    s.e(cx + 5, cy - 11, cx + 12, cy - 3, (150, 190, 205, 170)); s.e(cx + 6, cy - 10, cx + 8, cy - 8, (230, 245, 250, 220)); s.l([(cx + 8, cy - 3), (cx + 5, cy + 6), (cx + 12, cy + 12)], (140, 170, 180, 200))
    return s.im

def ect_machine(seed=6):
    W, H = 42, 42; s = S(W, H)
    s.bev(0, 0, 33, 31, '#4e6150', '#7f957f', '#1c2620'); s.tx(2, 2, 31, 29, P['pgreen'], seed, scale=1.5, dither=.14)
    s.bev(8, 3, 26, 8, '#0e1a1f', '#3a6670', '#050a0c'); s.l([(10, 7), (20, 4)], '#c0392b')
    for cx in (10, 24): s.circ(cx, 17, 6, '#15191d'); s.circ(cx, 17, 5, '#98a6b1'); s.circ(cx, 17, 4, '#2a2d2b'); s.l([(cx, 17), (cx + 3, 14)], '#d8d4c0'); s.pt(cx, 17, '#c0392b')
    for x in (6, 14, 22): s.bev(x, 25, x + 4, 28, '#23282d', '#6b7782', '#08090a'); s.pt(x + 2, 25, '#d6d5c3')
    s.r(28, 24, 31, 28, '#6b1014'); s.circ(31, 4, 1, '#c0392b')
    pts = [(31, 29), (35, 33), (33, 38), (37, 40)]; s.l(pts, '#050506', 2); s.l([(x - 1, y - 1) for x, y in pts], (90, 90, 90, 120))
    s.circ(37, 38, 3, '#8794a0'); s.circ(37, 38, 1, '#15191d'); return s.im

def ect_table(seed=7):
    W, H = 54, 112; s = S(W, H)
    s.bev(0, 0, W - 1, H - 1, '#444d56', '#8794a0', '#15191d'); s.tx(5, 5, W - 6, H - 6, P['leather'], seed, scale=1.4, dither=.12); s.r(5, 5, W - 6, 5, '#4d3118')
    for y in (28, 56, 86): s.r(5, y, W - 6, y, (0, 0, 0, 90))
    s.bev(14, 6, W - 15, 20, '#2a1a0e', '#4d3118', '#0a0604')
    strap(s, 5, W - 6, 44); strap(s, 5, W - 6, 78); strap(s, 8, W - 9, 100, True)
    for x in (19, W - 20): s.circ(x, 12, 3, '#8794a0'); s.circ(x, 12, 1, '#15191d')
    s.l([(19, 12), (12, 20), (6, 32), (-0, 40)], '#050506', 2); s.blob(27, 62, 3, 2, 2, (80, 12, 14, 170)); return s.im

def hydro_tub(mode='closed', seed=8):
    W, H = 52, 108; s = S(W, H)
    s.mtx(lambda d: d.rounded_rectangle([0, 0, W - 1, H - 1], radius=14, fill=255), P['white'], seed, scale=1.3, dither=.12, gain=.8)
    s.l([(3, 18), (3, 90)], (255, 255, 240, 60)); s.stain(seed + 1, (20, 15, 8), thr=.55, gain=5, maxa=.55, scale=1.4)
    if mode == 'closed':
        s.mtx(lambda d: d.rounded_rectangle([4, 4, W - 5, H - 14], radius=11, fill=255), P['canvas'], seed + 2, scale=2, dither=.14)
        s.rr(4, 4, W - 5, H - 14, (0, 0, 0, 0), 11)
        s.e(18, 14, 34, 30, '#0b1114'); s.e(19, 15, 33, 29, '#14262d'); s.arc = None
        s.e(21, 17, 31, 27, '#050a0c'); s.l([(18, 22), (34, 22)], (0, 0, 0, 0))
        for y in range(14, H - 16, 9):
            for x in (5, W - 7): s.bev(x, y, x + 2, y + 3, '#8794a0', '#dde3e8', '#2e353c')
        s.l([(8, 40), (W - 9, 44), (8, 62), (W - 9, 66)], (30, 28, 20, 120)); s.blob(34, 74, 6, 5, seed, (70, 40, 20, 90))
    else:
        s.mtx(lambda d: d.rounded_rectangle([5, 5, W - 6, H - 15], radius=10, fill=255), P['water'], seed + 3, scale=2.4, dither=.16, gain=1.2)
        if mode == 'blood': s.blob(26, 50, 15, 28, 4, (90, 14, 16, 120)); s.blob(22, 40, 9, 12, 6, (120, 20, 22, 90))
        for _ in range(11): x = int(np.random.default_rng(seed + _).integers(8, 44)); y = int(np.random.default_rng(seed + _ + 50).integers(8, 90)); s.l([(x, y), (x + 6, y)], (150, 190, 200, 60))
        s.blob(20, 30, 6, 4, 9, (14, 30, 20, 150)); s.l([(14, 20), (22, 26), (18, 38)], (8, 10, 8, 200))
    for x in (13, W - 14): s.circ(x, H - 8, 4, '#8794a0'); s.circ(x, H - 8, 2, '#c3ced6'); s.pt(x - 1, H - 9, '#ffffff')
    s.r(W // 2 - 3, H - 14, W // 2 + 3, H - 4, '#6f7c87'); s.r(W // 2 - 1, H - 14, W // 2 + 1, H - 12, '#15191d'); return s.im

def med_cart(seed=9):
    W, H = 38, 52; s = S(W, H)
    s.bev(1, 2, W - 2, H - 3, '#6f7c87', '#c3ced6', '#2e353c'); s.tx(4, 5, W - 5, H - 6, P['steel'], seed, scale=1.5, dither=.1)
    s.r(4, 0, W - 5, 2, '#444d56'); s.r(4, 0, W - 5, 0, '#8794a0')
    for x, y in ((0, 4), (W - 3, 4), (0, H - 8), (W - 3, H - 8)): s.bev(x, y, x + 2, y + 4, '#15191d', '#444d56', '#050607')
    cols = ['#a35f1c', '#6a8a8f', '#c6c5b3', '#a35f1c', '#4e6150']
    for i, c in enumerate(cols): x = 8 + (i % 3) * 8; y = 10 + (i // 3) * 8; s.circ(x, y, 3, c); s.circ(x, y, 1, '#15191d'); s.pt(x - 1, y - 1, '#fff2c0')
    s.e(6, 28, 24, 38, '#9aa6af'); s.e(8, 30, 22, 36, '#4a5760'); s.blob(15, 33, 3, 2, 1, (90, 14, 16, 220))
    s.l([(26, 14), (32, 30)], '#dddcc8', 1); s.pt(32, 31, '#c3ced6')
    for k in range(6): s.pt(10 + k * 3 % 17, 44 + k % 3, '#e8e4d0')
    return s.im

def surgical_lamp(seed=10):
    W = H = 66; s = S(W, H); c = 33
    s.l([(0, 0), (c, c)], '#444d56', 5); s.l([(0, 0), (c, c)], '#8794a0', 1)
    s.circ(c, c, 28, '#1d2227'); s.circ(c, c, 26, '#5f6b76'); s.circ(c, c, 22, '#98a6b1'); s.circ(c, c, 19, '#6f7c87')
    for k in range(8):
        a = k * .785; x = c + math.cos(a) * 14; y = c + math.sin(a) * 14; s.circ(int(x), int(y), 4, '#2e353c'); s.circ(int(x), int(y), 3, '#ffe9a6'); s.pt(int(x) - 1, int(y) - 1, '#ffffff')
    s.circ(c, c, 7, '#23282d'); s.circ(c, c, 5, '#5f6b76'); s.pt(c - 2, c - 2, '#c3ced6')
    s.l([(c - 24, c - 12), (c - 12, c - 24)], (255, 255, 255, 80)); return s.im

def steel_table(body=False, seed=11):
    W, H = 44, 122; s = S(W, H)
    s.bev(0, 0, W - 1, H - 1, '#6f7c87', '#c3ced6', '#2e353c'); s.tx(3, 3, W - 4, H - 4, P['steel'], seed, scale=2, dither=.1, gain=.8)
    s.r(3, 3, W - 4, 4, '#98a6b1'); s.r(W // 2 - 2, 8, W // 2 + 2, H - 14, '#15191d'); s.r(W // 2 - 2, 8, W // 2 - 2, H - 14, '#050607')
    s.r(8, 6, W - 9, 18, '#5f6b76'); s.circ(W // 2, H - 10, 5, '#15191d'); s.circ(W // 2, H - 10, 3, '#5f6b76'); s.l([(W // 2 - 2, H - 10), (W // 2 + 2, H - 10)], '#0a0d0f')
    for x in (6, W - 7): s.circ(x, H - 6, 2, '#15191d')
    s.stain(seed + 2, (60, 14, 12), thr=.66, gain=7, maxa=.55, scale=2.4)
    if body:
        sheet_poly(s, [(14, 14), (22, 10), (30, 14), (30, 22), (34, 30), (35, 70), (31, 104), (26, 112), (22, 108), (18, 112), (12, 104), (9, 70), (9, 30), (14, 22)], seed)
        s.blob(22, 50, 5, 7, 3, (92, 14, 16, 190)); s.r(18, 114, 24, 120, '#dddcc8'); s.l([(21, 112), (21, 114)], '#8a856a'); s.r(19, 116, 23, 116, '#6b6a5f')
    return s.im

def morgue_unit(open_=False, seed=12):
    W = 152; H = 52 + (96 if open_ else 0); s = S(W, H)
    s.bev(0, 0, W - 1, 51, '#6f7c87', '#c3ced6', '#2e353c'); s.tx(3, 3, W - 4, 48, P['steel'], seed, scale=3, dither=.1, gain=.8)
    for i in range(4): s.r(38 * i + 1, 3, 38 * i + 1, 48, '#2e353c')
    for i in range(4): s.bev(38 * i + 12, 44, 38 * i + 26, 48, '#98a6b1', '#e8eef2', '#3c454c')
    for x in (20, 58, 96, 134): s.r(x, 8, x + 3, 20, '#1d2227')
    s.stain(seed, (30, 40, 44), thr=.55, gain=5, maxa=.5, scale=2.2)
    if open_:
        s.bev(52, 52, 100, H - 1, '#98a6b1', '#e8eef2', '#3c454c'); s.tx(55, 55, 97, H - 4, P['steel'], seed + 1, scale=2)
        sheet_poly(s, [(63, 62), (76, 58), (89, 62), (89, 70), (93, 78), (94, 110), (90, 134), (83, 144), (76, 138), (69, 144), (62, 134), (58, 110), (59, 78), (63, 70)], seed)
        s.blob(76, 98, 6, 8, 3, (92, 14, 16, 190)); s.r(72, 138, 80, 146, '#dddcc8'); s.l([(76, 134), (76, 138)], '#8a856a')
    return s.im

def instrument_tray(seed=13):
    W, H = 44, 30; s = S(W, H)
    s.bev(0, 0, W - 1, H - 1, '#6f7c87', '#c3ced6', '#2e353c'); s.tx(2, 2, W - 3, H - 3, P['steel'], seed, scale=2, dither=.1)
    s.p([(5, 6), (22, 5), (24, 9), (6, 10)], '#d6d5c3'); s.l([(8, 8), (30, 14)], '#e8eef2'); s.l([(8, 8), (30, 14)], '#3c454c')
    s.l([(6, 18), (20, 16)], '#c3ced6', 2); s.l([(10, 24), (30, 22)], '#c3ced6'); s.r(26, 18, 38, 22, '#8794a0')
    for k in range(6): s.pt(27 + k * 2, 17, '#e8eef2')
    s.l([(30, 8), (38, 6)], '#c3ced6'); s.l([(30, 8), (37, 11)], '#c3ced6')
    for x, y in ((12, 13), (17, 12), (34, 25), (36, 15)): s.blob(x, y, 2, 2, x, (96, 14, 16, 230)); s.pt(x, y, '#d04040')
    return s.im

def mop_bucket(seed=14):
    W = H = 30; s = S(W, H)
    s.l([(15, 15), (26, 1)], '#7b765c', 2); s.circ(14, 15, 11, '#6b6120'); s.circ(14, 15, 10, '#8a7a2a'); s.circ(14, 15, 8, '#1b2216'); s.circ(14, 15, 7, '#2a3a2a')
    s.l([(9, 12), (14, 11)], (150, 190, 170, 80)); s.pt(10, 10, '#8a9a8a')
    for k in range(9): a = k * .7; s.l([(24, 22), (24 + math.cos(a) * 4, 22 + math.sin(a) * 4)], '#7b765c')
    s.circ(24, 22, 2, '#3a3830'); return s.im

# ---------------- administration
def desk(kind='director', seed=15):
    if kind == 'director':
        W, H = 104, 54; s = S(W, H)
        s.bev(0, 0, W - 1, H - 1, '#3b271a', '#82603f', '#150e0a'); s.tx(3, 3, W - 4, H - 4, P['wood'], seed, scale=2.2, dither=.12, gain=1.2)
        s.bev(18, 10, 86, 44, '#1c2620', '#3a4a3c', '#08100c'); s.r(20, 12, 84, 12, '#a67c28'); s.r(20, 42, 84, 42, '#a67c28'); s.r(20, 12, 20, 42, '#a67c28'); s.r(84, 12, 84, 42, '#a67c28')
        s.circ(12, 14, 6, '#2a4a35'); s.circ(12, 14, 4, '#3f7a52'); s.pt(10, 12, '#a5d9b5'); s.r(10, 20, 14, 22, '#2a2d2b')
        s.p([(34, 18), (60, 16), (62, 30), (36, 32)], '#c6c5b3'); s.l([(38, 22), (56, 21)], '#4a4636'); s.l([(38, 26), (58, 25)], '#4a4636'); s.p([(50, 28), (72, 30), (70, 38), (48, 36)], '#b5af8f')
        s.circ(92, 34, 5, '#2a2d2b'); s.circ(92, 34, 3, '#15191d'); s.pt(90, 33, '#c0392b'); s.l([(76, 20), (84, 14)], '#1c1c1c', 1)
        s.blob(72, 24, 3, 2, 1, (20, 12, 8, 190)); s.r(40, 40, 52, 44, '#4d3118')
    else:
        W, H = 84, 46; s = S(W, H); s.bev(0, 0, W - 1, H - 1, '#444d56', '#8794a0', '#15191d'); s.tx(3, 3, W - 4, H - 4, P['metal'], seed, scale=2, dither=.1)
        s.p([(8, 8), (30, 6), (32, 22), (10, 24)], '#b5af8f'); s.p([(26, 20), (52, 22), (50, 36), (24, 34)], '#c6c5b3'); s.l([(30, 26), (46, 28)], '#4a4636')
        s.bev(58, 8, 76, 22, '#23282d', '#6b7782', '#08090a'); s.r(60, 10, 74, 12, '#c6c5b3')
    s.stain(seed + 1, (10, 8, 6), thr=.6, gain=5, maxa=.55, scale=1.5); return s.im

def chair_office(seed=16, dir_=0):
    W = H = 30; s = S(W, H); c = 15
    for k in range(5):
        a = k * 1.2566 + .3; x = c + math.cos(a) * 12; y = c + math.sin(a) * 12; s.l([(c, c), (x, y)], '#2e353c', 2); s.circ(int(x), int(y), 2, '#08090a')
    s.circ(c, c, 9, '#15100a'); s.circ(c, c, 8, '#35210f'); s.circ(c - 2, c - 2, 4, '#4d3118'); s.pt(c - 3, c - 3, '#7a5a3a')
    s.bev(c - 8, 2, c + 8, 6, '#2a1a0e', '#4d3118', '#0a0604'); return rot(s.im, dir_)

def reception_desk(seed=17):
    W, H = 132, 70; s = S(W, H)
    def arc(r_out, r_in, c_):
        pts = [(66 + math.cos(a) * r_out[0], 4 + math.sin(a) * r_out[1]) for a in np.linspace(0, math.pi, 28)] + [(66 + math.cos(a) * r_in[0], 4 + math.sin(a) * r_in[1]) for a in np.linspace(math.pi, 0, 28)]
        return pts
    outer = arc((64, 62), (46, 44), 0)
    s.mtx(lambda d: d.polygon(outer, fill=255), P['wood'], seed, scale=2, dither=.12, gain=1.2)
    inner = arc((60, 58), (50, 48), 0); s.mtx(lambda d: d.polygon(inner, fill=255), RP('#3b271a', '#503523', '#68472f', '#82603f', '#99724a'), seed + 1, scale=3, dither=.1, gain=.8)
    s.l([(20, 40), (36, 52), (66, 60), (96, 52), (112, 40)], (255, 230, 200, 70))
    s.circ(46, 40, 3, '#a67c28'); s.pt(45, 39, '#fff2b0'); s.bev(70, 28, 86, 38, '#35210f', '#7a5a3a', '#0a0604'); s.l([(72, 31), (84, 31)], '#c6c5b3')
    s.p([(96, 34), (106, 36), (104, 42), (94, 40)], '#15191d'); s.stain(seed + 2, (10, 8, 6), thr=.6, gain=5, maxa=.5, scale=1.4); return s.im

def filing_cabinet(open_=False, seed=18):
    W, H = 32, 40 + (30 if open_ else 0); s = S(W, H)
    s.bev(0, 0, W - 1, 39, '#4e6150', '#7f957f', '#1c2620'); s.tx(3, 3, W - 4, 36, P['pgreen'], seed, scale=2, dither=.1); s.r(3, 36, W - 4, 36, '#101914')
    s.bev(11, 33, 21, 36, '#98a6b1', '#e8eef2', '#3c454c'); s.p([(6, 8), (22, 7), (23, 16), (8, 18)], '#b5af8f'); s.l([(9, 11), (20, 10)], '#4a4636')
    if open_:
        s.bev(3, 40, W - 4, H - 1, '#6f7c87', '#c3ced6', '#2e353c'); s.r(5, 42, W - 6, H - 3, '#15191d')
        for i, c in enumerate(('#b5af8f', '#c6c5b3', '#a59f80', '#d3cdac', '#968f72', '#b5af8f')): s.r(6 + i * 4, 44 + (i % 2), 8 + i * 4, H - 5, c); s.r(6 + i * 4, 44 + (i % 2), 8 + i * 4, 44 + (i % 2), '#e4dfc2')
    return s.im

def archive_shelf(seed=19):
    W, H = 124, 32; s = S(W, H); s.bev(0, 0, W - 1, H - 1, '#444d56', '#8794a0', '#15191d'); rng = np.random.default_rng(seed)
    x = 3
    while x < W - 14:
        w = int(rng.integers(10, 14)); h = int(rng.integers(20, 26)); c = ['#a59f80', '#8a856a', '#b5af8f', '#7b765c'][int(rng.integers(0, 4))]
        s.bev(x, 4, x + w, 4 + h, c); s.r(x + 2, 8, x + w - 2, 12, '#d3cdac'); s.l([(x + 3, 10), (x + w - 3, 10)], '#4a4636'); x += w + 1
    s.p([(70, 20), (84, 24), (80, 30), (66, 26)], '#c6c5b3'); s.stain(seed, (10, 8, 6), thr=.6, gain=5, maxa=.55, scale=1.4); return s.im

def smalls(sh, seed=20):
    s = S(28, 24); s.bev(0, 4, 27, 23, '#23282d', '#5f6b76', '#050607'); s.r(4, 0, 23, 6, '#c6c5b3'); s.r(4, 0, 23, 0, '#e4dfc2'); s.l([(7, 3), (20, 3)], '#4a4636'); s.r(3, 8, 24, 10, '#444d56')
    for r_ in range(3):
        for k in range(8): s.pt(4 + k * 3, 14 + r_ * 3, '#c3ced6')
    sh.add('prop_typewriter', F(s, .15))
    s = S(22, 20); s.rr(0, 4, 21, 19, '#15191d', 3); s.circ(11, 12, 6, '#2e353c'); s.circ(11, 12, 4, '#15191d')
    for k in range(8): a = k * .75; s.pt(int(11 + math.cos(a) * 5), int(12 + math.sin(a) * 5), '#c6c5b3')
    s.rr(0, 0, 21, 5, '#23282d', 2); s.l([(3, 2), (18, 2)], '#5f6b76'); sh.add('prop_phone_rotary', F(s, .15))
    s = S(26, 20); s.p([(2, 4), (22, 2), (24, 16), (3, 18)], '#a59f80'); s.p([(0, 7), (20, 5), (22, 18), (2, 19)], '#c6c5b3'); s.r(4, 9, 16, 9, '#6b6a5f'); s.r(4, 12, 14, 12, '#6b6a5f'); sh.add('prop_folders', F(s, .2))
    s = S(32, 26); s.bev(0, 0, 31, 25, '#a59f80'); s.bev(16, 1, 30, 24, '#c6c5b3'); s.bev(4, 5, 12, 14, '#15191d', '#4a4636', '#050403'); s.circ(8, 8, 2, '#8a6a58'); s.r(6, 11, 10, 13, '#8a6a58')
    for y in (6, 11, 16, 20): s.l([(18, y), (28, y)], '#4a4636')
    sh.add('prop_patient_file_open', F(s, .2))
    s = S(18, 18); s.circ(7, 7, 6, '#3d3b30'); s.circ(7, 7, 4, (0, 0, 0, 0))
    for k in range(3): s.bev(10 + k * 2, 4 + k * 3, 16 + k * 2, 6 + k * 3, '#a67c28', '#e8c864', '#4d3510')
    s.circ(7, 7, 3, '#15130d'); sh.add('prop_keys_ring', F(s, .1))
    s = S(20, 26); s.bev(0, 2, 19, 25, '#7a5a3a', '#a07a52', '#2a1a0e'); s.bev(2, 6, 17, 23, '#c6c5b3'); s.bev(6, 0, 13, 4, '#8794a0', '#c3ced6', '#2e353c')
    for y in (10, 14, 18): s.l([(4, y), (15, y)], '#4a4636')
    sh.add('prop_clipboard', F(s, .15))

def tv_cart(seed=21):
    W, H = 44, 54; s = S(W, H)
    s.bev(1, 20, W - 2, H - 2, '#444d56', '#8794a0', '#15191d')
    for x, y in ((0, 20), (W - 4, 20), (0, H - 6), (W - 4, H - 6)): s.bev(x, y, x + 3, y + 5, '#15191d', '#444d56', '#050607')
    s.bev(5, 22, W - 6, 46, '#a59f80', '#d3cdac', '#34322a'); s.tx(7, 24, W - 8, 44, P['canvas'], seed, scale=2, dither=.1)
    s.p([(10, 22), (W - 11, 22), (W - 15, 6), (14, 6)], '#7b765c'); s.l([(10, 22), (14, 6)], '#d3cdac'); s.l([(W - 11, 22), (W - 15, 6)], '#34322a'); s.r(14, 6, W - 15, 7, '#34322a')
    for k in range(5): s.l([(16 + k * 3, 10), (16 + k * 3, 17)], '#34322a')
    s.r(8, 46, W - 9, 48, '#c8d8e0'); s.r(10, 47, W - 11, 47, '#ffffff')
    s.l([(W // 2, 6), (W // 2 - 10, -0)], '#98a6b1'); s.l([(W // 2, 6), (W // 2 + 11, 0)], '#98a6b1'); return s.im

def bench(w=104, seed=22):
    s = S(w, 28); s.bev(0, 0, w - 1, 6, '#3b271a', '#82603f', '#150e0a'); s.tx(1, 1, w - 2, 5, P['wood'], seed, scale=3, dither=.1)
    for i, y in enumerate((9, 14, 19)): s.bev(1, y, w - 2, y + 3, '#503523', '#82603f', '#150e0a'); s.r(2, y + 1, w - 3, y + 1, (255, 220, 170, 40))
    for x in (6, w - 9): s.r(x, 8, x + 3, 25, '#1d2227')
    s.stain(seed, (10, 8, 6), thr=.6, gain=5, maxa=.5, scale=1.5); return s.im

def lockers(seed=23, w=126):
    s = S(w, 34); n = 5; cw = (w - 2) // n
    for i in range(n):
        x = 1 + i * cw; s.bev(x, 0, x + cw - 2, 33, '#4e6150', '#7f957f', '#1c2620'); s.tx(x + 2, 2, x + cw - 4, 31, P['pgreen'], seed + i, scale=2, dither=.1)
        for k in range(5): s.r(x + 5, 6 + k * 3, x + cw - 7, 6 + k * 3, '#08100c')
        s.bev(x + cw - 9, 22, x + cw - 6, 28, '#98a6b1', '#e8eef2', '#3c454c')
    s.stain(seed, (80, 40, 16), thr=.6, gain=6, maxa=.55, scale=1.8); return s.im

def sofa(seed=24):
    W, H = 96, 42; s = S(W, H)
    s.bev(0, 0, W - 1, H - 1, '#3d3b30', '#625e49', '#15130d'); s.tx(2, 2, W - 3, 10, P['canvas'], seed, scale=3, dither=.14)
    for x in (2, W - 12): s.bev(x, 10, x + 9, H - 3, '#4a4738', '#7b765c', '#1b1a12')
    for i in range(3): x = 14 + i * 24; s.bev(x, 12, x + 22, H - 4, '#55523f', '#8a856a', '#23221a'); s.circ(x + 11, 24, 1, '#15130d')
    s.stain(seed + 1, (22, 16, 10), thr=.55, gain=5, maxa=.7, scale=1.5); s.stain(seed + 2, (80, 20, 16), thr=.78, gain=9, maxa=.5, scale=2.4)
    s.l([(34, 14), (40, 22), (36, 30)], (8, 8, 6, 220)); return s.im

def chair_plastic(seed=25, rot_=0):
    s = S(24, 24); s.bev(2, 4, 21, 21, '#4e6a78', '#7f9fb0', '#1c2a32'); s.bev(2, 0, 21, 5, '#3b5260', '#6c8a99', '#12202a'); s.e(7, 9, 16, 16, (0, 0, 0, 30))
    for x, y in ((2, 20), (19, 20)): s.r(x, y, x + 2, y + 2, '#15191d')
    return rot(s.im, rot_)

def table_round(seed=26):
    s = S(34, 34); s.mtx(lambda d: d.ellipse([0, 0, 33, 33], fill=255), P['wood'], seed, scale=2.5, dither=.12, gain=1.2); s.l([(5, 12), (12, 5)], (255, 220, 170, 60))
    s.circ(11, 12, 3, '#9aa6af'); s.circ(11, 12, 2, '#2a1a0e'); s.circ(22, 20, 4, '#2a2d2b'); s.circ(22, 20, 2, '#15191d'); s.pt(21, 19, '#c0392b'); s.p([(14, 22), (24, 24), (22, 28), (12, 26)], '#c6c5b3')
    s.stain(seed, (10, 8, 6), thr=.6, gain=5, maxa=.5, scale=1.5); return s.im

# ---------------- patient traces
def chair_wood(seed=27, rot_=0):
    s = S(28, 28); s.bev(3, 5, 24, 25, '#503523', '#82603f', '#150e0a'); s.tx(5, 7, 22, 23, P['wood'], seed, scale=2, dither=.1)
    s.bev(2, 0, 25, 5, '#3b271a', '#68472f', '#0e0906')
    for x, y in ((1, 23), (23, 23)): s.r(x, y, x + 3, y + 3, '#150e0a'); s.pt(x + 1, y + 1, '#82603f')
    return rot(s.im, rot_)

def rocking_chair(seed=28):
    W, H = 34, 42; s = S(W, H)
    for x in (0, W - 4): s.mtx(lambda d, x=x: d.ellipse([x, 0, x + 3, H - 1], fill=255), P['wood'][:4], seed, scale=3)
    s.bev(5, 8, W - 6, 36, '#503523', '#82603f', '#150e0a'); s.tx(7, 10, W - 8, 34, P['wood'], seed, scale=2); s.bev(4, 2, W - 5, 8, '#3b271a', '#68472f', '#0e0906')
    for x in (4, W - 8): s.bev(x, 12, x + 3, 34, '#3b271a', '#68472f', '#0e0906')
    s.l([(10, 3), (10, 8)], '#150e0a'); s.l([(17, 3), (17, 8)], '#150e0a'); s.l([(24, 3), (24, 8)], '#150e0a'); return s.im

def doll(seed=29):
    W, H = 20, 28; s = S(W, H)
    s.p([(6, 10), (14, 10), (16, 22), (4, 22)], '#8a856a'); s.p([(6, 10), (10, 10), (10, 22), (4, 22)], '#a59f80'); s.l([(6, 11), (0, 15)], '#c6b898', 2); s.l([(14, 11), (19, 16)], '#c6b898', 2)
    s.l([(7, 22), (6, 27)], '#c6b898', 2); s.l([(13, 22), (14, 27)], '#c6b898', 2); s.circ(10, 6, 5, '#d6c6a6'); s.circ(9, 5, 3, '#e6d8b8')
    for x in (-1, 0, 1): s.l([(5 + x, 3), (3 + x * 2, 9)], '#2a1a0e')
    s.l([(15, 3), (17, 9)], '#2a1a0e'); s.l([(5, 1), (15, 1)], '#2a1a0e', 2); s.pt(8, 6, '#0a0a0a'); s.pt(12, 6, '#0a0a0a'); s.l([(7, 9), (13, 9)], '#4a1a1a')
    s.l([(7, 13), (13, 15)], '#4a4636'); s.pt(10, 14, '#15130d'); s.l([(11, 7), (11, 11)], (120, 20, 22, 200)); return s.im

def shoe(seed=30):
    s = S(14, 20); s.mtx(lambda d: d.polygon([(4, 0), (10, 0), (12, 6), (11, 14), (9, 19), (4, 19), (2, 13), (3, 6)], fill=255), P['leather'], seed, scale=2.5)
    s.circ(7, 6, 2, '#050302'); s.l([(4, 10), (10, 10)], '#c6c5b3'); s.l([(4, 13), (10, 13)], '#c6c5b3'); s.r(4, 16, 9, 19, '#0a0604'); return s.im

def cup_tin(seed=31):
    s = S(12, 12); s.circ(6, 6, 5, '#6b7782'); s.circ(6, 6, 4, '#98a6b1'); s.circ(6, 6, 3, '#2e353c'); s.pt(4, 4, '#e8eef2'); s.r(9, 5, 11, 7, '#6b7782'); return s.im

def music_box(seed=32):
    s = S(24, 20); s.bev(0, 0, 23, 19, '#3b271a', '#82603f', '#150e0a'); s.tx(2, 2, 21, 17, P['wood'], seed, scale=2); s.bev(2, 2, 21, 12, '#7a1a1e', '#a82a30', '#2a0508')
    s.circ(12, 7, 3, '#e8e4d0'); s.circ(12, 5, 1, '#e8c0a0'); s.l([(10, 8), (14, 8)], '#e8e4d0'); s.circ(18, 15, 1, '#a67c28'); return s.im

def build(sh_med, sh_adm, sh_trc):
    sh = sh_med
    sh.add('prop_bed_strapped', F(bed('strapped', 1))); sh.add('prop_bed_made', F(bed('made', 2))); sh.add('prop_bed_body_sheet', F(bed('body', 3)))
    sh.add('prop_gurney', F(gurney(2))); sh.add('prop_gurney_body', F(gurney(3, True))); sh.add('prop_wheelchair', F(wheelchair()))
    sh.add('prop_straitjacket_floor', F(straitjacket())); sh.add('prop_iv_stand', F(iv_stand())); sh.add('prop_ect_machine', F(ect_machine())); sh.add('prop_ect_table', F(ect_table()))
    sh.add('prop_hydro_tub_covered', F(hydro_tub('closed', 8))); sh.add('prop_hydro_tub_open', F(hydro_tub('open', 9))); sh.add('prop_hydro_tub_blood', F(hydro_tub('blood', 10)))
    sh.add('prop_med_cart', F(med_cart())); sh.add('prop_surgical_lamp', F(surgical_lamp(), .1)); sh.add('prop_operating_table', F(steel_table(False))); sh.add('prop_autopsy_table_body', F(steel_table(True)))
    sh.add('prop_morgue_unit', F(morgue_unit(False))); sh.add('prop_morgue_unit_drawer_open', F(morgue_unit(True))); sh.add('prop_instrument_tray', F(instrument_tray())); sh.add('prop_mop_bucket', F(mop_bucket()))
    a = sh_adm
    a.add('prop_desk_director', F(desk('director'))); a.add('prop_desk_steel', F(desk('steel', 16))); a.add('prop_chair_office', F(chair_office())); a.add('prop_chair_office_toppled', F(chair_office(17, 35)))
    a.add('prop_reception_desk', F(reception_desk())); a.add('prop_filing_cabinet', F(filing_cabinet(False))); a.add('prop_filing_cabinet_open', F(filing_cabinet(True)))
    a.add('prop_archive_shelf', F(archive_shelf())); smalls(a); a.add('prop_tv_cart', F(tv_cart())); a.add('prop_bench_waiting', F(bench())); a.add('prop_lockers', F(lockers()))
    a.add('prop_sofa_worn', F(sofa())); a.add('prop_chair_plastic', F(chair_plastic())); a.add('prop_chair_plastic_b', F(chair_plastic(26, 40))); a.add('prop_table_round', F(table_round()))
    t = sh_trc
    for i, r_ in enumerate((0, 90, 180, 270)): t.add(f'prop_chair_wood_{i}', F(chair_wood(27, r_)))
    t.add('prop_rocking_chair', F(rocking_chair())); t.add('prop_doll_rag', F(doll(), .1)); t.add('prop_shoe_single', F(shoe(), .1)); t.add('prop_cup_tin', F(cup_tin(), .1)); t.add('prop_music_box', F(music_box(), .1))

if __name__ == '__main__':
    a, b, c = Sheet('props_medical'), Sheet('props_admin_furniture'), Sheet('props_patient_traces')
    build(a, b, c)
    for x in (a, b, c): x.save()
