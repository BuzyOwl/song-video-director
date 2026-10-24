import type {ReelProps, Card} from '../types';
import {big, enter, exit, lane} from './util';
export const Title = ({p, t, c}: {p: ReelProps; t: number; c: Extract<Card, {type: 'title'}>}) => {
  const k = enter(t, c.s) * exit(t, c.e);
  return <div style={lane(c.y, p.h)}><div style={{...big(p.font, (c.size ?? 120) * p.w / 1080), transform: `scale(${k})`, opacity: Math.min(1, k * 3), textAlign: 'center', maxWidth: 0.9 * p.w}}>{c.text}</div></div>;
};
