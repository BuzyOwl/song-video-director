// full-screen slide; while any board is up the speaker shrinks into a PiP bubble (top-right, see pipGeo + Reel.tsx)
import {AbsoluteFill, OffthreadVideo, Sequence, staticFile} from 'remotion';
import type {CSSProperties} from 'react';
import type {ReelProps, Card, Timed} from '../types';
import {fontStack} from '../theme';
import {ease, exit, spring} from './util';

type B = Extract<Card, {type: 'board'}>;
const MONO = "Consolas, 'Courier New', monospace";
const CPS = 34;   // typing speed, chars per second

/** PiP bubble: centre x/y and diameter in output px. Board text keeps left of x - d/2 and below y + d/2. */
export const pipGeo = (p: ReelProps) => { const d = 0.36 * p.w; return {x: p.w - 0.055 * p.w - d / 2, y: 0.078 * p.h + d / 2, d}; };

/** 0 = full-frame speaker, 1 = PiP. Boards closer than 0.6 s merge so the bubble does not bounce between slides. */
export const pipK = (p: ReelProps, t: number) => {
  const bs = p.cards.filter((c) => c.type === 'board').map((c) => [c.s, c.e]).sort((a, b) => a[0] - b[0]);
  const spans: number[][] = [];
  for (const b of bs) { const l = spans[spans.length - 1]; if (l && b[0] - l[1] < 0.6) l[1] = Math.max(l[1], b[1]); else spans.push([...b]); }
  return Math.max(0, ...spans.map(([s, e]) => ease((t - s) / 0.5) * (1 - ease((t - e) / 0.5))));
};

export const Backdrop = ({p, t}: {p: ReelProps; t: number}) => (
  <AbsoluteFill style={{background: `radial-gradient(circle at ${18 + 6 * Math.sin(t * 0.3)}% ${14 + 5 * Math.cos(t * 0.23)}%, ${p.accent}30, transparent 46%),
    radial-gradient(circle at 88% 92%, #3b5bff26, transparent 52%), #0b0c10`}}>
    <AbsoluteFill style={{backgroundImage: 'radial-gradient(rgba(255,255,255,.07) 2px, transparent 2.6px)', backgroundSize: `${40 * p.w / 1080}px ${40 * p.w / 1080}px`}} />
  </AbsoluteFill>
);

// latest item due at t, typed in; an item that extends the previous one keeps the shared prefix instead of retyping it
const typed = (items: Timed[], t: number) => {
  const i = items.map((it) => it.t <= t).lastIndexOf(true);
  if (i < 0) return null;
  const cur = items[i], prev = items[i - 1];
  const from = prev && cur.text.startsWith(prev.text) ? prev.text.length : 0;
  return cur.text.slice(0, from + Math.floor((t - cur.t) * CPS) + 1);
};

