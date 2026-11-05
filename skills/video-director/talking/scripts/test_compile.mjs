// node scripts/test_compile.mjs — resolves refs against reels/test-01 and checks props shape
import {compile} from './compile.mjs';
import assert from 'node:assert/strict';
import path from 'node:path';
import os from 'node:os';
import {mkdirSync, copyFileSync, readFileSync, writeFileSync} from 'node:fs';
import {faceBox} from './camera.mjs';
const work = process.env.VD_TEST_REEL || 'D:/03_Projects/Video Caption Project MIC Class/reels/test-01';
if (!(await import('node:fs')).existsSync(path.join(work, 'words.json'))) { console.log('SKIP: set VD_TEST_REEL to a prepped reel'); process.exit(0); }
const edit = {size: [1080, 1920], tail: 1.2, punch: 1.12, zoom: 'auto', sfx: true,
  captions: {words: 3, accent: '#FFD23F', keys: ['fire', 'idea']},
  cards: [{type: 'title', at: 'test', until: 'one.e+0.3', text: 'TEST 01'},
          {type: 'stat', at: '100', until: 'up.e', tokens: [['100', '100'], ['−', 'minus'], ['25', '25'], ['=', 'equals'], ['75', '75']]},
          {type: 'arrow', at: 'bulb', until: 'bulb.e+1', target: 'face', shape: 'circle'}]};
const p = compile(work, edit);
assert.equal(p.fps, 30); assert.ok(p.dur > 26 && p.dur < 28, p.dur);
assert.ok(p.chunks.length > 10 && p.chunks.every((c) => c.words.length <= 3 && c.e > c.s));
assert.ok(p.chunks.some((c) => c.words.some((w) => w.key)), 'fire/idea must be keyed');
const stat = p.cards.find((c) => c.type === 'stat');
assert.equal(stat.tokens.length, 5); assert.ok(stat.tokens[4].t > stat.tokens[0].t);
const arrow = p.cards.find((c) => c.type === 'arrow');
// brief asserted 'upper half'; test-01's speaker sits low in frame, so assert the real property: the circle encloses the face box
const fb = faceBox(p, arrow.s);
assert.ok(arrow.from[0] < fb[0] / 1080 && arrow.from[1] < fb[1] / 1920 && arrow.to[0] > fb[2] / 1080 && arrow.to[1] > fb[3] / 1920, 'arrow encloses face');
assert.ok(p.zoom.length >= 1, 'auto zoom from emphasis[]');
assert.ok(p.sfx.some((s) => s.name === 'hit'));
assert.equal(p.capSize, 78);
assert.equal(compile(work, {captions: {size: 88}}).capSize, 88);
assert.throws(() => compile(work, {cards: [{type: 'title', at: 'nosuchword', until: 'end', text: 'x'}]}), /not in transcript/);
// lane logic: capture console.warn
const warns = (fn) => { const w = console.warn, got = []; console.warn = (m) => got.push(String(m)); try { return {r: fn(), got}; } finally { console.warn = w; } };
const copyWork = (boxes) => { const d = path.join(process.env.TEMP ?? os.tmpdir(), 'tc_work'); mkdirSync(d, {recursive: true});
  copyFileSync(path.join(work, 'words.json'), path.join(d, 'words.json'));
  const tr = JSON.parse(readFileSync(path.join(work, 'track.json'), 'utf8')); writeFileSync(path.join(d, 'track.json'), JSON.stringify({...tr, boxes})); return d; };
const big = copyWork([[0.5, 0.5, 0.6, 0.9]]);                          // face fills cy 0.5, h 0.9 -> band 0.05-0.95
assert.ok(warns(() => compile(big, {cards: [{type: 'title', at: 'test', until: 'one.e', text: 'x'}]})).got.some((m) => /FACE OVERLAP/.test(m)), 'FACE OVERLAP fires');
const t2 = {type: 'title', at: 'test', until: 'one.e', text: 'x'};
const two = warns(() => compile(work, {cards: [t2, t2]}));
const [c0, c1] = two.r.cards; assert.ok(Math.abs(c1.y - c0.y) >= 0.09 + 0.02 - 1e-9 && two.got.length === 0, 'second title shifted clear, no warning');
const L = {type: 'list', at: 'test', until: 'one.e', items: [['a', 'test'], ['b', 'test'], ['c', 'test'], ['d', 'test'], ['e', 'test']]};
assert.ok(warns(() => compile(work, {cards: [L, L, L]})).got.some((m) => /CARD OVERLAP/.test(m)), 'three stacked tall cards: no lane fits');
// benchmark edit is face-safe by compile's own model
const bench = JSON.parse(readFileSync(path.join(work, 'edit.json'), 'utf8'));
const hs = {title: 0.09, stat: 0.11, lowerthird: 0.11, quote: 0.16, cutout: 0.30, screenshot: 0.42};
const bw = warns(() => compile(work, bench)); const bp = bw.r;
const fband = (s, e) => { const fs = [s, (s + e) / 2, e].map((t) => faceBox(bp, Math.min(Math.max(t, 0), bp.dur))); return [Math.min(...fs.map((f) => f[1])) / bp.h, Math.max(...fs.map((f) => f[3])) / bp.h]; };
assert.ok(!bw.got.some((m) => /FACE OVERLAP/.test(m)), 'benchmark has no FACE OVERLAP');
for (const c of bp.cards) { if (c.type === 'arrow' || c.type === 'pip') continue;
  const h = c.type === 'list' ? Math.min(0.06 + 0.05 * c.items.length, 0.3) : hs[c.type]; const [top, bot] = fband(c.s, c.e);
  assert.ok(c.y + h / 2 <= top - 0.02 + 1e-9 || c.y - h / 2 >= bot + 0.02 - 1e-9, `${c.id} ${c.type} clears face`); }
// Devanagari refs/keys survive norm; non-vertical source is refused
{
  const {refResolver, chunkWords, norm} = await import('./compile.mjs');
  const dw = [{w: 'नमस्ते', s: 0, e: 0.5}, {w: 'दोस्तों', s: 0.6, e: 1.0}];
  assert.ok(norm('नमस्ते').length > 0);
  assert.equal(refResolver(dw, 2)('दोस्तों'), 0.6);
  assert.deepEqual(chunkWords(dw, 3, ['दोस्तों'])[0].words.map((x) => x.key), [false, true]);
  assert.throws(() => compile(work, {}, {track: {w: 1920, h: 1080, boxes: [[0.5, 0.5, 0.2, 0.2]]}}), /crop/);
}
// board: chips cascade / ref-timed, captions over a board keep cap.y, fix rewrites words before refs
{
  const ws = JSON.parse(readFileSync(path.join(work, 'words.json'), 'utf8')).words;
  const w0 = ws[0].w.replace(/[.,;:!?]+$/, '');
  const bp = compile(work, {fix: {[w0]: 'zebra'}, captions: {y: 0.84}, cards: [{type: 'board', at: 'zebra', until: 'end', title: 'T',
    chips: ['a', 'b'], prompt: [['hi', 'zebra']], rows: [['L', 'x', 'zebra']]}]});
  const b = bp.cards[0];
  assert.equal(b.type, 'board'); assert.ok(b.chips[1].t > b.chips[0].t && b.chips[0].t > b.s, 'bare chips cascade after start');
  assert.equal(b.prompt[0].t, b.s); assert.equal(b.rows[0].label, 'L');
  assert.ok(bp.chunks[0].words[0].w.startsWith('zebra'), 'fix rewrites the caption word');
  assert.ok(bp.chunks.every((c) => c.y === 0.84), 'captions over a board keep cap.y');
}
console.log('ok compile');
