"""Plain-assert tests for flicker_scan.py. Run: python -I test_flicker_scan.py"""
import os, shutil, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flicker_scan import scan_video

S = '480x270'


def ff(out, *args):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *args, '-c:v', 'libx264', '-crf', '12', '-pix_fmt', 'yuv420p', out],
                   check=True)
    return out


def main():
    d = tempfile.mkdtemp(prefix='flicker_scan_')
    j = lambda n: os.path.join(d, n)
    # a camera pan over a detailed still (testsrc2 can't be the clean case: its checker patch is per-frame noise)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'mandelbrot=size=960x540', '-frames:v', '1',
                    j('m.png')], check=True)
    src = ['-loop', '1', '-framerate', '24', '-t', '3', '-i', j('m.png')]
    pan = "crop=480:270:x='60+50*t':y='40+25*t'"

    # 1. smooth pan: real motion, nothing that comes back -> no strong event
    clean = ff(j('clean.mp4'), *src, '-vf', pan)
    r = scan_video(clean, out=j('o_clean'), height=270)
    worst = max([e['strength'] for e in r['events']], default=0)
    assert r['frames_scored'] >= r['frames_read'] - 3, r
    print(f'clean: {r["events_found"]} events, worst strength {worst}')

    # 2. same clip with a small patch that turns white for 1 frame, then for 2 frames -> caught at its place
    box = "drawbox=x=300:y=60:w=40:h=24:color=white:t=fill:enable='eq(n,20)+between(n,45,46)'"
    fl = ff(j('fl.mp4'), *src, '-vf', pan + ',' + box)
    r = scan_video(fl, out=j('o_fl'), height=270)
    top = r['events'][0]
    x0, y0, x1, y1 = top['box_norm']
    assert x0 <= 300 / 480 + .03 and x1 >= 340 / 480 - .03 and y0 <= 60 / 270 + .05 and y1 >= 84 / 270 - .05, top
    assert top['strength'] > 3 * max(worst, 0.1), (top, worst)
    hits = {e['peak_frame'] for e in r['events'] if e['strength'] > 3 * max(worst, 0.1)}
    assert any(abs(f - 20) <= 1 for f in hits) and any(45 <= f <= 46 for f in hits), hits
    assert os.path.exists(os.path.join(j('o_fl'), top['sheet'])) and os.path.exists(os.path.join(j('o_fl'), 'mask.mp4'))
    print(f'flicker: top event strength {top["strength"]} at frame {top["peak_frame"]}, box {top["box_norm"]}')

    # 3. a hard cut to a different picture that stays -> not flicker
    cut = ff(j('cut.mp4'), *src, '-f', 'lavfi', '-i', f'smptebars=size={S}:rate=24:d=1.5',
             '-filter_complex', f'[0]{pan},trim=0:1.5,setsar=1[a];[1]setsar=1[b];[a][b]concat=n=2:v=1:a=0')
    r = scan_video(cut, out=j('o_cut'), height=270)
    cw = max([e['strength'] for e in r['events']], default=0)
    assert cw < top['strength'] / 3, r['events'][:3]
    print(f'cut: worst strength {cw}')
    shutil.rmtree(d, ignore_errors=True)
    print('all flicker_scan tests passed')


if __name__ == '__main__':
    main()
