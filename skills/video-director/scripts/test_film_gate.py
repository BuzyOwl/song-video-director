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
    assert r['hard']['slideshow']['pass'] and r['hard']['dead_gap']['pass'], r['hard']
    assert 'loop' not in r['hard'], 'loop runs only with --loop'
    assert len(r['soft']['sections']['sections']) == 2 and r['soft']['feel_sync']['source'] == 'song.rms', r['soft']
    assert r['soft']['palette']['mean_dE'] is not None and 'beat_hits' in r['soft'], r['soft']
    print('PASS 1 testsrc2: slideshow + dead_gap pass, soft checks present')

    # 2. three 2 s solid colours: a slideshow of dead frames
    rgb = ff(j('rgb.mp4'), *lav(f'color=c=red:{S}:r=24:d=2'), *lav(f'color=c=green:{S}:r=24:d=2'),
             *lav(f'color=c=blue:{S}:r=24:d=2'), '-filter_complex', '[0][1][2]concat=n=3:v=1:a=0')
    r = gate(rgb)
    assert not r['hard']['slideshow']['pass'] and not r['hard']['dead_gap']['pass'] and not r['pass'], r['hard']
    assert r['hard']['slideshow']['cuts'] == 2, r['hard']['slideshow']   # red->green is isoluminant: chroma must catch it
    print('PASS 2 solid colours: slideshow + dead_gap fail, 2 cuts found')

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
    shutil.rmtree(d, ignore_errors=True)   # kept on failure for inspection
    print('all film_gate tests passed')


if __name__ == '__main__':
    main()
