#!/usr/bin/env python3
"""Bottiglie 3D della scheda prodotto, ricostruite dalle foto originali
(assets/prodotti/vino, sfondo bianco, alta risoluzione).

Per ogni prodotto:
  - profilo reale della bottiglia (dalla foto frontale)
  - texture colore "srotolata": le ETICHETTE sono prese dalle foto (fronte e
    retro); vetro e capsula hanno il loro colore medio riga per riga, SENZA i
    riflessi della foto (i riflessi li crea la scena 3D, fermi rispetto alla
    luce, come nella realtà)
  - mappa materiali: R = vetro lucido (clearcoat), G = ruvidità, B = metallo
Output in assets/prodotti/3d/: <slug>.jpg, <slug>-m.png, bottiglie.js
Uso: python3 .claude/genera-bottiglie.py [slug ...]
"""
import json, math, os, sys
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'assets/prodotti/vino')
OUT = os.path.join(ROOT, 'assets/prodotti/3d')

# slug: (foto fronte, foto retro, categoria del liquido)
PRODOTTI = {
    'vasia-rosso': ('vasia davanti.jpg', 'vasia .jpg', 'rosso'),
    'kalanero': ('kalanero-davanti.jpg', None, 'rosso'),
    'primula-rosso': ('primula bianco davanti.jpg', 'primula bianco retro.jpg', 'rosso'),
    'dalia-rosso': ('IMG_0970.jpg', 'retro dalia rosso.jpg', 'rosso'),
    'calasulu-rosso': ('calasulu rosso davanti.jpg', 'calasulu rosso retro.jpg', 'rosso'),
    'mareme-bianco': ('mareme davanti.jpg', 'mareme retro.jpg', 'bianco'),
    'primula-bianco': ('primula  davanti.jpg', 'primula retro.png', 'bianco'),
    'dalia-bianco': ('dalia bianco davanti.jpg', 'dalia bianco retro.jpg', 'bianco'),
    'calasulu-bianco': ('calasulu bianco davanti.jpg', 'calasulu bianco retro.jpg', 'bianco'),
    'murmuro-rosato': ('murmoro rosato davanti.jpg', 'murmoro rosato.jpg', 'rosato'),
    'primula-rosato': ('primula rosato davanti.jpg', 'primula rosato retro.jpg', 'rosato'),
    'dalia-rosato': ('dalia rosato davanti.jpg', 'dalia rosato retro.jpg', 'rosato'),
    'calasulu-rosato': ('calasulu rosato.davanti.jpg', 'calasulu rosato retro.jpg', 'rosato'),
    'amaro-korva': ('amaro corva davanti.jpg', 'amaro corva retro1.jpg', 'amaro'),
}
# Etichette scure che il riconoscimento automatico non vede: fasce in altezza
# (0 = fondo, 1 = sommità) da trattare comunque come etichetta.
ETICHETTE_MANUALI = {
    'kalanero': {'fronte': [(0.07, 0.36)], 'retro': [(0.07, 0.36)]},
    'amaro-korva': {'fronte': [(0.06, 0.52)], 'retro': [(0.06, 0.52)]},

}

# Etichette scure (nere su vetro scuro): niente rifinitura automatica dei bordi
ETICHETTE_SCURE = {'kalanero', 'amaro-korva'}
# larghezza massima (in sin dell'angolo) se il riconoscimento la sovrastima
LARGHEZZA_MAX = {('dalia-rosato', 'retro'): 0.8}

WORK_H = 2400          # altezza di lavoro delle foto
N_PROFILE = 200
TEX_W, TEX_H = 2048, 2048    # analisi; la texture del vetro viene salvata a 1024
LAB_W = 4096                 # etichette: larghezza (360°) versione computer
LAB_W_MOBILE = 2048
MAT_W, MAT_H = 512, 512
EDGE = 0.965           # oltre questo |sin| la foto è troppo schiacciata


# Prospettiva: le foto sono scattate un po' dall'alto, quindi un cerchio
# orizzontale della bottiglia appare come un'ellisse (il punto più vicino
# all'obiettivo sta più in basso dei lati). Spostamento verticale in pixel:
#   dy = e(t) * R * cos(angolo),   e(t) = e_fondo * (1 - t / TC)
# e_fondo si misura sull'ellisse del fondo di ogni foto; TC = altezza (0..1)
# a cui si trovava l'obiettivo (lì l'ellisse è una linea).
TC = 1.15


