#!/usr/bin/env node
// compile.mjs — <work>/edit.json -> <work>/props.json -> npx remotion render. Every word ref, lane and
// zoom is resolved here so the renderer is a pure function of props.
import {readFileSync, writeFileSync, mkdirSync, copyFileSync, rmSync, existsSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import path from 'node:path';
import os from 'node:os';
import {fileURLToPath} from 'node:url';
import {faceBox} from './camera.mjs';

const SKILL = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const REM = path.join(SKILL, 'remotion');
const TMP = process.env.VD_TMP || path.join(os.homedir(), '.video-director', 'tmp');  // heavy Chrome temp: point at a big drive
const FPS = 30;
const LANE = {title: 0.10, stat: 0.12, lowerthird: 0.20, quote: 0.24, list: 0.24, cutout: 0.24, screenshot: 0.24, pip: 0.1, arrow: 0.3};
export const norm = (w) => w.toLowerCase().replace(/[^\p{L}\p{M}\p{N}']/gu, '');

export const refResolver = (words, dur) => (ref) => {
  if (ref == null || typeof ref === 'number') return ref;
  const m = /^(.+?)(#\d+)?(\.e)?([+-]\d*\.?\d+)?$/.exec(String(ref).trim());
  if (!m) throw new Error(`bad ref ${ref}`);
  const [, base, nth, end, off] = m;
  const o = parseFloat(off ?? '0');
  if (base === 'end') return dur + o;
  if (base === 'start') return o;
  const hits = words.filter((w) => norm(w.w) === norm(base));
  const k = nth ? parseInt(nth.slice(1), 10) - 1 : 0;
  if (k >= hits.length) throw new Error(`edit.json: word ref '${ref}' not in transcript (see cut.txt)`);
  return (end ? hits[k].e : hits[k].s) + o;
};

export const chunkWords = (words, n, keys) => {
  const ks = new Set(keys.map(norm));
  const chunks = []; let cur = [];
  words.forEach((w, i) => {
    cur.push({w: w.w, s: w.s, e: w.e, key: ks.has(norm(w.w)) || /^\d/.test(w.w)});
    const nxt = words[i + 1];
    if (cur.length >= n || /[.?!]$/.test(w.w) || (/,$/.test(w.w) && cur.length > 1) || !nxt || nxt.s - w.e > 0.35) { chunks.push(cur); cur = []; }
  });
  return chunks.map((c, i) => ({words: c, s: c[0].s, e: Math.min(chunks[i + 1]?.[0].s ?? 1e9, c[c.length - 1].e + 0.5)}));
};

export const compile = (work, edit, inject = {}) => {
  const wj = inject.words ?? JSON.parse(readFileSync(path.join(work, 'words.json'), 'utf8'));
  const tr = inject.track ?? JSON.parse(readFileSync(path.join(work, 'track.json'), 'utf8'));
  const [w, h] = edit.size ?? [1080, 1920];
  const srcAspect = tr.w / tr.h, outAspect = w / h;
  if (Math.abs(srcAspect - outAspect) > 0.02) throw new Error(`source is ${tr.w}x${tr.h} (${srcAspect.toFixed(3)}) but output is ${w}x${h} (${outAspect.toFixed(3)}): crop the source to the output aspect first, e.g. ffmpeg -i cut.mp4 -vf "crop=ih*${w}/${h}:ih" cut_vertical.mp4, then re-run prep.py on it`);
  // fix: {"misheard": "right"} rewrites caption words (punctuation kept) before refs resolve, so it survives prep re-runs
  const fix = Object.fromEntries(Object.entries(edit.fix ?? {}).map(([a, b]) => [norm(a), b]));
  wj.words = wj.words.map((x) => fix[norm(x.w)] ? {...x, w: fix[norm(x.w)] + (/[.,;:!?]+$/.exec(x.w)?.[0] ?? '')} : x);
  const dur = wj.dur + (edit.tail ?? 1.2);
  const at = refResolver(wj.words, wj.dur);
  const cap = edit.captions ?? {};
  const accent = cap.accent ?? '#FFD23F';
  const p = {src: 'job/cut.mp4', fps: FPS, w, h, dur, srcDur: wj.dur, cuts: wj.cuts, face: tr.boxes, punch: edit.punch ?? 1.12,
    zoom: [], chunks: [], cards: [], sfx: [], accent, font: cap.font ?? 'Montserrat-ExtraBold', lang: wj.lang ?? 'en', capSize: cap.size ?? 78};
  if (edit.zoom !== 'off') p.zoom = (wj.emphasis ?? []).map((e) => ({t: e.t, z: e.z}));
  const face = (t) => faceBox(p, t);           // output px [x0,y0,x1,y1]
  // face band over [s,e]: sample every 0.5 s (a speaker leans in over a long card), return [minTop, maxBottom] normalised
  const faceBand = (s, e) => { const ts = [s]; for (let t = s + 0.5; t < e; t += 0.5) ts.push(t); ts.push(e);
    const fs = ts.map((t) => face(Math.min(Math.max(t, 0), dur)));
    return [Math.min(...fs.map((f) => f[1])) / h, Math.max(...fs.map((f) => f[3])) / h]; };
  // captions: one lane below the chin, never over the face, never under the platform UI zone (bottom 10%)
  // while a board is up the face is in the PiP bubble (top-right), so captions keep their own y
  const boards = (edit.cards ?? []).filter((c) => c.type === 'board').map((c) => [at(c.at), c.until != null ? at(c.until) : at(c.at) + 2]);
  if (edit.captions !== null) {
    p.chunks = chunkWords(wj.words, cap.words ?? 3, cap.keys ?? []).map((c) => {
      const onBoard = boards.some(([s, e]) => c.s >= s - 0.3 && c.e <= e + 0.5);
      const y = onBoard ? cap.y ?? 0.84 : Math.min(Math.max(cap.y ?? 0.84, faceBand(c.s, c.e)[1] + 0.06), 0.9);
      return {...c, y};
    });
  }
  const sfx = (t, name, gain) => edit.sfx !== false && p.sfx.push({t, name, gain});
  const lanes = [];
  (edit.cards ?? []).forEach((c, i) => {
    const id = `c${i}`; const s = at(c.at); const e = c.until != null ? at(c.until) : s + 2;
    const fb = face(s);
    let y = c.y ?? LANE[c.type] ?? 0.2;
    // Card heights as frame fractions (centre y +- h/2): approximations of the components' CSS in remotion/src/cards —
    // Title/Stat one text line, Quote/List panels grow with content, Cutout img maxHeight 0.42h (~0.30 typical), Screenshot frame 0.4h.
    const H = {title: 0.09, stat: 0.11, lowerthird: 0.11, quote: 0.16, list: Math.min(0.06 + 0.05 * (c.items?.length ?? 3), 0.3), cutout: 0.30, screenshot: 0.42, pip: 0.3};
    // arrow (drawn around a target) and pip (corner-anchored) take no lane, so they neither move nor block.
    if (c.type !== 'arrow' && c.type !== 'pip' && c.type !== 'board') {
      const hh = H[c.type] ?? 0.16; const [top, bot] = faceBand(s, e);
      const faceOk = (v) => v + hh / 2 <= top - 0.02 || v - hh / 2 >= bot + 0.02;
      const inBounds = (v) => v - hh / 2 >= 0.04 - 1e-9 && v + hh / 2 <= 0.78 + 1e-9;
      const hits = (v) => lanes.filter((o) => o.s < e && o.e > s && Math.abs(o.y - v) < o.h / 2 + hh / 2 + 0.02 - 1e-9);
      if (!faceOk(y)) {
        const up = top - 0.02 - hh / 2, down = bot + 0.02 + hh / 2;
        if (inBounds(up)) y = up; else if (inBounds(down)) y = down; else console.warn(`FACE OVERLAP ${id} ${c.type}`);
      }
      const other = hits(y)[0];
      if (other) {
        const alt = hits(y).flatMap((o) => [o.y + o.h / 2 + 0.02 + hh / 2, o.y - o.h / 2 - 0.02 - hh / 2]).find((v) => inBounds(v) && faceOk(v) && !hits(v).length);
        if (alt != null) y = alt; else console.warn(`CARD OVERLAP ${id} ${c.type} with ${other.id}`);
      }
      lanes.push({id, s, e, y, h: hh});
    }
    const base = {id, s, e, y};
    const asset = (src) => { if (!src) throw new Error(`${id}: src required`); const dst = `job/${path.basename(src)}`;
      mkdirSync(path.join(REM, 'public', 'job'), {recursive: true}); copyFileSync(path.join(work, src), path.join(REM, 'public', dst)); return dst; };
    switch (c.type) {
      case 'title': p.cards.push({...base, type: 'title', text: c.text, size: c.size}); sfx(s, 'pop', 0.5); break;
      case 'lowerthird': p.cards.push({...base, type: 'lowerthird', text: c.text, sub: c.sub}); sfx(s, 'whoosh', 0.3); break;
      case 'stat': { const tokens = c.tokens.map(([text, ref]) => ({text, t: at(ref)})); p.cards.push({...base, type: 'stat', tokens, size: c.size});
        tokens.forEach((tk, j) => sfx(tk.t, j === tokens.length - 1 ? 'hit' : 'pop', j === tokens.length - 1 ? 0.6 : 0.35)); break; }
      case 'quote': p.cards.push({...base, type: 'quote', text: c.text, by: c.by}); sfx(s, 'whoosh', 0.3); break;
      case 'list': { const items = c.items.map(([text, ref]) => ({text, t: at(ref)})); p.cards.push({...base, type: 'list', items}); items.forEach((it) => sfx(it.t, 'tick', 0.4)); break; }
      case 'cutout': p.cards.push({...base, type: 'cutout', src: asset(c.src), motion: c.motion ?? 'drift', frame: c.frame ?? 'torn'}); sfx(s, 'whoosh', 0.35); break;
      case 'screenshot': p.cards.push({...base, type: 'screenshot', src: asset(c.src), pan: c.pan ?? 'down'}); sfx(s, 'whoosh', 0.3); break;
      case 'pip': p.cards.push({...base, type: 'pip', src: asset(c.src), corner: c.corner ?? 'tr'}); sfx(s, 'pop', 0.4); break;
      case 'board': { const tm = ([text, ref]) => ({text, t: at(ref)});
        const prompt = (c.prompt ?? []).map(tm), rows = (c.rows ?? []).map(([label, text, ref]) => ({label, ...tm([text, ref])}));
        const chips = (c.chips ?? []).map((x, j) => typeof x === 'string' ? {text: x, t: s + 0.35 + j * 0.07} : tm(x));  // bare strings cascade in
        p.cards.push({...base, type: 'board', n: c.n, kicker: c.kicker, title: c.title, sub: c.sub, prompt, rows, label: c.label, chips});
        sfx(s, 'whoosh', 0.3); prompt.forEach((x) => sfx(x.t, 'tick', 0.3)); rows.forEach((x) => sfx(x.t, 'tick', 0.4));
        (c.chips ?? []).forEach((x, j) => typeof x !== 'string' ? sfx(chips[j].t, 'pop', 0.3) : j === 0 && sfx(chips[0].t, 'pop', 0.35)); break; }
      case 'arrow': { let from = c.from, to = c.to;
        if (c.target === 'face' || !from) { const pad = 0.02; from = [fb[0] / w - pad, fb[1] / h - pad]; to = [fb[2] / w + pad, fb[3] / h + pad]; }
        p.cards.push({...base, type: 'arrow', from, to, shape: c.shape ?? 'arrow'}); sfx(s, 'tick', 0.4); break; }
      default: throw new Error(`${id}: unknown card type ${c.type}`);
    }
  });
  return p;
};

const main = () => {
  const [editPath, ...flags] = process.argv.slice(2);
  if (!editPath) { console.error('usage: node compile.mjs <work>/edit.json [--preview] [--range a:b] [--no-render]'); process.exit(2); }
  const work = path.resolve(path.dirname(editPath));
  const edit = JSON.parse(readFileSync(editPath, 'utf8'));
  const preview = flags.includes('--preview') || flags.includes('--range');
  const p = compile(work, edit);
  writeFileSync(path.join(work, 'props.json'), JSON.stringify(p));
  if (flags.includes('--no-render')) return;
  mkdirSync(TMP, {recursive: true});
  mkdirSync(path.join(REM, 'public', 'job'), {recursive: true});
  copyFileSync(path.join(work, 'cut.mp4'), path.join(REM, 'public', 'job', 'cut.mp4'));
  const out = path.join(work, preview ? 'preview.mp4' : (edit.out ?? 'final.mp4'));
  const args = ['render', 'Reel', out, '--props', path.join(work, 'props.json'), '--concurrency', flags.includes('--concurrency') ? flags[flags.indexOf('--concurrency') + 1] : '4', '--codec', 'h264', '--crf', preview ? '23' : '17'];
  if (preview) args.push('--scale', '0.5');
  const r = flags.indexOf('--range');
  if (r >= 0) { const [a, b] = flags[r + 1].split(':').map(Number); args.push('--frames', `${Math.round(a * FPS)}-${Math.round(b * FPS)}`); }
  const t0 = Date.now();
  try {
  execFileSync(process.execPath, [path.join(REM, 'node_modules', '@remotion', 'cli', 'remotion-cli.js'), ...args], {cwd: REM, stdio: 'inherit', env: {...process.env, TEMP: TMP, TMP}});
  console.log(`rendered ${out} in ${((Date.now() - t0) / 1000).toFixed(1)}s`);
  if (!preview) execFileSync('python', ['-I', path.join(SKILL, 'scripts', 'verify.py'), work, path.basename(out)], {stdio: 'inherit'});
  } finally { rmSync(path.join(REM, 'public', 'job'), {recursive: true, force: true}); }
};
const same = (a, b) => path.resolve(a).toLowerCase() === path.resolve(b).toLowerCase();
if (process.argv[1] && same(fileURLToPath(import.meta.url), process.argv[1])) main();