import numpy as np, os, json, math
from PIL import Image, ImageDraw, ImageFont

T = 91          # 1 tile = 91 art px  -> x2 = 182 px final
OUT = '/home/claude/out'
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf'

def C(h, a=255):
    if isinstance(h, (tuple, list)):
        h = tuple(int(v) for v in h)
        return h if len(h) == 4 else h + (a,)
    h = h.lstrip('#')
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)

def RP(*hs): return [C(h) for h in hs]
def mix(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3)) + (255,)
def shd(c, f): return (int(min(255, c[0] * f)), int(min(255, c[1] * f)), int(min(255, c[2] * f)), c[3] if len(c) > 3 else 255)

# ---------------------------------------------------------------- palettes (dark -> light), desaturated horror grade
P = dict(
    wood=RP('#1a110c', '#2a1b12', '#3b271a', '#503523', '#68472f', '#82603f'),
    brick=RP('#2b1311', '#411c18', '#5b2a22', '#763a2e', '#925042', '#ab6654'),
    plaster=RP('#262822', '#383a31', '#4c4f42', '#636653', '#7d806a', '#999c84'),
    concrete=RP('#16181a', '#222528', '#32363a', '#454a4f', '#5b6167', '#767d83'),
    stone=RP('#1b1c1b', '#2a2c2b', '#3b3e3c', '#4e5250', '#646967', '#7c8280'),
    metal=RP('#101316', '#1d2227', '#2e353c', '#444d56', '#5f6b76', '#8794a0'),
    steel=RP('#1c2024', '#323a41', '#4d5760', '#6f7c87', '#98a6b1', '#c3ced6'),
    pgreen=RP('#1c2620', '#2a372d', '#3a4a3c', '#4e6150', '#657a66', '#7f957f'),
    rust=RP('#2a130a', '#431e0f', '#632f18', '#85441f', '#a5602d'),
    tilew=RP('#3b4341', '#566260', '#728080', '#8e9c98', '#abb7b0', '#c9d2c8'),
    tilec=RP('#242d2f', '#35413f', '#4a585b', '#617479', '#7c9097', '#9db0b6'),
    lino=RP('#313829', '#444c35', '#5a6444', '#727d52', '#8c9763'),
    lino2=RP('#4a463a', '#625d4b', '#7b765f', '#979078', '#b3ac90'),
    grass=RP('#09130f', '#102019', '#182f21', '#223f2a', '#2f5236', '#41683f'),
    dgrass=RP('#16150d', '#24221a', '#363324', '#4b4731', '#645e40', '#7d7650'),
    dirt=RP('#16110d', '#241b14', '#35271b', '#4b3825', '#654d33'),
    blood=RP('#150304', '#280507', '#420a0d', '#620f13', '#85181c'),
    water=RP('#070f12', '#0f1c22', '#182b34', '#233c47', '#33525e'),
    slate=RP('#0f1316', '#1a2025', '#272f36', '#363f48', '#485560'),
    canvas=RP('#34322a', '#4a4738', '#625e49', '#7b765c', '#968f72'),
    leather=RP('#120a05', '#22140a', '#35210f', '#4d3118'),
    paper=RP('#4a4636', '#6c6750', '#918b6e', '#b5af8f', '#d3cdac'),
    brass=RP('#2a1d08', '#4d3510', '#7a5719', '#a67c28', '#cfa645'),
    glass=RP('#0e1a1f', '#17303a', '#22464f', '#3a6670', '#7ea5ad'),
    sheet=RP('#4d4c44', '#6b6a5f', '#8b8a7c', '#aaa999', '#c6c5b3', '#dddcc8'),
    moss=RP('#0f1a10', '#192b17', '#264022', '#36582f', '#4b7440'),
    carpet=RP('#1d0f0f', '#2a1514', '#3a1d1b', '#4b2824', '#5e3430'),
    terra=RP('#2a120c', '#41200f', '#5d311a', '#7a4326', '#97583a'),
    bark=RP('#0e0a08', '#1a1210', '#2a1e18', '#3c2c22', '#53402f'),
    pine=RP('#06100c', '#0b1b14', '#122a1d', '#1b3b27', '#285234'),
    white=RP('#5a594f', '#7b7a6d', '#9c9b8c', '#bab9a8', '#d6d5c3', '#ececd8'),
)
OL = (12, 9, 11)   # outline colour (never pure black)

