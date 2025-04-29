import re

def simplify_text(text: str, max_len: int = 2000) -> str:
    clean = re.sub(r'\s+', ' ', text).strip()
    return clean[:max_len]
