import glob
from px import *
from PIL import ImageFilter

TS = 182
_cache = {}
def spr(name):
    if name not in _cache:
        fs = glob.glob(f'{OUT}/*/{name}.png')
        assert fs, name
        _cache[name] = Image.open(fs[0]).convert('RGBA')
    return _cache[name].copy()

def put(cv, name, x, y, anchor='c', rotate=0, flip=False, vflip=False, alpha=1.0):
    im = spr(name) if isinstance(name, str) else name
    if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
    if vflip: im = im.transpose(Image.FLIP_TOP_BOTTOM)
    if rotate:
        im = im.rotate(rotate, expand=True, resample=Image.NEAREST) if rotate % 90 else im.transpose({90: Image.ROTATE_90, 180: Image.ROTATE_180, 270: Image.ROTATE_270}[rotate % 360])
    if alpha < 1:
        a = np.array(im); a[..., 3] = (a[..., 3] * alpha).astype(np.uint8); im = Image.fromarray(a, 'RGBA')
    if anchor == 'c': x, y = x - im.width // 2, y - im.height // 2
    cv.alpha_composite(im, (int(x), int(y))) if (x >= 0 and y >= 0 and x < cv.width and y < cv.height and x + im.width <= cv.width and y + im.height <= cv.height) else paste_clip(cv, im, int(x), int(y))

def paste_clip(cv, im, x, y):
    x0, y0 = max(0, x), max(0, y); x1, y1 = min(cv.width, x + im.width), min(cv.height, y + im.height)
    if x1 <= x0 or y1 <= y0: return
    cv.alpha_composite(im.crop((x0 - x, y0 - y, x1 - x, y1 - y)), (x0, y0))

# ------------------------------------------------------------------ lighting
class Light:
    def __init__(s, W, H, ambient):
        s.W, s.H = W, H; s.L = np.zeros((H, W, 3), np.float32); s.L[:] = np.array(ambient, np.float32)
    def amb_rect(s, x0, y0, x1, y1, col, feather=60):
        m = Image.new('L', (s.W, s.H), 0); ImageDraw.Draw(m).rectangle([x0, y0, x1, y1], fill=255); m = np.array(m.filter(ImageFilter.GaussianBlur(feather))).astype(np.float32)[..., None] / 255
        s.L = s.L * (1 - m) + np.array(col, np.float32) * m
    def add(s, name, cx, cy, scale=1.0, rotate=0, k=1.0, tint=None, pivot=None, mask=None, flipv=False):
        im = spr(name) if isinstance(name, str) else name
        if flipv: im = im.transpose(Image.FLIP_TOP_BOTTOM)
        if scale != 1: im = im.resize((int(im.width * scale), int(im.height * scale)), Image.BILINEAR)
        px_, py_ = (im.width / 2, im.height / 2) if pivot is None else (pivot[0] * scale, pivot[1] * scale)
        if rotate:
            R = int(2 * max(im.width, im.height) + 4); big = Image.new('RGBA', (R, R), (0, 0, 0, 0)); big.paste(im, (int(R / 2 - px_), int(R / 2 - py_))); im = big.rotate(-rotate, resample=Image.BILINEAR); ox, oy = R / 2, R / 2
        else: ox, oy = px_, py_
        a = np.array(im).astype(np.float32); alpha = a[..., 3:4] / 255; col = a[..., :3] / 255
        if tint is not None: col = col * 0 + np.array(tint, np.float32) / 255
        c = col * alpha * k
        x0, y0 = int(cx - ox), int(cy - oy); h, w = c.shape[:2]
        sx0, sy0, sx1, sy1 = max(0, x0), max(0, y0), min(s.W, x0 + w), min(s.H, y0 + h)
        if sx1 <= sx0 or sy1 <= sy0: return
        add = c[sy0 - y0:sy1 - y0, sx0 - x0:sx1 - x0]
        if mask is not None: add = add * mask[sy0:sy1, sx0:sx1, None]
        s.L[sy0:sy1, sx0:sx1] += add

def region_mask(W, H, rects, feather=40):
    m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m)
    for r in rects: d.rectangle(r, fill=255)
    return np.array(m.filter(ImageFilter.GaussianBlur(feather))).astype(np.float32) / 255