export const Board = ({p, t, c}: {p: ReelProps; t: number; c: B}) => {
  // HyperFrames board (compile.mjs hfBoard): the rendered clip is the slide; its frame 0 is the board's start
  if (c.clip) return (
    <AbsoluteFill style={{opacity: exit(t, c.e)}}>
      <Sequence from={Math.round(c.s * p.fps)} layout="none">
        <OffthreadVideo muted src={staticFile(c.clip)} style={{position: 'absolute', width: '100%', height: '100%'}} />
      </Sequence>
    </AbsoluteFill>
  );
  const u = p.w / 1080, g = pipGeo(p);
  const font = fontStack(p.font), wt = p.font === 'Poppins-Bold' ? 700 : 800;
  const out = exit(t, c.e);
  const rise = (d: number): CSSProperties => { const k = Math.min(1, spring(t - c.s - d)); return {opacity: Math.min(1, Math.max(0, k * 2)), transform: `translateY(${(1 - k) * 50 * u}px)`}; };
  const txt = (size: number, color = '#fff', extra: CSSProperties = {}): CSSProperties => ({fontFamily: font, fontWeight: wt, fontSize: size * u, lineHeight: 1.08, color, ...extra});
  const longest = Math.max(...c.title.split(/\s+/).map((w) => w.length));
  const titleSize = Math.min(112, 0.88 * 1080 / (longest * 0.7));
  const shown = typed(c.prompt, t);
  const blink = Math.floor(t * 2.4) % 2 === 0;
  return (
    <AbsoluteFill style={{opacity: out, transform: `translateY(${(1 - out) * -30 * u}px)`}}>
      <div style={{position: 'absolute', left: 64 * u, top: g.y - g.d / 2, width: g.x - g.d / 2 - 100 * u, height: g.d, display: 'flex', flexDirection: 'column', justifyContent: 'center'}}>
        {c.n && <div style={{...txt(230, p.accent, {lineHeight: 0.9, letterSpacing: '-0.04em', textShadow: `0 0 ${40 * u}px ${p.accent}55`}), ...rise(0)}}>{c.n}</div>}
        {c.kicker && <div style={{...txt(32, p.accent, {textTransform: 'uppercase', letterSpacing: '0.14em', marginTop: 14 * u}), ...rise(0.05)}}>{c.kicker}</div>}
      </div>
      <div style={{position: 'absolute', left: 64 * u, right: 64 * u, top: g.y + g.d / 2 + 50 * u, display: 'flex', flexDirection: 'column', gap: 34 * u}}>
        <div style={{...txt(titleSize, '#fff', {textTransform: 'uppercase', letterSpacing: '-0.02em', lineHeight: 0.98}), ...rise(0.08)}}>{c.title}</div>
        {c.sub && <div style={{...txt(48, 'rgba(255,255,255,.78)', {fontWeight: 700}), ...rise(0.16)}}>{c.sub}</div>}
        {c.prompt.length > 0 && (
          <div style={{...rise(0.26), background: '#16171e', border: `${2 * u}px solid rgba(255,255,255,.14)`, borderRadius: 30 * u, padding: `${30 * u}px ${34 * u}px`,
            display: 'flex', alignItems: 'flex-end', gap: 24 * u, boxShadow: '0 24px 60px rgba(0,0,0,.45)', minHeight: 150 * u}}>
            <div style={{flex: 1, fontFamily: MONO, fontSize: 44 * u, lineHeight: 1.3, color: shown ? '#fff' : 'rgba(255,255,255,.4)', whiteSpace: 'pre-wrap'}}>
              {shown ?? 'Ask anything…'}<span style={{color: p.accent, opacity: blink ? 1 : 0}}>▍</span>
            </div>
            <div style={{width: 70 * u, height: 70 * u, borderRadius: 35 * u, flexShrink: 0, background: shown ? p.accent : 'rgba(255,255,255,.18)',
              display: 'flex', alignItems: 'center', justifyContent: 'center', ...txt(40, '#0b0c10')}}>↑</div>
          </div>
        )}
        {c.rows.length > 0 && (
          <div style={{display: 'flex', flexDirection: 'column', gap: 22 * u}}>
            {c.rows.map((r, i) => {
              const k = Math.min(1, spring(t - r.t));
              return <div key={i} style={{display: 'flex', alignItems: 'center', gap: 26 * u, opacity: t >= r.t ? 1 : 0.18, transform: `translateX(${(1 - k) * -40 * u}px)`}}>
                <div style={{...txt(34, '#0b0c10', {textTransform: 'uppercase', letterSpacing: '0.06em'}), background: t >= r.t ? p.accent : 'rgba(255,255,255,.5)',
                  borderRadius: 14 * u, padding: `${12 * u}px ${20 * u}px`, width: 250 * u, textAlign: 'center', flexShrink: 0}}>{r.label}</div>
                <div style={txt(46, '#fff', {fontWeight: 700})}>{t >= r.t ? r.text.slice(0, Math.floor((t - r.t) * CPS) + 1) : ''}</div>
              </div>;
            })}
          </div>
        )}
        {c.chips.length > 0 && (
          <div style={{...rise(0.3)}}>
            {c.label && <div style={{...txt(30, p.accent, {textTransform: 'uppercase', letterSpacing: '0.14em', marginBottom: 18 * u}), opacity: t >= c.chips[0].t ? 1 : 0}}>{c.label}</div>}
            <div style={{display: 'flex', flexWrap: 'wrap', gap: 16 * u}}>
              {c.chips.map((ch, i) => {
                const k = Math.min(1, spring(t - ch.t, 9, 13));
                return <div key={i} style={{...txt(38, '#fff', {fontWeight: 700}), border: `${2 * u}px solid rgba(255,255,255,.28)`, background: 'rgba(255,255,255,.07)',
                  borderRadius: 999, padding: `${12 * u}px ${26 * u}px`, transform: `scale(${t >= ch.t ? k : 0})`, opacity: t >= ch.t ? 1 : 0}}>{ch.text}</div>;
              })}
            </div>
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
