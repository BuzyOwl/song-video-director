"""doctor.py - one-shot setup check for video-director. Prints OK/FIX lines; exit 1 if a required tool is missing.

python -I doctor.py
"""
import importlib.util, os, shutil, subprocess, sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
bad = 0


def line(ok, what, fix=""):
    global bad
    print(("OK   " if ok else "FIX  ") + what + ("" if ok else f"  ->  {fix}"))
    bad += 0 if ok else 1


def version(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=20).stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        return ""


line(sys.version_info >= (3, 10), f"python {sys.version.split()[0]}", "install Python 3.10+")
for tool in ("ffmpeg", "ffprobe"):
    line(bool(shutil.which(tool)), tool, "install ffmpeg (winget install ffmpeg / brew install ffmpeg / apt install ffmpeg)")
node = version(["node", "-v"])
line(node.startswith("v") and int(node[1:].split(".")[0]) >= 22, f"node {node or 'missing'}", "install Node 22+ from nodejs.org")
line(importlib.util.find_spec("numpy") is not None, "numpy", "python -m pip install numpy")

# optional: printed as INFO so a missing one never blocks pure-code work
for mod, why in (("faster_whisper", "lyric/word timing"), ("PIL", "talking verify sheets")):
    print(("OK   " if importlib.util.find_spec(mod) else "INFO ") + f"{mod} ({why})" +
          ("" if importlib.util.find_spec(mod) else f"  ->  python -m pip install {'pillow' if mod == 'PIL' else 'faster-whisper'}"))
print(("OK   " if shutil.which("blender") else "INFO ") + "blender on PATH (3D guide / recreate engines)" +
      ("" if shutil.which("blender") else "  ->  optional: install Blender 4.2+; MCP: uvx mcp-for-blender"))
rem = SKILL / "talking" / "remotion" / "node_modules"
print(("OK   " if rem.exists() else "INFO ") + "talking pipeline deps" + ("" if rem.exists() else f"  ->  cd \"{rem.parent}\" && npm ci"))

# heavy temp + models belong on a big drive (Chrome profiles once filled C: with 7.8 GB)
for var in ("VD_TMP", "VD_MODELS"):
    path = Path(os.environ.get(var, Path.home() / ".video-director" / var[3:].lower()))
    path.mkdir(parents=True, exist_ok=True)
    free = shutil.disk_usage(path).free / 1e9
    print(("OK   " if free > 15 else "WARN ") + f"{var} = {path} ({free:.0f} GB free)" +
          ("" if free > 15 else f"  ->  set {var} to a folder on a drive with 15+ GB free"))

print("doctor:", "ready" if not bad else f"{bad} required fix(es)")
sys.exit(1 if bad else 0)
