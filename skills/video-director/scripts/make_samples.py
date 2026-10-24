"""make_samples.py - cut gallery sample clips (silent, 480p, <=1.5 MB) from finished films listed in gallery/samples.json.

python -I make_samples.py            # writes gallery/samples/<id>.mp4, skips ones that exist
python -I make_samples.py --force    # re-cut all
"""
import json, subprocess, sys
from pathlib import Path

GAL = Path(__file__).resolve().parent.parent / "gallery"
MAX = 1.5e6


def cut(e, out, crf):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(e["start"]), "-t", str(e["dur"]), "-i", e["src"], "-an",
                    "-vf", "scale=-2:480,fps=24", "-c:v", "libx264", "-crf", str(crf), "-preset", "slow",
                    "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)], check=True)


def main():
    force = "--force" in sys.argv
    (GAL / "samples").mkdir(exist_ok=True)
    for e in json.loads((GAL / "samples.json").read_text(encoding="utf-8")):
        out = GAL / "samples" / f"{e['id']}.mp4"
        if out.exists() and not force:
            print("keep ", out.name); continue
        if not Path(e["src"]).exists():
            print("MISS ", e["src"]); continue
        crf = 28
        cut(e, out, crf)
        while out.stat().st_size > MAX and crf < 40:  # ponytail: CRF bump loop, fine for 6-8 s clips
            crf += 3
            cut(e, out, crf)
        print(f"wrote {out.name} {out.stat().st_size / 1e6:.2f} MB crf {crf}")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(e["dur"] / 2), "-i", str(out), "-frames:v", "1", "-q:v", "4",
                        str(out.with_suffix(".jpg"))], check=True)   # poster: tile never shows black before playback
        assert out.stat().st_size <= MAX, out
    page()


def page():
    """gallery/index.html with the tile data inlined, so it opens from file:// with no server."""
    looks = {}
    for e in json.loads((GAL / "samples.json").read_text(encoding="utf-8")):
        base = e["id"].rsplit("-", 1)[0] if e["id"][-2:-1] == "-" and e["id"][-1].isdigit() else e["id"]
        looks.setdefault(base, {**e, "id": base, "clips": []})["clips"].append(f"samples/{e['id']}.mp4")
    tiles = "\n".join(
        f'<figure><video src="{l["clips"][0]}" poster="{l["clips"][0][:-4]}.jpg" data-clips="{",".join(l["clips"])}" muted autoplay loop playsinline></video>'
        f'<figcaption><b>{l["title"]}</b><span>{l["film"]} · {l["engine"]} · cost {l["cost"]}</span>'
        f'<button data-id="{l["id"]}">Borrow an idea</button></figcaption></figure>' for l in looks.values())
    (GAL / "index.html").write_text(TEMPLATE.replace("{{TILES}}", tiles), encoding="utf-8")
    print("wrote index.html", len(looks), "looks")


TEMPLATE = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>video-director looks</title><style>
:root{--bg:#111;--fg:#eee;--dim:#999;--card:#1b1b1b;--accent:#f2b66d}
@media (prefers-color-scheme:light){:root{--bg:#f4f1ea;--fg:#1a1a1a;--dim:#666;--card:#fff;--accent:#b5651d}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.45 system-ui,sans-serif;padding:32px 16px}
header{max-width:1200px;margin:0 auto 24px}h1{margin:0 0 6px;font-size:28px}p{margin:0;color:var(--dim)}
main{max-width:1200px;margin:auto;display:grid;gap:18px;grid-template-columns:repeat(auto-fill,minmax(340px,1fr))}
figure{margin:0;background:var(--card);border-radius:10px;overflow:hidden}video{width:100%;aspect-ratio:16/9;object-fit:cover;display:block;background:#000}
figcaption{padding:12px 14px;display:grid;gap:4px}figcaption span{color:var(--dim);font-size:13px}
button{justify-self:start;margin-top:6px;border:1px solid var(--accent);background:none;color:var(--fg);border-radius:6px;padding:6px 12px;cursor:pointer}
button.done{background:var(--accent);color:#111}footer{max-width:1200px;margin:28px auto 0;color:var(--dim);font-size:13px}a{color:var(--accent)}
</style></head><body><header><h1>What these engines can do</h1><p>Every tile is a clip from a finished film made with this skill. Tiles with a second clip swap on hover.
Your film gets its own new look. Use these as sparks: press <b>Borrow an idea</b> and tell Claude what you liked, or paste 1-3 references you love.</p></header>
<main>{{TILES}}</main>
<footer>More looks: motion-graphics styles in <a href="https://github.com/ItsssssJack/claude-video-2">claude-video-2</a> ·
36 art-history styles in <a href="https://github.com/alchaincyf/huashu-art-motion">huashu-art-motion</a>.
These films prove the pipelines; they are not the taste ceiling. Bring references you love.</footer>
<script>
document.querySelectorAll('figure').forEach(f=>{const v=f.querySelector('video'),c=v.dataset.clips.split(',');
 if(c.length>1){f.onmouseenter=()=>{v.src=c[1]};f.onmouseleave=()=>{v.src=c[0]}}});
document.querySelectorAll('button').forEach(b=>b.onclick=()=>{const id=b.dataset.id;
 (navigator.clipboard?navigator.clipboard.writeText(id):Promise.reject()).catch(()=>prompt('Copy this id:',id));
 b.textContent='Copied: '+id;b.classList.add('done')});
</script></body></html>"""


if __name__ == "__main__":
    main()
