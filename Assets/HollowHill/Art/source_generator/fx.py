from px import *
from PIL import ImageFilter
D = f'{OUT}/fx'

def save(name, im):
    os.makedirs(D, exist_ok=True); im.save(f'{D}/{name}.png'); return im

def lightmap(a, col):
    arr = np.zeros(a.shape + (4,), np.uint8); arr[..., :3] = col; arr[..., 3] = np.clip(a * 255, 0, 255).astype(np.uint8); return Image.fromarray(arr, 'RGBA')

def flashlight(size=768, half=.40, reach=0.92):
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32); ax, ay = 18, size / 2
    dx, dy = xx - ax, yy - ay; dist = np.sqrt(dx * dx + dy * dy); ang = np.abs(np.arctan2(dy, np.maximum(dx, .001)))
    angular = np.clip(1 - (ang / half) ** 2.4, 0, 1); radial = np.clip(1 - dist / (size * reach), 0, 1) ** 1.35
    core = np.exp(-(dist / 46) ** 2) * .85; a = np.clip(angular * radial * 1.0 + core, 0, 1)
    a += (np.random.default_rng(3).random(a.shape) - .5) * .018
    return lightmap(np.clip(a, 0, 1), (255, 244, 214))

def radial(size, col, power=2.0, peak=1.0):
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32); d = np.sqrt((xx - size / 2) ** 2 + (yy - size / 2) ** 2) / (size / 2)
    return lightmap(np.clip(1 - d, 0, 1) ** power * peak, col)

def barred_cast(w=200, h=300, col=(170, 200, 255)):
    m = Image.new('L', (w + 120, h), 0); d = ImageDraw.Draw(m)
    d.polygon([(30, 10), (30 + w - 40, 10), (w + 100, h - 20), (90, h - 20)], fill=255)
    for k in range(1, 5):
        x0 = 30 + k * (w - 40) // 5; d.polygon([(x0 - 5, 10), (x0 + 5, 10), (x0 + 5 + (w + 70 - (w - 40)) * .5, h - 20), (x0 - 5 + 60 + 20, h - 20)], fill=0)
    d.polygon([(40, h * .42), (w + 90, h * .42), (w + 96, h * .42 + 12), (46, h * .42 + 12)], fill=0)
    m = m.filter(ImageFilter.GaussianBlur(2.5)); a = np.array(m).astype(np.float32) / 255; yy = np.linspace(1, .35, a.shape[0])[:, None]
    return lightmap(a * .75 * yy, col)

