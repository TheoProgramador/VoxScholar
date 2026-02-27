import collections
import queue
import time
import wave

import numpy as np
import sounddevice as sd
import webrtcvad


class VADRecorder:
    """
    Grava do microfone e encerra automaticamente ao detectar silêncio por um tempo.
    Usa webrtcvad (bem melhor que RMS puro).
    """
    def __init__(
        self,
        sample_rate: int = 16000,
        frame_ms: int = 30,           # 10/20/30
        vad_mode: int = 2,            # 0..3 (3 mais agressivo)
        pre_speech_ms: int = 300,
        silence_ms: int = 1100,
        max_record_s: int = 25,
        input_device: int | None = None,
    ):
        if frame_ms not in (10, 20, 30):
            raise ValueError("frame_ms deve ser 10, 20 ou 30 (webrtcvad).")

        self.sample_rate = sample_rate
        self.frame_ms = frame_ms
        self.frame_samples = int(sample_rate * frame_ms / 1000)

        self.vad = webrtcvad.Vad(vad_mode)
        self.pre_speech_frames = max(1, int(pre_speech_ms / frame_ms))
        self.silence_frames_needed = max(1, int(silence_ms / frame_ms))
        self.max_frames = max(1, int((max_record_s * 1000) / frame_ms))

        self.input_device = input_device
        self._q: "queue.Queue[bytes]" = queue.Queue()

    def _callback(self, indata, frames, time_info, status):
        # float32 [-1,1] -> int16 PCM
        pcm16 = (indata[:, 0] * 32767).astype(np.int16).tobytes()
        self._q.put(pcm16)

    def record_utterance(self, wav_path: str = "utterance.wav") -> tuple[str | None, float]:
        """
        Retorna (wav_path, duration_s). Se não detectar fala, (None, 0).
        """
        self._drain_queue()

        ring = collections.deque(maxlen=self.pre_speech_frames)
        voiced: list[bytes] = []
        triggered = False
        silence_count = 0

        with sd.InputStream(
            channels=1,
            samplerate=self.sample_rate,
            blocksize=self.frame_samples,
            dtype="float32",
            callback=self._callback,
            device=self.input_device,
        ):
            start_time = time.time()
            frames_captured = 0

            while frames_captured < self.max_frames:
                try:
                    frame = self._q.get(timeout=1.0)
                except queue.Empty:
                    # sem áudio chegando e ainda não começou fala
                    if (time.time() - start_time) > 3.0 and not triggered:
                        return (None, 0.0)
                    continue

                frames_captured += 1
                is_speech = self.vad.is_speech(frame, self.sample_rate)

                if not triggered:
                    ring.append(frame)
                    if is_speech:
                        triggered = True
                        voiced.extend(ring)
                        ring.clear()
                        silence_count = 0
                else:
                    voiced.append(frame)
                    if is_speech:
                        silence_count = 0
                    else:
                        silence_count += 1
                        if silence_count >= self.silence_frames_needed:
                            break

        if not voiced:
            return (None, 0.0)

        self._write_wav(wav_path, voiced)
        duration_s = (len(voiced) * self.frame_samples) / self.sample_rate
        return (wav_path, duration_s)

    def _write_wav(self, path: str, frames_bytes: list[bytes]) -> None:
        with wave.open(path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # int16
            wf.setframerate(self.sample_rate)
            wf.writeframes(b"".join(frames_bytes))

    def _drain_queue(self) -> None:
        while True:
            try:
                self._q.get_nowait()
            except queue.Empty:
                break