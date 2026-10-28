import type {ReelProps, Card} from '../types';
import {big, enter, exit, Panel} from './util';
export const LowerThird = ({p, t, c}: {p: ReelProps; t: number; c: Extract<Card, {type: 'lowerthird'}>}) => {
  const k = enter(t, c.s) * exit(t, c.e);
  return (
    <div style={{position: 'absolute', left: 0.06 * p.w, top: c.y * p.h, transform: `translate(${(k - 1) * 120}px, -50%)`, opacity: k}}>
      <Panel style={{borderLeft: `10px solid ${p.accent}`, borderRadius: 18}}>
        <div style={big(p.font, 56 * p.w / 1080)}>{c.text}</div>
        {c.sub && <div style={{...big(p.font, 36 * p.w / 1080, 'rgba(255,255,255,.75)'), textTransform: 'none'}}>{c.sub}</div>}
      </Panel>
    </div>
  );
};
