// items reveal on their words
import type {ReelProps, Card} from '../types';
import {big, enter, exit, lane, Panel, spring} from './util';
export const List = ({p, t, c}: {p: ReelProps; t: number; c: Extract<Card, {type: 'list'}>}) => {
  const out = exit(t, c.e);
  return (
    <div style={{...lane(c.y, p.h), opacity: out * enter(t, c.s)}}>
      <Panel style={{minWidth: 0.42 * p.w}}>
        {c.items.map((it, i) => {
          const k = Math.min(1, spring(t - it.t));
          return <div key={i} style={{display: 'flex', alignItems: 'center', gap: 20, transform: `translateX(${(1 - k) * -60}px)`, opacity: t >= it.t ? 1 : 0, margin: '8px 0'}}>
            <div style={{width: 22, height: 22, borderRadius: 11, background: p.accent}} />
            <div style={{...big(p.font, 52 * p.w / 1080), textTransform: 'none'}}>{it.text}</div>
          </div>;
        })}
      </Panel>
    </div>
  );
};
