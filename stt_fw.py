from faster_whisper import WhisperModel


class FasterWhisperSTT:
    def __init__(
        self,
        model_name: str = "base",
        device: str = "cuda",           # "cuda" ou "cpu"
        compute_type: str = "float16",  # "float16" (CUDA), "int8" (CPU) etc.
        language="en",

    ):
        self.model = WhisperModel(model_name, device=device, compute_type=compute_type)

    def transcribe(self, wav_path: str, language: str = "en") -> str:
        segments, info = self.model.transcribe(wav_path, language=language)
        return " ".join(s.text.strip() for s in segments).strip()