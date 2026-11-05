import {AbsoluteFill} from 'remotion';
import type {ReelProps} from './types';
import {fontStack, SHADOW} from './theme';

const spring = (x: number, k = 7, w = 12) => (x <= 0 ? 0 : 1 - Math.exp(-k * x) * Math.cos(w * x));
const clamp01 = (x: number) => Math.min(1, Math.max(0, x));

export const Captions = ({p, t}: {p: ReelProps; t: number}) => {
  const ch = p.chunks.find((c) => c.s <= t && t < c.e);
  if (!ch) return null;
  const size = Math.round(Math.max(70, p.capSize) * (p.w / 1080));  // >= 70 px at 1080 wide (hard rule)
  const inAlpha = clamp01((t - ch.s) / 0.05);
  const pop = 0.9 + 0.1 * clamp01((t - ch.s) / 0.1);
  // stroke is painted under the fill (paintOrder) so only its outer half shows: hairline, and no variable-font overlap artefacts
  return (
    <AbsoluteFill style={{justifyContent: 'flex-start', alignItems: 'center', pointerEvents: 'none'}}>
      <div style={{position: 'absolute', top: ch.y * p.h, transform: `translateY(-50%) scale(${pop})`, opacity: inAlpha,
        display: 'flex', gap: size * 0.28, maxWidth: p.w * 0.9, flexWrap: 'wrap', justifyContent: 'center',
        fontFamily: fontStack(p.font), fontWeight: p.font === 'Poppins-Bold' ? 700 : 800, fontSize: size, lineHeight: 1.1, textTransform: 'uppercase',
        letterSpacing: '-0.01em', color: '#fff', textShadow: SHADOW, WebkitTextStroke: `${Math.max(2, size / 20)}px rgba(0,0,0,.9)`, paintOrder: 'stroke fill'}}>
        {ch.words.map((w, i) => {
          const active = w.s <= t && t < w.e + 0.05;
          const k = w.key || /^\d/.test(w.w);
          const s = active ? 1 + 0.12 * Math.min(1, spring(t - w.s)) : 1;
          return (
            // the 1.12 pop grows a word 6 % per side: reserve that as margin (est. width 0.7 em/char) so a long active word never touches its neighbour
            <span key={i} style={{display: 'inline-block', transform: `scale(${s})`, color: k ? p.accent : '#fff', margin: `0 ${0.06 * 0.7 * size * w.w.length}px`,
              opacity: t >= w.s - 0.02 ? 1 : 0.45}}>
              {w.w.replace(/[.,;:]+$/, '')}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