def stained_cast(size=320):
    m = Image.new('RGBA', (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(m); cols = [(200, 50, 50), (60, 90, 210), (220, 170, 50), (60, 160, 90), (170, 60, 160)]
    cx, w = size // 2, 90; rng = np.random.default_rng(4)
    arch = [(cx - w, size - 20), (cx - w, 120)] + [(cx + math.cos(t) * w, 120 - math.sin(t) * 90) for t in np.linspace(math.pi, 0, 18)] + [(cx + w, size - 20)]
    mask = Image.new('L', (size, size), 0); ImageDraw.Draw(mask).polygon(arch, fill=255)
    pan = Image.new('RGBA', (size, size), (0, 0, 0, 0)); dp = ImageDraw.Draw(pan)
    for gy in range(0, size, 40):
        for gx in range(cx - w, cx + w, 36): dp.rectangle([gx, 30 + gy, gx + 35, 30 + gy + 39], fill=cols[int(rng.integers(0, 5))] + (190,)); dp.rectangle([gx, 30 + gy, gx + 35, 30 + gy + 39], outline=(0, 0, 0, 255), width=3)
    dp.line([(cx, 30), (cx, size)], fill=(0, 0, 0, 255), width=5); out = Image.new('RGBA', (size, size), (0, 0, 0, 0)); out.paste(pan, (0, 0), mask)
    out = out.transform((size, size), Image.AFFINE, (1, .35, -40, 0, 1, 0), resample=Image.BILINEAR).filter(ImageFilter.GaussianBlur(2.2)); a = np.array(out).astype(np.float32); a[..., 3] *= .8; return Image.fromarray(a.astype(np.uint8), 'RGBA')

def vignette(w=1920, h=1080, strength=.88):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32); d = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    a = np.clip((d - .5) / .75, 0, 1) ** 1.7 * strength; arr = np.zeros((h, w, 4), np.uint8); arr[..., 3] = (a * 255).astype(np.uint8); return Image.fromarray(arr, 'RGBA')

def blood_vignette(w=1920, h=1080):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32); d = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    n = fbm(w // 4, h // 4, 7, 2); n = np.array(Image.fromarray((n * 255).astype(np.uint8)).resize((w, h), Image.BILINEAR)) / 255.
    a = np.clip((d - .55) / .6 + (n - .5) * .35, 0, 1) ** 1.4; arr = np.zeros((h, w, 4), np.uint8); arr[..., :3] = (120, 8, 10); arr[..., 3] = (a * 210).astype(np.uint8); return Image.fromarray(arr, 'RGBA')

def vhs_frame(seed, w=960, h=540):
    rng = np.random.default_rng(seed); arr = np.zeros((h, w, 4), np.uint8)
    n = rng.random((h, w)); arr[..., :3] = (180 + n[..., None] * 60).astype(np.uint8); arr[..., 3] = (n * 26).astype(np.uint8)
    arr[::2, :, 3] = np.minimum(255, arr[::2, :, 3].astype(int) + 0); arr[1::2, :, :3] = 0; arr[1::2, :, 3] = np.maximum(arr[1::2, :, 3], 30)
    y0 = int(rng.integers(40, h - 80)); bh = int(rng.integers(8, 22)); band = rng.random((bh, w)); arr[y0:y0 + bh, :, :3] = (200 + band[..., None] * 55).astype(np.uint8); arr[y0:y0 + bh, :, 3] = (6 + band * 22).astype(np.uint8)
    for k in range(int(rng.integers(0, 4))): yy = int(rng.integers(0, h)); x0 = int(rng.integers(0, w - 200)); arr[yy, x0:x0 + int(rng.integers(40, 200)), :] = (255, 255, 255, 46)
    return Image.fromarray(arr, 'RGBA')

def fog_tile(size=512, seed=9, mx=110):
    n = fbm(size, size, seed, 1.6); n2 = fbm(size, size, seed + 1, 3.2); v = np.clip((n * .7 + n2 * .3 - .32) * 2.0, 0, 1)
    arr = np.zeros((size, size, 4), np.uint8); arr[..., :3] = (196, 208, 214); arr[..., 3] = (v * mx).astype(np.uint8); return Image.fromarray(arr, 'RGBA')

def dust(i):
    s = 8 + (i % 3) * 3; yy, xx = np.mgrid[0:s, 0:s].astype(np.float32); d = np.sqrt((xx - s / 2 + .5) ** 2 + (yy - s / 2 + .5) ** 2) / (s / 2)
    return lightmap(np.clip(1 - d, 0, 1) ** (1.5 + i * .2) * (.5 + .08 * i), (230, 230, 214))

def tvglow(k, size=260):
    base = radial(size, (150, 190, 255), 1.7, .8); a = np.array(base).astype(np.float32); rng = np.random.default_rng(k)
    yy = np.arange(size)[:, None]; a[..., 3] *= (.7 + .3 * np.sin(yy / 5.0 + k * 1.7)) * (.8 + .2 * rng.random((size, 1))); return Image.fromarray(a.astype(np.uint8), 'RGBA')

def hud(rec=True, w=300, h=44):
    s = S(w, h)
    if rec: s.circ(18, 22, 9, '#e02020'); s.circ(15, 19, 3, '#ff8080')
    f = ImageFont.truetype(FONT, 30); d = ImageDraw.Draw(s.im); d.text((40, 3), 'REC', font=f, fill=(235, 235, 235, 255)); d.text((124, 3), '● SP', font=ImageFont.truetype(FONT, 20), fill=(235, 235, 235, 0))
    return s.im

def battery_icon(level):
    s = S(76, 34); s.d.rectangle([1, 4, 62, 29], outline=(235, 235, 235, 255), width=3); s.r(64, 12, 71, 21, (235, 235, 235, 255))
    for k in range(4):
        if k < level: s.r(6 + k * 14, 9, 17 + k * 14, 24, (235, 235, 235, 255) if level > 1 else (230, 40, 40, 255))
    return s.im

def build():
    save('fx_flashlight_cone', flashlight()); save('fx_flashlight_cone_narrow', flashlight(768, .22, .98)); save('fx_flashlight_cone_wide', flashlight(768, .62, .8))
    for n, size, col in (('S', 128, (255, 244, 214)), ('M', 256, (255, 244, 214)), ('L', 512, (255, 244, 214))): save(f'fx_light_radial_{n}', radial(size, col, 2.0))
    save('fx_light_sodium_lamp', radial(512, (255, 168, 72), 1.8, .95)); save('fx_light_cold_neon', radial(384, (190, 228, 255), 1.9, .95)); save('fx_light_red_emergency', radial(384, (255, 38, 28), 1.8, .95))
    save('fx_light_police_red', radial(420, (255, 40, 40), 1.6, .9)); save('fx_light_police_blue', radial(420, (60, 90, 255), 1.6, .9)); save('fx_light_candle', radial(200, (255, 170, 80), 2.2, .9))
    save('fx_cast_barred_window_moon', barred_cast()); save('fx_cast_stained_glass', stained_cast())
    for k in range(4): save(f'fx_tv_glow_{k}', tvglow(k))
    save('fx_vignette_1920x1080', vignette()); save('fx_vignette_damage_1920x1080', blood_vignette())
    for k in range(4): save(f'fx_vhs_overlay_960x540_{k}', vhs_frame(k))
    save('fx_fog_tile_512', fog_tile()); save('fx_fog_tile_512_b', fog_tile(512, 21, 80))
    for i in range(6): save(f'fx_dust_particle_{i}', dust(i))
    save('fx_hud_rec_on', hud(True)); save('fx_hud_rec_off', hud(False))
    for lv in range(5): save(f'fx_hud_battery_{lv}', battery_icon(lv))

if __name__ == '__main__':
    build()
