"""Plain-assert tests for film_gate.py. Run: python -I test_film_gate.py"""
import json, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.join(HERE, 'film_gate.py')
S = 's=320x180'


def ff(out, *args):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *args, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', out], check=True)
    return out


def gate(video, *extra):
    out = video + '.json'
    p = subprocess.run([sys.executable, '-I', GATE, video, '--json', out, *extra], capture_output=True, text=True)
    assert p.returncode in (0, 1), p.stderr
    r = json.load(open(out))
    assert p.returncode == (0 if r['pass'] else 1), (p.returncode, r['pass'])
    return r


def main():
    d = tempfile.mkdtemp(prefix='film_gate_')
    j = lambda name: os.path.join(d, name)
    lav = lambda g: ['-f', 'lavfi', '-i', g]

    # 1. moving test pattern: real motion, no dead gap; soft checks run without crashing
    ts = ff(j('ts.mp4'), *lav('testsrc2=size=320x180:rate=24'), '-t', '4')
    json.dump({'still': [], 'sections': [{'t0': 0, 't1': 2, 'cpm': [0, 10], 'still': [0, .2]}, {'t0': 2, 't1': 4}]}, open(j('feel.json'), 'w'))
    json.dump({'fps': 24, 'rms': [i / 96 for i in range(96)], 'beats': [0.5, 1, 1.5, 2, 2.5, 3, 3.5]}, open(j('song.json'), 'w'))
    open(j('STYLE.md'), 'w').write('palette: #101010 #F2F2F2 #FF3355\n')
    r = gate(ts, '--feel', j('feel.json'), '--song', j('song.json'), '--style', j('STYLE.md'))
    assert r['pass'] and 'slideshow' in r['soft'] and 'dead_gap' in r['soft'], r   # no feel "gate": pacing is INFO
    assert r['hard']['blank']['pass'] and r['hard']['delivery']['pass'], r['hard']
    assert 'loop' not in r['hard'], 'loop runs only with --loop'
    assert len(r['soft']['sections']['sections']) == 2 and r['soft']['feel_sync']['source'] == 'song.rms', r['soft']
    assert r['soft']['palette']['mean_dE'] is not None and 'beat_hits' in r['soft'], r['soft']
    print('PASS 1 testsrc2: passes; pacing reported as INFO without a feel gate')

    # 2. three 2 s solid colours: a slideshow of dead frames
    rgb = ff(j('rgb.mp4'), *lav(f'color=c=red:{S}:r=24:d=2'), *lav(f'color=c=green:{S}:r=24:d=2'),
             *lav(f'color=c=blue:{S}:r=24:d=2'), '-filter_complex', '[0][1][2]concat=n=3:v=1:a=0')
    r = gate(rgb)
    assert r['pass'] and r['soft']['slideshow']['cuts'] == 2, r   # a still style never fails; red->green needs chroma
    json.dump({'gate': {'dead_gap': 1.0, 'slideshow': 0.6}}, open(j('gate.json'), 'w'))
    r = gate(rgb, '--feel', j('gate.json'))
    assert not r['hard']['slideshow']['pass'] and not r['hard']['dead_gap']['pass'] and not r['pass'], r['hard']
    print('PASS 2 solid colours: pass with no gate; fail once the feel card sets dead_gap + slideshow')

    # 3. two white frames 0.1 s apart over black -> flicker; one white frame alone is fine
    box = "drawbox=x=0:y=0:w=iw:h=ih:color=white:t=fill:enable='{}'"
    fl2 = ff(j('fl2.mp4'), *lav(f'color=c=black:{S}:r=30:d=2,' + box.format('eq(n,30)+eq(n,33)')))
    fl1 = ff(j('fl1.mp4'), *lav(f'color=c=black:{S}:r=30:d=2,' + box.format('eq(n,30)')))
    assert not gate(fl2)['hard']['flicker']['pass']
    assert gate(fl1)['hard']['flicker']['pass']
    print('PASS 3 flicker: two flashes 0.1 s apart fail, single flash passes')

    # 4. loop: testsrc2 ends elsewhere; testsrc2 + its reverse ends on its first frame
    assert not gate(ts, '--loop')['hard']['loop']['pass']
    pal = ff(j('pal.mp4'), *lav('testsrc2=size=320x180:rate=24:d=2'), '-filter_complex', '[0]split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1:a=0')
    r = gate(pal, '--loop')
    assert r['hard']['loop']['pass'], r['hard']['loop']
    print('PASS 4 loop: testsrc2 fails, palindrome passes')

    # 5. palette: solid #FF0000 against a STYLE.md that names #FF0000
    red = ff(j('red.mp4'), *lav(f'color=c=0xFF0000:{S}:r=24:d=1'))
    open(j('red.md'), 'w').write('# Style\nAccent `#FF0000`, ink #0A0A0A.\n')
    p = gate(red, '--style', j('red.md'))['soft']['palette']
    assert p['mean_dE'] < 5, p
    print(f"PASS 5 palette: mean dE {p['mean_dE']} < 5")

    # 6. delivery: untagged, silent file fails bt709; tagged file with audio muxed from 0 passes, offset ~0
    dv = gate(ts)['hard']['delivery']
    assert not dv['bt709'] and dv['av_offset_ms'] is None and dv['cfr'], dv
    tag = ff(j('tag.mp4'), *lav('testsrc2=size=320x180:rate=24'), *lav('sine=f=440:r=48000'), '-t', '2',
             '-vf', 'setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709', '-c:a', 'aac')
    dv = gate(tag)['hard']['delivery']
    assert dv['bt709'] and dv['cfr'] and abs(dv['av_offset_ms']) < 50, dv
    late = ff(j('late.mp4'), *lav('testsrc2=size=320x180:rate=24'), '-itsoffset', '0.5', *lav('sine=f=440:r=48000'),
              '-t', '2', '-c:a', 'aac')
    r = gate(late)
    assert not r['hard']['delivery']['pass'] and r['hard']['delivery']['av_offset_ms'] > 400, r['hard']['delivery']
    print(f"PASS 6 delivery: bt709 reported, offset {dv['av_offset_ms']} ms passes, planted 0.5 s audio lag fails")

    # 7. blank: 1 s of black mid-film fails; the same span declared in feel "blank" passes; colour cards never count
    mid = ff(j('mid.mp4'), *lav(f'testsrc2={S}:r=24:d=1.5'), *lav(f'color=c=black:{S}:r=24:d=1'),
             *lav(f'testsrc2={S}:r=24:d=1.5'), '-filter_complex', '[0][1][2]concat=n=3:v=1:a=0')
    r = gate(mid)
    assert not r['hard']['blank']['pass'] and r['hard']['blank']['longest_s'] >= 0.9, r['hard']['blank']
    json.dump({'blank': [[1.4, 2.6]]}, open(j('blank.json'), 'w'))
    assert gate(mid, '--feel', j('blank.json'))['hard']['blank']['pass']
    assert gate(rgb)['hard']['blank']['pass']
    print('PASS 7 blank: mid-film black fails, declared span passes, solid colour cards pass')
    shutil.rmtree(d, ignore_errors=True)   # kept on failure for inspection
    print('all film_gate tests passed')


if __name__ == '__main__':
    main()
