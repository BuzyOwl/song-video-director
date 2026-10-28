import type {ReelProps, Card} from '../types';
import {big, enter, exit, lane, Panel} from './util';
export const Quote = ({p, t, c}: {p: ReelProps; t: number; c: Extract<Card, {type: 'quote'}>}) => {
  const k = enter(t, c.s) * exit(t, c.e);
  return (
    <div style={lane(c.y, p.h)}>
      <Panel style={{maxWidth: 0.86 * p.w, transform: `translateY(${(1 - k) * 40}px)`, opacity: k}}>
        <div style={{...big(p.font, 54 * p.w / 1080), textTransform: 'none', fontStyle: 'italic'}}>“{c.text}”</div>
        {c.by && <div style={{...big(p.font, 34 * p.w / 1080, p.accent), marginTop: 10}}>— {c.by}</div>}
      </Panel>
    </div>
  );
};
