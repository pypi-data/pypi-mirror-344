import os
import sys
import logging
from typing import Callable, Optional
from transformers import MarianTokenizer, MarianMTModel, logging as hf_logging
from .device import select_device

hf_logging.set_verbosity_error()

MODEL_MAP = {
    "Spanish":  "Helsinki-NLP/opus-mt-en-es",
    "French":   "Helsinki-NLP/opus-mt-en-fr",
    "German":   "Helsinki-NLP/opus-mt-en-de",
    "Chinese":  "Helsinki-NLP/opus-mt-en-zh",
    "Japanese": "Helsinki-NLP/opus-mt-en-jap"
}

def get_translation_model(repo: str, device: str):
    base = getattr(sys, "frozen", False) and os.path.dirname(sys.executable) or os.getcwd()
    name = repo.split("/")[-1]
    local = os.path.join(base, "models", "translation", name)
    key = (repo, device)
    cache = get_translation_model.__dict__.setdefault("_cache", {})
    if key not in cache:
        logging.info(f"Loading translation model '{repo}'")
        tokenizer = MarianTokenizer.from_pretrained(local if os.path.isdir(local) else repo)
        model = MarianMTModel.from_pretrained(local if os.path.isdir(local) else repo).to(device)
        cache[key] = (tokenizer, model)
    return cache[key]

def translate(
    text: str,
    target_lang: str,
    progress_callback: Optional[Callable[[int,int], None]] = None,
    **gen_kwargs
) -> str:
    if not text.strip():
        return ""
    if target_lang not in MODEL_MAP:
        raise ValueError(f"No model for '{target_lang}'")
    repo = MODEL_MAP[target_lang]
    device = select_device(min_vram_gb=4)
    tokenizer, model = get_translation_model(repo, device)

    # chunk text ~1200 chars
    chunks = []
    for para in text.split("\n"):
        while len(para) > 1200:
            chunks.append(para[:1200])
            para = para[1200:]
        chunks.append(para)

    out = []
    total = len(chunks)
    for i, chunk in enumerate(chunks, 1):
        inputs = tokenizer(chunk, return_tensors="pt", truncation=True).to(device)
        gen    = model.generate(**inputs, early_stopping=True, **gen_kwargs)
        out.append(tokenizer.decode(gen[0], skip_special_tokens=True))
        if progress_callback:
            progress_callback(i, total)
    return " ".join(out)

def translate_text(text: str, target_lang: str) -> str:
    return translate(text, target_lang)
