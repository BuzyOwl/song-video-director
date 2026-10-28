// a paper cutout with a torn/strip/newspaper frame; drift = slow float, drop = falls in
import {Img, staticFile} from 'remotion';
import type {ReelProps, Card} from '../types';
import {enter, exit, lane} from './util';
const FRAME = {
  torn: {padding: 14, background: '#f3efe4', clipPath: 'polygon(1% 3%, 8% 0, 30% 2%, 52% 0, 75% 2%, 97% 0, 100% 10%, 99% 40%, 100% 70%, 98% 100%, 70% 98%, 48% 100%, 25% 98%, 2% 100%, 0 70%, 1% 35%)'},
  strip: {padding: 10, background: '#fff', border: '3px solid #111'},
  news: {padding: 18, background: '#efe9d6', border: '2px solid #2b2b2b', outline: '6px solid #efe9d6'},
};
export const Cutout = ({p, t, c}: {p: ReelProps; t: number; c: Extract<Card, {type: 'cutout'}>}) => {
  const k = enter(t, c.s) * exit(t, c.e);
  const dt = t - c.s;
  const drift = c.motion === 'drift' ? `translate(${Math.sin(dt * 0.9) * 10}px, ${Math.cos(dt * 0.7) * 8}px) rotate(${-2 + Math.sin(dt * 0.5)}deg)`
    : c.motion === 'drop' ? `translateY(${(1 - k) * -220}px) rotate(${(1 - k) * -8 - 2}deg)` : 'rotate(-2deg)';
  return (
    <div style={lane(c.y, p.h)}>
      <div style={{...FRAME[c.frame], transform: `${drift} scale(${0.6 + 0.4 * k})`, opacity: Math.min(1, k * 2), boxShadow: '0 24px 50px rgba(0,0,0,.5)', maxWidth: 0.8 * p.w}}>
        <Img src={staticFile(c.src)} style={{width: '100%', display: 'block', maxHeight: 0.42 * p.h, objectFit: 'cover'}} />
      </div>
    </div>
  );
};
