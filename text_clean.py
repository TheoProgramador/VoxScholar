import re

def clean_for_tts(text: str) -> str:
    # remove restos de markdown caso escapem (defensivo)
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"^\s*-\s*", "", text, flags=re.MULTILINE)

    # normaliza espaços
    text = re.sub(r"[ \t]+", " ", text).strip()
    return text