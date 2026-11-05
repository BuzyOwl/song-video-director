// picture-in-picture image or video thumbnail in a corner
import {Img, staticFile} from 'remotion';
import type {ReelProps, Card} from '../types';
import {enter, exit} from './util';
export const Pip = ({p, t, c}: {p: ReelProps; t: number; c: Extract<Card, {type: 'pip'}>}) => {
  const k = enter(t, c.s) * exit(t, c.e);
  const pos = {tl: {left: 40, top: 0.08 * p.h}, tr: {right: 40, top: 0.08 * p.h}, bl: {left: 40, bottom: 0.22 * p.h}, br: {right: 40, bottom: 0.22 * p.h}}[c.corner];
  return <div style={{position: 'absolute', ...pos, width: 0.36 * p.w, borderRadius: 24, overflow: 'hidden', border: `4px solid ${p.accent}`,
    boxShadow: '0 20px 50px rgba(0,0,0,.5)', transform: `scale(${k})`, opacity: Math.min(1, k * 2)}}>
    <Img src={staticFile(c.src)} style={{width: '100%', display: 'block'}} />
  </div>;
};