def elev_px(D, t, R, s):
    e = D['eb'] * np.clip(1 - np.asarray(t) / TC, 0, None)
    return e * R * np.sqrt(np.clip(1 - np.asarray(s) ** 2, 0, 1))


def measure_eb(im, cx, top, bot, rad):
    """Inclinazione dell'obiettivo misurata sull'ellisse del fondo."""
    bg = np.concatenate([im[:, 8:30], im[:, -30:-8]], axis=1).mean(axis=1, keepdims=True)
    fg = (np.abs(im - bg).max(axis=2) > 12) | ((im.max(2) - im.min(2)) > 20)
    R = np.median(rad[bot - int((bot - top) * 0.2):bot - int((bot - top) * 0.05)])
    def lowest(sv):
        idx = np.nonzero(fg[top:, int(cx + sv * R)])[0]
        return top + idx[-1] if len(idx) else bot
    yc = np.median([lowest(v) for v in (-0.1, 0, 0.1)])
    ys = np.median([lowest(v) for v in (-0.75, -0.7, 0.7, 0.75)])
    e = (yc - ys) / (R * (1 - math.sqrt(1 - 0.725 ** 2)))
    return float(np.clip(e, 0.22, 0.4)) if 0.15 < e < 0.5 else 0.32


def load_full(name):
    im = Image.open(os.path.join(SRC, name))
    if im.mode == 'RGBA':
        bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3]); im = bg
    return np.asarray(im.convert('RGB'))


