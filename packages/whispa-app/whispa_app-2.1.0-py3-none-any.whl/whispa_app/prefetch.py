from whispa_app.transcription import get_whisper_model
from whispa_app.translation import MODEL_MAP, translate_text

def main():
    sizes = ["tiny","base","small","medium","large"]
    total = len(sizes) + len(MODEL_MAP)
    step = 1

    print(f"🔄 Prefetching {len(sizes)} Whisper + {len(MODEL_MAP)} translations")
    for s in sizes:
        print(f"[{step}/{total}] Whisper '{s}'")
        get_whisper_model(s, "cpu")
        step += 1
    for lang in MODEL_MAP:
        print(f"[{step}/{total}] Translation '{lang}'")
        translate_text("Hello", lang)
        step += 1
    print("✅ Caching complete.")
