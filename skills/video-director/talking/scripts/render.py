"""render.py - edit.json -> final.mp4 + sheet.jpg. Every frame is a pure function of t (no state between
frames), so chunks render in parallel and any frame can be re-rendered alone.

    python render.py <workdir>/edit.json                 full render, all cores
    python render.py <workdir>/edit.json --preview       half-res, fast encode -> preview.mp4
    python render.py <workdir>/edit.json --range 16:20   only that span (implies --preview)

edit.json (times are seconds or word refs on the CUT timeline: "fire", "fire#2", "fire.e" (word end),
"fire+0.3", "end-1"):
{
  "out": "final.mp4", "size": [1080, 1920], "tail": 1.2, "punch": 1.12,
  "captions": {"words": 3, "y": 0.84, "size": 78, "accent": "#FFD23F", "keys": ["fire", "idea"]},
  "fx": [
    {"type": "pop", "tokens": [["100", "100"], ["-", "minus"], ["25", "25"], ["=", "equals"], ["75", "75"]],
     "until": "up.e", "y": 0.12, "size": 170},
    {"type": "fire", "at": "fire", "until": "smoke+0.3"},
    {"type": "smoke", "at": "smoke", "until": "that.e+0.4"},
    {"type": "bulb", "at": "bulb", "on": "idea", "until": "end"}
  ]
}
"""
import argparse, json, math, os, re, subprocess, sys, time, wave
from functools import lru_cache
from multiprocessing import Pool
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FPS = 30
FONTS = ["C:/Windows/Fonts/seguibl.ttf", "C:/Windows/Fonts/arialbd.ttf",
         "/System/Library/Fonts/Supplemental/Arial Black.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
FONT = next((f for f in FONTS if Path(f).exists()), None)
C = {}  # per-process render context, filled by setup()


# ---------------------------------------------------------------- time refs + easing
def norm(w):
    return re.sub(r"[^\w']", "", w.lower())


def at(ref):
    if ref is None or isinstance(ref, (int, float)):
        return ref
    m = re.fullmatch(r"(.+?)(#\d+)?(\.e)?([+-]\d*\.?\d+)?", str(ref).strip())
    base, nth, end, off = m.groups()
    off = float(off or 0)
    if base == "end":
        return C["dur"] + off
    if base == "start":
        return off
    hits = [w for w in C["words"] if norm(w["w"]) == norm(base)]
    k = int(nth[1:]) - 1 if nth else 0
    if k >= len(hits):
        raise SystemExit(f"edit.json: word ref {ref!r} not in transcript (see cut.txt)")
    return (hits[k]["e"] if end else hits[k]["s"]) + off


def span_end(fx, default=2.0):
    return at(fx["until"]) if "until" in fx else at(fx["at"]) + default


def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def ease(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def spring(x, k=6.0, w=10.0):
    """0 -> 1 with a little overshoot; x in seconds since the event."""
    return 0.0 if x <= 0 else 1 - math.exp(-k * x) * math.cos(w * x)


def hash01(i):
    return (math.sin(i * 12.9898 + 78.233) * 43758.5453) % 1.0


def bgr(hexs):
    h = hexs.lstrip("#")
    return (int(h[4:6], 16), int(h[2:4], 16), int(h[0:2], 16))


# ---------------------------------------------------------------- noise (fire/smoke)
_LAT = np.random.default_rng(7).random((256, 256)).astype(np.float32)


def vnoise(x, y):
    xi, yi = np.floor(x).astype(np.int32), np.floor(y).astype(np.int32)
    xf, yf = x - xi, y - yi
    u, v = xf * xf * (3 - 2 * xf), yf * yf * (3 - 2 * yf)
    x0, x1, y0, y1 = xi & 255, (xi + 1) & 255, yi & 255, (yi + 1) & 255
    a, b, c, d = _LAT[y0, x0], _LAT[y0, x1], _LAT[y1, x0], _LAT[y1, x1]
    top, bot = a + (b - a) * u, c + (d - c) * u
    return top + (bot - top) * v


def fbm(x, y, octaves=4):
    s, amp, f = 0.0, 0.5, 1.0
    for _ in range(octaves):
        s = s + amp * vnoise(x * f, y * f)
        f, amp = f * 2, amp * 0.5
    return s / (1 - 0.5 ** octaves)


# ---------------------------------------------------------------- drawing helpers
@lru_cache(512)
def text_sprite(text, size, color):
    """White/colour bold text, dark stroke, soft drop shadow. Returns (bgr float32, alpha float32 0..1)."""
    font = ImageFont.truetype(FONT, size)
    sw = max(2, size // 11)
    l, t, r, b = font.getbbox(text, stroke_width=sw)
    pad = sw + size // 4
    img = Image.new("RGBA", (r - l + 2 * pad, b - t + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(img).text((pad - l, pad - t), text, font=font, fill=color[::-1] + (255,), stroke_width=sw,
                             stroke_fill=(12, 12, 16, 255))
    a = np.asarray(img).astype(np.float32) / 255
    rgb, al = a[..., :3][..., ::-1] * 255, a[..., 3]
    sh = np.roll(cv2.GaussianBlur(al, (0, 0), size * 0.07), (size // 18, size // 30), (0, 1)) * 0.6
    out_a = al + sh * (1 - al)
    out_rgb = rgb * (al / np.maximum(out_a, 1e-4))[..., None]
    return out_rgb.astype(np.float32), out_a.astype(np.float32)


def paste(frame, spr, cx, cy, scale=1.0, alpha=1.0):
    """Alpha-composite a sprite centred at (cx, cy). Uniform scale only (similarity, never squash)."""
    rgb, a = spr
    if scale <= 0.01 or alpha <= 0.003:
        return None
    if abs(scale - 1) > 0.004:
        h, w = a.shape
        size = (max(1, int(w * scale)), max(1, int(h * scale)))
        rgb, a = cv2.resize(rgb, size, interpolation=cv2.INTER_LINEAR), cv2.resize(a, size, interpolation=cv2.INTER_LINEAR)
    h, w = a.shape
    x0, y0 = int(round(cx - w / 2)), int(round(cy - h / 2))
    H, W = frame.shape[:2]
    fx0, fy0, fx1, fy1 = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
    if fx1 <= fx0 or fy1 <= fy0:
        return None
    sa = a[fy0 - y0:fy1 - y0, fx0 - x0:fx1 - x0, None] * alpha
    roi = frame[fy0:fy1, fx0:fx1]
    roi *= 1 - sa
    roi += rgb[fy0 - y0:fy1 - y0, fx0 - x0:fx1 - x0] * sa
    return (x0, y0, x0 + w, y0 + h)


def add_glow(frame, cx, cy, radius, color, amount):
    """Additive soft light (Gaussian blob) - bulb glow, flashes, accent halos."""
    if amount <= 0.003:
        return
    r = int(radius * 2.5)
    H, W = frame.shape[:2]
    x0, y0, x1, y1 = max(0, int(cx) - r), max(0, int(cy) - r), min(W, int(cx) + r), min(H, int(cy) + r)
    if x1 <= x0 or y1 <= y0:
        return
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    g = np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * radius * radius)) * amount
    frame[y0:y1, x0:x1] += g[..., None] * np.array(color, np.float32)


def add_light(frame, cx, cy, R, draw):
    """Additive patch: draw(layer, centre) paints into a black (2R+1)^2 layer that is ADDED to the frame, so a
    fading particle fades to nothing instead of painting a dark dot."""
    R = int(R) + 2
    x0, y0 = int(cx) - R, int(cy) - R
    H, W = frame.shape[:2]
    fx0, fy0, fx1, fy1 = max(0, x0), max(0, y0), min(W, x0 + 2 * R + 1), min(H, y0 + 2 * R + 1)
    if fx1 <= fx0 or fy1 <= fy0:
        return
    layer = np.zeros((2 * R + 1, 2 * R + 1, 3), np.float32)
    draw(layer, (R, R))
    frame[fy0:fy1, fx0:fx1] += layer[fy0 - y0:fy1 - y0, fx0 - x0:fx1 - x0]


def burst(frame, cx, cy, dt, color, n=26, seed=0, reach=260):
    """Radial spark burst dt seconds after an event (deterministic per seed)."""
    if not 0 <= dt < 0.7:
        return
    u = C["u"]
    life = 1 - dt / 0.7
    for i in range(n):
        ang = 2 * math.pi * (i + hash01(seed * 97 + i) * 0.6) / n
        sp = (0.55 + 0.45 * hash01(seed * 31 + i)) * reach * u
        d = sp * ease(dt / 0.45)
        x, y = cx + math.cos(ang) * d, cy + math.sin(ang) * d + 60 * u * dt * dt
        r = max(1, int((3 + 3 * hash01(i + seed)) * u * life))
        col = tuple(c * life for c in color)
        add_light(frame, x, y, r, lambda L, c, r=r, col=col: cv2.circle(L, c, r, col, -1, cv2.LINE_AA))
    ring = int(reach * u * ease(dt / 0.3))
    if dt < 0.3 and ring > 2:
        col = tuple(c * (1 - dt / 0.3) for c in color)
        add_light(frame, cx, cy, ring + 4 * u, lambda L, c: cv2.circle(L, c, ring, col, max(1, int(5 * u)), cv2.LINE_AA))


# ---------------------------------------------------------------- effects
def env(t, a, b, rise=0.3, fall=0.4):
    return ease((t - a) / rise) * (1 - ease((t - b) / fall)) if a <= t else 0.0


def fx_fire(frame, t, fx, face):
    a, b = at(fx["at"]), span_end(fx)
    k = env(t, a, b, 0.25, 0.45)
    if k <= 0.003:
        return
    H, W = frame.shape[:2]
    gu, gv = C["grid"]
    n = 0.7 * fbm(gu * 5 + 0.3 * np.sin(gv * 3 + t), gv * 7 + t * 4.2) + 0.3 * fbm(gu * 12, gv * 14 + t * 7.5)
    h = fx.get("height", 0.36) * k * (0.55 + 0.9 * np.abs(gu - 0.5) * 2)  # tall at the edges, low under the face
    d = (gv - (1 - h)) / np.maximum(h, 1e-3)
    I = np.clip((n - 0.45) * 2.4 + d * 1.15 - 0.35, 0, 1)
    ramp = np.array([0, 0.25, 0.5, 0.75, 1.0], np.float32)
    col = np.stack([np.interp(I, ramp, [0, 0, 10, 60, 210]),       # B
                    np.interp(I, ramp, [0, 15, 90, 190, 245]),     # G
                    np.interp(I, ramp, [0, 150, 255, 255, 255])], -1).astype(np.float32)  # R
    col = cv2.GaussianBlur(cv2.resize(col, (W, H), interpolation=cv2.INTER_LINEAR), (0, 0), 3 * C["u"])
    flicker = 1 + 0.07 * math.sin(t * 23) * math.sin(t * 7.3)
    frame *= np.array([1 - 0.32 * k, 1 - 0.12 * k, 1 + 0.04 * k], np.float32) * flicker  # warm grade
    frame += col * k
    u = C["u"]
    for i in range(70):  # embers
        life = 0.9 + 0.8 * hash01(i)
        age = ((t - a) / life + hash01(i * 7)) % 1.0
        x = hash01(i * 3) * W + 40 * u * math.sin(age * 6 + i)
        y = H * (1.02 - age * (0.45 + 0.35 * hash01(i * 5)))
        br = (1 - age) * k
        r = max(1, int((2 + 3 * hash01(i * 11)) * u))
        add_light(frame, x, y, r, lambda L, c, r=r, br=br: cv2.circle(L, c, r, (70 * br, 170 * br, 255 * br), -1,
                                                                      cv2.LINE_AA))


def fx_smoke(frame, t, fx, face):
    a, b = at(fx["at"]), span_end(fx)
    k = env(t, a, b, 0.5, 0.8)
    if k <= 0.003:
        return
    H, W = frame.shape[:2]
    gu, gv = C["grid"]
    n = 0.65 * fbm(gu * 3 + t * 0.15, gv * 3.2 + t * 1.1) + 0.35 * fbm(gu * 7 - t * 0.3, gv * 8 + t * 1.9)
    h = 0.9 * ease((t - a) / 1.2)
    d = (gv - (1 - h)) / max(h, 1e-3)
    side = np.clip(0.45 + 1.1 * np.abs(gu - 0.5) * 2, 0, 1)
    A = np.clip((n - 0.4) * 2.2 + d * 0.7 - 0.25, 0, 1) * side * k * 0.85
    fx0, fy0, fx1, fy1 = [v / s for v, s in zip(face, (W, H, W, H))]  # thin the smoke over the face
    fm = np.exp(-(((gu - (fx0 + fx1) / 2) / (fx1 - fx0 + 1e-3)) ** 2 + ((gv - (fy0 + fy1) / 2) / (fy1 - fy0 + 1e-3)) ** 2) * 3)
    A = A * (1 - 0.75 * fm)
    A = cv2.GaussianBlur(cv2.resize(A.astype(np.float32), (W, H), interpolation=cv2.INTER_LINEAR), (0, 0), 6 * C["u"])
    frame *= 1 - A[..., None]
    frame += A[..., None] * np.array([205, 200, 198], np.float32)


def fx_pop(frame, t, fx, face):
    """Big tokens that pop in on their words (an equation, a title). Last token = accent + spark burst."""
    toks = [(str(tx), at(ref)) for tx, ref in fx["tokens"]]
    end = at(fx.get("until", toks[-1][1] + 2))
    if t < toks[0][1] - 0.05 or t > end + 0.25:
        return
    u, H, W = C["u"], *frame.shape[:2]
    size = int(fx.get("size", 160) * u)
    acc = fx.get("accent", len(toks) - 1)
    sprites = [text_sprite(tx, size, C["accent"] if i == acc else (255, 255, 255)) for i, (tx, _) in enumerate(toks)]
    gap = size * 0.18
    widths = [s[1].shape[1] - size * 0.5 for s in sprites]  # minus the shadow padding
    total = sum(widths) + gap * (len(toks) - 1)
    fit = min(1.0, W * 0.92 / total)
    x = W / 2 - total * fit / 2
    y = fx.get("y", 0.12) * H
    out = 1 - ease((t - end) / 0.22)
    for i, ((tx, t0), spr, w) in enumerate(zip(toks, sprites, widths)):
        cx = x + w * fit / 2
        x += (w + gap) * fit
        if t < t0:
            continue
        if i == acc:
            add_glow(frame, cx, y, size * 0.9 * fit, C["accent"], 0.35 * out * (1 + 0.15 * math.sin(t * 9)))
            burst(frame, cx, y, t - t0, C["accent"], seed=i + 1, reach=230)
        box = paste(frame, spr, cx, y, spring(t - t0) * fit * out, clamp((t - t0) / 0.05) * out)
        C["boxes"].append(("pop " + tx, box))


def fx_bulb(frame, t, fx, face):
    a, on = at(fx["at"]), at(fx.get("on", fx["at"]))
    end = at(fx.get("until", "end"))
    if t < a or t > end + 0.25:
        return
    i = C["i"]
    L = 0.0 if t < on - 0.45 else (0.75 if hash01(i) < 0.45 else 0.06) if t < on else 1.0  # flicker, then on
    x0, y0, x1, y1 = face
    fh = y1 - y0
    px, py = (x0 + x1) / 2, y0 - 0.02 * frame.shape[0]  # pivot = base tip, just above the head box top
    # bulb is ~3.2 r tall: fit it in the headroom, never taller than the face wants
    r = max(8.0, min(fx.get("size", 1.0) * fh * 0.22, (py - 0.03 * frame.shape[0]) / 3.2))
    drop = spring(t - a, 7, 13)
    py -= (1 - drop) * 0.6 * frame.shape[0]
    ang = math.radians(12) * math.exp(-5 * (t - a)) * math.sin(11 * (t - a))
    out = 1 - ease((t - end) / 0.22)
    if L > 0:
        gcx, gcy = px + math.sin(ang) * 2.1 * r, py - math.cos(ang) * 2.1 * r
        pulse = 1 + 0.08 * math.sin(t * 6)
        add_glow(frame, gcx, gcy, r * 2.4, (60, 190, 255), 0.75 * L * pulse * out)
        if t >= on:  # rays, drawn only in a box around the bulb (a full-frame blur costs 3x the frame time)
            R = int(2.4 * r)
            bx0, by0 = int(gcx) - R, int(gcy) - R
            rays = np.zeros((2 * R, 2 * R), np.float32)
            for j in range(12):
                th = j * math.pi / 6 + t * 0.6
                r0, r1 = 1.45 * r, (1.95 + 0.25 * math.sin(t * 5 + j)) * r
                cv2.line(rays, (int(R + math.cos(th) * r0), int(R + math.sin(th) * r0)),
                         (int(R + math.cos(th) * r1), int(R + math.sin(th) * r1)), 1.0, max(2, int(0.08 * r)),
                         cv2.LINE_AA)
            rays = cv2.GaussianBlur(rays, (0, 0), 2)[..., None] * np.array([90, 220, 255], np.float32) * out
            H, W = frame.shape[:2]
            fx0, fy0, fx1, fy1 = max(0, bx0), max(0, by0), min(W, bx0 + 2 * R), min(H, by0 + 2 * R)
            if fx1 > fx0 and fy1 > fy0:
                frame[fy0:fy1, fx0:fx1] += rays[fy0 - by0:fy1 - by0, fx0 - bx0:fx1 - bx0]
            burst(frame, gcx, gcy, t - on, (110, 230, 255), n=30, seed=9, reach=300)
            frame += np.array([215, 240, 255], np.float32) * 0.45 * math.exp(-(t - on) * 9)  # flash
            # the idea lights him up: warm key light from the bulb falling on the face
            add_glow(frame, (x0 + x1) / 2, y0 + 0.35 * fh, fh * 0.75, (60, 170, 255), 0.22 * ease((t - on) / 0.3) * out)
    spr = bulb_sprite(int(r), round(L, 2), round(math.degrees(ang), 1))
    C["boxes"].append(("bulb", paste(frame, spr, px, py - 1.35 * r, out, out)))


@lru_cache(256)
def bulb_sprite(r, L, deg):
    """Procedural light bulb, drawn rotated about its base tip. Sprite centre = 1.35 r above the tip."""
    S = 4  # supersample for clean edges
    R = r * S
    w, h = int(3.6 * R), int(3.6 * R)
    cx, cy = w / 2, h / 2 + 1.35 * R  # base tip position inside the canvas
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    P = lambda x, y: (cx + x * c - y * s, cy + x * s + y * c)  # pivot-relative (y up is negative)
    pts = lambda seq: np.array([P(x, y) for x, y in seq], np.int32)
    img = np.zeros((h, w, 4), np.uint8)
    gy = -2.1 * R
    arc = [(math.cos(q) * R, gy + math.sin(q) * R) for q in np.linspace(math.radians(48), math.radians(-228), 60)]
    glass = arc + [(-0.42 * R, -0.95 * R), (0.42 * R, -0.95 * R)]
    fill = tuple(int(u + (v - u) * L) for u, v in zip((245, 245, 240), (110, 230, 255)))
    cv2.fillPoly(img, [pts(glass)], fill + (int(255 * (0.3 + 0.68 * L)),), cv2.LINE_AA)
    if L > 0.5:
        cv2.circle(img, tuple(map(int, P(0, gy + 0.1 * R))), int(0.55 * R), (215, 250, 255, 255), -1, cv2.LINE_AA)
    out_col = tuple(int(u + (v - u) * L) for u, v in zip((215, 215, 210), (40, 170, 255)))
    cv2.polylines(img, [pts(glass)], True, out_col + (255,), max(2, int(0.07 * R)), cv2.LINE_AA)
    fil = [(-0.2 * R, -0.95 * R), (-0.2 * R, gy + 0.25 * R), (-0.12 * R, gy - 0.05 * R), (-0.04 * R, gy + 0.2 * R),
           (0.04 * R, gy - 0.05 * R), (0.12 * R, gy + 0.2 * R), (0.2 * R, gy - 0.05 * R), (0.2 * R, -0.95 * R)]
    fcol = (140, 140, 150) if L < 0.5 else (170, 245, 255)
    cv2.polylines(img, [pts(fil)], False, fcol + (255,), max(2, int(0.05 * R)), cv2.LINE_AA)
    arc_hi = [(math.cos(q) * 0.72 * R, gy + math.sin(q) * 0.72 * R) for q in np.linspace(math.radians(-150), math.radians(-105), 12)]
    cv2.polylines(img, [pts(arc_hi)], False, (255, 255, 255, 230), max(2, int(0.09 * R)), cv2.LINE_AA)
    for k in range(3):  # screw base bands
        top, bot = -0.95 * R + k * 0.26 * R, -0.95 * R + k * 0.26 * R + 0.2 * R
        hw = (0.42 - 0.03 * k) * R
        cv2.fillPoly(img, [pts([(-hw, top), (hw, top), (hw, bot), (-hw, bot)])], (165, 160, 155, 255), cv2.LINE_AA)
        cv2.polylines(img, [pts([(-hw, top), (hw, top), (hw, bot), (-hw, bot)])], True, (80, 78, 76, 255),
                      max(1, int(0.03 * R)), cv2.LINE_AA)
    cv2.ellipse(img, tuple(map(int, P(0, -0.12 * R))), (int(0.2 * R), int(0.13 * R)), deg, 0, 360, (60, 58, 56, 255),
                -1, cv2.LINE_AA)
    img = cv2.resize(img, (w // S, h // S), interpolation=cv2.INTER_AREA).astype(np.float32)
    return img[..., :3], img[..., 3] / 255


def captions(frame, t, face):
    cfg = C["cap"]
    chunk = next((ch for ch in C["chunks"] if ch["s"] <= t < ch["e"]), None)
    if not chunk:
        return
    u, H, W = C["u"], *frame.shape[:2]
    size = int(cfg.get("size", 78) * u)
    keys = {norm(k) for k in cfg.get("keys", [])}
    words = chunk["words"]
    sprites = []
    for w in words:
        txt = re.sub(r"[.,;:]+$", "", w["w"])
        key = norm(w["w"]) in keys or norm(w["w"]).isdigit()
        sprites.append(text_sprite(txt, size, C["accent"] if key else (255, 255, 255)))
    pad = size * 0.5
    widths = [s[1].shape[1] - pad for s in sprites]
    space = size * 0.28
    total = sum(widths) + space * (len(words) - 1)
    fit = min(1.0, W * 0.88 / total)
    y = cfg.get("y", 0.8) * H
    y = min(max(y, face[3] + size * 0.9), H * 0.9)  # text never covers the face: sit below the chin
    pop = 0.85 + 0.15 * ease((t - chunk["s"]) / 0.1)
    x = W / 2 - total * fit * pop / 2
    for w, spr, wd in zip(words, sprites, widths):
        active = w["s"] <= t < w["e"] + 0.05
        cx = x + wd * fit * pop / 2
        x += (wd + space) * fit * pop
        box = paste(frame, spr, cx, y, fit * pop * (1.08 if active else 1.0), clamp((t - chunk["s"]) / 0.05))
        C["boxes"].append(("caption", box))


def chunk_words(words, n):
    chunks, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        if len(cur) >= n or (w["w"][-1:] in ".?!" ) or (w["w"][-1:] == "," and len(cur) > 1) or not nxt \
                or nxt["s"] - w["e"] > 0.35:
            chunks.append(cur)
            cur = []
    out = []
    for i, ch in enumerate(chunks):
        nxt = chunks[i + 1][0]["s"] if i + 1 < len(chunks) else 1e9
        out.append({"words": ch, "s": ch[0]["s"], "e": min(nxt, ch[-1]["e"] + 0.5)})
    return out


FX = {"fire": fx_fire, "smoke": fx_smoke, "pop": fx_pop, "bulb": fx_bulb}
ORDER = {"smoke": 0, "fire": 1, "bulb": 2, "pop": 3}


# ---------------------------------------------------------------- frame
def setup(plan_path, scale):
    plan = json.loads(Path(plan_path).read_text(encoding="utf-8"))
    work = Path(plan_path).parent
    wj = json.loads((work / "words.json").read_text(encoding="utf-8"))
    tr = json.loads((work / "track.json").read_text())
    W, H = [int(v * scale) // 2 * 2 for v in plan.get("size", [1080, 1920])]
    C.update(plan=plan, work=work, words=wj["words"], cuts=wj["cuts"], src_dur=wj["dur"],
             dur=wj["dur"] + plan.get("tail", 0.0), track=tr, W=W, H=H, u=W / 1080,
             accent=bgr(plan.get("captions", {}).get("accent", "#FFD23F")), cap=plan.get("captions", {}))
    gw, gh = 180, int(180 * H / W)
    C["grid"] = np.meshgrid(np.linspace(0, 1, gw, dtype=np.float32), np.linspace(0, 1, gh, dtype=np.float32))
    C["chunks"] = chunk_words(C["words"], C["cap"].get("words", 3)) if plan.get("captions") is not None else []
    C["fx"] = sorted(plan.get("fx", []), key=lambda f: ORDER.get(f["type"], 9))
    shakes = []
    C["pushes"], C["bumps"] = [], []  # a pooled worker can run setup() twice; never accumulate
    for f in plan.get("fx", []):
        if f["type"] == "fire":
            shakes.append((at(f["at"]), 14))
        elif f["type"] == "bulb":
            shakes.append((at(f.get("on", f["at"])), 9))
            C.setdefault("pushes", []).append(at(f.get("on", f["at"])))  # signature moment: push in and hold
        elif f["type"] == "pop":
            shakes.append((at(f["tokens"][f.get("accent", len(f["tokens"]) - 1)][1]), 10))
            C.setdefault("bumps", []).append(at(f["tokens"][f.get("accent", len(f["tokens"]) - 1)][1]))
    C["shakes"] = shakes
    # finishing: vignette + fine grain tie phone footage and graphics into one look (precomputed, deterministic)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r2 = ((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2
    C["vignette"] = np.clip(1 - 0.22 * (r2 - 0.35), 0.72, 1.0)[..., None].astype(np.float32)
    C["grain"] = np.random.default_rng(11).normal(0, 3.2, (256, 256)).astype(np.float32)


def frame_at(i, src):
    """src = decoded cut.mp4 frame (uint8) for this instant. Returns the finished frame (uint8)."""
    t = i / FPS
    C["i"], C["boxes"] = i, []
    W, H, u = C["W"], C["H"], C["u"]
    sh, sw = src.shape[:2]
    n = len(C["track"]["boxes"])
    fcx, fcy, fw, fh = C["track"]["boxes"][min(int(round(min(t, C["src_dur"]) * FPS)), n - 1)]
    # camera: punch-in on alternate shots hides the jump cuts; similarity transform only (faces never squash)
    shot = sum(1 for c in C["cuts"] if c <= min(t, C["src_dur"] - 1e-3))
    edges = [0] + C["cuts"] + [C["src_dur"]]
    long_shot = edges[shot + 1] - edges[shot] >= 0.6
    z = C["plan"].get("punch", 1.12) if shot % 2 and long_shot else 1.0
    for t0 in C.get("pushes", []):
        z *= 1 + 0.07 * ease((t - t0) / 0.6) if t >= t0 else 1
    for t0 in C.get("bumps", []):
        if 0 <= t - t0 < 0.5:
            z *= 1 + 0.04 * math.sin(math.pi * (t - t0) / 0.5)
    if t > C["src_dur"]:  # tail: slow push on the frozen last frame
        z *= 1 + 0.06 * ease((t - C["src_dur"]) / max(C["plan"].get("tail", 1), 0.1))
    s = max(W / sw, H / sh) * z * 1.03  # 3% overscan = room to shake without showing an edge
    cx = clamp(fcx * sw, W / (2 * s), sw - W / (2 * s)) if W / (2 * s) < sw / 2 else sw / 2
    cy = clamp(fcy * sh, H / (2 * s), sh - H / (2 * s)) if H / (2 * s) < sh / 2 else sh / 2
    dx = dy = 0.0
    for t0, amp in C["shakes"]:
        if 0 <= t - t0 < 0.5:
            dec = amp * u * math.exp(-(t - t0) * 9)
            dx += dec * math.sin((t - t0) * 2 * math.pi * 13)
            dy += dec * math.cos((t - t0) * 2 * math.pi * 11)
    M = np.float32([[s, 0, W / 2 - s * cx + dx], [0, s, H / 2 - s * cy + dy]])
    frame = cv2.warpAffine(src, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT).astype(np.float32)
    fx0, fy0 = M[0, 0] * (fcx - fw / 2) * sw + M[0, 2], M[1, 1] * (fcy - fh / 2) * sh + M[1, 2]
    fx1, fy1 = fx0 + M[0, 0] * fw * sw, fy0 + M[1, 1] * fh * sh
    # Haar's box runs hairline -> chin; beards and jaws hang lower, so the no-text zone extends 20% down
    face = (fx0, fy0, fx1, fy1 + 0.2 * (fy1 - fy0))
    for f in C["fx"]:
        FX[f["type"]](frame, t, f, face)
    frame *= C["vignette"]
    if C["chunks"]:
        captions(frame, t, face)
    g = np.roll(C["grain"], (i * 37) % 256, axis=(0, 1))  # new grain every frame, same grain for the same frame
    frame += np.tile(g, (H // 256 + 1, W // 256 + 1))[:H, :W, None]
    hits = [name for name, b in C["boxes"] if b and name != "bulb" and overlap(b, face) > 0.12]
    return np.clip(frame, 0, 255).astype(np.uint8), hits


def overlap(b, f):
    ix = max(0, min(b[2], f[2]) - max(b[0], f[0]))
    iy = max(0, min(b[3], f[3]) - max(b[1], f[1]))
    return ix * iy / max(1, (b[2] - b[0]) * (b[3] - b[1]))


# ---------------------------------------------------------------- chunked parallel render
def render_chunk(job):
    plan_path, scale, f0, f1, out, fast = job
    setup(plan_path, scale)
    cut = str(C["work"] / "cut.mp4")
    sw, sh = C["track"]["w"], C["track"]["h"]
    nsrc = len(C["track"]["boxes"])
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{min(f0, nsrc - 1) / FPS:.4f}", "-i", cut,
                            "-frames:v", str(max(1, min(f1, nsrc) - f0)), "-f", "rawvideo",
                            "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{C['W']}x{C['H']}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "ultrafast" if fast else "fast",
                            "-crf", "23" if fast else "17", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    last, warn = None, {}
    for i in range(f0, f1):
        if i < nsrc or last is None:  # a tail-only chunk still needs the last real frame once
            buf = dec.stdout.read(sw * sh * 3)
            if len(buf) == sw * sh * 3:
                last = np.frombuffer(buf, np.uint8).reshape(sh, sw, 3)
        img, hits = frame_at(i, last)  # past the end of the cut: hold the last frame (tail freeze)
        for h in hits:
            warn.setdefault(h, []).append(i / FPS)
        enc.stdin.write(img.tobytes())
    dec.stdout.read()  # drain so the decoder exits cleanly
    dec.wait()
    enc.stdin.close()
    enc.wait()
    return warn


# ---------------------------------------------------------------- sound design (synthesised, deterministic)
SR = 48000


def sfx_track(dur):
    rng = np.random.default_rng(3)
    n = int(dur * SR) + SR
    out = np.zeros(n, np.float32)

    def put(sig, t, gain):
        k = int(t * SR)
        if 0 <= k < n:
            m = min(len(sig), n - k)
            out[k:k + m] += sig[:m] * gain

    def tt(d):
        return np.arange(int(d * SR)) / SR

    def lowpass(x, k):
        return np.convolve(x, np.ones(k) / k, "same")

    pop = np.sin(2 * np.pi * np.cumsum(900 * np.exp(-tt(0.09) * 25) + 250) / SR) * np.exp(-tt(0.09) * 45)
    f = 110 * np.exp(-tt(0.6) * 8) + 45
    hit = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt(0.6) * 7) + rng.standard_normal(len(f)) * np.exp(-tt(0.6) * 120) * 0.4
    wn = rng.standard_normal(int(0.5 * SR))
    whoosh = (lowpass(wn, 24) - lowpass(wn, 220)) * np.sin(np.pi * np.linspace(0, 1, len(wn))) ** 2 * 3
    ding = sum(a * np.sin(2 * np.pi * fr * tt(1.4)) * np.exp(-tt(1.4) * d) for fr, a, d in
               [(1318.5, 1.0, 3), (2637, 0.45, 5), (3955, 0.2, 8)])
    for f_ in C["plan"].get("fx", []):
        ty = f_["type"]
        if ty == "pop":
            toks = f_["tokens"]
            acc = f_.get("accent", len(toks) - 1)
            for j, (_, ref) in enumerate(toks):
                put(hit if j == acc else pop, at(ref), 0.5 if j == acc else 0.35)
        elif ty in ("fire", "smoke"):
            a, b = at(f_["at"]), span_end(f_)
            put(whoosh, a - 0.25, 0.5 if ty == "fire" else 0.3)
            if ty == "fire":
                d = b - a + 0.5
                rumble = lowpass(rng.standard_normal(int(d * SR)), 300) * 6
                clicks = (rng.random(int(d * SR)) < 40 / SR) * rng.standard_normal(int(d * SR))
                crackle = rumble + np.convolve(clicks, np.exp(-np.arange(150) / 25), "same")
                put(crackle * np.minimum(1, np.minimum(tt(d) / 0.2, (d - tt(d)) / 0.4)), a, 0.25)
        elif ty == "bulb":
            put(whoosh, at(f_["at"]) - 0.3, 0.25)
            put(pop, at(f_["at"]) + 0.12, 0.35)
            put(ding, at(f_.get("on", f_["at"])), 0.3)
    return out[: int(dur * SR)]


def write_wav(path, x):
    x = np.clip(x, -1, 1)
    pcm = (np.repeat(x[:, None], 2, 1) * 32767).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def contact_sheet(video, times, out, labels):
    tiles = []
    for t, lab in zip(times, labels):
        p = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(video), "-frames:v", "1", "-vf",
                            "scale=270:-2", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
        if not p.stdout:
            continue
        im = Image.frombytes("RGB", (270, len(p.stdout) // (270 * 3)), p.stdout)
        ImageDraw.Draw(im).text((6, 4), f"{t:.2f}s {lab}", fill=(255, 255, 0))
        tiles.append(im)
    cols = 6
    rows = math.ceil(len(tiles) / cols)
    sheet = Image.new("RGB", (cols * 270, rows * tiles[0].height), (0, 0, 0))
    for k, im in enumerate(tiles):
        sheet.paste(im, ((k % cols) * 270, (k // cols) * im.height))
    sheet.save(out, quality=88)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--range", default=None, help="a:b seconds, implies --preview")
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 2))
    a = ap.parse_args()
    fast = a.preview or a.range
    scale = 0.5 if fast else 1.0
    setup(a.plan, scale)
    work, plan = C["work"], C["plan"]
    total = int(round(C["dur"] * FPS))
    f0, f1 = (0, total) if not a.range else [int(float(v) * FPS) for v in a.range.split(":")]
    out = work / ("preview.mp4" if fast else plan.get("out", "final.mp4"))
    tmp = work / ".chunks"
    tmp.mkdir(exist_ok=True)
    t_start = time.time()
    n = max(1, min(a.workers, (f1 - f0) // 30))
    bounds = np.linspace(f0, f1, n + 1).astype(int)
    jobs = [(a.plan, scale, int(bounds[k]), int(bounds[k + 1]), str(tmp / f"c{k:03d}.mp4"), fast) for k in range(n)]
    with Pool(n) as pool:
        warns = pool.map(render_chunk, jobs)
    (tmp / "list.txt").write_text("".join(f"file '{Path(j[4]).name}'\n" for j in jobs))
    sfx = tmp / "sfx.wav"
    write_wav(sfx, sfx_track(C["dur"]) if plan.get("sfx", True) else np.zeros(int(C["dur"] * SR), np.float32))
    ss, d = f0 / FPS, (f1 - f0) / FPS
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(tmp / "list.txt"),
                    "-ss", f"{ss:.3f}", "-t", f"{d:.3f}", "-i", str(work / "cut.mp4"),
                    "-ss", f"{ss:.3f}", "-t", f"{d:.3f}", "-i", str(sfx),
                    "-filter_complex", "[1:a]apad[sp];[sp][2:a]amix=inputs=2:duration=longest:normalize=0,"
                    "alimiter=limit=0.95[a]", "-map", "0:v", "-map", "[a]", "-t", f"{d:.3f}", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)], check=True)
    for p in tmp.iterdir():
        p.unlink()
    tmp.rmdir()
    took = time.time() - t_start
    print(f"rendered {out.name}: {d:.1f}s video, {f1 - f0} frames in {took:.1f}s ({(f1 - f0) / took:.0f} fps, {n} workers)")

    merged = {}
    for w in warns:
        for k, v in w.items():
            merged.setdefault(k, []).extend(v)
    for k, v in merged.items():
        print(f"  FACE COVERED by {k}: {min(v):.2f}-{max(v):.2f}s ({len(v)} frames) -> move its y")
    marks = [(0.2, "open")]
    for f in plan.get("fx", []):
        for key in ("at", "on", "until"):
            if key in f and f[key] != "end":
                marks.append((at(f[key]) + (0.35 if key != "until" else -0.3), f"{f['type']}.{key}"))
        if f["type"] == "pop":
            marks.append((at(f["tokens"][-1][1]) + 0.2, "pop.accent"))
    marks.append((C["dur"] - 0.2, "end"))
    marks = sorted((m for m in marks if ss <= m[0] < ss + d), key=lambda m: m[0])
    if marks:
        contact_sheet(out, [m[0] - ss for m in marks], work / "sheet.jpg", [m[1] for m in marks])
        print(f"  sheet: {work / 'sheet.jpg'}")


if __name__ == "__main__":
    sys.exit(main())