def label_texture(slug, F, B, imF, imB, has_back, scale_units):
    imF_full, imB_full = imF, imB
    """Texture ad alta risoluzione delle sole etichette (fronte + retro) dalle
    foto originali, con maschera alfa a bordi netti."""
    rects = [(r, 1) for r in F['rects']] + [(r, -1) for r in B['rects']]
    if not rects:
        return None
    tmin = max(0.0, min(r[0][0] for r in rects) - 0.004)
    tmax = min(1.0, max(r[0][1] for r in rects) + 0.004)
    # densità: texel quadrati sul raggio massimo delle etichette
    rows_t = np.linspace(tmin, tmax, 64)
    Ru = np.interp(F['bot'] - rows_t * (F['bot'] - F['top']), np.arange(len(F['rad'])), F['rad']).max() * scale_units
    Lh = int(round((tmax - tmin) * 6 * LAB_W / (2 * math.pi * Ru) / 8)) * 8
    Lh = min(Lh, 2048)
    phi = (np.arange(LAB_W) + 0.5) / LAB_W * 2 * math.pi
    sphi, cphi = np.sin(phi), np.cos(phi)
    tex = np.zeros((Lh, LAB_W, 3), np.uint8)
    alpha = np.zeros((Lh, LAB_W), np.uint8)
    for D, full, sgn, cols in ((F, imF, 1, cphi >= 0), (B, imB, -1, cphi < 0)):
        fs = full.shape[0] / WORK_H                       # da coordinate di lavoro a originale
        ci = np.nonzero(cols)[0]
        sv = sgn * sphi[ci]
        for j0 in range(0, Lh, 128):
            j = np.arange(j0, min(Lh, j0 + 128))
            t = tmax - (j + 0.5) / Lh * (tmax - tmin)
            m = np.zeros((len(j), len(ci)), bool)
            for (tl, th, sl, sr) in D['rects']:
                m |= ((t >= tl) & (t <= th))[:, None] & ((sv >= sl) & (sv <= sr))[None, :]
            if not m.any():
                continue
            y = D['bot'] - t * (D['bot'] - D['top'])
            R = np.interp(y, np.arange(len(D['rad'])), D['rad'])
            ss = np.clip(sv, -EDGE, EDGE)
            xs = (D['cx'] + R[:, None] * ss[None, :]) * fs
            ys = (y[:, None] + elev_px(D, t[:, None], R[:, None], ss[None, :])) * fs
            c = bilinear(full, xs, ys)
            blk = tex[j][:, ci]
            blk[m] = np.clip(c[m], 0, 255).astype(np.uint8)
            tex[j[:, None], ci[None, :]] = blk
            a = alpha[j][:, ci]
            a[m] = 255
            alpha[j[:, None], ci[None, :]] = a
    # Bordi alto/basso curvi (foto scattata un po' dall'alto): colonna per
    # colonna si tolgono i pixel "uguali al vetro" partendo dal bordo
    # dell'etichetta verso l'interno (solo nel 18% esterno, così i disegni
    # interni dello stesso colore del vetro restano).
    if slug not in ETICHETTE_SCURE:
        tt = tmax - (np.arange(Lh) + 0.5) / Lh * (tmax - tmin)
        rowsN = np.clip(((1 - tt) * TEX_H).astype(int), 0, TEX_H - 1)
        for D, cols in ((F, cphi >= 0), (B, cphi < 0)):
            g = D['glass'][rowsN]                                  # Lh x 3
            def med(v, w=25):
                pad = np.pad(v, w, mode='edge')
                return np.array([np.median(pad[i:i + 2 * w + 1]) for i in range(len(v))])
            # bordi laterali: stessa cosa riga per riga, dentro la metà della foto
            seg_cols = np.nonzero(cols)[0]
            # la metà frontale è spezzata in due (0..90° e 270..360°): la si
            # riordina in un'unica striscia continua da sinistra a destra
            if cphi[0] >= 0:
                split = np.nonzero(np.diff(seg_cols) > 1)[0]
                if len(split):
                    k0 = split[0] + 1
                    seg_cols = np.concatenate([seg_cols[k0:], seg_cols[:k0]])
            sub_a = alpha[:, seg_cols] > 0
            sub_t = tex[:, seg_cols].astype(np.float32)
            dl = np.zeros(Lh); dr = np.zeros(Lh)
            for r in range(Lh):
                a = sub_a[r]
                if not a.any():
                    continue
                idx = np.nonzero(a)[0]
                x0, x1 = idx[0], idx[-1]
                zone = int((x1 - x0) * 0.08)
                like = np.abs(sub_t[r, x0:x1 + 1] - g[r]).max(axis=1) < 48
                d = 0
                while d < zone and like[d]: d += 1
                dl[r] = d
                d = 0
                while d < zone and like[len(like) - 1 - d]: d += 1
                dr[r] = d
            dl = med(dl); dr = med(dr)
            for r in range(Lh):
                a = sub_a[r]
                if not a.any():
                    continue
                idx = np.nonzero(a)[0]
                x0, x1 = idx[0], idx[-1]
                if dl[r] > 0: alpha[r, seg_cols[x0:x0 + int(dl[r])]] = 0
                if dr[r] > 0: alpha[r, seg_cols[x1 - int(dr[r]) + 1:x1 + 1]] = 0
    img = Image.fromarray(tex)
    img.save(os.path.join(OUT, slug + '-e.jpg'), quality=86, optimize=True, progressive=True)
    img.resize((LAB_W_MOBILE, Lh // 2), Image.LANCZOS).save(
        os.path.join(OUT, slug + '-e2.jpg'), quality=86, optimize=True, progressive=True)
    from PIL import ImageFilter
    am = Image.fromarray(alpha).filter(ImageFilter.MinFilter(11))   # bordo pulito, senza il vetro
    am.resize((LAB_W // 2, Lh // 2), Image.BOX).save(
        os.path.join(OUT, slug + '-a.png'), optimize=True)
    return [round(tmin, 5), round(tmax, 5)]


def load(name):
    im = Image.open(os.path.join(SRC, name))
    if im.mode == 'RGBA':
        bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3]); im = bg
    im = im.convert('RGB')
    w = round(im.width * WORK_H / im.height)
    return np.asarray(im.resize((w, WORK_H), Image.LANCZOS)).astype(np.float32)