# ---------------------------------------------------------------- noise
_B4 = (np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0 - 0.5)
def bayer(w, h): return np.tile(_B4, (h // 4 + 1, w // 4 + 1))[:h, :w]

def quant(n, rp, dither=0.0):
    h, w = n.shape
    if dither: n = n + bayer(w, h) * dither
    idx = np.clip((np.clip(n, 0, 0.9999) * len(rp)).astype(int), 0, len(rp) - 1)
    return Image.fromarray(np.array(rp, dtype=np.uint8)[idx], 'RGBA')

def vnoise(w, h, gx, gy, seed):
    rng = np.random.default_rng(seed)
    g = rng.random((gy, gx))
    xs = np.arange(w) * gx / w; ys = np.arange(h) * gy / h
    x0 = xs.astype(int) % gx; y0 = ys.astype(int) % gy
    x1 = (x0 + 1) % gx; y1 = (y0 + 1) % gy
    fx = xs - np.floor(xs); fy = ys - np.floor(ys)
    fx = fx * fx * (3 - 2 * fx); fy = fy * fy * (3 - 2 * fy)
    a = g[np.ix_(y0, x0)]; b = g[np.ix_(y0, x1)]; c = g[np.ix_(y1, x0)]; d = g[np.ix_(y1, x1)]
    top = a + (b - a) * fx[None, :]; bot = c + (d - c) * fx[None, :]
    return top + (bot - top) * fy[:, None]

def fbm(w, h, seed, scale=1.0, octs=((3, .5), (6, .3), (12, .15), (24, .08))):
    n = np.zeros((h, w)); tot = 0
    for i, (g, wt) in enumerate(octs):
        gx = max(1, int(round(g * scale * w / T))); gy = max(1, int(round(g * scale * h / T)))
        n += wt * vnoise(w, h, gx, gy, int(seed) * 131 + i); tot += wt
    n /= tot
    lo, hi = n.min(), n.max()
    return (n - lo) / (hi - lo + 1e-9)

def tex(w, h, rp, seed, scale=1.0, dither=0.10, gain=1.0, bias=0.0):
    n = fbm(w, h, seed, scale)
    n = np.clip((n - .5) * gain + .5 + bias, 0, .999)
    return quant(n, rp, dither)

# morphology
def dil(m, n=1):
    for _ in range(n):
        o = m.copy(); o[1:, :] |= m[:-1, :]; o[:-1, :] |= m[1:, :]; o[:, 1:] |= m[:, :-1]; o[:, :-1] |= m[:, 1:]; m = o
    return m
def ero(m, n=1, edge=True):
    p = np.pad(m, n, mode='edge' if edge else 'constant')
    e = ~dil(~p, n)
    return e[n:-n, n:-n]
def shift(m, dx, dy, edge=False):
    h, w = m.shape; pad = max(abs(dx), abs(dy)) + 1
    p = np.pad(m, pad, mode='edge' if edge else 'constant')
    return p[pad - dy:pad - dy + h, pad - dx:pad - dx + w]

# ---------------------------------------------------------------- canvas
class S:
    def __init__(s, w, h, wrap=False):
        s.w, s.h, s.wrap = w, h, wrap
        s.im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); s.d = ImageDraw.Draw(s.im, 'RGBA')
    def setim(s, im): s.im = im.convert('RGBA'); s.d = ImageDraw.Draw(s.im, 'RGBA'); return s
    def _o(s): return [(dx, dy) for dx in (-s.w, 0, s.w) for dy in (-s.h, 0, s.h)] if s.wrap else [(0, 0)]
    def _dr(s, c, fn):
        c = C(c)
        if c[3] == 255:
            fn(s.d, c)
        else:
            lay = Image.new('RGBA', (s.w, s.h), (0, 0, 0, 0)); fn(ImageDraw.Draw(lay), c); s.im.alpha_composite(lay)
    def r(s, x0, y0, x1, y1, c):
        s._dr(c, lambda d, c_: [d.rectangle([x0 + dx, y0 + dy, x1 + dx, y1 + dy], fill=c_) for dx, dy in s._o()])
    def rr(s, x0, y0, x1, y1, c, rad=3):
        s._dr(c, lambda d, c_: [d.rounded_rectangle([x0 + dx, y0 + dy, x1 + dx, y1 + dy], radius=rad, fill=c_) for dx, dy in s._o()])
    def l(s, pts, c, w=1):
        s._dr(c, lambda d, c_: [d.line([(x + dx, y + dy) for x, y in pts], fill=c_, width=w) for dx, dy in s._o()])
    def e(s, x0, y0, x1, y1, c):
        s._dr(c, lambda d, c_: [d.ellipse([x0 + dx, y0 + dy, x1 + dx, y1 + dy], fill=c_) for dx, dy in s._o()])
    def p(s, pts, c):
        s._dr(c, lambda d, c_: [d.polygon([(x + dx, y + dy) for x, y in pts], fill=c_) for dx, dy in s._o()])
    def pt(s, x, y, c):
        s._dr(c, lambda d, c_: [d.point((x + dx, y + dy), fill=c_) for dx, dy in s._o()])
    def circ(s, cx, cy, r, c): s.e(cx - r, cy - r, cx + r, cy + r, c)
    def bev(s, x0, y0, x1, y1, mid, hi=None, lo=None):
        mid = C(mid); hi = C(hi) if hi else shd(mid, 1.35); lo = C(lo) if lo else shd(mid, 0.6)
        s.r(x0, y0, x1, y1, mid); s.r(x0, y0, x1, y0, hi); s.r(x0, y0, x0, y1, hi); s.r(x0, y1, x1, y1, lo); s.r(x1, y0, x1, y1, lo)
    def tx(s, x0, y0, x1, y1, rp, seed, **kw):
        t = tex(x1 - x0 + 1, y1 - y0 + 1, rp, seed, **kw); s.im.paste(t, (x0, y0))
    def mtx(s, fn, rp, seed, **kw):
        m = Image.new('L', (s.w, s.h), 0); fn(ImageDraw.Draw(m))
        t = tex(s.w, s.h, rp, seed, **kw); s.im.paste(t, (0, 0), m)
    def paste(s, im, x, y):
        if isinstance(im, S): im = im.im
        s.im.alpha_composite(im, (int(x), int(y)))
    def stain(s, seed, col, thr=.6, gain=6, maxa=.6, scale=1.0, levels=4, within=True):
        n = fbm(s.w, s.h, seed, scale)
        a = np.clip(np.round(np.clip((n - thr) * gain, 0, 1) * levels) / levels * maxa, 0, 1)
        arr = np.array(s.im).astype(np.float32)
        if within: a = a * (arr[..., 3] > 0)
        for i in range(3): arr[..., i] = arr[..., i] * (1 - a) + col[i] * a
        s.setim(Image.fromarray(arr.astype(np.uint8), 'RGBA'))
    def speck(s, seed, dens, cols):
        rng = np.random.default_rng(seed); arr = np.array(s.im)
        m = (rng.random((s.h, s.w)) < dens) & (arr[..., 3] > 0)
        idx = rng.integers(0, len(cols), (s.h, s.w))
        cc = np.array([C(c) for c in cols], dtype=np.uint8)[idx]
        arr[m, :3] = cc[m][:, :3]
        s.setim(Image.fromarray(arr, 'RGBA'))
    def crack(s, seed, x, y, steps, dark=(10, 8, 8), light=(140, 138, 120), branch=0.07, ang=None, hi=True):
        rng = np.random.default_rng(seed); a = rng.uniform(0, 6.28) if ang is None else ang
        for _ in range(steps):
            a += rng.normal(0, .45); x += math.cos(a); y += math.sin(a)
            for dx, dy in s._o():
                px_, py_ = int(x) % s.w if s.wrap else int(x), int(y) % s.h if s.wrap else int(y)
                if 0 <= px_ < s.w and 0 <= py_ < s.h and s.im.getpixel((px_, py_))[3] > 0:
                    s.im.putpixel((px_, py_), C(dark, 255))
                    if hi and 0 <= px_ + 1 < s.w and 0 <= py_ + 1 < s.h and rng.random() < .5 and s.im.getpixel((px_ + 1, py_ + 1))[3] > 0:
                        s.im.putpixel((px_ + 1, py_ + 1), tuple(int(v) for v in mix(s.im.getpixel((px_ + 1, py_ + 1)), light, .32)[:3]) + (255,))
                if not s.wrap: break
            if rng.random() < branch and steps > 6: s.crack(int(rng.integers(1 << 30)), x, y, steps // 3, dark, light, 0, a + rng.choice([-.9, .9]), hi)
    def blob(s, cx, cy, rx, ry, seed, c, rough=.3, pts=18):
        rng = np.random.default_rng(seed); ang = np.linspace(0, 2 * np.pi, pts, endpoint=False)
        rad = 1 + rough * (rng.random(pts) - .5) * 2; rad = (rad + np.roll(rad, 1)) / 2
        s.p([(cx + math.cos(a) * rx * r_, cy + math.sin(a) * ry * r_) for a, r_ in zip(ang, rad)], c)
    def text(s, x, y, t, c, size=8, jitter=0, seed=0):
        f = ImageFont.truetype(FONT, size); m = Image.new('L', (s.w, s.h), 0); dm = ImageDraw.Draw(m)
        rng = np.random.default_rng(seed); cx = x
        for ch in t:
            dm.text((cx, y + (int(rng.integers(-jitter, jitter + 1)) if jitter else 0)), ch, font=f, fill=255)
            cx += f.getlength(ch) + (int(rng.integers(0, 2)) if jitter else 0)
        m = m.point(lambda v: 255 if v > 110 else 0)
        s.im.paste(Image.new('RGBA', (s.w, s.h), C(c)), (0, 0), m)

def rot(im, deg):
    if isinstance(im, S): im = im.im
    k = int(deg) % 360
    if k == 90: return im.transpose(Image.ROTATE_90)
    if k == 180: return im.transpose(Image.ROTATE_180)
    if k == 270: return im.transpose(Image.ROTATE_270)
    if k == 0: return im.copy()
    return im.rotate(deg, expand=True, resample=Image.NEAREST)

def flipx(im): return (im.im if isinstance(im, S) else im).transpose(Image.FLIP_LEFT_RIGHT)

# ---------------------------------------------------------------- finalize: grunge, rim light (top-left), outline, drop shadow
def finalize(im, pad=5, outline=True, rim=True, shadow=True, grunge=0.0, seed=1, sd=(3, 4), sa=105, edge=False, ocol=OL):
    if isinstance(im, S): im = im.im
    if pad:
        big = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0)); big.alpha_composite(im, (pad, pad)); im = big
    a = np.array(im).astype(np.float32)
    al = a[..., 3] > 60
    rgb = a[..., :3]
    if grunge > 0:
        n = fbm(im.width, im.height, seed + 7, scale=1.8)
        dk = np.clip((n - .55) * 2.2, 0, 1) * grunge
        rgb = rgb * (1 - dk[..., None] * 0.6)
        rs = np.random.default_rng(seed).random(al.shape)
        rgb = np.where((rs < 0.03 * grunge * 4)[..., None], rgb * 0.78, rgb)
    if rim:
        up = ~shift(al, 0, 1, edge); lf = ~shift(al, 1, 0, edge); dn = ~shift(al, 0, -1, edge); rt = ~shift(al, -1, 0, edge)
        hi = al & (up | lf); lo = al & (dn | rt) & ~hi
        rgb = np.where(hi[..., None], np.minimum(255, rgb * 1.28 + 10), rgb)
        rgb = np.where(lo[..., None], rgb * 0.62, rgb)
    out = np.zeros_like(a); out[..., :3] = rgb; out[..., 3] = a[..., 3]
    full = al.copy()
    if outline:
        ol = dil(al) & ~al
        out[ol, :3] = ocol; out[ol, 3] = 255; full |= ol
    if shadow:
        s1 = shift(full, sd[0], sd[1], edge); s2 = dil(s1)
        sa_arr = np.where(s1 & ~full, sa, np.where(s2 & ~full, int(sa * .4), 0))
        sel = (out[..., 3] == 0) & (sa_arr > 0)
        out[sel, :3] = (5, 4, 6); out[sel, 3] = sa_arr[sel]
    return Image.fromarray(out.astype(np.uint8), 'RGBA')