def timestamp(img, text, pos, size=34, col=(238, 238, 238)):
    d = ImageDraw.Draw(img); f = ImageFont.truetype(FONT, size)
    d.text((pos[0] + 3, pos[1]), text, font=f, fill=(255, 40, 40, 150)); d.text((pos[0] - 3, pos[1]), text, font=f, fill=(40, 240, 255, 130)); d.text(pos, text, font=f, fill=col + (255,))

def postfx(base, L, fog=None, fogk=.35, seed=1, stamp=('OCT 31 1993', '02:47:19'), tracking=True):
    rng = np.random.default_rng(seed); img = base[..., :3].astype(np.float32) / 255
    lit = img * np.clip(L, 0, 1.35)
    bright = np.clip(lit - .62, 0, 1); bl = np.array(Image.fromarray((np.clip(bright, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(22))).astype(np.float32) / 255
    lit = lit + bl * .85
    if fog is not None:
        fa = fog[..., 3:4].astype(np.float32) / 255 * fogk; fc = np.array([.62, .68, .72], np.float32) * np.clip(L, .05, 1.1) * .9; lit = lit * (1 - fa) + fc * fa
    g = lit.mean(axis=2, keepdims=True); lit = g + (lit - g) * .8
    lit = np.clip(lit, 0, 1) ** 1.04 * np.array([.94, 1.0, 1.05], np.float32)
    H, W = lit.shape[:2]; xs = (np.abs(np.arange(W) - W / 2) / (W / 2)) ** 2; sh = 3
    r_ = np.roll(lit[..., 0], sh, axis=1); b_ = np.roll(lit[..., 2], -sh, axis=1); lit[..., 0] = lit[..., 0] * (1 - xs[None, :]) + r_ * xs[None, :]; lit[..., 2] = lit[..., 2] * (1 - xs[None, :]) + b_ * xs[None, :]
    if tracking:
        y0 = int(rng.integers(H // 2, H - 80)); bh = 14
        lit[y0:y0 + bh] = np.roll(lit[y0:y0 + bh], 16, axis=1) * 1.18 + .03
    lit += rng.normal(0, .028, (H, W, 1)).astype(np.float32); lit[1::2] *= .9
    out = Image.fromarray((np.clip(lit, 0, 1) * 255).astype(np.uint8), 'RGB').convert('RGBA')
    vg = np.array(Image.open(f'{OUT}/fx/fx_vignette_1920x1080.png')); vg[..., 3] = (vg[..., 3] * .72).astype(np.uint8); out.alpha_composite(Image.fromarray(vg, 'RGBA'))
    v = Image.open(f'{OUT}/fx/fx_vhs_overlay_960x540_{seed % 4}.png').resize((W, H), Image.NEAREST); out.alpha_composite(v)
    out.alpha_composite(Image.open(f'{OUT}/fx/fx_hud_rec_on.png'), (64, 44)); timestamp(out, stamp[0], (64, 100), 30); timestamp(out, stamp[1], (64, 138), 30)
    timestamp(out, 'PLAY >', (W - 240, 54), 30); out.alpha_composite(Image.open(f'{OUT}/fx/fx_hud_battery_3.png'), (W - 150, H - 84)); return out

def player(ang=0):
    s = S(30, 30); c = 15
    s.e(6, 9, 24, 21, '#22302e'); s.e(7, 10, 22, 17, '#2f4340'); s.l([(18, 13), (27, 12)], '#22302e', 3); s.l([(18, 18), (27, 18)], '#22302e', 3)
    s.bev(24, 9, 29, 21, '#444d56', '#8794a0', '#15191d'); s.circ(c, 15, 5, '#c8a888'); s.e(10, 10, 17, 16, '#2a1e18'); s.circ(c + 1, 15, 2, '#1a1210'); s.pt(26, 11, '#e03030')
    im = finalize(s.im, pad=3, grunge=.1, sd=(2, 3)); im = im.resize((im.width * 2, im.height * 2), Image.NEAREST); return im.rotate(-ang, expand=True, resample=Image.NEAREST)

def autotile_walls(cv, solid, cols, rows, doors_skip, style='wall_int'):
    def sol(c, r): return True if (c < 0 or r < 0 or c >= cols or r >= rows) else (c, r) in solid
    for (c, r) in sorted(solid):
        if (c, r) in doors_skip: continue
        m = (1 if sol(c, r - 1) else 0) | (2 if sol(c + 1, r) else 0) | (4 if sol(c, r + 1) else 0) | (8 if sol(c - 1, r) else 0)
        put(cv, f'{style}_{m:02d}', c * TS, r * TS, 'tl')

# ------------------------------------------------------------------ scene 1: ward corridor
def scene_ward():
    COLS, ROWS = 12, 7; cv = Image.new('RGBA', (COLS * TS, ROWS * TS), (0, 0, 0, 255)); rng = np.random.default_rng(5)
    def fl(c, r, n): put(cv, n, c * TS, r * TS, 'tl')
    for c in range(COLS):
        for r in range(ROWS):
            if r in (3, 4): fl(c, r, ['floor_lino_worn', 'floor_lino_b', 'floor_lino_peeled', 'floor_lino_a'][int(rng.integers(0, 4))])
            elif r in (2, 5): fl(c, r, 'floor_conc_a')
            elif r in (0, 1): fl(c, r, 'floor_padded_stained' if c < 3 else ('floor_parquet_rotted' if c < 7 else 'floor_parquet_b'))
            else: fl(c, r, 'floor_morgue_b' if c < 3 else ('floor_hex_b' if c < 7 else 'floor_quarry_greasy'))
    solid = set(); doors = {(1, 2): 'door_wood_h_closed', (5, 2): 'door_steel_h_open', (9, 2): 'door_wood_h_broken', (1, 5): 'window_barred_h', (4, 5): 'door_cell_h_closed', (6, 5): 'window_barred_h_broken', (8, 5): 'door_double_h_closed'}
    for c in range(COLS): solid.add((c, 2)); solid.add((c, 5))
    for r in (0, 1, 6):
        for c in (3, 7, 11): solid.add((c, r))
    skip = set(doors) | {(9, 5)}
    autotile_walls(cv, solid, COLS, ROWS, skip)
    # decals / floor-level
    P_ = lambda n, c, r, **k: put(cv, n, c * TS, r * TS, **k)
    P_('decal_blood_pool_b', 5.1, 1.35); P_('decal_blood_handprints', 1.6, 0.5); P_('decal_claw_scratches', 0.45, 0.8); P_('decal_spiral_scratch', 2.1, 1.3); P_('decal_blood_splatter_a', 6.1, 0.9)
    P_('decal_blood_footprints', 3.2, 3.85, rotate=90); P_('decal_blood_drag', 9.45, 3.55); P_('decay_puddle_b', 2.5, 3.5); P_('decal_text_dont_look_up', 5.6, 3.15); P_('decay_debris_plaster_a', 6.9, 4.35)
    P_('decal_chalk_body_a', 1.0, 4.15, rotate=90); P_('decal_evidence_marker_1', 0.35, 3.75); P_('decal_evidence_marker_2', 1.65, 3.6); P_('decay_papers_a', 2.9, 4.5); P_('decay_glass_shards_a', 6.45, 5.0); P_('decay_mold_a', 10.4, 3.2); P_('decal_text_get_out', 8.2, 6.5)
    # props
    P_('prop_straitjacket_floor', 1.2, 0.75); P_('prop_bed_strapped', 5.15, 0.85); P_('prop_chair_wood_2', 4.55, 1.45); P_('prop_doll_rag', 5.95, 0.55, rotate=20); P_('prop_shoe_single', 4.6, 0.35)
    P_('prop_bed_body_sheet', 9.1, 0.95); P_('prop_iv_stand', 9.9, 0.55); P_('prop_tv_cart', 8.45, 0.75); P_('prop_wheelchair', 4.2, 3.75, rotate=345); P_('prop_gurney_body', 8.1, 4.45, rotate=90)
    P_('prop_med_cart', 3.35, 4.4, rotate=12); P_('prop_chair_wood_1', 7.1, 3.4); P_('decay_pigeon_dead', 0.6, 4.6); P_('prop_autopsy_table_body', 1.5, 6.6); P_('prop_hydro_tub_covered', 5.2, 6.6, rotate=90); P_('prop_ect_table', 9.2, 6.7, rotate=90)
    P_('decay_cobweb_tl', 0.12, 0.12, anchor='tl'); P_('decay_cobweb_tr', 2.5, 0.12, anchor='tl'); P_('decay_cobweb_tl', 7.12, 0.12, anchor='tl')
    for (c, r), n in doors.items():
        put(cv, n, c * TS, r * TS, 'tl')
    # overhead
    P_('anim_lamp_neon_on', 2.1, 4.0); P_('anim_lamp_neon_half', 5.9, 4.0); P_('anim_lamp_neon_broken', 9.4, 4.0)
    ox, oy = 150, 120; base = cv.crop((ox, oy, ox + 1920, oy + 1080)); W, H = 1920, 1080
    # lighting
    Lg = Light(W, H, (.13, .155, .21)); S_ = lambda c, r: (c * TS - ox, r * TS - oy)
    Lg.amb_rect(*S_(0, 2.3), *S_(12, 5.7), (.30, .36, .43), 80)
    corr = region_mask(W, H, [(*S_(-1, 2.55), *S_(13, 5.45))], 30)
    pl = S_(3.1, 3.7); Lg.add('fx_flashlight_cone', pl[0], pl[1], 1.55, -3, 1.9, pivot=(18, 384), mask=np.clip(corr + region_mask(W, H, [(*S_(4.6, 0), *S_(6.4, 3.3))], 20) * .85, 0, 1))
    Lg.add('fx_light_cold_neon', *S_(2.1, 4.0), 2.4, 0, 1.35, mask=corr); Lg.add('fx_light_cold_neon', *S_(5.9, 4.0), 2.0, 0, .8, mask=corr)
    Lg.add('fx_cast_barred_window_moon', *S_(1.5, 4.0), 1.5, 0, 1.2, mask=corr, flipv=True); Lg.add('fx_light_red_emergency', *S_(11.4, 4.0), 2.6, 0, 1.4, mask=corr)
    room_c = region_mask(W, H, [(*S_(7.1, 0), *S_(10.95, 2.1))], 18); Lg.add('fx_tv_glow_1', *S_(8.45, 0.85), 2.6, 0, 1.6, mask=room_c)
    roomb = region_mask(W, H, [(*S_(3.1, 0), *S_(6.95, 2.2))], 18); Lg.add('fx_light_cold_neon', *S_(5.5, 2.4), 1.6, 0, .9, mask=roomb); Lg.add('fx_light_candle', *S_(5.15, 0.9), 1.0, 0, .0, mask=roomb)
    Lg.add('fx_light_radial_M', *S_(1.2, 0.8), 2.0, 0, .0)
    fog = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ft = spr('fx_fog_tile_512').resize((1024, 1024), Image.BILINEAR)
    for xx in range(-200, W, 1024):
        for yy in range(-300, H, 1024): fog.alpha_composite(ft, (xx, yy)) if xx >= 0 and yy >= 0 else paste_clip(fog, ft, xx, yy)
    fa = np.array(fog); fa[..., 3] = (fa[..., 3] * corr).astype(np.uint8)
    out = base.copy(); put(out, player(0), *S_(3.1, 3.7), 'c')
    return postfx(np.array(out), Lg.L, fa, .55, 2)

# ------------------------------------------------------------------ scene 2: front courtyard
def scene_courtyard():
    W, H = 1920, 1080; cv = Image.new('RGBA', (W, H), (0, 0, 0, 255)); rng = np.random.default_rng(11)
    gr = ['floor_grass_a', 'floor_grass_b', 'floor_grass_c', 'floor_grass_dead_a', 'floor_grass_leaves', 'floor_cemetery_grass']
    for c in range(-1, 12):
        for r in range(-1, 7):
            put(cv, gr[int(rng.integers(0, 6))], c * TS - 14, r * TS - 20, 'tl')
    for c in range(3, 8):
        for r in range(1, 5): put(cv, 'floor_pavers_mossy' if (c + r) % 3 == 0 else 'floor_pavers_a', c * TS - 14, r * TS - 20, 'tl')
    for c in range(-1, 12): put(cv, rot(spr('floor_asphalt_line_v'), 90), c * TS - 14, 5 * TS - 20, 'tl')
    for c in (1, 2, 8, 9): put(cv, 'floor_dirt_path_v', c * TS - 14 + 0, 3 * TS - 20 if False else 2 * TS - 20, 'tl') if False else None
    P_ = lambda n, x, y, **k: put(cv, n, x, y, **k)
    # fence + gate
    x = -20; i = 0
    while x < W + 100:
        if 770 < x < 1150: x += 182; continue
        n = ['fence_iron_h', 'fence_iron_broken_h', 'fence_iron_h', 'fence_iron_h', 'fence_iron_broken_h'][i % 5] if 300 < x < 1500 else 'fence_chain_h'
        put(cv, n, x, 858, 'tl'); x += 182 - 12 + 12; i += 1
    P_('gate_iron_open', 960, 898)
    P_('decal_blood_drag', 905, 700); P_('decal_blood_footprints', 1012, 740); P_('decal_blood_pool_c', 960, 650)
    for xx in (600, 1330): P_('decay_papers_b', xx, 800)
    # building
    P_('roof_wing_gable_h', 224 + 289, 150, 'c') if False else None
    put(cv, 'roof_wing_gable_h', 190, -14, 'tl'); put(cv, 'roof_wing_gable_h', 1150, -14, 'tl'); put(cv, 'roof_tower_pyramid', 960, 160, 'c')
    put(cv, 'roof_dormer', 520, 150, 'c'); put(cv, 'roof_dormer', 1400, 150, 'c'); put(cv, 'roof_dormer', 330, 150, 'c')
    put(cv, 'chimney_top_round', 700, 70, 'c'); put(cv, 'chimney_top_round', 1250, 60, 'c')
    # fountain & yard
    P_('fountain_angel_dry', 960, 560); P_('crow_a', 1010, 470); P_('crow_b', 1390, 850); P_('flagpole_torn_flag', 420, 420)
    P_('tree_elm_dead_a', 170, 360); P_('tree_elm_dead_c', 1760, 400); P_('tree_pine_dark_a', 130, 740); P_('tree_pine_dark_b', 1790, 700); P_('tree_oak_dark', 300, 560); P_('bush_dead', 600, 470); P_('bush_overgrown', 1330, 470)
    P_('streetlamp', 730, 560, rotate=0); P_('streetlamp', 1190, 560, flip=True)
    P_('vehicle_police_car_blue', 520, 975, rotate=90); P_('vehicle_ambulance_rear_open', 1500, 985, rotate=270); P_('prop_gurney', 1010, 990, rotate=20); P_('prop_iv_stand', 1080, 960)
    P_('cemetery_marker_07', 1500, 330); P_('cemetery_marker_13', 1580, 360)
    # lighting
    L = Light(W, H, (.30, .37, .52)); L.amb_rect(300, 150, 1620, 880, (.38, .46, .62), 200)
    L.add('fx_light_sodium_lamp', 790, 560, 2.0, 0, 1.5); L.add('fx_light_sodium_lamp', 1130, 560, 2.0, 0, 1.5)
    L.add('fx_light_police_blue', 560, 960, 1.9, 0, .8); L.add('fx_light_police_red', 380, 990, 1.4, 0, .45)
    L.add('fx_light_candle', 330, 160, 2.2, 0, .9, tint=(255, 190, 110)); L.add('fx_light_red_emergency', 1500, 920, 1.5, 0, .55)
    L.add('fx_flashlight_cone', 975, 800, 1.9, -90, 2.4, pivot=(18, 384))
    fog = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ft = spr('fx_fog_tile_512').resize((1024, 1024), Image.BILINEAR)
    for xx in (-100, 924):
        for yy in (-200, 824): paste_clip(fog, ft, xx, yy)
    fa = np.array(fog); yy_ = np.linspace(.35, 1, H)[:, None]; fa[..., 3] = (fa[..., 3] * yy_).astype(np.uint8)
    out = cv.copy(); put(out, player(270), 975, 800, 'c')
    return postfx(np.array(out), L.L, fa, .5, 3, ('OCT 31 1993', '02:31:08'))

def contact_sheet():
    names = ['tiles_floor_interior', 'tiles_floor_exterior', 'tiles_walls', 'tiles_doors_windows', 'props_medical', 'props_admin_furniture', 'props_patient_traces', 'decals_blood_marks', 'decay_props', 'items_90s', 'anim_frames', 'pickups', 'props_chapel', 'props_kitchen', 'props_tunnel', 'props_vegetation', 'props_landmarks_fences', 'props_cemetery', 'props_yard_camp', 'props_vehicles', 'props_roofs']
    return names

if __name__ == '__main__':
    a = scene_ward(); a.convert('RGB').save(f'{OUT}/PREVIEW_scene_ward_corridor.png'); print('ward ok')
    b = scene_courtyard(); b.convert('RGB').save(f'{OUT}/PREVIEW_scene_front_courtyard.png'); print('court ok')
