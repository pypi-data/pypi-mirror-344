import os
import sys
import time
import logging
from faster_whisper import WhisperModel
from .device import select_device

_model_cache: dict[tuple[str, str], WhisperModel] = {}

def get_whisper_model(model_size: str, device: str) -> WhisperModel:
    """
    First try to load from a local 'models/{model_size}' folder next
    to the EXE (or in dev), else fall back to downloading from HF hub.
    """
    if getattr(sys, "frozen", False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.getcwd()
    models_root = os.path.join(base_dir, "models")
    local_path = os.path.join(models_root, model_size)

    key = (local_path if os.path.isdir(local_path) else model_size, device)
    if key not in _model_cache:
        source = "local" if os.path.isdir(local_path) else "hub"
        logging.info(f"Loading Whisper model from {source}: {model_size}")
        try:
            _model_cache[key] = WhisperModel(
                key[0],
                device=device
            )
        except Exception as e:
            logging.error(f"Failed to load Whisper model '{model_size}': {e}")
            raise RuntimeError(
                "Could not load the Whisper model. "
                "Ensure you have an internet connection for first-run downloads, "
                "or place a 'models/{model_size}' folder beside the EXE."
            )
    return _model_cache[key]

def transcribe_file(
    filepath: str,
    model_size: str,
    min_vram_gb: int,
    progress_callback: callable,
    beam_size: int = 5,
    vad_filter: bool = True
) -> str:
    """
    Transcribe `filepath` with:
      • beam_size: beam search width
      • vad_filter: whether to filter out non-speech
    Reports progress via progress_callback(fraction, elapsed_seconds).
    """
    device = select_device(min_vram_gb)
    logging.info(f"Transcribing on device {device}")
    model = get_whisper_model(model_size, device)

    try:
        segments, info = model.transcribe(
            filepath,
            beam_size=beam_size,
            vad_filter=vad_filter
        )
    except Exception as e:
        logging.error(f"Transcription failed: {e}")
        raise RuntimeError("Transcription error – see log for details.")

    start = time.time()
    total = info.duration
    lines: list[str] = []

    for seg in segments:
        # preserve segment breaks
        lines.append(seg.text.strip())
        progress_callback(seg.end / total, time.time() - start)

    # double newline between segments for clarity
    return "\n\n".join(lines)
