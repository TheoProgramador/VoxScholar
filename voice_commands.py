import re

# padrões simples e bem específicos (evita falso positivo)
CHAT_PATTERNS = [
    r"\b(chat mode)\b",
    r"\b(conversation mode)\b",
    r"\b(free talk)\b",
    r"\b(let's just talk)\b",
    r"\b(switch to chat)\b",
    r"\b(go back to chat)\b",
]

STRICT_PATTERNS = [
    r"\b(strict mode)\b",
    r"\b(trainer mode)\b",
    r"\b(correction mode)\b",
    r"\b(be strict)\b",
    r"\b(correct me strictly)\b",
    r"\b(switch to strict)\b",
    r"\b(enable strict)\b",
]


BEGINNER_PATTERNS = [
    r"\b(beginner mode)\b",
    r"\b(duolingo mode)\b",
    r"\b(english for beginners)\b",
    r"\b(beginner english teacher)\b",
    r"\b(switch to beginner)\b",
    r"\b(enable beginner mode)\b",
]

RESET_PATTERNS = [
    r"\b(reset context)\b",
    r"\b(reset conversation)\b",
    r"\b(clear context)\b",
    r"\b(clear conversation)\b",
]

QUIT_PATTERNS = [
    r"\b(quit)\b",
    r"\b(exit)\b",
    r"\b(stop)\b",
    r"\b(shut down)\b",
]

def detect_command(text: str) -> str | None:
    """
    Retorna: "chat" | "strict" | "beginner" | "reset" | "quit" | None
    """
    t = text.lower().strip()
    t = re.sub(r"\s+", " ", t)

    def matches(patterns: list[str]) -> bool:
        return any(re.search(p, t) for p in patterns)

    if matches(QUIT_PATTERNS):
        return "quit"
    if matches(RESET_PATTERNS):
        return "reset"
    if matches(STRICT_PATTERNS):
        return "strict"
    if matches(CHAT_PATTERNS):
        return "chat"
    if matches(BEGINNER_PATTERNS):
        return "beginner"
    return None