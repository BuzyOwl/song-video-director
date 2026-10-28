// KEEP IN SYNC with remotion/src/Camera.ts
const ease = (x) => { x = Math.min(1, Math.max(0, x)); return 1 - (1 - x) ** 3; };
const spring = (x, k = 6, w = 10) => (x <= 0 ? 0 : 1 - Math.exp(-k * x) * Math.cos(w * x));
export const OVERSCAN = 1.03;

export const faceIndex = (p, t) =>
  Math.min(p.face.length - 1, Math.max(0, Math.round(Math.min(t, p.srcDur - 1e-3) * p.fps)));

export const camera = (p, t) => {
  const srcT = Math.min(t, p.srcDur - 1e-3);
  const shot = p.cuts.filter((c) => c <= srcT).length;
  const edges = [0, ...p.cuts, p.srcDur];
  const longShot = edges[shot + 1] - edges[shot] >= 0.6;
  let z = shot % 2 === 1 && longShot ? p.punch : 1;
  for (const ev of p.zoom) {
    const dt = t - ev.t;
    if (dt >= 0 && dt < 0.9) z *= 1 + (ev.z - 1) * Math.min(1, spring(dt, 9, 14)) * (1 - ease((dt - 0.4) / 0.5));
  }
  if (t > p.srcDur) z *= 1 + 0.06 * ease((t - p.srcDur) / Math.max(p.dur - p.srcDur, 0.1));
  z = Math.max(1, z) * OVERSCAN;
  const [fcx, fcy] = p.face[faceIndex(p, t)] ?? [0.5, 0.4];
  const half = 0.5 / z;
  const cx = Math.min(1 - half, Math.max(half, fcx));
  const cy = Math.min(1 - half, Math.max(half, fcy));
  return {z, cx, cy};
};

export const faceBox = (p, t) => {
  const {z, cx, cy} = camera(p, t);
  const [fcx, fcy, fw, fh] = p.face[faceIndex(p, t)] ?? [0.5, 0.4, 0.4, 0.22];
  const sx = (x) => (0.5 + (x - cx) * z) * p.w;
  const sy = (y) => (0.5 + (y - cy) * z) * p.h;
  return [sx(fcx - fw / 2), sy(fcy - fh / 2), sx(fcx + fw / 2), sy(fcy + fh / 2 + 0.2 * fh)];
};
