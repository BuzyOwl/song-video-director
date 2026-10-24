import {AbsoluteFill, Audio, Freeze, OffthreadVideo, Sequence, useCurrentFrame, useVideoConfig, staticFile, delayRender, continueRender, cancelRender} from 'remotion';
import {useEffect, useMemo, useState} from 'react';
import type {ReelProps} from './types';
import {camera, faceIndex} from './Camera';
import {Backdrop, Board, pipGeo, pipK} from './cards/Board';
import {Captions} from './Captions';
import {Cards} from './cards';
import {ensureFonts, fontStack} from './theme';

export const Reel = (p: ReelProps) => {
  const [h] = useState(() => delayRender('fonts'));
  useEffect(() => { ensureFonts().then(() => continueRender(h)).catch((e) => cancelRender(e)); }, [h]);
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const lastSrcFrame = Math.round(p.srcDur * p.fps) - 1;
  const {z, cx, cy} = camera(p, t);
  // PiP morph (k 0 -> 1 while a board is up): scale/centre/position lerp from the camera to a face-centred bubble, circle clip closes in log space
  const k = pipK(p, t), g = pipGeo(p);
  const fw = useMemo(() => p.face.map((f) => f[2]).sort((a, b) => a - b)[p.face.length >> 1] ?? 0.4, [p.face]);
  const sP = (0.68 * g.d) / (fw * p.w);            // face width ~68 % of the bubble (room to centre it); median width so it does not breathe
  const [fx, fy, , fh] = p.face[faceIndex(p, t)] ?? [0.5, 0.4, 0.4, 0.22];
  const hx = g.d / 2 / (sP * p.w), hy = g.d / 2 / (sP * p.h);
  const pcx = Math.min(1 - hx, Math.max(hx, fx)), pcy = Math.min(1 - hy, Math.max(hy, fy + 0.08 * fh));
  const L = (a: number, b: number) => a + (b - a) * k;
  const S = L(z, sP), X = L(p.w / 2, g.x), Y = L(p.h / 2, g.y);
  const R = Math.exp(L(Math.log(Math.hypot(p.w, p.h)), Math.log(g.d / 2)));
  const tf = `translate(${X - p.w / 2}px, ${Y - p.h / 2}px) scale(${S}) translate(${(0.5 - L(cx, pcx)) * p.w}px, ${(0.5 - L(cy, pcy)) * p.h}px)`;
  return (
    <AbsoluteFill style={{background: '#000'}}>
      {k > 0 && <Backdrop p={p} t={t} />}
      {k > 0 && p.cards.map((c) => c.type === 'board' && c.s - 0.1 <= t && t <= c.e + 0.3 ? <Board key={c.id} p={p} t={t} c={c} /> : null)}
      <AbsoluteFill style={{clipPath: k > 0 ? `circle(${R}px at ${X}px ${Y}px)` : undefined}}>
        <AbsoluteFill style={{transform: tf, transformOrigin: '50% 50%'}}>
          <Freeze frame={lastSrcFrame} active={frame > lastSrcFrame}>
            <OffthreadVideo src={staticFile(p.src)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
          </Freeze>
        </AbsoluteFill>
      </AbsoluteFill>
      {k > 0 && <div style={{position: 'absolute', left: X - R, top: Y - R, width: 2 * R, height: 2 * R, borderRadius: '50%', boxSizing: 'border-box',
        border: `${6 * p.w / 1080}px solid ${p.accent}`, boxShadow: '0 24px 60px rgba(0,0,0,.55)', opacity: Math.min(1, Math.max(0, (k - 0.5) * 2))}} />}
      <Cards p={p} t={t} />
      <Captions p={p} t={t} />
      {p.sfx.map((s, i) => (
        <Sequence key={i} from={Math.round(s.t * fps)} durationInFrames={Math.round(1.5 * fps)}>
          <Audio src={staticFile(`sfx/${s.name}.wav`)} volume={s.gain} />
        </Sequence>
      ))}
      {p.debugText && (
        <div style={{position: 'absolute', top: 200, left: 40, fontSize: 140, color: '#fff', fontFamily: fontStack(p.font), fontWeight: 800}}>
          {p.debugText}
        </div>
      )}
    </AbsoluteFill>
  );
};
