import type {CSSProperties, ReactNode} from 'react';
import {fontStack, SHADOW} from '../theme';
export const spring = (x: number, k = 7, w = 11) => (x <= 0 ? 0 : 1 - Math.exp(-k * x) * Math.cos(w * x));
export const ease = (x: number) => { x = Math.min(1, Math.max(0, x)); return 1 - (1 - x) ** 3; };
export const enter = (t: number, s: number) => Math.min(1, spring(t - s));
export const exit = (t: number, e: number) => 1 - ease((t - e) / 0.22);
export const lane = (y: number, h: number): CSSProperties => ({position: 'absolute', left: 0, right: 0, top: y * h,
  transform: 'translateY(-50%)', display: 'flex', justifyContent: 'center', pointerEvents: 'none'});
export const Panel = ({children, style}: {children: ReactNode; style?: CSSProperties}) => (
  <div style={{background: 'rgba(12,12,16,.72)', backdropFilter: 'blur(14px)', border: '2px solid rgba(255,255,255,.14)',
    borderRadius: 28, padding: '22px 36px', boxShadow: '0 20px 60px rgba(0,0,0,.45)', ...style}}>{children}</div>
);
export const big = (font: string, size: number, color = '#fff'): CSSProperties => ({fontFamily: fontStack(font),
  fontWeight: font === 'Poppins-Bold' ? 700 : 800, fontSize: size, lineHeight: 1.05, textTransform: 'uppercase',
  letterSpacing: '-0.015em', color, textShadow: SHADOW,
  WebkitTextStroke: `${Math.max(2, size / 20)}px rgba(0,0,0,.9)`, paintOrder: 'stroke fill'});
