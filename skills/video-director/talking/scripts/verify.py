"""verify.py - look at the ENCODED final.mp4, not a preview.  python -I scripts/verify.py <work>"""
import json, math, os, shutil, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw

TMP = os.environ.get("VD_TMP", str(Path.home() / ".video-director" / "tmp"))


def frame(video, t):
    p = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(video), "-frames:v", "1", "-vf", "scale=270:-2",
                        "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
    return Image.frombytes("RGB", (270, len(p.stdout) // (270 * 3)), p.stdout) if p.stdout else None


def main():
    work = Path(sys.argv[1])
    p = json.loads((work / "props.json").read_text())
    video = work / (sys.argv[2] if len(sys.argv) > 2 else "final.mp4")
    if not video.exists():
        sys.exit(f"verify: {video} not found")
    marks = [(0.2, "open")]
    for c in p["cards"]:
        marks += [(c["s"] + 0.35, f"{c['type']}.in"), (c["e"] - 0.3, f"{c['type']}.out")]
        for k in ("tokens", "items"):
            marks += [(x["t"] + 0.2, f"{c['type']}.{x['text'][:8]}") for x in c.get(k, [])]
    marks.append((p["dur"] - 0.2, "end"))
    marks = sorted((m for m in marks if 0 <= m[0] < p["dur"]), key=lambda m: m[0])
    tiles = []
    for t, lab in marks:
        im = frame(video, t)
        if im:
            ImageDraw.Draw(im).text((6, 4), f"{t:.2f}s {lab}", fill=(255, 255, 0))
            tiles.append(im)
    cols = 6
    rows = math.ceil(len(tiles) / cols)
    if not tiles:
        sys.exit("verify: ffmpeg returned no frames (bad or empty video)")
    sheet = Image.new("RGB", (cols * 270, rows * tiles[0].height))
    for k, im in enumerate(tiles):
        sheet.paste(im, ((k % cols) * 270, (k // cols) * im.height))
    sheet.save(work / "sheet.jpg", quality=88)
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)],
                             capture_output=True, text=True).stdout)
    print(f"sheet: {work / 'sheet.jpg'}  ({len(tiles)} frames)")
    ok = abs(d - p["dur"]) < 0.1
    print("duration ok" if ok else f"duration MISMATCH {d:.2f} vs {p['dur']:.2f}")
    if not ok:
        sys.exit(1)
    for f in ("preview.mp4",):
        (work / f).unlink(missing_ok=True)
    # verified render: empty the scratch dir, then recreate it so the next render has its TEMP
    shutil.rmtree(TMP, ignore_errors=True)
    os.makedirs(TMP, exist_ok=True)


if __name__ == "__main__":
    sys.exit(main())