def silhouette(im):
    h, w, _ = im.shape
    bg = np.concatenate([im[:, 8:30], im[:, -30:-8]], axis=1).mean(axis=1, keepdims=True)
    diff = np.abs(im - bg).max(axis=2)
    sat = im.max(axis=2) - im.min(axis=2)
    pulito = bg.mean() > 248
    fg = (diff > (9 if pulito else 24)) | (sat > (20 if pulito else 30))
    fg[:, :14] = False; fg[:, -14:] = False; fg[:6] = False; fg[-6:] = False
    rows = []
    for y in range(h):
        xs = np.nonzero(fg[y])[0]
        rows.append((xs[0], xs[-1]) if len(xs) >= 6 else None)
    ys = [y for y, r in enumerate(rows) if r and r[1] - r[0] > 14]
    top, bot = ys[0], ys[-1]
    body = [rows[y] for y in range(top + (bot - top) // 2, bot - (bot - top) // 10) if rows[y]]
    cx = float(np.median([(a + b) / 2 for a, b in body]))
    rad = np.zeros(h)
    for y in range(top, bot + 1):
        r = rows[y]
        if r:
            rad[y] = min(cx - r[0], r[1] - cx) + 0.5
    for y in range(top, bot + 1):
        if rad[y] <= 0:
            rad[y] = rad[y - 1]
    k = 16
    seg = rad[top:bot + 1].copy()
    seg = np.array([np.median(seg[max(0, i - k):i + k + 1]) for i in range(len(seg))])
    n = 52   # chiusura 1D: riempie capsule chiare su fondo chiaro
    dil = np.array([seg[max(0, i - n):i + n + 1].max() for i in range(len(seg))])
    clo = np.array([dil[max(0, i - n):i + n + 1].min() for i in range(len(seg))])
    seg = np.maximum(seg, clo)
    g = np.exp(-0.5 * (np.arange(-15, 16) / 5.0) ** 2); g /= g.sum()
    seg = np.convolve(np.pad(seg, 15, mode='edge'), g, mode='valid')
    rad[top:bot + 1] = seg
    return cx, top, bot, rad


def bilinear(im, xs, ys):
    h, w, _ = im.shape
    xs = np.clip(xs, 0, w - 1.001); ys = np.clip(ys, 0, h - 1.001)
    x0 = xs.astype(int); y0 = ys.astype(int); fx = (xs - x0)[..., None]; fy = (ys - y0)[..., None]
    return (im[y0, x0] * (1 - fx) * (1 - fy) + im[y0, x0 + 1] * fx * (1 - fy)
            + im[y0 + 1, x0] * (1 - fx) * fy + im[y0 + 1, x0 + 1] * fx * fy)


def smooth1d(a, sigma):
    r = int(sigma * 3) + 1
    g = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma) ** 2); g /= g.sum()
    if a.ndim == 1:
        return np.convolve(np.pad(a, r, mode='edge'), g, mode='valid')
    return np.stack([smooth1d(a[:, i], sigma) for i in range(a.shape[1])], axis=1)


def analyze(im, manual=None, smax_cap=None):
    """Per ogni altezza t (0 fondo .. 1 cima, N campioni): raggio, colore del
    vetro/capsula senza riflessi, maschera etichetta in funzione di sin(angolo)."""
    cx, top, bot, rad = silhouette(im)
    eb = measure_eb(im, cx, top, bot, rad)
    hgt = bot - top
    N = TEX_H
    t = 1 - (np.arange(N) + 0.5) / N                 # riga 0 = sommità
    ys = bot - t * hgt
    R = np.interp(ys, np.arange(len(rad)), rad)
    S = np.linspace(-EDGE, EDGE, 257)                # sin(angolo) campionati
    xs = cx + R[:, None] * S[None, :]
    yy = ys[:, None] + elev_px({'eb': eb}, t[:, None], R[:, None], S[None, :])
    col = bilinear(im, xs, yy)                       # N x 257 x 3
    L = col.mean(axis=2)
    sat = col.max(axis=2) - col.min(axis=2)
    paper = (L > 160) & (sat < 80)
    gx = np.abs(np.diff(L, axis=1, prepend=L[:, :1]))
    texture = gx > 22
    # dettaglio fine (testi, disegni) misurato sulla foto a piena risoluzione
    labelish = paper | texture
    centre = np.abs(S) < 0.6
    body = R > 0.7 * R.max()                         # niente etichette su collo/capsula

    def runs_of(mask):
        out = []; i = 0
        while i < len(mask):
            if mask[i]:
                j = i
                while j < len(mask) and mask[j]: j += 1
                out.append([i, j]); i = j
            else:
                i += 1
        merged = []
        for a, b in out:
            if merged and a - merged[-1][1] < N * 0.06:
                merged[-1][1] = b
            else:
                merged.append([a, b])
        return [r for r in merged if r[1] - r[0] > N * 0.03]

    def glass_outside(runs):
        inrun = np.zeros(N, bool)
        for a, b in runs:
            inrun[max(0, a - int(N * 0.006)):b + int(N * 0.006)] = True
        g = np.zeros((N, 3))
        for i in range(N):
            c = col[i, np.abs(S) < 0.8]
            Li = c.mean(axis=1)
            g[i] = np.median(c[Li <= np.percentile(Li, 55)], axis=0)
        ok = np.nonzero(~inrun)[0]
        if len(ok) > 2:
            for ch in range(3):
                g[:, ch] = np.interp(np.arange(N), ok, g[ok, ch])
        return smooth1d(g, N * 0.003), inrun

    # passo 1: carta bianca o dettagli fini (testi)
    frac = labelish[:, centre].mean(axis=1)
    runs = runs_of((smooth1d(frac.astype(float), N * 0.004) > 0.5) & body)
    glass, _ = glass_outside(runs)
    # passo 2: tutto ciò che è diverso dal vetro (anche acquerelli e colori)
    if manual:
        runs = [[int((1 - m[1]) * N), int((1 - m[0]) * N)] for m in manual]
    else:
        diff = np.abs(col - glass[:, None, :]).max(axis=2) > 55
        frac2 = diff[:, centre].mean(axis=1)
        runs = runs_of((smooth1d(frac2.astype(float), N * 0.004) > 0.5) & body)
        runs = [r for r in runs if (1 - r[0] / N) > 0.07]      # niente "etichette" sul fondo
    glass, inrun = glass_outside(runs)
    merged = runs
    # estensione orizzontale di ogni etichetta
    mask = np.zeros((N, len(S)), bool)
    rects = []
    for k, (a, b) in enumerate(merged):
        d = np.abs(col[a:b] - glass[a:b, None, :]).max(axis=2) > 55
        lab = smooth1d(d.mean(axis=0), 1.5)
        c = len(S) // 2
        l = c
        while l > 0 and lab[l - 1] > 0.6: l -= 1
        r = c
        while r < len(S) - 1 and lab[r + 1] > 0.6: r += 1
        if manual:
            smax = manual[k][2] if len(manual[k]) > 2 else 1
            l = int(np.searchsorted(S, -smax)); r = int(np.searchsorted(S, smax)) - 1
        elif r - l < 6:
            l, r = 0, len(S) - 1
        else:
            l = l + 1 if l > 0 else l
            r = r - 1 if r < len(S) - 1 else r
        if smax_cap:
            l = max(l, int(np.searchsorted(S, -smax_cap)))
            r = min(r, int(np.searchsorted(S, smax_cap)) - 1)
        mask[a:b, l:r + 1] = True
        rects.append((1 - (b - 0.5) / N, 1 - (a + 0.5) / N, float(S[l]), float(S[r])))
    return dict(eb=eb, cx=cx, top=top, bot=bot, rad=rad, R=R, S=S, t=t, ys=ys, mask=mask, rects=rects,
                glass=glass, runs=merged, inrun=inrun)


