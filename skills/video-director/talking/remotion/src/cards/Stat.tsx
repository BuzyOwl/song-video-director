// tokens spring in on their words; the last token is the accent
import type {ReelProps, Card} from '../types';
import {big, exit, lane, spring} from './util';
export const Stat = ({p, t, c}: {p: ReelProps; t: number; c: Extract<Card, {type: 'stat'}>}) => {
  const out = exit(t, c.e);
  const size = (c.size ?? 160) * p.w / 1080;
  return (
    <div style={{...lane(c.y, p.h), gap: size * 0.18, opacity: out}}>
      {c.tokens.map((tk, i) => {
        const k = Math.min(1, spring(t - tk.t));
        const acc = i === c.tokens.length - 1;
        return <div key={i} style={{...big(p.font, size, acc ? p.accent : '#fff'), transform: `scale(${k})`, opacity: t >= tk.t ? 1 : 0,
          filter: acc && t >= tk.t ? `drop-shadow(0 0 ${18 * p.w / 1080}px ${p.accent})` : undefined}}>{tk.text}</div>;
      })}
    </div>
  );
};
