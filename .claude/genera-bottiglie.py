#!/usr/bin/env python3
"""Genera per ogni prodotto: profilo 3D (dalla foto frontale) + texture
'srotolata' (fronte + retro) per la scheda prodotto 3D.
Output: assets/prodotti/3d/<slug>.jpg  +  assets/prodotti/3d/bottiglie.js
"""
import json, math, os, sys
import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB = os.path.join(ROOT, 'assets/prodotti/web')
OUT = os.path.join(ROOT, 'assets/prodotti/3d')

PRODOTTI = {  # slug: (fronte, retro)
    'vasia-rosso': ('vasia-rosso', 'vasia-rosso-retro'),
    'kalanero': ('kalanero', None),
    'primula-rosso': ('primula-rosso', 'primula-rosso-retro'),
    'dalia-rosso': ('dalia-rosso', 'dalia-rosso-retro'),
    'calasulu-rosso': ('calasulu-rosso', 'calasulu-rosso-retro'),
    'mareme-bianco': ('mareme-bianco', 'mareme-bianco-retro'),
    'primula-bianco': ('primula-bianco', 'primula-bianco-retro'),
    'dalia-bianco': ('dalia-bianco', 'dalia-bianco-retro'),
    'calasulu-bianco': ('calasulu-bianco', 'calasulu-bianco-retro'),
    'murmuro-rosato': ('murmuro-rosato', 'murmuro-rosato-retro'),
    'primula-rosato': ('primula-rosato', 'primula-rosato-retro'),
    'dalia-rosato': ('dalia-rosato', 'dalia-rosato-retro'),
    'calasulu-rosato': ('calasulu-rosato', 'calasulu-rosato-retro'),
    'amaro-korva': ('amaro-korva', 'amaro-korva-retro-1'),
}

N_ROWS = 160          # punti del profilo
TEX_W, TEX_H = 1024, 1024