def capsule_bottom(glassF, R, N):
    """Altezza (riga della texture) dove finisce la capsula: salto di colore sul collo."""
    neck = np.nonzero(R < 0.62 * R.max())[0]
    neck = neck[neck < N * 0.45]
    if len(neck) < 10:
        return int(N * 0.12)
    a, b = neck[0], neck[-1]
    w = max(4, int(N * 0.006))
    best, by = 0, None
    for y in range(a + int((b - a) * 0.12) + w, b - w):
        d = np.abs(glassF[y - w:y].mean(axis=0) - glassF[y:y + w].mean(axis=0)).sum()
        if d > best:
            best, by = d, y
    if by is None or best < 40:
        return int(a + (b - a) * 0.62)
    return by


def build(slug, fronte, retro, liquido):
    man = ETICHETTE_MANUALI.get(slug, {})
    imF = load(fronte)
    F = analyze(imF, man.get('fronte'), LARGHEZZA_MAX.get((slug, 'fronte')))
    if retro:
        imB = load(retro)
        B = analyze(imB, man.get('retro'), LARGHEZZA_MAX.get((slug, 'retro')))
    else:
        imB, B = imF, F
    N = TEX_H
    # profilo dalla foto frontale (altezza 6, centrata)
    hF = F['bot'] - F['top']
    tp = np.linspace(0, 1, N_PROFILE)
    radp = np.interp(F['bot'] - tp * hF, np.arange(len(F['rad'])), F['rad'])
    scale = 6.0 / hF
    profile = [[round(float(r * scale), 4), round(float(tt * 6 - 3), 4)] for r, tt in zip(radp, tp)]

    # --- texture colore -----------------------------------------------------
    phi = (np.arange(TEX_W) + 0.5) / TEX_W * 2 * math.pi
    s = np.sin(phi); c = np.cos(phi)
    front = c >= 0
    # stesso vetro: media fronte/retro, solo dove nessuna delle due ha l'etichetta
    glass = (F['glass'] + B['glass']) / 2
    bad = F['inrun'] | B['inrun']
    # fondo (ultimo 12%): nella foto è scurito da ombre e spessore del vetro e
    # creerebbe una fascia; prende il colore del vetro pulito più in basso
    bad |= np.arange(N) > N * 0.88
    ok = np.nonzero(~bad)[0]
    if len(ok) > 2:
        for ch in range(3):
            glass[:, ch] = np.interp(np.arange(N), ok, glass[ok, ch])
    tex = np.repeat(glass[:, None, :], TEX_W, axis=1).astype(np.float32)
    labelM = np.zeros((N, TEX_W), np.float32)

    def paint(D, im, cols, sgn):
        ss = np.clip(sgn * s[cols], -EDGE, EDGE)
        # indice nella maschera
        si = np.round((ss + EDGE) / (2 * EDGE) * (len(D['S']) - 1)).astype(int)
        m = D['mask'][:, si]                         # N x ncols
        if not m.any():
            return
        rowsI = np.nonzero(m.any(axis=1))[0]
        xs = D['cx'] + D['R'][rowsI, None] * ss[None, :]
        yy = D['ys'][rowsI, None] + elev_px(D, D['t'][rowsI, None], D['R'][rowsI, None], ss[None, :])
        sample = bilinear(im, xs, yy)
        sub = m[rowsI][..., None]
        blk = tex[rowsI][:, cols]
        tex[rowsI[:, None], cols[None, :]] = np.where(sub, sample, blk)
        labelM[rowsI[:, None], cols[None, :]] = np.maximum(labelM[rowsI[:, None], cols[None, :]], m[rowsI].astype(np.float32))

    colsF = np.nonzero(front)[0]
    colsB = np.nonzero(~front)[0]
    paint(F, imF, colsF, 1)
    paint(B, imB, colsB, -1 if retro else -1)
    # le etichette vere sono nello strato ad alta risoluzione: sotto resta il vetro
    tex = np.repeat(glass[:, None, :], TEX_W, axis=1).astype(np.float32)
    # etichette avvolgenti: riempi il fianco (oltre il limite della foto)
    # se sia fronte sia retro arrivano al bordo alla stessa altezza
    capY = capsule_bottom(glass, F['R'], N)
    lab = label_texture(slug, F, B, load_full(fronte), load_full(retro) if retro else load_full(fronte),
                        bool(retro), scale)

    # --- mappa materiali ----------------------------------------------------
    mat = np.zeros((N, TEX_W, 3), np.float32)
    mat[..., 0] = 255          # clearcoat (vetro)
    mat[..., 1] = 0.06 * 255   # ruvidità vetro
    mat[..., 2] = 0
    # capsula: lamina satinata, un po' metallica
    mat[:capY, :, 0] = 70
    mat[:capY, :, 1] = 0.38 * 255
    mat[:capY, :, 2] = 0.45 * 255
    # etichette: carta opaca
    lm = labelM[..., None]
    paper = np.array([0, 0.62 * 255, 0], np.float32)
    mat = mat * (1 - lm) + paper * lm

    Image.fromarray(np.clip(tex, 0, 255).astype(np.uint8)).resize((1024, 1024), Image.LANCZOS).save(
        os.path.join(OUT, slug + '.jpg'), quality=88, optimize=True, progressive=True)
    Image.fromarray(np.clip(mat, 0, 255).astype(np.uint8)).resize((MAT_W, MAT_H), Image.BILINEAR).save(
        os.path.join(OUT, slug + '-m.png'), optimize=True)
    return {
        'p': profile,
        'cap': round(float(3 - capY / N * 6), 3),     # y (coordinate 3D) di fine capsula
        'liq': liquido,
        'lab': lab,                                    # fascia (0..1) della texture etichette
    }


def main():
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, 'bottiglie.js')
    data = {}
    if os.path.exists(path):
        try:
            data = json.loads(open(path).read().split('=', 1)[1].strip().rstrip(';'))
            data = {k: v for k, v in data.items() if isinstance(v, dict)}
        except Exception:
            data = {}
    only = sys.argv[1:] or list(PRODOTTI)
    for slug in only:
        f, r, liq = PRODOTTI[slug]
        data[slug] = build(slug, f, r, liq)
        print('ok', slug, 'capsula y =', data[slug]['cap'])
    js = ('/* Generato da .claude/genera-bottiglie.py: profilo (raggio, y), fine capsula, liquido */\n'
          'window.SFM_BOTTIGLIE = ' + json.dumps(data, separators=(',', ':')) + ';\n')
    with open(path, 'w') as fh:
        fh.write(js)


if __name__ == '__main__':
    main()
