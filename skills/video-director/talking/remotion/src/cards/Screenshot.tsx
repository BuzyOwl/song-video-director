// browser-chrome frame, slow pan
import {Img, staticFile} from 'remotion';
import type {ReelProps, Card} from '../types';
import {ease, enter, exit, lane} from './util';
export const Screenshot = ({p, t, c}: {p: ReelProps; t: number; c: Extract<Card, {type: 'screenshot'}>}) => {
  const k = enter(t, c.s) * exit(t, c.e);
  const prog = ease((t - c.s) / Math.max(0.5, c.e - c.s));
  // 'down' scrolls the page up (0 -> -35%); 'up' starts scrolled and returns to the top (-35% -> 0): never a blank band
  const pan = c.pan === 'none' ? 0 : c.pan === 'down' ? -prog * 0.35 : (prog - 1) * 0.35;
  return (
    <div style={lane(c.y, p.h)}>
      <div style={{width: 0.86 * p.w, height: 0.4 * p.h, borderRadius: 22, overflow: 'hidden', background: '#111', boxShadow: '0 24px 50px rgba(0,0,0,.5)',
        transform: `scale(${0.7 + 0.3 * k})`, opacity: Math.min(1, k * 2)}}>
        <div style={{height: 44, background: '#2a2a2e', display: 'flex', gap: 8, alignItems: 'center', padding: '0 16px'}}>
          {['#ff5f57', '#febc2e', '#28c840'].map((col) => <div key={col} style={{width: 14, height: 14, borderRadius: 7, background: col}} />)}
        </div>
        <div style={{position: 'relative', height: 'calc(100% - 44px)', overflow: 'hidden'}}>
          <Img src={staticFile(c.src)} style={{width: '100%', display: 'block', transform: `translateY(${pan * 100}%)`}} />
        </div>
      </div>
    </div>
  );
};
