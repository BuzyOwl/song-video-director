// hand-drawn accent arrow / circle / underline, draws on
import type {ReelProps, Card} from '../types';
import {ease, exit} from './util';
export const Arrow = ({p, t, c}: {p: ReelProps; t: number; c: Extract<Card, {type: 'arrow'}>}) => {
  const d = ease((t - c.s) / 0.35) * exit(t, c.e);
  const [x0, y0] = [c.from[0] * p.w, c.from[1] * p.h], [x1, y1] = [c.to[0] * p.w, c.to[1] * p.h];
  const sw = 14 * p.w / 1080;
  const common = {fill: 'none', stroke: p.accent, strokeWidth: sw, strokeLinecap: 'round' as const, strokeLinejoin: 'round' as const,
    style: {filter: 'drop-shadow(0 3px 0 rgba(0,0,0,.6))'}};
  let path: string, len: number;
  if (c.shape === 'circle') {  // ellipse that hugs the from/to box (not its diagonal), slightly loose and hand-drawn
    const rx = Math.abs(x1 - x0) / 2 * 1.08, ry = Math.abs(y1 - y0) / 2 * 1.08, cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
    path = `M ${cx + rx} ${cy} A ${rx} ${ry} -6 1 1 ${cx + rx} ${cy - 1}`; len = Math.PI * (rx + ry); }
  else if (c.shape === 'underline') { path = `M ${x0} ${y0} Q ${(x0 + x1) / 2} ${y0 + 18} ${x1} ${y1}`; len = Math.hypot(x1 - x0, y1 - y0) * 1.05; }
  else { const mx = (x0 + x1) / 2 + (y1 - y0) * 0.25, my = (y0 + y1) / 2 - (x1 - x0) * 0.25;
    path = `M ${x0} ${y0} Q ${mx} ${my} ${x1} ${y1}`; len = Math.hypot(x1 - x0, y1 - y0) * 1.2; }
  const ang = Math.atan2(y1 - y0, x1 - x0);
  const hl = 34 * p.w / 1080;
  const head = c.shape === 'arrow' && d > 0.95 ? `M ${x1 - hl * Math.cos(ang - 0.5)} ${y1 - hl * Math.sin(ang - 0.5)} L ${x1} ${y1} L ${x1 - hl * Math.cos(ang + 0.5)} ${y1 - hl * Math.sin(ang + 0.5)}` : '';
  return (
    <svg width={p.w} height={p.h} style={{position: 'absolute', inset: 0, pointerEvents: 'none'}}>
      <path d={path} {...common} strokeDasharray={len} strokeDashoffset={len * (1 - d)} />
      {head && <path d={head} {...common} />}
    </svg>
  );
};