def silhouette(path):
    im = np.asarray(Image.open(path).convert('RGB')).astype(np.float32)
    h, w, _ = im.shape
    # sfondo stimato riga per riga dai bordi (gestisce anche sfondi sfumati)
    bg = np.concatenate([im[:, 4:16], im[:, -16:-4]], axis=1).mean(axis=1, keepdims=True)
    diff = np.abs(im - bg).max(axis=2)
    sat = im.max(axis=2) - im.min(axis=2)
    pulito = bg.mean() > 248          # fondo bianco scontornato
    fg = (diff > (9 if pulito else 24)) | (sat > (20 if pulito else 30))
    # le etichette bianche sono "uguali" allo sfondo: si prende il pixel
    # più a sinistra / più a destra della riga (cornici grigie escluse)
    fg[:, :6] = False; fg[:, -6:] = False
    fg[:3] = False; fg[-3:] = False
    rows = []
    for y in range(h):
        xs = np.nonzero(fg[y])[0]
        rows.append((xs[0], xs[-1]) if len(xs) >= 3 else None)
    ys = [y for y, r in enumerate(rows) if r and r[1] - r[0] > 6]
    top, bot = ys[0], ys[-1]
    body = [rows[y] for y in range(top + (bot - top) // 2, bot - (bot - top) // 10) if rows[y]]
    cx = float(np.median([(a + b) / 2 for a, b in body]))
    rad = np.zeros(h)
    for y in range(top, bot + 1):
        r = rows[y]
        if r:
            rad[y] = min(cx - r[0], r[1] - cx) + 0.5  # lato più stretto = niente ombre/riflessi
    # riempi buchi + mediana
    for y in range(top, bot + 1):
        if rad[y] <= 0:
            rad[y] = rad[y - 1]
    k = 7
    sm = rad.copy()
    for y in range(top, bot + 1):
        sm[y] = np.median(rad[max(top, y - k):min(bot, y + k) + 1])
    # chiusura morfologica 1D: riempie i "buchi" (capsule bianche su fondo bianco)
    seg = sm[top:bot + 1]
    n = 22
    dil = np.array([seg[max(0, i - n):i + n + 1].max() for i in range(len(seg))])
    clo = np.array([dil[max(0, i - n):i + n + 1].min() for i in range(len(seg))])
    clo = np.maximum(seg, clo)
    # leggera gaussiana per togliere le irregolarità dei riflessi
    g = np.exp(-0.5 * (np.arange(-6, 7) / 2.2) ** 2); g /= g.sum()
    pad = np.pad(clo, 6, mode='edge')
    sm[top:bot + 1] = np.convolve(pad, g, mode='valid')
    return im, cx, top, bot, sm


def sample(im, xs, ys):
    h, w, _ = im.shape
    xs = np.clip(xs, 0, w - 1.001); ys = np.clip(ys, 0, h - 1.001)
    x0 = xs.astype(int); y0 = ys.astype(int); fx = xs - x0; fy = ys - y0
    def g(yy, xx): return im[yy, xx]
    c = (g(y0, x0) * ((1 - fx) * (1 - fy))[..., None] + g(y0, x0 + 1) * (fx * (1 - fy))[..., None]
         + g(y0 + 1, x0) * ((1 - fx) * fy)[..., None] + g(y0 + 1, x0 + 1) * (fx * fy)[..., None])
    return c


def build(slug, fronte, retro):
    F = silhouette(os.path.join(WEB, fronte + '.jpg'))
    B = silhouette(os.path.join(WEB, retro + '.jpg')) if retro else F
    imF, cxF, tF, bF, rF = F
    imB, cxB, tB, bB, rB = B
    hF = bF - tF
    # profilo normalizzato: altezza 6, raggio in proporzione
    t = np.linspace(0, 1, N_ROWS)            # 0 = fondo, 1 = sommità
    yF = bF - t * hF
    radF = np.interp(yF, np.arange(len(rF)), rF)
    scale = 6.0 / hF
    profile = [[round(float(r * scale), 4), round(float(tt * 6.0 - 3.0), 4)] for r, tt in zip(radF, t)]
    # texture: colonne = angolo phi (0..2pi), righe = altezza (alto -> basso)
    phi = (np.arange(TEX_W) + 0.5) / TEX_W * 2 * math.pi
    tv = 1 - (np.arange(TEX_H) + 0.5) / TEX_H         # riga 0 = sommità
    s = np.sin(phi)[None, :]; c = np.cos(phi)[None, :]
    yf = (bF - tv * hF)[:, None] * np.ones_like(s)
    rf = np.interp(yf[:, 0], np.arange(len(rF)), rF)[:, None]
    hB = bB - tB
    yb = (bB - tv * hB)[:, None] * np.ones_like(s)
    rb = np.interp(yb[:, 0], np.arange(len(rB)), rB)[:, None]
    # leggero rientro (0.97) per non campionare il bordo sfondo
    front = sample(imF, cxF + rf * 0.97 * s, yf)
    if retro:
        back = sample(imB, cxB - rb * 0.97 * s, yb)
    else:  # nessun retro: specchia il fronte
        back = sample(imF, cxF - rf * 0.97 * s, yf)
    # dissolvenza morbida sulla giunzione laterale
    wgt = np.clip((c + 0.12) / 0.24, 0, 1)[..., None] * np.ones((TEX_H, 1, 1))
    tex = front * wgt + back * (1 - wgt)
    img = Image.fromarray(np.clip(tex, 0, 255).astype(np.uint8))
    img.save(os.path.join(OUT, slug + '.jpg'), quality=86, optimize=True, progressive=True)
    return profile


def main():
    os.makedirs(OUT, exist_ok=True)
    data = {}
    for slug, (f, r) in PRODOTTI.items():
        data[slug] = build(slug, f, r)
        print('ok', slug)
    js = ('/* Generato da .claude/genera-bottiglie.py — profili 3D (raggio, y) */\n'
          'window.SFM_BOTTIGLIE = ' + json.dumps(data, separators=(',', ':')) + ';\n')
    with open(os.path.join(OUT, 'bottiglie.js'), 'w') as fh:
        fh.write(js)

if __name__ == '__main__':
    main()
