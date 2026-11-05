import type {ReelProps} from '../types';
import {Title} from './Title'; import {LowerThird} from './LowerThird'; import {Stat} from './Stat';
import {Quote} from './Quote'; import {List} from './List';
import {Cutout} from './Cutout'; import {Screenshot} from './Screenshot'; import {Arrow} from './Arrow'; import {Pip} from './Pip';
export const Cards = ({p, t}: {p: ReelProps; t: number}) => (
  <>
    {p.cards.filter((c) => c.s - 0.1 <= t && t <= c.e + 0.3).map((c) => {
      switch (c.type) {
        case 'title': return <Title key={c.id} p={p} t={t} c={c} />;
        case 'lowerthird': return <LowerThird key={c.id} p={p} t={t} c={c} />;
        case 'stat': return <Stat key={c.id} p={p} t={t} c={c} />;
        case 'quote': return <Quote key={c.id} p={p} t={t} c={c} />;
        case 'list': return <List key={c.id} p={p} t={t} c={c} />;
        case 'cutout': return <Cutout key={c.id} p={p} t={t} c={c} />;
        case 'screenshot': return <Screenshot key={c.id} p={p} t={t} c={c} />;
        case 'arrow': return <Arrow key={c.id} p={p} t={t} c={c} />;
        case 'pip': return <Pip key={c.id} p={p} t={t} c={c} />;
        default: return null;
      }
    })}
  </>
);
