import re

_WORD = re.compile(r"[a-zA-Z0-9]+(?:'[a-z0-9]+)?")  # words and simple contractions

def tokenize(text: str):
    text = text.lower()
    return _WORD.findall(text)