# ---------------------------------------------------------------- sheet packer (x2 nearest upscale -> 182 px tiles)
ALL = []
class Sheet:
    def __init__(s, name): s.name = name; s.items = []; ALL.append(s)
    def add(s, name, im, **meta):
        if isinstance(im, S): im = im.im
        s.items.append((name, im.copy(), meta))
    def save(s, maxw=2048, gap=8, scale=2, cols=None):
        d = f'{OUT}/{s.name}'; os.makedirs(d, exist_ok=True)
        bigs = []
        for n, im, m in s.items:
            b = im.resize((im.width * scale, im.height * scale), Image.NEAREST); b.save(f'{d}/{n}.png'); bigs.append((n, b, m))
        pos = {}; x = y = rowh = 0; W = 0
        if cols:
            cw = max(b.width for _, b, _ in bigs) + gap; ch = max(b.height for _, b, _ in bigs) + gap
            for i, (n, b, m) in enumerate(bigs): pos[n] = ((i % cols) * cw, (i // cols) * ch)
            W = cols * cw; H = ((len(bigs) + cols - 1) // cols) * ch
        else:
            for n, b, m in bigs:
                if x + b.width > maxw: x = 0; y += rowh + gap; rowh = 0
                pos[n] = (x, y); x += b.width + gap; rowh = max(rowh, b.height); W = max(W, x)
            H = y + rowh + gap
        atlas = Image.new('RGBA', (max(W, 1), max(H, 1)), (0, 0, 0, 0))
        meta = {}
        for n, b, m in bigs:
            atlas.alpha_composite(b, pos[n])
            meta[n] = dict(x=pos[n][0], y=pos[n][1], w=b.width, h=b.height, art_w=b.width // scale, art_h=b.height // scale, **m)
        atlas.save(f'{OUT}/{s.name}_atlas.png'); json.dump(meta, open(f'{OUT}/{s.name}_atlas.json', 'w'), indent=1)
        return atlas
