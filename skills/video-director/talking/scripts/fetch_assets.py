"""fetch_assets.py - one-time downloads for talking-head-director v2 (all on D:).
    python -I scripts/fetch_assets.py
"""
import os, sys, urllib.request
from pathlib import Path

MODELS = Path(os.environ.get("VD_MODELS", Path.home() / ".video-director" / "models"))
os.environ.setdefault("HF_HOME", str(MODELS / "hf"))
SKILL = Path(__file__).resolve().parent.parent
FONTS = SKILL / "remotion" / "public" / "fonts"

URLS = {
    MODELS / "mediapipe" / "blaze_face_short_range.tflite":
        "https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/latest/blaze_face_short_range.tflite",
    MODELS / "mediapipe" / "gesture_recognizer.task":
        "https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/latest/gesture_recognizer.task",
    MODELS / "yunet" / "face_detection_yunet_2023mar.onnx":
        "https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx",
    FONTS / "Montserrat-ExtraBold.ttf":
        "https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat%5Bwght%5D.ttf",
    FONTS / "Poppins-Bold.ttf":
        "https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Bold.ttf",
    FONTS / "NotoSansDevanagari-Bold.ttf":
        "https://github.com/google/fonts/raw/main/ofl/notosansdevanagari/NotoSansDevanagari%5Bwdth,wght%5D.ttf",
}


def main():
    for dst, url in URLS.items():
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists() and dst.stat().st_size > 1000:
            print("ok     ", dst.name)
            continue
        print("fetch  ", dst.name, flush=True)
        urllib.request.urlretrieve(url, dst)
        assert dst.stat().st_size > 1000, f"{dst} looks empty"
    from huggingface_hub import hf_hub_download
    for repo, f in [("onnx-community/mms-300m-1130-forced-aligner-ONNX", "onnx/model_int8.onnx"),
                    ("onnx-community/mms-300m-1130-forced-aligner-ONNX", "vocab.json"),
                    ("onnx-community/wav2vec2-base-960h-ONNX", "onnx/model.onnx"),
                    ("onnx-community/wav2vec2-base-960h-ONNX", "vocab.json")]:
        print("hf     ", repo, f, "->", hf_hub_download(repo, f))
    print("done")


if __name__ == "__main__":
    sys.exit(main())
