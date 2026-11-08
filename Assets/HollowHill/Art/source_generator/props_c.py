from px import *
from props_a import F, sheet_poly, chair_wood

def pew(seed=1, w=156):
    H = 34; s = S(w, H)
    s.bev(0, 0, w - 1, 8, '#3b271a', '#82603f', '#150e0a'); s.tx(2, 2, w - 3, 7, P['wood'], seed, scale=4, dither=.1)
    for i, y in enumerate((11, 16, 21)): s.bev(4, y, w - 5, y + 3, '#503523', '#82603f', '#150e0a'); s.r(5, y + 1, w - 6, y + 1, (255, 220, 170, 40))
    for x in (0, w - 7): s.bev(x, 0, x + 6, 28, '#2a1b12', '#68472f', '#0e0906'); s.r(x + 2, 3, x + 4, 24, (0, 0, 0, 60))
    s.bev(6, 27, w - 7, 32, '#35210f', '#68472f', '#0a0604'); s.stain(seed, (10, 8, 6), thr=.58, gain=5, maxa=.6, scale=1.6); return F(s)

def altar(seed=2):
    W, H = 78, 48; s = S(W, H); s.bev(0, 0, W - 1, H - 1, '#4e5250', '#9aa09d', '#1b1c1b'); s.tx(2, 2, W - 3, H - 3, P['stone'], seed, scale=2, dither=.12)
    s.bev(10, 6, W - 11, H - 8, '#aaa999', '#ececd8', '#5a594f'); s.r(10, 6, W - 11, 8, '#8a1a1a'); s.r(10, H - 10, W - 11, H - 8, '#8a1a1a')
    s.stain(seed + 1, (60, 40, 20), thr=.55, gain=5, maxa=.6, scale=1.8)
    for x in (16, W - 22):
        s.circ(x + 3, 14, 5, '#7a5719'); s.circ(x + 3, 14, 4, '#a67c28'); s.circ(x + 3, 14, 2, '#e4dfc2'); s.pt(x + 2, 13, '#fff2b0'); s.blob(x + 6, 18, 3, 2, x, (200, 196, 170, 255))
    s.circ(W // 2, 20, 5, '#a67c28'); s.circ(W // 2, 20, 3, '#cfa645'); s.circ(W // 2, 20, 1, '#4d3510')
    s.p([(26, 28), (42, 26), (43, 36), (27, 38)], '#b5af8f'); s.l([(34, 27), (35, 37)], '#4a4636'); s.l([(29, 30), (40, 29)], '#4a4636'); s.l([(29, 34), (41, 33)], '#4a4636')
    s.blob(W - 24, 32, 6, 4, 1, (96, 14, 16, 215)); return F(s, .35)

def piano(seed=3):
    W, H = 80, 38; s = S(W, H); s.bev(0, 0, W - 1, H - 1, '#15110e', '#4d4036', '#050403'); s.tx(2, 2, W - 3, H - 3, RP('#0a0807', '#14100d', '#1f1814', '#2c211a'), seed, scale=3, dither=.1)
    s.l([(4, 4), (W - 5, 4)], (255, 255, 255, 36)); s.r(2, 24, W - 3, 25, '#050403'); s.bev(8, 6, 32, 20, '#0a0807', '#3a2c22', '#000000'); s.p([(40, 8), (56, 6), (58, 18), (42, 20)], '#c6c0a0'); s.l([(44, 11), (54, 10)], '#4a3a2a'); s.l([(44, 14), (54, 13)], '#4a3a2a')
    s.circ(68, 14, 4, '#3a2a1a'); s.circ(68, 14, 2, '#6a1a1a'); s.l([(68, 12), (70, 6)], '#2a3a1a'); s.l([(68, 12), (65, 7)], '#2a3a1a'); s.stain(seed, (30, 28, 24), thr=.6, gain=6, maxa=.7, scale=1.5)
    s.crack(seed, 12, 30, 14, dark=(0, 0, 0), light=(90, 80, 70)); return F(s, .35)

def stool(seed=4):
    s = S(26, 26); s.circ(13, 13, 10, '#150e0a'); s.circ(13, 13, 9, '#35210f'); s.circ(12, 12, 6, '#4d3118'); s.circ(10, 10, 2, '#7a5a3a'); return F(s, .2)

def pulpit(seed=5):
    s = S(34, 34); s.mtx(lambda d: d.polygon([(10, 1), (23, 1), (32, 10), (32, 23), (23, 32), (10, 32), (1, 23), (1, 10)], fill=255), P['wood'], seed, scale=2.2, dither=.12)
    s.p([(10, 10), (22, 8), (24, 20), (11, 22)], '#d3cdac'); s.l([(16, 9), (17, 21)], '#4a4636'); s.l([(11, 13), (15, 13)], '#4a4636'); s.l([(18, 13), (22, 13)], '#4a4636'); s.circ(26, 25, 2, '#a67c28'); return F(s, .3)

def candelabra(lit=False, seed=6):
    s = S(26, 26); c = 13; s.circ(c, c, 9, '#15191d'); s.circ(c, c, 8, '#2e353c'); s.l([(c, c), (c, c)], '#444d56')
    for k in range(5):
        a = k * 1.2566 - 1.57; x = int(c + math.cos(a) * 7); y = int(c + math.sin(a) * 7); s.circ(x, y, 2, '#d6d0b0'); s.pt(x - 1, y - 1, '#ffffff'); s.circ(x, y, 1, '#ffd070' if lit else '#4a4636')
    s.circ(c, c, 2, '#7a5719'); return F(s, .2)

# ----------------------------------------------------------------- kitchen
def table_long(seed=7, w=188):
    H = 52; s = S(w, H); s.bev(0, 0, w - 1, H - 1, '#6f7c87', '#c3ced6', '#2e353c'); s.tx(3, 3, w - 4, H - 4, P['steel'], seed, scale=4, dither=.1, gain=.8)
    for i in range(6): x = 8 + i * 30; s.bev(x, 8, x + 22, 22, '#98a6b1', '#e8eef2', '#3c454c'); s.r(x + 3, 11, x + 19, 19, '#444d56' if i % 2 else '#2a3a2a'); s.l([(x + 4, 13), (x + 10, 13)], '#c6b898') if i % 3 == 0 else None
    for x, y in ((24, 36), (70, 38), (122, 36), (158, 40)): s.circ(x, y, 6, '#8794a0'); s.circ(x, y, 5, '#3c454c'); s.circ(x, y, 3, '#1a2024' if x != 122 else '#4a1a1a')
    s.l([(90, 32), (104, 44)], '#c3ced6', 2); s.circ(88, 31, 3, '#8794a0'); s.stain(seed + 1, (56, 12, 10), thr=.66, gain=7, maxa=.6, scale=2.2); return F(s)

def stove(seed=8):
    W, H = 88, 58; s = S(W, H); s.bev(0, 0, W - 1, H - 1, '#23282d', '#5f6b76', '#08090a'); s.tx(2, 2, W - 3, H - 3, P['metal'], seed, scale=2.5, dither=.1)
    for x in (4, 26, 48, 70):
        for y in (6, 28): s.circ(x + 7, y + 7, 9, '#08090a'); s.circ(x + 7, y + 7, 7, '#15191d'); s.circ(x + 7, y + 7, 3, '#4a1a0a')
        for y in (6, 28): s.l([(x - 2, y + 7), (x + 16, y + 7)], '#444d56'); s.l([(x + 7, y - 2), (x + 7, y + 16)], '#444d56')
    for x in range(6, W - 6, 11): s.circ(x, 52, 2, '#98a6b1'); s.pt(x - 1, 51, '#ffffff')
    s.circ(26, 20, 8, '#444d56'); s.circ(26, 20, 6, '#6f7c87'); s.circ(26, 20, 2, '#15191d'); s.stain(seed + 2, (60, 30, 10), thr=.55, gain=6, maxa=.65, scale=2); return F(s, .4)

def pot(open_=False, seed=9):
    s = S(34, 34); s.circ(16, 16, 15, '#2e353c'); s.circ(16, 16, 14, '#6f7c87'); s.bev(0, 14, 4, 20, '#2e353c', '#98a6b1', '#08090a'); s.bev(28, 14, 32, 20, '#2e353c', '#98a6b1', '#08090a')
    if open_: s.circ(16, 16, 11, '#2e353c'); s.circ(16, 16, 10, '#4a4a3a'); s.blob(16, 16, 7, 6, seed, (70, 66, 48, 255)); s.l([(10, 12), (16, 10)], (190, 190, 160, 100)); s.pt(18, 18, '#8a1a1a')
    else: s.circ(16, 16, 12, '#98a6b1'); s.circ(15, 15, 8, '#8794a0'); s.circ(16, 16, 2, '#15191d'); s.l([(7, 8), (12, 5)], (255, 255, 255, 120))
    return F(s, .3)

def prep_table(seed=10):
    W, H = 108, 50; s = S(W, H); s.bev(0, 0, W - 1, H - 1, '#6f7c87', '#c3ced6', '#2e353c'); s.tx(3, 3, W - 4, H - 4, P['steel'], seed, scale=3, dither=.1)
    s.bev(10, 8, 44, 40, '#503523', '#82603f', '#150e0a'); s.tx(12, 10, 42, 38, P['wood'], seed + 1, scale=2); s.l([(16, 14), (38, 30)], '#3a1a1a', 2)
    s.p([(54, 14), (74, 12), (76, 20), (56, 22)], '#c3ced6'); s.l([(54, 14), (74, 12)], '#ffffff'); s.r(74, 13, 84, 18, '#35210f')
    s.blob(30, 24, 8, 6, 2, (96, 14, 16, 225)); s.blob(64, 36, 6, 4, 3, (96, 14, 16, 215)); s.stain(seed + 3, (70, 14, 12), thr=.64, gain=7, maxa=.55, scale=2.2); return F(s)

def sink(seed=11):
    W, H = 78, 42; s = S(W, H); s.bev(0, 0, W - 1, H - 1, '#6f7c87', '#c3ced6', '#2e353c')
    for x in (5, 41): s.bev(x, 6, x + 31, 36, '#3c454c', '#98a6b1', '#1d2227'); s.tx(x + 3, 9, x + 28, 33, P['water'], seed + x, scale=2.4, dither=.15); s.circ(x + 15, 21, 2, '#050607')
    s.circ(39, 3, 4, '#8794a0'); s.l([(39, 3), (39, 14)], '#6f7c87', 3); s.blob(52, 24, 5, 3, 2, (60, 14, 12, 150)); return F(s)

# ----------------------------------------------------------------- tunnel
def pipes(seed=12, variant=0):
    W, H = 188, 38; s = S(W, H); y = 3
    specs = [('#4a2a14', '#85441f', '#2a130a'), ('#4e6150', '#7f957f', '#1c2620'), ('#a59f80', '#d6d0b0', '#5a5642')] if variant == 0 else [('#85441f', '#a5602d', '#2a130a'), ('#a59f80', '#d6d0b0', '#5a5642'), ('#444d56', '#8794a0', '#15191d')]
    for i, (m, hi, lo) in enumerate(specs):
        h = 9 + (i == 1) * 2; s.r(0, y, W - 1, y + h - 1, lo); s.r(0, y + 1, W - 1, y + h - 3, m); s.r(0, y + 1, W - 1, y + 2, hi); s.pt(5, y + 1, '#ffffff')
        if 'a59f80' in m:
            for x in range(4, W, 8): s.l([(x, y + 1), (x + 3, y + h - 2)], (60, 56, 40, 130))
        y += h + 2
    for x in (22, 70, 118, 164): s.bev(x, 1, x + 6, H - 2, '#2e353c', '#8794a0', '#08090a'); [s.pt(x + 3, yy, '#c3ced6') for yy in (6, 18, 30)]
    s.blob(96, 30, 4, 3, seed, (24, 43, 52, 200)); s.stain(seed + 1, (90, 46, 20), thr=.58, gain=6, maxa=.6, scale=2.2); return F(s, .4)

def valve(seed=13):
    s = S(34, 34); s.r(15, 2, 19, 32, '#2e353c'); s.r(15, 2, 15, 32, '#8794a0'); s.circ(17, 17, 13, '#7a1a1a'); s.circ(17, 17, 10, (0, 0, 0, 0))
    for k in range(6): a = k * 1.047; s.l([(17, 17), (17 + math.cos(a) * 12, 17 + math.sin(a) * 12)], '#8a2a2a', 2)
    s.circ(17, 17, 12, '#7a1a1a'); s.circ(17, 17, 9, (0, 0, 0, 0)); s.circ(17, 17, 3, '#2e353c'); s.pt(16, 16, '#c3ced6'); s.stain(seed, (80, 40, 16), thr=.6, gain=6, maxa=.5, scale=2.5); return F(s)

def vent(frame, seed=14):
    s = S(44, 60); s.bev(2, 28, 41, 57, '#23282d', '#5f6b76', '#050607')
    for y in range(32, 54, 5): s.r(6, y, 37, y + 2, '#050607'); s.r(6, y, 37, y, '#444d56')
    rng = np.random.default_rng(seed); out = finalize(s.im, pad=2, grunge=.3, sd=(2, 3)); st = S(out.width, out.height)
    for k in range(7):
        t = ((frame / 4) + k / 7) % 1; y = 50 - t * 44; r_ = 3 + t * 7; a = int(150 * (1 - t) ** 1.2); x = 22 + math.sin(k * 2 + frame) * 5 * t
        st.e(int(x - r_), int(y - r_), int(x + r_), int(y + r_), (215, 225, 225, a))
    out.alpha_composite(st.im); return out

def trolley(body=False, seed=15):
    W, H = 46, 70; s = S(W, H); s.bev(3, 0, W - 4, H - 1, '#444d56', '#8794a0', '#15191d'); s.tx(5, 2, W - 6, H - 3, P['metal'], seed, scale=2)
    for y in (10, 35, 60): s.r(5, y, W - 6, y, '#15191d')
    for y in (6, H - 12): s.bev(0, y, 3, y + 6, '#15191d', '#444d56', '#050607'); s.bev(W - 4, y, W - 1, y + 6, '#15191d', '#444d56', '#050607')
    s.stain(seed, (100, 50, 20), thr=.5, gain=5, maxa=.65, scale=2)
    if body: sheet_poly(s, [(13, 8), (22, 4), (31, 8), (32, 18), (36, 26), (36, 48), (32, 62), (24, 66), (14, 62), (10, 48), (10, 26), (14, 18)], seed); s.blob(24, 30, 5, 6, 2, (92, 14, 16, 190))
    return F(s)

def rails(seed=16):
    s = S(T, T); rng = np.random.default_rng(seed)
    for y in range(4, T, 14): s.bev(14, y, 76, y + 5, '#2a1e18', '#53402f', '#0e0a08'); s.tx(15, y + 1, 75, y + 4, P['bark'], seed + y, scale=3)
    for x in (24, 60): s.r(x, 0, x + 4, T - 1, '#15191d'); s.r(x + 1, 0, x + 3, T - 1, '#6b7782'); s.r(x + 1, 0, x + 1, T - 1, '#c3ced6'); s.r(x + 4, 0, x + 4, T - 1, '#08090a')
    for y in range(8, T, 14):
        for x in (23, 59): s.pt(x, y, '#8a8a7a')
    s.stain(seed, (100, 56, 24), thr=.62, gain=7, maxa=.5, scale=2.4); return finalize(s.im, pad=0, outline=False, rim=False, sd=(2, 3), sa=90, edge=True)

def build(ch, ki, tu):
    ch.add('prop_pew', pew()); ch.add('prop_altar', altar()); ch.add('prop_piano_upright', piano()); ch.add('prop_piano_stool', stool()); ch.add('prop_pulpit', pulpit()); ch.add('prop_candelabra_unlit', candelabra(False)); ch.add('prop_candelabra_lit', candelabra(True))
    ki.add('prop_table_long_steel', table_long()); ki.add('prop_stove_industrial', stove()); ki.add('prop_pot_big_closed', pot(False)); ki.add('prop_pot_big_open', pot(True)); ki.add('prop_prep_table_bloody', prep_table()); ki.add('prop_sink_double', sink())
    ki.add('prop_chair_overturned', F(rot(chair_wood(27, 0), 0).rotate(62, expand=True, resample=Image.NEAREST) if False else chair_wood(27, 62)))
    tu.add('tunnel_pipes_a', pipes(12, 0)); tu.add('tunnel_pipes_b', pipes(13, 1)); tu.add('tunnel_valve_wheel', valve()); tu.add('tunnel_trolley', trolley()); tu.add('tunnel_trolley_body', trolley(True))
    for k in range(4): tu.add(f'anim_steam_vent_{k}', vent(k))
    r = rails(); tu.add('tunnel_rails_v', r); tu.add('tunnel_rails_h', rot(r, 90))

if __name__ == '__main__':
    sh = [Sheet(n) for n in ('props_chapel', 'props_kitchen', 'props_tunnel')]
    build(*sh)
    for x in sh: x.save()
