export type Word = {w: string; s: number; e: number; key?: boolean};
export type Chunk = {s: number; e: number; y: number; words: Word[]};  // y = normalised baseline, face-safe
export type ZoomEvent = {t: number; z: number};
export type CardBase = {s: number; e: number; y: number; id: string};    // y = normalised centre of the card lane
export type Card =
  | (CardBase & {type: 'title'; text: string; size?: number})
  | (CardBase & {type: 'lowerthird'; text: string; sub?: string})
  | (CardBase & {type: 'stat'; tokens: {text: string; t: number}[]; size?: number})
  | (CardBase & {type: 'quote'; text: string; by?: string})
  | (CardBase & {type: 'list'; items: {text: string; t: number}[]})
  | (CardBase & {type: 'cutout'; src: string; motion: 'drift' | 'drop' | 'none'; frame: 'torn' | 'strip' | 'news'})
  | (CardBase & {type: 'screenshot'; src: string; pan: 'down' | 'up' | 'none'})
  | (CardBase & {type: 'arrow'; from: [number, number]; to: [number, number]; shape: 'arrow' | 'circle' | 'underline'})
  | (CardBase & {type: 'pip'; src: string; corner: 'tl' | 'tr' | 'bl' | 'br'})
  | (CardBase & {type: 'board'; n?: string; kicker?: string; title: string; sub?: string; prompt: Timed[];
      rows: (Timed & {label: string})[]; label?: string; chips: Timed[]; clip?: string});  // full-screen slide; the speaker shrinks to a PiP bubble; clip = HyperFrames render
export type Timed = {text: string; t: number};
export type Sfx = {t: number; name: 'pop' | 'hit' | 'whoosh' | 'tick' | 'riser' | 'ding'; gain: number};
export type ReelProps = {
  src: string;            // staticFile path, e.g. 'job/cut.mp4'
  fps: number; w: number; h: number;
  dur: number;            // total seconds incl. tail
  srcDur: number;         // cut.mp4 seconds
  cuts: number[];         // jump-cut times (cut timeline)
  face: number[][];       // per source frame [cx, cy, w, h] normalised
  punch: number;          // alternate-shot zoom, e.g. 1.12
  zoom: ZoomEvent[];      // emphasis punch-ins
  chunks: Chunk[];
  cards: Card[];
  sfx: Sfx[];
  accent: string;         // '#FFD23F'
  font: 'Montserrat-ExtraBold' | 'Poppins-Bold';
  lang: string;           // 'en' | 'hi' ...
  capSize: number;        // caption font px at 1080 wide (>= 70 enforced in Captions)
  debugText?: string;     // test harness only: renders this string in the caption font
};
