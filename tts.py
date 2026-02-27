# tts.py
import threading
import pyttsx3
import time

class TTS:
    def __init__(self, rate: int = 175, volume: float = 1.0, voice_contains: str | None = None):
        self.rate = rate
        self.volume = volume
        self.voice_contains = voice_contains
        self._lock = threading.Lock()
        self._is_speaking = False

    @property
    def is_speaking(self) -> bool:
        return self._is_speaking

    def _make_engine(self):
        eng = pyttsx3.init()
        eng.setProperty("rate", self.rate)
        eng.setProperty("volume", self.volume)

        if self.voice_contains:
            target = self.voice_contains.lower()
            for v in eng.getProperty("voices"):
                name = (getattr(v, "name", "") or "").lower()
                vid = (getattr(v, "id", "") or "").lower()
                if target in name or target in vid:
                    eng.setProperty("voice", v.id)
                    break
        return eng

    def speak_blocking(self, text: str):
        with self._lock:
            self._is_speaking = True
            try:
                eng = self._make_engine()
                eng.say(text)
                eng.runAndWait()
                eng.stop()
            finally:
                self._is_speaking = False

    def speak_async(self, text: str):
        def _run():
            self.speak_blocking(text)
        threading.Thread(target=_run, daemon=True).start()

    def speak(self, text: str, timeout_s: float = 20.0):
        # roda TTS em thread e não deixa travar o loop inteiro
        def _run():
            try:
                eng = self._make_engine()
                eng.say(text)
                eng.runAndWait()
                eng.stop()
            except Exception:
                pass

        with self._lock:
            th = threading.Thread(target=_run, daemon=True)
            th.start()
            th.join(timeout=timeout_s)
            # se travar, a thread morre “sozinha” (daemon) e seu loop segue vivo